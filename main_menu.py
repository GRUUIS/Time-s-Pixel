#!/usr/bin/env python3
"""
Time's Pixel - Enhanced Main Menu System
A comprehensive menu for accessing all visualization modes with scrolling support
"""

import pygame
import sys
import os
import subprocess
from typing import Dict, List

class TimePixelMainMenu:
    """Enhanced main menu system for Time's Pixel visualizations"""
    
    def __init__(self, width: int = 1400, height: int = 950):
        pygame.init()
        
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Time's Pixel - Enhanced Visualization Menu")
        
        # Scrolling variables
        self.scroll_y = 0
        self.max_scroll = 0
        self.scroll_speed = 30
        
        # Layout constants
        self.card_width = 380
        self.card_height = 260
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
            self.font_subtitle = pygame.font.Font(None, 28)
            self.font_body = pygame.font.Font(None, 22)
            self.font_small = pygame.font.Font(None, 18)
        except:
            # Fallback to default font
            self.font_title = pygame.font.SysFont('Arial', 48, bold=True)
            self.font_subtitle = pygame.font.SysFont('Arial', 28, bold=True)
            self.font_body = pygame.font.SysFont('Arial', 22)
            self.font_small = pygame.font.SysFont('Arial', 18)
        
        # Menu items configuration
        self.menu_items = [
            # Interactive Visualizations
            {
                'title': '🌅 Timelapse Animation',
                'subtitle': 'Hong Kong Skyline Journey',
                'description': 'Experience a full year of Hong Kong sunrises and sunsets with realistic skyline animation.',
                'features': ['16:9 Optimized Display', 'Adaptive Screen Sizing', '20% Viewport Cropping', 'F11 Fullscreen Mode'],
                'script': 'scripts/run_timelapse.py',
                'category': 'interactive'
            },
            {
                'title': '🌀 3D Time Spiral',
                'subtitle': 'Innovative Temporal Structure',
                'description': 'Explore time as a beautiful 3D spiral where each day becomes a point in space.',
                'features': ['Custom 3D Engine', 'Interactive Rotation', 'Astronomical Mapping', 'Moon Phase Colors'],
                'script': 'scripts/run_spiral_3d.py',
                'category': 'interactive'
            },
            {
                'title': '🎯 Interactive Explorer',
                'subtitle': 'Click-to-Discover Interface',
                'description': 'Navigate through time with pixel-perfect precision and detailed astronomical data.',
                'features': ['Pixel-level Interaction', 'Smooth Scrolling', 'Real-time Data Display', 'Multiple Palettes'],
                'script': 'scripts/run_interactive.py',
                'category': 'interactive'
            },
            # Static Image Display
            {
                'title': '🎨 Enhanced Pixel Art',
                'subtitle': 'View High-Resolution Artwork',
                'description': 'View beautiful pixel art representations of astronomical data with enhanced colors and palettes.',
                'features': ['High Resolution Display', 'Multiple Color Palettes', 'Seasonal Markers', 'Moon Phase Integration'],
                'script': 'scripts/image_generation/run_enhanced_pixel_art.py',
                'category': 'static'
            },
            {
                'title': '⭕ Circular Cosmic Clock',
                'subtitle': 'View Radial Time Art',
                'description': 'View circular visualizations that show the cosmic rhythm of time in Hong Kong.',
                'features': ['Circular Layout', 'Radial Time Mapping', 'Cosmic Design', 'Full Resolution'],
                'script': 'scripts/image_generation/run_circular_clock.py',
                'category': 'static'
            },
            {
                'title': '🌙 Moon Phase Analysis',
                'subtitle': 'View Lunar Cycle Art',
                'description': 'View detailed moon phase visualizations with accurate lunar cycle data and beautiful design.',
                'features': ['Accurate Moon Phases', 'Lunar Calendar', 'Phase Progression', 'Scientific Data'],
                'script': 'scripts/image_generation/run_moon_analysis.py',
                'category': 'static'
            }
        ]
        
        # Group items by category
        self.interactive_items = [item for item in self.menu_items if item.get('category') == 'interactive']
        self.static_items = [item for item in self.menu_items if item.get('category') == 'static']
        
        # Calculate layout positions
        self.calculate_layout()
        
        # State
        self.selected_item = 0
        self.mouse_pos = (0, 0)
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Get project root for script execution
        self.project_root = os.path.dirname(os.path.abspath(__file__))
        
        # Calculate maximum scroll distance
        self.calculate_max_scroll()
    
    def calculate_layout(self):
        """Calculate card positions for both categories"""
        # Interactive row
        interactive_width = len(self.interactive_items) * self.card_width + (len(self.interactive_items) - 1) * self.card_margin
        self.interactive_start_x = (self.width - interactive_width) // 2
        self.interactive_y = self.header_height + 60
        
        # Static row
        static_width = len(self.static_items) * self.card_width + (len(self.static_items) - 1) * self.card_margin
        self.static_start_x = (self.width - static_width) // 2
        self.static_y = self.interactive_y + self.card_height + 80
    
    def calculate_max_scroll(self):
        """Calculate the maximum scroll distance needed"""
        content_bottom = self.static_y + self.card_height + 50
        visible_area = self.height - self.footer_height
        self.max_scroll = max(0, content_bottom - visible_area)
        
    def clamp_scroll(self):
        """Keep scroll within valid bounds"""
        self.scroll_y = max(0, min(self.scroll_y, self.max_scroll))
    
    def wrap_text(self, text: str, font: pygame.font.Font, max_width: int) -> List[str]:
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
            y = self.interactive_y - self.scroll_y
        else:  # static items
            # Find position in static items
            static_index = next(i for i, it in enumerate(self.static_items) if it == item)
            x = self.static_start_x + static_index * (self.card_width + self.card_margin)
            y = self.static_y - self.scroll_y
            
        return pygame.Rect(x, y, self.card_width, self.card_height)
    
    def get_launch_button_rect(self, item_index: int) -> pygame.Rect:
        """Get the rectangle for a launch button"""
        card_rect = self.get_card_rect(item_index)
        button_width = 160
        button_height = 32
        x = card_rect.x + (self.card_width - button_width) // 2
        y = card_rect.bottom - 45
        return pygame.Rect(x, y, button_width, button_height)
    
    def launch_visualization(self, script_path: str):
        """Launch a visualization script"""
        try:
            full_path = os.path.join(self.project_root, script_path)
            print(f"🚀 Launching: {script_path}")
            print(f"Python: {sys.executable}")
            print(f"Script: {full_path}")
            
            if os.path.exists(full_path):
                result = subprocess.run([sys.executable, full_path], 
                                      cwd=self.project_root,
                                      capture_output=False)
                print(f"✅ Visualization completed with code: {result.returncode}")
            else:
                print(f"❌ Script not found: {full_path}")
                
        except Exception as e:
            print(f"❌ Error launching visualization: {e}")
    
    def handle_mouse_click(self, pos):
        """Handle mouse clicks on buttons"""
        for i, item in enumerate(self.menu_items):
            button_rect = self.get_launch_button_rect(i)
            if button_rect.collidepoint(pos):
                self.launch_visualization(item['script'])
                break
    
    def handle_events(self):
        """Handle pygame events with scroll support"""
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
    
    def draw_header(self):
        """Draw the header with title and subtitle"""
        title_text = self.font_title.render("Time's Pixel", True, self.colors['text_primary'])
        title_rect = title_text.get_rect(center=(self.width // 2, 40))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.font_body.render("Enhanced Visualization Suite - Choose Your Experience", True, self.colors['accent'])
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 80))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_categories(self):
        """Draw category headers"""
        # Interactive category header
        interactive_y = self.interactive_y - 40 - self.scroll_y
        if interactive_y > -30 and interactive_y < self.height:
            interactive_text = self.font_subtitle.render("🎮 Interactive Visualizations", True, self.colors['accent'])
            interactive_rect = interactive_text.get_rect(center=(self.width // 2, interactive_y))
            self.screen.blit(interactive_text, interactive_rect)
        
        # Static category header  
        static_y = self.static_y - 40 - self.scroll_y
        if static_y > -30 and static_y < self.height:
            static_text = self.font_subtitle.render("🖼️ Static Image Gallery", True, self.colors['accent'])
            static_rect = static_text.get_rect(center=(self.width // 2, static_y))
            self.screen.blit(static_text, static_rect)
    
    def draw_card(self, index: int, item: Dict):
        """Draw a menu card with proper text wrapping and boundary checking"""
        card_rect = self.get_card_rect(index)
        button_rect = self.get_launch_button_rect(index)
        
        # Skip drawing if card is completely outside visible area
        if card_rect.bottom < -50 or card_rect.top > self.height + 50:
            return
        
        # Check if mouse is over card or button
        mouse_over_card = card_rect.collidepoint(self.mouse_pos)
        mouse_over_button = button_rect.collidepoint(self.mouse_pos)
        
        # Determine category for styling
        is_interactive = item.get('category') == 'interactive'
        
        # Category-specific colors
        if is_interactive:
            card_color = (60, 80, 120) if mouse_over_card else (40, 50, 80)
            border_color = (100, 150, 200) if mouse_over_card else (80, 100, 140)
            button_color = (80, 150, 200) if mouse_over_button else (60, 120, 180)
            text_color = (220, 240, 255)
            subtitle_color = (120, 170, 255)
        else:
            card_color = (80, 60, 100) if mouse_over_card else (60, 40, 70)
            border_color = (150, 100, 180) if mouse_over_card else (100, 80, 120)
            button_color = (150, 80, 150) if mouse_over_button else (120, 60, 120)
            text_color = (240, 220, 255)
            subtitle_color = (200, 150, 200)
        
        # Draw card background
        pygame.draw.rect(self.screen, card_color, card_rect, border_radius=12)
        pygame.draw.rect(self.screen, border_color, card_rect, width=2, border_radius=12)
        
        # Content positioning with proper margins
        content_x = card_rect.x + 15
        content_width = self.card_width - 30
        current_y = card_rect.y + 15
        
        # Title (ensure it fits)
        title_lines = self.wrap_text(item['title'], self.font_subtitle, content_width)
        for line in title_lines[:1]:
            title_text = self.font_subtitle.render(line, True, text_color)
            self.screen.blit(title_text, (content_x, current_y))
            current_y += 32
        
        # Subtitle
        subtitle_lines = self.wrap_text(item['subtitle'], self.font_body, content_width)
        for line in subtitle_lines[:1]:
            subtitle_text = self.font_body.render(line, True, subtitle_color)
            self.screen.blit(subtitle_text, (content_x, current_y))
            current_y += 26
        
        # Description (wrapped, limited lines)
        desc_text = item['description'].replace('\\n', ' ')
        wrapped_desc = self.wrap_text(desc_text, self.font_small, content_width)
        
        for line in wrapped_desc[:3]:
            desc_surface = self.font_small.render(line, True, self.colors['text_secondary'])
            self.screen.blit(desc_surface, (content_x, current_y))
            current_y += 18
        
        current_y += 8
        
        # Features (limited to fit in card)
        max_features = 2
        for feature in item.get('features', [])[:max_features]:
            wrapped_feature = self.wrap_text(f"• {feature}", self.font_small, content_width - 10)
            for line in wrapped_feature[:1]:
                feature_text = self.font_small.render(line, True, self.colors['text_secondary'])
                self.screen.blit(feature_text, (content_x + 5, current_y))
                current_y += 16
        
        # Launch button
        pygame.draw.rect(self.screen, button_color, button_rect, border_radius=8)
        
        button_text_content = "🚀 Launch" if is_interactive else "🖼️ View"
        button_text = self.font_body.render(button_text_content, True, (255, 255, 255))
        button_text_rect = button_text.get_rect(center=button_rect.center)
        self.screen.blit(button_text, button_text_rect)
    
    def draw_scroll_indicator(self):
        """Draw scroll indicator if content is scrollable"""
        if self.max_scroll > 0:
            # Scroll bar background
            bar_x = self.width - 20
            bar_y = self.header_height
            bar_height = self.height - self.header_height - self.footer_height
            
            pygame.draw.rect(self.screen, (40, 40, 40), (bar_x, bar_y, 15, bar_height))
            
            # Scroll indicator
            indicator_height = max(20, bar_height * (self.height / (self.height + self.max_scroll)))
            indicator_y = bar_y + (bar_height - indicator_height) * (self.scroll_y / self.max_scroll)
            
            pygame.draw.rect(self.screen, self.colors['accent'], (bar_x + 2, indicator_y, 11, indicator_height), border_radius=5)
    
    def draw_footer(self):
        """Draw footer with instructions"""
        footer_y = self.height - 80
        
        instructions = [
            "🖱️ Mouse wheel or ↑↓ arrows to scroll • Click buttons to launch/view",
            "⌨️ Press 1-6 for quick access • ESC to exit",
            "🎮 Tip: Try the Timelapse Animation first for the best experience!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.colors['accent'] if i == 2 else self.colors['text_secondary']
            font = self.font_body if i == 2 else self.font_small
            
            text = font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width // 2, footer_y + i * 22))
            self.screen.blit(text, text_rect)
    
    def draw(self):
        """Draw the entire menu with scroll support"""
        # Clear screen
        self.screen.fill(self.colors['background'])
        
        # Draw components (header stays fixed)
        self.draw_header()
        
        # Draw scrollable content
        self.draw_categories()
        
        # Draw cards
        for i, item in enumerate(self.menu_items):
            self.draw_card(i, item)
        
        # Draw UI elements
        self.draw_scroll_indicator()
        self.draw_footer()
        
        # Update display
        pygame.display.flip()
    
    def update(self):
        """Update the menu state"""
        pass
    
    def run(self):
        """Main menu loop"""
        print("🎨 Time's Pixel - Enhanced Main Menu")
        print("=" * 60)
        print("Welcome to the comprehensive Time's Pixel visualization suite!")
        print("Choose from 6 amazing ways to explore astronomical data:")
        print()
        print("🎮 INTERACTIVE VISUALIZATIONS:")
        for i, item in enumerate(self.interactive_items, 1):
            print(f"  {i}. {item['title']} - {item['subtitle']}")
        print()
        print("🖼️ STATIC IMAGE GALLERY:")
        for i, item in enumerate(self.static_items, 4):
            print(f"  {i}. {item['title']} - {item['subtitle']}")
        print()
        print("🎮 Controls:")
        print("  • Click buttons to launch visualizations or view images")
        print("  • Mouse wheel or arrow keys to scroll")
        print("  • Press 1-6 for quick access")
        print("  • ESC to exit")
        print("=" * 60)
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        print("\\n👋 Thanks for exploring Time's Pixel!")

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
        print("\\n👋 Menu closed by user")
    except Exception as e:
        print(f"❌ Error running menu: {e}")
        print("💡 Make sure pygame is installed: pip install pygame")

if __name__ == "__main__":
    main()