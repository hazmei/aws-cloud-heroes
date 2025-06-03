"""
Game logic for AWS Cloud Heroes.
Contains the main game mechanics and state management.
"""

import pygame
import random
import sys
from pygame.locals import *
from config import *
from ui import Button, TextRenderer
from animations import AnimationManager

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

class Game:
    """Main game class that manages the game loop and states."""
    
    def __init__(self):
        """Initialize the game."""
        # Initialize pygame
        pygame.init()
        
        try:
            # Set up the window
            self.window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
            pygame.display.set_caption('AWS Cloud Heroes')
            
            # Initialize fonts
            self._init_fonts()
            
            # Create overlay surface for effects
            self.overlay = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT), pygame.SRCALPHA)
            
            # Initialize game state
            self.game_state = GameState()
            
            # Pre-compute all descriptions for efficiency
            self.all_descriptions = [service["description"] for service in AWS_SERVICES]
            
            # Initialize animation manager
            self.animation_manager = AnimationManager(self.window)
            
            # Initialize UI elements
            self._init_ui()
            
        except Exception as e:
            print(f"Error initializing game: {e}")
            pygame.quit()
            sys.exit(1)
    
    def _init_fonts(self):
        """Initialize game fonts with fallbacks."""
        try:
            self.title_font = pygame.font.SysFont('Times New Roman', TITLE_FONT_SIZE)
            self.game_font = pygame.font.SysFont('Times New Roman', GAME_FONT_SIZE)
            self.button_font = pygame.font.SysFont('Times New Roman', BUTTON_FONT_SIZE)
            self.feedback_font = pygame.font.SysFont('Times New Roman', FEEDBACK_FONT_SIZE)
        except:
            # Fallback to default font if custom font not available
            self.title_font = pygame.font.Font(None, TITLE_FONT_SIZE)
            self.game_font = pygame.font.Font(None, GAME_FONT_SIZE)
            self.button_font = pygame.font.Font(None, BUTTON_FONT_SIZE)
            self.feedback_font = pygame.font.Font(None, FEEDBACK_FONT_SIZE)
    
    def _init_ui(self):
        """Initialize UI elements."""
        # Create buttons
        center_x = WINDOW_WIDTH / 2
        
        self.start_button = Button(
            center_x, 375, 200, 50, ORANGE, "Start Game", WHITE, 
            self.button_font, (255, 140, 0), 3
        )
        self.start_button.pulsing = True
        
        self.play_again_button = Button(
            center_x, 325, 200, 50, ORANGE, "Play Again", WHITE,
            self.button_font, (255, 140, 0), 3
        )
        
        self.menu_button = Button(
            center_x, 395, 200, 50, ORANGE, "Main Menu", WHITE,
            self.button_font, (255, 140, 0), 3
        )
    
    def run(self):
        """Run the main game loop."""
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                
                if event.type == MOUSEBUTTONDOWN:
                    self._handle_mouse_click(event.pos)
            
            # Update animations if in menu state
            if self.game_state.state == MENU:
                self.animation_manager.update()
            
            # Draw the current game state
            self._draw_current_state()
            
            # Update the display
            pygame.display.update()
            clock.tick(FPS)
        
        pygame.quit()
        sys.exit()
    
    def _handle_mouse_click(self, pos):
        """Handle mouse clicks based on current game state."""
        if self.game_state.state == MENU:
            if self.start_button.is_clicked(pos):
                self._start_game()
        
        elif self.game_state.state == PLAYING:
            self._handle_playing_click(pos)
        
        elif self.game_state.state == GAME_OVER:
            if self.play_again_button.is_clicked(pos):
                self._start_game()
            elif self.menu_button.is_clicked(pos):
                self.game_state.state = MENU
    
    def _handle_playing_click(self, pos):
        """Handle mouse clicks during gameplay."""
        # Check if an option was clicked
        for i in range(len(self.game_state.options)):
            y_pos = 250 + i * OPTION_VERTICAL_SPACING
            option_box = pygame.Rect(
                WINDOW_WIDTH/2 - OPTION_BOX_WIDTH/2, 
                y_pos, 
                OPTION_BOX_WIDTH, 
                OPTION_BOX_HEIGHT
            )
            
            if option_box.collidepoint(pos):
                self.game_state.selected_option = i
                is_correct = (i == self.game_state.correct_option)
                
                if is_correct:
                    self.game_state.score += 10
                
                self._show_feedback(is_correct)
    
    def _draw_current_state(self):
        """Draw the current game state."""
        if self.game_state.state == MENU:
            self._draw_menu()
        elif self.game_state.state == PLAYING:
            self._draw_game()
            # Check if time's up
            elapsed_time = (pygame.time.get_ticks() - self.game_state.start_time - 
                           self.game_state.total_pause_time) // 1000
            if elapsed_time >= GAME_DURATION:
                self.game_state.state = GAME_OVER
        elif self.game_state.state == FEEDBACK:
            self._draw_game()  # Draw the game screen with selected option highlighted
            self._draw_feedback()  # Draw the feedback on top
        elif self.game_state.state == GAME_OVER:
            self._draw_game_over()
    
    def _draw_menu(self):
        """Draw the main menu screen."""
        self.window.fill(LIGHT_BLUE)  # Lighter blue for sky background
        
        # Draw animated AWS-themed elements
        self.animation_manager.draw()
        
        # Title with shadow effect
        TextRenderer.render_text(
            self.window, 
            "AWS Cloud Heroes", 
            self.title_font, 
            ORANGE, 
            (WINDOW_WIDTH/2, 100),
            shadow=True
        )
        
        # Description
        TextRenderer.render_text(
            self.window,
            "Learn about AWS cloud services!",
            self.game_font,
            BLACK,
            (WINDOW_WIDTH/2, 200)
        )
        
        TextRenderer.render_text(
            self.window,
            "Match the service with what it does.",
            self.game_font,
            BLACK,
            (WINDOW_WIDTH/2, 240)
        )
        
        # Draw start button
        self.start_button.draw(self.window)
    
    def _draw_game(self):
        """Draw the main gameplay screen."""
        self.window.fill(BLUE)
        
        # Draw time and score
        elapsed_time = (pygame.time.get_ticks() - self.game_state.start_time - 
                       self.game_state.total_pause_time) // 1000
        time_remaining = max(0, GAME_DURATION - elapsed_time)
        
        TextRenderer.render_text(
            self.window,
            f"Time: {time_remaining}s",
            self.game_font,
            BLACK,
            (20, 20),
            center=False
        )
        
        # Draw score more prominently
        score_box = pygame.Rect(WINDOW_WIDTH - 200, 10, 180, 40)
        pygame.draw.rect(self.window, WHITE, score_box, 0, 10)
        
        TextRenderer.render_text(
            self.window,
            f"Score: {self.game_state.score}",
            self.game_font,
            BLACK,
            score_box.center
        )
        
        # Draw the service name
        self._draw_service_box()
        
        # Draw the options
        self._draw_options()
    
    def _draw_service_box(self):
        """Draw the service box with the current service name."""
        service_box = pygame.Rect(
            WINDOW_WIDTH/2 - SERVICE_BOX_WIDTH/2, 
            100, 
            SERVICE_BOX_WIDTH, 
            SERVICE_BOX_HEIGHT
        )
        
        # Draw a thicker border for the service box
        border_box = pygame.Rect(
            WINDOW_WIDTH/2 - SERVICE_BOX_WIDTH/2 - 5, 
            95, 
            SERVICE_BOX_WIDTH + 10, 
            SERVICE_BOX_HEIGHT + 10
        )
        pygame.draw.rect(self.window, BLACK, border_box, 0, 12)
        pygame.draw.rect(self.window, self.game_state.current_service["color"], service_box, 0, 10)
        
        TextRenderer.render_text(
            self.window,
            self.game_state.current_service["name"],
            self.title_font,
            WHITE,
            service_box.center
        )
    
    def _draw_options(self):
        """Draw the answer options."""
        for i, option in enumerate(self.game_state.options):
            y_pos = 250 + i * OPTION_VERTICAL_SPACING
            option_box = pygame.Rect(
                WINDOW_WIDTH/2 - OPTION_BOX_WIDTH/2, 
                y_pos, 
                OPTION_BOX_WIDTH, 
                OPTION_BOX_HEIGHT
            )
            
            # Highlight selected option
            if i == self.game_state.selected_option:
                if i == self.game_state.correct_option:
                    box_color = GREEN  # Correct answer
                else:
                    box_color = RED    # Wrong answer
            else:
                box_color = WHITE      # Unselected
                
            pygame.draw.rect(self.window, box_color, option_box, 0, 10)
            
            TextRenderer.render_text(
                self.window,
                option,
                self.game_font,
                BLACK,
                option_box.center
            )
    
    def _draw_feedback(self):
        """Draw feedback overlay after an answer is selected."""
        # Create a semi-transparent black overlay
        self.overlay.fill((0, 0, 0, 180))  # Black with 70% opacity
        self.window.blit(self.overlay, (0, 0))
        
        # Create a feedback box
        feedback_box = pygame.Rect(WINDOW_WIDTH/2 - 200, WINDOW_HEIGHT/2 - 100, 400, 200)
        pygame.draw.rect(self.window, DARK_GRAY, feedback_box, 0, 15)  # Dark gray box with rounded corners
        pygame.draw.rect(self.window, self.game_state.feedback_color, feedback_box, 4, 15)  # Colored border
        
        # Draw the feedback message
        TextRenderer.render_text(
            self.window,
            self.game_state.feedback_message,
            self.feedback_font,
            self.game_state.feedback_color,
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 - 40)
        )
        
        # Draw current score
        TextRenderer.render_text(
            self.window,
            f"Score: {self.game_state.score}",
            self.feedback_font,
            WHITE,
            (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 + 20)
        )
        
        # Check if feedback time is over
        current_time = pygame.time.get_ticks()
        if current_time - self.game_state.feedback_start_time >= FEEDBACK_DURATION:
            # Add the pause duration to total_pause_time before moving on
            self.game_state.total_pause_time += (current_time - self.game_state.pause_time)
            self._new_question()
            self.game_state.state = PLAYING
    
    def _draw_game_over(self):
        """Draw the game over screen."""
        self.window.fill(BLUE)
        
        # Game over text
        TextRenderer.render_text(
            self.window,
            "Game Over!",
            self.title_font,
            ORANGE,
            (WINDOW_WIDTH/2, 100),
            shadow=True
        )
        
        # Final score
        TextRenderer.render_text(
            self.window,
            f"Your Score: {self.game_state.score}",
            self.game_font,
            BLACK,
            (WINDOW_WIDTH/2, 200)
        )
        
        # Draw buttons
        self.play_again_button.draw(self.window)
        self.menu_button.draw(self.window)
    
    def _start_game(self):
        """Initialize a new game."""
        self.game_state.state = PLAYING
        self.game_state.score = 0
        self.game_state.start_time = pygame.time.get_ticks()
        self.game_state.total_pause_time = 0
        self._new_question()
    
    def _reset_game_state(self):
        """Reset the game state for a new question."""
        self.game_state.selected_option = -1
    
    def _select_random_service(self):
        """Select a random AWS service to quiz the player on."""
        return random.choice(AWS_SERVICES)
    
    def _generate_answer_options(self, correct_description):
        """Generate a list of answer options (one correct, three wrong)."""
        # Remove the correct answer from potential wrong answers
        wrong_descriptions = [desc for desc in self.all_descriptions if desc != correct_description]
        
        # Select 3 random wrong descriptions
        selected_wrong = random.sample(wrong_descriptions, min(3, len(wrong_descriptions)))
        
        # Combine with correct and shuffle
        options = [correct_description] + selected_wrong
        random.shuffle(options)
        
        return options
    
    def _find_correct_option_index(self, options, correct_description):
        """Find the index of the correct option in the options list."""
        return options.index(correct_description)
    
    def _new_question(self):
        """Set up a new question for the player."""
        # Reset game state
        self._reset_game_state()
        
        # Select a random service
        self.game_state.current_service = self._select_random_service()
        correct_description = self.game_state.current_service["description"]
        
        # Generate answer options
        self.game_state.options = self._generate_answer_options(correct_description)
        
        # Track the correct option
        self.game_state.correct_option = self._find_correct_option_index(
            self.game_state.options, correct_description
        )
    
    def _show_feedback(self, is_correct):
        """Show feedback after an answer is selected."""
        if is_correct:
            self.game_state.feedback_message = "CORRECT!"
            self.game_state.feedback_color = GREEN
        else:
            self.game_state.feedback_message = "WRONG!"
            self.game_state.feedback_color = RED
        
        self.game_state.state = FEEDBACK
        self.game_state.feedback_start_time = pygame.time.get_ticks()
        self.game_state.pause_time = pygame.time.get_ticks()  # Record when feedback started
