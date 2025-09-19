#!/usr/bin/env python3
"""Test sun visibility precisely around sunrise/sunset times."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_precise_sun_times():
    """Test sun visibility precisely around sunrise and sunset."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    # Test day 2 (January 2nd)
    engine.day_of_year = 2
    day_data = engine._get_cached_day_data(2)
    
    if not day_data:
        print("No day data for day 2")
        return
    
    sunrise = day_data['sunrise']
    sunset = day_data['sunset']
    
    print(f"Day 2 - Sunrise: {sunrise:.3f} ({int(sunrise)}:{int((sunrise % 1) * 60):02d})")
    print(f"Day 2 - Sunset: {sunset:.3f} ({int(sunset)}:{int((sunset % 1) * 60):02d})")
    print()
    
    # Test times around sunrise
    test_times = [
        sunrise - 0.1,  # 6 minutes before sunrise
        sunrise - 0.05, # 3 minutes before sunrise
        sunrise,        # exact sunrise
        sunrise + 0.05, # 3 minutes after sunrise
        sunrise + 0.1,  # 6 minutes after sunrise
        12.0,           # noon
        sunset - 0.1,   # 6 minutes before sunset
        sunset - 0.05,  # 3 minutes before sunset
        sunset,         # exact sunset
        sunset + 0.05,  # 3 minutes after sunset
        sunset + 0.1,   # 6 minutes after sunset
    ]
    
    for hour in test_times:
        engine.animation_time = hour
        
        # Check if sun should be visible
        is_daytime = sunrise <= hour <= sunset
        
        # Calculate position
        sun_x, sun_y = engine._calculate_raw_sun_position()
        
        time_str = f"{int(hour)}:{int((hour % 1) * 60):02d}"
        print(f"Time {hour:06.3f}h ({time_str}): daytime={is_daytime}, pos=({sun_x}, {sun_y})")

if __name__ == "__main__":
    test_precise_sun_times()