"""
Advanced Twilight Visualization for Time's Pixel
Creates stunning visualizations with realistic civil, nautical, and astronomical twilight.
"""
import pandas as pd
from PIL import Image
import sys

# Import our advanced modules
try:
    from twilight_calculator import AdvancedSkyPalette, TwilightCalculator
    from time_utils import load_astronomical_data, get_day_data
    from moon_phases import MoonPhaseCalculator, EnhancedMoonVisualizer
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

# Configuration
IMG_WIDTH = 24  # hours in a day
OUTPUT_FILE = "advanced_twilight_visualization.png"
COMPARISON_FILE = "twilight_comparison.png"

def generate_advanced_twilight_pixels(day_data, sky_palette, moon_calculator, moon_visualizer):
    """Generate pixels using advanced twilight calculations."""
    if day_data is None:
        return [(15, 15, 35)] * IMG_WIDTH
    
    pixels = []
    date_str = day_data['date']
    day_of_year = day_data['day_of_year']
    sunrise = day_data['sunrise']
    sunset = day_data['sunset']
    moonrise = day_data['moonrise']
    moonset = day_data['moonset']
    
    # Get moon phase data
    moon_illumination = moon_calculator.get_moon_illumination(date_str) if date_str else 0.5
    
    for hour in range(IMG_WIDTH):
        # Get advanced sky color with proper twilight calculations
        sky_color = sky_palette.get_advanced_sky_color(
            hour, sunrise, sunset, date_str or "2024-01-01", day_of_year or 1
        )
        
        # Check if moon is up
        moon_up = False
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                moon_up = moonrise <= hour < moonset
            else:
                moon_up = hour >= moonrise or hour < moonset
        
        if moon_up and date_str:
            # Get moon color based on phase
            moon_color = moon_visualizer.get_moon_color_by_phase(date_str)
            
            # Blend moon with sky based on illumination
            opacity = 0.1 + (moon_illumination * 0.4)  # 10% to 50% opacity
            final_color = overlay_color_with_opacity(sky_color, moon_color, opacity)
        else:
            final_color = sky_color
        
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

def create_advanced_twilight_visualization():
    """Create visualization with advanced twilight calculations."""
    print("🌅 CREATING ADVANCED TWILIGHT VISUALIZATION")
    print("="*60)
    
    # Initialize advanced systems
    sky_palette = AdvancedSkyPalette()
    moon_calculator = MoonPhaseCalculator()
    moon_visualizer = EnhancedMoonVisualizer()
    
    # Load data
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None or moon_df is None:
        print("Failed to load data files.")
        return
    
    # Generate pixels with advanced twilight
    print("Generating advanced twilight pixels...")
    all_pixels = []
    total_days = min(len(sun_df), len(moon_df))
    
    twilight_stats = {
        'golden_hours': 0,
        'blue_hours': 0,
        'civil_twilight': 0,
        'nautical_twilight': 0,
        'astronomical_twilight': 0
    }
    
    for day_idx in range(total_days):
        day_data = get_day_data(sun_df, moon_df, day_idx)
        
        # Generate advanced pixels
        hour_pixels = generate_advanced_twilight_pixels(
            day_data, sky_palette, moon_calculator, moon_visualizer
        )
        all_pixels.append(hour_pixels)
        
        # Collect twilight statistics
        if day_data and day_data['date']:
            collect_twilight_stats(day_data, sky_palette, twilight_stats)
        
        if (day_idx + 1) % 50 == 0:
            print(f"Processed {day_idx + 1}/{total_days} days...")
    
    # Create main visualization
    print("Creating advanced twilight image...")
    img_height = len(all_pixels)
    img = Image.new('RGB', (IMG_WIDTH, img_height))
    pixels_flat = [pixel for row in all_pixels for pixel in row]
    img.putdata(pixels_flat)
    img.save(OUTPUT_FILE)
    
    print(f"Advanced twilight visualization saved as {OUTPUT_FILE}")
    
    # Print statistics
    print_twilight_statistics(twilight_stats, total_days)

def collect_twilight_stats(day_data, sky_palette, stats):
    """Collect statistics about twilight types throughout the year."""
    date_str = day_data['date']
    sunrise = day_data['sunrise']
    sunset = day_data['sunset']
    
    if not all([date_str, sunrise, sunset]):
        return
    
    twilight_calc = TwilightCalculator()
    twilight_times = twilight_calc.calculate_twilight_times(date_str, sunrise, sunset)
    
    # Count different twilight types based on duration
    for twilight_type, times in twilight_times.items():
        if 'morning' in times and 'evening' in times:
            duration = times['evening'] - times['morning']
            
            if twilight_type == 'golden_hour' and duration > 2:
                stats['golden_hours'] += 1
            elif twilight_type == 'blue_hour' and duration > 1:
                stats['blue_hours'] += 1
            elif twilight_type == 'civil' and duration > 13:
                stats['civil_twilight'] += 1
            elif twilight_type == 'nautical' and duration > 14:
                stats['nautical_twilight'] += 1
            elif twilight_type == 'astronomical' and duration > 15:
                stats['astronomical_twilight'] += 1

def print_twilight_statistics(stats, total_days):
    """Print twilight statistics for the visualization."""
    print(f"\n🌅 TWILIGHT STATISTICS")
    print("="*50)
    print(f"Total days analyzed: {total_days}")
    
    for twilight_type, count in stats.items():
        percentage = (count / total_days) * 100
        readable_name = twilight_type.replace('_', ' ').title()
        print(f"{readable_name}: {count} days ({percentage:.1f}%)")
    
    print(f"\nTwilight features in visualization:")
    print("- Civil twilight: Bright twilight when sun is 6° below horizon")
    print("- Nautical twilight: Navigation possible, horizon visible")
    print("- Astronomical twilight: Faintest stars visible")
    print("- Blue hour: Deep blue sky before sunrise/after sunset") 
    print("- Golden hour: Warm light when sun is low on horizon")

def create_twilight_comparison_image():
    """Create side-by-side comparison of basic vs advanced twilight."""
    print(f"\n🎨 CREATING TWILIGHT COMPARISON")
    print("="*50)
    
    from color_palettes import ColorPalette
    
    # Initialize both palette systems
    basic_palette = ColorPalette()
    advanced_palette = AdvancedSkyPalette()
    
    # Load sample data
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None:
        return
    
    # Select interesting days (equinoxes and solstices)
    sample_days = [79, 172, 266, 355]  # Approximate equinoxes and solstices
    
    comparison_pixels = []
    
    for day_idx in sample_days:
        day_data = get_day_data(sun_df, moon_df, day_idx)
        
        if day_data:
            # Basic twilight row
            basic_row = []
            for hour in range(IMG_WIDTH):
                color = basic_palette.get_twilight_color(
                    hour, day_data['sunrise'], day_data['sunset'], day_data['day_of_year']
                )
                basic_row.append(color)
            comparison_pixels.append(basic_row)
            
            # Advanced twilight row
            advanced_row = []
            for hour in range(IMG_WIDTH):
                color = advanced_palette.get_advanced_sky_color(
                    hour, day_data['sunrise'], day_data['sunset'], 
                    day_data['date'], day_data['day_of_year']
                )
                advanced_row.append(color)
            comparison_pixels.append(advanced_row)
    
    # Create comparison image
    comp_height = len(comparison_pixels)
    comp_img = Image.new('RGB', (IMG_WIDTH, comp_height))
    pixels_flat = [pixel for row in comparison_pixels for pixel in row]
    comp_img.putdata(pixels_flat)
    
    # Scale up for better visibility
    scale_factor = 20
    comp_img_scaled = comp_img.resize(
        (IMG_WIDTH * scale_factor, comp_height * scale_factor),
        Image.Resampling.NEAREST
    )
    
    comp_img_scaled.save(COMPARISON_FILE)
    print(f"Twilight comparison saved as {COMPARISON_FILE}")
    print("Comparison shows basic (odd rows) vs advanced (even rows) twilight")

def demonstrate_twilight_features():
    """Demonstrate specific twilight calculation features."""
    print(f"\n🔬 TWILIGHT FEATURE DEMONSTRATION")
    print("="*50)
    
    twilight_calc = TwilightCalculator()
    sky_palette = AdvancedSkyPalette()
    
    # Summer solstice - longest day
    summer_date = "2024-06-21"
    summer_sunrise = 5.67
    summer_sunset = 19.17
    
    print(f"Summer Solstice ({summer_date}):")
    twilight_times = twilight_calc.calculate_twilight_times(summer_date, summer_sunrise, summer_sunset)
    
    print("Twilight Phase Schedule:")
    for phase, times in twilight_times.items():
        morning = times.get('morning', 0)
        evening = times.get('evening', 0)
        duration = evening - morning
        print(f"  {phase.replace('_', ' ').title():>18}: {morning:5.2f}h - {evening:5.2f}h ({duration:.2f}h)")
    
    print(f"\nColor progression through the day:")
    print("Time | Phase                 | Color")
    print("-" * 40)
    
    for hour in [3, 5, 6, 7, 12, 18, 19, 20, 21]:
        color = sky_palette.get_advanced_sky_color(hour, summer_sunrise, summer_sunset, summer_date, 173)
        sky_type = twilight_calc.get_sky_type(hour, summer_sunrise, summer_sunset, twilight_times)
        print(f"{hour:4d} | {sky_type:<21} | {color}")

if __name__ == "__main__":
    print("🌅 ADVANCED TWILIGHT VISUALIZATION SYSTEM")
    print("="*70)
    
    # Create the advanced visualization
    create_advanced_twilight_visualization()
    
    # Create comparison
    create_twilight_comparison_image()
    
    # Demonstrate features
    demonstrate_twilight_features()
    
    print(f"\n" + "="*70)
    print("ADVANCED TWILIGHT SYSTEM COMPLETE!")
    print("="*70)
    print(f"Main visualization: {OUTPUT_FILE}")
    print(f"Comparison image: {COMPARISON_FILE}")
    print("\nAdvanced features implemented:")
    print("- Accurate solar position calculations for Hong Kong")
    print("- Civil, nautical, and astronomical twilight periods")
    print("- Golden hour and blue hour identification")
    print("- Smooth color transitions between twilight phases")
    print("- Seasonal color variations")
    print("- Integration with accurate moon phase data")
    print("="*70)