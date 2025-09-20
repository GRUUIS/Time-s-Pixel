#!/usr/bin/env python3
"""
Time Spiral - 3D Temporal Data Visualization
Transform Hong Kong 2024 sun and moon rise/set data into a beautiful 3D time spiral artwork

Creative Concept:
- 365 days form a spiral structure, each day is a point on the spiral
- Daylight duration determines point height (summer high, winter low)
- Moon phase data affects point color and size
- The entire structure can rotate, users can observe time flow from different angles
"""

import pygame
import numpy as np
import math
import csv
from datetime import datetime, timedelta
from typing import List, Tuple, Dict, Optional

class TimeSpiral3D:
    """3D Time Spiral Visualization"""
    
    def __init__(self, width: int = 1200, height: int = 800):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Time Spiral - 3D Temporal Visualization")
        
        # 3D projection parameters
        self.camera_distance = 800
        self.rotation_x = 0
        self.rotation_y = 0
        self.rotation_z = 0
        self.zoom = 1.0
        
        # Spiral parameters
        self.spiral_radius = 200
        self.spiral_height = 400
        self.turns = 3  # Number of spiral turns
        
        # Data storage
        self.sun_data = []
        self.moon_data = []
        self.spiral_points = []
        
        # Animation parameters
        self.auto_rotate = True
        self.rotation_speed = 0.01
        
        # Color theme
        self.bg_color = (5, 5, 20)  # Deep space background
        self.spiral_colors = {
            'spring': (100, 255, 150),  # Spring - Fresh green
            'summer': (255, 200, 50),   # Summer - Golden yellow
            'autumn': (255, 100, 50),   # Autumn - Orange red
            'winter': (150, 200, 255)   # Winter - Ice blue
        }
        
        self.load_data()
        self.generate_spiral()
        
        print("🌟 Time Spiral Visualization Initialized!")
        print("Controls:")
        print("  Mouse: Rotate view")
        print("  Wheel: Zoom in/out")
        print("  SPACE: Toggle auto-rotation")
        print("  R: Reset view")
        print("  ESC: Exit")
    
    def load_data(self):
        """Load sun and moon rise/set data"""
        try:
            # Try to use the proper data path relative to project root
            import os
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            sun_data_path = os.path.join(project_root, 'data', 'hongkong_sunrise_sunset_2024_clean.csv')
            moon_data_path = os.path.join(project_root, 'data', 'moonrise_moonset_2024_clean.csv')
            
            # Load sun data (sunrise, transit, sunset)
            with open(sun_data_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row['RISE'] and row['SET']:
                        rise_time = self.parse_time(row['RISE'])
                        set_time = self.parse_time(row['SET'])
                        transit_time = self.parse_time(row['TRAN.']) if row['TRAN.'] else None
                        
                        if rise_time and set_time:
                            # Calculate daylight duration (hours)
                            if set_time > rise_time:
                                daylight_hours = (set_time - rise_time) / 3600
                            else:
                                # Cross-day case (shouldn't happen with sun data)
                                daylight_hours = (24 * 3600 - rise_time + set_time) / 3600
                            
                            self.sun_data.append({
                                'date': row['YYYY-MM-DD'],
                                'rise': rise_time,
                                'transit': transit_time,
                                'set': set_time,
                                'daylight_hours': daylight_hours
                            })
            
            # Load moon data (moonrise, transit, moonset)
            with open(moon_data_path, 'r') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    moon_rise = self.parse_time(row['RISE']) if row['RISE'] else None
                    moon_set = self.parse_time(row['SET']) if row['SET'] else None
                    moon_transit = self.parse_time(row['TRAN.']) if row['TRAN.'] else None
                    
                    # Calculate moon visibility duration if both rise and set exist
                    moon_visibility = None
                    if moon_rise is not None and moon_set is not None:
                        if moon_set > moon_rise:
                            moon_visibility = (moon_set - moon_rise) / 3600
                        else:
                            # Moon crosses midnight
                            moon_visibility = (24 * 3600 - moon_rise + moon_set) / 3600
                    
                    self.moon_data.append({
                        'date': row['YYYY-MM-DD'],
                        'rise': moon_rise,
                        'transit': moon_transit,
                        'set': moon_set,
                        'visibility_hours': moon_visibility
                    })
            
            print(f"📅 Loaded {len(self.sun_data)} days of sun rise/set data")
            print(f"🌙 Loaded {len(self.moon_data)} days of moon rise/set data")
            
        except Exception as e:
            print(f"❌ Error loading data: {e}")
            # Generate sample data
            self.generate_sample_data()
    
    def parse_time(self, time_str: str) -> Optional[float]:
        """Convert time string to seconds"""
        if not time_str or time_str.strip() == '':
            return None
        try:
            hours, minutes = map(int, time_str.split(':'))
            return hours * 3600 + minutes * 60
        except:
            return None
    
    def generate_sample_data(self):
        """Generate sample data (if unable to load real data)"""
        print("🔧 Generating sample data...")
        for day in range(365):
            # Simulate seasonal daylight variation
            angle = day / 365 * 2 * math.pi
            base_daylight = 12 + 2 * math.sin(angle - math.pi/2)  # 10-14 hours
            
            self.sun_data.append({
                'date': f"2024-{(day//30)+1:02d}-{(day%30)+1:02d}",
                'daylight_hours': base_daylight
            })
            
            # Simulate moon phase (29.5 day cycle)
            moon_phase = (day % 29.5) / 29.5
            self.moon_data.append({
                'date': f"2024-{(day//30)+1:02d}-{(day%30)+1:02d}",
                'phase': moon_phase
            })
    
    def generate_spiral(self):
        """Generate 3D spiral points"""
        self.spiral_points = []
        
        for i, sun_day in enumerate(self.sun_data):
            if i >= len(self.moon_data):
                break
                
            # Spiral parameters
            t = i / len(self.sun_data) * self.turns * 2 * math.pi
            
            # X, Y coordinates (spiral)
            x = self.spiral_radius * math.cos(t) * (1 + i / len(self.sun_data))
            y = self.spiral_radius * math.sin(t) * (1 + i / len(self.sun_data))
            
            # Z coordinate (height based on daylight duration)
            daylight = sun_day.get('daylight_hours', 12)
            z = (daylight - 10) / 4 * self.spiral_height - self.spiral_height / 2
            
            # Determine color based on season
            season = self.get_season(i)
            base_color = self.spiral_colors[season]
            
            # Moon phase affects point size and brightness
            moon_day = self.moon_data[i]
            if moon_day.get('visibility_hours') is not None:
                # Use actual moon visibility data
                moon_visibility = moon_day['visibility_hours']
                brightness = min(1.0, moon_visibility / 12)  # Normalize to 0-1
            else:
                # Estimate moon phase from day cycle
                moon_phase = (i % 29.5) / 29.5
                brightness = 0.3 + 0.7 * (1 - abs(moon_phase - 0.5) * 2)  # Full moon brightest
            
            size = 2 + 4 * brightness
            color = tuple(int(c * brightness) for c in base_color)
            
            self.spiral_points.append({
                'pos': (x, y, z),
                'color': color,
                'size': size,
                'day': i,
                'date': sun_day['date'],
                'daylight': daylight,
                'moon_visibility': moon_day.get('visibility_hours'),
                'sun_rise': sun_day.get('rise'),
                'sun_set': sun_day.get('set'),
                'moon_rise': moon_day.get('rise'),
                'moon_set': moon_day.get('set')
            })
    
    def get_season(self, day_of_year: int) -> str:
        """Determine season based on day of year"""
        if day_of_year < 91:
            return 'winter'
        elif day_of_year < 182:
            return 'spring'
        elif day_of_year < 273:
            return 'summer'
        else:
            return 'autumn'
    
    def project_3d_to_2d(self, x: float, y: float, z: float) -> Tuple[int, int]:
        """Project 3D coordinates to 2D screen coordinates"""
        # Apply rotation transformations
        # Y-axis rotation
        cos_y, sin_y = math.cos(self.rotation_y), math.sin(self.rotation_y)
        x_rot = x * cos_y - z * sin_y
        z_rot = x * sin_y + z * cos_y
        
        # X-axis rotation
        cos_x, sin_x = math.cos(self.rotation_x), math.sin(self.rotation_x)
        y_rot = y * cos_x - z_rot * sin_x
        z_final = y * sin_x + z_rot * cos_x
        
        # Z-axis rotation
        cos_z, sin_z = math.cos(self.rotation_z), math.sin(self.rotation_z)
        x_final = x_rot * cos_z - y_rot * sin_z
        y_final = x_rot * sin_z + y_rot * cos_z
        
        # Perspective projection
        if z_final + self.camera_distance <= 0:
            return (-1000, -1000)  # Behind camera, don't display
        
        scale = self.camera_distance / (z_final + self.camera_distance) * self.zoom
        
        screen_x = int(self.width / 2 + x_final * scale)
        screen_y = int(self.height / 2 - y_final * scale)
        
        return (screen_x, screen_y)
    
    def handle_events(self) -> bool:
        """Handle user input"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.auto_rotate = not self.auto_rotate
                    print(f"🔄 Auto-rotation: {'ON' if self.auto_rotate else 'OFF'}")
                elif event.key == pygame.K_r:
                    self.rotation_x = self.rotation_y = self.rotation_z = 0
                    self.zoom = 1.0
                    print("🔄 View reset")
            
            elif event.type == pygame.MOUSEMOTION:
                if pygame.mouse.get_pressed()[0]:  # Left click drag
                    dx, dy = pygame.mouse.get_rel()
                    self.rotation_y += dx * 0.01
                    self.rotation_x += dy * 0.01
            
            elif event.type == pygame.MOUSEWHEEL:
                zoom_factor = 1.1 if event.y > 0 else 0.9
                self.zoom *= zoom_factor
                self.zoom = max(0.1, min(3.0, self.zoom))
        
        return True
    
    def render(self):
        """Render 3D spiral"""
        self.screen.fill(self.bg_color)
        
        # Sort by Z coordinate for proper depth display
        points_with_depth = []
        for point in self.spiral_points:
            x, y, z = point['pos']
            screen_x, screen_y = self.project_3d_to_2d(x, y, z)
            
            if 0 <= screen_x < self.width and 0 <= screen_y < self.height:
                # Calculate rotated Z coordinate for sorting
                cos_y, sin_y = math.cos(self.rotation_y), math.sin(self.rotation_y)
                cos_x, sin_x = math.cos(self.rotation_x), math.sin(self.rotation_x)
                
                x_rot = x * cos_y - z * sin_y
                z_rot = x * sin_y + z * cos_y
                y_rot = y * cos_x - z_rot * sin_x
                z_final = y * sin_x + z_rot * cos_x
                
                points_with_depth.append((z_final, screen_x, screen_y, point))
        
        # Sort by depth (far ones first)
        points_with_depth.sort(key=lambda p: p[0], reverse=True)
        
        # Draw points
        for z_depth, screen_x, screen_y, point in points_with_depth:
            size = max(1, int(point['size'] * self.zoom))
            pygame.draw.circle(self.screen, point['color'], (screen_x, screen_y), size)
            
            # Draw connections for seasonal transitions (every 91 days)
            if point['day'] % 91 == 0 and point['day'] > 0:  # Connect each season
                prev_point = self.spiral_points[point['day'] - 1]
                prev_x, prev_y, prev_z = prev_point['pos']
                prev_screen_x, prev_screen_y = self.project_3d_to_2d(prev_x, prev_y, prev_z)
                
                if (0 <= prev_screen_x < self.width and 0 <= prev_screen_y < self.height):
                    pygame.draw.line(self.screen, point['color'], 
                                   (prev_screen_x, prev_screen_y), 
                                   (screen_x, screen_y), 1)
        
        # Render information panel
        self.render_info()
    
    def render_info(self):
        """Render information panel"""
        font = pygame.font.Font(None, 24)
        info_lines = [
            "🌟 Time Spiral - Hong Kong 2024",
            f"📊 {len(self.spiral_points)} days visualized",
            f"🔄 Rotation: {self.auto_rotate and 'AUTO' or 'MANUAL'}",
            f"🔍 Zoom: {self.zoom:.1f}x",
            "",
            "Data Sources:",
            "☀️ Sun rise/set times",
            "🌙 Moon rise/set times",
            "",
            "Visualization:",
            "• Height = Daylight duration",
            "• Color = Season",
            "• Brightness = Moon visibility",
            "",
            "Controls:",
            "  Mouse: Rotate view",
            "  Wheel: Zoom",
            "  SPACE: Toggle rotation",
            "  R: Reset view"
        ]
        
        y_offset = 10
        for line in info_lines:
            if line:  # Skip empty lines
                text = font.render(line, True, (255, 255, 255))
                self.screen.blit(text, (10, y_offset))
            y_offset += 20
    
    def update(self):
        """Update animation"""
        if self.auto_rotate:
            self.rotation_y += self.rotation_speed
            if self.rotation_y > 2 * math.pi:
                self.rotation_y -= 2 * math.pi
    
    def run(self):
        """Main loop"""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            running = self.handle_events()
            self.update()
            self.render()
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

def main():
    """Launch 3D Time Spiral Visualization"""
    try:
        spiral = TimeSpiral3D()
        spiral.run()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()