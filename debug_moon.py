# Debug script to test moon visibility logic directly
import sys
sys.path.append(r'c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\src')

from core.time_utils import load_astronomical_data, get_day_data

# Load data
sun_df, moon_df = load_astronomical_data(
    sun_file=r"c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\data\hongkong_sunrise_sunset_2024_clean.csv",
    moon_file=r"c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\data\moonrise_moonset_2024_clean.csv"
)

# Test January 2nd moon visibility logic exactly as the animation does
day_2_data = get_day_data(sun_df, moon_df, 1)  # Jan 2 (0-indexed)

def calculate_moon_visibility(current_hour, moonrise, moonset):
    """Exact copy of the animation's moon visibility calculation"""
    if moonrise < moonset:
        # Normal case: moon rises then sets within same day
        if moonrise <= current_hour <= moonset:
            moon_duration = moonset - moonrise
            progress = (current_hour - moonrise) / moon_duration if moon_duration > 0 else 0
            return True, progress
        else:
            return False, None
    else:
        # Moon sets after midnight (moonrise > moonset)
        if current_hour >= moonrise or current_hour <= moonset:
            if current_hour >= moonrise:
                # After moonrise, before midnight
                time_since_rise = current_hour - moonrise
                total_visible = (24 - moonrise) + moonset
                progress = time_since_rise / total_visible if total_visible > 0 else 0
            else:
                # After midnight, before moonset
                time_since_rise = (24 - moonrise) + current_hour
                total_visible = (24 - moonrise) + moonset
                progress = time_since_rise / total_visible if total_visible > 0 else 0
            
            return True, progress
        else:
            return False, None

print("=== CSV Data vs Animation Logic Test ===")
print(f"Jan 2 Moonrise: {day_2_data['moonrise']:.2f} ({int(day_2_data['moonrise'])}:{int((day_2_data['moonrise']%1)*60):02d})")
print(f"Jan 2 Moonset:  {day_2_data['moonset']:.2f} ({int(day_2_data['moonset'])}:{int((day_2_data['moonset']%1)*60):02d})")

# The key test: when does the moon become visible according to the logic?
print("\n=== Precise Moonrise Test ===")
test_times = [23.0, 23.1, 23.15, 23.16, 23.17, 23.2, 23.25, 23.28, 23.3, 23.5]

print("Time   | Visible? | Progress | Note")
print("-" * 45)

moonrise = day_2_data['moonrise']  # Should be 23.28
moonset = day_2_data['moonset']

for time in test_times:
    is_visible, progress = calculate_moon_visibility(time, moonrise, moonset)
    
    if time == 23.17:
        note = "← YOUR OBSERVATION"
    elif time == moonrise:
        note = "← CSV MOONRISE"
    else:
        note = ""
    
    prog_str = f"{progress:.3f}" if progress is not None else "None"
    print(f"{time:6.2f} | {str(is_visible):8s} | {prog_str:8s} | {note}")

print(f"\n=== ANALYSIS ===")
print(f"CSV says moonrise is at {moonrise:.2f} ({int(moonrise)}:{int((moonrise%1)*60):02d})")
print(f"You observed moon appearing at night start, but it should wait until {int(moonrise)}:{int((moonrise%1)*60):02d}")

print(f"\n=== HYPOTHESIS ===")
print("If the animation is showing moon 'as soon as night falls', it means:")
print("1. The code is falling back to the simple day/night logic")
print("2. OR there's a bug in the visibility calculation")
print("3. OR the CSV data isn't being loaded properly")

# Let's verify if the calculation matches what you observed
print(f"\n=== Your Observation Check ===")
print("You said: 'As soon as night falls (around 18:00), moon appears'")
sunset_time = day_2_data['sunset']
print(f"Sunset on Jan 2: {sunset_time:.2f}")

is_visible_at_sunset, _ = calculate_moon_visibility(sunset_time, moonrise, moonset)
print(f"Should moon be visible at sunset? {is_visible_at_sunset}")

# Test some night hours
night_hours = [18.5, 19.0, 20.0, 21.0, 22.0]
print(f"\nTesting visibility during night hours:")
for hour in night_hours:
    visible, _ = calculate_moon_visibility(hour, moonrise, moonset)
    print(f"  {hour:4.1f}h: {visible}")

print("\nIf any of these show True, there's a bug in the visibility logic!")
print("If they all show False, then the problem is elsewhere in the animation.")