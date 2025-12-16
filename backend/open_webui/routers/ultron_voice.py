"""
ULTRON Voice Router - Voice Input/Output Integration
Handles TTS (pyttsx3, ElevenLabs) and STT (SpeechRecognition)
Linux-compatible voice features for ARMORY
"""

import logging
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
from io import BytesIO

from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user
from open_webui.config import WEBUI_NAME

log = logging.getLogger(__name__)
router = APIRouter()


class VoiceSettings(BaseModel):
    """Voice configuration settings"""
    tts_engine: str = "pyttsx3"  # pyttsx3, elevenlabs
    tts_voice: Optional[str] = None
    tts_rate: int = 150
    tts_volume: float = 1.0
    stt_engine: str = "google"  # google, whisper
    language: str = "en-US"
    elevenlabs_api_key: Optional[str] = None
    elevenlabs_voice_id: Optional[str] = None


class TTSRequest(BaseModel):
    """Text-to-speech request"""
    text: str
    engine: Optional[str] = None
    voice: Optional[str] = None
    rate: Optional[int] = None


class STTResponse(BaseModel):
    """Speech-to-text response"""
    text: str
    confidence: Optional[float] = None
    language: str


class UltronVoiceManager:
    """Manages voice input/output on Linux"""
    
    def __init__(self):
        self.settings = VoiceSettings()
        self.tts_engine = None
        self.stt_recognizer = None
        self._initialize_engines()
    
    def _initialize_engines(self):
        """Initialize voice engines with Linux compatibility"""
        # Initialize TTS (pyttsx3 works on Linux with espeak)
        try:
            import pyttsx3
            self.tts_engine = pyttsx3.init(driverName='espeak')
            self.tts_engine.setProperty('rate', self.settings.tts_rate)
            self.tts_engine.setProperty('volume', self.settings.tts_volume)
            log.info("pyttsx3 TTS engine initialized with espeak")
        except Exception as e:
            log.error(f"Failed to initialize TTS engine: {e}")
            self.tts_engine = None
        
        # Initialize STT (SpeechRecognition with pyaudio)
        try:
            import speech_recognition as sr
            self.stt_recognizer = sr.Recognizer()
            log.info("SpeechRecognition STT engine initialized")
        except Exception as e:
            log.error(f"Failed to initialize STT engine: {e}")
            self.stt_recognizer = None
    
    async def text_to_speech(self, text: str, engine: Optional[str] = None) -> bytes:
        """Convert text to speech audio"""
        engine = engine or self.settings.tts_engine
        
        if engine == "pyttsx3":
            return await self._tts_pyttsx3(text)
        elif engine == "elevenlabs":
            return await self._tts_elevenlabs(text)
        else:
            raise ValueError(f"Unsupported TTS engine: {engine}")
    
    async def _tts_pyttsx3(self, text: str) -> bytes:
        """Generate speech using pyttsx3"""
        if not self.tts_engine:
            raise RuntimeError("TTS engine not initialized")
        
        # Save to BytesIO buffer
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp_path = tmp.name
        
        try:
            # Run in thread pool since pyttsx3 is blocking
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(
                None,
                lambda: self._save_speech(text, tmp_path)
            )
            
            # Read audio file
            with open(tmp_path, 'rb') as f:
                audio_data = f.read()
            
            return audio_data
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def _save_speech(self, text: str, path: str):
        """Helper to save speech to file"""
        self.tts_engine.save_to_file(text, path)
        self.tts_engine.runAndWait()
    
    async def _tts_elevenlabs(self, text: str) -> bytes:
        """Generate speech using ElevenLabs"""
        if not self.settings.elevenlabs_api_key:
            raise ValueError("ElevenLabs API key not configured")
        
        import httpx
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{self.settings.elevenlabs_voice_id or 'default'}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                url,
                headers={
                    "xi-api-key": self.settings.elevenlabs_api_key,
                    "Content-Type": "application/json"
                },
                json={
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": {
                        "stability": 0.5,
                        "similarity_boost": 0.5
                    }
                }
            )
            response.raise_for_status()
            return response.content
    
    async def speech_to_text(self, audio_file: BytesIO, engine: Optional[str] = None) -> STTResponse:
        """Convert speech audio to text"""
        if not self.stt_recognizer:
            raise RuntimeError("STT engine not initialized")
        
        engine = engine or self.settings.stt_engine
        
        import speech_recognition as sr
        
        # Save to temp WAV file
        import tempfile
        import os
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as tmp:
            tmp.write(audio_file.read())
            tmp_path = tmp.name
        
        try:
            # Load audio file
            with sr.AudioFile(tmp_path) as source:
                audio = self.stt_recognizer.record(source)
            
            # Recognize speech
            loop = asyncio.get_event_loop()
            
            if engine == "google":
                text = await loop.run_in_executor(
                    None,
                    lambda: self.stt_recognizer.recognize_google(audio, language=self.settings.language)
                )
            elif engine == "whisper":
                text = await loop.run_in_executor(
                    None,
                    lambda: self.stt_recognizer.recognize_whisper(audio, language=self.settings.language.split('-')[0])
                )
            else:
                raise ValueError(f"Unsupported STT engine: {engine}")
            
            return STTResponse(
                text=text,
                confidence=None,  # Most engines don't provide confidence
                language=self.settings.language
            )
        
        except sr.UnknownValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not understand audio"
            )
        except sr.RequestError as e:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"Speech recognition service error: {e}"
            )
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
    
    def get_available_voices(self) -> List[str]:
        """Get list of available TTS voices"""
        if not self.tts_engine:
            return []
        
        voices = self.tts_engine.getProperty('voices')
        return [voice.id for voice in voices]
    
    def set_voice(self, voice_id: str):
        """Set TTS voice"""
        if not self.tts_engine:
            raise RuntimeError("TTS engine not initialized")
        
        self.tts_engine.setProperty('voice', voice_id)
        self.settings.tts_voice = voice_id


# Initialize voice manager
voice_manager = UltronVoiceManager()


@router.get("/settings", response_model=VoiceSettings)
async def get_voice_settings(user=Depends(get_verified_user)):
    """Get current voice settings"""
    return voice_manager.settings


@router.post("/settings", response_model=VoiceSettings)
async def update_voice_settings(settings: VoiceSettings, user=Depends(get_verified_user)):
    """Update voice settings"""
    voice_manager.settings = settings
    voice_manager._initialize_engines()
    return settings


@router.get("/voices")
async def get_voices(user=Depends(get_verified_user)):
    """Get available TTS voices"""
    try:
        voices = voice_manager.get_available_voices()
        return {"voices": voices}
    except Exception as e:
        log.error(f"Failed to get voices: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/tts")
async def text_to_speech(request: TTSRequest, user=Depends(get_verified_user)):
    """Convert text to speech"""
    try:
        audio_data = await voice_manager.text_to_speech(
            text=request.text,
            engine=request.engine
        )
        
        from fastapi.responses import Response
        return Response(
            content=audio_data,
            media_type="audio/wav",
            headers={
                "Content-Disposition": "attachment; filename=speech.wav"
            }
        )
    except Exception as e:
        log.error(f"TTS failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/stt", response_model=STTResponse)
async def speech_to_text(
    audio: UploadFile = File(...),
    engine: Optional[str] = None,
    user=Depends(get_verified_user)
):
    """Convert speech to text"""
    try:
        audio_data = await audio.read()
        audio_file = BytesIO(audio_data)
        
        result = await voice_manager.speech_to_text(audio_file, engine)
        return result
    except HTTPException:
        raise
    except Exception as e:
        log.error(f"STT failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/speak")
async def speak_text(request: TTSRequest, user=Depends(get_verified_user)):
    """Speak text using system audio output"""
    try:
        if not voice_manager.tts_engine:
            raise RuntimeError("TTS engine not initialized")
        
        # Speak directly (blocking)
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(
            None,
            lambda: voice_manager.tts_engine.say(request.text) or voice_manager.tts_engine.runAndWait()
        )
        
        return {"status": "success", "message": "Text spoken successfully"}
    except Exception as e:
        log.error(f"Speak failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )
