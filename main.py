import pygame
import sys
import os
from settings import *
from game import Game, Horse

class GUI:
    def __init__(self):
        # Initialize Pygame
        pygame.init()
        pygame.font.init()

        # Setup Display
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chess Knight Project')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.assets = {}
        self._load_assets()

        self.game = Game()
        self.running = True

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

    def get_row_col_from_mouse(self, pos):
        x, y = pos
        if y < PANEL_HEIGHT:
            return None, None
        col = x // TILE_SIZE
        row = (y - PANEL_HEIGHT) // TILE_SIZE
        return row, col

    def draw_panel(self):
        # Draw panel background
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, SCREEN_WIDTH, PANEL_HEIGHT))
        
        # Draw Info
        turn_text = self.font.render(f"Turn: {self.game.turn.name}", True, COLOR_TEXT)
        self.screen.blit(turn_text, (20, 20))
        
        # Scores
        score_text = self.small_font.render(f"Scores - White (AI): {self.game.white_horse.score} | Black (Player): {self.game.black_horse.score}", True, COLOR_TEXT)
        self.screen.blit(score_text, (20, 60))
        
        info_text = self.small_font.render("White: AI (Random) | Black: Player", True, COLOR_TEXT)
        self.screen.blit(info_text, (20, 85))

    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.board[row][col]

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
                if (row, col) in self.game.get_valid_moves():
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

    def draw_game_over(self, winner):
        # Overlay
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Game Over Text
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)

        # Winner Text
        winner_name = "Draw"
        if winner == 'WH':
            winner_name = "White (AI)"
        elif winner == 'BH':
            winner_name = "Black (Player)"
            
        winner_text_str = f"Winner: {winner_name}"
        winner_text = self.font.render(winner_text_str, True, COLOR_TEXT)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(winner_text, winner_rect)

        # Score Text
        score_str = f"White: {self.game.white_horse.score} - Black: {self.game.black_horse.score}"
        score_text = self.small_font.render(score_str, True, COLOR_TEXT)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score_text, score_rect)

        # Restart Button
        button_rect = pygame.Rect(0, 0, 200, 50)
        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
        pygame.draw.rect(self.screen, (0, 255, 0), button_rect)
        
        restart_text = self.font.render("RESTART", True, (0, 0, 0))
        restart_rect = restart_text.get_rect(center=button_rect.center)
        self.screen.blit(restart_text, restart_rect)

        return button_rect

    def run(self):
        while self.running:
            self.clock.tick(FPS)
            
            game_over = self.game.game_over()
            winner = None


            if game_over:
                winner = self.game.check_winner()
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!Game Over! Winner: {winner}")
            else:
                # Check if current player has moves, if not, skip turn
                if not self.game.get_valid_moves():
                    print(f"No moves for {self.game.turn.name}, skipping turn...")
                    self.game.change_turn()
                    continue



            if self.game.turn == self.game.white_horse and not game_over:
                self.game.ai_move()



            # Event Handling
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if game_over:
                        button_rect = pygame.Rect(0, 0, 200, 50)
                        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
                        if button_rect.collidepoint(pos):
                            self.game = Game() # Restart game
                            game_over = False
                            winner = None
                    else:
                        # Game logic clicks
                        if self.game.turn == self.game.black_horse:
                             row, col = self.get_row_col_from_mouse(pos)
                             if row is not None and col is not None:
                                 self.game.move(end=(row, col))


            
            # Drawing
            self.draw_panel()
            self.draw_board()

            if game_over:
                print(f"!!!!!!!!!!!!!!!!!!!!!!!!!!dibujando game over")
                self.draw_game_over(winner)

            pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
