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
        self.board = [
            [-3, 0, 0, 0, 0, 0, 0, 0], 
            [5, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 1, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 'WH', 0, -5], 
            ['BH', 0, 0, 0, -1, 0, 0, 0]]
        self.board = self._init_board()
        self.white_horse = Horse('WH')
        self.black_horse = Horse('BH')
        self.turn = self.black_horse

        self.set_horse_position()
        
        
        
    #INIT
    def _init_board(self):
        board = [[0 for _ in range(COLS)] for _ in range(ROWS)]
        elements_to_place = [-1, -3, -5, -10, 1, 3, 5, 10, 'WH', 'BH']
        
        # Generate all possible positions
        all_positions = [(x, y) for x in range(ROWS) for y in range(COLS)]

        # Randomly select unique positions for the elements
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
        


    #HORSES
    def get_valid_moves(self):
        moves = []
        # Knight moves: L-shape
        # (row +/- 2, col +/- 1) and (row +/- 1, col +/- 2)
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
                # Check if tile is destroyed
                if self.board[x][y] == -20:
                    continue
                
                target = self.board[x][y]

                # Can move to empty square or capture enemy
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

        # Update piece position
        self.turn.set_position(end_row, end_col)

        
        # Update score (1 point per move)
        piece = self.board[end_row][end_col]
        if isinstance(piece, int) and piece != -20:
            self.turn.score += piece
        
        # Update board
        self.board[start_row][start_col] = -20
        self.board[end_row][end_col] = self.turn.name
        
        
        self.change_turn()



    def get_ai_decision(self):
        # Returns the best move found by Minimax
        # print(f"AI Thinking... Depth: {self.difficulty}")
        _, best_move = self.minimax(self, self.difficulty, True)
        return best_move



    def evaluate_board(self, game_state):
        # Heuristic Function
        # 1. Score Difference (Primary)
        score_diff = game_state.white_horse.score - game_state.black_horse.score
        
        # 2. Mobility (Secondary)
        # Calculate available moves for both to encourage keeping options open
        # and to avoid the -4 penalty situation.
        white_moves = len(self.get_valid_moves_sim(game_state, game_state.white_horse))
        black_moves = len(self.get_valid_moves_sim(game_state, game_state.black_horse))
        
        mobility_score = (white_moves - black_moves) * 0.5 # Weight mobility less than actual points

        return score_diff + mobility_score



    def get_valid_moves_sim(self, game_state, horse):
        # Helper to get moves for a specific state and horse without changing self.turn
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
        # Base case: Depth reached or Game Over
        white_moves = self.get_valid_moves_sim(game_state, game_state.white_horse)
        black_moves = self.get_valid_moves_sim(game_state, game_state.black_horse)
        
        game_over = len(white_moves) == 0 and len(black_moves) == 0
        
        if depth == 0 or game_over:
            return self.evaluate_board(game_state), None

        if is_maximizing:
            max_eval = float('-inf')
            best_move = None
            
            # If AI has no moves, it passes turn (effectively) or game ends?
            # The rules say: "En cada turno el jugador debe mover su caballo, a no ser que no tengo movimientos posibles."
            # If AI has no moves but Player does, AI passes.
            if not white_moves:
                # Apply penalty if applicable? 
                # "Si durante su turno un jugador no tiene movimientos disponibles pero su adversario sí los tiene, recibirá una penalización de -4 puntos."
                # We simulate this by just passing turn and checking next state.
                # However, to keep it simple in recursion, if no moves, we just evaluate here or skip to next layer with same board?
                # Let's assume if no moves, we return current eval (or handle pass logic if we want to be precise).
                # For simplicity: if no moves, treat as terminal for this branch or just return eval.
                # But wait, if opponent has moves, game isn't over.
                if black_moves:
                     # AI passes, opponent plays (minimizing step)
                     # We apply the -4 penalty to AI score in the copy for accurate evaluation
                     new_game_state = copy.deepcopy(game_state)
                     new_game_state.white_horse.score -= 4
                     eval_score, _ = self.minimax(new_game_state, depth - 1, False)
                     return eval_score, None
                else:
                    # Both no moves -> Game Over (handled by base case above usually, but double check)
                    return self.evaluate_board(game_state), None

            for move in white_moves:
                # Create a copy of the game state to simulate the move
                new_game_state = copy.deepcopy(game_state)
                
                # Execute move on the copy
                # We need to manually do what move() does but on the new state
                start_r, start_c = new_game_state.white_horse.get_position()
                end_r, end_c = move
                
                # Update score
                piece = new_game_state.board[end_r][end_c]
                if isinstance(piece, int) and piece != -20:
                    new_game_state.white_horse.score += piece
                
                # Update board
                new_game_state.board[start_r][start_c] = -20
                new_game_state.board[end_r][end_c] = 'WH'
                new_game_state.white_horse.set_position(end_r, end_c)
                
                # Recursive call (Minimizing step)
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
                    # Player passes, AI plays (maximizing step)
                    # Player gets -4 penalty
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




    #GAME STATE
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
                    # Check if tile is destroyed
                    if self.board[x][y] == -20:
                        continue
                    
                    target = self.board[x][y]

                    # Cant move to empty square or capture enemy
                    if target in [-20, 'BH', 'WH']:
                        continue

                    moves.append((x, y))

            return moves
        
        white_moves = get_valid_moves_by_horse(self.white_horse)
        black_moves = get_valid_moves_by_horse(self.black_horse)

        print(f"==============White Moves: {white_moves}")
        print(f"==============Black Moves: {black_moves}")
        
        if len(white_moves) == 0 and len(black_moves) == 0:
            print("ambos se quedaron sin movimientos")
            return True
        
        print("aun pueden jugar")
        return False


