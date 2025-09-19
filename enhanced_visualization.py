"""
Enhanced Time's Pixel Visualization with improved color palettes and twilight transitions.
This version uses the new color palette system for more realistic and beautiful visualizations.
"""
import pandas as pd
from PIL import Image
import sys
import os

# Import our new modules
try:
    from color_palettes import create_palette, get_moon_phase
    from time_utils import load_astronomical_data, get_day_data, generate_hour_pixels
except ImportError as e:
    print(f"Error importing modules: {e}")
    print("Make sure color_palettes.py and time_utils.py are in the same directory")
    sys.exit(1)

# Configuration
IMG_WIDTH = 24  # hours in a day
PALETTE_TYPE = "naturalistic"  # Options: "naturalistic", "vibrant", "monochrome", "classic"
OUTPUT_FILE = "enhanced_sun_moon_365days.png"

def create_enhanced_visualization():
    """Create enhanced visualization with new color palette system."""
    
    # Load data
    print("Loading astronomical data...")
    sun_df, moon_df = load_astronomical_data()
    
    if sun_df is None or moon_df is None:
        print("Failed to load data files. Please ensure the CSV files exist.")
        return
    
    # Create color palette
    print(f"Creating {PALETTE_TYPE} color palette...")
    palette = create_palette(PALETTE_TYPE)
    
    # Generate pixels for each day
    print("Generating enhanced pixel art...")
    all_pixels = []
    total_days = min(len(sun_df), len(moon_df))
    
    for day_idx in range(total_days):
        # Get day data
        day_data = get_day_data(sun_df, moon_df, day_idx)
        
        # Generate hour pixels with enhanced colors
        hour_pixels = generate_hour_pixels(day_data, palette, IMG_WIDTH)
        all_pixels.append(hour_pixels)
        
        # Progress indicator
        if (day_idx + 1) % 50 == 0:
            print(f"Processed {day_idx + 1}/{total_days} days...")
    
    # Create image
    print("Creating image...")
    img_height = len(all_pixels)
    img = Image.new('RGB', (IMG_WIDTH, img_height))
    
    # Flatten pixel data for PIL
    pixels_flat = [pixel for row in all_pixels for pixel in row]
    img.putdata(pixels_flat)
    
    # Save image
    img.save(OUTPUT_FILE)
    print(f"Enhanced visualization saved as {OUTPUT_FILE}")
    
    # Print some statistics
    print(f"\nVisualization Statistics:")
    print(f"Days processed: {total_days}")
    print(f"Image dimensions: {IMG_WIDTH} x {img_height}")
    print(f"Color palette: {PALETTE_TYPE}")
    print(f"Total pixels: {IMG_WIDTH * img_height:,}")

def create_palette_comparison():
    """Create a comparison of different color palettes."""
    print("\nCreating palette comparison...")
    
    # Load data
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None or moon_df is None:
        return
    
    palettes = ["naturalistic", "vibrant", "monochrome", "classic"]
    sample_days = [1, 91, 182, 273]  # Winter, Spring, Summer, Autumn
    
    comparison_pixels = []
    
    for palette_name in palettes:
        palette = create_palette(palette_name)
        palette_row = []
        
        for day_idx in sample_days:
            day_data = get_day_data(sun_df, moon_df, day_idx)
            hour_pixels = generate_hour_pixels(day_data, palette, IMG_WIDTH)
            palette_row.extend(hour_pixels)
        
        comparison_pixels.append(palette_row)
    
    # Create comparison image
    comp_width = IMG_WIDTH * len(sample_days)
    comp_height = len(palettes)
    comp_img = Image.new('RGB', (comp_width, comp_height))
    
    pixels_flat = [pixel for row in comparison_pixels for pixel in row]
    comp_img.putdata(pixels_flat)
    
    # Scale up for better visibility
    scale_factor = 10
    comp_img_scaled = comp_img.resize(
        (comp_width * scale_factor, comp_height * scale_factor), 
        Image.Resampling.NEAREST
    )
    
    comp_img_scaled.save("palette_comparison.png")
    print("Palette comparison saved as palette_comparison.png")

def print_color_info():
    """Print information about the enhanced color system."""
    print("\n" + "="*60)
    print("ENHANCED COLOR PALETTE SYSTEM")
    print("="*60)
    
    print("\nAvailable Palettes:")
    print("- naturalistic: Realistic sky colors and natural tones")
    print("- vibrant: Bright, artistic colors for expressive visualizations")  
    print("- monochrome: Elegant grayscale palette")
    print("- classic: Original color scheme from basic version")
    
    print("\nEnhancements:")
    print("- Seasonal color tinting based on time of year")
    print("- Smooth twilight transitions (dawn/dusk gradients)")
    print("- Moon phase integration affecting moon brightness")
    print("- Dynamic color temperature changes")
    print("- Proper color blending for moon/sky overlays")
    
    print("\nColor Features:")
    print("- Dawn: Warm orange/pink gradients")
    print("- Day: Dynamic sky colors varying by season")
    print("- Dusk: Sunset color transitions")
    print("- Night: Deep blues with seasonal variations")
    print("- Moon: Phase-based brightness with seasonal tinting")

if __name__ == "__main__":
    print_color_info()
    
    # Create enhanced visualization
    create_enhanced_visualization()
    
    # Create palette comparison
    create_palette_comparison()
    
    print(f"\n" + "="*60)
    print("ENHANCEMENT COMPLETE!")
    print("="*60)
    print(f"Main visualization: {OUTPUT_FILE}")
    print("Palette comparison: palette_comparison.png")
    print("\nTry changing PALETTE_TYPE at the top of this file to:")
    print("'vibrant', 'monochrome', or 'classic' for different looks!")