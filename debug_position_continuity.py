#!/usr/bin/env python3
"""Test moon position continuity across days."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_moon_position_continuity():
    """Test that moon position is continuous across day boundary."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== Moon Position Continuity Test ===")
    
    # Test times around day boundary
    test_times = [
        (2, 23.9, "Day 2 - 23:54 (near end)"),
        (2, 24.0, "Day 2 - 24:00 (end of day)"),
        (3, 0.0, "Day 3 - 00:00 (start of day)"),
        (3, 0.1, "Day 3 - 00:06 (just started)"),
    ]
    
    for day, hour, description in test_times:
        engine.day_of_year = day
        engine.animation_time = hour
        
        try:
            moon_x, moon_y = engine._calculate_raw_moon_position()
            is_visible = moon_x > 0 and moon_y > 0
            print(f"{description:<25}: pos=({moon_x:4d}, {moon_y:4d}), visible={is_visible}")
        except Exception as e:
            print(f"{description:<25}: Error: {e}")
    
    print()
    print("Expected behavior:")
    print("- Moon position should be continuous from Day 2 24:00 to Day 3 00:00")
    print("- No sudden jumps in position")
    print("- Moon should complete its arc only at Day 3 11:43")

if __name__ == "__main__":
    test_moon_position_continuity()