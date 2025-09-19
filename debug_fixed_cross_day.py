#!/usr/bin/env python3
"""Test the fixed cross-day moon logic."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_fixed_cross_day():
    """Test the fixed cross-day moon logic."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== Testing Fixed Cross-Day Moon Logic ===")
    
    # Get data for calculation
    day2_data = engine._get_cached_day_data(2)
    day3_data = engine._get_cached_day_data(3)
    
    print(f"Day 2 data: moonrise={day2_data['moonrise']:.3f}, moonset={day3_data['moonset']:.3f} (actually Day 3)")
    print(f"Day 3 data: moonrise={day3_data['moonrise']}, moonset={day3_data['moonset']:.3f}")
    
    # Calculate expected total duration
    moonrise_day2 = day2_data['moonrise']  # 23.283
    moonset_day3 = day3_data['moonset']    # 11.717
    total_duration = (24.0 - moonrise_day2) + moonset_day3
    print(f"Expected total duration: (24.0 - {moonrise_day2:.3f}) + {moonset_day3:.3f} = {total_duration:.3f} hours")
    print()
    
    # Test times across both days
    test_data = [
        (2, 22.0, "Day 2 - Before moonrise"),
        (2, 23.3, "Day 2 - After moonrise"),
        (2, 24.0, "Day 2 - End of day"),
        (3, 0.0, "Day 3 - Start of day"),
        (3, 6.0, "Day 3 - Morning"),
        (3, 11.7, "Day 3 - At moonset"),
        (3, 12.0, "Day 3 - After moonset"),
    ]
    
    for day, hour, description in test_data:
        engine.day_of_year = day
        engine.animation_time = hour
        
        try:
            moon_x, moon_y = engine._calculate_raw_moon_position()
            is_visible = moon_x > 0 and moon_y > 0
            
            # Calculate expected progress manually
            if day == 2 and hour >= moonrise_day2:
                expected_progress = (hour - moonrise_day2) / total_duration
            elif day == 3 and hour <= moonset_day3:
                expected_progress = ((24.0 - moonrise_day2) + hour) / total_duration
            else:
                expected_progress = None
            
            if expected_progress is not None:
                print(f"{description:<25}: {hour:04.1f}h → visible={is_visible}, expected_progress={expected_progress:.3f}")
            else:
                print(f"{description:<25}: {hour:04.1f}h → visible={is_visible}")
                
        except Exception as e:
            print(f"{description:<25}: {hour:04.1f}h → Error: {e}")

if __name__ == "__main__":
    test_fixed_cross_day()