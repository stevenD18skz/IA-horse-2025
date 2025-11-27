from game import Game

def test_game():
    game = Game()
    print(f"Initial Turn: {game.turn}")
    print(f"Board at (7, 1): {game.board[7][1]}") # WN
    print(f"Board at (0, 6): {game.board[0][6]}") # BN
    
    # AI Move (White)
    print("Executing AI Move...")
    if game.ai_move():
        print("AI Moved.")
    else:
        print("AI Failed to move.")
        
    print(f"Turn after AI: {game.turn}")
    
    if game.turn == 'black':
        # Player Turn
        # Find Black Knight
        bn_pos = None
        for r in range(8):
            for c in range(8):
                if game.board[r][c] == 'BN':
                    bn_pos = (r, c)
                    break
        
        print(f"Black Knight at: {bn_pos}")
        
        # Select Black Knight
        print(f"Selecting {bn_pos}...")
        game.select(bn_pos[0], bn_pos[1])
        print(f"Selected Piece: {game.selected_piece}")
        print(f"Valid Moves: {game.valid_moves}")
        
        if game.valid_moves:
            target = game.valid_moves[0]
            print(f"Moving to {target}...")
            game.select(target[0], target[1])
            print(f"Turn after Player Move: {game.turn}")
            print(f"Old pos {bn_pos} in destroyed? {bn_pos in game.destroyed_tiles}")
        else:
            print("ERROR: Black Knight has no valid moves!")

if __name__ == "__main__":
    test_game()
