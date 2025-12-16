"""
ULTRON Vision Router - Computer Vision & OCR Integration
Handles screenshot analysis, OCR with tesseract, image processing with OpenCV
Linux-compatible vision features for ARMORY
"""

import logging
import asyncio
from typing import Optional, List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from pydantic import BaseModel, Field
import base64
from io import BytesIO

from open_webui.models.users import Users
from open_webui.utils.auth import get_verified_user
from open_webui.config import WEBUI_NAME

log = logging.getLogger(__name__)
router = APIRouter()


class OCRRequest(BaseModel):
    """OCR request model"""
    image_base64: Optional[str] = None
    language: str = "eng"
    psm: int = 3  # Page segmentation mode


class OCRResponse(BaseModel):
    """OCR response model"""
    text: str
    confidence: Optional[float] = None
    language: str


class ImageAnalysisRequest(BaseModel):
    """Image analysis request"""
    image_base64: str
    task: str = "describe"  # describe, detect, classify
    model: Optional[str] = None


class ImageAnalysisResponse(BaseModel):
    """Image analysis response"""
    description: str
    objects: Optional[List[Dict[str, Any]]] = None
    labels: Optional[List[str]] = None


class ScreenshotRequest(BaseModel):
    """Screenshot capture request"""
    region: Optional[Dict[str, int]] = None  # x, y, width, height
    monitor: int = 0


class UltronVisionManager:
    """Manages computer vision and OCR on Linux"""
    
    def __init__(self):
        self.tesseract_available = False
        self.opencv_available = False
        self._check_dependencies()
    
    def _check_dependencies(self):
        """Check if required libraries are available"""
        try:
            import pytesseract
            self.tesseract_available = True
            log.info("Tesseract OCR is available")
        except ImportError:
            log.warning("pytesseract not installed")
        
        try:
            import cv2
            self.opencv_available = True
            log.info("OpenCV is available")
        except ImportError:
            log.warning("opencv-python not installed")
    
    async def perform_ocr(self, image_data: bytes, language: str = "eng", psm: int = 3) -> OCRResponse:
        """Perform OCR on image"""
        if not self.tesseract_available:
            raise RuntimeError("Tesseract OCR not available. Install with: pip install pytesseract")
        
        import pytesseract
        from PIL import Image
        
        # Load image
        image = Image.open(BytesIO(image_data))
        
        # Configure tesseract
        custom_config = f'--oem 3 --psm {psm}'
        
        # Run OCR in thread pool
        loop = asyncio.get_event_loop()
        text = await loop.run_in_executor(
            None,
            lambda: pytesseract.image_to_string(image, lang=language, config=custom_config)
        )
        
        # Get confidence if available
        try:
            data = await loop.run_in_executor(
                None,
                lambda: pytesseract.image_to_data(image, lang=language, config=custom_config, output_type=pytesseract.Output.DICT)
            )
            # Calculate average confidence
            confidences = [float(c) for c in data['conf'] if c != '-1']
            avg_confidence = sum(confidences) / len(confidences) if confidences else None
        except:
            avg_confidence = None
        
        return OCRResponse(
            text=text.strip(),
            confidence=avg_confidence,
            language=language
        )
    
    async def capture_screenshot(self, region: Optional[Dict[str, int]] = None, monitor: int = 0) -> bytes:
        """Capture screenshot on Linux"""
        try:
            import mss
            from PIL import Image
        except ImportError:
            raise RuntimeError("mss library not installed. Install with: pip install mss")
        
        loop = asyncio.get_event_loop()
        
        def _capture():
            with mss.mss() as sct:
                if region:
                    # Capture specific region
                    monitor_data = {
                        "top": region["y"],
                        "left": region["x"],
                        "width": region["width"],
                        "height": region["height"]
                    }
                else:
                    # Capture entire monitor
                    monitor_data = sct.monitors[monitor]
                
                screenshot = sct.grab(monitor_data)
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                
                # Save to BytesIO
                buf = BytesIO()
                img.save(buf, format='PNG')
                buf.seek(0)
                return buf.getvalue()
        
        return await loop.run_in_executor(None, _capture)
    
    async def analyze_image(self, image_data: bytes, task: str = "describe") -> ImageAnalysisResponse:
        """Analyze image using OpenCV and AI"""
        if not self.opencv_available:
            raise RuntimeError("OpenCV not available. Install with: pip install opencv-python")
        
        import cv2
        import numpy as np
        from PIL import Image
        
        # Load image
        image = Image.open(BytesIO(image_data))
        img_array = np.array(image)
        
        # Convert RGB to BGR for OpenCV
        if len(img_array.shape) == 3:
            img_bgr = cv2.cvtColor(img_array, cv2.COLOR_RGB2BGR)
        else:
            img_bgr = img_array
        
        loop = asyncio.get_event_loop()
        
        if task == "detect":
            # Object detection (simple edge detection for demo)
            def _detect():
                gray = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 50, 150)
                contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
                
                objects = []
                for i, contour in enumerate(contours[:10]):  # Limit to 10 objects
                    x, y, w, h = cv2.boundingRect(contour)
                    objects.append({
                        "id": i,
                        "bbox": {"x": int(x), "y": int(y), "width": int(w), "height": int(h)},
                        "confidence": 0.8
                    })
                
                return ImageAnalysisResponse(
                    description=f"Detected {len(objects)} objects",
                    objects=objects,
                    labels=None
                )
            
            return await loop.run_in_executor(None, _detect)
        
        elif task == "classify":
            # Image classification (simple color analysis)
            def _classify():
                # Calculate dominant colors
                pixels = img_bgr.reshape(-1, 3)
                avg_color = pixels.mean(axis=0)
                
                # Simple classification based on dominant color
                b, g, r = avg_color
                if r > g and r > b:
                    label = "red-tinted"
                elif g > r and g > b:
                    label = "green-tinted"
                elif b > r and b > g:
                    label = "blue-tinted"
                else:
                    label = "neutral"
                
                return ImageAnalysisResponse(
                    description=f"Image classified as {label}",
                    objects=None,
                    labels=[label, f"avg_color_rgb({int(r)},{int(g)},{int(b)})"]
                )
            
            return await loop.run_in_executor(None, _classify)
        
        else:  # describe
            # Image description (basic stats)
            height, width = img_bgr.shape[:2]
            channels = img_bgr.shape[2] if len(img_bgr.shape) == 3 else 1
            
            return ImageAnalysisResponse(
                description=f"Image size: {width}x{height}, channels: {channels}",
                objects=None,
                labels=[f"resolution_{width}x{height}", f"channels_{channels}"]
            )
    
    async def extract_text_from_screen(self, region: Optional[Dict[str, int]] = None) -> str:
        """Capture screenshot and perform OCR"""
        screenshot = await self.capture_screenshot(region)
        ocr_result = await self.perform_ocr(screenshot)
        return ocr_result.text


# Initialize vision manager
vision_manager = UltronVisionManager()


@router.get("/status")
async def get_vision_status(user=Depends(get_verified_user)):
    """Get vision subsystem status"""
    return {
        "tesseract_available": vision_manager.tesseract_available,
        "opencv_available": vision_manager.opencv_available,
        "screenshot_available": True  # mss works on Linux
    }


@router.post("/ocr", response_model=OCRResponse)
async def perform_ocr(
    image: UploadFile = File(...),
    language: str = "eng",
    psm: int = 3,
    user=Depends(get_verified_user)
):
    """Perform OCR on uploaded image"""
    try:
        image_data = await image.read()
        result = await vision_manager.perform_ocr(image_data, language, psm)
        return result
    except Exception as e:
        log.error(f"OCR failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/ocr/base64", response_model=OCRResponse)
async def perform_ocr_base64(request: OCRRequest, user=Depends(get_verified_user)):
    """Perform OCR on base64-encoded image"""
    try:
        if not request.image_base64:
            raise ValueError("image_base64 is required")
        
        image_data = base64.b64decode(request.image_base64)
        result = await vision_manager.perform_ocr(image_data, request.language, request.psm)
        return result
    except Exception as e:
        log.error(f"OCR failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/screenshot")
async def capture_screenshot(request: ScreenshotRequest, user=Depends(get_verified_user)):
    """Capture screenshot"""
    try:
        screenshot_data = await vision_manager.capture_screenshot(
            region=request.region,
            monitor=request.monitor
        )
        
        # Return as base64
        screenshot_base64 = base64.b64encode(screenshot_data).decode('utf-8')
        
        return {
            "image_base64": screenshot_base64,
            "format": "png"
        }
    except Exception as e:
        log.error(f"Screenshot failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/analyze", response_model=ImageAnalysisResponse)
async def analyze_image(
    image: UploadFile = File(...),
    task: str = "describe",
    user=Depends(get_verified_user)
):
    """Analyze uploaded image"""
    try:
        image_data = await image.read()
        result = await vision_manager.analyze_image(image_data, task)
        return result
    except Exception as e:
        log.error(f"Image analysis failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.post("/screen/ocr")
async def screen_ocr(request: ScreenshotRequest, user=Depends(get_verified_user)):
    """Capture screenshot and perform OCR"""
    try:
        text = await vision_manager.extract_text_from_screen(request.region)
        return {"text": text}
    except Exception as e:
        log.error(f"Screen OCR failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )


@router.get("/languages")
async def get_ocr_languages(user=Depends(get_verified_user)):
    """Get available OCR languages"""
    try:
        import pytesseract
        
        loop = asyncio.get_event_loop()
        langs = await loop.run_in_executor(
            None,
            lambda: pytesseract.get_languages()
        )
        
        return {"languages": langs}
    except Exception as e:
        log.error(f"Failed to get languages: {e}")
        return {"languages": ["eng"]}  # Default fallback
