#!/usr/bin/env python3
"""
Time's Pixel - Timelapse Visualization Launcher
Launch the enhanced timelapse visualization with adaptive display and viewport cropping.
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(project_root)
sys.path.insert(0, parent_dir)

if __name__ == "__main__":
    try:
        from src.visualizations.timelapse_visualization import TimeLapseVisualization
        
        print("🌅 Starting Time's Pixel Timelapse Visualization...")
        print("📺 Features: Adaptive display, 20% left viewport cropping, F11 fullscreen")
        print("🎮 Controls: Press F11 for fullscreen, ESC to quit")
        print("=" * 60)
        
        app = TimeLapseVisualization()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Make sure you're running this script from the scripts/ directory")
        print("💡 And ensure all dependencies are installed")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)