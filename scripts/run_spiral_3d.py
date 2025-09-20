#!/usr/bin/env python3
"""
Time's Pixel - 3D Time Spiral Visualization Launcher
Launch the innovative 3D spiral visualization of temporal astronomical data.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    try:
        from src.visualizations.time_spiral_3d import TimeSpiral3D
        
        print("🌀 Starting Time's Pixel 3D Spiral Visualization...")
        print("🎮 Controls:")
        print("   WASD/Arrow Keys: Rotate view")
        print("   Mouse Wheel: Zoom in/out")
        print("   SPACE: Toggle auto-rotation")
        print("   R: Reset view")
        print("   ESC: Quit")
        print("=" * 60)
        
        app = TimeSpiral3D()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're running this script from the scripts/ directory")
        print("💡 And ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)