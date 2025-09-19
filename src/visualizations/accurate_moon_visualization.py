"""
Enhanced Time's Pixel Visualization with Accurate Moon Phases
Uses precise astronomical calculations for moon phases and improved color rendering.
"""
import pandas as pd
from PIL import Image
import sys
import os

# Import our enhanced modules
try:
    from src.core.color_palettes import create_palette
    from src.core.time_utils import load_astronomical_data, get_day_data
    from src.core.moon_phases import MoonPhaseCalculator, EnhancedMoonVisualizer
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Configuration
IMG_WIDTH = 24  # hours in a day
PALETTE_TYPE = "naturalistic"  # Options: "naturalistic", "vibrant", "monochrome", "classic"
OUTPUT_FILE = "accurate_moon_visualization.png"

def generate_accurate_hour_pixels(day_data, palette, moon_calculator, moon_visualizer):
    """Generate pixel colors with accurate moon phase data."""
    if day_data is None:
        return [(30, 30, 60)] * IMG_WIDTH
    
    pixels = []
    date_str = day_data['date']
    day_of_year = day_data['day_of_year']
    sunrise = day_data['sunrise']
    sunset = day_data['sunset']
    moonrise = day_data['moonrise']
    moonset = day_data['moonset']
    
    # Get accurate moon phase data
    moon_illumination = moon_calculator.get_moon_illumination(date_str)
    moon_phase_name = moon_calculator.get_moon_phase_name(date_str)
    
    for hour in range(IMG_WIDTH):
        # Get base sky color with twilight transitions
        base_color = palette.get_twilight_color(hour, sunrise, sunset, day_of_year or 1)
        
        # Check if moon is up
        moon_up = False
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                moon_up = moonrise <= hour < moonset
            else:
                moon_up = hour >= moonrise or hour < moonset
        
        if moon_up:
            # Get accurate moon color based on phase
            moon_color = moon_visualizer.get_moon_color_by_phase(date_str)
            
            # Apply seasonal tinting to moon color
            moon_color = palette.apply_seasonal_tint(moon_color, day_of_year or 1, intensity=0.2)
            
            # Blend moon color with sky color based on illumination
            opacity = 0.2 + (moon_illumination * 0.5)  # 20% to 70% opacity based on phase
            final_color = overlay_color_with_opacity(base_color, moon_color, opacity)
        else:
            final_color = base_color
        
        pixels.append(final_color)
    
    return pixels

def overlay_color_with_opacity(base_color, overlay_color, opacity):
    """Overlay one color on another with specified opacity."""
    opacity = max(0, min(1, opacity))
    r_base, g_base, b_base = base_color
    r_over, g_over, b_over = overlay_color
    
    r = int(r_base * (1 - opacity) + r_over * opacity)
    g = int(g_base * (1 - opacity) + g_over * opacity)
    b = int(b_base * (1 - opacity) + b_over * opacity)
    
    return (r, g, b)

def create_moon_phase_visualization():
    """Create visualization showing moon phases throughout the year."""
    print("Creating accurate moon phase visualization...")
    
    # Initialize moon calculations
    moon_calculator = MoonPhaseCalculator()
    moon_visualizer = EnhancedMoonVisualizer()
    
    # Load data
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None or moon_df is None:
        print("Failed to load data files.")
        return
    
    # Create color palette
    palette = create_palette(PALETTE_TYPE)
    
    # Generate pixels with accurate moon phases
    all_pixels = []
    total_days = min(len(sun_df), len(moon_df))
    
    moon_phase_info = []  # Store moon phase data for analysis
    
    for day_idx in range(total_days):
        day_data = get_day_data(sun_df, moon_df, day_idx)
        
        if day_data and day_data['date']:
            # Get moon phase info
            illumination = moon_calculator.get_moon_illumination(day_data['date'])
            phase_name = moon_calculator.get_moon_phase_name(day_data['date'])
            
            moon_phase_info.append({
                'date': day_data['date'],
                'illumination': illumination,
                'phase_name': phase_name
            })
        
        # Generate enhanced pixels
        hour_pixels = generate_accurate_hour_pixels(day_data, palette, moon_calculator, moon_visualizer)
        all_pixels.append(hour_pixels)
        
        if (day_idx + 1) % 50 == 0:
            print(f"Processed {day_idx + 1}/{total_days} days...")
    
    # Create main visualization
    img_height = len(all_pixels)
    img = Image.new('RGB', (IMG_WIDTH, img_height))
    pixels_flat = [pixel for row in all_pixels for pixel in row]
    img.putdata(pixels_flat)
    img.save(OUTPUT_FILE)
    
    print(f"Accurate moon phase visualization saved as {OUTPUT_FILE}")
    
    # Create moon phase strip visualization
    create_moon_phase_strip(moon_phase_info, moon_visualizer)
    
    # Print statistics
    print_moon_statistics(moon_phase_info)

def create_moon_phase_strip(moon_phase_info, moon_visualizer):
    """Create a strip showing moon phases throughout the year."""
    print("Creating moon phase strip...")
    
    strip_width = len(moon_phase_info)
    strip_height = 50
    
    # Create image for moon phase strip
    phase_img = Image.new('RGB', (strip_width, strip_height))
    
    phase_pixels = []
    for info in moon_phase_info:
        date = info['date']
        illumination = info['illumination']
        
        # Get moon color based on phase
        moon_color = moon_visualizer.get_moon_color_by_phase(date)
        
        # Create gradient from black to moon color based on illumination
        for y in range(strip_height):
            gradient_factor = y / strip_height
            if gradient_factor <= illumination:
                # Illuminated part
                pixel_color = moon_color
            else:
                # Dark part
                pixel_color = (20, 20, 30)
            
            phase_pixels.append(pixel_color)
    
    phase_img.putdata(phase_pixels)
    phase_img.save("moon_phase_strip.png")
    print("Moon phase strip saved as moon_phase_strip.png")

def print_moon_statistics(moon_phase_info):
    """Print statistics about moon phases in the visualization."""
    print(f"\n🌙 MOON PHASE STATISTICS")
    print("="*50)
    
    # Count phases
    phase_counts = {}
    total_illumination = 0
    
    for info in moon_phase_info:
        phase_name = info['phase_name']
        illumination = info['illumination']
        
        phase_counts[phase_name] = phase_counts.get(phase_name, 0) + 1
        total_illumination += illumination
    
    print(f"Total days analyzed: {len(moon_phase_info)}")
    print(f"Average illumination: {total_illumination / len(moon_phase_info):.1%}")
    
    print(f"\nPhase distribution:")
    for phase, count in sorted(phase_counts.items()):
        percentage = (count / len(moon_phase_info)) * 100
        print(f"  {phase}: {count} days ({percentage:.1f}%)")
    
    # Find notable moon events
    print(f"\nNotable lunar events:")
    
    # Brightest moons (>95% illumination)
    bright_moons = [info for info in moon_phase_info if info['illumination'] > 0.95]
    print(f"  Brightest moons (>95%): {len(bright_moons)} occasions")
    
    # New moons (<5% illumination)
    new_moons = [info for info in moon_phase_info if info['illumination'] < 0.05]
    print(f"  New moons (<5%): {len(new_moons)} occasions")
    
    # Show a few examples
    if bright_moons:
        print(f"  Brightest moon: {bright_moons[0]['date']} at {bright_moons[0]['illumination']:.1%}")
    
    if new_moons:
        print(f"  Darkest moon: {new_moons[0]['date']} at {new_moons[0]['illumination']:.1%}")

def compare_moon_accuracy():
    """Compare old vs new moon phase calculations side by side."""
    print("\n🔬 ACCURACY COMPARISON")
    print("="*50)
    
    from src.core.color_palettes import get_moon_phase
    from src.core.time_utils import date_to_day_of_year
    
    moon_calculator = MoonPhaseCalculator()
    
    # Test dates throughout the year
    test_dates = [
        "2024-01-11",  # Known new moon
        "2024-01-25",  # Full moon
        "2024-06-21",  # Summer solstice
        "2024-12-21",  # Winter solstice
    ]
    
    print("Date       | Old Method | New Method | Accuracy Gain")
    print("-" * 55)
    
    for date_str in test_dates:
        day_of_year = date_to_day_of_year(date_str)
        
        # Old calculation
        old_phase = get_moon_phase(day_of_year)
        
        # New accurate calculation
        new_illumination = moon_calculator.get_moon_illumination(date_str)
        phase_name = moon_calculator.get_moon_phase_name(date_str)
        
        accuracy_gain = abs(new_illumination - old_phase)
        
        print(f"{date_str} | {old_phase:9.3f} | {new_illumination:9.3f} | {accuracy_gain:+9.3f}")
        print(f"           |           | {phase_name:>9s} |")

if __name__ == "__main__":
    print("🌙 ACCURATE MOON PHASE VISUALIZATION")
    print("="*60)
    
    # Create the enhanced visualization
    create_moon_phase_visualization()
    
    # Compare accuracy
    compare_moon_accuracy()
    
    print(f"\n" + "="*60)
    print("ACCURATE MOON INTEGRATION COMPLETE!")
    print("="*60)
    print(f"Main visualization: {OUTPUT_FILE}")
    print("Moon phase strip: moon_phase_strip.png")
    print("\nThe visualization now uses:")
    print("- Precise astronomical moon phase calculations")
    print("- Realistic moon illumination percentages")
    print("- Phase-dependent moon color intensity")
    print("- Seasonal moon color tinting")
    print("="*60)