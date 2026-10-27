"""NVIDIA Nemotron Nano Model Loader
Loads NVIDIA Nemotron-Nano-9B-v2 using transformers
"""
import logging
from typing import Optional, Dict, Any
import torch

log = logging.getLogger(__name__)


class NemotronLoader:
    """Load and manage NVIDIA Nemotron Nano models"""
    
    def __init__(self):
        self.model = None
        self.tokenizer = None
        self.device = self._get_device()
        self.model_name = "nvidia/NVIDIA-Nemotron-Nano-9B-v2"
        
    def _get_device(self) -> str:
        """Determine best available device"""
        if torch.cuda.is_available():
            return "cuda"
        elif torch.backends.mps.is_available():
            return "mps"
        else:
            return "cpu"
    
    def load_model(
        self,
        model_name: Optional[str] = None,
        dtype: str = "auto",
        device_map: str = "auto"
    ) -> Dict[str, Any]:
        """
        Load NVIDIA Nemotron model
        
        Args:
            model_name: HuggingFace model ID (default: nvidia/NVIDIA-Nemotron-Nano-9B-v2)
            dtype: Data type for model weights ("auto", "float16", "bfloat16", "float32")
            device_map: Device mapping strategy ("auto", "cpu", "cuda")
            
        Returns:
            Dict with model info and status
        """
        try:
            from transformers import AutoModel, AutoTokenizer
            
            model_id = model_name or self.model_name
            
            log.info(f"🚀 Loading NVIDIA Nemotron model: {model_id}")
            log.info(f"📍 Device: {self.device}")
            log.info(f"🔧 Dtype: {dtype}")
            
            # Load tokenizer
            log.info("Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(model_id)
            
            # Load model with specified dtype
            log.info("Loading model...")
            self.model = AutoModel.from_pretrained(
                model_id,
                torch_dtype=dtype if dtype != "auto" else "auto",
                device_map=device_map
            )
            
            # Move to device if not using device_map="auto"
            if device_map != "auto" and self.model is not None:
                self.model = self.model.to(self.device)
            
            log.info(f"✅ Nemotron model loaded successfully on {self.device}")
            
            return {
                "status": "success",
                "model_name": model_id,
                "device": self.device,
                "dtype": dtype,
                "parameters": self._count_parameters(),
                "loaded": True
            }
            
        except ImportError as e:
            log.error("❌ transformers library not found")
            return {
                "status": "error",
                "error": "transformers not installed",
                "message": "Install with: pip install transformers torch",
                "loaded": False
            }
        except Exception as e:
            log.error(f"❌ Error loading Nemotron model: {e}")
            return {
                "status": "error",
                "error": str(e),
                "loaded": False
            }
    
    def _count_parameters(self) -> Optional[int]:
        """Count total model parameters"""
        if self.model is None:
            return None
        try:
            return sum(p.numel() for p in self.model.parameters())
        except:
            return None
    
    def generate(
        self,
        prompt: str,
        max_length: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate text using Nemotron model
        
        Args:
            prompt: Input text prompt
            max_length: Maximum tokens to generate
            temperature: Sampling temperature
            top_p: Nucleus sampling parameter
            
        Returns:
            Dict with generated text and metadata
        """
        if self.model is None or self.tokenizer is None:
            return {
                "status": "error",
                "error": "Model not loaded. Call load_model() first."
            }
        
        try:
            from transformers import pipeline
            
            # Create text generation pipeline
            generator = pipeline(
                "text-generation",
                model=self.model,
                tokenizer=self.tokenizer,
                device=self.device if self.device != "auto" else None
            )
            
            # Generate
            outputs = generator(
                prompt,
                max_length=max_length,
                temperature=temperature,
                top_p=top_p,
                do_sample=True,
                **kwargs
            )
            
            return {
                "status": "success",
                "prompt": prompt,
                "generated_text": outputs[0]["generated_text"],
                "model": self.model_name
            }
            
        except Exception as e:
            log.error(f"Generation error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def get_embeddings(self, text: str) -> Dict[str, Any]:
        """
        Get embeddings from Nemotron model
        
        Args:
            text: Input text
            
        Returns:
            Dict with embeddings and metadata
        """
        if self.model is None or self.tokenizer is None:
            return {
                "status": "error",
                "error": "Model not loaded"
            }
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                text,
                return_tensors="pt",
                padding=True,
                truncation=True
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Get embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
                embeddings = outputs.last_hidden_state.mean(dim=1)
            
            return {
                "status": "success",
                "embeddings": embeddings.cpu().tolist(),
                "shape": list(embeddings.shape),
                "text": text
            }
            
        except Exception as e:
            log.error(f"Embedding error: {e}")
            return {
                "status": "error",
                "error": str(e)
            }
    
    def unload_model(self) -> Dict[str, str]:
        """Unload model from memory"""
        try:
            if self.model is not None:
                del self.model
                self.model = None
            if self.tokenizer is not None:
                del self.tokenizer
                self.tokenizer = None
            
            # Clear CUDA cache if using GPU
            if torch.cuda.is_available():
                torch.cuda.empty_cache()
            
            log.info("✅ Nemotron model unloaded")
            return {"status": "success", "message": "Model unloaded"}
        except Exception as e:
            return {"status": "error", "error": str(e)}
    
    def get_status(self) -> Dict[str, Any]:
        """Get current model status"""
        return {
            "loaded": self.model is not None,
            "model_name": self.model_name,
            "device": self.device,
            "tokenizer_loaded": self.tokenizer is not None,
            "parameters": self._count_parameters() if self.model else None
        }


# Global instance
nemotron_loader = NemotronLoader()
