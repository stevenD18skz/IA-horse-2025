import pygame

# Screen Dimensions
TILE_SIZE = 64
ROWS = 8
COLS = 8
BOARD_WIDTH = TILE_SIZE * COLS
BOARD_HEIGHT = TILE_SIZE * ROWS
PANEL_HEIGHT = 150
SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + PANEL_HEIGHT

# Colors (Serious Chess Palette)
# Light Wood / Beige
COLOR_BOARD_LIGHT = (240, 217, 181) 
# Dark Wood / Brown
COLOR_BOARD_DARK = (181, 136, 99)
# Highlight color for valid moves (Greenish for better visibility on brown)
COLOR_HIGHLIGHT = (100, 255, 100)
# Panel background (Dark Grey)
COLOR_PANEL = (50, 50, 50)
# Text color (White)
COLOR_TEXT = (255, 255, 255)

# Framerate
FPS = 60
