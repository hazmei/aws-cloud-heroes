import pygame
import sys
import random
from pygame.locals import *

# Initialize pygame
pygame.init()

# Set up the window
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption('AWS Cloud Heroes')

# Colors
WHITE = (255, 255, 255)
BLUE = (135, 206, 250)
ORANGE = (255, 165, 0)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Fonts
title_font = pygame.font.SysFont('comicsansms', 48)
game_font = pygame.font.SysFont('comicsansms', 24)
button_font = pygame.font.SysFont('comicsansms', 20)
feedback_font = pygame.font.SysFont('comicsansms', 32)

# AWS Services for kids (simplified)
aws_services = [
    {"name": "S3", "description": "Stores your pictures and videos", "color": (244, 153, 66)},
    {"name": "EC2", "description": "Runs your computer games", "color": (237, 130, 14)},
    {"name": "Lambda", "description": "Does magic when you click buttons", "color": (254, 153, 0)},
    {"name": "DynamoDB", "description": "Remembers your high scores", "color": (79, 104, 189)},
    {"name": "CloudWatch", "description": "Watches over your games", "color": (66, 133, 244)},
    {"name": "IAM", "description": "Keeps your games safe", "color": (214, 91, 48)}
]

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
FEEDBACK = 3
game_state = MENU

# Game variables
score = 0
current_service = None
options = []
correct_option = None
time_left = 30
start_time = 0
feedback_message = ""
feedback_color = BLACK
feedback_start_time = 0
selected_option = -1
pause_time = 0
total_pause_time = 0

def draw_menu():
    window.fill(BLUE)
    
    # Title
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
    
    # Start button
    pygame.draw.rect(window, ORANGE, (WINDOW_WIDTH/2 - 100, 350, 200, 50), 0, 10)
    start_text = button_font.render("Start Game", True, WHITE)
    start_text_rect = start_text.get_rect(center=(WINDOW_WIDTH/2, 375))
    window.blit(start_text, start_text_rect)

def start_game():
    global game_state, score, start_time, total_pause_time
    game_state = PLAYING
    score = 0
    start_time = pygame.time.get_ticks()
    total_pause_time = 0
    new_question()

def new_question():
    global current_service, options, correct_option, selected_option
    
    # Reset selected option
    selected_option = -1
    
    # Select a random service
    current_service = random.choice(aws_services)
    
    # Create options (one correct, three wrong)
    all_descriptions = [service["description"] for service in aws_services]
    correct_description = current_service["description"]
    
    # Remove the correct answer from potential wrong answers
    wrong_descriptions = [desc for desc in all_descriptions if desc != correct_description]
    
    # Select 3 random wrong descriptions
    selected_wrong = random.sample(wrong_descriptions, min(3, len(wrong_descriptions)))
    
    # Combine with correct and shuffle
    options = [correct_description] + selected_wrong
    random.shuffle(options)
    
    # Track the correct option
    correct_option = options.index(correct_description)

def show_feedback(is_correct):
    global game_state, feedback_message, feedback_color, feedback_start_time, pause_time
    
    if is_correct:
        feedback_message = "CORRECT!"
        feedback_color = GREEN
    else:
        feedback_message = "WRONG!"
        feedback_color = RED
    
    game_state = FEEDBACK
    feedback_start_time = pygame.time.get_ticks()
    pause_time = pygame.time.get_ticks()  # Record when feedback started

def draw_game():
    window.fill(BLUE)
    
    # Draw time and score
    elapsed_time = (pygame.time.get_ticks() - start_time - total_pause_time) // 1000
    time_remaining = max(0, 30 - elapsed_time)
    
    time_text = game_font.render(f"Time: {time_remaining}s", True, BLACK)
    window.blit(time_text, (20, 20))
    
    # Draw score more prominently
    score_box = pygame.Rect(WINDOW_WIDTH - 200, 10, 180, 40)
    pygame.draw.rect(window, WHITE, score_box, 0, 10)
    score_text = game_font.render(f"Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=score_box.center)
    window.blit(score_text, score_rect)
    
    # Draw the service name
    service_box = pygame.Rect(WINDOW_WIDTH/2 - 100, 100, 200, 100)
    pygame.draw.rect(window, current_service["color"], service_box, 0, 10)
    
    service_text = title_font.render(current_service["name"], True, WHITE)
    service_text_rect = service_text.get_rect(center=service_box.center)
    window.blit(service_text, service_text_rect)
    
    # Draw the options
    for i, option in enumerate(options):
        y_pos = 250 + i * 80
        option_box = pygame.Rect(WINDOW_WIDTH/2 - 300, y_pos, 600, 60)
        
        # Highlight selected option
        if i == selected_option:
            if i == correct_option:
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
        game_state = GAME_OVER

def draw_feedback():
    global game_state, total_pause_time
    
    # Create a semi-transparent black overlay
    overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
    window.blit(overlay, (0, 0))
    
    # Create a feedback box
    feedback_box = pygame.Rect(WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 - 100, 400, 200)
    pygame.draw.rect(window, (50, 50, 50), feedback_box, 0, 15)  # Dark gray box with rounded corners
    pygame.draw.rect(window, feedback_color, feedback_box, 4, 15)  # Colored border
    
    # Draw the feedback message
    feedback_text = feedback_font.render(feedback_message, True, feedback_color)
    feedback_rect = feedback_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40))
    window.blit(feedback_text, feedback_rect)
    
    # Draw current score
    score_text = feedback_font.render(f"Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20))
    window.blit(score_text, score_rect)
    
    # Check if feedback time is over (1.5 seconds)
    current_time = pygame.time.get_ticks()
    if current_time - feedback_start_time >= 1500:
        # Add the pause duration to total_pause_time before moving on
        total_pause_time += (current_time - pause_time)
        new_question()
        game_state = PLAYING

def draw_game_over():
    window.fill(BLUE)
    
    # Game over text
    game_over_text = title_font.render("Game Over!", True, ORANGE)
    game_over_rect = game_over_text.get_rect(center=(WINDOW_WIDTH/2, 100))
    window.blit(game_over_text, game_over_rect)
    
    # Final score
    score_text = game_font.render(f"Your Score: {score}", True, BLACK)
    score_rect = score_text.get_rect(center=(WINDOW_WIDTH/2, 200))
    window.blit(score_text, score_rect)
    
    # Play again button
    pygame.draw.rect(window, ORANGE, (WINDOW_WIDTH/2 - 100, 300, 200, 50), 0, 10)
    play_again_text = button_font.render("Play Again", True, WHITE)
    play_again_rect = play_again_text.get_rect(center=(WINDOW_WIDTH/2, 325))
    window.blit(play_again_text, play_again_rect)
    
    # Menu button
    pygame.draw.rect(window, ORANGE, (WINDOW_WIDTH/2 - 100, 370, 200, 50), 0, 10)
    menu_text = button_font.render("Main Menu", True, WHITE)
    menu_rect = menu_text.get_rect(center=(WINDOW_WIDTH/2, 395))
    window.blit(menu_text, menu_rect)

# Main game loop
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        
        if event.type == MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            
            if game_state == MENU:
                # Check if start button clicked
                if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and 350 <= mouse_pos[1] <= 400:
                    start_game()
            
            elif game_state == PLAYING:
                # Check if an option was clicked
                for i in range(len(options)):
                    y_pos = 250 + i * 80
                    option_box = pygame.Rect(WINDOW_WIDTH/2 - 300, y_pos, 600, 60)
                    
                    if option_box.collidepoint(mouse_pos):
                        selected_option = i
                        is_correct = (i == correct_option)
                        
                        if is_correct:
                            score += 10
                        
                        show_feedback(is_correct)
            
            elif game_state == GAME_OVER:
                # Check if play again button clicked
                if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and 300 <= mouse_pos[1] <= 350:
                    start_game()
                
                # Check if menu button clicked
                if WINDOW_WIDTH/2 - 100 <= mouse_pos[0] <= WINDOW_WIDTH/2 + 100 and 370 <= mouse_pos[1] <= 420:
                    game_state = MENU
    
    # Draw the current game state
    if game_state == MENU:
        draw_menu()
    elif game_state == PLAYING:
        draw_game()
        # Check if time's up
        elapsed_time = (pygame.time.get_ticks() - start_time - total_pause_time) // 1000
        if elapsed_time >= 30:
            game_state = GAME_OVER
    elif game_state == FEEDBACK:
        draw_game()  # Draw the game screen with selected option highlighted
        draw_feedback()  # Draw the feedback on top
    elif game_state == GAME_OVER:
        draw_game_over()
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()
sys.exit()
