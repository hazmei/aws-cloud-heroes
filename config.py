"""
Configuration file for AWS Cloud Heroes game.
Contains game settings and AWS service definitions.
"""

# Game settings
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
FPS = 60
GAME_DURATION = 30  # seconds
FEEDBACK_DURATION = 1500  # milliseconds

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

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
FEEDBACK = 3

# AWS Services for kids (simplified)
AWS_SERVICES = [
    {"name": "S3", "description": "Stores your pictures and videos", "color": (244, 153, 66)},
    {"name": "EC2", "description": "Runs your computer games", "color": (237, 130, 14)},
    {"name": "Lambda", "description": "Does magic when you click buttons", "color": (254, 153, 0)},
    {"name": "DynamoDB", "description": "Remembers your high scores", "color": (79, 104, 189)},
    {"name": "CloudWatch", "description": "Watches over your games", "color": (66, 133, 244)},
    {"name": "IAM", "description": "Keeps your games safe", "color": (214, 91, 48)}
]

# Font settings
TITLE_FONT_SIZE = 48
GAME_FONT_SIZE = 24
BUTTON_FONT_SIZE = 20
FEEDBACK_FONT_SIZE = 32

# UI settings
BUTTON_PADDING = 10
SERVICE_BOX_WIDTH = 300
SERVICE_BOX_HEIGHT = 100
OPTION_BOX_WIDTH = 600
OPTION_BOX_HEIGHT = 60
OPTION_VERTICAL_SPACING = 80
