import requests
import json
import logging

log = logging.getLogger(__name__)

class MinimaxOasisGenerator:
    def __init__(self):
        self.api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJkcWlrZm94IiwiVXNlck5hbWUiOiJkcWlrZm94IiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5MzkyNjUzOTAyNTczNzgyMzgiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxOTM5MjY1MzkwMjU3Mzc4MjM4IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMTItMDggMTQ6MzI6MzEiLCJpc3MiOiJtaW5pbWF4In0.dqikfox"
        self.group_id = "1939265390257378238"
        
    def generate_oasis_image(self, prompt_type):
        prompts = {
            "cyberpunk_city": "Ultra-realistic cyberpunk cityscape with towering neon skyscrapers, holographic advertisements, flying vehicles, dark atmosphere with red and blue neon lighting, futuristic architecture, rain-soaked streets reflecting neon lights, 8K resolution",
            "ai_neural_network": "Abstract visualization of artificial intelligence neural network, glowing red nodes connected by flowing data streams, digital brain patterns, circuit board aesthetics, dark background with bright red connections, futuristic AI visualization",
            "digital_matrix": "Digital matrix code rain effect, green and red binary code falling, cyberpunk aesthetic, dark background, glowing characters, computer screen effect, high-tech visualization",
            "robot_army": "Army of advanced humanoid robots in formation, metallic chrome finish with red glowing eyes, futuristic military aesthetic, dark industrial background, dramatic lighting",
            "space_station": "Massive futuristic space station orbiting a red planet, sleek metallic design, glowing windows, solar panels, space debris, stars in background, sci-fi realism"
        }
        
        url = "https://api.minimax.chat/v1/text_to_image"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": "abab6.5-chat",
            "prompt": prompts.get(prompt_type, prompts["cyberpunk_city"]),
            "width": 1920,
            "height": 1080
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            if response.status_code == 200:
                result = response.json()
                return result.get("data", {}).get("url")
            else:
                log.error(f"MiniMax API error: {response.status_code}")
                return None
        except Exception as e:
            log.error(f"MiniMax generation error: {e}")
            return None

generator = MinimaxOasisGenerator()