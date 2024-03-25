class ChessSquare:
    def __init__(self, position, piece='-', mean_rgb_value=None, status='empty'):
        self.position = position        # The position on the board, e.g., 'a1', 'd4', etc.
        self.piece = piece              # The piece on the square: 'P', 'p', 'R', 'r', etc., or '-' for empty
        self.mean_rgb_value = mean_rgb_value  # The mean RGB value of the square
        self.status = status            # The status of the square: 'empty', 'occupied', etc.

# Initialize a dictionary with the starting piece positions
starting_pieces = {
    'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
    'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
    'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
    'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r'
}

# Create a list of all board positions
chess_positions = [f"{chr(file)}{rank}" for rank in range(1, 9) for file in range(ord('a'), ord('h')+1)]

# Initialize the board with ChessSquare objects
board = [ChessSquare(position, starting_pieces.get(position, '-')) for position in chess_positions]
for square in board:
    print(f"Position: {square.position}, Piece {square.piece}")