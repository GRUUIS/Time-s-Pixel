"""
Static Hong Kong Time-lapse Preview Generator
Creates preview images showing Hong Kong skyline at different times of day.
Demonstrates the time-lapse effect without full animation.
"""
import pygame
import sys
from datetime import datetime, timedelta

# Import our time-lapse components
try:
    from ..timelapse_visualization import HongKongSkylineRenderer, SkyAnimationEngine
except ImportError as e:
    print(f"Error importing time-lapse modules: {e}")
    print("Trying absolute import...")
    try:
        import sys
        import os
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
        sys.path.insert(0, project_root)
        from src.visualizations.timelapse_visualization import HongKongSkylineRenderer, SkyAnimationEngine
    except ImportError as e2:
        print(f"Absolute import also failed: {e2}")
        sys.exit(1)

def generate_timelapse_preview():
    """Generate a preview showing Hong Kong skyline at 6 different times."""
    pygame.init()
    
    # Image configuration
    single_width = 400
    single_height = 300
    cols = 3
    rows = 2
    total_width = single_width * cols
    total_height = single_height * rows
    
    # Create large surface for composite image
    composite_surface = pygame.Surface((total_width, total_height))
    composite_surface.fill((0, 0, 0))
    
    # Time points to capture
    time_points = [
        (1, 6.0, "Dawn"),         # Day 1, 6:00 AM
        (1, 12.0, "Noon"),        # Day 1, 12:00 PM  
        (1, 18.0, "Dusk"),        # Day 1, 6:00 PM
        (100, 2.0, "Night"),      # Day 100, 2:00 AM
        (200, 14.0, "Summer"),    # Day 200, 2:00 PM
        (300, 20.0, "Autumn")     # Day 300, 8:00 PM
    ]
    
    print("Generating Hong Kong time-lapse preview...")
    
    for i, (day, hour, label) in enumerate(time_points):
        print(f"Rendering {label}...")
        
        # Calculate grid position
        col = i % cols
        row = i // cols
        x_offset = col * single_width
        y_offset = row * single_height
        
        # Create individual frame surface
        frame_surface = pygame.Surface((single_width, single_height))
        
        # Initialize renderers for this frame
        skyline = HongKongSkylineRenderer(single_width, single_height)
        sky_engine = SkyAnimationEngine(single_width, single_height)
        
        # Set specific time
        sky_engine.set_time(day, hour)
        
        # Render sky background
        sky_engine.render_sky_gradient(frame_surface)
        
        # Render celestial bodies
        sky_engine.render_celestial_bodies(frame_surface)
        
        # Render Hong Kong skyline
        skyline.render_skyline(frame_surface, sky_engine.is_night_time())
        
        # Add label overlay
        font = pygame.font.Font(None, 24)
        text_surface = font.render(label, True, (255, 255, 255))
        text_bg = pygame.Surface((text_surface.get_width() + 10, text_surface.get_height() + 6))
        text_bg.fill((0, 0, 0))
        text_bg.set_alpha(128)
        
        frame_surface.blit(text_bg, (10, 10))
        frame_surface.blit(text_surface, (15, 13))
        
        # Add time info
        time_info = f"Day {day}, {int(hour):02d}:{int((hour % 1) * 60):02d}"
        time_surface = pygame.font.Font(None, 18).render(time_info, True, (200, 200, 200))
        frame_surface.blit(time_surface, (15, 35))
        
        # Blit frame to composite
        composite_surface.blit(frame_surface, (x_offset, y_offset))
    
    # Add title
    title_font = pygame.font.Font(None, 36)
    title_text = title_font.render("Hong Kong Time-lapse Preview", True, (255, 255, 255))
    title_bg = pygame.Surface((title_text.get_width() + 20, title_text.get_height() + 10))
    title_bg.fill((0, 0, 0))
    title_bg.set_alpha(180)
    
    title_x = (total_width - title_text.get_width()) // 2
    composite_surface.blit(title_bg, (title_x - 10, 10))
    composite_surface.blit(title_text, (title_x, 15))
    
    # Save composite image
    filename = "hongkong_timelapse_preview.png"
    pygame.image.save(composite_surface, filename)
    
    print(f"\nHong Kong time-lapse preview saved as '{filename}'")
    print(f"Image size: {total_width}x{total_height} pixels")
    print("Shows 6 different times of day across seasons")
    
    pygame.quit()

def generate_single_frame(day: int = 1, hour: float = 12.0, filename: str = None):
    """Generate a single high-quality frame of the Hong Kong skyline."""
    pygame.init()
    
    # High resolution for single frame
    width = 1920
    height = 1080
    
    # Create surface
    surface = pygame.Surface((width, height))
    
    # Initialize renderers
    skyline = HongKongSkylineRenderer(width, height)
    sky_engine = SkyAnimationEngine(width, height)
    
    # Set time
    sky_engine.set_time(day, hour)
    
    print(f"Generating single frame: Day {day}, {hour:.1f} hours...")
    
    # Render components
    sky_engine.render_sky_gradient(surface)
    sky_engine.render_celestial_bodies(surface)
    skyline.render_skyline(surface, sky_engine.is_night_time())
    
    # Add subtle title
    font = pygame.font.Font(None, 48)
    title = f"Hong Kong Time's Pixel - Day {day}"
    text_surface = font.render(title, True, (255, 255, 255, 150))
    
    # Position title in bottom right
    text_x = width - text_surface.get_width() - 30
    text_y = height - text_surface.get_height() - 30
    
    # Semi-transparent background
    text_bg = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
    text_bg.fill((0, 0, 0))
    text_bg.set_alpha(100)
    surface.blit(text_bg, (text_x - 10, text_y - 5))
    
    # Blit title
    surface.blit(text_surface, (text_x, text_y))
    
    # Save image
    if filename is None:
        filename = f"hongkong_day{day}_hour{hour:.0f}.png"
    
    pygame.image.save(surface, filename)
    print(f"High-resolution frame saved as '{filename}'")
    print(f"Image size: {width}x{height} pixels")
    
    pygame.quit()

def main():
    """Main function for preview generation."""
    print("Hong Kong Time-lapse Preview Generator")
    print("=====================================")
    
    # Generate preview grid
    generate_timelapse_preview()
    
    # Generate a few high-quality single frames
    print("\nGenerating high-quality sample frames...")
    generate_single_frame(1, 6.0, "hongkong_dawn.png")      # Dawn
    generate_single_frame(150, 14.0, "hongkong_summer.png") # Summer afternoon
    generate_single_frame(300, 20.0, "hongkong_autumn.png") # Autumn evening
    
    print("\nPreview generation complete!")
    print("Files created:")
    print("  - hongkong_timelapse_preview.png (6-panel overview)")
    print("  - hongkong_dawn.png (high-res dawn)")
    print("  - hongkong_summer.png (high-res summer)")
    print("  - hongkong_autumn.png (high-res autumn)")

if __name__ == "__main__":
    main()