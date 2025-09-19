#!/usr/bin/env python3
"""Debug script to test SkyAnimationEngine initialization."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_sky_animation_engine():
    """Test SkyAnimationEngine initialization."""
    print("Testing SkyAnimationEngine initialization...")
    
    try:
        from src.visualizations.timelapse_visualization import SkyAnimationEngine
        print("Successfully imported SkyAnimationEngine")
        
        # Create an instance
        print("Creating SkyAnimationEngine instance...")
        engine = SkyAnimationEngine(1200, 800)
        
        print(f"Engine has_data: {engine.has_data}")
        if hasattr(engine, 'sun_df') and engine.sun_df is not None:
            print(f"Sun data shape: {engine.sun_df.shape}")
        if hasattr(engine, 'moon_df') and engine.moon_df is not None:
            print(f"Moon data shape: {engine.moon_df.shape}")
            
        return engine
        
    except Exception as e:
        print(f"Error creating SkyAnimationEngine: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    engine = test_sky_animation_engine()