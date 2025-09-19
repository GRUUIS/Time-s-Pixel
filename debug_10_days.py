#!/usr/bin/env python3
"""Comprehensive test for the first 10 days of moon logic."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.visualizations.timelapse_visualization import SkyAnimationEngine

def test_first_10_days():
    """Test moon logic for the first 10 days comprehensively."""
    engine = SkyAnimationEngine(1200, 800)
    
    if not engine.has_data:
        print("No data loaded, exiting")
        return
    
    print("=== First 10 Days Moon Data Analysis ===")
    
    # First, let's look at the raw CSV data for first 10 days
    for day in range(1, 11):
        day_data = engine._get_cached_day_data(day)
        if day_data:
            moonrise = day_data.get('moonrise')
            moonset = day_data.get('moonset')
            print(f"Day {day:2d}: moonrise={moonrise if moonrise is not None else 'None':>6}, moonset={moonset if moonset is not None else 'None':>6}")
        else:
            print(f"Day {day:2d}: No data")
    
    print("\n=== Day by Day Analysis ===")
    
    # Test each day's moon behavior
    for day in range(1, 11):
        print(f"\n--- Day {day} ---")
        engine.day_of_year = day
        day_data = engine._get_cached_day_data(day)
        
        if not day_data:
            print(f"Day {day}: No data available")
            continue
            
        moonrise = day_data.get('moonrise')
        moonset = day_data.get('moonset')
        
        # Determine the case
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                case_type = "Normal (same day)"
                print(f"Case: {case_type} - Rise: {moonrise:.3f}, Set: {moonset:.3f}")
            else:
                case_type = "Cross-day (set next day)"
                print(f"Case: {case_type} - Rise: {moonrise:.3f}, Set: {moonset:.3f} (next day)")
        elif moonrise is None and moonset is not None:
            case_type = "Previous day moon (set only)"
            print(f"Case: {case_type} - Set: {moonset:.3f}")
        elif moonrise is not None and moonset is None:
            case_type = "Rise only (set next day)"
            print(f"Case: {case_type} - Rise: {moonrise:.3f}")
        else:
            case_type = "No moon data"
            print(f"Case: {case_type}")
            continue
        
        # Test key time points for this day
        test_times = []
        
        if moonrise is not None:
            test_times.extend([
                moonrise - 0.1,  # Before rise
                moonrise + 0.1,  # After rise
            ])
        
        if moonset is not None:
            test_times.extend([
                moonset - 0.1,   # Before set
                moonset + 0.1,   # After set
            ])
        
        # Add standard times
        test_times.extend([0.0, 6.0, 12.0, 18.0, 24.0])
        
        # Remove duplicates and sort
        test_times = sorted(list(set(test_times)))
        
        for hour in test_times:
            if hour < 0 or hour > 24:
                continue
                
            engine.animation_time = hour
            
            try:
                moon_x, moon_y = engine._calculate_raw_moon_position()
                is_visible = moon_x > 0 and moon_y > 0
                
                time_str = f"{int(hour):02d}:{int((hour % 1) * 60):02d}"
                print(f"  {time_str}: visible={is_visible}, pos=({moon_x:4d}, {moon_y:4d})")
                
            except Exception as e:
                print(f"  {hour:04.1f}h: ERROR - {e}")

def test_day_transitions():
    """Test transitions between days to check for discontinuities."""
    engine = SkyAnimationEngine(1200, 800)
    
    print("\n=== Day Transition Analysis ===")
    
    for day in range(1, 5):  # Test first few transitions
        print(f"\n--- Day {day} to Day {day+1} Transition ---")
        
        # Test end of current day and start of next day
        transition_times = [
            (day, 23.9, f"Day {day} end"),
            (day, 24.0, f"Day {day} midnight"),
            (day+1, 0.0, f"Day {day+1} start"),
            (day+1, 0.1, f"Day {day+1} early"),
        ]
        
        for test_day, hour, description in transition_times:
            engine.day_of_year = test_day
            engine.animation_time = hour
            
            try:
                moon_x, moon_y = engine._calculate_raw_moon_position()
                is_visible = moon_x > 0 and moon_y > 0
                print(f"  {description:<15}: visible={is_visible}, pos=({moon_x:4d}, {moon_y:4d})")
            except Exception as e:
                print(f"  {description:<15}: ERROR - {e}")

if __name__ == "__main__":
    test_first_10_days()
    test_day_transitions()