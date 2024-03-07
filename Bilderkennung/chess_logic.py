class ChessSquare:
    def __init__(self, position, piece='-', mean_rgb_value=(0, 0, 0), status='empty'):
        self.position = position
        self.piece = piece
        self.mean_rgb_value = mean_rgb_value
        self.status = status

    def calc_difference(self, new_rgb_value):
        """Berechnet den Farbunterschied zum gespeicherten mean_rgb_value."""
        return sum(abs(a-b) for a, b in zip(self.mean_rgb_value, new_rgb_value))
    
    def update_square(self, new_rgb_value, new_status=None, new_piece=None):
        """Aktualisiert die Eigenschaften des Schachfelds."""
        self.mean_rgb_value = new_rgb_value
        if new_status:
            self.status = new_status
        if new_piece:
            self.piece = new_piece
class ChessBoard:
    def __init__(self):
        self.squares = [ChessSquare(position, starting_pieces.get(position, '-')) 
                        for position in chess_positions]
    
    def initialize_board(self):
        """Initialisiert das Schachbrett mit den Startpositionen der Figuren."""
        # Dies wurde bereits im Konstruktor gemacht, kann aber für spätere Resets nützlich sein

    def update_board(self, new_rgb_values):
        """Aktualisiert das Brett basierend auf neuen RGB-Werten."""
        for square in self.squares:
            if square.position in new_rgb_values:
                square.update_square(new_rgb_values[square.position])

    def detect_changes(self, threshold):
        """Erkennt Änderungen auf dem Brett anhand eines Farbunterschiedsschwellenwerts."""
        changed_squares = []
        for square in self.squares:
            if square.calc_difference(new_rgb_values[square.position]) > threshold:
                changed_squares.append(square.position)
        return changed_squares
        
    def to_fen(self):
        """Generiert die FEN-Notation des aktuellen Bretts."""
        rows = []
        for row in range(8, 0, -1):  # Schachbrettreihen von 8 bis 1
            empty_squares = 0
            fen_row = ''
            for col in 'abcdefgh':  # Schachbrettspalten von 'a' bis 'h'
                square = next(s for s in self.squares if s.position == f'{col}{row}')
                if square.piece == '-':
                    empty_squares += 1
                else:
                    if empty_squares:
                        fen_row += str(empty_squares)
                        empty_squares = 0
                    fen_row += square.piece
            if empty_squares:  # Für die letzte Reihe, falls noch leere Felder übrig sind
                fen_row += str(empty_squares)
            rows.append(fen_row)
        return '/'.join(rows) + ' w KQkq - 0 1'  # Beispiel: Ergänzt wer am Zug ist, Rochademöglichkeiten etc.

    def from_fen(self, fen_string):
        """Aktualisiert das Schachbrett basierend auf der gegebenen FEN-Notation."""
        rows = fen_string.split(' ')[0].split('/')
        for row_index, row in enumerate(rows):
            col_index = 0
            for char in row:
                if char.isdigit():
                    col_index += int(char)  # Überspringt leere Felder
                else:
                    position = f'{chr(97 + col_index)}{8 - row_index}'
                    square = next(s for s in self.squares if s.position == position)
                    square.piece = char
                    col_index += 1
        

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