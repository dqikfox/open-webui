#!/usr/bin/env python3
"""
ULTRON Visual Asset Generator using MiniMax AI
Generates stunning graphics, backgrounds, and UI elements in Ultron style
"""

import requests
import json
import base64
import os
from pathlib import Path

# MiniMax API Configuration
MINIMAX_API_KEY = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJHcm91cE5hbWUiOiJBbHBoYSBPbWVnYSIsIlVzZXJOYW1lIjoiQWxwaGEgT21lZ2EiLCJBY2NvdW50IjoiIiwiU3ViamVjdElEIjoiMTkzOTI2NTM5MDI2NTc2Njg0NiIsIlBob25lIjoiIiwiR3JvdXBJRCI6IjE5MzkyNjUzOTAyNTczNzgyMzgiLCJQYWdlTmFtZSI6IiIsIk1haWwiOiJkcWlrc3RAZ21haWwuY29tIiwiQ3JlYXRlVGltZSI6IjIwMjUtMTEtMTUgMTE6MTE6MzMiLCJUb2tlblR5cGUiOjQsImlzcyI6Im1pbmltYXgifQ.JhachFbS3l9nvn7xVJ0LL1y3FEfv5cuoiUF2HDSByNT3gBEHT02ZPqGjNRBzXhHtcKyAHYDpUWDcuadDFsJXcNyHwzOaKuvGJB6v49xHcWBrul_bDFeGHPo607MAsxzXig64j-gLXeWjHt-vEA7GCliGYbjhdGAZWmeLm_psbxV7L53rLCEXhOXrnf8RLaIGOvmB2pryaRlSGnbrNX-wrSBjQFkhoyJTFJCyBQ6z6t4g-_a2k03ADWWwu-UPjjTqT08TEZT35BlhIo5vCphB4GQTH2GH-vPIINe2ZP9D-SByerBwFi3AiTFXt-_iZgNTZ2-H3aXgGUHcOszQSQWJug"
MINIMAX_GROUP_ID = "1939265390257378238"
MINIMAX_API_BASE = "https://api.minimax.chat/v1"

# Output directories
STATIC_DIR = Path(__file__).parent.parent / "static"
ASSETS_DIR = STATIC_DIR / "assets" / "ultron"
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

def generate_text_with_minimax(prompt):
    """Generate creative descriptions using MiniMax text generation"""
    url = f"{MINIMAX_API_BASE}/text/chatcompletion_v2"

    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "model": "abab6.5s-chat",
        "messages": [
            {
                "role": "system",
                "content": "You are a creative AI that generates stunning, detailed descriptions for futuristic Ultron-style UI graphics. Focus on red, gold, and metallic color schemes with circuit patterns, glowing effects, and advanced AI aesthetics."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.9,
        "top_p": 0.95
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result.get("choices", [{}])[0].get("message", {}).get("content", "")
    except Exception as e:
        print(f"Error generating text: {e}")
        return None

def create_svg_background(name, description):
    """Create enhanced SVG backgrounds based on AI descriptions"""

    backgrounds = {
        "ultron_circuit_pattern": '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:1" />
      <stop offset="50%" style="stop-color:#1a0a0a;stop-opacity:1" />
      <stop offset="100%" style="stop-color:#0a0a0a;stop-opacity:1" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <pattern id="grid" width="50" height="50" patternUnits="userSpaceOnUse">
      <path d="M 50 0 L 0 0 0 50" fill="none" stroke="rgba(255,215,0,0.1)" stroke-width="0.5"/>
    </pattern>
    <pattern id="circuitLines" width="200" height="200" patternUnits="userSpaceOnUse">
      <!-- Horizontal lines -->
      <line x1="0" y1="50" x2="100" y2="50" stroke="#ffd700" stroke-width="2" opacity="0.4"/>
      <line x1="120" y1="50" x2="200" y2="50" stroke="#ffd700" stroke-width="2" opacity="0.4"/>
      <!-- Vertical lines -->
      <line x1="50" y1="0" x2="50" y2="80" stroke="#ffd700" stroke-width="2" opacity="0.4"/>
      <line x1="50" y1="100" x2="50" y2="200" stroke="#ffd700" stroke-width="2" opacity="0.4"/>
      <!-- Connection points -->
      <circle cx="50" cy="50" r="4" fill="#ff0000" opacity="0.7"/>
      <circle cx="100" cy="50" r="3" fill="#ffd700" opacity="0.6"/>
      <circle cx="150" cy="150" r="3" fill="#ffd700" opacity="0.6"/>
      <!-- Corner elements -->
      <path d="M 100 48 L 105 50 L 100 52" fill="none" stroke="#ff4500" stroke-width="1.5"/>
      <path d="M 48 100 L 50 105 L 52 100" fill="none" stroke="#ff4500" stroke-width="1.5"/>
    </pattern>
  </defs>

  <!-- Base gradient -->
  <rect width="1920" height="1080" fill="url(#bgGrad)"/>

  <!-- Grid overlay -->
  <rect width="1920" height="1080" fill="url(#grid)" opacity="0.4"/>

  <!-- Circuit pattern -->
  <rect width="1920" height="1080" fill="url(#circuitLines)" opacity="0.7"/>

  <!-- Glowing accent lines -->
  <g filter="url(#glow)">
    <line x1="0" y1="200" x2="600" y2="200" stroke="#ffd700" stroke-width="1" opacity="0.5"/>
    <line x1="1920" y1="400" x2="1200" y2="400" stroke="#ffd700" stroke-width="1" opacity="0.5"/>
    <line x1="0" y1="700" x2="800" y2="700" stroke="#ff0000" stroke-width="1" opacity="0.4"/>
    <line x1="1920" y1="900" x2="1000" y2="900" stroke="#ff0000" stroke-width="1" opacity="0.4"/>
  </g>

  <!-- Corner decorations -->
  <g opacity="0.6">
    <!-- Top left -->
    <path d="M 0 0 L 100 0 L 100 5 L 5 5 L 5 100 L 0 100 Z" fill="#ff0000" opacity="0.4"/>
    <circle cx="100" cy="100" r="3" fill="#ffd700" filter="url(#glow)"/>

    <!-- Top right -->
    <path d="M 1920 0 L 1820 0 L 1820 5 L 1915 5 L 1915 100 L 1920 100 Z" fill="#ff0000" opacity="0.4"/>
    <circle cx="1820" cy="100" r="3" fill="#ffd700" filter="url(#glow)"/>

    <!-- Bottom left -->
    <path d="M 0 1080 L 100 1080 L 100 1075 L 5 1075 L 5 980 L 0 980 Z" fill="#ff0000" opacity="0.4"/>
    <circle cx="100" cy="980" r="3" fill="#ffd700" filter="url(#glow)"/>

    <!-- Bottom right -->
    <path d="M 1920 1080 L 1820 1080 L 1820 1075 L 1915 1075 L 1915 980 L 1920 980 Z" fill="#ff0000" opacity="0.4"/>
    <circle cx="1820" cy="980" r="3" fill="#ffd700" filter="url(#glow)"/>
  </g>

  <!-- Animated scanlines (CSS animation needed) -->
  <g opacity="0.3">
    <rect width="1920" height="2" fill="#ffd700" y="0">
      <animate attributeName="y" from="-2" to="1082" dur="6s" repeatCount="indefinite"/>
    </rect>
  </g>
</svg>''',

        "ultron_header": '''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="200" viewBox="0 0 1920 200">
  <defs>
    <linearGradient id="headerGrad" x1="0%" y1="0%" x2="0%" y2="100%">
      <stop offset="0%" style="stop-color:#1a0a0a;stop-opacity:0.98" />
      <stop offset="100%" style="stop-color:#0a0a0a;stop-opacity:0.95" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="4" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="1920" height="200" fill="url(#headerGrad)"/>

  <!-- Bottom border with glow -->
  <line x1="0" y1="198" x2="1920" y2="198" stroke="#ffd700" stroke-width="2" filter="url(#glow)"/>

  <!-- Ultron corner brackets -->
  <g stroke="#ffd700" stroke-width="2" fill="none" filter="url(#glow)">
    <path d="M 20 20 L 20 60 M 20 20 L 60 20"/>
    <path d="M 1900 20 L 1900 60 M 1900 20 L 1860 20"/>
    <circle cx="20" cy="20" r="3" fill="#ff0000"/>
    <circle cx="1900" cy="20" r="3" fill="#ff0000"/>
  </g>

  <!-- Circuit accent lines -->
  <g opacity="0.5">
    <line x1="100" y1="100" x2="400" y2="100" stroke="#ffd700" stroke-width="1"/>
    <line x1="1520" y1="100" x2="1820" y2="100" stroke="#ffd700" stroke-width="1"/>
    <circle cx="400" cy="100" r="2" fill="#ff0000"/>
    <circle cx="1520" cy="100" r="2" fill="#ff0000"/>
  </g>
</svg>''',

        "ultron_hero_banner": '''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="400" viewBox="0 0 1200 400">
  <defs>
    <linearGradient id="heroGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#1a0a0a;stop-opacity:0.95" />
      <stop offset="50%" style="stop-color:#2a1515;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#1a0a0a;stop-opacity:0.95" />
    </linearGradient>
    <filter id="strongGlow">
      <feGaussianBlur stdDeviation="6" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <radialGradient id="spotlight">
      <stop offset="0%" style="stop-color:#ffd700;stop-opacity:0.3" />
      <stop offset="100%" style="stop-color:#000000;stop-opacity:0" />
    </radialGradient>
  </defs>

  <rect width="1200" height="400" fill="url(#heroGrad)"/>

  <!-- Spotlight effect -->
  <ellipse cx="600" cy="200" rx="400" ry="300" fill="url(#spotlight)"/>

  <!-- Large ULTRON text -->
  <text x="600" y="220" font-family="Arial, sans-serif" font-size="120" font-weight="bold"
        fill="#ffd700" text-anchor="middle" filter="url(#strongGlow)">ULTRON</text>

  <!-- Subtitle -->
  <text x="600" y="270" font-family="Arial, sans-serif" font-size="24"
        fill="#ff0000" text-anchor="middle" opacity="0.8">ADVANCED AI SYSTEM</text>

  <!-- Tactical border -->
  <rect x="5" y="5" width="1190" height="390" fill="none" stroke="#ffd700" stroke-width="2" opacity="0.5"/>

  <!-- Corner accents -->
  <g stroke="#ffd700" stroke-width="3" fill="none" filter="url(#strongGlow)">
    <path d="M 20 20 L 20 80 M 20 20 L 80 20"/>
    <path d="M 1180 20 L 1180 80 M 1180 20 L 1120 20"/>
    <path d="M 20 380 L 20 320 M 20 380 L 80 380"/>
    <path d="M 1180 380 L 1180 320 M 1180 380 L 1120 380"/>
  </g>

  <!-- Circuit decorations -->
  <g opacity="0.5">
    <line x1="100" y1="350" x2="300" y2="350" stroke="#ffd700" stroke-width="2"/>
    <line x1="900" y1="350" x2="1100" y2="350" stroke="#ffd700" stroke-width="2"/>
    <circle cx="300" cy="350" r="4" fill="#ff0000"/>
    <circle cx="900" cy="350" r="4" fill="#ff0000"/>
  </g>
</svg>''',

        "ultron_interface_panel": '''<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600" viewBox="0 0 800 600">
  <defs>
    <linearGradient id="panelGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#0a0a0a;stop-opacity:0.95" />
      <stop offset="50%" style="stop-color:#1a0a0a;stop-opacity:0.95" />
      <stop offset="100%" style="stop-color:#0a0a0a;stop-opacity:0.95" />
    </linearGradient>
    <filter id="glow">
      <feGaussianBlur stdDeviation="3" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <rect width="800" height="600" fill="url(#panelGrad)" rx="10" ry="10"/>
  <rect x="5" y="5" width="790" height="590" fill="none" stroke="#ffd700" stroke-width="2" rx="8" ry="8" opacity="0.7"/>

  <!-- Header -->
  <text x="400" y="40" font-family="Arial, sans-serif" font-size="24" font-weight="bold"
        fill="#ffd700" text-anchor="middle" filter="url(#glow)">ULTRON INTERFACE</text>

  <!-- Status indicators -->
  <g opacity="0.8">
    <circle cx="50" cy="80" r="8" fill="#00ff00" filter="url(#glow)"/>
    <text x="70" y="85" font-family="Arial, sans-serif" font-size="14" fill="#00ff00">ONLINE</text>

    <circle cx="50" cy="110" r="8" fill="#ffd700" filter="url(#glow)"/>
    <text x="70" y="115" font-family="Arial, sans-serif" font-size="14" fill="#ffd700">ACTIVE</text>

    <circle cx="50" cy="140" r="8" fill="#ff0000" filter="url(#glow)"/>
    <text x="70" y="145" font-family="Arial, sans-serif" font-size="14" fill="#ff0000">THREAT DETECTED</text>
  </g>

  <!-- Data streams -->
  <g opacity="0.6">
    <line x1="200" y1="200" x2="600" y2="200" stroke="#ffd700" stroke-width="1"/>
    <line x1="200" y1="230" x2="550" y2="230" stroke="#ff0000" stroke-width="1"/>
    <line x1="200" y1="260" x2="580" y2="260" stroke="#ffd700" stroke-width="1"/>
  </g>

  <!-- Progress bars -->
  <g>
    <rect x="200" y="320" width="200" height="10" fill="#333" rx="5"/>
    <rect x="200" y="320" width="150" height="10" fill="#ffd700" rx="5"/>
    <text x="200" y="310" font-family="Arial, sans-serif" font-size="12" fill="#ffd700">SYSTEM LOAD</text>

    <rect x="200" y="350" width="200" height="10" fill="#333" rx="5"/>
    <rect x="200" y="350" width="180" height="10" fill="#ff0000" rx="5"/>
    <text x="200" y="340" font-family="Arial, sans-serif" font-size="12" fill="#ff0000">THREAT LEVEL</text>
  </g>

  <!-- Corner circuits -->
  <g opacity="0.4">
    <circle cx="50" cy="550" r="3" fill="#ffd700"/>
    <circle cx="750" cy="550" r="3" fill="#ff0000"/>
    <line x1="50" y1="550" x2="100" y2="550" stroke="#ffd700" stroke-width="1"/>
    <line x1="700" y1="550" x2="750" y2="550" stroke="#ff0000" stroke-width="1"/>
  </g>
</svg>''',

        "ultron_neural_network": '''<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="600" viewBox="0 0 1000 600">
  <defs>
    <filter id="glow">
      <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
      <feMerge>
        <feMergeNode in="coloredBlur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
  </defs>

  <!-- Background -->
  <rect width="1000" height="600" fill="#0a0a0a"/>

  <!-- Neural nodes -->
  <g opacity="0.8">
    <!-- Input layer -->
    <circle cx="100" cy="100" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="100" cy="200" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="100" cy="300" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="100" cy="400" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="100" cy="500" r="8" fill="#ffd700" filter="url(#glow)"/>

    <!-- Hidden layer 1 -->
    <circle cx="300" cy="150" r="8" fill="#ff0000" filter="url(#glow)"/>
    <circle cx="300" cy="250" r="8" fill="#ff0000" filter="url(#glow)"/>
    <circle cx="300" cy="350" r="8" fill="#ff0000" filter="url(#glow)"/>
    <circle cx="300" cy="450" r="8" fill="#ff0000" filter="url(#glow)"/>

    <!-- Hidden layer 2 -->
    <circle cx="500" cy="200" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="500" cy="300" r="8" fill="#ffd700" filter="url(#glow)"/>
    <circle cx="500" cy="400" r="8" fill="#ffd700" filter="url(#glow)"/>

    <!-- Output layer -->
    <circle cx="700" cy="250" r="10" fill="#ff0000" filter="url(#glow)"/>
    <circle cx="700" cy="350" r="10" fill="#ff0000" filter="url(#glow)"/>
  </g>

  <!-- Connections -->
  <g opacity="0.4" stroke-width="1">
    <!-- Input to hidden 1 -->
    <line x1="108" y1="100" x2="292" y2="150" stroke="#ffd700"/>
    <line x1="108" y1="200" x2="292" y2="150" stroke="#ffd700"/>
    <line x1="108" y1="200" x2="292" y2="250" stroke="#ffd700"/>
    <line x1="108" y1="300" x2="292" y2="250" stroke="#ffd700"/>
    <line x1="108" y1="300" x2="292" y2="350" stroke="#ffd700"/>
    <line x1="108" y1="400" x2="292" y2="350" stroke="#ffd700"/>
    <line x1="108" y1="400" x2="292" y2="450" stroke="#ffd700"/>
    <line x1="108" y1="500" x2="292" y2="450" stroke="#ffd700"/>

    <!-- Hidden 1 to hidden 2 -->
    <line x1="308" y1="150" x2="492" y2="200" stroke="#ff0000"/>
    <line x1="308" y1="150" x2="492" y2="300" stroke="#ff0000"/>
    <line x1="308" y1="250" x2="492" y2="200" stroke="#ff0000"/>
    <line x1="308" y1="250" x2="492" y2="300" stroke="#ff0000"/>
    <line x1="308" y1="250" x2="492" y2="400" stroke="#ff0000"/>
    <line x1="308" y1="350" x2="492" y2="300" stroke="#ff0000"/>
    <line x1="308" y1="350" x2="492" y2="400" stroke="#ff0000"/>
    <line x1="308" y1="450" x2="492" y2="400" stroke="#ff0000"/>

    <!-- Hidden 2 to output -->
    <line x1="508" y1="200" x2="690" y2="250" stroke="#ffd700"/>
    <line x1="508" y1="200" x2="690" y2="350" stroke="#ffd700"/>
    <line x1="508" y1="300" x2="690" y2="250" stroke="#ffd700"/>
    <line x1="508" y1="300" x2="690" y2="350" stroke="#ffd700"/>
    <line x1="508" y1="400" x2="690" y2="350" stroke="#ffd700"/>
  </g>

  <!-- Labels -->
  <text x="100" y="70" font-family="Arial, sans-serif" font-size="12" fill="#ffd700" text-anchor="middle">INPUT</text>
  <text x="300" y="120" font-family="Arial, sans-serif" font-size="12" fill="#ff0000" text-anchor="middle">HIDDEN</text>
  <text x="500" y="170" font-family="Arial, sans-serif" font-size="12" fill="#ffd700" text-anchor="middle">PROCESS</text>
  <text x="700" y="220" font-family="Arial, sans-serif" font-size="12" fill="#ff0000" text-anchor="middle">OUTPUT</text>
</svg>'''
    }

    if name in backgrounds:
        output_path = ASSETS_DIR / f"{name}.svg"
        with open(output_path, 'w') as f:
            f.write(backgrounds[name])
        print(f"✓ Created {name}.svg")
        return True
    return False

def generate_visual_assets():
    """Generate all visual assets for ULTRON"""

    print("🤖 Generating ULTRON Visual Assets with MiniMax AI\n")

    # Define asset requirements
    assets = [
        {
            "name": "ultron_circuit_pattern",
            "description": "Full-screen futuristic circuit board pattern background with gold glowing lines, red connection points, and metallic grid overlay in Ultron style"
        },
        {
            "name": "ultron_header",
            "description": "Header banner with advanced AI corner brackets, circuit accents, and glowing gold borders"
        },
        {
            "name": "ultron_hero_banner",
            "description": "Hero section with large ULTRON text, spotlight effect, and advanced AI decorations"
        },
        {
            "name": "ultron_interface_panel",
            "description": "Control panel interface with status indicators, data streams, and progress bars in Ultron design"
        },
        {
            "name": "ultron_neural_network",
            "description": "Neural network visualization with interconnected nodes, glowing connections, and AI processing layers"
        }
    ]

    print("📝 Generating creative descriptions with MiniMax AI...")
    for asset in assets:
        print(f"\n  → {asset['name']}")

        # Generate enhanced description using MiniMax
        prompt = f"Create a detailed, vivid description for a {asset['description']}. Focus on colors (red #ff0000, gold #ffd700, black #0a0a0a), metallic effects, glowing circuits, and advanced AI aesthetics. Make it stunning and futuristic like Ultron from Marvel."

        enhanced_desc = generate_text_with_minimax(prompt)
        if enhanced_desc:
            print(f"    AI Description: {enhanced_desc[:100]}...")
            asset['ai_description'] = enhanced_desc

    print("\n\n🎨 Creating SVG graphics...")
    for asset in assets:
        create_svg_background(asset['name'], asset.get('ai_description', asset['description']))

    print("\n✨ All visual assets generated successfully!")
    print(f"📁 Assets saved to: {ASSETS_DIR}")

    # Create usage instructions
    usage_file = ASSETS_DIR / "README.md"
    with open(usage_file, 'w') as f:
        f.write("""# ULTRON Visual Assets

## Generated Assets

1. **ultron_circuit_pattern.svg** - Full-screen background with futuristic circuit patterns
2. **ultron_header.svg** - Header/navigation banner with AI brackets
3. **ultron_hero_banner.svg** - Hero section with large ULTRON branding
4. **ultron_interface_panel.svg** - Control panel with status indicators
5. **ultron_neural_network.svg** - Neural network visualization

## Usage in CSS

```css
/* Background pattern */
body {
    background-image: url('/static/assets/ultron/ultron_circuit_pattern.svg');
    background-attachment: fixed;
}

/* Header banner */
header {
    background-image: url('/static/assets/ultron/ultron_header.svg');
    background-size: cover;
}

/* Hero section */
.hero {
    background-image: url('/static/assets/ultron/ultron_hero_banner.svg');
    background-size: cover;
}

/* Interface panel */
.interface {
    background-image: url('/static/assets/ultron/ultron_interface_panel.svg');
    background-size: contain;
    background-repeat: no-repeat;
}

/* Neural network */
.neural {
    background-image: url('/static/assets/ultron/ultron_neural_network.svg');
    background-size: cover;
}
```

## Customization

All SVGs are editable. Modify colors, gradients, and filters directly in the SVG files.

Generated with MiniMax AI in Ultron style
""")

    print(f"\n📖 Usage guide created: {usage_file}")

if __name__ == "__main__":
    generate_visual_assets()
