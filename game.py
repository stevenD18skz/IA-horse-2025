import random
from settings import *
import copy

class Horse:
    def __init__(self, name):
        self.name = name
        self.score = 0
        self.position = None

    def set_position(self, row, col):
        self.position = (row, col)

    def get_position(self):
        return self.position




class Game:
    def __init__(self, difficulty=4):
        self.difficulty = difficulty
        self.board = self._init_board()
        self.white_horse = Horse('WH')
        self.black_horse = Horse('BH')
        self.turn = self.white_horse

        self.set_horse_position()

        self.white_horse_penality = False
        self.black_horse_penality = False
        
        
        
    # INICIO
    def _init_board(self):
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        elements_to_place = [-1, -3, -4, -5, -10, 1, 3, 4, 5, 10, 'WH', 'BH']
        
        # Generar todas las posiciones posibles
        all_positions = [(x, y) for x in range(ROWS) for y in range(COLS)]

        # Seleccionar aleatoriamente posiciones únicas para los elementos
        random_positions = random.sample(all_positions, len(elements_to_place))
        
        for i, element in enumerate(elements_to_place):
            row, col = random_positions[i]
            board[row][col] = element
        
        return board



    def set_horse_position(self):
        for r in range(ROWS):
            for c in range(COLS):
                if self.board[r][c] == 'WH':
                    self.white_horse.set_position(r, c)
                elif self.board[r][c] == 'BH':
                    self.black_horse.set_position(r, c)
        


    # CABALLOS
    def get_valid_moves(self):
        moves = []
        # Movimientos del Caballo: Forma de L
        # (fila +/- 2, col +/- 1) y (fila +/- 1, col +/- 2)
        offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        row, col = self.turn.get_position()

        for dx, dy in offsets:
            x, y = row + dx, col + dy
            if 0 <= x < ROWS and 0 <= y < COLS:
                # Verificar si la casilla está destruida
                if self.board[x][y] == -20:
                    continue
                
                target = self.board[x][y]

                # Puede moverse a una casilla vacía o capturar al enemigo
                if target == -20 or target == 'BH' or target == 'WH':
                    continue

                moves.append((x, y))

        return moves



    def move(self, end):
        start_row, start_col = self.turn.get_position()
        end_row, end_col = end

        valides = self.get_valid_moves()
        if (end_row, end_col) not in valides:
            return

        # Actualizar posición de la pieza
        self.turn.set_position(end_row, end_col)

        
        # Actualizar puntaje (1 punto por movimiento)
        piece = self.board[end_row][end_col]
        if isinstance(piece, int) and piece != -20:
            self.turn.score += piece
        
        # Actualizar tablero
        self.board[start_row][start_col] = -20
        self.board[end_row][end_col] = self.turn.name
        
        
        self.change_turn()



    def get_ai_decision(self):
        _, best_move = self.minimax(self, self.difficulty, True)
        return best_move



    def evaluate_board(self, game_state):
        # Función Heurística
        # 1. Diferencia de Puntaje (Primaria)
        score_diff = game_state.white_horse.score - game_state.black_horse.score
        
        # 2. Movilidad (Secundaria)
        # Calcular movimientos disponibles para ambos para fomentar mantener opciones abiertas
        # y evitar la situación de penalización de -4.
        white_moves = len(self.get_valid_moves_sim(game_state, game_state.white_horse))
        black_moves = len(self.get_valid_moves_sim(game_state, game_state.black_horse))
        
        mobility_score = (white_moves - black_moves) * 0.5 # Ponderar la movilidad menos que los puntos reales

        return score_diff + mobility_score



    def get_valid_moves_sim(self, game_state, horse):
        # Ayudante para obtener movimientos para un estado y caballo específicos sin cambiar self.turn
        moves = []
        offsets = [
            (-2, -1), (-2, 1), (-1, -2), (-1, 2),
            (1, -2), (1, 2), (2, -1), (2, 1)
        ]
        row, col = horse.get_position()
        
        for dx, dy in offsets:
            x, y = row + dx, col + dy
            if 0 <= x < ROWS and 0 <= y < COLS:
                if game_state.board[x][y] == -20:
                    continue
                target = game_state.board[x][y]
                if target in [-20, 'BH', 'WH']:
                    continue
                moves.append((x, y))
        return moves

    def minimax(self, game_state, depth, is_maximizing):
        # Caso base: Profundidad alcanzada o Fin del Juego
        white_moves = self.get_valid_moves_sim(game_state, game_state.white_horse)
        black_moves = self.get_valid_moves_sim(game_state, game_state.black_horse)
        
        game_over = len(white_moves) == 0 and len(black_moves) == 0
        
        if depth == 0 or game_over:
            return self.evaluate_board(game_state), None

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None

            if not white_moves:
                if black_moves:
                     # IA pasa, el oponente juega (paso de minimización)
                     # Aplicamos la penalización de -4 al puntaje de la IA en la copia para una evaluación precisa
                     new_game_state = copy.deepcopy(game_state)
                     new_game_state.white_horse.score -= 4
                     eval_score, _ = self.minimax(new_game_state, depth - 1, False)
                     return eval_score, None
                else:
                    # Ambos sin movimientos -> Fin del Juego (manejado por el caso base arriba usualmente, pero verificar doblemente)
                    return self.evaluate_board(game_state), None

            for move in white_moves:
                # Crear una copia del estado del juego para simular el movimiento
                new_game_state = copy.deepcopy(game_state)
                
                # Ejecutar movimiento en la copia
                # Necesitamos hacer manualmente lo que hace move() pero en el nuevo estado
                start_r, start_c = new_game_state.white_horse.get_position()
                end_r, end_c = move
                
                # Update score
                piece = new_game_state.board[end_r][end_c]
                if isinstance(piece, int) and piece != -20:
                    new_game_state.white_horse.score += piece
                
                # Actualizar tablero
                new_game_state.board[start_r][start_c] = -20
                new_game_state.board[end_r][end_c] = 'WH'
                new_game_state.white_horse.set_position(end_r, end_c)
                
                # Llamada recursiva (Paso de minimización)
                eval_score, _ = self.minimax(new_game_state, depth - 1, False)
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_move = move
            
            return max_eval, best_move
        
        else: # Minimizing (Player's turn)
            min_eval = float('inf')
            best_move = None
            
            if not black_moves:
                if white_moves:
                    # Jugador pasa, IA juega (paso de maximización)
                    # Jugador recibe penalización de -4
                    new_game_state = copy.deepcopy(game_state)
                    new_game_state.black_horse.score -= 4
                    eval_score, _ = self.minimax(new_game_state, depth - 1, True)
                    return eval_score, None
                else:
                    return self.evaluate_board(game_state), None

            for move in black_moves:
                new_game_state = copy.deepcopy(game_state)
                
                start_r, start_c = new_game_state.black_horse.get_position()
                end_r, end_c = move
                
                piece = new_game_state.board[end_r][end_c]
                if isinstance(piece, int) and piece != -20:
                    new_game_state.black_horse.score += piece
                
                new_game_state.board[start_r][start_c] = -20
                new_game_state.board[end_r][end_c] = 'BH'
                new_game_state.black_horse.set_position(end_r, end_c)
                
                eval_score, _ = self.minimax(new_game_state, depth - 1, True)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
            
            return min_eval, best_move




    # ESTADO DEL JUEGO
    def change_turn(self):
        if self.turn == self.black_horse:
            self.turn = self.white_horse
        else:
            self.turn = self.black_horse



    def check_winner(self):
        if self.white_horse.score > self.black_horse.score:
            return self.white_horse.name
        elif self.black_horse.score > self.white_horse.score:
            return self.black_horse.name
        return None



    def game_over(self):
        def get_valid_moves_by_horse(horse):
            moves = []
            # Knight moves: L-shape
            # (row +/- 2, col +/- 1) and (row +/- 1, col +/- 2)
            offsets = [
                (-2, -1), (-2, 1),
                (-1, -2), (-1, 2),
                (1, -2), (1, 2),
                (2, -1), (2, 1)
            ]

            row, col = horse.get_position()

            for dx, dy in offsets:
                x, y = row + dx, col + dy
                if 0 <= x < ROWS and 0 <= y < COLS:
                    # Verificar si la casilla está destruida
                    if self.board[x][y] == -20:
                        continue
                    
                    target = self.board[x][y]

                    # No puede moverse a casilla vacía o capturar enemigo
                    if target in [-20, 'BH', 'WH']:
                        continue

                    moves.append((x, y))

            return moves
        
        white_moves = get_valid_moves_by_horse(self.white_horse)
        black_moves = get_valid_moves_by_horse(self.black_horse)

        if len(white_moves) == 0 and len(black_moves) == 0:
            return True

        if len(white_moves) == 0:
            if not self.white_horse_penality:
                self.white_horse_penality = True
                self.white_horse.score -= 4
            
        if len(black_moves) == 0:
            if not self.black_horse_penality:
                self.black_horse_penality = True
                self.black_horse.score -= 4
            
        return False


