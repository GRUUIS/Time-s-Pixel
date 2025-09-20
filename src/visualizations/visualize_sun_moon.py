import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import os

# Configurable parameters
IMG_WIDTH = 24  # hours in a day
IMG_HEIGHT = 30  # days per month (max)
BRIGHT_COLOR = (255, 255, 180)  # Daytime pixel color
NIGHT_COLOR = (30, 30, 60)      # Night pixel color
MOON_COLOR = (180, 180, 255)    # Moon pixel overlay

# Get the project root directory
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
data_dir = os.path.join(project_root, 'data')

# Load cleaned sun and moon data
sun_df = pd.read_csv(os.path.join(data_dir, 'hongkong_sunrise_sunset_2024_clean.csv'))
moon_df = pd.read_csv(os.path.join(data_dir, 'moonrise_moonset_2024_clean.csv'))

# Helper to convert HH:MM to hour as float
def time_to_hour(t):
    if pd.isna(t) or t == '':
        return None
    h, m = map(int, str(t).split(':'))
    return h + m / 60.0

# Visualization logic
pixels = []
for idx, row in sun_df.iterrows():
    sunrise = time_to_hour(row['RISE'])
    sunset = time_to_hour(row['SET'])
    moon_row = moon_df.iloc[idx]
    moonrise = time_to_hour(moon_row['RISE'])
    moonset = time_to_hour(moon_row['SET'])
    day_pixels = []
    for hour in range(24):
        color = NIGHT_COLOR
        # Daytime
        if sunrise is not None and sunset is not None and sunrise <= hour < sunset:
            color = BRIGHT_COLOR
        # Moon up
        moon_up = False
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                moon_up = moonrise <= hour < moonset
            else:
                moon_up = hour >= moonrise or hour < moonset
        if moon_up:
            # Overlay moon color (simple blend)
            color = tuple(np.mean([color, MOON_COLOR], axis=0).astype(int))
        day_pixels.append(color)
    pixels.append(day_pixels)

# Create pixel art image
img_height = len(pixels)
img = Image.new('RGB', (IMG_WIDTH, img_height))
pixels_flat = [px for row in pixels for px in row]
img.putdata(pixels_flat)
img.save('sun_moon_pixelart_2024.png')
print('Visualization saved as sun_moon_pixelart_2024.png')
