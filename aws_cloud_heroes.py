"""
AWS Cloud Heroes - An educational game for children to learn about AWS services.

This game introduces basic AWS services to children under 10 years old through
a fun matching game where they connect service names with their functions.

Run this file to start the game.
"""

from game import Game

if __name__ == "__main__":
    try:
        game = Game()
        game.run()
    except Exception as e:
        print(f"Error running game: {e}")
