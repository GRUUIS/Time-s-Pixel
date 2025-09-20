#!/usr/bin/env python3
"""
Circular Cosmic Clock Display
Show the circular time visualization that was previously generated
"""

import sys
import os
import subprocess

def main():
    try:
        print("⭕ Opening Circular Cosmic Clock Visualization...")
        print("🕰️ Features: Radial time mapping, cosmic design, circular layout")
        print("=" * 60)
        
        # Get the project root and image path
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        image_path = os.path.join(project_root, "output", "images", "circular_time_visualization.png")
        viewer_script = os.path.join(project_root, "scripts", "image_viewer.py")
        
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            print("� Try running the image generation script first")
            return
        
        # Launch image viewer
        subprocess.run([sys.executable, viewer_script, image_path], cwd=project_root)
        
        print("✅ Circular cosmic clock display completed!")
        
    except Exception as e:
        print(f"❌ Error displaying circular clock: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()