"""
Hong Kong Skyline Renderer for Time's Pixel
Creates a realistic Hong Kong Kowloon City skyline silhouette with animated sky background.
Implements smooth time-lapse animation showing day/night cycles throughout the year.
"""
import pygame
import math
import numpy as np
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional

class HongKongSkylineRenderer:
    """Renders Hong Kong Kowloon City skyline silhouette with detailed building profiles."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.skyline_height = int(height * 0.4)  # Skyline takes up bottom 40% of screen
        self.sky_height = height - self.skyline_height
        
        # Generate realistic Hong Kong Kowloon City skyline
        self.skyline_points = self._generate_kowloon_skyline()
        
        # Building lighting system for night scenes
        self.building_windows = self._generate_building_windows()
    
    def _generate_kowloon_skyline(self) -> List[Tuple[int, int]]:
        """Generate realistic Kowloon City skyline profile with varied building heights."""
        points = [(0, self.height)]  # Start from bottom left
        
        # Define building segments with realistic proportions
        segments = [
            # Low-rise residential areas
            {'width_ratio': 0.15, 'height_range': (0.6, 0.8), 'building_count': 8},
            # Mid-rise commercial buildings
            {'width_ratio': 0.25, 'height_range': (0.4, 0.9), 'building_count': 12},
            # High-rise towers (iconic Hong Kong skyline)
            {'width_ratio': 0.35, 'height_range': (0.2, 0.6), 'building_count': 15},
            # Mixed development area
            {'width_ratio': 0.15, 'height_range': (0.5, 0.8), 'building_count': 10},
            # Waterfront low-rise
            {'width_ratio': 0.1, 'height_range': (0.7, 0.9), 'building_count': 5}
        ]
        
        current_x = 0
        
        for segment in segments:
            segment_width = int(self.width * segment['width_ratio'])
            building_width = segment_width // segment['building_count']
            min_height, max_height = segment['height_range']
            
            for i in range(segment['building_count']):
                # Random building height within segment range
                height_factor = min_height + (max_height - min_height) * (
                    0.5 + 0.5 * math.sin(i * 0.8) * np.random.uniform(0.7, 1.3)
                )
                height_factor = max(min_height, min(max_height, height_factor))
                
                building_height = int(self.skyline_height * height_factor)
                building_top = self.height - building_height
                
                # Add building corners with slight variations
                building_left = current_x + i * building_width
                building_right = building_left + building_width
                
                # Add rooftop details (antennas, equipment)
                if np.random.random() > 0.6:  # 40% chance of rooftop details
                    antenna_height = int(building_height * 0.1)
                    points.extend([
                        (building_left, building_top + antenna_height),
                        (building_left + building_width//4, building_top),
                        (building_right - building_width//4, building_top),
                        (building_right, building_top + antenna_height)
                    ])
                else:
                    points.extend([
                        (building_left, building_top),
                        (building_right, building_top)
                    ])
                
                # Add building base
                points.extend([
                    (building_right, self.height)
                ])
            
            current_x += segment_width
        
        # Ensure skyline ends at right edge
        points.append((self.width, self.height))
        
        return points
    
    def _generate_building_windows(self) -> List[Dict]:
        """Generate window positions for building lighting effects during night."""
        windows = []
        
        # Analyze skyline to find building segments
        for i in range(0, len(self.skyline_points) - 1, 2):
            if i + 1 < len(self.skyline_points):
                left_x = self.skyline_points[i][0]
                top_y = self.skyline_points[i][1]
                right_x = self.skyline_points[i + 1][0]
                
                # Skip if this is ground level
                if top_y >= self.height - 10:
                    continue
                
                building_width = right_x - left_x
                building_height = self.height - top_y
                
                # Add windows in grid pattern
                window_size = 3
                spacing_x = 8
                spacing_y = 12
                
                if building_width > spacing_x and building_height > spacing_y:
                    for wx in range(left_x + spacing_x//2, right_x - spacing_x//2, spacing_x):
                        for wy in range(top_y + spacing_y//2, self.height - spacing_y//2, spacing_y):
                            # Random chance for window to be lit
                            if np.random.random() > 0.4:  # 60% chance of lit window
                                windows.append({
                                    'x': wx,
                                    'y': wy,
                                    'size': window_size,
                                    'brightness': np.random.uniform(0.3, 1.0)
                                })
        
        return windows
    
    def render_skyline(self, surface: pygame.Surface, is_night: bool = False):
        """Render the Hong Kong skyline silhouette with optimized window effects."""
        # Draw skyline silhouette
        if len(self.skyline_points) > 2:
            pygame.draw.polygon(surface, (0, 0, 0), self.skyline_points)
        
        # Add building windows during night time with optimized rendering
        if is_night:
            current_time = pygame.time.get_ticks() * 0.001  # Convert to seconds
            
            # Batch render windows for better performance
            window_rects = []
            window_colors = []
            
            for window in self.building_windows:
                # Optimize flicker calculation - use simpler function
                flicker_phase = current_time * 2 + window['x'] * 0.01
                flicker = 0.85 + 0.15 * math.sin(flicker_phase)  # Reduced flicker intensity
                
                brightness = window['brightness'] * flicker
                
                # Pre-calculate base color to avoid repeated calculations
                base_color = (255, 220, 120)
                color = tuple(int(c * brightness) for c in base_color)
                
                # Collect rects and colors for batch rendering
                window_rect = pygame.Rect(
                    window['x'] - window['size']//2,
                    window['y'] - window['size']//2,
                    window['size'],
                    window['size']
                )
                
                window_rects.append(window_rect)
                window_colors.append(color)
            
            # Batch render all windows
            for rect, color in zip(window_rects, window_colors):
                pygame.draw.rect(surface, color, rect)

class SkyAnimationEngine:
    """Handles smooth sky color animations and celestial body movements."""
    
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.animation_time = 0.0  # Current animation time in hours (0-24)
        self.day_of_year = 1  # Current day (1-366)
        self.animation_speed = 0.05  # Animation speed multiplier (much slower, more contemplative)
        
        # Time range control for user selection
        self.time_range_start = {'day': 1, 'hour': 0.0}  # Start of time range
        self.time_range_end = {'day': 366, 'hour': 24.0}  # End of time range
        self.loop_time_range = False  # Whether to loop within time range
        
        # Enhanced speed control
        self.speed_presets = [0.01, 0.02, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0]
        self.current_speed_index = 2  # Start with 0.05x speed
        
        # Sky gradient parameters
        self.horizon_blend = 0.3  # How much of screen height for horizon gradient
        
        # Sun and moon parameters
        self.sun_radius = 15
        self.moon_radius = 12
        
        # Performance optimization: Pre-render glow effects
        self._sun_glow_cache = {}
        self._moon_glow_cache = {}
        self._position_cache = {}
        self._last_cache_time = 0
        
        # Smooth movement tracking
        self.sun_pos_history = []
        self.moon_pos_history = []
        self.position_smoothing = 0.3  # Interpolation factor for smooth movement
        
        # Import our existing astronomical systems
        print("DEBUG: Starting astronomical data initialization...")
        try:
            print("DEBUG: Attempting imports...")
            
            # Try relative imports first, then absolute
            try:
                from src.core.twilight_calculator import AdvancedSkyPalette
                from src.core.moon_phases import MoonPhaseCalculator
                from src.core.time_utils import load_astronomical_data, get_day_data
            except ImportError:
                # If relative imports fail, try adding the project root to path
                import sys
                import os
                project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
                if project_root not in sys.path:
                    sys.path.insert(0, project_root)
                
                from src.core.twilight_calculator import AdvancedSkyPalette
                from src.core.moon_phases import MoonPhaseCalculator
                from src.core.time_utils import load_astronomical_data, get_day_data
            
            print("DEBUG: All imports successful")
            
            self.sky_palette = AdvancedSkyPalette()
            self.moon_calculator = MoonPhaseCalculator()
            print("DEBUG: Astronomical objects created")
            
            # Load astronomical data with absolute paths
            import os
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))  # Go up to project root
            sun_file = os.path.join(project_root, "data", "hongkong_sunrise_sunset_2024_clean.csv")
            moon_file = os.path.join(project_root, "data", "moonrise_moonset_2024_clean.csv")
            
            print(f"Loading sun data from: {sun_file}")
            print(f"Loading moon data from: {moon_file}")
            print(f"Sun file exists: {os.path.exists(sun_file)}")
            print(f"Moon file exists: {os.path.exists(moon_file)}")
            
            self.sun_df, self.moon_df = load_astronomical_data(sun_file, moon_file)
            self.has_data = self.sun_df is not None and self.moon_df is not None
            
            print(f"Data loading result: has_data = {self.has_data}")
            if self.has_data:
                print(f"Loaded {len(self.sun_df)} days of sun data, {len(self.moon_df)} days of moon data")
            
        except ImportError as e:
            print(f"Warning: Could not import astronomical modules: {e}")
            self.has_data = False
        except Exception as e:
            print(f"Error loading astronomical data: {e}")
            import traceback
            traceback.print_exc()
            self.has_data = False
        
        # Initialize performance optimizations
        self._init_glow_caches()
        self._init_data_caches()
    
    def _init_data_caches(self):
        """Initialize astronomical data caches for better performance."""
        self._astronomical_cache = {}
        self._sky_color_cache = {}
        self._moon_illumination_cache = {}
        
        # Pre-calculate commonly used data if available
        if self.has_data:
            self._precompute_astronomical_data()
    
    def _precompute_astronomical_data(self):
        """Pre-compute astronomical data for all days to improve runtime performance."""
        try:
            from src.core.time_utils import get_day_data
            
            print("Pre-computing astronomical data for performance...")
            
            for day in range(1, 367):  # All days of year
                day_idx = day - 1
                day_data = get_day_data(self.sun_df, self.moon_df, day_idx)
                
                if day_data:
                    # Cache the astronomical data
                    self._astronomical_cache[day] = {
                        'sunrise': day_data.get('sunrise', 6.0),
                        'sunset': day_data.get('sunset', 18.0),
                        'moonrise': day_data.get('moonrise'),
                        'moonset': day_data.get('moonset'),
                        'date': day_data.get('date', f'2024-{day:03d}')
                    }
                    
                    # Pre-compute moon illumination if moon calculator available
                    if hasattr(self, 'moon_calculator') and self.moon_calculator:
                        try:
                            base_date = datetime(2024, 1, 1)
                            current_date = base_date + timedelta(days=day - 1)
                            date_str = current_date.strftime('%Y-%m-%d')
                            illumination = self.moon_calculator.get_moon_illumination(date_str)
                            self._moon_illumination_cache[day] = illumination
                        except Exception:
                            self._moon_illumination_cache[day] = 0.5
            
            print(f"Pre-computed data for {len(self._astronomical_cache)} days")
            
        except Exception as e:
            print(f"Warning: Could not pre-compute astronomical data: {e}")
    
    def _get_cached_day_data(self, day: int) -> Optional[Dict]:
        """Get cached astronomical data for a specific day."""
        return self._astronomical_cache.get(day)
    
    def update_animation(self, delta_time: float):
        """Update animation state with time range control and cache management."""
        # Advance animation time
        self.animation_time += delta_time * self.animation_speed
        
        # Handle day rollover and time range constraints
        if self.animation_time >= 24.0:
            self.animation_time -= 24.0
            self.day_of_year += 1
            
            # Clean up old cache entries to prevent memory growth
            self._cleanup_caches()
        
        # Handle time range boundaries
        if self.loop_time_range:
            # Check if we've reached the end of the time range
            if (self.day_of_year > self.time_range_end['day'] or 
                (self.day_of_year == self.time_range_end['day'] and 
                 self.animation_time >= self.time_range_end['hour'])):
                # Loop back to start of time range
                self.day_of_year = self.time_range_start['day']
                self.animation_time = self.time_range_start['hour']
                print(f"Time range loop: returning to Day {self.day_of_year}, {self.animation_time:.1f}h")
        else:
            # Normal year rollover
            if self.day_of_year > 366:
                self.day_of_year = 1
                
        # Ensure we stay within valid bounds
        if self.day_of_year < 1:
            self.day_of_year = 1
        if self.animation_time < 0:
            self.animation_time = 0
    
    def _cleanup_caches(self):
        """Clean up old cache entries to manage memory usage."""
        # Keep only recent cache entries for position and sky colors
        max_cache_size = 100
        
        if len(self._position_cache) > max_cache_size:
            # Remove oldest entries (simple FIFO approach)
            keys_to_remove = list(self._position_cache.keys())[:-max_cache_size//2]
            for key in keys_to_remove:
                del self._position_cache[key]
        
        if len(self._sky_color_cache) > max_cache_size:
            keys_to_remove = list(self._sky_color_cache.keys())[:-max_cache_size//2]
            for key in keys_to_remove:
                del self._sky_color_cache[key]
    
    def set_time(self, day: int, hour: float):
        """Set specific day and time for animation."""
        self.day_of_year = max(1, min(366, day))
        self.animation_time = max(0.0, min(24.0, hour))
    
    def set_time_range(self, start_day: int, start_hour: float, end_day: int, end_hour: float, loop: bool = True):
        """Set time range for looped playback."""
        self.time_range_start = {
            'day': max(1, min(366, start_day)), 
            'hour': max(0.0, min(24.0, start_hour))
        }
        self.time_range_end = {
            'day': max(1, min(366, end_day)), 
            'hour': max(0.0, min(24.0, end_hour))
        }
        self.loop_time_range = loop
        
        # Set current time to start of range
        self.day_of_year = self.time_range_start['day']
        self.animation_time = self.time_range_start['hour']
        
        print(f"Time range set: Day {start_day} {start_hour:.1f}h - Day {end_day} {end_hour:.1f}h (Loop: {loop})")
    
    def cycle_speed_preset(self, direction: int = 1):
        """Cycle through speed presets. Direction: 1=faster, -1=slower"""
        self.current_speed_index += direction
        self.current_speed_index = max(0, min(len(self.speed_presets) - 1, self.current_speed_index))
        self.animation_speed = self.speed_presets[self.current_speed_index]
        return self.animation_speed
    
    def get_animation_info(self) -> Dict[str, any]:
        """Get current animation state information with time range details."""
        hour = int(self.animation_time)
        minute = int((self.animation_time - hour) * 60)
        time_str = f"{hour:02d}:{minute:02d}"
        
        # Calculate progress within time range if looping
        progress_info = ""
        if self.loop_time_range:
            total_range_days = self.time_range_end['day'] - self.time_range_start['day']
            current_day_in_range = self.day_of_year - self.time_range_start['day']
            if total_range_days > 0:
                progress = (current_day_in_range / total_range_days) * 100
                progress_info = f" ({progress:.1f}% of range)"
        
        return {
            'day': self.day_of_year,
            'time_str': time_str,
            'speed': self.animation_speed,
            'speed_preset': f"{self.animation_speed:.2f}x",
            'hour': self.animation_time,
            'loop_range': self.loop_time_range,
            'range_start': f"Day {self.time_range_start['day']} {self.time_range_start['hour']:.1f}h",
            'range_end': f"Day {self.time_range_end['day']} {self.time_range_end['hour']:.1f}h",
            'progress_info': progress_info
        }
    
    def _init_glow_caches(self):
        """Pre-render glow effects for better performance."""
        # Pre-render sun glow in different intensities
        for intensity in [0.3, 0.5, 0.7, 1.0]:
            glow_radius = self.sun_radius + 15
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            
            # Create layered glow effect
            for r in range(glow_radius, self.sun_radius, -3):  # Fewer layers for performance
                alpha = int(40 * intensity * (1 - (r - self.sun_radius) / 15))
                if alpha > 0:
                    glow_color = (255, 220, 150, alpha)
                    pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), r)
            
            self._sun_glow_cache[intensity] = glow_surf
        
        # Pre-render moon glow in different phases
        for phase in [0.2, 0.5, 0.8, 1.0]:
            glow_radius = self.moon_radius + 8
            glow_surf = pygame.Surface((glow_radius*2, glow_radius*2), pygame.SRCALPHA)
            
            alpha = int(30 * phase)
            if alpha > 0:
                glow_color = (200, 200, 220, alpha)
                pygame.draw.circle(glow_surf, glow_color, (glow_radius, glow_radius), glow_radius)
            
            self._moon_glow_cache[phase] = glow_surf
    
    def _smooth_position(self, new_pos: Tuple[int, int], history: List[Tuple[int, int]], max_history: int = 3) -> Tuple[int, int]:
        """Apply smoothing to position changes to avoid sudden jumps."""
        history.append(new_pos)
        
        # Keep only recent positions
        if len(history) > max_history:
            history.pop(0)
        
        # If position is off-screen, don't smooth
        if new_pos[0] < 0 or new_pos[1] < 0:
            return new_pos
        
        # Calculate weighted average for smooth movement
        if len(history) > 1:
            total_weight = 0
            weighted_x = 0
            weighted_y = 0
            
            for i, pos in enumerate(history):
                # More recent positions have higher weight
                weight = (i + 1) ** 2
                weighted_x += pos[0] * weight
                weighted_y += pos[1] * weight
                total_weight += weight
            
            if total_weight > 0:
                smooth_x = int(weighted_x / total_weight)
                smooth_y = int(weighted_y / total_weight)
                return (smooth_x, smooth_y)
        
        return new_pos
        """Update animation state based on time delta."""
        # Advance animation time
        self.animation_time += delta_time * self.animation_speed
        
        # Handle day rollover
        if self.animation_time >= 24.0:
            self.animation_time -= 24.0
            self.day_of_year += 1
            if self.day_of_year > 366:
                self.day_of_year = 1
    
    def set_time(self, day: int, hour: float):
        """Set specific day and time for animation."""
        self.day_of_year = max(1, min(366, day))
        self.animation_time = max(0.0, min(24.0, hour))
    
    def get_sky_colors(self) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """Get current sky gradient colors with caching for performance."""
        # Check cache first
        cache_key = (self.day_of_year, round(self.animation_time, 1))
        if cache_key in self._sky_color_cache:
            return self._sky_color_cache[cache_key]
        
        if not self.has_data:
            # Fallback colors if no astronomical data
            result = self._get_fallback_sky_colors()
            self._sky_color_cache[cache_key] = result
            return result
        
        try:
            # Use cached astronomical data
            day_data = self._get_cached_day_data(self.day_of_year)
            
            if day_data and self.sky_palette:
                # Use our advanced sky palette
                sky_color = self.sky_palette.get_advanced_sky_color(
                    self.animation_time,
                    day_data.get('sunrise', 6.0),
                    day_data.get('sunset', 18.0),
                    day_data.get('date', '2024-01-01'),
                    self.day_of_year
                )
                
                # Create gradient effect - darker at top, lighter at horizon
                top_color = tuple(int(c * 0.7) for c in sky_color)
                horizon_color = sky_color
                
                result = (top_color, horizon_color)
                self._sky_color_cache[cache_key] = result
                return result
            
        except Exception as e:
            print(f"Error getting sky colors: {e}")
        
        # Fallback if data access fails
        result = self._get_fallback_sky_colors()
        self._sky_color_cache[cache_key] = result
        return result
    
    def _get_fallback_sky_colors(self) -> Tuple[Tuple[int, int, int], Tuple[int, int, int]]:
        """Generate fallback sky colors based on time of day."""
        hour = self.animation_time
        
        if 5 <= hour <= 7:  # Dawn
            top = (50, 50, 100)
            horizon = (255, 150, 80)
        elif 7 < hour <= 17:  # Day
            top = (100, 150, 255)
            horizon = (150, 200, 255)
        elif 17 < hour <= 19:  # Dusk
            top = (100, 50, 150)
            horizon = (255, 100, 50)
        else:  # Night
            top = (10, 10, 30)
            horizon = (20, 20, 50)
        
        return top, horizon
    
    def render_sky_gradient(self, surface: pygame.Surface):
        """Render smooth sky gradient from top to horizon."""
        top_color, horizon_color = self.get_sky_colors()
        
        # Create vertical gradient
        gradient_height = int(self.height * (1.0 - self.horizon_blend))
        
        for y in range(gradient_height):
            # Calculate blend factor (0.0 at top, 1.0 at horizon)
            blend = y / gradient_height
            
            # Interpolate colors
            color = tuple(
                int(top_color[i] * (1 - blend) + horizon_color[i] * blend)
                for i in range(3)
            )
            
            # Draw horizontal line
            pygame.draw.line(surface, color, (0, y), (self.width, y))
        
        # Fill bottom part with horizon color
        pygame.draw.rect(surface, horizon_color, (
            0, gradient_height, self.width, self.height - gradient_height
        ))
    
    def get_sun_position(self) -> Tuple[int, int]:
        """Calculate sun position with smooth interpolation and caching."""
        # Check cache first for performance
        cache_key = (self.day_of_year, round(self.animation_time, 1))
        if cache_key in self._position_cache:
            cached_pos = self._position_cache[cache_key]
            return self._smooth_position(cached_pos, self.sun_pos_history)
        
        # Calculate new position
        raw_pos = self._calculate_raw_sun_position()
        
        # Cache the result
        self._position_cache[cache_key] = raw_pos
        
        # Apply smoothing
        return self._smooth_position(raw_pos, self.sun_pos_history)
    
    def _calculate_raw_sun_position(self) -> Tuple[int, int]:
        """Calculate raw sun position without smoothing."""
        hour = self.animation_time
        
        # Get actual sunrise/sunset data for current day
        if self.has_data:
            day_data = self._get_cached_day_data(self.day_of_year)
            if day_data and day_data.get('sunrise') is not None and day_data.get('sunset') is not None:
                sunrise = day_data['sunrise']
                sunset = day_data['sunset']
                
                # Use actual astronomical data for sun position
                if hour < sunrise:
                    day_progress = 0  # Before sunrise
                elif hour > sunset:
                    day_progress = 1  # After sunset
                else:
                    daylight_duration = sunset - sunrise
                    day_progress = (hour - sunrise) / daylight_duration if daylight_duration > 0 else 0
            else:
                # Fallback to default times if no data
                day_progress = self._get_fallback_day_progress(hour)
        else:
            # No data available, use fallback
            day_progress = self._get_fallback_day_progress(hour)
        
        # Sun path parameters
        arc_width = self.width * 0.8
        arc_height = self.height * 0.5
        center_x = self.width // 2
        base_y = self.height * 0.8
        
        # Smooth arc calculation
        x_offset = (arc_width / 2) * (2 * day_progress - 1)  # -1 to 1
        sun_x = center_x + x_offset
        
        # Parabolic height calculation for smooth arc
        height_factor = 1 - (2 * day_progress - 1) ** 2  # Parabola: 0 at edges, 1 at center
        sun_y = base_y - arc_height * height_factor
        
        return int(sun_x), int(sun_y)
    
    def _get_fallback_day_progress(self, hour: float) -> float:
        """Fallback day progress calculation when no astronomical data available."""
        # Use default sunrise/sunset times (6 AM to 6 PM)
        if hour < 6:
            return 0  # Before sunrise
        elif hour > 18:
            return 1  # After sunset
        else:
            return (hour - 6) / 12  # 0 to 1 during day
    
    def get_moon_position(self) -> Tuple[int, int]:
        """Calculate moon position with smooth interpolation based on real data."""
        # Check cache first
        cache_key = (self.day_of_year, round(self.animation_time, 1))
        if cache_key in self._position_cache:
            cached_pos = self._position_cache.get(cache_key + ('moon',))
            if cached_pos:
                return self._smooth_position(cached_pos, self.moon_pos_history)
        
        # Calculate new position
        raw_pos = self._calculate_raw_moon_position()
        
        # Cache the result
        self._position_cache[cache_key + ('moon',)] = raw_pos
        
        # Apply smoothing
        return self._smooth_position(raw_pos, self.moon_pos_history)
    
    def _calculate_raw_moon_position(self) -> Tuple[int, int]:
        """Calculate raw moon position using cached astronomical data."""
        if not self.has_data:
            print(f"DEBUG: Using fallback moon position (no data) at {self.animation_time:.2f}h")
            return self._get_fallback_moon_position()
        
        try:
            # Use cached astronomical data
            day_data = self._get_cached_day_data(self.day_of_year)
            current_hour = self.animation_time
            
            # First check if we should use previous day's cross-day moon
            prev_day_data = self._get_cached_day_data(self.day_of_year - 1) if self.day_of_year > 1 else None
            if (prev_day_data and 
                prev_day_data.get('moonrise') is not None and 
                prev_day_data.get('moonset') is not None and
                prev_day_data['moonrise'] > prev_day_data['moonset']):
                # Previous day had cross-day moon that should continue to today
                prev_moonrise = prev_day_data['moonrise']
                prev_moonset = prev_day_data['moonset']  # This is the moonset time for today
                
                # Moon should be visible from 00:00 until the moonset time
                if current_hour <= prev_moonset:
                    # Calculate progress: moon has been visible since prev_moonrise yesterday
                    total_duration = (24.0 - prev_moonrise) + prev_moonset
                    time_since_rise = (24.0 - prev_moonrise) + current_hour
                    progress = time_since_rise / total_duration if total_duration > 0 else 0
                    
                    return self._calculate_moon_arc_position(progress)
            
            if day_data and day_data.get('moonrise') is not None and day_data.get('moonset') is not None:
                # Case: both moonrise and moonset exist for current day
                moonrise = day_data['moonrise']
                moonset = day_data['moonset']
                
                # Check if moon is currently visible with improved logic
                is_visible, progress = self._calculate_moon_visibility(current_hour, moonrise, moonset)
                
                if is_visible and progress is not None:
                    return self._calculate_moon_arc_position(progress)
                else:
                    return (-100, -100)  # Off-screen position
                    
            elif day_data and day_data.get('moonrise') is None and day_data.get('moonset') is not None:
                # Cross-day case: no moonrise today but moonset exists (moon rose yesterday)
                moonset = day_data['moonset']
                current_hour = self.animation_time
                
                # Moon is visible from start of day until moonset
                if current_hour <= moonset:
                    # Need to get previous day's moonrise to calculate total duration
                    prev_day_data = self._get_cached_day_data(self.day_of_year - 1)
                    if prev_day_data and prev_day_data.get('moonrise') is not None:
                        prev_moonrise = prev_day_data['moonrise']
                        # Total duration spans from previous day's moonrise to today's moonset
                        total_duration = (24.0 - prev_moonrise) + moonset
                        # Time elapsed since moonrise (including previous day)
                        time_since_rise = (24.0 - prev_moonrise) + current_hour
                        progress = time_since_rise / total_duration if total_duration > 0 else 0
                    else:
                        # Fallback: approximate progress based on current day only
                        progress = current_hour / moonset if moonset > 0 else 0
                    
                    return self._calculate_moon_arc_position(progress)
                else:
                    return (-100, -100)  # Off-screen position
            else:
                print(f"DEBUG: Invalid day data for day {self.day_of_year}, using fallback")
            
        except Exception as e:
            print(f"Moon position calculation error: {e}")
            print(f"DEBUG: Exception in moon calculation, using fallback")
        
        return self._get_fallback_moon_position()
    
    def _calculate_moon_visibility(self, current_hour: float, moonrise: float, moonset: float) -> Tuple[bool, Optional[float]]:
        """Determine if moon is visible and calculate its progress along arc."""
        if moonrise < moonset:
            # Normal case: moon rises then sets within same day
            if moonrise <= current_hour <= moonset:
                moon_duration = moonset - moonrise
                progress = (current_hour - moonrise) / moon_duration if moon_duration > 0 else 0
                return True, progress
            else:
                return False, None
        else:
            # Cross-day case: moonrise > moonset means moonset is NEXT day
            # Total moon duration spans from moonrise on current day to moonset on next day
            total_duration = (24.0 - moonrise) + moonset  # e.g., (24-23.283) + 11.233 = 12.05 hours
            
            if current_hour >= moonrise:
                # Current day: after moonrise until end of day
                time_since_rise = current_hour - moonrise
                progress = time_since_rise / total_duration if total_duration > 0 else 0
                return True, progress
            else:
                # Current day: before moonrise - not visible
                return False, None
    
    def _calculate_moon_arc_position(self, progress: float) -> Tuple[int, int]:
        """Calculate moon position along its arc given progress (0.0 to 1.0)."""
        # Moon arc parameters
        arc_width = self.width * 0.85  # Moon travels 85% of screen width
        arc_height = self.height * 0.6  # Maximum moon height
        center_x = self.width // 2
        base_y = self.height * 0.85  # Moon's baseline
        
        # Calculate position along arc
        angle = progress * math.pi  # 0 to π radians
        moon_x = center_x - (arc_width // 2) + (arc_width * progress)
        moon_y = base_y - arc_height * math.sin(angle)
        
        return int(moon_x), int(moon_y)
    
    def _get_fallback_moon_position(self) -> Tuple[int, int]:
        """Fallback moon position calculation when no data available."""
        print(f"DEBUG: Using fallback moon logic at {self.animation_time:.2f}h on day {self.day_of_year}")
        
        # Try to use approximate moonrise/moonset times even in fallback mode
        # Most moons rise in evening/night and set in morning
        approximate_moonrise = 20.0  # 8 PM average
        approximate_moonset = 8.0    # 8 AM average
        
        # Check if moon should be visible using approximate times
        current_hour = self.animation_time
        
        # Moon is visible from moonrise to moonset (crossing midnight)
        if current_hour >= approximate_moonrise or current_hour <= approximate_moonset:
            # Calculate progress through visibility period
            if current_hour >= approximate_moonrise:
                # After moonrise, before midnight
                time_since_rise = current_hour - approximate_moonrise
                total_visible = (24 - approximate_moonrise) + approximate_moonset
                progress = time_since_rise / total_visible if total_visible > 0 else 0
            else:
                # After midnight, before moonset
                time_since_rise = (24 - approximate_moonrise) + current_hour
                total_visible = (24 - approximate_moonrise) + approximate_moonset
                progress = time_since_rise / total_visible if total_visible > 0 else 0
            
            # Use the same arc calculation as normal moon
            return self._calculate_moon_arc_position(progress)
        else:
            # Daytime - moon not visible
            return (-100, -100)  # Off-screen
        
        # Use same movement pattern as moon arc (LEFT to RIGHT)
        arc_width = self.width * 0.7
        arc_height = self.height * 0.5
        center_x = self.width // 2
        base_y = self.height * 0.9
        
        # Calculate position using same formula as real moon data
        moon_x = center_x - (arc_width // 2) + (arc_width * night_progress)
        
        # Calculate height using sine for natural arc
        angle = night_progress * math.pi  # 0 to π radians
        moon_y = base_y - arc_height * math.sin(angle)
        
        return int(moon_x), int(moon_y)
    
    def render_celestial_bodies(self, surface: pygame.Surface):
        """Render sun and moon with optimized cached glow effects and smooth transitions."""
        # Get actual sunrise/sunset times from data instead of hardcoded values
        if self.has_data:
            day_data = self._get_cached_day_data(self.day_of_year)
            if day_data and day_data.get('sunrise') is not None and day_data.get('sunset') is not None:
                sunrise = day_data['sunrise']
                sunset = day_data['sunset']
                is_day = sunrise <= self.animation_time <= sunset
            else:
                # Fallback to default times if no data
                is_day = 6 <= self.animation_time <= 18
        else:
            # No data available, use fallback
            is_day = 6 <= self.animation_time <= 18
        
        # Render sun during day with cached glow and fade transitions
        if is_day:
            sun_x, sun_y = self.get_sun_position()
            
            # Calculate visibility alpha for smooth edge transitions
            sun_alpha = self._calculate_celestial_alpha(sun_x, sun_y)
            
            if sun_alpha > 0:
                # Determine sun intensity based on time of day
                sun_intensity = self._calculate_sun_intensity()
                
                # Use cached glow effect with alpha
                if sun_intensity in self._sun_glow_cache:
                    glow_surface = self._sun_glow_cache[sun_intensity].copy()
                    # Apply alpha to glow
                    if sun_alpha < 1.0:
                        glow_surface.set_alpha(int(255 * sun_alpha))
                    
                    glow_radius = self.sun_radius + 15
                    surface.blit(glow_surface, (sun_x - glow_radius, sun_y - glow_radius), 
                               special_flags=pygame.BLEND_ADD)
                
                # Sun body - simple and efficient with alpha
                sun_color = (255, 255, 200)
                if sun_alpha < 1.0:
                    # Create alpha surface for smooth fade
                    sun_surf = pygame.Surface((self.sun_radius*2, self.sun_radius*2), pygame.SRCALPHA)
                    pygame.draw.circle(sun_surf, (*sun_color, int(255 * sun_alpha)), 
                                     (self.sun_radius, self.sun_radius), self.sun_radius)
                    surface.blit(sun_surf, (sun_x - self.sun_radius, sun_y - self.sun_radius))
                else:
                    pygame.draw.circle(surface, sun_color, (sun_x, sun_y), self.sun_radius)
                    pygame.draw.circle(surface, (255, 220, 100), (sun_x, sun_y), self.sun_radius, 2)
        
        # Render moon with cached glow and smooth transitions
        moon_x, moon_y = self.get_moon_position()
        
        # Calculate moon visibility alpha
        moon_alpha = self._calculate_celestial_alpha(moon_x, moon_y) if moon_x > 0 and moon_y > 0 else 0
        
        if moon_alpha > 0:
            # Get moon phase and render efficiently
            moon_illumination = self._get_moon_illumination()
            
            # Moon color intensity based on illumination
            base_intensity = 200
            moon_intensity = int(base_intensity * (0.3 + 0.7 * moon_illumination))
            moon_color = (moon_intensity, moon_intensity, moon_intensity)
            
            # Use cached glow based on moon phase
            if moon_illumination > 0.3:  # Only show glow for brighter moon phases
                # Find closest cached glow
                closest_phase = min(self._moon_glow_cache.keys(), key=lambda x: abs(x - moon_illumination))
                if closest_phase in self._moon_glow_cache:
                    glow_surface = self._moon_glow_cache[closest_phase].copy()
                    # Apply alpha to glow
                    if moon_alpha < 1.0:
                        glow_surface.set_alpha(int(255 * moon_alpha))
                    
                    glow_radius = self.moon_radius + 8
                    surface.blit(glow_surface, (moon_x - glow_radius, moon_y - glow_radius),
                               special_flags=pygame.BLEND_ADD)
            
            # Draw moon body with smooth edge transition
            if moon_alpha < 1.0:
                # Create alpha surface for smooth fade
                moon_surf = pygame.Surface((self.moon_radius*2, self.moon_radius*2), pygame.SRCALPHA)
                pygame.draw.circle(moon_surf, (*moon_color, int(255 * moon_alpha)), 
                                 (self.moon_radius, self.moon_radius), self.moon_radius)
                surface.blit(moon_surf, (moon_x - self.moon_radius, moon_y - self.moon_radius))
            else:
                pygame.draw.circle(surface, moon_color, (moon_x, moon_y), self.moon_radius)
    
    def _calculate_celestial_alpha(self, x: int, y: int) -> float:
        """Calculate alpha for smooth edge transitions when celestial bodies move off-screen."""
        if x < 0 or y < 0 or x > self.width or y > self.height:
            return 0.0
        
        # Create fade zones at screen edges
        fade_zone = 50  # Pixels from edge where fade starts
        alpha = 1.0
        
        # Left edge fade
        if x < fade_zone:
            alpha = min(alpha, x / fade_zone)
        
        # Right edge fade
        if x > self.width - fade_zone:
            alpha = min(alpha, (self.width - x) / fade_zone)
        
        # Top edge fade
        if y < fade_zone:
            alpha = min(alpha, y / fade_zone)
        
        # Bottom edge fade (less aggressive for horizon)
        if y > self.height - fade_zone//2:
            alpha = min(alpha, (self.height - y) / (fade_zone//2))
        
        return max(0.0, min(1.0, alpha))
    
    def _calculate_sun_intensity(self) -> float:
        """Calculate sun intensity based on time of day."""
        hour = self.animation_time
        if hour < 6 or hour > 18:
            return 0.3  # Dim during non-day hours
        elif 6 <= hour <= 8 or 16 <= hour <= 18:
            return 0.7  # Medium during sunrise/sunset
        else:
            return 1.0  # Bright during midday
    
    def _get_moon_illumination(self) -> float:
        """Get moon illumination with caching for performance."""
        # Check cache first
        if self.day_of_year in self._moon_illumination_cache:
            return self._moon_illumination_cache[self.day_of_year]
        
        if hasattr(self, 'moon_calculator') and self.moon_calculator:
            try:
                # Calculate date for moon phase
                base_date = datetime(2024, 1, 1)
                current_date = base_date + timedelta(days=self.day_of_year - 1)
                date_str = current_date.strftime('%Y-%m-%d')
                
                illumination = self.moon_calculator.get_moon_illumination(date_str)
                # Cache the result
                self._moon_illumination_cache[self.day_of_year] = illumination
                return illumination
            except Exception:
                return 0.5  # Fallback illumination
        else:
            return 0.5  # Default illumination
    
    def is_night_time(self) -> bool:
        """Check if current time is night."""
        return not (6 <= self.animation_time <= 18)

class TimeLapseVisualization:
    """Main class combining Hong Kong skyline with animated sky."""
    
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Time's Pixel - Hong Kong Time Lapse")
        
        # Initialize components
        self.skyline_renderer = HongKongSkylineRenderer(width, height)
        self.sky_animation = SkyAnimationEngine(width, height)
        
        # Animation control
        self.paused = False
        self.show_help = False
        self.clock = pygame.time.Clock()
        
        # Fonts for UI
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 18)
        
        print("Hong Kong Time Lapse Visualization initialized!")
        print("Controls:")
        print("  SPACE - Pause/Resume animation")
        print("  ← → - Change animation speed (0.01x to 5.0x)")
        print("  Q W - Fine speed control (cycle presets)")
        print("  ↑ ↓ - Jump days")
        print("  1-9 - Quick time range presets")
        print("  T - Toggle time range loop")
        print("  R - Reset to day 1")
        print("  ESC - Exit")
        print()
        print("Time Range Presets:")
        print("  1 - Dawn (4-8 AM)")
        print("  2 - Morning (6-12 PM)")
        print("  3 - Sunset (4-8 PM)")
        print("  4 - Night (6 PM-6 AM)")
        print("  5 - Full day (24 hours)")
        print("  6 - Spring season")
        print("  7 - Summer season")
        print("  8 - Autumn season")
        print("  9 - Winter season")
        print("  R - Reset to day 1")
        print("  ESC - Exit")
    
    def handle_events(self) -> bool:
        """Handle user input events with enhanced time range and speed controls."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                    print(f"Animation {'paused' if self.paused else 'resumed'}")
                
                # Speed controls
                elif event.key == pygame.K_LEFT:
                    self.sky_animation.animation_speed = max(0.01, self.sky_animation.animation_speed - 0.01)
                    print(f"Speed: {self.sky_animation.animation_speed:.3f}x")
                elif event.key == pygame.K_RIGHT:
                    self.sky_animation.animation_speed = min(5.0, self.sky_animation.animation_speed + 0.01)
                    print(f"Speed: {self.sky_animation.animation_speed:.3f}x")
                elif event.key == pygame.K_q:
                    speed = self.sky_animation.cycle_speed_preset(-1)
                    print(f"Speed preset: {speed:.3f}x")
                elif event.key == pygame.K_w:
                    speed = self.sky_animation.cycle_speed_preset(1)
                    print(f"Speed preset: {speed:.3f}x")
                
                # Day controls
                elif event.key == pygame.K_UP:
                    self.sky_animation.day_of_year = min(366, self.sky_animation.day_of_year + 1)
                    print(f"Day: {self.sky_animation.day_of_year}")
                elif event.key == pygame.K_DOWN:
                    self.sky_animation.day_of_year = max(1, self.sky_animation.day_of_year - 1)
                    print(f"Day: {self.sky_animation.day_of_year}")
                
                # Time range presets
                elif event.key == pygame.K_1:  # Dawn (4-8 AM)
                    self.sky_animation.set_time_range(1, 4.0, 1, 8.0, True)
                elif event.key == pygame.K_2:  # Morning (6-12 PM)
                    self.sky_animation.set_time_range(1, 6.0, 1, 12.0, True)
                elif event.key == pygame.K_3:  # Sunset (4-8 PM)
                    self.sky_animation.set_time_range(1, 16.0, 1, 20.0, True)
                elif event.key == pygame.K_4:  # Night (6 PM-6 AM)
                    self.sky_animation.set_time_range(1, 18.0, 2, 6.0, True)
                elif event.key == pygame.K_5:  # Full day
                    self.sky_animation.set_time_range(1, 0.0, 1, 24.0, True)
                elif event.key == pygame.K_6:  # Spring (Mar-May)
                    self.sky_animation.set_time_range(80, 0.0, 150, 24.0, True)
                elif event.key == pygame.K_7:  # Summer (Jun-Aug)
                    self.sky_animation.set_time_range(151, 0.0, 243, 24.0, True)
                elif event.key == pygame.K_8:  # Autumn (Sep-Nov)
                    self.sky_animation.set_time_range(244, 0.0, 334, 24.0, True)
                elif event.key == pygame.K_9:  # Winter (Dec-Feb)
                    self.sky_animation.set_time_range(335, 0.0, 79, 24.0, True)
                
                # Other controls
                elif event.key == pygame.K_h:
                    self.show_help = not self.show_help
                    print(f"Help {'shown' if self.show_help else 'hidden'}")
                elif event.key == pygame.K_t:
                    self.sky_animation.loop_time_range = not self.sky_animation.loop_time_range
                    print(f"Time range loop: {'ON' if self.sky_animation.loop_time_range else 'OFF'}")
                elif event.key == pygame.K_r:
                    self.sky_animation.set_time(1, 6.0)
                    self.sky_animation.loop_time_range = False
                    print("Reset to day 1, 6:00 AM (loop disabled)")
        
        return True
    
    def render_ui(self):
        """Render enhanced user interface overlay with time range information."""
        info = self.sky_animation.get_animation_info()
        
        # Calculate UI panel size based on content
        panel_height = 200 if info['loop_range'] else 140
        
        # Semi-transparent background for UI
        ui_surface = pygame.Surface((400, panel_height), pygame.SRCALPHA)
        ui_surface.fill((0, 0, 0, 128))
        self.screen.blit(ui_surface, (10, 10))
        
        # Time and date information
        date_text = self.font_medium.render(f"Day {info['day']}/366{info['progress_info']}", True, (255, 255, 255))
        time_text = self.font_medium.render(f"Time: {info['time_str']}", True, (255, 255, 255))
        speed_text = self.font_small.render(f"Speed: {info['speed_preset']}", True, (255, 255, 255))
        status_text = self.font_small.render("PAUSED" if self.paused else "PLAYING", True, 
                                           (255, 100, 100) if self.paused else (100, 255, 100))
        
        # Blit basic UI text
        y_offset = 20
        self.screen.blit(date_text, (20, y_offset))
        y_offset += 25
        self.screen.blit(time_text, (20, y_offset))
        y_offset += 25
        self.screen.blit(speed_text, (20, y_offset))
        y_offset += 25
        self.screen.blit(status_text, (20, y_offset))
        y_offset += 25
        
        # Time range information if active
        if info['loop_range']:
            range_title = self.font_small.render("Time Range Loop:", True, (200, 255, 200))
            range_start = self.font_small.render(f"Start: {info['range_start']}", True, (255, 255, 255))
            range_end = self.font_small.render(f"End: {info['range_end']}", True, (255, 255, 255))
            
            self.screen.blit(range_title, (20, y_offset))
            y_offset += 20
            self.screen.blit(range_start, (20, y_offset))
            y_offset += 20
            self.screen.blit(range_end, (20, y_offset))
        
        # Controls hint (bottom right)
        controls_text = self.font_small.render("Press H for help", True, (150, 150, 150))
        self.screen.blit(controls_text, (self.width - 120, self.height - 25))
    
    def render_help_overlay(self):
        """Render help overlay with all controls."""
        if not self.show_help:
            return
        
        # Create semi-transparent overlay
        overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))
        
        # Help content
        help_lines = [
            "TIME'S PIXEL - HELP",
            "",
            "Animation Controls:",
            "  SPACE - Pause/Resume",
            "  Q/W - Cycle speed presets",
            "  ← → - Fine speed adjustment",
            "  T - Toggle time range loop",
            "",
            "Navigation:",
            "  ↑ ↓ - Jump days",
            "  R - Reset to Day 1",
            "",
            "Time Range Presets:",
            "  1 - Dawn (4-8 AM)",
            "  2 - Morning (6-12 PM)",
            "  3 - Sunset (4-8 PM)",
            "  4 - Night (6 PM-6 AM)",
            "  5 - Full day (24 hours)",
            "  6 - Spring season",
            "  7 - Summer season",
            "  8 - Autumn season",
            "  9 - Winter season",
            "",
            "Press H to close help",
            "Press ESC to exit"
        ]
        
        # Render help text
        start_y = 50
        for i, line in enumerate(help_lines):
            if line == "TIME'S PIXEL - HELP":
                text = self.font_large.render(line, True, (255, 255, 100))
                x = (self.width - text.get_width()) // 2
            elif line.startswith("  "):
                text = self.font_small.render(line, True, (200, 200, 200))
                x = 100
            elif line == "":
                continue
            else:
                text = self.font_medium.render(line, True, (255, 255, 255))
                x = 80
            
            self.screen.blit(text, (x, start_y + i * 25))
    
    def run(self):
        """Main animation loop."""
        running = True
        
        while running:
            # Handle events
            running = self.handle_events()
            
            # Update animation
            if not self.paused:
                delta_time = self.clock.get_time() / 1000.0 * 30  # Convert to minutes (slower pace)
                self.sky_animation.update_animation(delta_time)
            
            # Render frame
            self.screen.fill((0, 0, 0))
            
            # Render sky background
            self.sky_animation.render_sky_gradient(self.screen)
            
            # Render celestial bodies
            self.sky_animation.render_celestial_bodies(self.screen)
            
            # Render Hong Kong skyline
            self.skyline_renderer.render_skyline(self.screen, self.sky_animation.is_night_time())
            
            # Render UI
            self.render_ui()
            
            # Render help overlay if active
            self.render_help_overlay()
            
            # Update display
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()

# Entry point for running the visualization
def main():
    """Run the Hong Kong time-lapse visualization."""
    try:
        visualization = TimeLapseVisualization()
        visualization.run()
    except Exception as e:
        print(f"Error running visualization: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()