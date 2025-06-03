"""
AWS Cloud Heroes - An educational game for children to learn about AWS services.

This game introduces basic AWS services to children under 10 years old through
a fun matching game where they connect service names with their functions.
"""

import pygame
import sys
import random
import math
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GAME_DURATION = 30  # seconds

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
FEEDBACK = 3

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
LIGHT_BLUE = (173, 216, 230)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GRAY = (50, 50, 50)
YELLOW = (255, 255, 0)

# Set up the window
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AWS Cloud Heroes')

# Fonts
try:
    title_font = pygame.font.SysFont('Times New Roman', 48)
    game_font = pygame.font.SysFont('Times New Roman', 24)
    button_font = pygame.font.SysFont('Times New Roman', 20)
    feedback_font = pygame.font.SysFont('Times New Roman', 32)
except:
    # Fallback to default font if custom font not available
    title_font = pygame.font.Font(None, 48)
    game_font = pygame.font.Font(None, 24)
    button_font = pygame.font.Font(None, 20)
    feedback_font = pygame.font.Font(None, 32)

# AWS Services for kids (simplified)
aws_services = [
    {"name": "S3", "description": "Stores your pictures and videos", "color": (244, 153, 66)},
    {"name": "EC2", "description": "Runs your computer games", "color": (237, 130, 14)},
    {"name": "Lambda", "description": "Does magic when you click buttons", "color": (254, 153, 0)},
    {"name": "DynamoDB", "description": "Remembers your high scores", "color": (79, 104, 189)},
    {"name": "CloudWatch", "description": "Watches over your games", "color": (66, 133, 244)},
    {"name": "IAM", "description": "Keeps your games safe", "color": (214, 91, 48)}
]

# Pre-compute all descriptions for efficiency
all_descriptions = [service["description"] for service in aws_services]

# Create overlay surface once for efficiency
overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)

# Animation variables
clouds = []
stars = []
lambda_functions = []

def init_animations():
    """Initialize animation elements for the menu screen."""
    global clouds, stars, lambda_functions
    
    # Create clouds (representing AWS cloud)
    clouds = []
    for i in range(5):
        cloud = {
            'x': random.randint(0, WINDOW_WIDTH),
            'y': random.randint(50, 150),
            'size': random.randint(60, 100),
            'speed': random.uniform(0.5, 1.5)
        }
        clouds.append(cloud)
    
    # Create stars (representing S3)
    stars = []
    for i in range(8):
        star = {
            'x': random.randint(0, WINDOW_WIDTH),
            'y': random.randint(50, WINDOW_HEIGHT - 100),
            'size': random.randint(15, 30),
            'angle': 0,
            'speed': random.uniform(0.02, 0.05)
        }
        stars.append(star)
    
    # Create lambda functions (representing AWS Lambda)
    lambda_functions = []
    for i in range(3):
        lambda_func = {
            'x': random.randint(50, WINDOW_WIDTH - 50),
            'y': random.randint(WINDOW_HEIGHT - 200, WINDOW_HEIGHT - 100),
            'size': random.randint(30, 50),
            'direction': random.choice([-1, 1]),
            'speed': random.uniform(1, 2)
        }
        lambda_functions.append(lambda_func)

def draw_cloud(x, y, size):
    """Draw a simple cloud shape."""
    # Main cloud body
    pygame.draw.circle(window, WHITE, (int(x), int(y)), int(size))
    pygame.draw.circle(window, WHITE, (int(x - size/2), int(y)), int(size*0.7))
    pygame.draw.circle(window, WHITE, (int(x + size/2), int(y)), int(size*0.7))
    pygame.draw.circle(window, WHITE, (int(x - size/4), int(y - size/3)), int(size*0.6))
    pygame.draw.circle(window, WHITE, (int(x + size/4), int(y - size/3)), int(size*0.6))
    
    # AWS logo hint (simplified)
    pygame.draw.line(window, ORANGE, (int(x - size/3), int(y + size/6)), 
                    (int(x + size/3), int(y + size/6)), 3)

def draw_star(x, y, size, angle):
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
    
    pygame.draw.polygon(window, YELLOW, points)
    # S3 text
    s3_text = pygame.font.SysFont('Times New Roman', int(size/2)).render("S3", True, BLACK)
    text_rect = s3_text.get_rect(center=(x, y))
    window.blit(s3_text, text_rect)

def draw_lambda_symbol(x, y, size):
    """Draw the AWS Lambda symbol (λ)."""
    lambda_color = (254, 153, 0)  # Lambda orange
    font = pygame.font.SysFont('Times New Roman', size)
    lambda_text = font.render("λ", True, lambda_color)
    text_rect = lambda_text.get_rect(center=(x, y))
    window.blit(lambda_text, text_rect)
    
    # Small box around lambda
    box_rect = pygame.Rect(x - size/2, y - size/2, size, size)
    pygame.draw.rect(window, lambda_color, box_rect, 2, 3)

def update_animations():
    """Update positions of animated elements."""
    # Update cloud positions
    for cloud in clouds:
        cloud['x'] += cloud['speed']
        if cloud['x'] > WINDOW_WIDTH + cloud['size']:
            cloud['x'] = -cloud['size']
            cloud['y'] = random.randint(50, 150)
    
    # Update star rotations
    for star in stars:
        star['angle'] += star['speed']
    
    # Update lambda positions
    for lambda_func in lambda_functions:
        lambda_func['x'] += lambda_func['speed'] * lambda_func['direction']
        if lambda_func['x'] > WINDOW_WIDTH - 50 or lambda_func['x'] < 50:
            lambda_func['direction'] *= -1

def draw_animations():
    """Draw all animated elements."""
    # Draw clouds
    for cloud in clouds:
        draw_cloud(cloud['x'], cloud['y'], cloud['size'])
    
    # Draw stars
    for star in stars:
        draw_star(star['x'], star['y'], star['size'], star['angle'])
    
    # Draw lambda symbols
    for lambda_func in lambda_functions:
        draw_lambda_symbol(lambda_func['x'], lambda_func['y'], lambda_func['size'])

class GameState:
    """Class to manage game state and variables."""
    
    def __init__(self):
        self.state = MENU
        self.score = 0
        self.current_service = None
        self.options = []
        self.correct_option = None
        self.start_time = 0
        self.feedback_message = ""
        self.feedback_color = BLACK
        self.feedback_start_time = 0
        self.selected_option = -1
        self.pause_time = 0
        self.total_pause_time = 0

# Initialize game state
game = GameState()

def draw_menu():
    """Draw the main menu screen."""
    window.fill(LIGHT_BLUE)  # Lighter blue for sky background
    
    # Draw animated AWS-themed elements
    draw_animations()
    
    # Title with shadow effect for better visibility
    title_shadow = title_font.render("AWS Cloud Heroes", True, BLACK)
    title_shadow_rect = title_shadow.get_rect(center=(WINDOW_WIDTH/2 + 3, 103))
    window.blit(title_shadow, title_shadow_rect)
    
    title = title_font.render("AWS Cloud Heroes", True, ORANGE)
    title_rect = title.get_rect(center=(WINDOW_WIDTH/2, 100))
    window.blit(title, title_rect)
    
    # Description
    desc1 = game_font.render("Learn about AWS cloud services!", True, BLACK)
    desc1_rect = desc1.get_rect(center=(WINDOW_WIDTH/2, 200))
    window.blit(desc1, desc1_rect)
    
    desc2 = game_font.render("Match the service with what it does.", True, BLACK)
    desc2_rect = desc2.get_rect(center=(WINDOW_WIDTH/2, 240))
    window.blit(desc2, desc2_rect)
    
    # Start button with pulsing effect
    button_size = 1.0 + 0.05 * math.sin(pygame.time.get_ticks() / 200)
    button_width = 200 * button_size
    button_height = 50 * button_size
    
    pygame.draw.rect(window, ORANGE, 
                    (WINDOW_WIDTH/2 - button_width/2, 350, button_width, button_height), 0, 10)
    pygame.draw.rect(window, (255, 140, 0),  # Darker orange border
                    (WINDOW_WIDTH/2 - button_width/2, 350, button_width, button_height), 3, 10)
    
    start_text = button_font.render("Start Game", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH/2, 375))
    window.blit(start_text, start_text_rect)

def draw_button(x, y, width, height, color, text, text_color):
    """Draw a button with text."""
    pygame.draw.rect(window, color, (x, y, width, height), 0, 10)
    text_surf = button_font.render(text, True, text_color)
    text_rect = text_surf.get_rect(center=(x + width/2, y + height/2))
    window.blit(text_surf, text_rect)

def start_game():
    """Initialize a new game."""
    game.state = PLAYING
    game.score = 0
    game.start_time = pygame.time.get_ticks()
    game.total_pause_time = 0
    new_question()

def reset_game_state():
    """Reset the game state for a new question."""
    game.selected_option = -1

def select_random_service():
    """Select a random AWS service to quiz the player on."""
    return random.choice(aws_services)

def generate_answer_options(correct_description):
    """Generate a list of answer options (one correct, three wrong)."""
    # Remove the correct answer from potential wrong answers
    wrong_descriptions = [desc for desc in all_descriptions if desc != correct_description]
    
    # Select 3 random wrong descriptions
    selected_wrong = random.sample(wrong_descriptions, min(3, len(wrong_descriptions)))
    
    # Combine with correct and shuffle
    options = [correct_description] + selected_wrong
    random.shuffle(options)
    
    return options

def find_correct_option_index(options, correct_description):
    """Find the index of the correct option in the options list."""
    return options.index(correct_description)

def new_question():
    """Set up a new question for the player."""
    # Reset game state
    reset_game_state()
    
    # Select a random service
    game.current_service = select_random_service()
    correct_description = game.current_service["description"]
    
    # Generate answer options
    game.options = generate_answer_options(correct_description)
    
    # Track the correct option
    game.correct_option = find_correct_option_index(game.options, correct_description)

def show_feedback(is_correct):
    """Show feedback after an answer is selected."""
    if is_correct:
        game.feedback_message = "CORRECT!"
        game.feedback_color = GREEN
    else:
        game.feedback_message = "WRONG!"
        game.feedback_color = RED
    
    game.state = FEEDBACK
    game.feedback_start_time = pygame.time.get_ticks()
    game.pause_time = pygame.time.get_ticks()  # Record when feedback started

def draw_game():
    """Draw the main gameplay screen."""
    window.fill(BLUE)
    
    # Draw time and score
    elapsed_time = (pygame.time.get_ticks() - game.start_time - game.total_pause_time) // 1000
    time_remaining = max(0, GAME_DURATION - elapsed_time)
    
    time_text = game_font.render(f"Time: {time_remaining}s", True, BLACK)
    window.blit(time_text, (20, 20))
    
    # Draw score more prominently
    score_box = pygame.Rect(WINDOW_WIDTH - 200, 10, 180, 40)
    pygame.draw.rect(window, WHITE, score_box, 0, 10)
    score_text = game_font.render(f"Score: {game.score}", True, BLACK)
    score_rect = score_text.get_rect(center=score_box.center)
    window.blit(score_text, score_rect)
    
    # Draw the service name
    service_box = pygame.Rect(WINDOW_WIDTH/2 - 150, 100, 300, 100)  # Wider box for longer service names
    
    # Draw a thicker border for the service box
    border_box = pygame.Rect(WINDOW_WIDTH/2 - 155, 95, 310, 110)
    pygame.draw.rect(window, BLACK, border_box, 0, 12)
    pygame.draw.rect(window, game.current_service["color"], service_box, 0, 10)
    
    service_text = title_font.render(game.current_service["name"], True, WHITE)
    service_text_rect = service_text.get_rect(center=service_box.center)
    window.blit(service_text, service_text_rect)
    
    # Draw the options
    for i, option in enumerate(game.options):
        y_pos = 250 + i * 80
        option_box = pygame.Rect(WINDOW_WIDTH/2 - 300, y_pos, 600, 60)
        
        # Highlight selected option
        if i == game.selected_option:
            if i == game.correct_option:
                box_color = GREEN  # Correct answer
            else:
                box_color = RED    # Wrong answer
        else:
            box_color = WHITE      # Unselected
            
        pygame.draw.rect(window, box_color, option_box, 0, 10)
        
        option_text = game_font.render(option, True, BLACK)
        option_text_rect = option_text.get_rect(center=option_box.center)
        window.blit(option_text, option_text_rect)
    
    # Check if time's up
    if time_remaining <= 0:
        game.state = GAME_OVER

def draw_feedback():
    """Draw feedback overlay after an answer is selected."""
    # Create a semi-transparent black overlay
    overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
    window.blit(overlay, (0, 0))
    
    # Create a feedback box
    feedback_box = pygame.Rect(WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 - 100, 400, 200)
    pygame.draw.rect(window, DARK_GRAY, feedback_box, 0, 15)  # Dark gray box with rounded corners
    pygame.draw.rect(window, game.feedback_color, feedback_box, 4, 15)  # Colored border
    
    # Draw the feedback message
    feedback_text = feedback_font.render(game.feedback_message, True, game.feedback_color)
    feedback_rect = feedback_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40))
    window.blit(feedback_text, feedback_rect)
    
    # Draw current score
    score_text = feedback_font.render(f"Score: {game.score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
    window.blit(score_text, score_rect)
    
    # Check if feedback time is over (1.5 seconds)
    current_time = pygame.time.get_ticks()
    if current_time - game.feedback_start_time >= 1500:
        # Add the pause duration to total_pause_time before moving on
        game.total_pause_time += (current_time - game.pause_time)
        new_question()
        game.state = PLAYING

def draw_game_over():
    """Draw the game over screen."""
    window.fill(BLUE)
    
    # Game over text
    game_over_text = title_font.render("Game Over!", True, ORANGE)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, 100))
    window.blit(game_over_text, game_over_rect)
    
    # Final score
    score_text = game_font.render(f"Your Score: {game.score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 200))
    window.blit(score_text, score_rect)
    
    # Play again button
    draw_button(WINDOW_WIDTH/2 - 100, 300, 200, 50, ORANGE, "Play Again", WHITE)
    
    # Menu button
    draw_button(WINDOW_WIDTH/2 - 100, 370, 200, 50, ORANGE, "Main Menu", WHITE)

def handle_menu_click(mouse_pos):
    """Handle mouse clicks on the menu screen."""
    # Calculate button dimensions (matching the pulsing effect in draw_menu)
    button_size = 1.0 + 0.05 * math.sin(pygame.time.get_ticks() / 200)
    button_width = 200 * button_size
    button_height = 50 * button_size
    
    # Check if start button clicked
    if (WINDOW_WIDTH/2 - button_width/2 <= mouse_pos[0] <= WINDOW_WIDTH/2 + button_width/2 and 
        350 <= mouse_pos[1] <= 350 + button_height):
        start_game()

def handle_playing_click(mouse_pos):
    """Handle mouse clicks during gameplay."""
    # Check if an option was clicked
    for i, _ in enumerate(game.options):
        y_pos = 250 + i * 80
        option_box = pygame.Rect(WINDOW_WIDTH/2 - 300, y_pos, 600, 60)
        
        if option_box.collidepoint(mouse_pos):
            game.selected_option = i
            is_correct = (i == game.correct_option)
            
            if is_correct:
                game.score += 10
            
            show_feedback(is_correct)

def handle_game_over_click(mouse_pos):
    """Handle mouse clicks on the game over screen."""
    # Check if play again button clicked
    if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and 300 <= mouse_pos[1] <= 350:
        start_game()
    
    # Check if menu button clicked
    if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and 370 <= mouse_pos[1] <= 420:
        game.state = MENU

def main():
    """Main game loop."""
    clock = pygame.time.Clock()
    running = True
    
    # Initialize animations for the menu screen
    init_animations()

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            
            if event.type == MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if game.state == MENU:
                    handle_menu_click(mouse_pos)
                elif game.state == PLAYING:
                    handle_playing_click(mouse_pos)
                elif game.state == GAME_OVER:
                    handle_game_over_click(mouse_pos)
        
        # Update animations
        if game.state == MENU:
            update_animations()
        
        # Draw the current game state
        if game.state == MENU:
            draw_menu()
        elif game.state == PLAYING:
            draw_game()
            # Check if time's up
            elapsed_time = (pygame.time.get_ticks() - game.start_time - game.total_pause_time) // 1000
            if elapsed_time >= GAME_DURATION:
                game.state = GAME_OVER
        elif game.state == FEEDBACK:
            draw_game()  # Draw the game screen with selected option highlighted
            draw_feedback()  # Draw the feedback on top
        elif game.state == GAME_OVER:
            draw_game_over()
        
        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
