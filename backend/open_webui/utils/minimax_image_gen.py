import os
import logging
import requests
from typing import Optional

log = logging.getLogger(__name__)

MINIMAX_API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJBbHBoYSBPbWVnYSIsIlVzZXJOYW1lIjoiQWxwaGEgT21lZ2EiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTkzOTI2NTM5MDI2NTc2Njg0NiIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5MzkyNjUzOTAyNTczNzgyMzgiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJkcWlrc3RAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTUgMTE6MTE6MzMiLCJUb2tlblR5cGUiOjQsImlzcyI6Im1pbmltYXgifQ.JhachFbS3l9nvn7xVJ0LL1y3FEfv5cuoiUF2HDSByNT3gBEHT02ZPqGjNRBzXhHtcKyAHYDpUWDcuadDFsJXcNyHwzOaKuvGJB6v49xHcWBrul_bDFeGHPo607MAsxzXig64j-gLXeWjHt-vEA7GCliGYbjhdGAZWmeLm_psbxV7L53rLCEXhOXrnf8RLaIGOvmB2pryaRlSGnbrNX-wrSBjQFkhoyJTFJCyBQ6z6t4g-_a2k03ADWWwu-UPjjTqT08TEZT35BlhIo5vCphB4GQTH2GH-vPIINe2ZP9D-SByerBwFi3AiTFXt-_iZgNTZ2-H3aXgGUHcOszQSQWJug"
MINIMAX_GROUP_ID = "1939265390257378238"


def generate_ultron_image(
    prompt: str,
    width: int = 1024,
    height: int = 1024,
    output_path: Optional[str] = None
) -> Optional[str]:
    """Generate HD Ultron-themed image using MiniMax API"""
    
    url = f"https://api.minimax.chat/v1/text_to_image?GroupId={MINIMAX_GROUP_ID}"
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "text_to_image_v2",
        "prompt": f"Ultron themed, futuristic, dark background, glowing red circuits, high detail, 8K quality: {prompt}",
        "width": width,
        "height": height
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers, timeout=60)
        response.raise_for_status()
        
        data = response.json()
        image_url = data.get("image_url")
        
        if image_url and output_path:
            img_response = requests.get(image_url, timeout=30)
            img_response.raise_for_status()
            
            os.makedirs(os.path.dirname(output_path), exist_ok=True)
            with open(output_path, "wb") as f:
                f.write(img_response.content)
            
            log.info(f"Image saved to {output_path}")
            return output_path
        
        return image_url
        
    except Exception as e:
        log.error(f"MiniMax image generation failed: {e}")
        return None


# Predefined Ultron theme images to generate
ULTRON_IMAGES = {
    "background": "futuristic cityscape at night with red glowing circuits in the sky, cyberpunk style",
    "logo": "Ultron face logo, glowing red eyes, metallic texture, centered composition",
    "circuit_pattern": "abstract circuit board pattern, red glowing lines, dark background, seamless tile",
    "hero_banner": "Ultron standing in futuristic city, red energy emanating, dramatic lighting, wide angle",
    "sidebar_bg": "vertical circuit pattern, dark metallic texture, red accents, subtle glow"
}


def generate_all_ultron_assets(output_dir: str = "static/assets/ultron"):
    """Generate all Ultron theme assets"""
    results = {}
    
    for name, prompt in ULTRON_IMAGES.items():
        output_path = os.path.join(output_dir, f"{name}.png")
        result = generate_ultron_image(prompt, output_path=output_path)
        results[name] = result
        log.info(f"Generated {name}: {result}")
    
    return results


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    generate_all_ultron_assets()
