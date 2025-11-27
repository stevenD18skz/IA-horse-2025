import pygame
import sys
import os
from settings import *
from game import Game, Horse

class GUI:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.assets = {}
        self._load_assets()



    def _load_assets(self):
        # Paths
        base_path = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Load and scale images
        try:    
            self.assets['WH'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'horse_ia.png')), (TILE_SIZE, TILE_SIZE))
            self.assets['BH'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'horse_player.png')), (TILE_SIZE, TILE_SIZE))
            self.assets['destroy'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'destroy.png')), (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Fallback to None or handle gracefully
            pass



    def draw_panel(self, game):
        # Draw panel background
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, SCREEN_WIDTH, PANEL_HEIGHT))
        
        # Draw Info
        turn_text = self.font.render(f"Turn: {game.turn.name}", True, COLOR_TEXT)
        self.screen.blit(turn_text, (20, 20))
        
        # Scores
        score_text = self.small_font.render(f"Scores - White (AI): {game.white_horse.score} | Black (Player): {game.black_horse.score}", True, COLOR_TEXT)
        self.screen.blit(score_text, (20, 60))
        
        info_text = self.small_font.render("White: AI (Random) | Black: Player", True, COLOR_TEXT)
        self.screen.blit(info_text, (20, 85))



    def draw_board(self, game):
        for row in range(ROWS):
            for col in range(COLS):
                piece = game.board[row][col]

                # Determine color
                color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
                
                # Draw square (offset by PANEL_HEIGHT)
                rect = (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                

                # Draw Destroyed Tile
                if piece == -20:
                    if 'destroy' in self.assets:
                        self.screen.blit(self.assets['destroy'], (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))
                    else:
                        # Fallback visual
                        pygame.draw.rect(self.screen, (50, 50, 50), rect)
                

                # Draw Highlight if valid move
                if (row, col) in game.get_valid_moves():
                    # Create a surface for transparency
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    s.set_alpha(128)
                    s.fill(COLOR_HIGHLIGHT)
                    self.screen.blit(s, (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))



                if piece not in [-20, 'HW', 'HB', 0]:
                    # Render the integer as text
                    piece_text = self.small_font.render(str(piece), True, (0, 0, 0))
                    text_rect = piece_text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2,
                                                                row * TILE_SIZE + PANEL_HEIGHT + TILE_SIZE // 2))
                    self.screen.blit(piece_text, text_rect)
                    


                # Draw Piece 
                if piece in ['WH', 'BH']:
                    if piece in self.assets:
                        self.screen.blit(self.assets[piece], (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))
                    else:
                        # Fallback text
                        text_color = (0, 0, 0) if piece == 'WH' else (50, 50, 50)
                        piece_text = self.font.render(piece, True, text_color)
                        text_rect = piece_text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, 
                                                                row * TILE_SIZE + PANEL_HEIGHT + TILE_SIZE // 2))
                        self.screen.blit(piece_text, text_rect)
 


def get_row_col_from_mouse(pos):
    x, y = pos
    if y < PANEL_HEIGHT:
        return None, None
    col = x // TILE_SIZE
    row = (y - PANEL_HEIGHT) // TILE_SIZE
    return row, col



def main():
    # Initialize Pygame
    pygame.init()
    pygame.font.init()

    # Setup Display
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Chess Knight Project')
    clock = pygame.time.Clock()

    game = Game()
    gui = GUI(screen)
    
    running = True
    
    

    while running:
        clock.tick(FPS)

        # Verifica si el juego termino
        if game.game_over():
            game.check_winner()
            running = False

        # MUEVE LA IA
        if game.turn == game.white_horse:
            game.ai_move()

        # MUEVE EL JUGADOR
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                row, col = get_row_col_from_mouse(pygame.mouse.get_pos())
                print(f"Clicked at: {row}, {col}")

                if row is not None and col is not None:
                    game.move(end=(row, col))
           
           

        
        # Drawing
        gui.draw_panel(game)
        gui.draw_board(game)
        
        pygame.display.update()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
