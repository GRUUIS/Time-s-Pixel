#!/usr/bin/env python3
"""Test to understand the cross-day moon issue."""

import sys
import os
sys.path.append(os.path.dirname(__file__))

def test_cross_day_logic():
    """Test the cross-day moon logic issue."""
    # Day 2 data
    moonrise_day2 = 23.283  # 23:17
    moonset_day2 = 11.233   # 11:14 (but this is actually Day 3!)
    
    print("=== Current INCORRECT logic ===")
    print(f"Day 2: moonrise={moonrise_day2:.3f}, moonset={moonset_day2:.3f}")
    print(f"Since moonrise > moonset ({moonrise_day2} > {moonset_day2}), code thinks moon sets after midnight")
    print("This makes moon visible from 0:00-11:14, which is WRONG!")
    print()
    
    print("=== CORRECT interpretation ===")
    print("Day 2 (Jan 2):")
    print(f"  - Moon rises: 23:17 (moonrise={moonrise_day2:.3f})")
    print(f"  - Moon visible: 23:17-24:00 on Day 2")
    print()
    print("Day 3 (Jan 3):")
    print(f"  - Moon continues visible: 00:00-11:14 on Day 3")
    print(f"  - Moon sets: 11:14 (moonset={moonset_day2:.3f})")
    print()
    
    # Test current hours
    test_hours = [0, 6, 7, 11, 12, 18, 23, 23.5, 24]
    
    print("=== Current logic results (WRONG) ===")
    for hour in test_hours:
        if moonrise_day2 < moonset_day2:
            # Normal case
            visible = moonrise_day2 <= hour <= moonset_day2
        else:
            # Cross-midnight case (CURRENT BUGGY LOGIC)
            visible = hour >= moonrise_day2 or hour <= moonset_day2
        
        print(f"Hour {hour:04.1f}: visible={visible}")
    
    print()
    print("=== What should happen ===")
    print("Day 2 (0-24h): Moon visible only from 23:17-24:00")
    print("Day 3 (0-24h): Moon visible only from 00:00-11:14")

if __name__ == "__main__":
    test_cross_day_logic()