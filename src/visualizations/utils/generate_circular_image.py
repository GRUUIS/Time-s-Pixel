"""
Generate a static circular visualization image for Time's Pixel
Creates a high-quality circular representation saved as PNG
"""
import pygame
import math
import sys
from datetime import datetime

# Import our enhanced modules
try:
    from src.core.twilight_calculator import AdvancedSkyPalette, TwilightCalculator
    from src.core.time_utils import load_astronomical_data, get_day_data, hour_to_time
    from src.core.moon_phases import MoonPhaseCalculator, EnhancedMoonVisualizer
    from src.core.color_palettes import create_palette
    from src.core.seasonal_markers import SeasonalMarkerRenderer, AstronomicalEvents
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

def generate_static_circular_visualization():
    """Generate and save a static circular visualization."""
    pygame.init()
    
    # High resolution for static image
    size = 1200
    center_x = size // 2
    center_y = size // 2
    inner_radius = size // 6
    outer_radius = size // 2 - 60
    
    # Create surface
    surface = pygame.Surface((size, size))
    surface.fill((20, 20, 30))  # Dark background
    
    # Colors
    colors = {
        'month_markers': (80, 80, 100),
        'season_markers': (120, 120, 140),
        'text': (180, 180, 200),
        'seasonal_events': {
            'spring': (100, 255, 100),
            'summer': (255, 255, 100),
            'fall': (255, 150, 100),
            'winter': (150, 150, 255)
        }
    }
    
    # Initialize astronomical systems
    sky_palette = AdvancedSkyPalette()
    moon_calculator = MoonPhaseCalculator()
    moon_visualizer = EnhancedMoonVisualizer()
    twilight_calculator = TwilightCalculator()
    
    # Initialize seasonal markers
    seasonal_renderer = SeasonalMarkerRenderer()
    astronomical_events = AstronomicalEvents()
    moon_visualizer = EnhancedMoonVisualizer()
    
    # Load data
    print("Loading astronomical data...")
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None:
        print("Failed to load data!")
        return
    
    # Generate and draw pixels
    print("Generating circular pixel layout...")
    total_days = min(len(sun_df), len(moon_df))
    
    # Draw data points in circular pattern
    for day_idx in range(total_days):
        day_data = get_day_data(sun_df, moon_df, day_idx)
        
        if day_data:
            # Calculate angle for this day
            day_of_year = day_data['day_of_year'] or (day_idx + 1)
            angle = (day_of_year - 1) / 366 * 360 - 90  # Start from top
            
            # Generate colors for each hour
            for hour in range(24):
                # Get sky color
                sky_color = sky_palette.get_advanced_sky_color(
                    hour, day_data['sunrise'], day_data['sunset'], 
                    day_data['date'] or "2024-01-01", day_of_year
                )
                
                # Add moon influence if visible
                if day_data['moonrise'] and day_data['moonset'] and day_data['date']:
                    moon_up = False
                    if day_data['moonrise'] < day_data['moonset']:
                        moon_up = day_data['moonrise'] <= hour < day_data['moonset']
                    else:
                        moon_up = hour >= day_data['moonrise'] or hour < day_data['moonset']
                    
                    if moon_up:
                        moon_color = moon_visualizer.get_moon_color_by_phase(day_data['date'])
                        illumination = moon_calculator.get_moon_illumination(day_data['date'])
                        opacity = 0.1 + (illumination * 0.3)
                        
                        # Blend colors
                        r_sky, g_sky, b_sky = sky_color
                        r_moon, g_moon, b_moon = moon_color
                        
                        r = int(r_sky * (1 - opacity) + r_moon * opacity)
                        g = int(g_sky * (1 - opacity) + g_moon * opacity)
                        b = int(b_sky * (1 - opacity) + b_moon * opacity)
                        sky_color = (r, g, b)
                
                # Calculate radius based on hour (midnight outer, noon inner)
                hour_progress = hour / 24
                radius_factor = 1.0 - (0.2 * math.sin(math.pi * hour_progress))
                radius = inner_radius + (radius_factor * (outer_radius - inner_radius))
                
                # Convert to cartesian coordinates
                angle_rad = math.radians(angle)
                x = center_x + radius * math.cos(angle_rad)
                y = center_y + radius * math.sin(angle_rad)
                
                # Draw pixel as small circle
                pygame.draw.circle(surface, sky_color, (int(x), int(y)), 2)
        
        if (day_idx + 1) % 50 == 0:
            print(f"Processed {day_idx + 1}/{total_days} days...")
    
    # Draw grid and labels
    print("Adding grid and labels...")
    
    # Month markers
    month_days = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
             "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    
    font = pygame.font.Font(None, 20)
    
    for month_idx, day_start in enumerate(month_days):
        angle = (day_start - 1) / 366 * 360 - 90
        angle_rad = math.radians(angle)
        
        # Draw radial line
        inner_x = center_x + inner_radius * math.cos(angle_rad)
        inner_y = center_y + inner_radius * math.sin(angle_rad)
        outer_x = center_x + outer_radius * math.cos(angle_rad)
        outer_y = center_y + outer_radius * math.sin(angle_rad)
        
        pygame.draw.line(surface, colors['month_markers'], 
                        (inner_x, inner_y), (outer_x, outer_y), 1)
        
        # Draw month label
        label_radius = outer_radius + 30
        label_x = center_x + label_radius * math.cos(angle_rad)
        label_y = center_y + label_radius * math.sin(angle_rad)
        
        text = font.render(months[month_idx], True, colors['text'])
        text_rect = text.get_rect(center=(label_x, label_y))
        surface.blit(text, text_rect)
    
    # Enhanced seasonal markers with comprehensive astronomical events
    print("Adding seasonal markers...")
    all_events = seasonal_renderer.get_events_for_visualization()
    
    for event in all_events:
        # Calculate day of year from date
        day_of_year = astronomical_events.calculate_day_of_year(event['date'])
        
        # Convert to angle
        angle = (day_of_year - 1) / 366 * 360 - 90
        angle_rad = math.radians(angle)
        
        # Position based on importance
        if event['importance'] == 'high':
            marker_radius = outer_radius + 20
            label_radius = outer_radius + 55
            marker_size = 10
        elif event['importance'] == 'medium':
            marker_radius = outer_radius + 12
            label_radius = outer_radius + 45
            marker_size = 7
        else:
            marker_radius = outer_radius + 6
            label_radius = outer_radius + 35
            marker_size = 4
        
        # Calculate position
        x = center_x + marker_radius * math.cos(angle_rad)
        y = center_y + marker_radius * math.sin(angle_rad)
        
        # Draw glow effect for high importance events
        if event['importance'] == 'high':
            for r in range(15, 0, -2):
                alpha = int(50 * (1 - r / 15) ** 2)
                glow_color = (*event['color'], alpha)
                # Note: pygame doesn't support per-pixel alpha easily in this context
                # So we'll just draw the marker with extra prominence
        
        # Draw main marker
        pygame.draw.circle(surface, event['color'], (int(x), int(y)), marker_size)
        pygame.draw.circle(surface, (255, 255, 255), (int(x), int(y)), marker_size, 2)
        
        # Draw label for important events
        if event['importance'] in ['high', 'medium']:
            text = font.render(event['name'], True, event['color'])
            label_x = center_x + label_radius * math.cos(angle_rad)
            label_y = center_y + label_radius * math.sin(angle_rad)
            text_rect = text.get_rect(center=(label_x, label_y))
            
            # Add text shadow for better readability
            shadow = font.render(event['name'], True, (0, 0, 0))
            shadow_rect = text_rect.copy()
            shadow_rect.x += 1
            shadow_rect.y += 1
            surface.blit(shadow, shadow_rect)
            surface.blit(text, text_rect)
    
    # Draw concentric circles for hour references
    for hour in [0, 6, 12, 18]:
        hour_progress = hour / 24
        radius_factor = 1.0 - (0.2 * math.sin(math.pi * hour_progress))
        radius = inner_radius + (radius_factor * (outer_radius - inner_radius))
        pygame.draw.circle(surface, colors['month_markers'], 
                         (center_x, center_y), int(radius), 1)
    
    # Draw center circle with title
    pygame.draw.circle(surface, (40, 40, 60), (center_x, center_y), inner_radius)
    
    title_font = pygame.font.Font(None, 36)
    subtitle_font = pygame.font.Font(None, 24)
    
    title = title_font.render("Time's Pixel", True, colors['text'])
    subtitle = subtitle_font.render("Circular View 2024", True, colors['text'])
    
    title_rect = title.get_rect(center=(center_x, center_y - 20))
    subtitle_rect = subtitle.get_rect(center=(center_x, center_y + 10))
    
    surface.blit(title, title_rect)
    surface.blit(subtitle, subtitle_rect)
    
    # Save the image
    filename = "circular_time_visualization.png"
    pygame.image.save(surface, filename)
    print(f"\n>>> Circular visualization saved as '{filename}'")
    print(f"Image size: {size}x{size} pixels")
    
    pygame.quit()
    return filename

if __name__ == "__main__":
    print("🎨 GENERATING STATIC CIRCULAR VISUALIZATION")
    print("="*50)
    
    try:
        filename = generate_static_circular_visualization()
        print(f"\n🌟 Success! Check out your circular Time's Pixel visualization!")
        print(f"File: {filename}")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)