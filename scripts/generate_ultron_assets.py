#!/usr/bin/env python3
"""Generate Ultron theme HD images using MiniMax AI"""

import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from backend.oasis.utils.minimax_image_gen import generate_all_ultron_assets

if __name__ == "__main__":
    print("🤖 Generating Ultron HD Assets with MiniMax AI...")
    results = generate_all_ultron_assets()
    
    print("\n✅ Generation Complete:")
    for name, path in results.items():
        status = "✓" if path else "✗"
        print(f"  {status} {name}: {path}")
