# Test if the animation's caching is working correctly
import sys
sys.path.append(r'c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\src')

from core.time_utils import load_astronomical_data, get_day_data

# Simulate the animation's caching logic
def simulate_precompute():
    """Simulate how the animation pre-computes data"""
    sun_df, moon_df = load_astronomical_data()
    astronomical_cache = {}
    
    print("=== Simulating Animation Pre-computation ===")
    
    # Test specifically for day 2
    day = 2
    day_idx = day - 1  # 0-indexed
    
    print(f"Getting data for day {day} (index {day_idx})")
    day_data = get_day_data(sun_df, moon_df, day_idx)
    
    print(f"Raw day_data: {day_data}")
    
    if day_data:
        cached_data = {
            'sunrise': day_data.get('sunrise', 6.0),
            'sunset': day_data.get('sunset', 18.0),
            'moonrise': day_data.get('moonrise'),
            'moonset': day_data.get('moonset'),
            'date': day_data.get('date', f'2024-{day:03d}')
        }
        astronomical_cache[day] = cached_data
        print(f"Cached data for day {day}: {cached_data}")
        
        # Test the exact condition used in animation
        moonrise_valid = cached_data.get('moonrise') is not None
        moonset_valid = cached_data.get('moonset') is not None
        
        print(f"Moonrise valid: {moonrise_valid}")
        print(f"Moonset valid: {moonset_valid}")
        
        if moonrise_valid and moonset_valid:
            print("✓ Animation would use real moon data")
            
            # Test visibility calculation
            moonrise = cached_data['moonrise']
            moonset = cached_data['moonset']
            
            print(f"Testing visibility at different times:")
            test_times = [18.0, 19.0, 20.0, 23.0, 23.17, 23.3]
            
            for time in test_times:
                # Same logic as animation
                if moonrise < moonset:
                    visible = moonrise <= time <= moonset
                else:
                    visible = time >= moonrise or time <= moonset
                    
                print(f"  {time:5.1f}h: {'visible' if visible else 'hidden'}")
                
        else:
            print("✗ Animation would use fallback logic!")
    else:
        print("✗ No day data found - animation would use fallback logic!")
        
    return astronomical_cache.get(day)

# Run the simulation
cached_result = simulate_precompute()

print(f"\n=== Testing Fallback Logic ===")
if cached_result is None:
    print("Since caching failed, let's see what fallback would do:")
    test_times = [18.0, 19.0, 20.0, 21.0, 22.0, 23.0, 23.17]
    
    for time in test_times:
        # Fallback logic: simple day/night check
        fallback_visible = not (6 <= time <= 18)
        print(f"  {time:5.1f}h: {'visible' if fallback_visible else 'hidden'} (fallback)")
    
    print(f"\nThis matches your observation! Moon appears at 19:00 instead of 23:17")
else:
    print("Caching worked correctly, so the problem must be elsewhere.")

print(f"\n=== Recommendation ===")
print("Add debug prints to the animation to see which logic path it's taking!")