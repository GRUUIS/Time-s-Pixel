#!/usr/bin/env python3
"""Test the cross-day moon logic for Day 3."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_day3_moon():
    """Test Day 3 cross-day moon visibility."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== Testing Day 3 Cross-Day Moon ===")
    engine.day_of_year = 3
    
    # Day 3 should have moonset at 11:43 but no moonrise (moon rose on Day 2)
    test_times = [0, 5, 10, 11, 11.5, 11.7, 11.8, 12, 15, 20]
    
    for hour in test_times:
        engine.animation_time = hour
        
        # Try to calculate moon position using the engine's method
        try:
            moon_x, moon_y = engine._calculate_raw_moon_position()
            is_visible = moon_x > 0 and moon_y > 0  # Check if moon is on screen
            print(f"Day 3, {hour:04.1f}h: position=({moon_x}, {moon_y}), visible={is_visible}")
        except Exception as e:
            print(f"Day 3, {hour:04.1f}h: Error calculating position: {e}")

if __name__ == "__main__":
    test_day3_moon()