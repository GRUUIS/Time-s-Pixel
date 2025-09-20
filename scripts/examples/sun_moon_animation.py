import pandas as pd
import numpy as np
from PIL import Image, ImageDraw
import imageio

# Configurable parameters
IMG_WIDTH = 24  # hours in a day
IMG_HEIGHT = 1  # single day per frame
BRIGHT_COLOR = (255, 255, 180)  # Daytime pixel color
NIGHT_COLOR = (30, 30, 60)      # Night pixel color
MOON_COLOR = (180, 180, 255)    # Moon pixel overlay
SUNSET_COLOR = (255, 120, 60)   # Sun is going down
MOONRISE_COLOR = (120, 120, 255) # Moon is rising

# Load cleaned sun and moon data
sun_df = pd.read_csv('hongkong_sunrise_sunset_2024_clean.csv')
moon_df = pd.read_csv('moonrise_moonset_2024_clean.csv')

# Helper to convert HH:MM to hour as float
def time_to_hour(t):
    if pd.isna(t) or t == '':
        return None
    h, m = map(int, str(t).split(':'))
    return h + m / 60.0

frames = []
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
            # Near sunset (last hour before sunset)
            if sunset - hour <= 1 and sunset - hour > 0:
                color = SUNSET_COLOR
        # Moon up
        moon_up = False
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                moon_up = moonrise <= hour < moonset
            else:
                moon_up = hour >= moonrise or hour < moonset
        if moon_up:
            # Moon is rising (first hour after moonrise)
            if hour - moonrise < 1 and hour - moonrise >= 0:
                color = MOONRISE_COLOR
            else:
                color = tuple(np.mean([color, MOON_COLOR], axis=0).astype(int))
        day_pixels.append(color)
    # Create image for this day
    img = Image.new('RGB', (IMG_WIDTH, IMG_HEIGHT))
    img.putdata(day_pixels)
    frames.append(np.array(img))

# Save as GIF animation
imageio.mimsave('sun_moon_animation_2024.gif', frames, duration=0.1)
print('Animation saved as sun_moon_animation_2024.gif')
