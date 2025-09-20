"""
Shared utility functions for Time's Pixel visualization project.
Contains common data processing, time conversion, and helper functions.
"""
import pandas as pd
import math
from datetime import datetime

def time_to_hour(t):
    """Convert HH:MM time string to hour as float."""
    if pd.isna(t) or t == '':
        return None
    try:
        h, m = map(int, str(t).split(':'))
        return h + m / 60.0
    except (ValueError, AttributeError):
        return None

def hour_to_time(hour_float):
    """Convert hour float back to HH:MM time string."""
    if hour_float is None:
        return None
    hours = int(hour_float)
    minutes = int((hour_float - hours) * 60)
    return f"{hours:02d}:{minutes:02d}"

def date_to_day_of_year(date_str):
    """Convert YYYY-MM-DD date string to day of year (1-365/366)."""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        return date_obj.timetuple().tm_yday
    except ValueError:
        return None

def load_astronomical_data(sun_file="data/hongkong_sunrise_sunset_2024_clean.csv", 
                          moon_file="data/moonrise_moonset_2024_clean.csv"):
    """Load and return cleaned astronomical data."""
    try:
        sun_df = pd.read_csv(sun_file)
        moon_df = pd.read_csv(moon_file)
        return sun_df, moon_df
    except FileNotFoundError as e:
        print(f"Error loading data files: {e}")
        return None, None

def get_day_data(sun_df, moon_df, day_index):
    """Get astronomical data for a specific day index."""
    if day_index >= len(sun_df) or day_index >= len(moon_df):
        return None
    
    sun_row = sun_df.iloc[day_index]
    moon_row = moon_df.iloc[day_index]
    
    return {
        'date': sun_row['YYYY-MM-DD'],
        'day_of_year': date_to_day_of_year(sun_row['YYYY-MM-DD']),
        'sunrise': time_to_hour(sun_row['RISE']),
        'sunset': time_to_hour(sun_row['SET']),
        'sun_transit': time_to_hour(sun_row['TRAN.']),
        'moonrise': time_to_hour(moon_row['RISE']),
        'moonset': time_to_hour(moon_row['SET']),
        'moon_transit': time_to_hour(moon_row['TRAN.'])
    }

def calculate_daylight_duration(sunrise, sunset):
    """Calculate daylight duration in hours."""
    if sunrise is None or sunset is None:
        return None
    
    if sunset > sunrise:
        return sunset - sunrise
    else:
        # Handle case where sunset is next day
        return (24 - sunrise) + sunset

def is_moon_up(hour, moonrise, moonset):
    """Check if moon is above horizon at given hour."""
    if moonrise is None or moonset is None:
        return False
    
    if moonrise < moonset:
        # Moon rises and sets on same day
        return moonrise <= hour < moonset
    else:
        # Moon sets on next day
        return hour >= moonrise or hour < moonset

def get_astronomical_season(day_of_year):
    """Get astronomical season based on day of year."""
    # Approximate dates for 2024 (leap year)
    if day_of_year < 80:  # Before March 20
        return "Winter"
    elif day_of_year < 173:  # Before June 21
        return "Spring"  
    elif day_of_year < 267:  # Before September 23
        return "Summer"
    elif day_of_year < 356:  # Before December 21
        return "Autumn"
    else:
        return "Winter"

def interpolate_color(color1, color2, factor):
    """Linearly interpolate between two RGB colors."""
    factor = max(0, min(1, factor))
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    
    r = int(r1 + (r2 - r1) * factor)
    g = int(g1 + (g2 - g1) * factor)
    b = int(b1 + (b2 - b1) * factor)
    
    return (r, g, b)

def overlay_color(base_color, overlay_color, opacity=0.5):
    """Overlay one color on another with given opacity."""
    opacity = max(0, min(1, opacity))
    
    r_base, g_base, b_base = base_color
    r_over, g_over, b_over = overlay_color
    
    r = int(r_base * (1 - opacity) + r_over * opacity)
    g = int(g_base * (1 - opacity) + g_over * opacity)
    b = int(b_base * (1 - opacity) + b_over * opacity)
    
    return (r, g, b)

def generate_hour_pixels(day_data, palette, img_width=24):
    """Generate pixel colors for all hours of a day."""
    if day_data is None:
        return [(30, 30, 60)] * img_width  # Default night color
    
    pixels = []
    day_of_year = day_data['day_of_year']
    sunrise = day_data['sunrise']
    sunset = day_data['sunset']
    moonrise = day_data['moonrise']
    moonset = day_data['moonset']
    
    # Import here to avoid circular import
    from src.core.color_palettes import get_moon_phase
    moon_phase = get_moon_phase(day_of_year) if day_of_year else 0.5
    
    for hour in range(img_width):
        # Get base sky color with twilight transitions
        base_color = palette.get_twilight_color(hour, sunrise, sunset, day_of_year or 1)
        
        # Check for moon overlay
        moon_color = palette.get_moon_color(hour, moonrise, moonset, moon_phase, day_of_year or 1)
        
        if moon_color is not None:
            # Blend moon color with sky color
            final_color = overlay_color(base_color, moon_color, opacity=0.4)
        else:
            final_color = base_color
        
        pixels.append(final_color)
    
    return pixels

def calculate_seasonal_stats(sun_df):
    """Calculate seasonal statistics from sun data."""
    stats = {
        'shortest_day': {'duration': float('inf'), 'date': None},
        'longest_day': {'duration': 0, 'date': None},
        'earliest_sunrise': {'time': 24, 'date': None},
        'latest_sunrise': {'time': 0, 'date': None},
        'earliest_sunset': {'time': 24, 'date': None},
        'latest_sunset': {'time': 0, 'date': None}
    }
    
    for idx, row in sun_df.iterrows():
        date = row['YYYY-MM-DD']
        sunrise = time_to_hour(row['RISE'])
        sunset = time_to_hour(row['SET'])
        
        if sunrise is not None and sunset is not None:
            duration = calculate_daylight_duration(sunrise, sunset)
            
            # Track extremes
            if duration < stats['shortest_day']['duration']:
                stats['shortest_day'] = {'duration': duration, 'date': date}
            
            if duration > stats['longest_day']['duration']:
                stats['longest_day'] = {'duration': duration, 'date': date}
            
            if sunrise < stats['earliest_sunrise']['time']:
                stats['earliest_sunrise'] = {'time': sunrise, 'date': date}
            
            if sunrise > stats['latest_sunrise']['time']:
                stats['latest_sunrise'] = {'time': sunrise, 'date': date}
            
            if sunset < stats['earliest_sunset']['time']:
                stats['earliest_sunset'] = {'time': sunset, 'date': date}
            
            if sunset > stats['latest_sunset']['time']:
                stats['latest_sunset'] = {'time': sunset, 'date': date}
    
    return stats

# Example usage and testing
if __name__ == "__main__":
    # Test utility functions
    sun_df, moon_df = load_astronomical_data()
    
    if sun_df is not None and moon_df is not None:
        print("Data loaded successfully!")
        print(f"Sun data: {len(sun_df)} days")
        print(f"Moon data: {len(moon_df)} days")
        
        # Test day data extraction
        day_100_data = get_day_data(sun_df, moon_df, 99)  # 100th day (April 9, 2024)
        print(f"\nDay 100 data: {day_100_data}")
        
        # Calculate seasonal statistics
        stats = calculate_seasonal_stats(sun_df)
        print(f"\nSeasonal Statistics:")
        print(f"Shortest day: {stats['shortest_day']['duration']:.2f}h on {stats['shortest_day']['date']}")
        print(f"Longest day: {stats['longest_day']['duration']:.2f}h on {stats['longest_day']['date']}")
        print(f"Earliest sunrise: {hour_to_time(stats['earliest_sunrise']['time'])} on {stats['earliest_sunrise']['date']}")
        print(f"Latest sunset: {hour_to_time(stats['latest_sunset']['time'])} on {stats['latest_sunset']['date']}")
    else:
        print("Failed to load data files")