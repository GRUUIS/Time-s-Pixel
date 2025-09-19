#!/usr/bin/env python3
"""Test sun visibility at specific times on day 2."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_sun_times():
    """Test sun visibility at different times on day 2."""
    engine = SkyAnimationEngine(1200, 800)
    
    print(f"Engine has_data: {engine.has_data}")
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    # Test different times on day 2
    engine.day_of_year = 2
    test_times = [5.0, 6.0, 7.0, 12.0, 16.0, 17.0, 18.0, 19.0, 20.0]
    
    for hour in test_times:
        engine.animation_time = hour
        
        # Get day data
        day_data = engine._get_cached_day_data(2)
        if day_data:
            sunrise = day_data['sunrise']
            sunset = day_data['sunset']
            
            # Check if sun should be visible
            is_daytime = sunrise <= hour <= sunset
            
            # Calculate position
            sun_x, sun_y = engine._calculate_raw_sun_position()
            
            print(f"Time {hour:05.1f}h: sunrise={sunrise:.3f}, sunset={sunset:.3f}, daytime={is_daytime}, pos=({sun_x}, {sun_y})")
        else:
            print(f"Time {hour:05.1f}h: No day data")

if __name__ == "__main__":
    test_sun_times()