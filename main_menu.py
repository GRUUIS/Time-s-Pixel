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
        
        # Layout constants (optimized for better spacing)
        self.card_width = 240
        self.card_height = 220
        self.card_margin = 25
        self.header_height = 100
        self.footer_height = 80
        
        # Colors (refined modern theme)
        self.colors = {
            'background': (18, 28, 38),      # Darker modern blue
            'card_bg': (28, 40, 56),         # Card background
            'card_hover': (40, 56, 76),      # Hover state
            'text_primary': (245, 248, 250), # Off-white
            'text_secondary': (165, 180, 195), # Light gray
            'accent': (88, 144, 255),        # Brighter accent blue
            'button': (88, 144, 255),        # Primary button color
            'button_hover': (108, 164, 255), # Button hover
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
                'title': 'Timelapse Animation',
                'subtitle': 'Hong Kong Skyline Journey',
                'description': 'Full year Hong Kong sunrises and sunsets animation.',
                'features': ['Optimized Display', 'Fullscreen Mode', 'Adaptive Sizing'],
                'script': 'scripts/run_timelapse.py',
                'category': 'interactive'
            },
            {
                'title': '3D Time Spiral',
                'subtitle': 'Innovative Temporal Structure',
                'description': 'Time visualized as an interactive 3D spiral.',
                'features': ['3D Engine', 'Interactive Rotation', 'Moon Phases'],
                'script': 'scripts/run_spiral_3d.py',
                'category': 'interactive'
            },
            {
                'title': 'Interactive Explorer',
                'subtitle': 'Click-to-Discover Interface',
                'description': 'Navigate time with pixel-perfect precision.',
                'features': ['Pixel Interaction', 'Smooth Scrolling', 'Multiple Palettes'],
                'script': 'scripts/run_interactive.py',
                'category': 'interactive'
            },
            # Dynamic Circular Visualization
            {
                'title': 'Dynamic Circular Clock',
                'subtitle': 'Interactive Radial Time Explorer',
                'description': 'Dynamic circular time visualization with interaction.',
                'features': ['Real-time Navigation', 'Seasonal Markers', 'Click Exploration'],
                'script': 'src/visualizations/circular_visualization.py',
                'category': 'interactive'
            },
            {
                'title': 'Circular Cosmic Clock',
                'subtitle': 'View Radial Time Art',
                'description': 'Static circular visualization of Hong Kong time.',
                'features': ['Circular Layout', 'Cosmic Design', 'High Resolution'],
                'script': 'scripts/image_generation/run_circular_clock.py',
                'category': 'static'
            },
            {
                'title': 'Moon Phase Analysis',
                'subtitle': 'View Lunar Cycle Art',
                'description': 'Detailed moon phase visualizations and data.',
                'features': ['Accurate Phases', 'Lunar Calendar', 'Scientific Data'],
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
        """Calculate card positions for both categories with improved spacing"""
        # Interactive row - check if cards fit in one row
        max_cards_per_row = (self.width - 2 * self.card_margin) // (self.card_width + self.card_margin)
        
        # Interactive row
        interactive_count = len(self.interactive_items)
        if interactive_count <= max_cards_per_row:
            # Single row
            interactive_width = interactive_count * self.card_width + (interactive_count - 1) * self.card_margin
            self.interactive_start_x = (self.width - interactive_width) // 2
            self.interactive_y = self.header_height + 40
        else:
            # Multi-row layout (if needed in future)
            self.interactive_start_x = self.card_margin
            self.interactive_y = self.header_height + 40
        
        # Static row
        static_count = len(self.static_items)
        if static_count <= max_cards_per_row:
            # Single row
            static_width = static_count * self.card_width + (static_count - 1) * self.card_margin
            self.static_start_x = (self.width - static_width) // 2
            self.static_y = self.interactive_y + self.card_height + 60
        else:
            # Multi-row layout (if needed in future)
            self.static_start_x = self.card_margin
            self.static_y = self.interactive_y + self.card_height + 60
    
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
            print(f"Launching: {script_path}")
            print(f"Python: {sys.executable}")
            print(f"Script: {full_path}")
            
            if os.path.exists(full_path):
                result = subprocess.run([sys.executable, full_path], 
                                      cwd=self.project_root,
                                      capture_output=False)
                print(f"Visualization completed with code: {result.returncode}")
            else:
                print(f"Script not found: {full_path}")
                
        except Exception as e:
            print(f"Error launching visualization: {e}")
    
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
        """Draw the header with improved styling"""
        # Main title
        title_text = self.font_title.render("Time's Pixel", True, self.colors['text_primary'])
        title_rect = title_text.get_rect(center=(self.width // 2, 35))
        self.screen.blit(title_text, title_rect)
        
        # Subtitle with better spacing
        subtitle_text = self.font_body.render("Enhanced Visualization Suite", True, self.colors['accent'])
        subtitle_rect = subtitle_text.get_rect(center=(self.width // 2, 70))
        self.screen.blit(subtitle_text, subtitle_rect)
    
    def draw_categories(self):
        """Draw category headers"""
        # Interactive category header
        interactive_y = self.interactive_y - 40 - self.scroll_y
        if interactive_y > -30 and interactive_y < self.height:
            interactive_text = self.font_subtitle.render("Interactive Visualizations", True, self.colors['accent'])
            interactive_rect = interactive_text.get_rect(center=(self.width // 2, interactive_y))
            self.screen.blit(interactive_text, interactive_rect)
        
        # Static category header  
        static_y = self.static_y - 40 - self.scroll_y
        if static_y > -30 and static_y < self.height:
            static_text = self.font_subtitle.render("Static Image Gallery", True, self.colors['accent'])
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
        
        button_text_content = "Launch" if is_interactive else "View"
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
            "Scroll: Mouse wheel/arrows • Click: Launch • 1-6: Quick access • ESC: Exit",
            "Tip: Try Timelapse Animation first!"
        ]
        
        for i, instruction in enumerate(instructions):
            color = self.colors['accent'] if i == 1 else self.colors['text_secondary']
            font = self.font_body if i == 1 else self.font_small
            
            text = font.render(instruction, True, color)
            text_rect = text.get_rect(center=(self.width // 2, footer_y + i * 25))
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
        print("Time's Pixel - Main Menu")
        print("=" * 40)
        print("Astronomical Data Visualization Suite")
        print()
        print("INTERACTIVE VISUALIZATIONS:")
        for i, item in enumerate(self.interactive_items, 1):
            print(f"  {i}. {item['title']}")
        print()
        print("STATIC IMAGE GALLERY:")
        for i, item in enumerate(self.static_items, 4):
            print(f"  {i}. {item['title']}")
        print()
        print("Controls: Click buttons, scroll, press 1-6, ESC to exit")
        print("=" * 40)
        
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        print("\\nThanks for using Time's Pixel!")

def main():
    """Main function"""
    # Check if we're in the right directory
    if not os.path.exists('src'):
        print("Warning: Please run this script from the Time-s-Pixel root directory")
        print("Current directory should contain 'src', 'scripts', and 'data' folders")
    
    try:
        menu = TimePixelMainMenu()
        menu.run()
    except KeyboardInterrupt:
        print("\\nMenu closed by user")
    except Exception as e:
        print(f"Error running menu: {e}")
        print("Make sure pygame is installed: pip install pygame")

if __name__ == "__main__":
    main()