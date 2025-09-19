#!/usr/bin/env python3
"""Test the fixed moon visibility logic."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_fixed_moon_logic():
    """Test moon visibility for Days 2 and 3 with the fixed logic."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== Testing Day 2 (Jan 2) ===")
    engine.day_of_year = 2
    day2_data = engine._get_cached_day_data(2)
    print(f"Day 2 data: {day2_data}")
    
    test_times_day2 = [0, 6, 7, 11, 18, 22, 23, 23.3, 24]
    
    for hour in test_times_day2:
        engine.animation_time = hour
        
        if day2_data:
            moonrise = day2_data.get('moonrise')
            moonset = day2_data.get('moonset')
            
            if moonrise is not None and moonset is not None:
                is_visible, progress = engine._calculate_moon_visibility(hour, moonrise, moonset)
                print(f"Day 2, {hour:04.1f}h: moonrise={moonrise:.3f}, moonset={moonset:.3f}, visible={is_visible}")
            else:
                print(f"Day 2, {hour:04.1f}h: Missing moonrise or moonset data")
        else:
            print(f"Day 2, {hour:04.1f}h: No day data")
    
    print("\n=== Testing Day 3 (Jan 3) ===")
    engine.day_of_year = 3
    day3_data = engine._get_cached_day_data(3)
    print(f"Day 3 data: {day3_data}")
    
    test_times_day3 = [0, 6, 7, 11, 11.2, 11.3, 12, 18, 23]
    
    for hour in test_times_day3:
        engine.animation_time = hour
        
        if day3_data:
            moonrise = day3_data.get('moonrise')
            moonset = day3_data.get('moonset')
            
            print(f"Day 3, {hour:04.1f}h: moonrise={moonrise}, moonset={moonset}")
            
            # This should show that Day 3 has no moonrise but has moonset
            # Meaning moon from previous day is visible until moonset

if __name__ == "__main__":
    test_fixed_moon_logic()