#!/usr/bin/env python3
"""
Image Viewer for Time's Pixel Generated Images
Simple pygame-based image viewer with navigation controls
"""

import pygame
import sys
import os
from PIL import Image
import subprocess

class ImageViewer:
    """Simple image viewer for Time's Pixel images"""
    
    def __init__(self, image_path: str, title: str = "Time's Pixel Image Viewer"):
        pygame.init()
        
        self.image_path = image_path
        self.title = title
        
        # Check if image exists
        if not os.path.exists(image_path):
            print(f"❌ Image not found: {image_path}")
            return
        
        # Load and prepare image
        self.load_image()
        
        # Create window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption(f"{self.title} - {os.path.basename(image_path)}")
        
        # Colors
        self.bg_color = (20, 30, 40)
        self.text_color = (255, 255, 255)
        self.info_color = (150, 200, 255)
        
        # Font
        try:
            self.font = pygame.font.Font(None, 24)
            self.small_font = pygame.font.Font(None, 18)
        except:
            self.font = pygame.font.SysFont('Arial', 24)
            self.small_font = pygame.font.SysFont('Arial', 18)
        
        self.running = True
        self.clock = pygame.time.Clock()
        
    def load_image(self):
        """Load and scale image to fit screen"""
        try:
            # Load image with PIL first to get info
            pil_image = Image.open(self.image_path)
            original_width, original_height = pil_image.size
            
            # Calculate optimal window size (max 1200x800, maintain aspect ratio)
            max_width, max_height = 1200, 800
            aspect_ratio = original_width / original_height
            
            if aspect_ratio > max_width / max_height:
                # Image is wider
                display_width = min(max_width, original_width)
                display_height = int(display_width / aspect_ratio)
            else:
                # Image is taller
                display_height = min(max_height, original_height)
                display_width = int(display_height * aspect_ratio)
            
            # Add padding for UI
            self.window_width = display_width + 40
            self.window_height = display_height + 100
            
            # Load image with pygame
            self.image = pygame.image.load(self.image_path)
            self.image = pygame.transform.scale(self.image, (display_width, display_height))
            self.image_rect = self.image.get_rect(center=(self.window_width // 2, (self.window_height - 60) // 2))
            
            # Store image info
            self.original_size = (original_width, original_height)
            self.display_size = (display_width, display_height)
            
        except Exception as e:
            print(f"❌ Error loading image: {e}")
            sys.exit(1)
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_o:
                    # Open in default image viewer
                    self.open_in_external_viewer()
                elif event.key == pygame.K_f:
                    # Open folder containing the image
                    self.open_folder()
    
    def open_in_external_viewer(self):
        """Open image in system default viewer"""
        try:
            if sys.platform == "win32":
                os.startfile(self.image_path)
            elif sys.platform == "darwin":
                subprocess.run(["open", self.image_path])
            else:
                subprocess.run(["xdg-open", self.image_path])
        except Exception as e:
            print(f"❌ Error opening external viewer: {e}")
    
    def open_folder(self):
        """Open folder containing the image"""
        try:
            folder_path = os.path.dirname(self.image_path)
            if sys.platform == "win32":
                subprocess.run(["explorer", folder_path])
            elif sys.platform == "darwin":
                subprocess.run(["open", folder_path])
            else:
                subprocess.run(["xdg-open", folder_path])
        except Exception as e:
            print(f"❌ Error opening folder: {e}")
    
    def draw_info(self):
        """Draw image information"""
        info_y = self.window_height - 55
        
        # Image name
        name_text = self.font.render(os.path.basename(self.image_path), True, self.text_color)
        name_rect = name_text.get_rect(center=(self.window_width // 2, info_y))
        self.screen.blit(name_text, name_rect)
        
        # Size info
        size_info = f"Original: {self.original_size[0]}×{self.original_size[1]} | Display: {self.display_size[0]}×{self.display_size[1]}"
        size_text = self.small_font.render(size_info, True, self.info_color)
        size_rect = size_text.get_rect(center=(self.window_width // 2, info_y + 25))
        self.screen.blit(size_text, size_rect)
        
        # Controls
        controls = "ESC/Q: Close | O: Open in external viewer | F: Open folder"
        controls_text = self.small_font.render(controls, True, self.info_color)
        controls_rect = controls_text.get_rect(center=(self.window_width // 2, 15))
        self.screen.blit(controls_text, controls_rect)
    
    def draw(self):
        """Draw the viewer"""
        self.screen.fill(self.bg_color)
        
        # Draw image
        self.screen.blit(self.image, self.image_rect)
        
        # Draw border around image
        pygame.draw.rect(self.screen, (100, 100, 100), self.image_rect, 2)
        
        # Draw info
        self.draw_info()
        
        pygame.display.flip()
    
    def run(self):
        """Main viewer loop"""
        print(f"🖼️ Opening image viewer: {os.path.basename(self.image_path)}")
        print(f"📐 Original size: {self.original_size[0]}×{self.original_size[1]}")
        print(f"🎮 Controls: ESC/Q to close, O to open externally, F to open folder")
        
        while self.running:
            self.handle_events()
            self.draw()
            self.clock.tick(60)
        
        pygame.quit()
        print(f"👋 Image viewer closed")

def main():
    """Main function"""
    if len(sys.argv) != 2:
        print("Usage: python image_viewer.py <image_path>")
        sys.exit(1)
    
    image_path = sys.argv[1]
    viewer = ImageViewer(image_path, "Time's Pixel Gallery")
    viewer.run()

if __name__ == "__main__":
    main()