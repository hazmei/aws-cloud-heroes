"""
UI components for AWS Cloud Heroes game.
Contains classes and functions for rendering UI elements.
"""

import pygame
import math
from config import *

class Button:
    """A clickable button with text."""
    
    def __init__(self, x, y, width, height, color, text, text_color, font=None, border_color=None, border_width=0):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = font
        self.border_color = border_color
        self.border_width = border_width
        self.pulsing = False
        self.pulse_speed = 200  # milliseconds per pulse cycle
        self.pulse_amount = 0.05  # how much to scale during pulse
    
    def draw(self, surface):
        """Draw the button on the given surface."""
        width = self.width
        height = self.height
        
        # Apply pulsing effect if enabled
        if self.pulsing:
            pulse_factor = 1.0 + self.pulse_amount * math.sin(pygame.time.get_ticks() / self.pulse_speed)
            width *= pulse_factor
            height *= pulse_factor
        
        # Calculate centered position
        x = self.x - width/2
        y = self.y - height/2
        
        # Draw button background
        button_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, self.color, button_rect, 0, BUTTON_PADDING)
        
        # Draw border if specified
        if self.border_color and self.border_width > 0:
            pygame.draw.rect(surface, self.border_color, button_rect, self.border_width, BUTTON_PADDING)
        
        # Draw text
        if self.font:
            text_surf = self.font.render(self.text, True, self.text_color)
            text_rect = text_surf.get_rect(center=(self.x, self.y))
            surface.blit(text_surf, text_rect)
    
    def is_clicked(self, pos):
        """Check if the button was clicked."""
        width = self.width
        height = self.height
        
        # Apply pulsing effect if enabled
        if self.pulsing:
            pulse_factor = 1.0 + self.pulse_amount * math.sin(pygame.time.get_ticks() / self.pulse_speed)
            width *= pulse_factor
            height *= pulse_factor
        
        # Calculate centered position
        x = self.x - width/2
        y = self.y - height/2
        
        return x <= pos[0] <= x + width and y <= pos[1] <= y + height

class TextRenderer:
    """Helper class for rendering text with effects."""
    
    @staticmethod
    def render_text(surface, text, font, color, position, center=True, shadow=False, shadow_color=BLACK, shadow_offset=(2, 2)):
        """Render text with optional shadow effect."""
        # Render shadow if requested
        if shadow:
            shadow_surf = font.render(text, True, shadow_color)
            shadow_pos = position[0] + shadow_offset[0], position[1] + shadow_offset[1]
            
            if center:
                shadow_rect = shadow_surf.get_rect(center=shadow_pos)
            else:
                shadow_rect = shadow_surf.get_rect(topleft=shadow_pos)
                
            surface.blit(shadow_surf, shadow_rect)
        
        # Render main text
        text_surf = font.render(text, True, color)
        
        if center:
            text_rect = text_surf.get_rect(center=position)
        else:
            text_rect = text_surf.get_rect(topleft=position)
            
        surface.blit(text_surf, text_rect)
        
        return text_rect
