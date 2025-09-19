#!/usr/bin/env python3
"""
Time's Pixel - Timelapse Visualization Launcher
Compatible entry point for the reorganized project structure.
"""

import sys
import os

# Add current directory to Python path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

if __name__ == "__main__":
    # Import and run the timelapse visualization
    from src.visualizations.timelapse_visualization import TimeLapseVisualization
    
    print("Starting Time's Pixel Timelapse Visualization...")
    print("Using reorganized project structure with src/ folder.")
    
    app = TimeLapseVisualization()
    app.run()