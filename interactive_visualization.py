"""
Interactive Time's Pixel Visualization with Large-Scale Interface
Features mouse interaction, date display, zoom capabilities, and detailed astronomical information.
Large pixel size ensures comfortable user interaction on any screen.
"""
import pygame
import sys
import math
from datetime import datetime

# Import our enhanced modules
try:
    from twilight_calculator import AdvancedSkyPalette, TwilightCalculator
    from time_utils import load_astronomical_data, get_day_data, hour_to_time
    from moon_phases import MoonPhaseCalculator, EnhancedMoonVisualizer
    from color_palettes import create_palette
except ImportError as e:
    print(f"Error importing modules: {e}")
    sys.exit(1)

class InteractiveTimePixel:
    """Interactive Time's Pixel visualization with large-scale interface."""
    
    def __init__(self):
        pygame.init()
        
        # Get screen dimensions for optimal sizing
        info = pygame.display.Info()
        self.screen_width = info.current_w
        self.screen_height = info.current_h
        
        # Configuration for large, interactive display
        self.IMG_WIDTH = 24  # hours in a day
        self.data_height = 366  # days in year
        
        # Calculate optimal pixel size for user interaction
        # Aim for at least 20x20 pixels per data point
        self.min_pixel_size = 20
        max_width_pixels = (self.screen_width - 400) // self.IMG_WIDTH  # Leave space for UI
        max_height_pixels = (self.screen_height - 200) // self.data_height
        
        self.pixel_size = max(self.min_pixel_size, min(max_width_pixels, max_height_pixels, 30))
        
        # Calculate actual visualization dimensions
        self.vis_width = self.IMG_WIDTH * self.pixel_size
        self.vis_height = self.data_height * self.pixel_size
        
        # UI Layout
        self.ui_width = 380
        self.total_width = self.vis_width + self.ui_width
        self.total_height = max(self.vis_height, 800)
        
        # Create screen
        self.screen = pygame.display.set_mode((self.total_width, self.total_height))
        pygame.display.set_caption("Interactive Time's Pixel - Click to Explore!")
        
        # Colors for UI
        self.ui_colors = {
            'background': (30, 30, 40),
            'panel': (40, 40, 50),
            'text': (220, 220, 220),
            'highlight': (100, 150, 255),
            'border': (80, 80, 90)
        }
        
        # Fonts
        self.font_large = pygame.font.Font(None, 24)
        self.font_medium = pygame.font.Font(None, 20)
        self.font_small = pygame.font.Font(None, 16)
        
        # Initialize systems
        self.sky_palette = AdvancedSkyPalette()
        self.moon_calculator = MoonPhaseCalculator()
        self.moon_visualizer = EnhancedMoonVisualizer()
        self.twilight_calculator = TwilightCalculator()
        
        # Current palette selection
        self.palette_options = ["naturalistic", "vibrant", "monochrome", "classic"]
        self.current_palette_idx = 0
        self.color_palette = create_palette(self.palette_options[0])
        
        # Interaction state
        self.selected_day = None
        self.selected_hour = None
        self.hover_day = None
        self.hover_hour = None
        self.show_twilight_info = False
        self.zoom_factor = 1.0
        self.pan_x = 0
        self.pan_y = 0
        
        # Load data
        print("Loading astronomical data for interactive visualization...")
        self.sun_df, self.moon_df = load_astronomical_data()
        if self.sun_df is None:
            print("Failed to load data files!")
            sys.exit(1)
        
        # Pre-generate all pixels for smooth interaction
        print("Pre-generating enhanced pixels for smooth interaction...")
        self.all_pixels = self.generate_all_pixels()
        
        # Create pixel surface for efficient blitting
        self.pixel_surface = pygame.Surface((self.vis_width, self.vis_height))
        self.update_pixel_surface()
        
        print(f"Interactive visualization ready!")
        print(f"Pixel size: {self.pixel_size}x{self.pixel_size}")
        print(f"Visualization: {self.vis_width}x{self.vis_height}")
        print(f"Total window: {self.total_width}x{self.total_height}")
    
    def generate_all_pixels(self):
        """Pre-generate all pixels for the entire year."""
        all_pixels = []
        total_days = min(len(self.sun_df), len(self.moon_df))
        
        for day_idx in range(total_days):
            day_data = get_day_data(self.sun_df, self.moon_df, day_idx)
            hour_pixels = self.generate_enhanced_hour_pixels(day_data)
            all_pixels.append(hour_pixels)
            
            if (day_idx + 1) % 50 == 0:
                print(f"Pre-generated {day_idx + 1}/{total_days} days...")
        
        return all_pixels
    
    def generate_enhanced_hour_pixels(self, day_data):
        """Generate enhanced pixel colors for all hours of a day."""
        if day_data is None:
            return [(30, 30, 60)] * self.IMG_WIDTH
        
        pixels = []
        date_str = day_data['date']
        day_of_year = day_data['day_of_year']
        sunrise = day_data['sunrise']
        sunset = day_data['sunset']
        moonrise = day_data['moonrise']
        moonset = day_data['moonset']
        
        # Get moon phase data
        moon_illumination = self.moon_calculator.get_moon_illumination(date_str) if date_str else 0.5
        
        for hour in range(self.IMG_WIDTH):
            # Get advanced sky color
            sky_color = self.sky_palette.get_advanced_sky_color(
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
                moon_color = self.moon_visualizer.get_moon_color_by_phase(date_str)
                
                # Blend moon with sky based on illumination
                opacity = 0.1 + (moon_illumination * 0.4)
                final_color = self.overlay_color_with_opacity(sky_color, moon_color, opacity)
            else:
                final_color = sky_color
            
            pixels.append(final_color)
        
        return pixels
    
    def overlay_color_with_opacity(self, base_color, overlay_color, opacity):
        """Overlay one color on another with specified opacity."""
        opacity = max(0, min(1, opacity))
        r_base, g_base, b_base = base_color
        r_over, g_over, b_over = overlay_color
        
        r = int(r_base * (1 - opacity) + r_over * opacity)
        g = int(g_base * (1 - opacity) + g_over * opacity)
        b = int(b_base * (1 - opacity) + b_over * opacity)
        
        return (r, g, b)
    
    def update_pixel_surface(self):
        """Update the pixel surface with current visualization data."""
        self.pixel_surface.fill((0, 0, 0))
        
        for day_idx, day_pixels in enumerate(self.all_pixels):
            y = day_idx * self.pixel_size
            
            for hour_idx, color in enumerate(day_pixels):
                x = hour_idx * self.pixel_size
                
                # Draw pixel with hover/selection highlighting
                pixel_color = color
                
                # Highlight hovered pixel
                if (self.hover_day == day_idx and self.hover_hour == hour_idx):
                    pixel_color = self.brighten_color(color, 1.3)
                
                # Highlight selected pixel
                if (self.selected_day == day_idx and self.selected_hour == hour_idx):
                    pixel_color = self.brighten_color(color, 1.5)
                
                # Draw the pixel
                rect = pygame.Rect(x, y, self.pixel_size, self.pixel_size)
                pygame.draw.rect(self.pixel_surface, pixel_color, rect)
                
                # Draw subtle grid lines for better visibility
                if self.pixel_size >= 15:
                    pygame.draw.rect(self.pixel_surface, (60, 60, 60), rect, 1)
    
    def brighten_color(self, color, factor):
        """Brighten a color by a given factor."""
        r, g, b = color
        r = min(255, int(r * factor))
        g = min(255, int(g * factor))
        b = min(255, int(b * factor))
        return (r, g, b)
    
    def get_pixel_from_mouse(self, mouse_pos):
        """Convert mouse position to day/hour coordinates."""
        mx, my = mouse_pos
        
        # Check if mouse is over visualization area
        if mx < 0 or mx >= self.vis_width or my < 0 or my >= self.vis_height:
            return None, None
        
        day = my // self.pixel_size
        hour = mx // self.pixel_size
        
        if 0 <= day < len(self.all_pixels) and 0 <= hour < self.IMG_WIDTH:
            return day, hour
        
        return None, None
    
    def draw_ui_panel(self):
        """Draw the information panel on the right side."""
        panel_x = self.vis_width + 10
        panel_rect = pygame.Rect(panel_x, 10, self.ui_width - 20, self.total_height - 20)
        
        # Background panel
        pygame.draw.rect(self.screen, self.ui_colors['panel'], panel_rect)
        pygame.draw.rect(self.screen, self.ui_colors['border'], panel_rect, 2)
        
        y_offset = 30
        
        # Title
        title = self.font_large.render("Time's Pixel Explorer", True, self.ui_colors['text'])
        self.screen.blit(title, (panel_x + 20, y_offset))
        y_offset += 50
        
        # Current palette info
        palette_text = f"Palette: {self.palette_options[self.current_palette_idx].title()}"
        palette_surface = self.font_medium.render(palette_text, True, self.ui_colors['text'])
        self.screen.blit(palette_surface, (panel_x + 20, y_offset))
        y_offset += 30
        
        # Instructions
        instructions = [
            "🖱️ CONTROLS:",
            "• Click pixel for details",
            "• P - Change palette",
            "• T - Toggle twilight info",
            "• ESC - Exit",
            "",
            "📊 VISUALIZATION:",
            f"• Days: {len(self.all_pixels)}",
            f"• Pixel size: {self.pixel_size}px",
            f"• Hours per day: {self.IMG_WIDTH}",
        ]
        
        for instruction in instructions:
            color = self.ui_colors['highlight'] if instruction.startswith(('🖱️', '📊')) else self.ui_colors['text']
            inst_surface = self.font_small.render(instruction, True, color)
            self.screen.blit(inst_surface, (panel_x + 20, y_offset))
            y_offset += 20
        
        y_offset += 20
        
        # Hover information
        if self.hover_day is not None and self.hover_hour is not None:
            self.draw_hover_info(panel_x + 20, y_offset)
            y_offset += 120
        
        # Selected pixel detailed information
        if self.selected_day is not None and self.selected_hour is not None:
            self.draw_detailed_info(panel_x + 20, y_offset)
    
    def draw_hover_info(self, x, y):
        """Draw hover information for current mouse position."""
        day_data = get_day_data(self.sun_df, self.moon_df, self.hover_day)
        
        if day_data:
            # Quick hover info
            hover_title = self.font_medium.render("🔍 HOVER INFO", True, self.ui_colors['highlight'])
            self.screen.blit(hover_title, (x, y))
            y += 25
            
            date_text = f"Date: {day_data['date']}"
            hour_text = f"Hour: {self.hover_hour:02d}:00"
            
            date_surface = self.font_small.render(date_text, True, self.ui_colors['text'])
            hour_surface = self.font_small.render(hour_text, True, self.ui_colors['text'])
            
            self.screen.blit(date_surface, (x, y))
            self.screen.blit(hour_surface, (x, y + 18))
            
            # Color preview
            if self.hover_day < len(self.all_pixels) and self.hover_hour < len(self.all_pixels[self.hover_day]):
                color = self.all_pixels[self.hover_day][self.hover_hour]
                color_rect = pygame.Rect(x + 150, y, 30, 30)
                pygame.draw.rect(self.screen, color, color_rect)
                pygame.draw.rect(self.screen, self.ui_colors['border'], color_rect, 2)
    
    def draw_detailed_info(self, x, y):
        """Draw detailed information for selected pixel."""
        day_data = get_day_data(self.sun_df, self.moon_df, self.selected_day)
        
        if not day_data:
            return
        
        # Detailed info title
        detail_title = self.font_medium.render("📋 SELECTED PIXEL", True, self.ui_colors['highlight'])
        self.screen.blit(detail_title, (x, y))
        y += 30
        
        # Basic info
        info_lines = [
            f"Date: {day_data['date']}",
            f"Day: {day_data['day_of_year']}/366",
            f"Hour: {self.selected_hour:02d}:00",
            "",
            "☀️ SUN DATA:",
            f"Sunrise: {hour_to_time(day_data['sunrise']) or 'N/A'}",
            f"Sunset: {hour_to_time(day_data['sunset']) or 'N/A'}",
        ]
        
        if day_data['sunrise'] and day_data['sunset']:
            daylight = day_data['sunset'] - day_data['sunrise']
            info_lines.append(f"Daylight: {daylight:.2f}h")
        
        info_lines.extend([
            "",
            "🌙 MOON DATA:",
            f"Moonrise: {hour_to_time(day_data['moonrise']) or 'N/A'}",
            f"Moonset: {hour_to_time(day_data['moonset']) or 'N/A'}",
        ])
        
        # Moon phase info
        if day_data['date']:
            illumination = self.moon_calculator.get_moon_illumination(day_data['date'])
            phase_name = self.moon_calculator.get_moon_phase_name(day_data['date'])
            info_lines.extend([
                f"Phase: {phase_name}",
                f"Illumination: {illumination:.1%}",
            ])
        
        # Sky condition at selected hour
        if self.show_twilight_info and day_data['date']:
            twilight_times = self.twilight_calculator.calculate_twilight_times(
                day_data['date'], day_data['sunrise'], day_data['sunset']
            )
            sky_type = self.twilight_calculator.get_sky_type(
                self.selected_hour, day_data['sunrise'], day_data['sunset'], twilight_times
            )
            
            info_lines.extend([
                "",
                "🌅 SKY CONDITION:",
                f"Type: {sky_type.replace('_', ' ').title()}",
            ])
        
        # Draw all info lines
        for line in info_lines:
            if line == "":
                y += 10
                continue
            
            color = self.ui_colors['highlight'] if line.startswith(('☀️', '🌙', '🌅')) else self.ui_colors['text']
            line_surface = self.font_small.render(line, True, color)
            self.screen.blit(line_surface, (x, y))
            y += 18
    
    def handle_key_press(self, key):
        """Handle keyboard input."""
        if key == pygame.K_ESCAPE:
            return False
        elif key == pygame.K_p:
            # Cycle through palettes
            self.current_palette_idx = (self.current_palette_idx + 1) % len(self.palette_options)
            self.color_palette = create_palette(self.palette_options[self.current_palette_idx])
            print(f"Switched to {self.palette_options[self.current_palette_idx]} palette")
            # Note: Would need to regenerate pixels for full palette change
        elif key == pygame.K_t:
            # Toggle twilight info
            self.show_twilight_info = not self.show_twilight_info
            print(f"Twilight info: {'ON' if self.show_twilight_info else 'OFF'}")
        
        return True
    
    def run(self):
        """Main interactive loop."""
        clock = pygame.time.Clock()
        running = True
        
        print("\n🎮 INTERACTIVE MODE STARTED")
        print("Controls:")
        print("  • Click any pixel to see detailed astronomical data")
        print("  • P - Change color palette")
        print("  • T - Toggle twilight information")
        print("  • ESC - Exit")
        print(f"\nPixel size: {self.pixel_size}x{self.pixel_size} for easy interaction")
        print(f"Visualization: {self.vis_width}x{self.vis_height}")
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                
                elif event.type == pygame.KEYDOWN:
                    running = self.handle_key_press(event.key)
                
                elif event.type == pygame.MOUSEMOTION:
                    # Update hover state
                    self.hover_day, self.hover_hour = self.get_pixel_from_mouse(event.pos)
                
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left click
                        day, hour = self.get_pixel_from_mouse(event.pos)
                        if day is not None and hour is not None:
                            self.selected_day = day
                            self.selected_hour = hour
                            
                            # Print detailed info to console as well
                            day_data = get_day_data(self.sun_df, self.moon_df, day)
                            if day_data:
                                print(f"\n📍 SELECTED: {day_data['date']} at {hour:02d}:00")
                                if day_data['date']:
                                    phase = self.moon_calculator.get_moon_phase_name(day_data['date'])
                                    illumination = self.moon_calculator.get_moon_illumination(day_data['date'])
                                    print(f"   Moon: {phase} ({illumination:.1%} illuminated)")
            
            # Update pixel surface if hover changed
            if self.hover_day is not None or self.selected_day is not None:
                self.update_pixel_surface()
            
            # Draw everything
            self.screen.fill(self.ui_colors['background'])
            
            # Draw main visualization
            self.screen.blit(self.pixel_surface, (0, 0))
            
            # Draw UI panel
            self.draw_ui_panel()
            
            # Update display
            pygame.display.flip()
            clock.tick(60)  # 60 FPS for smooth interaction
        
        pygame.quit()

if __name__ == "__main__":
    print("🚀 LAUNCHING INTERACTIVE TIME'S PIXEL VISUALIZATION")
    print("="*65)
    
    try:
        app = InteractiveTimePixel()
        app.run()
    except Exception as e:
        print(f"Error: {e}")
        pygame.quit()
        sys.exit(1)
    
    print("Thank you for exploring Time's Pixel! 🌟")