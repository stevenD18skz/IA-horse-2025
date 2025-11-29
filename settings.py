import pygame

# Dimensiones de la Pantalla
TILE_SIZE = 64
ROWS = 8
COLS = 8
BOARD_WIDTH = TILE_SIZE * COLS
BOARD_HEIGHT = TILE_SIZE * ROWS
PANEL_HEIGHT = 150
SCREEN_WIDTH = BOARD_WIDTH
SCREEN_HEIGHT = BOARD_HEIGHT + PANEL_HEIGHT

# Colores (Paleta Seria de Ajedrez)
# Madera Clara / Beige
COLOR_BOARD_LIGHT = (240, 217, 181) 
# Madera Oscura / Marrón
COLOR_BOARD_DARK = (181, 136, 99)
# Color de resaltado para movimientos válidos (Verdoso para mejor visibilidad sobre marrón)
COLOR_HIGHLIGHT = (100, 255, 100)
# Fondo del panel (Gris Oscuro)
COLOR_PANEL = (50, 50, 50)
# Color del texto (Blanco)
COLOR_TEXT = (255, 255, 255)

# Tasa de fotogramas
FPS = 60
