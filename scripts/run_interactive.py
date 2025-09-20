#!/usr/bin/env python3
"""
Time's Pixel - Interactive Visualization Launcher
Launch the interactive circular time visualization.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    try:
        from src.visualizations.interactive_visualization import InteractiveTimePixel
        
        print("🎯 Starting Time's Pixel Interactive Visualization...")
        print("🎮 Controls:")
        print("   Click and drag: Navigate through time")
        print("   Mouse wheel: Zoom timeline")
        print("   Hover: See time details")
        print("   ESC: Quit")
        print("=" * 60)
        
        app = InteractiveTimePixel()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're running this script from the scripts/ directory")
        print("💡 And ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)