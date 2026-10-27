# ARMORY Theme - Visual Enhancements

## Overview
ARMORY features a complete tactical-style visual overhaul with red circuit aesthetics, advanced animations, and a command-center interface design.

## Key Visual Features

### 🎨 Color Palette
- **Primary Red**: `#ff0000` (ARMORY Red)
- **Dark Red**: `#cc0000` / `#e60000`
- **Gold Accent**: `#cc9900` (for special elements)
- **Background**: Deep blacks (#0a0a0a, #050505) with red tints
- **Glows**: Multi-layer red glow effects for depth

### ✨ Enhanced Components

#### Buttons
- Gradient backgrounds with tactical styling
- Ripple effect on hover (expanding circle animation)
- Strong red glow on interaction
- Smooth cubic-bezier transitions
- Scale effects (1.02 on hover, 0.98 on click)

#### Cards & Panels
- Dual gradient backgrounds
- Left border accent (3px ARMORY red)
- Tactical hover effects with transform
- Backdrop blur (15px) for depth
- Inset glow effects

#### Input Fields
- Command-prompt style with `> ` prefix
- Courier New monospace font
- Enhanced border effects (left border 4px)
- Tactical glow shadows
- Smooth focus transitions

#### Chat Messages
**User Messages:**
- Right-aligned red accent border
- Gradient overlay effect
- Circuit glow shadows

**AI Messages:**
- Left-aligned bright red border
- Diamond indicator (`◆`) with pulse animation
- Distinct background gradient

#### Scrollbars
- Custom styled with red gradient thumb
- Red glow effects on hover
- Tactical border accents
- Smooth transitions

### 🎯 Special Effects

#### Circuit Grid Overlay
- Repeating grid pattern (50px intervals)
- Subtle red tint (3% opacity)
- Fixed position, non-interactive
- Adds tactical atmosphere

#### Glow Animations
**Pulse Red:**
```css
- 0%/100%: 10px glow
- 50%: 20px glow
- 2s duration, ease-in-out
```

**Progress Glow:**
- Opacity animation (0.8 → 1 → 0.8)
- 2s cycle
- Applied to progress bars

**Circuit Flow:**
- Animated gradient movement
- 3s duration
- Horizontal scanning effect

#### Hover Effects
- Icons: Scale 1.1 + 10px drop shadow
- Chat items: 3px translate + inset shadow
- Buttons: Expand ripple + lift effect
- Cards: Border intensification + slide

### 🖼️ Custom Graphics

#### ARMORY Logo
- Shield-shaped design
- Red gradient fill with glow filter
- Letter "A" in tactical font
- Circuit line decorations
- "ARMORY" text with gradient
- SVG format for scalability

### 📱 UI Enhancements

#### Navigation/Sidebar
- Dark gradient background
- Right border (2px red)
- 5px shadow with red tint
- Icon glow effects on hover

#### Model Selector
- Bold tactical styling
- 2px red border
- Tactical glow shadow
- Red-bright text color

#### Settings Panel
- Deep black background (98% opacity)
- 2px red border
- 40px glow radius
- 20px backdrop blur

#### Status Indicators
- Online/Active: Red with text shadow
- Pulsing dot animation
- 2s ease-in-out cycle

#### Context Menu
- 98% opacity black background
- 2px red border
- 30px shadow radius
- Hover: 20% red background

### 🎭 Message States

#### Error Messages
- Dark red background (20% opacity)
- 4px left border (#cc0000)
- Red-bright text (#ff6666)
- Circuit glow shadow

#### Success Messages
- Green tint (10% opacity)
- Green border (#00cc00)
- Bright green text (#66ff66)

#### Warning Messages
- Gold background (20% opacity)
- Gold border (--armory-gold)
- Gold text with glow

### 🔧 Utility Classes

#### Text Colors
- `.text-primary`: ARMORY red
- `.accent`: Gold with shadow

#### Background Colors
- `.bg-primary`: ARMORY red solid

#### Effects
- `.circuit-line`: Animated scanning line
- `.status-dot`: Pulsing indicator
- `.loading-text`: Pulsing text

### 📊 Tables
- Separate border spacing
- Red border (30% opacity)
- Header: Dark gradient + 2px red bottom
- Rows: Hover with red tint + inset shadow

### 💻 Code Blocks
- Near-black background (90% opacity)
- 3px left red accent border
- Inset + circuit glow
- Courier New font
- Red-bright syntax colors

### 🎨 Theme Files

1. **ultron.css** (Main theme)
   - Core color variables
   - Component styling
   - Animations
   - Global effects

2. **custom.css** (ARMORY enhancements)
   - Chat-specific styling
   - Tactical overlays
   - Message formatting
   - Status indicators

3. **armory-logo.svg** (Brand logo)
   - Shield design
   - Gradients + filters
   - Circuit decorations

### 🚀 Performance Optimizations
- CSS transitions use `cubic-bezier` for smooth motion
- Animations use `transform` and `opacity` (GPU-accelerated)
- Backdrop filters limited to 20px max
- Glow effects optimized with multiple shadow layers

### 🌐 Browser Compatibility
- Modern browsers (Chrome, Firefox, Edge, Safari)
- CSS Grid and Flexbox
- CSS Custom Properties (variables)
- SVG support required for logo
- Backdrop-filter support recommended

### 📝 Customization

To adjust colors, modify variables in `ultron.css`:
```css
--armory-red: #e60000;        /* Primary red */
--armory-gold: #cc9900;       /* Accent gold */
--ultron-red-bright: #ff6666; /* Bright red */
```

To adjust glow intensity:
```css
--tactical-glow: 0 0 20px rgba(255, 0, 0, 0.6);
```

### 🎯 Key Improvements Summary
1. ✅ Custom ARMORY logo with shield design
2. ✅ Enhanced button animations with ripple effects
3. ✅ Tactical card styling with transform effects
4. ✅ Command-prompt style input fields
5. ✅ Distinct user/AI message styling
6. ✅ Custom scrollbar with red gradients
7. ✅ Circuit grid background overlay
8. ✅ Multiple glow and pulse animations
9. ✅ Enhanced hover states for all interactive elements
10. ✅ Tactical status indicators
11. ✅ Gold accent color for special elements
12. ✅ Comprehensive error/success/warning styles
13. ✅ Code block tactical styling
14. ✅ Custom manifest with ARMORY branding
15. ✅ Progressive Web App support

### 🔄 Future Enhancement Ideas
- Add particle effects for background
- Implement scanline animation
- Add sound effects for interactions
- Create loading screen with ARMORY logo animation
- Add theme customizer panel
- Implement color scheme variations (blue, green)

---

**Version**: 1.0.0  
**Last Updated**: December 2025  
**Theme**: ARMORY Tactical Command Center
