import random
from settings import *

class Game:
    def __init__(self):
        self.board = [[None for _ in range(COLS)] for _ in range(ROWS)]
        self.turn = 'white'  # 'white' or 'black'
        self.selected_piece = None
        self.valid_moves = []
        self.destroyed_tiles = [] # List of (row, col)
        self.scores = {'white': 0, 'black': 0}
        self._init_board()

    def _init_board(self):
        # Initialize with a White Knight at a random position or fixed
        self.board[7][1] = 'WN' # White Knight
        self.board[0][6] = 'BN' # Black Knight

    def get_piece(self, row, col):
        if 0 <= row < ROWS and 0 <= col < COLS:
            return self.board[row][col]
        return None

    def select(self, row, col):
        piece = self.get_piece(row, col)
        
        # If a piece is already selected, try to move to the clicked square
        if self.selected_piece:
            if (row, col) in self.valid_moves:
                self.move(self.selected_piece, (row, col))
                self.selected_piece = None
                self.valid_moves = []
                return True
            else:
                # If clicked on another piece of same color, select that instead
                if piece and piece[0] == self.turn[0].upper():
                    self.selected_piece = (row, col)
                    self.valid_moves = self.get_valid_moves(row, col)
                    return True
                else:
                    # Deselect if clicked elsewhere
                    self.selected_piece = None
                    self.valid_moves = []
                    return False
        
        # If no piece selected, try to select one
        if piece and piece[0] == self.turn[0].upper():
            self.selected_piece = (row, col)
            self.valid_moves = self.get_valid_moves(row, col)
            return True

        return False

    def get_valid_moves(self, row, col):
        moves = []
        piece = self.board[row][col]
        if not piece:
            return moves

        # Knight moves: L-shape
        # (row +/- 2, col +/- 1) and (row +/- 1, col +/- 2)
        offsets = [
            (-2, -1), (-2, 1),
            (-1, -2), (-1, 2),
            (1, -2), (1, 2),
            (2, -1), (2, 1)
        ]

        for dr, dc in offsets:
            r, c = row + dr, col + dc
            if 0 <= r < ROWS and 0 <= c < COLS:
                # Check if tile is destroyed
                if (r, c) in self.destroyed_tiles:
                    continue
                
                target = self.board[r][c]
                # Can move to empty square or capture enemy
                if target is None or target[0] != piece[0]:
                    moves.append((r, c))
        
        return moves

    def move(self, start, end):
        start_row, start_col = start
        end_row, end_col = end
        
        piece = self.board[start_row][start_col]
        
        # Destroy the tile where the piece was
        self.destroyed_tiles.append((start_row, start_col))
        
        # Update board
        self.board[start_row][start_col] = None
        self.board[end_row][end_col] = piece
        
        # Update score (1 point per move)
        self.scores[self.turn] += 1
        
        self.change_turn()

    def change_turn(self):
        if self.turn == 'white':
            self.turn = 'black'
        else:
            self.turn = 'white'

    def ai_move(self):
        # Find White Knight (assuming only one for now based on prompt)
        # Prompt says "caballo blanco (IA)"
        # If it's white's turn and AI controls white
        if self.turn == 'white':
            knights = []
            for r in range(ROWS):
                for c in range(COLS):
                    if self.board[r][c] == 'WN':
                        knights.append((r, c))
            
            if knights:
                # Pick a random knight (if multiple)
                knight_pos = random.choice(knights)
                moves = self.get_valid_moves(knight_pos[0], knight_pos[1])
                if moves:
                    target = random.choice(moves)
                    self.move(knight_pos, target)
                    return True
        return False
