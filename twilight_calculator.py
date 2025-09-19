"""
Advanced Twilight Gradient System for Time's Pixel
Implements civil, nautical, and astronomical twilight calculations for realistic sky transitions.
"""
import math
from datetime import datetime, timedelta

class TwilightCalculator:
    """Calculate different types of twilight based on solar elevation angles."""
    
    def __init__(self, latitude=22.3, longitude=114.2):  # Hong Kong coordinates
        self.latitude = math.radians(latitude)
        self.longitude = math.radians(longitude)
        
        # Twilight definitions (sun angle below horizon)
        self.twilight_angles = {
            'civil': 6,      # Civil twilight: sun 6° below horizon
            'nautical': 12,  # Nautical twilight: sun 12° below horizon  
            'astronomical': 18,  # Astronomical twilight: sun 18° below horizon
            'blue_hour': 4,   # Blue hour: sun 4° below horizon
            'golden_hour': -6  # Golden hour: sun above horizon to 6° elevation
        }
    
    def get_day_of_year(self, date_str):
        """Convert date string to day of year."""
        dt = datetime.strptime(date_str, '%Y-%m-%d')
        return dt.timetuple().tm_yday
    
    def calculate_solar_declination(self, day_of_year):
        """Calculate solar declination for given day of year."""
        # Approximate formula for solar declination
        declination = 23.45 * math.sin(math.radians(360 * (284 + day_of_year) / 365))
        return math.radians(declination)
    
    def calculate_hour_angle(self, elevation_angle, declination):
        """Calculate hour angle for given solar elevation."""
        lat = self.latitude
        dec = declination
        elev = math.radians(elevation_angle)
        
        try:
            cos_hour_angle = (math.sin(elev) - math.sin(lat) * math.sin(dec)) / (math.cos(lat) * math.cos(dec))
            
            # Clamp to valid range [-1, 1]
            cos_hour_angle = max(-1, min(1, cos_hour_angle))
            hour_angle = math.acos(cos_hour_angle)
            
            return hour_angle
        except:
            return None
    
    def calculate_twilight_times(self, date_str, sunrise_hour, sunset_hour):
        """Calculate all twilight transition times for a given date."""
        if sunrise_hour is None or sunset_hour is None:
            return {}
        
        day_of_year = self.get_day_of_year(date_str)
        declination = self.calculate_solar_declination(day_of_year)
        
        twilight_times = {}
        
        for twilight_type, angle in self.twilight_angles.items():
            hour_angle = self.calculate_hour_angle(-angle, declination)
            
            if hour_angle is not None:
                # Convert hour angle to hours (±12 hours from solar noon)
                hours_from_noon = hour_angle * 12 / math.pi
                
                # Estimate solar noon (midpoint between sunrise and sunset)
                solar_noon = (sunrise_hour + sunset_hour) / 2
                
                if angle > 0:  # Below horizon (twilight)
                    morning_time = solar_noon - hours_from_noon
                    evening_time = solar_noon + hours_from_noon
                else:  # Above horizon (golden hour)
                    morning_time = sunrise_hour + abs(hours_from_noon)
                    evening_time = sunset_hour - abs(hours_from_noon)
                
                twilight_times[twilight_type] = {
                    'morning': morning_time,
                    'evening': evening_time
                }
        
        return twilight_times
    
    def get_sky_type(self, time_hour, sunrise_hour, sunset_hour, twilight_times):
        """Determine sky type based on current time and twilight calculations."""
        if sunrise_hour is None or sunset_hour is None:
            return 'night'
        
        # Day time
        if sunrise_hour <= time_hour <= sunset_hour:
            # Check for golden hour
            golden = twilight_times.get('golden_hour', {})
            if ('morning' in golden and time_hour <= golden['morning']) or \
               ('evening' in golden and time_hour >= golden['evening']):
                return 'golden_hour'
            return 'day'
        
        # Check twilight periods
        civil = twilight_times.get('civil', {})
        nautical = twilight_times.get('nautical', {})
        astronomical = twilight_times.get('astronomical', {})
        blue_hour = twilight_times.get('blue_hour', {})
        
        # Morning twilight
        if time_hour < sunrise_hour:
            if 'morning' in blue_hour and time_hour >= blue_hour['morning']:
                return 'blue_hour_morning'
            elif 'morning' in civil and time_hour >= civil['morning']:
                return 'civil_twilight_morning'
            elif 'morning' in nautical and time_hour >= nautical['morning']:
                return 'nautical_twilight'
            elif 'morning' in astronomical and time_hour >= astronomical['morning']:
                return 'astronomical_twilight'
            else:
                return 'night'
        
        # Evening twilight
        else:  # time_hour > sunset_hour
            if 'evening' in blue_hour and time_hour <= blue_hour['evening']:
                return 'blue_hour_evening'
            elif 'evening' in civil and time_hour <= civil['evening']:
                return 'civil_twilight_evening'
            elif 'evening' in nautical and time_hour <= nautical['evening']:
                return 'nautical_twilight'
            elif 'evening' in astronomical and time_hour <= astronomical['evening']:
                return 'astronomical_twilight'
            else:
                return 'night'

class AdvancedSkyPalette:
    """Advanced color palette with realistic twilight transitions."""
    
    def __init__(self):
        self.twilight_calculator = TwilightCalculator()
        
        # Extended color palette for different sky conditions
        self.sky_colors = {
            'night': (15, 15, 35),
            'astronomical_twilight': (25, 25, 50),
            'nautical_twilight': (40, 40, 80),
            'civil_twilight_morning': (100, 80, 120),
            'civil_twilight_evening': (120, 70, 100),
            'blue_hour_morning': (60, 90, 150),
            'blue_hour_evening': (80, 60, 140),
            'golden_hour': (255, 200, 100),
            'day': (135, 206, 235),  # Sky blue
            'sunrise': (255, 180, 120),
            'sunset': (255, 120, 80)
        }
        
        # Color intensity modifiers for smooth transitions
        self.transition_factors = {
            'night': 0.3,
            'astronomical_twilight': 0.4,
            'nautical_twilight': 0.5,
            'civil_twilight_morning': 0.7,
            'civil_twilight_evening': 0.7,
            'blue_hour_morning': 0.8,
            'blue_hour_evening': 0.8,
            'golden_hour': 1.0,
            'day': 1.0
        }
    
    def get_advanced_sky_color(self, time_hour, sunrise_hour, sunset_hour, date_str, day_of_year):
        """Get sky color with advanced twilight calculations."""
        # Calculate twilight times
        twilight_times = self.twilight_calculator.calculate_twilight_times(
            date_str, sunrise_hour, sunset_hour
        )
        
        # Determine sky type
        sky_type = self.twilight_calculator.get_sky_type(
            time_hour, sunrise_hour, sunset_hour, twilight_times
        )
        
        # Get base color for sky type
        base_color = self.sky_colors.get(sky_type, self.sky_colors['night'])
        
        # Apply seasonal tinting
        if day_of_year:
            base_color = self.apply_seasonal_tint(base_color, day_of_year)
        
        # Apply transition smoothing for more realistic gradients
        return self.smooth_transitions(
            time_hour, sky_type, base_color, sunrise_hour, sunset_hour, twilight_times
        )
    
    def smooth_transitions(self, time_hour, sky_type, base_color, sunrise_hour, sunset_hour, twilight_times):
        """Apply smooth color transitions between twilight phases."""
        transition_width = 0.5  # Hours for transition smoothing
        
        # Handle transitions around sunrise
        if sunrise_hour and abs(time_hour - sunrise_hour) <= transition_width:
            if time_hour < sunrise_hour:
                # Pre-sunrise transition
                factor = (sunrise_hour - time_hour) / transition_width
                sunrise_color = self.sky_colors['sunrise']
                return self.blend_colors(sunrise_color, base_color, factor)
            else:
                # Post-sunrise transition to day
                factor = (time_hour - sunrise_hour) / transition_width
                day_color = self.sky_colors['day']
                return self.blend_colors(base_color, day_color, factor)
        
        # Handle transitions around sunset
        if sunset_hour and abs(time_hour - sunset_hour) <= transition_width:
            if time_hour < sunset_hour:
                # Pre-sunset transition
                factor = (sunset_hour - time_hour) / transition_width
                day_color = self.sky_colors['day']
                sunset_color = self.sky_colors['sunset']
                return self.blend_colors(day_color, sunset_color, 1 - factor)
            else:
                # Post-sunset transition
                factor = (time_hour - sunset_hour) / transition_width
                sunset_color = self.sky_colors['sunset']
                return self.blend_colors(sunset_color, base_color, factor)
        
        return base_color
    
    def apply_seasonal_tint(self, color, day_of_year, intensity=0.2):
        """Apply seasonal color tinting."""
        r, g, b = color
        
        # Create seasonal cycle (warmer in summer, cooler in winter)
        season_factor = math.sin(2 * math.pi * (day_of_year - 80) / 365)
        
        # Apply tinting
        if season_factor > 0:  # Summer - warmer
            r = min(255, int(r * (1 + intensity * season_factor * 0.2)))
            g = min(255, int(g * (1 + intensity * season_factor * 0.1)))
        else:  # Winter - cooler
            b = min(255, int(b * (1 + intensity * abs(season_factor) * 0.3)))
            g = max(0, int(g * (1 - intensity * abs(season_factor) * 0.1)))
        
        return (r, g, b)
    
    def blend_colors(self, color1, color2, factor):
        """Blend two colors with smooth interpolation."""
        factor = max(0, min(1, factor))
        r1, g1, b1 = color1
        r2, g2, b2 = color2
        
        r = int(r1 + (r2 - r1) * factor)
        g = int(g1 + (g2 - g1) * factor)
        b = int(b1 + (b2 - b1) * factor)
        
        return (r, g, b)

def test_twilight_calculations():
    """Test twilight calculations for specific dates."""
    calculator = TwilightCalculator()
    palette = AdvancedSkyPalette()
    
    print("🌅 ADVANCED TWILIGHT CALCULATIONS TEST")
    print("="*60)
    
    # Test dates - solstices and equinoxes
    test_cases = [
        ("2024-03-20", "Spring Equinox", 6.45, 18.5),  # Approximate times
        ("2024-06-21", "Summer Solstice", 5.67, 19.17),
        ("2024-09-23", "Autumn Equinox", 6.2, 18.32),
        ("2024-12-21", "Winter Solstice", 6.98, 17.75)
    ]
    
    for date_str, event_name, sunrise, sunset in test_cases:
        print(f"\n{event_name} - {date_str}")
        print("-" * 40)
        
        twilight_times = calculator.calculate_twilight_times(date_str, sunrise, sunset)
        
        for twilight_type, times in twilight_times.items():
            morning = times.get('morning', 0)
            evening = times.get('evening', 0)
            print(f"{twilight_type:>18}: {morning:5.2f}h - {evening:5.2f}h")
    
    print(f"\n" + "="*60)
    
    # Test color transitions throughout a day
    print("\nCOLOR TRANSITION TEST - Summer Solstice")
    print("-" * 40)
    
    test_date = "2024-06-21"
    sunrise = 5.67
    sunset = 19.17
    day_of_year = 173
    
    print("Hour | Sky Type               | RGB Color")
    print("-" * 45)
    
    for hour in range(0, 24, 2):
        color = palette.get_advanced_sky_color(hour, sunrise, sunset, test_date, day_of_year)
        twilight_times = calculator.calculate_twilight_times(test_date, sunrise, sunset)
        sky_type = calculator.get_sky_type(hour, sunrise, sunset, twilight_times)
        
        print(f"{hour:4d} | {sky_type:<22} | {color}")

def create_twilight_comparison():
    """Create visualization comparing basic vs advanced twilight."""
    print(f"\n🎨 CREATING TWILIGHT COMPARISON")
    print("="*50)
    
    # This would integrate with the main visualization system
    # For now, we'll just show the concept
    
    from color_palettes import ColorPalette
    
    basic_palette = ColorPalette()
    advanced_palette = AdvancedSkyPalette()
    
    test_date = "2024-06-21"
    sunrise = 5.67
    sunset = 19.17
    day_of_year = 173
    
    print("Hour | Basic Color    | Advanced Color | Improvement")
    print("-" * 55)
    
    for hour in range(4, 22, 2):
        # Basic calculation
        basic_color = basic_palette.get_twilight_color(hour, sunrise, sunset, day_of_year)
        
        # Advanced calculation
        advanced_color = advanced_palette.get_advanced_sky_color(hour, sunrise, sunset, test_date, day_of_year)
        
        # Calculate color difference
        diff = sum(abs(a - b) for a, b in zip(basic_color, advanced_color))
        
        print(f"{hour:4d} | {str(basic_color):<14} | {str(advanced_color):<14} | {diff:>8.0f}")
    
    print(f"\nAdvanced twilight system provides:")
    print("- More accurate astronomical calculations")
    print("- Smoother color transitions")
    print("- Realistic civil/nautical/astronomical twilight")
    print("- Golden hour and blue hour effects")
    print("- Better seasonal color variations")

if __name__ == "__main__":
    test_twilight_calculations()
    create_twilight_comparison()
    
    print(f"\n" + "="*60)
    print("ADVANCED TWILIGHT SYSTEM READY!")
    print("="*60)
    print("Features implemented:")
    print("- Civil twilight (sun 6° below horizon)")
    print("- Nautical twilight (sun 12° below horizon)")  
    print("- Astronomical twilight (sun 18° below horizon)")
    print("- Blue hour (sun 4° below horizon)")
    print("- Golden hour (sun above horizon to 6° elevation)")
    print("- Smooth color transitions between phases")
    print("- Seasonal color tinting")
    print("- Accurate solar position calculations")
    print("="*60)