# Test data loading separately
import sys
sys.path.append(r'c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\src')

try:
    from src.core.twilight_calculator import AdvancedSkyPalette
    print("✓ AdvancedSkyPalette imported successfully")
except ImportError as e:
    print(f"✗ Failed to import AdvancedSkyPalette: {e}")

try:
    from src.core.moon_phases import MoonPhaseCalculator
    print("✓ MoonPhaseCalculator imported successfully")
except ImportError as e:
    print(f"✗ Failed to import MoonPhaseCalculator: {e}")

try:
    from src.core.time_utils import load_astronomical_data, get_day_data
    print("✓ time_utils imported successfully")
except ImportError as e:
    print(f"✗ Failed to import time_utils: {e}")

# Test path calculation
import os
current_file = __file__
print(f"Current file: {current_file}")

# Simulate the path calculation from the SkyAnimationEngine
visualizations_dir = r'c:\Users\ALIENWARE\Desktop\Poly\5913_Creative_Programming\Tutorials\Time-s-Pixel\src\visualizations\timelapse_visualization.py'
project_root = os.path.dirname(os.path.dirname(os.path.dirname(visualizations_dir)))
sun_file = os.path.join(project_root, "data", "hongkong_sunrise_sunset_2024_clean.csv")
moon_file = os.path.join(project_root, "data", "moonrise_moonset_2024_clean.csv")

print(f"Calculated project root: {project_root}")
print(f"Sun file path: {sun_file}")
print(f"Moon file path: {moon_file}")
print(f"Sun file exists: {os.path.exists(sun_file)}")
print(f"Moon file exists: {os.path.exists(moon_file)}")

# Test data loading
try:
    from src.core.time_utils import load_astronomical_data
    sun_df, moon_df = load_astronomical_data(sun_file, moon_file)
    has_data = sun_df is not None and moon_df is not None
    print(f"Data loading result: has_data = {has_data}")
    if has_data:
        print(f"Loaded {len(sun_df)} days of sun data, {len(moon_df)} days of moon data")
except Exception as e:
    print(f"Error loading data: {e}")
    import traceback
    traceback.print_exc()