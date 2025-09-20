#!/usr/bin/env python3
"""
Time's Pixel - Direct Timelapse Launcher
Direct launcher for the timelapse visualization (maintains backward compatibility)
"""

import sys
import os

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    print("🌅 Time's Pixel - Direct Timelapse Launcher")
    print("=" * 50)
    print("Launching Timelapse Animation directly...")
    print("For the full menu experience, run: python timelapse_visualization.py")
    print("=" * 50)
    print()
    
    try:
        from src.visualizations.timelapse_visualization import TimeLapseVisualization
        
        print("🚀 Starting Timelapse Visualization...")
        app = TimeLapseVisualization()
        app.run()
        
    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print("💡 Please ensure all dependencies are installed")
        print("💡 Try running from the scripts/ directory: python scripts/run_timelapse.py")
        sys.exit(1)