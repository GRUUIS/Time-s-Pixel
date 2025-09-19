#!/usr/bin/env python3
"""Test moon visibility at specific times on day 2."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_moon_times():
    """Test moon visibility at different times on day 2."""
    engine = SkyAnimationEngine(1200, 800)
    
    print(f"Engine has_data: {engine.has_data}")
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    # Test different times on day 2
    engine.day_of_year = 2
    test_times = [18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 23.2, 23.3, 24.0]
    
    for hour in test_times:
        engine.animation_time = hour
        
        # Get day data
        day_data = engine._get_cached_day_data(2)
        if day_data:
            moonrise = day_data['moonrise']
            moonset = day_data['moonset']
            
            # Check visibility
            is_visible, progress = engine._calculate_moon_visibility(hour, moonrise, moonset)
            
            print(f"Time {hour:05.1f}h: moonrise={moonrise:.3f}, moonset={moonset:.3f}, visible={is_visible}")
        else:
            print(f"Time {hour:05.1f}h: No day data")

if __name__ == "__main__":
    test_moon_times()