
# --- New Fullscreen Daytime Animation ---
import pandas as pd
import numpy as np
import pygame
import sys

# Configurable parameters
IMG_WIDTH = 24  # hours in a day
IMG_HEIGHT = 1  # one row per day
BRIGHT_COLOR = (255, 255, 180)
NIGHT_COLOR = (30, 30, 60)
MOON_COLOR = (180, 180, 255)
SUNSET_COLOR = (255, 120, 60)
MOONRISE_COLOR = (120, 120, 255)
BG_COLOR = (10, 10, 20)

# Load cleaned sun and moon data
sun_df = pd.read_csv('hongkong_sunrise_sunset_2024_clean.csv')
moon_df = pd.read_csv('moonrise_moonset_2024_clean.csv')

def time_to_hour(t):
    if pd.isna(t) or t == '':
        return None
    h, m = map(int, str(t).split(':'))
    return h + m / 60.0

# Get screen size
pygame.init()
info = pygame.display.Info()
screen_width = info.current_w
screen_height = info.current_h
PIXEL_SIZE = min(screen_width // IMG_WIDTH, screen_height // IMG_HEIGHT)
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN)
pygame.display.set_caption('Sun & Moon Daytime Animation')
clock = pygame.time.Clock()

def get_day_pixels(idx):
    row = sun_df.iloc[idx]
    sunrise = time_to_hour(row['RISE'])
    sunset = time_to_hour(row['SET'])
    moon_row = moon_df.iloc[idx]
    moonrise = time_to_hour(moon_row['RISE'])
    moonset = time_to_hour(moon_row['SET'])
    day_pixels = []
    for hour in range(IMG_WIDTH):
        color = NIGHT_COLOR
        if sunrise is not None and sunset is not None and sunrise <= hour < sunset:
            color = BRIGHT_COLOR
            if sunset - hour <= 1 and sunset - hour > 0:
                color = SUNSET_COLOR
        moon_up = False
        if moonrise is not None and moonset is not None:
            if moonrise < moonset:
                moon_up = moonrise <= hour < moonset
            else:
                moon_up = hour >= moonrise or hour < moonset
        if moon_up:
            if hour - moonrise < 1 and hour - moonrise >= 0:
                color = MOONRISE_COLOR
            else:
                color = tuple(np.mean([color, MOON_COLOR], axis=0).astype(int))
        day_pixels.append(color)
    return day_pixels

running = True
frame = 0
total_days = min(len(sun_df), len(moon_df))
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            running = False
            break
    screen.fill(BG_COLOR)
    # Draw current day's pixels as a grid
    day_pixels = get_day_pixels(frame)
    for hour in range(IMG_WIDTH):
        color = day_pixels[hour]
        rect = pygame.Rect(hour * PIXEL_SIZE, 0, PIXEL_SIZE, screen_height)
        pygame.draw.rect(screen, color, rect)
    pygame.display.flip()
    frame += 1
    if frame >= total_days:
        frame = 0  # Loop animation
    clock.tick(2)  # 2 FPS, adjust for speed

pygame.quit()
sys.exit()
