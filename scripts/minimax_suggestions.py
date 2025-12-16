#!/usr/bin/env python3
import requests
import json

class MinimaxSuggestions:
    def __init__(self):
        self.api_key = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJkcWlrZm94IiwiVXNlck5hbWUiOiJkcWlrZm94IiwiQWNjb3VudCI6IiIsIlN1YmplY3RJRCI6IjE5MzkyNjUzOTAyNTczNzgyMzgiLCJQaG9uZSI6IiIsIkdyb3VwSUQiOiIxOTM5MjY1MzkwMjU3Mzc4MjM4IiwiUGFnZU5hbWUiOiIiLCJNYWlsIjoiIiwiQ3JlYXRlVGltZSI6IjIwMjQtMTItMDggMTQ6MzI6MzEiLCJpc3MiOiJtaW5pbWF4In0.dqikfox"
        
    def get_oasis_image_suggestions(self):
        """Get AI suggestions for OASIS-themed images"""
        
        url = "https://api.minimax.chat/v1/text_to_image"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        suggestions = {
            "hero_background": "Futuristic OASIS command center with holographic displays, red neon lighting, multiple screens showing AI data streams, dark metallic surfaces, cyberpunk aesthetic, ultra-wide panoramic view",
            
            "login_background": "Secure OASIS access terminal, biometric scanner interface, red security lights, digital authentication screens, high-tech security chamber, dramatic lighting",
            
            "dashboard_bg": "OASIS control room with multiple AI agent workstations, glowing red circuit patterns on walls, holographic data visualizations, futuristic command center aesthetic",
            
            "chat_background": "AI conversation interface with flowing data streams, neural network visualizations, red glowing nodes, digital communication pathways, abstract tech background",
            
            "loading_screen": "OASIS system initialization sequence, progress bars with red loading indicators, system diagnostics displays, boot-up interface, high-tech startup screen"
        }
        
        print("🎨 OASIS Image Suggestions from MiniMax AI:")
        print("=" * 50)
        
        for name, prompt in suggestions.items():
            print(f"\n📸 {name.upper()}:")
            print(f"   Prompt: {prompt}")
            
            # Generate image URL (simulated)
            data = {
                "model": "abab6.5-chat", 
                "prompt": prompt,
                "width": 1920,
                "height": 1080
            }
            
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    result = response.json()
                    image_url = result.get("data", {}).get("url")
                    if image_url:
                        print(f"   ✅ Generated: {image_url}")
                    else:
                        print(f"   ⚠️  No URL in response")
                else:
                    print(f"   ❌ API Error: {response.status_code}")
            except Exception as e:
                print(f"   ❌ Error: {e}")
        
        return suggestions

if __name__ == "__main__":
    generator = MinimaxSuggestions()
    generator.get_oasis_image_suggestions()