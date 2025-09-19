"""
Enhanced Color Palette System for Time's Pixel
Provides seasonal color gradients, twilight transitions, and dynamic color temperature changes.
"""
import numpy as np
import colorsys
from datetime import datetime, date
import math

class ColorPalette:
    """Base class for color palettes with seasonal and time-based variations."""
    
    def __init__(self):
        self.base_colors = {
            'night': (30, 30, 60),
            'dawn': (255, 180, 100),
            'day': (255, 255, 180),
            'sunset': (255, 120, 60),
            'moon': (180, 180, 255),
            'moon_bright': (220, 220, 255),
            'moon_dim': (100, 100, 150)
        }
    
    def get_seasonal_modifier(self, day_of_year):
        """Get seasonal color modifier based on day of year (1-365)."""
        # Create a sinusoidal cycle with peak warmth around summer solstice (day 172)
        season_cycle = math.sin(2 * math.pi * (day_of_year - 80) / 365)
        return season_cycle
    
    def apply_seasonal_tint(self, color, day_of_year, intensity=0.3):
        """Apply seasonal color tinting to a base color."""
        r, g, b = color
        modifier = self.get_seasonal_modifier(day_of_year)
        
        # Convert to HSV for easier color manipulation
        h, s, v = colorsys.rgb_to_hsv(r/255, g/255, b/255)
        
        # Adjust hue and saturation based on season
        # Summer: warmer (more red/orange), Winter: cooler (more blue)
        h_shift = modifier * intensity * 0.1  # Shift hue slightly
        s_shift = modifier * intensity * 0.2  # Adjust saturation
        
        h = (h + h_shift) % 1.0
        s = max(0, min(1, s + s_shift))
        
        # Convert back to RGB
        r_new, g_new, b_new = colorsys.hsv_to_rgb(h, s, v)
        return (int(r_new * 255), int(g_new * 255), int(b_new * 255))
    
    def get_twilight_color(self, time_hour, sunrise_hour, sunset_hour, day_of_year):
        """Get color for twilight periods with smooth transitions."""
        if sunrise_hour is None or sunset_hour is None:
            return self.base_colors['night']
        
        # Define twilight periods (civil twilight = sun 6 degrees below horizon)
        dawn_start = sunrise_hour - 0.5
        dawn_end = sunrise_hour + 0.5
        dusk_start = sunset_hour - 0.5
        dusk_end = sunset_hour + 0.5
        
        base_color = self.base_colors['night']
        
        # Dawn transition
        if dawn_start <= time_hour <= dawn_end:
            progress = (time_hour - dawn_start) / (dawn_end - dawn_start)
            base_color = self._blend_colors(
                self.base_colors['night'],
                self.base_colors['dawn'],
                progress
            )
        # Day time
        elif dawn_end < time_hour < dusk_start:
            base_color = self.base_colors['day']
        # Dusk transition  
        elif dusk_start <= time_hour <= dusk_end:
            progress = (time_hour - dusk_start) / (dusk_end - dusk_start)
            base_color = self._blend_colors(
                self.base_colors['day'],
                self.base_colors['sunset'],
                progress
            )
        # Post-sunset transition to night
        elif dusk_end < time_hour <= dusk_end + 1:
            progress = (time_hour - dusk_end) / 1.0
            base_color = self._blend_colors(
                self.base_colors['sunset'],
                self.base_colors['night'],
                progress
            )
        
        # Apply seasonal tinting
        return self.apply_seasonal_tint(base_color, day_of_year)
    
    def get_moon_color(self, time_hour, moonrise_hour, moonset_hour, moon_phase, day_of_year):
        """Get moon color based on moon phase and position."""
        if moonrise_hour is None or moonset_hour is None:
            return None
        
        # Check if moon is up
        moon_up = False
        if moonrise_hour < moonset_hour:
            moon_up = moonrise_hour <= time_hour < moonset_hour
        else:
            moon_up = time_hour >= moonrise_hour or time_hour < moonset_hour
        
        if not moon_up:
            return None
        
        # Calculate moon intensity based on phase (0 = new moon, 1 = full moon)
        moon_intensity = moon_phase
        
        # Blend between dim and bright moon colors
        moon_color = self._blend_colors(
            self.base_colors['moon_dim'],
            self.base_colors['moon_bright'],
            moon_intensity
        )
        
        # Apply seasonal tinting
        return self.apply_seasonal_tint(moon_color, day_of_year, intensity=0.2)
    
    def _blend_colors(self, color1, color2, factor):
        """Blend two colors with given factor (0=color1, 1=color2)."""
        factor = max(0, min(1, factor))
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return (r, g, b)

class NaturalisticPalette(ColorPalette):
    """Naturalistic color palette mimicking real sky and lighting conditions."""
    
    def __init__(self):
        super().__init__()
        self.base_colors.update({
            'night': (15, 15, 35),
            'dawn': (255, 200, 120),
            'day': (135, 206, 235),  # Sky blue
            'sunset': (255, 94, 77),
            'moon': (245, 245, 220),  # Beige moon
            'moon_bright': (255, 255, 240),
            'moon_dim': (180, 180, 190)
        })

class VibrantPalette(ColorPalette):
    """Vibrant, artistic color palette for more expressive visualizations."""
    
    def __init__(self):
        super().__init__()
        self.base_colors.update({
            'night': (25, 25, 80),
            'dawn': (255, 150, 50),
            'day': (255, 255, 100),
            'sunset': (255, 50, 100),
            'moon': (150, 255, 255),
            'moon_bright': (200, 255, 255),
            'moon_dim': (75, 150, 200)
        })

class MonochromePalette(ColorPalette):
    """Monochrome palette for elegant, minimalist visualizations."""
    
    def __init__(self):
        super().__init__()
        self.base_colors.update({
            'night': (20, 20, 20),
            'dawn': (120, 120, 120),
            'day': (220, 220, 220),
            'sunset': (180, 180, 180),
            'moon': (160, 160, 160),
            'moon_bright': (200, 200, 200),
            'moon_dim': (100, 100, 100)
        })

def get_moon_phase(day_of_year):
    """
    Calculate approximate moon phase for a given day of year.
    Returns value between 0 (new moon) and 1 (full moon).
    This is a simplified calculation - real moon phases are more complex.
    """
    # Lunar cycle is approximately 29.53 days
    lunar_cycle = 29.53
    
    # Reference: approximate new moon on Jan 11, 2024 (day 11)
    reference_new_moon = 11
    
    days_since_new_moon = (day_of_year - reference_new_moon) % lunar_cycle
    phase_progress = days_since_new_moon / lunar_cycle
    
    # Convert to intensity (0 at new moon, 1 at full moon)
    # Using cosine function: full moon at 0.5 cycle, new moon at 0 and 1
    moon_intensity = (1 - math.cos(2 * math.pi * phase_progress)) / 2
    
    return moon_intensity

def create_palette(palette_type="naturalistic"):
    """Factory function to create color palettes."""
    palettes = {
        "naturalistic": NaturalisticPalette,
        "vibrant": VibrantPalette,
        "monochrome": MonochromePalette,
        "classic": ColorPalette
    }
    
    if palette_type not in palettes:
        palette_type = "naturalistic"
    
    return palettes[palette_type]()

# Example usage and testing
if __name__ == "__main__":
    # Test the color palette system
    palette = create_palette("naturalistic")
    
    # Test a summer day (day 172 = June 21)
    summer_day = 172
    sunrise = 5.5  # 5:30 AM
    sunset = 19.0  # 7:00 PM
    moonrise = 22.0  # 10:00 PM
    moonset = 6.0   # 6:00 AM next day
    
    print("Summer Day Color Test (Day 172):")
    for hour in range(0, 24, 3):
        moon_phase = get_moon_phase(summer_day)
        
        # Get twilight color
        sky_color = palette.get_twilight_color(hour, sunrise, sunset, summer_day)
        
        # Get moon color if applicable
        moon_color = palette.get_moon_color(hour, moonrise, moonset, moon_phase, summer_day)
        
        print(f"Hour {hour:2d}: Sky={sky_color}, Moon={moon_color}, Phase={moon_phase:.2f}")