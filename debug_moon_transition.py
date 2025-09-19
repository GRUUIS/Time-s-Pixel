#!/usr/bin/env python3
"""Test the complete Day 2 to Day 3 moon transition."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_moon_transition():
    """Test moon transition from Day 2 to Day 3."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== Day 2 to Day 3 Moon Transition ===")
    
    # Test times around the transition
    test_data = [
        (2, 22.0, "Day 2 - Before moonrise"),
        (2, 23.0, "Day 2 - Before moonrise"), 
        (2, 23.3, "Day 2 - After moonrise"),
        (2, 24.0, "Day 2 - End of day"),
        (3, 0.0, "Day 3 - Start of day"),
        (3, 5.0, "Day 3 - Early morning"),
        (3, 11.0, "Day 3 - Before moonset"),
        (3, 11.8, "Day 3 - After moonset"),
    ]
    
    for day, hour, description in test_data:
        engine.day_of_year = day
        engine.animation_time = hour
        
        try:
            moon_x, moon_y = engine._calculate_raw_moon_position()
            is_visible = moon_x > 0 and moon_y > 0
            print(f"{description:<25}: Day {day}, {hour:04.1f}h → position=({moon_x:4d}, {moon_y:4d}), visible={is_visible}")
        except Exception as e:
            print(f"{description:<25}: Day {day}, {hour:04.1f}h → Error: {e}")

if __name__ == "__main__":
    test_moon_transition()