"""
Animation components for AWS Cloud Heroes game.
Contains classes and functions for creating and managing animations.
"""

import pygame
import random
import math
from config import *

class AnimationManager:
    """Manages animated elements on the screen."""
    
    def __init__(self, surface):
        self.surface = surface
        self.clouds = []
        self.stars = []
        self.lambda_functions = []
        self.initialized = False
    
    def initialize(self):
        """Initialize animation elements."""
        # Create clouds (representing AWS cloud)
        self.clouds = []
        for i in range(5):
            cloud = {
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(50, 150),
                'size': random.randint(60, 100),
                'speed': random.uniform(0.5, 1.5)
            }
            self.clouds.append(cloud)
        
        # Create stars (representing S3)
        self.stars = []
        for i in range(8):
            star = {
                'x': random.randint(0, WINDOW_WIDTH),
                'y': random.randint(50, WINDOW_HEIGHT - 100),
                'size': random.randint(15, 30),
                'angle': 0,
                'speed': random.uniform(0.02, 0.05)
            }
            self.stars.append(star)
        
        # Create lambda functions (representing AWS Lambda)
        self.lambda_functions = []
        for i in range(3):
            lambda_func = {
                'x': random.randint(50, WINDOW_WIDTH - 50),
                'y': random.randint(WINDOW_HEIGHT - 200, WINDOW_HEIGHT - 100),
                'size': random.randint(30, 50),
                'direction': random.choice([-1, 1]),
                'speed': random.uniform(1, 2)
            }
            self.lambda_functions.append(lambda_func)
        
        self.initialized = True
    
    def update(self):
        """Update positions of animated elements."""
        if not self.initialized:
            self.initialize()
            
        # Update cloud positions
        for cloud in self.clouds:
            cloud['x'] += cloud['speed']
            if cloud['x'] > WINDOW_WIDTH + cloud['size']:
                cloud['x'] = -cloud['size']
                cloud['y'] = random.randint(50, 150)
        
        # Update star rotations
        for star in self.stars:
            star['angle'] += star['speed']
        
        # Update lambda positions
        for lambda_func in self.lambda_functions:
            lambda_func['x'] += lambda_func['speed'] * lambda_func['direction']
            if lambda_func['x'] > WINDOW_WIDTH - 50 or lambda_func['x'] < 50:
                lambda_func['direction'] *= -1
    
    def draw(self):
        """Draw all animated elements."""
        if not self.initialized:
            self.initialize()
            
        # Draw clouds
        for cloud in self.clouds:
            self._draw_cloud(cloud['x'], cloud['y'], cloud['size'])
        
        # Draw stars
        for star in self.stars:
            self._draw_star(star['x'], star['y'], star['size'], star['angle'])
        
        # Draw lambda symbols
        for lambda_func in self.lambda_functions:
            self._draw_lambda_symbol(lambda_func['x'], lambda_func['y'], lambda_func['size'])
    
    def _draw_cloud(self, x, y, size):
        """Draw a simple cloud shape."""
        # Main cloud body
        pygame.draw.circle(self.surface, WHITE, (int(x), int(y)), int(size))
        pygame.draw.circle(self.surface, WHITE, (int(x - size/2), int(y)), int(size*0.7))
        pygame.draw.circle(self.surface, WHITE, (int(x + size/2), int(y)), int(size*0.7))
        pygame.draw.circle(self.surface, WHITE, (int(x - size/4), int(y - size/3)), int(size*0.6))
        pygame.draw.circle(self.surface, WHITE, (int(x + size/4), int(y - size/3)), int(size*0.6))
        
        # AWS logo hint (simplified)
        pygame.draw.line(self.surface, ORANGE, (int(x - size/3), int(y + size/6)), 
                        (int(x + size/3), int(y + size/6)), 3)
    
    def _draw_star(self, x, y, size, angle):
        """Draw a star shape (representing S3)."""
        points = []
        for i in range(5):
            # Outer points
            outer_x = x + size * math.cos(angle + i * 2 * math.pi / 5)
            outer_y = y + size * math.sin(angle + i * 2 * math.pi / 5)
            points.append((outer_x, outer_y))
            
            # Inner points
            inner_x = x + size/2.5 * math.cos(angle + i * 2 * math.pi / 5 + math.pi/5)
            inner_y = y + size/2.5 * math.sin(angle + i * 2 * math.pi / 5 + math.pi/5)
            points.append((inner_x, inner_y))
        
        pygame.draw.polygon(self.surface, YELLOW, points)
        
        # S3 text
        try:
            s3_font = pygame.font.SysFont('Times New Roman', int(size/2))
            s3_text = s3_font.render("S3", True, BLACK)
            text_rect = s3_text.get_rect(center=(x, y))
            self.surface.blit(s3_text, text_rect)
        except:
            # Fallback if font fails
            pass
    
    def _draw_lambda_symbol(self, x, y, size):
        """Draw the AWS Lambda symbol (λ)."""
        lambda_color = (254, 153, 0)  # Lambda orange
        try:
            font = pygame.font.SysFont('Times New Roman', size)
            lambda_text = font.render("λ", True, lambda_color)
            text_rect = lambda_text.get_rect(center=(x, y))
            self.surface.blit(lambda_text, text_rect)
            
            # Small box around lambda
            box_rect = pygame.Rect(x - size/2, y - size/2, size, size)
            pygame.draw.rect(self.surface, lambda_color, box_rect, 2, 3)
        except:
            # Fallback if font fails
            pygame.draw.rect(self.surface, lambda_color, 
                            (x - size/2, y - size/2, size, size), 2, 3)
