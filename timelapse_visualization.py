#!/usr/bin/env python3
"""
Time's Pixel - Main Menu & Visualization Launcher
A comprehensive menu system to explore all visualization modes in the Time's Pixel project.

Features:
- Visual menu with preview images
- Easy navigation between different visualization modes
- Project information and controls guide
- Direct launch capability for each visualization
"""

import pygame
import sys
import os
import subprocess
from typing import Dict, List, Tuple, Optional

class TimePixelMainMenu:
    """Main menu system for Time's Pixel visualizations"""
    
    def __init__(self, width: int = 1400, height: int = 950):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Time's Pixel - Visualization Menu")
        
        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30
        
        # Layout constants
        self.card_width = 400
        self.card_height = 280
        self.cards_per_row = 3
        self.card_margin = 30
        self.header_height = 120
        self.footer_height = 100
        
        # Colors
        self.colors = {
            'background': (15, 25, 35),      # Dark blue
            'card_bg': (25, 35, 50),         # Slightly lighter blue
            'card_hover': (35, 50, 70),      # Hover state
            'text_primary': (255, 255, 255), # White
            'text_secondary': (180, 190, 200), # Light gray
            'accent': (100, 150, 255),       # Blue accent
            'button': (50, 120, 200),        # Button blue
            'button_hover': (70, 140, 220),  # Button hover
        }
        
        # Fonts
        try:
            self.font_title = pygame.font.Font(None, 48)
            self.font_subtitle = pygame.font.Font(None, 32)
            self.font_body = pygame.font.Font(None, 24)
            self.font_small = pygame.font.Font(None, 20)
        except:
            # Fallback to default font
            self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
            self.font_subtitle = pygame.font.SysFont('Arial', 32, bold=True)
            self.font_body = pygame.font.SysFont('Arial', 24)
            self.font_small = pygame.font.SysFont('Arial', 20)
        
        # Menu items configuration
        self.menu_items = [
            {
                'title': '🌅 Timelapse Animation',
                'subtitle': 'Hong Kong Skyline Journey',
                'description': 'Experience a full year of Hong Kong sunrises and sunsets\nwith realistic skyline animation and atmospheric colors.',
                'features': ['16:9 Optimized Display', 'Adaptive Screen Sizing', '20% Viewport Cropping', 'F11 Fullscreen Mode'],
                'script': 'scripts/run_timelapse.py',
                'difficulty': 'Beginner Friendly',
                'duration': '∞ (Interactive)',
                'type': 'Animation',
                'category': 'interactive'
            },
            {
                'title': '🌀 3D Time Spiral',
                'subtitle': 'Innovative Temporal Structure',
                'description': 'Explore time as a beautiful 3D spiral where each day\nbecomes a point in space, colored by astronomical data.',
                'features': ['Custom 3D Engine', 'Interactive Rotation', 'Astronomical Mapping', 'Moon Phase Colors'],
                'script': 'scripts/run_spiral_3d.py',
                'difficulty': 'Intermediate',
                'duration': '∞ (Interactive)',
                'type': 'Innovation',
                'category': 'interactive'
            },
            {
                'title': '🎯 Interactive Explorer',
                'subtitle': 'Click-to-Discover Interface',
                'description': 'Click any day to explore detailed astronomical data\nwith smooth scrolling and real-time information.',
                'features': ['Click-to-Explore', 'Real-time Data', 'Multiple Palettes', 'Smooth Scrolling'],
                'script': 'scripts/run_interactive.py',
                'difficulty': 'Beginner Friendly',
                'duration': '∞ (Interactive)',
                'type': 'Exploration',
                'category': 'interactive'
            },
            {
                'title': '🎨 Enhanced Pixel Art',
                'subtitle': 'High-Resolution Static Image',
                'description': 'Generate beautiful pixel art visualization with\nenhanced colors and realistic twilight transitions.',
                'features': ['Multiple Color Palettes', 'High Resolution Output', 'PNG Export', 'Realistic Twilight'],
                'script': 'src/visualizations/enhanced_visualization.py',
                'difficulty': 'Beginner Friendly',
                'duration': '~30 seconds',
                'type': 'Image Generation',
                'category': 'static'
            },
            {
                'title': '⭕ Circular Cosmic Clock',
                'subtitle': 'Radial Time Visualization',
                'description': 'Create a stunning circular visualization showing\nthe full year as a cosmic clock with seasonal markers.',
                'features': ['Circular Layout', 'Seasonal Markers', '1200x1200 Resolution', 'Astronomical Events'],
                'script': 'src/visualizations/utils/generate_circular_image.py',
                'difficulty': 'Intermediate',
                'duration': '~45 seconds',
                'type': 'Image Generation',
                'category': 'static'
            },
            {
                'title': '🌙 Moon Phase Analysis',
                'subtitle': 'Lunar Cycle Visualization',
                'description': 'Generate detailed moon phase visualizations\nwith accurate lunar calculations and phase strips.',
                'features': ['Accurate Moon Phases', 'Visual Phase Strip', 'Astronomical Precision', 'Educational Content'],
                'script': 'src/visualizations/accurate_moon_visualization.py',
                'difficulty': 'Intermediate',
                'duration': '~20 seconds',
                'type': 'Image Generation',
                'category': 'static'
            }
        ]
        
        # Layout configuration
        self.card_width = 300
        self.card_height = 420
        self.card_margin = 20
        self.header_height = 140
        self.category_height = 40
        
        # Group items by category
        self.interactive_items = [item for item in self.menu_items if item.get('category') == 'interactive']
        self.static_items = [item for item in self.menu_items if item.get('category') == 'static']
        
        # Calculate positions for two rows
        interactive_width = len(self.interactive_items) * self.card_width + (len(self.interactive_items) - 1) * self.card_margin
        static_width = len(self.static_items) * self.card_width + (len(self.static_items) - 1) * self.card_margin
        
        self.interactive_start_x = (self.width - interactive_width) // 2
        self.static_start_x = (self.width - static_width) // 2
        self.interactive_y = self.header_height + self.category_height + 20
        self.static_y = self.interactive_y + self.card_height + self.category_height + 40
        
        # State
        self.selected_item = 0
        self.mouse_pos = (0, 0)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Get project root for script execution
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # Calculate maximum scroll distance
        self.calculate_max_scroll()
    
    def calculate_max_scroll(self):
        """Calculate the maximum scroll distance needed"""
        # Calculate total content height
        content_bottom = self.static_y + self.card_height + 50  # Extra padding
        visible_area = self.height - self.footer_height
        
        self.max_scroll = max(0, content_bottom - visible_area)
        
    def clamp_scroll(self):
        """Keep scroll within valid bounds"""
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> list:
        """Wrap text to fit within specified width"""
        words = text.split(' ')
        lines = []
        current_line = ""
        
        for word in words:
            test_line = current_line + word + " " if current_line else word + " "
            if font.size(test_line)[0] <= max_width:
                current_line = test_line
            else:
                if current_line:
                    lines.append(current_line.strip())
                    current_line = word + " "
                else:
                    # Single word is too long, force it anyway
                    lines.append(word)
                    current_line = ""
        
        if current_line:
            lines.append(current_line.strip())
        
        return lines
        
    def get_card_rect(self, item_index: int) -> pygame.Rect:
        """Get the rectangle for a menu card based on category with scroll support"""
        item = self.menu_items[item_index]
        
        if item.get('category') == 'interactive':
            # Find position in interactive items
            interactive_index = next(i for i, it in enumerate(self.interactive_items) if it == item)
            x = self.interactive_start_x + interactive_index * (self.card_width + self.card_margin)
            y = self.interactive_y - self.scroll_y  # Apply scroll offset
        else:  # static items
            # Find position in static items
            static_index = next(i for i, it in enumerate(self.static_items) if it == item)
            x = self.static_start_x + static_index * (self.card_width + self.card_margin)
            y = self.static_y - self.scroll_y  # Apply scroll offset
            
        return pygame.Rect(x, y, self.card_width, self.card_height)
    
    def get_launch_button_rect(self, item_index: int) -> pygame.Rect:
        """Get the rectangle for a launch button"""
        card_rect = self.get_card_rect(item_index)
        button_width = 180
        button_height = 35
        x = card_rect.x + (self.card_width - button_width) // 2
        y = card_rect.bottom - 50
        return pygame.Rect(x, y, button_width, button_height)
    
    def draw_header(self):
        """Draw the main header"""
        # Title
        title_text = self.font_title.render("Time's Pixel", True, self.colors['text_primary'])
        title_rect = title_text.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle_text = self.font_subtitle.render("Choose Your Visualization Journey", True, self.colors['text_secondary'])
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_card(self, index: int, item: Dict):
        """Draw a menu card"""
        card_rect = self.get_card_rect(index)
        button_rect = self.get_launch_button_rect(index)
        
        # Check if mouse is over card or button
        mouse_over_card = card_rect.collidepoint(self.mouse_pos)
        mouse_over_button = button_rect.collidepoint(self.mouse_pos)
        
        # Card background
        card_color = self.colors['card_hover'] if mouse_over_card else self.colors['card_bg']
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=15)
        
        # Card border
        border_color = self.colors['accent'] if mouse_over_card else self.colors['text_secondary']
        pygame.draw.rect(self.screen, border_color, card_rect, width=2, border_radius=15)
        
        # Content positioning
        content_x = card_rect.x + 20
        current_y = card_rect.y + 20
        
        # Title
        title_text = self.font_subtitle.render(item['title'], True, self.colors['text_primary'])
        self.screen.blit(title_text, (content_x, current_y))
        current_y += 40
        
        # Subtitle
        subtitle_text = self.font_body.render(item['subtitle'], True, self.colors['accent'])
        self.screen.blit(subtitle_text, (content_x, current_y))
        current_y += 40
        
        # Description (multi-line)
        desc_lines = item['description'].split('\n')
        for line in desc_lines:
            desc_text = self.font_small.render(line, True, self.colors['text_secondary'])
            self.screen.blit(desc_text, (content_x, current_y))
            current_y += 25
        
        current_y += 15
        
        # Features
        features_title = self.font_body.render("✨ Features:", True, self.colors['text_primary'])
        self.screen.blit(features_title, (content_x, current_y))
        current_y += 30
        
        for feature in item['features']:
            feature_text = self.font_small.render(f"• {feature}", True, self.colors['text_secondary'])
            self.screen.blit(feature_text, (content_x + 10, current_y))
            current_y += 22
        
        current_y += 15
        
        # Info badges
        info_y = current_y
        
        # Difficulty
        diff_text = self.font_small.render(f"🎯 {item['difficulty']}", True, self.colors['text_secondary'])
        self.screen.blit(diff_text, (content_x, info_y))
        
        # Type
        type_text = self.font_small.render(f"� {item['type']}", True, self.colors['text_secondary'])
        self.screen.blit(type_text, (content_x, info_y + 20))
        
        # Launch button
        button_color = self.colors['button_hover'] if mouse_over_button else self.colors['button']
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
        
        button_text = self.font_body.render("🚀 Launch", True, self.colors['text_primary'])
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
    
    def draw_footer(self):
        """Draw footer with instructions"""
        footer_y = self.height - 100
        
        instructions = [
            "Click '🚀 Launch' for interactive experiences or '🎨 Generate' for static images",
            "Press 1-6 for quick launch • Press ESC to exit",
            "🎮 Tip: Try the Timelapse Animation first for the best experience!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.colors['accent'] if i == 2 else self.colors['text_secondary']
            font = self.font_body if i == 2 else self.font_small
            
            text = font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width // 2, footer_y + i * 25))
            self.screen.blit(text, text_rect)
    
    def launch_visualization(self, script_path: str):
        """Launch a visualization script"""
        try:
            # Get the Python executable path
            python_exe = os.path.join(self.project_root, '.venv', 'Scripts', 'python.exe')
            if not os.path.exists(python_exe):
                python_exe = 'python'  # Fallback to system Python
            
            script_full_path = os.path.join(self.project_root, script_path)
            
            print(f"🚀 Launching: {script_path}")
            print(f"Python: {python_exe}")
            print(f"Script: {script_full_path}")
            
            # Launch the script
            subprocess.Popen([python_exe, script_full_path], cwd=self.project_root)
            
            print("✅ Visualization launched successfully!")
            print("🔄 Returning to menu in a moment...")
            
        except Exception as e:
            print(f"❌ Error launching visualization: {e}")
            print("💡 Make sure the script exists and Python environment is properly set up")
    
    def handle_mouse_click(self, pos: Tuple[int, int]):
        """Handle mouse click events"""
        for i, item in enumerate(self.menu_items):
            button_rect = self.get_launch_button_rect(i)
            if button_rect.collidepoint(pos):
                self.launch_visualization(item['script'])
                break
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_UP:
                    self.scroll_y -= self.scroll_speed
                    self.clamp_scroll()
                elif event.key == pygame.K_DOWN:
                    self.scroll_y += self.scroll_speed
                    self.clamp_scroll()
                elif event.key == pygame.K_PAGEUP:
                    self.scroll_y -= self.scroll_speed * 3
                    self.clamp_scroll()
                elif event.key == pygame.K_PAGEDOWN:
                    self.scroll_y += self.scroll_speed * 3
                    self.clamp_scroll()
                elif event.key == pygame.K_HOME:
                    self.scroll_y = 0
                elif event.key == pygame.K_END:
                    self.scroll_y = self.max_scroll
                elif event.key == pygame.K_1 and len(self.menu_items) > 0:
                    self.launch_visualization(self.menu_items[0]['script'])
                elif event.key == pygame.K_2 and len(self.menu_items) > 1:
                    self.launch_visualization(self.menu_items[1]['script'])
                elif event.key == pygame.K_3 and len(self.menu_items) > 2:
                    self.launch_visualization(self.menu_items[2]['script'])
                elif event.key == pygame.K_4 and len(self.menu_items) > 3:
                    self.launch_visualization(self.menu_items[3]['script'])
                elif event.key == pygame.K_5 and len(self.menu_items) > 4:
                    self.launch_visualization(self.menu_items[4]['script'])
                elif event.key == pygame.K_6 and len(self.menu_items) > 5:
                    self.launch_visualization(self.menu_items[5]['script'])
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_mouse_click(event.pos)
                elif event.button == 4:  # Mouse wheel up
                    self.scroll_y -= self.scroll_speed
                    self.clamp_scroll()
                elif event.button == 5:  # Mouse wheel down
                    self.scroll_y += self.scroll_speed
                    self.clamp_scroll()
            
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
    
    def update(self):
        """Update game state"""
        pass
    
    def draw_categories(self):
        """Draw category headers"""
        # Interactive category header
        interactive_y = 180
        interactive_text = self.font_subtitle.render("🎮 Interactive Visualizations", True, self.colors['accent'])
        interactive_rect = interactive_text.get_rect(center=(self.width // 2, interactive_y))
        self.screen.blit(interactive_text, interactive_rect)
        
        # Static category header  
        static_y = 550
        static_text = self.font_subtitle.render("🖼️ Static Image Generation", True, self.colors['accent'])
        static_rect = static_text.get_rect(center=(self.width // 2, static_y))
        self.screen.blit(static_text, static_rect)

    def draw(self):
        """Draw the entire menu"""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw components
        self.draw_header()
        self.draw_categories()
        
        # Draw cards
        for i, item in enumerate(self.menu_items):
            self.draw_card(i, item)
        
        self.draw_footer()
        
        # Update display
        pygame.display.flip()
    
    def run(self):
        """Main menu loop"""
        print("🎨 Time's Pixel - Main Menu")
        print("=" * 50)
        print("Welcome to the Time's Pixel visualization suite!")
        print("Choose from three amazing ways to explore astronomical data:")
        print()
        for i, item in enumerate(self.menu_items, 1):
            print(f"{i}. {item['title']} - {item['subtitle']}")
        print()
        print("🎮 Controls:")
        print("  • Click buttons to launch visualizations")
        print("  • Press 1, 2, 3 for quick launch")
        print("  • ESC to exit")
        print("=" * 50)
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        print("\n👋 Thanks for exploring Time's Pixel!")

def main():
    """Main function"""
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("⚠️  Warning: Please run this script from the Time-s-Pixel root directory")
        print("💡 Current directory should contain 'src', 'scripts', and 'data' folders")
    
    try:
        menu = TimePixelMainMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\n👋 Menu closed by user")
    except Exception as e:
        print(f"❌ Error running menu: {e}")
        print("💡 Make sure pygame is installed: pip install pygame")

if __name__ == "__main__":
    main()