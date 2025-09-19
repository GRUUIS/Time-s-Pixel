#!/usr/bin/env python3
"""Analyze the current wrong logic for Day 2 moon arc."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def analyze_wrong_logic():
    """Analyze why moon completes rotation before 6am on Day 2."""
    
    # Day 2 data from CSV
    moonrise_day2 = 23.283  # 23:17 on Day 2
    moonset_day2 = 11.233   # 11:14 on Day 3 (NOT Day 2!)
    
    print("=== Current WRONG Logic Analysis ===")
    print(f"Day 2 moonrise: {moonrise_day2:.3f} (23:17)")
    print(f"Day 2 moonset: {moonset_day2:.3f} (11:14 - but this is Day 3!)")
    print()
    
    # Current wrong logic in _calculate_moon_visibility
    print("Current _calculate_moon_visibility logic:")
    print("Since moonrise > moonset (23.283 > 11.233):")
    print("  - Treats as cross-day case")
    print("  - Moon visible from moonrise to 24:00 on Day 2")
    print("  - Progress calculated as: (current_hour - moonrise) / (24 - moonrise)")
    print()
    
    # Calculate wrong progress at different times
    test_times = [23.3, 24.0, 0.0, 6.0, 11.0]
    
    for hour in test_times:
        if hour >= moonrise_day2:
            # Current wrong calculation for Day 2
            time_since_rise = hour - moonrise_day2
            total_visible_today = 24 - moonrise_day2  # Wrong! Only counts Day 2
            progress = time_since_rise / total_visible_today
            
            print(f"Hour {hour:04.1f}: time_since_rise={time_since_rise:.3f}, total_visible={total_visible_today:.3f}, progress={progress:.3f}")
            
            if progress >= 1.0:
                print(f"  → WRONG: Moon completes arc at {hour:04.1f}h!")
    
    print()
    print("=== CORRECT Logic Should Be ===")
    print("Day 2 moonrise: 23:17")
    print("Day 3 moonset: 11:14 (next day)")
    print("Total visible duration: (24:00 - 23:17) + (11:14 - 00:00) = 0:43 + 11:14 = 12:57")
    print("Moon should complete arc only when it reaches Day 3 at 11:14")

if __name__ == "__main__":
    analyze_wrong_logic()