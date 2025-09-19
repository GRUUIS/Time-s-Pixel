#!/usr/bin/env python3
"""Check Day 0 (Dec 31, 2023) moon data."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def check_day_0():
    """Check if there's data for day 0."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    # Check days around 0 and 1
    for day in range(-1, 5):
        print(f"\n--- Day {day} ---")
        day_data = engine._get_cached_day_data(day)
        if day_data:
            moonrise = day_data.get('moonrise')
            moonset = day_data.get('moonset')
            print(f"  moonrise: {moonrise}")
            print(f"  moonset: {moonset}")
            
            # Test if Day 1 should use previous day moon
            if day == 0:
                if moonrise is not None and moonset is not None and moonrise > moonset:
                    print(f"  Day 0 cross-day moon: rises {moonrise:.3f}, sets {moonset:.3f} (on Day 1)")
        else:
            print(f"  No data for day {day}")
    
    # Test Day 1 at early hours
    print(f"\n--- Day 1 Early Hours Test ---")
    engine.day_of_year = 1
    for hour in [0, 6, 10.5, 10.8, 11]:
        engine.animation_time = hour
        pos = engine._calculate_raw_moon_position()
        print(f"  {hour:4.1f}h: pos={pos}")

if __name__ == "__main__":
    check_day_0()