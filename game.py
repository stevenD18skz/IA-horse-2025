import random
from settings import *
import random

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
    def __init__(self):
        self.board = self._init_board()
        self.board = [
            [-3, 0, 0, 0, 0, 0, 0, 0], 
            [5, 0, 0, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 1, 0, 0], 
            [0, 0, 0, 0, 0, 0, 10, 0], 
            [0, 0, -10, 0, 0, 0, 0, 0], 
            [0, 0, 0, 0, 0, 0, 0, 0], 
            [0, -20, 0, 0, 0, 'WH', 0, -5], 
            [3, 0, 0, 'BH', -1, 0, 0, 0]]
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



    def ai_move(self):
        moves = self.get_valid_moves()

        if moves:
            target = random.choice(moves)
            self.move(target)
            return True
        return False




    #GAME STATE
    def change_turn(self):
        if self.turn == self.black_horse:
            self.turn = self.white_horse
        else:
            self.turn = self.black_horse



    def check_winner(self):
        if self.white_horse.score > self.black_horse.score:
            return 'WH'
        elif self.black_horse.score > self.white_horse.score:
            return 'BH'
        return None



    def game_over(self):
        return False


