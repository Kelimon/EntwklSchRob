import numpy as np
import cv2

class ChessSquare:
    def __init__(self, position, piece='-', mean_rgb_value=(0, 0, 0), status='empty'):
        self.position = position
        self.piece = piece
        self.rgb_values = []
        self.last_rgb_value = (0, 0, 0)
        self.mean_rgb_value = np.array(mean_rgb_value)
        self.status = status

        if self.piece != '-':
            self.status = 'occupied'

    def calc_difference(self, new_rgb_value):
        """Berechnet den Farbunterschied zum gespeicherten mean_rgb_value unter Verwendung von NumPy."""
        new_rgb_array = np.array(new_rgb_value)
        difference = np.abs(self.mean_rgb_value - new_rgb_array)
        return np.sum(difference)
    
    def update_square(self, new_rgb_value, new_status=None, new_piece=None):
        """Aktualisiert die Eigenschaften des Schachfelds."""
        self.mean_rgb_value = new_rgb_value
        if new_status:
            self.status = new_status
        if new_piece:
            self.piece = new_piece


class ChessBoard:

    '''starting_pieces = {
        'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
        'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
        'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
        'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r'
    }'''
    starting_pieces = {
    'a8': 'r', 'b8': '-', 'c8': '-', 'd8': '-', 'e8': 'k', 'f8': '-', 'g8': '-', 'h8': '-',
    'a7': '-', 'b7': '-', 'c7': '-', 'd7': '-', 'e7': '-', 'f7': '-', 'g7': '-', 'h7': '-',
    'a6': '-', 'b6': '-', 'c6': '-', 'd6': '-', 'e6': '-', 'f6': '-', 'g6': '-', 'h6': '-',
    'a5': '-', 'b5': '-', 'c5': '-', 'd5': '-', 'e5': '-', 'f5': '-', 'g5': '-', 'h5': '-',
    'a4': '-', 'b4': '-', 'c4': '-', 'd4': '-', 'e4': '-', 'f4': '-', 'g4': '-', 'h4': '-',
    'a3': '-', 'b3': '-', 'c3': '-', 'd3': '-', 'e3': '-', 'f3': '-', 'g3': '-', 'h3': '-',
    'a2': '-', 'b2': '-', 'c2': '-', 'd2': '-', 'e2': '-', 'f2': '-', 'g2': '-', 'h2': '-',
    'a1': '-', 'b1': '-', 'c1': '-', 'd1': '-', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': '-',
}

    chess_positions = [f"{chr(file)}{rank}" for rank in range(8, 0, -1) for file in range(ord('a'), ord('h')+1)]
    
    
    def __init__(self):
        
        self.squares = [ChessSquare(position, self.starting_pieces.get(position, '-')) 
                        for position in self.chess_positions]

    
    def initialize_board(self):
        """Initialisiert das Schachbrett mit den Startpositionen der Figuren."""
        # Dies wurde bereits im Konstruktor gemacht, kann aber für spätere Resets nützlich sein

    def get_square_by_position(self, position):
        # Gibt das Schachfeld-Objekt zurück, das der angegebenen Position entspricht
        for square in self.squares:
            if square.position == position:
                return square
        return None  # Gibt None zurück, wenn kein Feld mit der Position gefunden wurde
    
    def calculate_mean(self):
        for square in self.squares:
            square.last_rgb_value = square.mean_rgb_value
            square.mean_rgb_value = np.mean(square.rgb_values, axis=0)
            square.rgb_values=[]

    def     find_most_significant_changes(self, num_changes=5):
        changes = []
        for square in self.squares:
            difference = np.linalg.norm(np.array(square.last_rgb_value) - np.array(square.mean_rgb_value))
            changes.append((square.position, difference))
                
        
        # Sortieren der Veränderungen nach ihrer Signifikanz
        changes.sort(key=lambda x: x[1], reverse=True)
        print("changes", changes)
        # Auswahl der n signifikantesten Veränderungen
        significant_changes = changes[:num_changes]
        print("changes", significant_changes)
        return [change[0] for change in significant_changes]


    def calculate_average_rgb_for_each_square(self, frame, corners):
        if corners is None or len(corners) != 81:
            return False  # Schachbrett wurde nicht gefunden oder falsche Anzahl von Ecken

        # Ecken zu einem 7x7 Gitter umformen
        #corners_reshaped = corners.reshape((7, 7, 2))

        for row in range(8):  # 6 Reihen von Feldern, basierend auf den 7x7 erkannten Ecken
            for col in range(8):  # 6 Spalten von Feldern
                # Ecken für das aktuelle Feld extrahieren
                top_left = corners[row * 9 + col]
                top_right = corners[row * 9 + (col + 1)]
                bottom_left = corners[(row + 1) * 9 + col]
                bottom_right = corners[(row + 1) * 9 + (col + 1)]
                # Compute the bounding rectangle of the current field
                x_min = int(min(top_left[0], bottom_left[0], top_right[0], bottom_right[0]))
                x_max = int(max(top_left[0], bottom_left[0], top_right[0], bottom_right[0]))
                y_min = int(min(top_left[1], bottom_left[1], top_right[1], bottom_right[1]))
                y_max = int(max(top_left[1], bottom_left[1], top_right[1], bottom_right[1]))

                # Extract the region of interest (ROI) from the frame
                field_roi = frame[y_min:y_max, x_min:x_max]

                # Calculate the average color within this ROI
                avg_color = np.mean(field_roi, axis=(0, 1))
                self.squares[row * 8 + col].rgb_values.append(avg_color)
                #self.squares[row * 8 + col].update_square(new_rgb_value=avg_color)
                '''
                top_left = corners_reshaped[row, col]
                top_right = corners_reshaped[row, col + 1]
                bottom_left = corners_reshaped[row + 1, col]
                bottom_right = corners_reshaped[row + 1, col + 1]

                # Ecken des Feld-ROI (Region of Interest)
                rect = np.array([top_left, top_right, bottom_right, bottom_left], dtype="float32")

                # Das Zielquadrat, in das wir transformieren werden
                # Die Größe (100x100) kann basierend auf Ihrer Anwendung angepasst werden
                dst = np.array([[0, 0], [100 - 1, 0], [100 - 1, 100 - 1], [0, 100 - 1]], dtype="float32")

                # Führen Sie die Transformation durch
                M = cv2.getPerspectiveTransform(rect, dst)
                warped = cv2.warpPerspective(frame, M, (100, 100))

                # Durchschnittlichen RGB-Wert für das transformierte Feld berechnen
                square_rgb = np.mean(warped, axis=(0, 1))

                # Berechnen der Schachbrett-Position basierend auf (row, col) und Aktualisieren des entsprechenden ChessSquare
                # Beachten Sie, dass die Positionsberechnung angepasst werden muss, um die richtigen Schachfelder zu adressieren
                position = chr(97 + col) + str(8 - row)
                chess_square = self.squares[0]
                if chess_square:
                    chess_square.update_square(new_rgb_value=square_rgb)
'''
        return True

    
    def sort_corners(corners):
        sorted_rows = []
        
        while len(corners) > 0:
            # Finde den obersten linken Punkt
            corners = corners.reshape(-1, 2)

            sums = corners[:, 0] + corners[:, 1]
            top_left_index = np.argmin(sums)
            top_left_point = corners[top_left_index]
            
            # Finde alle Punkte in der gleichen Reihe
            row_points = [point for point in corners if abs(point[1] - top_left_point[1]) <= 15]
            
            # Sortiere die Punkte in der Reihe nach ihrer X-Koordinate
            row_points_sorted = sorted(row_points, key=lambda x: x[0])
            
            # Füge die sortierte Reihe zu `sorted_rows` hinzu
            sorted_rows.append(row_points_sorted)
            
            # Entferne die verarbeiteten Punkte
            corners = np.array([point for point in corners if not is_point_in_list(point, row_points_sorted)])

        
        # Konvertiere `sorted_rows` in ein einziges Array für die Ausgabe
        sorted_corners = np.vstack(sorted_rows)
        return sorted_corners

    def update_chessboard(self, changes, whiteTurn):
        # Identifizieren der Felder basierend auf den Änderungen
        from_square = None
        to_square = None
        print("changes", changes)
        input("Drücken Sie Enter, wenn sie fortfahren wollen...")
        # Ermitteln, welches der geänderten Felder das Startfeld (from_square) ist
        for change in changes[:2]:
            square = self.get_square_by_position(change)
            print("square", square.position)
            # Wenn whiteTurn True ist, suche nach einem Feld mit einem Großbuchstaben (weiße Figur)
            # Sonst suche nach einem Feld mit einem Kleinbuchstaben (schwarze Figur)
            if (whiteTurn and square.piece.isupper()) or (not whiteTurn and square.piece.islower()):
                from_square = square
            else:
                to_square = square
        print("fromsquare")
        print("To square:", to_square.position)
        try:
            print("From square:", from_square.position)
        finally:
            print("From square:", from_square)
        # Sicherstellen, dass sowohl Start- als auch Zielfeld identifiziert wurden
        if not from_square or not to_square:
            print("Fehler: Konnte die Züge nicht korrekt identifizieren.")
            return
        
        # Bewegung auf ein leeres Feld oder Schlagen eines Gegners
        to_square.piece = from_square.piece
        to_square.status = 'occupied'
        from_square.piece = '-'
        from_square.status = 'empty'

        return from_square.position +  to_square.position

    def make_move(self, move):
        # Zerlegt den Zug in Start- und Zielfeld
        from_pos, to_pos = move[:2], move[2:]
        from_square = self.get_square_by_position(from_pos)
        to_square = self.get_square_by_position(to_pos)

        # Aktualisiert das Zielfeld mit der Figur vom Startfeld
        to_square.piece = from_square.piece
        to_square.status = 'occupied' if from_square.piece != '-' else 'empty'
        
        # Das Startfeld wird geleert
        from_square.piece = '-'
        from_square.status = 'empty'



    # Hier muss zusätzliche Logik implementiert werden, um zu bestimmen, welches Feld das Start- und Zielfeld ist,
    # da die obige Annahme nicht immer zutrifft. Dies könnte durch Vergleichen der Farben der Figuren,
    # der Spielregeln und möglicher legaler Züge erfolgen.


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

# Create a list of all board positions


# Initialize the board with ChessSquare objects
#board = [ChessSquare(position, starting_pieces.get(position, '-')) for position in chess_positions]
#for square in board:
 #   print(f"Position: {square.position}, Piece {square.piece}")
                    
