# MiniMax AI Image Generation - Setup Guide

## Overview
Using MiniMax AI to generate HD Ultron-themed images for the interface.

## API Configuration
- **API Key**: Configured in `backend/oasis/utils/minimax_image_gen.py`
- **Group ID**: 1939265390257378238
- **Model**: text_to_image_v2
- **Resolution**: 1024x1024 (configurable)

## Generated Assets

### 1. Background (1024x1024)
- Futuristic cityscape at night
- Red glowing circuits in sky
- Cyberpunk style
- Usage: Main body background

### 2. Logo (1024x1024)
- Ultron face with glowing red eyes
- Metallic texture
- Centered composition
- Usage: Header, branding

### 3. Circuit Pattern (1024x1024)
- Abstract circuit board pattern
- Seamless tileable texture
- Red glowing lines on dark background
- Usage: Card backgrounds, overlays

### 4. Hero Banner (1024x1024)
- Ultron in futuristic city
- Red energy effects
- Dramatic lighting, wide angle
- Usage: Landing page, hero sections

### 5. Sidebar Background (1024x1024)
- Vertical circuit pattern
- Dark metallic texture
- Red accents with subtle glow
- Usage: Navigation sidebar

## How to Generate Images

### Method 1: Run Python Script
```bash
cd /home/ultro/projects/openui/oasis
python3 scripts/generate_ultron_assets.py
```

### Method 2: Use Python Module
```python
from backend.oasis.utils.minimax_image_gen import generate_all_ultron_assets

# Generate all assets
results = generate_all_ultron_assets()

# Generate single image
from backend.oasis.utils.minimax_image_gen import generate_ultron_image

image_url = generate_ultron_image(
    prompt="futuristic Ultron interface element",
    width=1024,
    height=1024,
    output_path="static/assets/ultron/custom.png"
)
```

### Method 3: Custom Prompts
```python
from backend.oasis.utils.minimax_image_gen import generate_ultron_image

# Generate custom image
generate_ultron_image(
    prompt="your custom description here",
    width=1920,
    height=1080,
    output_path="static/assets/ultron/custom_image.png"
)
```

## File Structure
```
static/
└── assets/
    └── ultron/
        ├── background.png       (Main background)
        ├── logo.png            (Ultron logo)
        ├── circuit_pattern.png (Tileable pattern)
        ├── hero_banner.png     (Hero section)
        └── sidebar_bg.png      (Sidebar background)
```

## CSS Integration

Images are automatically integrated via `ultron-images.css`:

### Body Background
```css
body {
  background-image: url('/assets/ultron/background.png');
}
```

### Logo Usage
```html
<div class="ultron-logo"></div>
```

### Circuit Overlay
```html
<div class="circuit-overlay">
  <!-- Content here -->
</div>
```

### Hero Section
```html
<div class="ultron-hero">
  <h1>Welcome to Ultron</h1>
</div>
```

## Customization

### Change Image Prompts
Edit `ULTRON_IMAGES` dictionary in `minimax_image_gen.py`:
```python
ULTRON_IMAGES = {
    "background": "your custom prompt here",
    "logo": "your custom logo prompt",
    # ... add more
}
```

### Adjust Resolution
```python
generate_ultron_image(
    prompt="...",
    width=1920,  # Custom width
    height=1080  # Custom height
)
```

### Add New Images
```python
generate_ultron_image(
    prompt="Ultron themed button background",
    width=512,
    height=128,
    output_path="static/assets/ultron/button_bg.png"
)
```

## API Limits & Costs
- Check MiniMax documentation for rate limits
- Monitor API usage in MiniMax dashboard
- Images are cached locally after generation

## Troubleshooting

### Images Not Generating
1. Check API key is valid
2. Verify internet connection
3. Check MiniMax API status
4. Review logs for error messages

### Images Not Displaying
1. Ensure images are in `static/assets/ultron/`
2. Check file permissions
3. Clear browser cache
4. Verify CSS import in `app.css`

### Low Quality Images
1. Increase resolution in generation call
2. Enhance prompt with quality keywords:
   - "8K quality"
   - "high detail"
   - "photorealistic"
   - "ultra HD"

## Performance Optimization

### Image Optimization
After generation, optimize images:
```bash
# Install optimization tools
npm install -g sharp-cli

# Optimize images
sharp -i static/assets/ultron/*.png -o static/assets/ultron/optimized/ --webp
```

### Lazy Loading
Images are loaded with CSS, automatically lazy-loaded by browser.

### Caching
Images are static assets, cached by browser automatically.

## Next Steps

1. **Generate Images**: Run the script to create all assets
2. **Review Output**: Check `static/assets/ultron/` directory
3. **Customize**: Adjust prompts if needed and regenerate
4. **Optimize**: Compress images for production
5. **Deploy**: Images will be served with the application

## Example: Generate Now

```bash
# Navigate to project
cd /home/ultro/projects/openui/oasis

# Create output directory
mkdir -p static/assets/ultron

# Generate all Ultron assets
python3 scripts/generate_ultron_assets.py
```

Images will be saved to `static/assets/ultron/` and automatically integrated into the theme.
