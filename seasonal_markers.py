"""
Seasonal Markers Integration for Time's Pixel
Provides comprehensive astronomical event tracking and visualization.
Includes solstices, equinoxes, meteor showers, supermoons, and other celestial events.
"""
import math
from datetime import datetime, timedelta
from typing import Dict, List, Tuple, Optional

class AstronomicalEvents:
    """Database and calculator for major astronomical events throughout the year."""
    
    def __init__(self, year: int = 2024):
        self.year = year
        self.events = self._initialize_events()
    
    def _initialize_events(self) -> Dict:
        """Initialize comprehensive astronomical events database."""
        events = {
            # Major seasonal events (solstices and equinoxes)
            'seasonal': [
                {
                    'date': f'{self.year}-03-20',
                    'name': 'Spring Equinox',
                    'type': 'equinox',
                    'category': 'seasonal',
                    'description': 'Day and night are approximately equal in length worldwide',
                    'significance': 'Marks the beginning of spring in Northern Hemisphere',
                    'color': (100, 255, 100),  # Fresh green
                    'symbol': 'Spring',
                    'importance': 'high'
                },
                {
                    'date': f'{self.year}-06-21',
                    'name': 'Summer Solstice',
                    'type': 'solstice',
                    'category': 'seasonal', 
                    'description': 'Longest day of the year in Northern Hemisphere',
                    'significance': 'Sun reaches its highest point in the sky',
                    'color': (255, 255, 100),  # Golden yellow
                    'symbol': 'Summer',
                    'importance': 'high'
                },
                {
                    'date': f'{self.year}-09-22',
                    'name': 'Fall Equinox',
                    'type': 'equinox',
                    'category': 'seasonal',
                    'description': 'Day and night are approximately equal in length worldwide',
                    'significance': 'Marks the beginning of autumn in Northern Hemisphere',
                    'color': (255, 150, 100),  # Autumn orange
                    'symbol': 'Fall',
                    'importance': 'high'
                },
                {
                    'date': f'{self.year}-12-21',
                    'name': 'Winter Solstice',
                    'type': 'solstice',
                    'category': 'seasonal',
                    'description': 'Shortest day of the year in Northern Hemisphere',
                    'significance': 'Sun reaches its lowest point in the sky',
                    'color': (150, 150, 255),  # Ice blue
                    'symbol': 'Winter',
                    'importance': 'high'
                }
            ],
            
            # Meteor shower peaks
            'meteor_showers': [
                {
                    'date': f'{self.year}-01-03',
                    'name': 'Quadrantids Peak',
                    'type': 'meteor_shower',
                    'category': 'cosmic',
                    'description': 'One of the best meteor showers of the year',
                    'significance': 'Up to 120 meteors per hour at peak',
                    'color': (255, 200, 150),  # Meteor orange
                    'symbol': 'Star',
                    'importance': 'medium'
                },
                {
                    'date': f'{self.year}-04-22',
                    'name': 'Lyrids Peak',
                    'type': 'meteor_shower',
                    'category': 'cosmic',
                    'description': 'Ancient meteor shower known for bright trails',
                    'significance': 'Peak activity with 15-20 meteors per hour',
                    'color': (200, 150, 255),  # Cosmic purple
                    'symbol': 'Sparkle',
                    'importance': 'medium'
                },
                {
                    'date': f'{self.year}-08-12',
                    'name': 'Perseids Peak',
                    'type': 'meteor_shower',
                    'category': 'cosmic',
                    'description': 'Most popular meteor shower of the year',
                    'significance': 'Up to 60 meteors per hour, very reliable',
                    'color': (255, 180, 200),  # Summer pink
                    'symbol': 'Meteor',
                    'importance': 'high'
                },
                {
                    'date': f'{self.year}-12-14',
                    'name': 'Geminids Peak',
                    'type': 'meteor_shower',
                    'category': 'cosmic',
                    'description': 'Best meteor shower of the year for many observers',
                    'significance': 'Up to 120 meteors per hour, multicolored',
                    'color': (150, 255, 200),  # Winter green
                    'symbol': 'Comet',
                    'importance': 'high'
                }
            ],
            
            # Moon-related events
            'lunar_events': [
                {
                    'date': f'{self.year}-01-25',
                    'name': 'Wolf Moon (Supermoon)',
                    'type': 'supermoon',
                    'category': 'lunar',
                    'description': 'Full moon at closest approach to Earth',
                    'significance': 'Moon appears 14% larger and 30% brighter',
                    'color': (255, 255, 200),  # Bright moonlight
                    'symbol': 'Moon',
                    'importance': 'medium'
                },
                {
                    'date': f'{self.year}-09-18',
                    'name': 'Partial Lunar Eclipse',
                    'type': 'eclipse',
                    'category': 'lunar',
                    'description': 'Earth casts partial shadow on the moon',
                    'significance': 'Visible from many parts of the world',
                    'color': (200, 100, 100),  # Eclipse red
                    'symbol': 'Eclipse',
                    'importance': 'high'
                },
                {
                    'date': f'{self.year}-11-15',
                    'name': 'Beaver Moon (Supermoon)',
                    'type': 'supermoon',
                    'category': 'lunar',
                    'description': 'Last supermoon of the year',
                    'significance': 'Traditional name from Native American calendar',
                    'color': (255, 220, 180),  # Warm moon glow
                    'symbol': 'FullMoon',
                    'importance': 'medium'
                }
            ],
            
            # Planetary events
            'planetary_events': [
                {
                    'date': f'{self.year}-01-27',
                    'name': 'Mars Opposition',
                    'type': 'opposition',
                    'category': 'planetary',
                    'description': 'Mars at closest approach to Earth',
                    'significance': 'Best time to observe Mars through telescope',
                    'color': (255, 100, 100),  # Mars red
                    'symbol': 'Mars',
                    'importance': 'medium'
                },
                {
                    'date': f'{self.year}-09-07',
                    'name': 'Jupiter Opposition',
                    'type': 'opposition',
                    'category': 'planetary',
                    'description': 'Jupiter at closest approach to Earth',
                    'significance': 'Best time to observe Jupiter and its moons',
                    'color': (255, 200, 100),  # Jupiter gold
                    'symbol': 'Jupiter',
                    'importance': 'medium'
                }
            ]
        }
        
        return events
    
    def get_all_events(self) -> List[Dict]:
        """Get all astronomical events as a flat list."""
        all_events = []
        for category in self.events.values():
            all_events.extend(category)
        
        # Sort by date
        all_events.sort(key=lambda x: datetime.strptime(x['date'], '%Y-%m-%d'))
        return all_events
    
    def get_events_by_category(self, category: str) -> List[Dict]:
        """Get events filtered by category."""
        return self.events.get(category, [])
    
    def get_events_by_importance(self, importance: str) -> List[Dict]:
        """Get events filtered by importance level."""
        all_events = self.get_all_events()
        return [event for event in all_events if event['importance'] == importance]
    
    def get_event_by_date(self, date_str: str) -> Optional[Dict]:
        """Get specific event by date string."""
        all_events = self.get_all_events()
        for event in all_events:
            if event['date'] == date_str:
                return event
        return None
    
    def get_events_in_range(self, start_date: str, end_date: str) -> List[Dict]:
        """Get all events within a date range."""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        all_events = self.get_all_events()
        events_in_range = []
        
        for event in all_events:
            event_date = datetime.strptime(event['date'], '%Y-%m-%d')
            if start <= event_date <= end:
                events_in_range.append(event)
        
        return events_in_range
    
    def calculate_day_of_year(self, date_str: str) -> int:
        """Convert date string to day of year (1-366)."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        return date.timetuple().tm_yday

class SeasonalMarkerRenderer:
    """Handles the visual rendering of seasonal markers in visualizations."""
    
    def __init__(self):
        self.events_db = AstronomicalEvents()
        self.glow_animation = 0  # For animated effects
        
        # Marker style configurations
        self.marker_styles = {
            'high': {
                'base_size': 15,
                'glow_radius': 25,
                'glow_intensity': 0.7,
                'pulse_amplitude': 0.3
            },
            'medium': {
                'base_size': 10,
                'glow_radius': 18,
                'glow_intensity': 0.5,
                'pulse_amplitude': 0.2
            },
            'low': {
                'base_size': 6,
                'glow_radius': 12,
                'glow_intensity': 0.3,
                'pulse_amplitude': 0.1
            }
        }
    
    def update_animation(self, time_delta: float):
        """Update animation state for breathing/pulsing effects."""
        self.glow_animation += time_delta * 2  # Animation speed
        if self.glow_animation > 2 * math.pi:
            self.glow_animation -= 2 * math.pi
    
    def get_marker_size(self, event: Dict) -> int:
        """Calculate animated marker size based on importance."""
        style = self.marker_styles[event['importance']]
        base_size = style['base_size']
        pulse_amplitude = style['pulse_amplitude']
        
        # Create breathing effect
        pulse = math.sin(self.glow_animation) * pulse_amplitude
        return int(base_size * (1 + pulse))
    
    def get_glow_intensity(self, event: Dict) -> float:
        """Calculate animated glow intensity."""
        style = self.marker_styles[event['importance']]
        base_intensity = style['glow_intensity']
        
        # Create subtle glow pulse
        pulse = (math.sin(self.glow_animation * 0.7) + 1) / 2  # 0 to 1
        return base_intensity * (0.5 + 0.5 * pulse)
    
    def render_marker_glow(self, surface, x: int, y: int, event: Dict):
        """Render glow effect around marker (pygame implementation)."""
        import pygame
        
        style = self.marker_styles[event['importance']]
        glow_radius = style['glow_radius']
        intensity = self.get_glow_intensity(event)
        
        # Create glow surface
        glow_size = glow_radius * 2
        glow_surface = pygame.Surface((glow_size, glow_size), pygame.SRCALPHA)
        
        # Create radial gradient for glow
        color = event['color']
        center = (glow_radius, glow_radius)
        
        for r in range(glow_radius, 0, -2):
            alpha = int(intensity * 255 * (1 - r / glow_radius) ** 2)
            glow_color = (*color, alpha)
            pygame.draw.circle(glow_surface, glow_color, center, r)
        
        # Blit glow to main surface
        glow_rect = glow_surface.get_rect(center=(x, y))
        surface.blit(glow_surface, glow_rect, special_flags=pygame.BLEND_ALPHA_SDL2)
    
    def render_marker(self, surface, x: int, y: int, event: Dict):
        """Render main marker (pygame implementation)."""
        import pygame
        
        size = self.get_marker_size(event)
        color = event['color']
        
        # Render glow first
        self.render_marker_glow(surface, x, y, event)
        
        # Render main marker circle
        pygame.draw.circle(surface, color, (x, y), size)
        pygame.draw.circle(surface, (255, 255, 255), (x, y), size, 2)  # White border
        
        # Add inner highlight for 3D effect
        highlight_pos = (x - size//3, y - size//3)
        highlight_radius = max(2, size // 4)
        pygame.draw.circle(surface, (255, 255, 255, 128), highlight_pos, highlight_radius)
    
    def render_marker_label(self, surface, x: int, y: int, event: Dict, font):
        """Render marker label text (pygame implementation)."""
        import pygame
        
        # Create text surface
        text = font.render(event['name'], True, (255, 255, 255))
        
        # Add text shadow for better readability
        shadow = font.render(event['name'], True, (0, 0, 0))
        
        # Position text offset from marker
        offset_distance = 30
        text_x = x + offset_distance
        text_y = y - 10
        
        # Blit shadow then text
        surface.blit(shadow, (text_x + 1, text_y + 1))
        surface.blit(text, (text_x, text_y))
    
    def get_events_for_visualization(self, filter_importance: str = 'all') -> List[Dict]:
        """Get events filtered for visualization display."""
        if filter_importance == 'all':
            return self.events_db.get_all_events()
        else:
            return self.events_db.get_events_by_importance(filter_importance)

class SeasonalMarkerInfo:
    """Provides detailed information and educational content for seasonal markers."""
    
    def __init__(self):
        self.events_db = AstronomicalEvents()
    
    def get_event_tooltip(self, event: Dict) -> str:
        """Generate tooltip text for an event."""
        tooltip = f"{event['name']}\n"
        tooltip += f"Date: {event['date']}\n"
        tooltip += f"Type: {event['type'].replace('_', ' ').title()}\n"
        tooltip += f"Description: {event['description']}\n"
        tooltip += f"Significance: {event['significance']}"
        return tooltip
    
    def get_seasonal_context(self, date_str: str) -> Dict:
        """Get seasonal context for a given date."""
        date = datetime.strptime(date_str, '%Y-%m-%d')
        day_of_year = date.timetuple().tm_yday
        
        # Determine season based on day of year (Northern Hemisphere)
        if day_of_year <= 79 or day_of_year >= 355:
            season = 'winter'
        elif day_of_year <= 171:
            season = 'spring'
        elif day_of_year <= 265:
            season = 'summer'
        else:
            season = 'fall'
        
        # Get nearby events
        start_date = (date - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = (date + timedelta(days=30)).strftime('%Y-%m-%d')
        nearby_events = self.events_db.get_events_in_range(start_date, end_date)
        
        return {
            'season': season,
            'day_of_year': day_of_year,
            'nearby_events': nearby_events,
            'season_progress': self._calculate_season_progress(day_of_year, season)
        }
    
    def _calculate_season_progress(self, day_of_year: int, season: str) -> float:
        """Calculate how far through the season we are (0.0 to 1.0)."""
        season_starts = {
            'spring': 80,   # Around March 20
            'summer': 172,  # Around June 21
            'fall': 266,    # Around September 22
            'winter': 355   # Around December 21
        }
        
        season_lengths = {
            'spring': 92,   # Days in spring
            'summer': 94,   # Days in summer
            'fall': 89,     # Days in fall
            'winter': 90    # Days in winter (crossing year boundary)
        }
        
        start_day = season_starts[season]
        season_length = season_lengths[season]
        
        if season == 'winter':
            # Handle winter crossing year boundary
            if day_of_year >= 355:
                progress = (day_of_year - 355) / season_length
            else:
                progress = (day_of_year + 11) / season_length  # 11 days from Dec 21 to Dec 31
        else:
            progress = (day_of_year - start_day) / season_length
        
        return max(0.0, min(1.0, progress))

# Example usage and testing functions
def demonstrate_seasonal_markers():
    """Demonstrate the seasonal markers system."""
    print("*** SEASONAL MARKERS SYSTEM DEMONSTRATION")
    print("="*50)
    
    # Initialize system
    events_db = AstronomicalEvents()
    marker_renderer = SeasonalMarkerRenderer()
    info_provider = SeasonalMarkerInfo()
    
    # Show all events
    print("\n>>> ALL ASTRONOMICAL EVENTS FOR 2024:")
    all_events = events_db.get_all_events()
    
    for event in all_events:
        day_of_year = events_db.calculate_day_of_year(event['date'])
        print(f"  Day {day_of_year:3d}: {event['name']:25} ({event['importance']:6} importance)")
    
    print(f"\nTotal events: {len(all_events)}")
    
    # Show events by category
    print("\n>>> EVENTS BY CATEGORY:")
    for category in ['seasonal', 'meteor_showers', 'lunar_events', 'planetary_events']:
        events = events_db.get_events_by_category(category)
        print(f"  {category:15}: {len(events)} events")
    
    # Show high importance events
    print("\n>>> HIGH IMPORTANCE EVENTS:")
    high_importance = events_db.get_events_by_importance('high')
    for event in high_importance:
        print(f"  {event['date']}: {event['name']} - {event['description']}")
    
    print("\n*** Seasonal markers system ready for integration!")

if __name__ == "__main__":
    demonstrate_seasonal_markers()