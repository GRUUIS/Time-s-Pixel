"""
Accurate Moon Phase Data Integration for Time's Pixel
Provides precise moon phase calculations and lunar calendar features.
"""
import math
from datetime import datetime, timedelta

class MoonPhaseCalculator:
    """Calculate accurate moon phases using astronomical algorithms."""
    
    def __init__(self):
        # Known new moon reference: January 11, 2024, 11:57 UTC
        self.reference_new_moon = datetime(2024, 1, 11, 11, 57)
        self.lunar_cycle_days = 29.530588861  # Precise synodic month length
    
    def get_moon_age(self, date):
        """Get moon age in days since last new moon."""
        if isinstance(date, str):
            date = datetime.strptime(date, '%Y-%m-%d')
        
        days_since_reference = (date - self.reference_new_moon).total_seconds() / 86400
        moon_age = days_since_reference % self.lunar_cycle_days
        
        return moon_age
    
    def get_moon_phase(self, date):
        """Get moon phase as fraction (0=new moon, 0.5=full moon, 1=new moon)."""
        moon_age = self.get_moon_age(date)
        phase = moon_age / self.lunar_cycle_days
        return phase
    
    def get_moon_illumination(self, date):
        """Get moon illumination percentage (0-1)."""
        phase = self.get_moon_phase(date)
        # Convert phase to illumination using cosine function
        # Maximum illumination at phase 0.5 (full moon)
        illumination = (1 - math.cos(2 * math.pi * phase)) / 2
        return illumination
    
    def get_moon_phase_name(self, date):
        """Get descriptive name of moon phase."""
        illumination = self.get_moon_illumination(date)
        phase = self.get_moon_phase(date)
        
        if illumination < 0.05:
            return "New Moon"
        elif illumination < 0.25:
            if phase < 0.5:
                return "Waxing Crescent"
            else:
                return "Waning Crescent"
        elif illumination < 0.75:
            if phase < 0.5:
                return "First Quarter"
            else:
                return "Last Quarter"
        elif illumination < 0.95:
            if phase < 0.5:
                return "Waxing Gibbous"
            else:
                return "Waning Gibbous"
        else:
            return "Full Moon"
    
    def get_major_moon_phases_2024(self):
        """Get dates of major moon phases for 2024."""
        phases = {
            'new_moons': [],
            'full_moons': [],
            'first_quarters': [],
            'last_quarters': []
        }
        
        # Start from first new moon of 2024
        current_date = datetime(2024, 1, 1)
        end_date = datetime(2024, 12, 31)
        
        while current_date <= end_date:
            phase = self.get_moon_phase(current_date)
            illumination = self.get_moon_illumination(current_date)
            
            # Check for major phase transitions (approximate)
            if illumination < 0.02:  # New moon
                phases['new_moons'].append(current_date.strftime('%Y-%m-%d'))
            elif 0.48 <= illumination <= 0.52:  # Full moon
                phases['full_moons'].append(current_date.strftime('%Y-%m-%d'))
            elif 0.23 <= illumination <= 0.27 and phase < 0.5:  # First quarter
                phases['first_quarters'].append(current_date.strftime('%Y-%m-%d'))
            elif 0.23 <= illumination <= 0.27 and phase > 0.5:  # Last quarter  
                phases['last_quarters'].append(current_date.strftime('%Y-%m-%d'))
            
            current_date += timedelta(days=1)
        
        return phases

class EnhancedMoonVisualizer:
    """Enhanced moon visualization with accurate phase data."""
    
    def __init__(self):
        self.calculator = MoonPhaseCalculator()
        
        # Moon colors by phase
        self.moon_colors = {
            'new': (80, 80, 120),      # Very dim
            'crescent': (140, 140, 180), # Dim
            'quarter': (180, 180, 220),  # Medium
            'gibbous': (220, 220, 240),  # Bright
            'full': (255, 255, 245)      # Very bright
        }
    
    def get_moon_color_by_phase(self, date, base_moon_color=None):
        """Get moon color based on accurate phase calculation."""
        illumination = self.calculator.get_moon_illumination(date)
        phase_name = self.calculator.get_moon_phase_name(date)
        
        # Select base color based on phase
        if 'New' in phase_name:
            base_color = self.moon_colors['new']
        elif 'Crescent' in phase_name:
            base_color = self.moon_colors['crescent']
        elif 'Quarter' in phase_name:
            base_color = self.moon_colors['quarter']
        elif 'Gibbous' in phase_name:
            base_color = self.moon_colors['gibbous']
        else:  # Full moon
            base_color = self.moon_colors['full']
        
        # Apply illumination factor
        r, g, b = base_color
        factor = 0.3 + (illumination * 0.7)  # Scale between 30% and 100%
        
        return (int(r * factor), int(g * factor), int(b * factor))
    
    def create_moon_phase_calendar(self, year=2024):
        """Create a visual calendar showing moon phases."""
        phases = self.calculator.get_major_moon_phases_2024()
        
        print(f"\n🌙 MOON PHASE CALENDAR {year} 🌙")
        print("="*50)
        
        for phase_type, dates in phases.items():
            print(f"\n{phase_type.replace('_', ' ').title()}:")
            for date in dates[:6]:  # Show first 6 instances
                dt = datetime.strptime(date, '%Y-%m-%d')
                illumination = self.calculator.get_moon_illumination(date)
                print(f"  {date} ({dt.strftime('%B %d')}) - {illumination:.1%} illuminated")
        
        return phases

def integrate_moon_phases_with_visualization():
    """Demonstrate integration of accurate moon phases with existing visualization."""
    from time_utils import load_astronomical_data, date_to_day_of_year
    
    print("\n🔬 MOON PHASE INTEGRATION TEST")
    print("="*50)
    
    # Initialize moon calculator
    moon_calc = MoonPhaseCalculator()
    moon_viz = EnhancedMoonVisualizer()
    
    # Load astronomical data
    sun_df, moon_df = load_astronomical_data()
    if sun_df is None:
        print("Could not load astronomical data")
        return
    
    print("\nComparing old vs new moon phase calculations:")
    print("Date         | Old Phase | New Phase | Illumination | Phase Name")
    print("-" * 70)
    
    # Test several dates throughout the year
    test_dates = ['2024-01-01', '2024-03-15', '2024-06-21', '2024-09-15', '2024-12-15']
    
    for date_str in test_dates:
        # Old calculation (from color_palettes.py)
        day_of_year = date_to_day_of_year(date_str)
        if day_of_year:
            old_phase = get_moon_phase_simple(day_of_year)
        else:
            old_phase = 0.5
        
        # New accurate calculation
        new_phase = moon_calc.get_moon_phase(date_str)
        illumination = moon_calc.get_moon_illumination(date_str)
        phase_name = moon_calc.get_moon_phase_name(date_str)
        
        print(f"{date_str} | {old_phase:8.3f} | {new_phase:8.3f} | {illumination:11.1%} | {phase_name}")
    
    # Create moon phase calendar
    moon_viz.create_moon_phase_calendar()

def get_moon_phase_simple(day_of_year):
    """Simple moon phase calculation for comparison (from original code)."""
    lunar_cycle = 29.53
    reference_new_moon = 11
    days_since_new_moon = (day_of_year - reference_new_moon) % lunar_cycle
    phase_progress = days_since_new_moon / lunar_cycle
    moon_intensity = (1 - math.cos(2 * math.pi * phase_progress)) / 2
    return moon_intensity

def create_enhanced_moon_palette():
    """Create color palette that uses accurate moon phase data."""
    from color_palettes import ColorPalette
    
    class AccurateMoonPalette(ColorPalette):
        """Color palette with accurate moon phase integration."""
        
        def __init__(self):
            super().__init__()
            self.moon_calculator = MoonPhaseCalculator()
            self.moon_visualizer = EnhancedMoonVisualizer()
        
        def get_moon_color(self, time_hour, moonrise_hour, moonset_hour, date_str, day_of_year):
            """Get moon color using accurate phase calculation."""
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
            
            # Get accurate moon color based on phase
            if date_str:
                moon_color = self.moon_visualizer.get_moon_color_by_phase(date_str)
            else:
                # Fallback to old calculation
                moon_phase = get_moon_phase_simple(day_of_year or 1)
                moon_color = self._blend_colors(
                    self.base_colors['moon_dim'],
                    self.base_colors['moon_bright'],
                    moon_phase
                )
            
            # Apply seasonal tinting
            return self.apply_seasonal_tint(moon_color, day_of_year or 1, intensity=0.2)
    
    return AccurateMoonPalette()

# Example usage and testing
if __name__ == "__main__":
    print("🌙 ACCURATE MOON PHASE INTEGRATION")
    print("="*60)
    
    # Test moon phase calculator
    calc = MoonPhaseCalculator()
    
    print("\nTesting Moon Phase Calculator:")
    test_date = "2024-06-21"  # Summer solstice
    phase = calc.get_moon_phase(test_date)
    illumination = calc.get_moon_illumination(test_date)
    name = calc.get_moon_phase_name(test_date)
    
    print(f"Date: {test_date}")
    print(f"Phase: {phase:.3f}")
    print(f"Illumination: {illumination:.1%}")
    print(f"Phase Name: {name}")
    
    # Run integration test
    integrate_moon_phases_with_visualization()
    
    print(f"\n" + "="*60)
    print("MOON PHASE INTEGRATION COMPLETE!")
    print("The system now uses accurate astronomical calculations")
    print("for moon phases instead of simple approximations.")
    print("="*60)