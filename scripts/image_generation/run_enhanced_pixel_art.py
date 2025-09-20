#!/usr/bin/env python3
"""
Enhanced Pixel Art Display
Show the enhanced pixel art visualization that was previously generated
"""

import sys
import os
import subprocess

def main():
    try:
        print("🎨 Opening Enhanced Pixel Art Visualization...")
        print("🖼️ Features: High-resolution output, multiple palettes, seasonal markers")
        print("=" * 60)
        
        # Get the project root and image path
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(project_root, "output", "images", "enhanced_sun_moon_365days.png")
        viewer_script = os.path.join(project_root, "scripts", "image_viewer.py")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            print("� Try running the image generation script first")
            return
        
        # Launch image viewer
        subprocess.run([sys.executable, viewer_script, image_path], cwd=project_root)
        
        print("✅ Enhanced pixel art display completed!")
        
    except Exception as e:
        print(f"❌ Error displaying enhanced pixel art: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()