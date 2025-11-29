import pygame
import sys
import os
from settings import *
from game import Game, Horse

class GUI:
    def __init__(self):
        # Inicializar Pygame
        pygame.init()
        pygame.font.init()

        # Configurar Pantalla
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption('Chess Knight Project')
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont('Arial', 32, bold=True)
        self.small_font = pygame.font.SysFont('Arial', 20)
        self.assets = {}
        self._load_assets()

        self.game = None # El juego comienza después de la selección de dificultad
        self.difficulty = None
        self.state = 'START' # INICIO, JUGANDO, FIN_DEL_JUEGO
        self.running = True
        self.status_message = "Welcome! Select difficulty."
        self.ai_target_pos = None # Para resaltar el movimiento intencionado de la IA



    def draw_start_screen(self):
        self.screen.fill(COLOR_PANEL)
        
        title_text = self.font.render("Smart Horses", True, COLOR_TEXT)
        title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, 100))
        self.screen.blit(title_text, title_rect)
        
        subtitle_text = self.small_font.render("Select Difficulty", True, COLOR_TEXT)
        subtitle_rect = subtitle_text.get_rect(center=(SCREEN_WIDTH // 2, 160))
        self.screen.blit(subtitle_text, subtitle_rect)

        # Botones
        buttons = [
            ("Beginner (Depth 2)", 2, 200),
            ("Amateur (Depth 4)", 4, 280),
            ("Expert (Depth 6)", 6, 360)
        ]

        button_rects = []
        for text, diff, y in buttons:
            rect = pygame.Rect(0, 0, 300, 60)
            rect.center = (SCREEN_WIDTH // 2, y)
            pygame.draw.rect(self.screen, (200, 200, 200), rect)
            pygame.draw.rect(self.screen, (0, 0, 0), rect, 2)
            
            label = self.font.render(text, True, (0, 0, 0))
            label_rect = label.get_rect(center=rect.center)
            self.screen.blit(label, label_rect)
            
            button_rects.append((rect, diff))
            
        return button_rects



    def _load_assets(self):
        # Rutas
        base_path = os.path.join(os.path.dirname(__file__), 'assets')
        
        # Cargar y escalar imágenes
        try:    
            self.assets['WH'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'horse_ia.png')), (TILE_SIZE, TILE_SIZE))
            self.assets['BH'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'horse_player.png')), (TILE_SIZE, TILE_SIZE))
            self.assets['destroy'] = pygame.transform.scale(
                pygame.image.load(os.path.join(base_path, 'destroy.png')), (TILE_SIZE, TILE_SIZE))
        except Exception as e:
            print(f"Error loading assets: {e}")
            # Recurrir a None o manejar con gracia
            pass



    def get_row_col_from_mouse(self, pos):
        x, y = pos
        if y < PANEL_HEIGHT:
            return None, None
        col = x // TILE_SIZE
        row = (y - PANEL_HEIGHT) // TILE_SIZE
        return row, col

    def draw_panel(self):
        # Dibujar fondo del panel
        pygame.draw.rect(self.screen, COLOR_PANEL, (0, 0, SCREEN_WIDTH, PANEL_HEIGHT))
        
        # Dibujar Información
        try:
            turn_text = self.font.render(f"Turn: {self.game.turn.name}", True, COLOR_TEXT)
            self.screen.blit(turn_text, (20, 20))
        except AttributeError:
            turn_text = self.font.render("Turn: -", True, COLOR_TEXT)
            self.screen.blit(turn_text, (20, 20))
        
        # Puntajes
        try:
            score_text = self.small_font.render(f"Scores => White (AI): {self.game.white_horse.score}  VS  Black (Player): {self.game.black_horse.score}", True, COLOR_TEXT)
            self.screen.blit(score_text, (20, 60))
        except AttributeError:
            score_text = self.small_font.render("Scores => White (AI): -  VS  Black (Player): -", True, COLOR_TEXT)
            self.screen.blit(score_text, (20, 60))
        
        try:
            info_text = self.small_font.render(f"White: AI (Depth {self.game.difficulty}) | Black: Player", True, COLOR_TEXT)
            self.screen.blit(info_text, (20, 85))
        except AttributeError:
            info_text = self.small_font.render("White: AI (Depth -) | Black: Player", True, COLOR_TEXT)
            self.screen.blit(info_text, (20, 85))

        # Mensaje de Estado
        try:
            status_text = self.small_font.render(f"Status: {self.status_message}", True, (255, 50, 50))
            self.screen.blit(status_text, (20, 110))
        except AttributeError:
            status_text = self.small_font.render("Status: -", True, (255, 50, 50))
            self.screen.blit(status_text, (20, 110))



    def draw_board(self):
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.game.board[row][col]

                # Determinar color
                color = COLOR_BOARD_LIGHT if (row + col) % 2 == 0 else COLOR_BOARD_DARK
                
                # Dibujar casilla (desplazada por PANEL_HEIGHT)
                rect = (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, color, rect)
                
                # Dibujar Casilla Destruida
                if piece == -20:
                    if 'destroy' in self.assets:
                        self.screen.blit(self.assets['destroy'], (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))
                    else:
                        # Visual alternativo
                        pygame.draw.rect(self.screen, (50, 50, 50), rect)
                
                # Dibujar Resaltado si es movimiento válido
                if (row, col) in self.game.get_valid_moves():
                    # Crear una superficie para transparencia
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    s.set_alpha(128)
                    s.fill(COLOR_HIGHLIGHT)
                    self.screen.blit(s, (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))
                
                # Dibujar Resaltado de Objetivo de IA
                if self.ai_target_pos == (row, col):
                    s = pygame.Surface((TILE_SIZE, TILE_SIZE))
                    s.set_alpha(180)
                    s.fill((255, 0, 0)) # Resaltado rojo para intención de IA
                    self.screen.blit(s, (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))

                if piece not in [-20, 'WH', 'BH', 0]:
                    # Renderizar el entero como texto
                    piece_text = self.small_font.render(str(piece), True, (0, 0, 0))
                    text_rect = piece_text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2,
                                                                row * TILE_SIZE + PANEL_HEIGHT + TILE_SIZE // 2))
                    self.screen.blit(piece_text, text_rect)
                    
                # Dibujar Pieza
                if piece in ['WH', 'BH']:
                    if piece in self.assets:
                        self.screen.blit(self.assets[piece], (col * TILE_SIZE, row * TILE_SIZE + PANEL_HEIGHT))
                    else:
                        # Texto alternativo
                        text_color = (0, 0, 0) if piece == 'WH' else (50, 50, 50)
                        piece_text = self.font.render(piece, True, text_color)
                        text_rect = piece_text.get_rect(center=(col * TILE_SIZE + TILE_SIZE // 2, 
                                                                row * TILE_SIZE + PANEL_HEIGHT + TILE_SIZE // 2))
                        self.screen.blit(piece_text, text_rect)



    def draw_game_over(self, winner):
        # Superposición
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
        overlay.set_alpha(200)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 0))

        # Texto de Fin del Juego
        game_over_text = self.font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 100))
        self.screen.blit(game_over_text, text_rect)

        # Texto del Ganador
        winner_name = "Draw"
        if winner == 'WH':
            winner_name = "White (AI)"
        elif winner == 'BH':
            winner_name = "Black (Player)"
            
        winner_text_str = f"Winner: {winner_name}"
        winner_text = self.font.render(winner_text_str, True, COLOR_TEXT)
        winner_rect = winner_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
        self.screen.blit(winner_text, winner_rect)

        # Texto de Puntaje
        score_str = f"White: {self.game.white_horse.score} - Black: {self.game.black_horse.score}"
        score_text = self.small_font.render(score_str, True, COLOR_TEXT)
        score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 10))
        self.screen.blit(score_text, score_rect)

        # Botón de Reinicio
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
            
            if self.state == 'START':
                button_rects = self.draw_start_screen()
                
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        self.running = False
                    
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pos = pygame.mouse.get_pos()
                        for rect, diff in button_rects:
                            if rect.collidepoint(pos):
                                self.difficulty = diff
                                self.game = Game(difficulty=self.difficulty)
                                self.state = 'PLAYING'
                
                pygame.display.update()
                continue

            # ESTADO DE JUEGO
            game_over = self.game.game_over()
            winner = None

            if game_over:
                winner = self.game.check_winner()
                self.status_message = f"Game Over! Winner: {winner}"
                
            else:
                # Verificar si el jugador actual tiene movimientos
                if not self.game.get_valid_moves():
                    self.status_message = f"No moves for {self.game.turn.name}. Skipping turn..."
                    # Dibujar para mostrar mensaje antes de saltar
                    self.draw_panel()
                    self.draw_board()
                    pygame.display.update()
                    pygame.time.wait(1500)
                    
                    self.game.change_turn()
                    continue

            if self.game.turn == self.game.white_horse and not game_over:
                # 1. Actualizar Estado a Pensando
                self.status_message = "AI Thinking..."
                self.draw_panel()
                self.draw_board()
                pygame.display.update()
                
                # 2. Retraso Artificial para "Pensando"
                pygame.time.wait(500)
                
                # 3. Obtener Decisión
                best_move = self.game.get_ai_decision()
                
                if best_move:
                    # 4. Resaltar Objetivo
                    self.ai_target_pos = best_move
                    self.status_message = f"AI moving to {best_move}..."
                    self.draw_panel()
                    self.draw_board()
                    pygame.display.update()
                    
                    # 5. Retraso para mostrar resaltado
                    pygame.time.wait(1000)
                    
                    # 6. Ejecutar Movimiento
                    self.game.move(best_move)
                    self.ai_target_pos = None # Limpiar resaltado
                else:
                    # Debería ser manejado por la verificación de no movimientos, pero por si acaso
                    self.status_message = "AI has no moves!"
                    self.draw_panel()
                    self.draw_board()
                    pygame.display.update()
                    pygame.time.wait(1000)
            
            # Actualizar estado para turno del jugador
            if self.game and self.game.turn == self.game.black_horse and not game_over:
                 self.status_message = "Your Turn (Black Horse)"

            # Manejo de Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                
                if event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    
                    if game_over:
                        button_rect = pygame.Rect(0, 0, 200, 50)
                        button_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80)
                        if button_rect.collidepoint(pos):
                            self.state = 'START' # Volver a la pantalla de inicio
                            self.game = Game(difficulty=self.difficulty)
                            game_over = False
                            winner = None
                    else:
                        # Clics de lógica del juego
                        if self.game.turn == self.game.black_horse:
                             row, col = self.get_row_col_from_mouse(pos)
                             if row is not None and col is not None:
                                 self.game.move(end=(row, col))
            
            # Dibujando
            self.draw_panel()
            self.draw_board()

            if game_over:
                self.draw_game_over(winner)

            pygame.display.update()

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    gui = GUI()
    gui.run()
