"""
Circular Layout Visualization for Time's Pixel
Creates a radial/circular representation of the year with astronomical data.
Days are arranged in a circle, hours radiate inward/outward from center.
"""
import pygame
import math
import sys
import os
from datetime import datetime

# Add project root to Python path for imports
project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Import our enhanced modules
try:
    from src.core.twilight_calculator import AdvancedSkyPalette, TwilightCalculator
    from src.core.time_utils import load_astronomical_data, get_day_data, hour_to_time
    from src.core.moon_phases import MoonPhaseCalculator, EnhancedMoonVisualizer
    from src.core.color_palettes import create_palette
    from src.core.seasonal_markers import SeasonalMarkerRenderer, SeasonalMarkerInfo, AstronomicalEvents
except ImportError as e:
    print(f"Error importing modules: {e}")
    print(f"Project root: {project_root}")
    print(f"Python path: {sys.path}")
    sys.exit(1)

class CircularTimeMapper:
    """Handles coordinate transformations between day/hour and polar coordinates."""
    
    def __init__(self, center_x, center_y, inner_radius, outer_radius):
        self.center_x = center_x
        self.center_y = center_y
        self.inner_radius = inner_radius
        self.outer_radius = outer_radius
        self.radius_range = outer_radius - inner_radius
    
    def day_to_angle(self, day_of_year):
        """Convert day of year (1-366) to angle in degrees."""
        # Start from top (12 o'clock), go clockwise
        angle = (day_of_year - 1) / 366 * 360 - 90
        return angle
    
    def hour_to_radius(self, hour):
        """Convert hour (0-23) to radius from center."""
        # Midnight (0) at outer edge, noon (12) closer to center
        hour_progress = hour / 24
        # Create a subtle radial variation - outer for night, inner for day
        radius_factor = 1.0 - (0.3 * math.sin(math.pi * hour_progress))
        return self.inner_radius + (radius_factor * self.radius_range)
    
    def polar_to_cartesian(self, angle_deg, radius):
        """Convert polar coordinates to cartesian (x, y)."""
        angle_rad = math.radians(angle_deg)
        x = self.center_x + radius * math.cos(angle_rad)
        y = self.center_y + radius * math.sin(angle_rad)
        return int(x), int(y)
    
    def cartesian_to_polar(self, x, y):
        """Convert cartesian coordinates back to polar (angle, radius)."""
        dx = x - self.center_x
        dy = y - self.center_y
        radius = math.sqrt(dx*dx + dy*dy)
        angle_rad = math.atan2(dy, dx)
        angle_deg = math.degrees(angle_rad)
        return angle_deg, radius
    
    def get_day_hour_from_mouse(self, mouse_x, mouse_y):
        """Convert mouse position to day and hour."""
        angle, radius = self.cartesian_to_polar(mouse_x, mouse_y)
        
        # Check if within valid radius range
        if radius < self.inner_radius or radius > self.outer_radius:
            return None, None
        
        # Convert angle to day (add 90 to adjust for starting at top)
        day_angle = (angle + 90) % 360
        day_of_year = int((day_angle / 360) * 366) + 1
        day_of_year = max(1, min(366, day_of_year))
        
        # Convert radius to hour (approximate)
        radius_factor = (radius - self.inner_radius) / self.radius_range
        # Reverse the hour calculation
        hour_progress = math.asin(max(-1, min(1, (1.0 - radius_factor) / 0.3))) / math.pi
        hour = int(hour_progress * 24)
        hour = max(0, min(23, hour))
        
        return day_of_year - 1, hour  # Return 0-based day index

class CircularVisualization:
    """Main circular visualization class with interactive features."""
    
    def __init__(self):
        pygame.init()
        
        # Get screen dimensions
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Window configuration - make it square for circular design
        size = min(self.screen_width - 100, self.screen_height - 100, 1000)
        self.window_size = size
        self.center_x = size // 2
        self.center_y = size // 2
        
        # Circular layout parameters
        self.inner_radius = size // 6      # Inner circle
        self.outer_radius = size // 2 - 50 # Outer circle with margin
        self.middle_radius = (self.inner_radius + self.outer_radius) // 2
        
        # Create screen
        self.screen = pygame.display.set_mode((self.window_size, self.window_size))
        pygame.display.set_caption("Time's Pixel - Circular View")
        
        # Initialize coordinate mapper
        self.mapper = CircularTimeMapper(
            self.center_x, self.center_y, 
            self.inner_radius, self.outer_radius
        )
        
        # Colors
        self.colors = {
            'background': (20, 20, 30),
            'center_circle': (40, 40, 60),
            'month_markers': (100, 100, 120),
            'season_markers': (150, 150, 180),
            'text': (200, 200, 220),
            'highlight': (255, 255, 100),
            'hover': (255, 200, 100)
        }
        
        # Fonts
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 18)
        self.font_small = pygame.font.Font(None, 14)
        
        # Initialize astronomical systems
        self.sky_palette = AdvancedSkyPalette()
        self.moon_calculator = MoonPhaseCalculator()
        self.moon_visualizer = EnhancedMoonVisualizer()
        self.twilight_calculator = TwilightCalculator()
        
        # Initialize seasonal markers system
        self.seasonal_renderer = SeasonalMarkerRenderer()
        self.seasonal_info = SeasonalMarkerInfo()
        self.astronomical_events = AstronomicalEvents()
        self.show_seasonal_markers = True  # Toggle for seasonal markers display
        
        # Interaction state
        self.hover_day = None
        self.hover_hour = None
        self.selected_day = None
        self.selected_hour = None
        self.rotation_offset = 0  # For rotating the entire circle
        
        # Load astronomical data
        print("Loading astronomical data for circular visualization...")
        self.sun_df, self.moon_df = load_astronomical_data()
        if self.sun_df is None:
            print("Failed to load data files!")
            sys.exit(1)
        
        # Pre-generate pixel data for smooth rendering
        print("Pre-generating pixel colors for circular layout...")
        self.generate_circular_pixels()
        
        print(f"Circular visualization ready!")
        print(f"Window: {self.window_size}x{self.window_size}")
        print(f"Inner radius: {self.inner_radius}, Outer radius: {self.outer_radius}")
    
    def generate_circular_pixels(self):
        """Pre-generate colors for all day/hour combinations."""
        self.pixel_colors = []
        total_days = min(len(self.sun_df), len(self.moon_df))
        
        for day_idx in range(total_days):
            day_data = get_day_data(self.sun_df, self.moon_df, day_idx)
            day_colors = []
            
            if day_data:
                for hour in range(24):
                    # Get sky color using our advanced palette
                    sky_color = self.sky_palette.get_advanced_sky_color(
                        hour, day_data['sunrise'], day_data['sunset'], 
                        day_data['date'] or "2024-01-01", day_data['day_of_year'] or 1
                    )
                    
                    # Add moon influence if visible
                    moon_up = self.is_moon_visible(hour, day_data['moonrise'], day_data['moonset'])
                    if moon_up and day_data['date']:
                        moon_color = self.moon_visualizer.get_moon_color_by_phase(day_data['date'])
                        illumination = self.moon_calculator.get_moon_illumination(day_data['date'])
                        opacity = 0.1 + (illumination * 0.3)
                        sky_color = self.blend_colors(sky_color, moon_color, opacity)
                    
                    day_colors.append(sky_color)
            else:
                # Default colors for missing data
                day_colors = [(30, 30, 60)] * 24
            
            self.pixel_colors.append(day_colors)
            
            if (day_idx + 1) % 50 == 0:
                print(f"Generated colors for {day_idx + 1}/{total_days} days...")
    
    def is_moon_visible(self, hour, moonrise, moonset):
        """Check if moon is visible at given hour."""
        if moonrise is None or moonset is None:
            return False
        
        if moonrise < moonset:
            return moonrise <= hour < moonset
        else:
            return hour >= moonrise or hour < moonset
    
    def blend_colors(self, base_color, overlay_color, opacity):
        """Blend two colors with given opacity."""
        opacity = max(0, min(1, opacity))
        r_base, g_base, b_base = base_color
        r_over, g_over, b_over = overlay_color
        
        r = int(r_base * (1 - opacity) + r_over * opacity)
        g = int(g_base * (1 - opacity) + g_over * opacity)
        b = int(b_base * (1 - opacity) + b_over * opacity)
        
        return (r, g, b)
    
    def draw_circular_visualization(self):
        """Draw the main circular time visualization."""
        # Sample points around the circle for rendering
        angle_step = 2  # degrees between samples
        
        for angle in range(0, 360, angle_step):
            adjusted_angle = (angle + self.rotation_offset) % 360
            day_of_year = int((adjusted_angle / 360) * 366) + 1
            day_index = min(day_of_year - 1, len(self.pixel_colors) - 1)
            
            if day_index >= 0 and day_index < len(self.pixel_colors):
                day_colors = self.pixel_colors[day_index]
                
                # Draw hour segments for this day
                for hour in range(0, 24, 2):  # Sample every 2 hours for performance
                    if hour < len(day_colors):
                        color = day_colors[hour]
                        
                        # Calculate position
                        radius = self.mapper.hour_to_radius(hour)
                        x, y = self.mapper.polar_to_cartesian(adjusted_angle, radius)
                        
                        # Draw a small circle for each data point
                        point_size = 2
                        pygame.draw.circle(self.screen, color, (x, y), point_size)
    
    def draw_circular_grid(self):
        """Draw grid lines and markers for the circular layout."""
        # Draw concentric circles for hour markers
        for hour in [0, 6, 12, 18]:
            radius = self.mapper.hour_to_radius(hour)
            pygame.draw.circle(self.screen, self.colors['center_circle'], 
                             (self.center_x, self.center_y), int(radius), 1)
        
        # Draw radial lines for months
        month_days = [1, 32, 60, 91, 121, 152, 182, 213, 244, 274, 305, 335]  # Approximate month starts
        for month, day_start in enumerate(month_days):
            angle = self.mapper.day_to_angle(day_start) + self.rotation_offset
            
            # Draw line from inner to outer radius
            inner_x, inner_y = self.mapper.polar_to_cartesian(angle, self.inner_radius)
            outer_x, outer_y = self.mapper.polar_to_cartesian(angle, self.outer_radius)
            pygame.draw.line(self.screen, self.colors['month_markers'], 
                           (inner_x, inner_y), (outer_x, outer_y), 1)
            
            # Draw month labels
            label_radius = self.outer_radius + 20
            label_x, label_y = self.mapper.polar_to_cartesian(angle, label_radius)
            
            months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", 
                     "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
            text = self.font_small.render(months[month], True, self.colors['text'])
            text_rect = text.get_rect(center=(label_x, label_y))
            self.screen.blit(text, text_rect)
    
    def draw_seasonal_markers(self):
        """Draw enhanced seasonal markers with astronomical events."""
        if not self.show_seasonal_markers:
            return
        
        # Update animation for breathing effect
        self.seasonal_renderer.update_animation(0.016)  # ~60 FPS delta
        
        # Get all astronomical events
        all_events = self.seasonal_renderer.get_events_for_visualization()
        
        for event in all_events:
            # Calculate day of year from date
            day_of_year = self.astronomical_events.calculate_day_of_year(event['date'])
            
            # Convert to angle with rotation offset
            angle = self.mapper.day_to_angle(day_of_year) + self.rotation_offset
            
            # Position marker based on importance
            if event['importance'] == 'high':
                marker_radius = self.outer_radius + 15
                label_radius = self.outer_radius + 45
            elif event['importance'] == 'medium':
                marker_radius = self.outer_radius + 8
                label_radius = self.outer_radius + 35
            else:
                marker_radius = self.outer_radius + 3
                label_radius = self.outer_radius + 25
            
            # Get marker position
            x, y = self.mapper.polar_to_cartesian(angle, marker_radius)
            
            # Render enhanced marker with glow effect
            self.seasonal_renderer.render_marker(self.screen, x, y, event)
            
            # Render label for high importance events or when hovering nearby
            if event['importance'] == 'high' or self.is_near_marker(x, y):
                self.seasonal_renderer.render_marker_label(
                    self.screen, x, y, event, self.font_small
                )
    
    def is_near_marker(self, marker_x, marker_y, threshold=50):
        """Check if mouse is near a marker position."""
        if hasattr(self, 'mouse_pos'):
            mouse_x, mouse_y = self.mouse_pos
            distance = math.sqrt((mouse_x - marker_x)**2 + (mouse_y - marker_y)**2)
            return distance < threshold
        return False
    
    def draw_center_info(self):
        """Draw information in the center circle."""
        # Background circle
        pygame.draw.circle(self.screen, self.colors['center_circle'], 
                         (self.center_x, self.center_y), self.inner_radius)
        
        # Title
        title = self.font_large.render("Time's Pixel", True, self.colors['text'])
        title_rect = title.get_rect(center=(self.center_x, self.center_y - 40))
        self.screen.blit(title, title_rect)
        
        subtitle = self.font_medium.render("Circular View", True, self.colors['text'])
        subtitle_rect = subtitle.get_rect(center=(self.center_x, self.center_y - 20))
        self.screen.blit(subtitle, subtitle_rect)
        
        # Current selection info
        if self.selected_day is not None and self.selected_hour is not None:
            day_data = get_day_data(self.sun_df, self.moon_df, self.selected_day)
            if day_data:
                date_text = f"{day_data['date']}"
                hour_text = f"{self.selected_hour:02d}:00"
                
                date_surface = self.font_small.render(date_text, True, self.colors['highlight'])
                hour_surface = self.font_small.render(hour_text, True, self.colors['highlight'])
                
                date_rect = date_surface.get_rect(center=(self.center_x, self.center_y + 10))
                hour_rect = hour_surface.get_rect(center=(self.center_x, self.center_y + 25))
                
                self.screen.blit(date_surface, date_rect)
                self.screen.blit(hour_surface, hour_rect)
        
        # Instructions
        instructions = ["Click to select", "R - Rotate", "ESC - Exit"]
        for i, instruction in enumerate(instructions):
            text = self.font_small.render(instruction, True, self.colors['text'])
            text_rect = text.get_rect(center=(self.center_x, self.center_y + 50 + i * 15))
            self.screen.blit(text, text_rect)
    
    def handle_mouse_motion(self, mouse_pos):
        """Handle mouse movement for hover effects."""
        self.mouse_pos = mouse_pos  # Store for marker proximity detection
        day, hour = self.mapper.get_day_hour_from_mouse(*mouse_pos)
        self.hover_day = day
        self.hover_hour = hour
    
    def handle_mouse_click(self, mouse_pos):
        """Handle mouse clicks for selection."""
        day, hour = self.mapper.get_day_hour_from_mouse(*mouse_pos)
        if day is not None and hour is not None:
            self.selected_day = day
            self.selected_hour = hour
            
            # Print info to console
            day_data = get_day_data(self.sun_df, self.moon_df, day)
            if day_data:
                print(f"\nSelected: {day_data['date']} at {hour:02d}:00")
                if day_data['date']:
                    phase = self.moon_calculator.get_moon_phase_name(day_data['date'])
                    illumination = self.moon_calculator.get_moon_illumination(day_data['date'])
                    print(f"Moon: {phase} ({illumination:.1%} illuminated)")
    
    def handle_key_press(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_r:
            # Rotate the visualization
            self.rotation_offset = (self.rotation_offset + 30) % 360
            print(f"Rotated to {self.rotation_offset} degrees")
        elif key == pygame.K_LEFT:
            self.rotation_offset = (self.rotation_offset - 10) % 360
        elif key == pygame.K_RIGHT:
            self.rotation_offset = (self.rotation_offset + 10) % 360
        elif key == pygame.K_s:
            # Toggle seasonal markers
            self.show_seasonal_markers = not self.show_seasonal_markers
            status = "ON" if self.show_seasonal_markers else "OFF"
            print(f"Seasonal markers: {status}")
        
        return True
    
    def run(self):
        """Main application loop."""
        clock = pygame.time.Clock()
        running = True
        
        print("\n🎮 CIRCULAR VISUALIZATION STARTED")
        print("Controls:")
        print("  • Click any point to select day/hour")
        print("  • R - Rotate 30 degrees")
        print("  • ← → - Fine rotation")
        print("  • S - Toggle seasonal markers")
        print("  • ESC - Exit")
        print(f"\nWindow: {self.window_size}x{self.window_size}")
        print(f"Radius range: {self.inner_radius} to {self.outer_radius}")
        print(f"Seasonal markers: {'ON' if self.show_seasonal_markers else 'OFF'}")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_key_press(event.key)
                
                elif event.type == pygame.MOUSEMOTION:
                    self.handle_mouse_motion(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        self.handle_mouse_click(event.pos)
            
            # Clear screen
            self.screen.fill(self.colors['background'])
            
            # Draw all components
            self.draw_circular_visualization()
            self.draw_circular_grid()
            self.draw_seasonal_markers()
            self.draw_center_info()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS
        
        pygame.quit()

if __name__ == "__main__":
    print("🌀 LAUNCHING CIRCULAR TIME'S PIXEL VISUALIZATION")
    print("="*55)
    
    try:
        app = CircularVisualization()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)
    
    print("Thank you for exploring circular time! 🌌")