from stockfish import Stockfish

class StockfishIntegration:
    def __init__(self, path_to_stockfish, skill_level=10, elo_rating=None):
        """
        Initialisiert Stockfish mit optionalen Parametern für den Schwierigkeitsgrad und die ELO-Bewertung.
        """
        print("skill elvel ist", skill_level)
        print("elorating", elo_rating)
        self.stockfish = Stockfish(path=path_to_stockfish)
        if elo_rating:
            self.stockfish.update_engine_parameters({
                "UCI_LimitStrength": "true",
                "UCI_Elo": elo_rating
            })
        if skill_level is not None and not elo_rating:
            self.stockfish.update_engine_parameters({
                "Skill Level": skill_level
            })
    def set_fen_position(self, fen_str):
        """Setzt die aktuelle Position auf dem Schachbrett mit einer FEN-Notation."""
        self.stockfish.set_fen_position(fen_str)
        
    def get_best_move(self, time=1):
        """Ermittelt den besten Zug für die aktuelle Position innerhalb einer bestimmten Zeit."""
        best_move = self.stockfish.get_best_move_time(time)
        piece = self.get_piece_at_move(best_move)
        print("piece is", piece)
        return best_move, piece
        
    def make_move(self, move):
        """Führt einen Zug aus und aktualisiert die Position auf dem Brett."""
        self.stockfish.make_moves_from_current_position([move])
        
    def get_fen_position(self):
        """Gibt die aktuelle Position als FEN-String zurück."""
        return self.stockfish.get_fen_position()
    
    def get_board_visual(self):
        return self.stockfish.get_board_visual()
    
    def get_piece_at_move(self, move):
        """Gibt die Figur zurück, die sich am Ausgangspunkt des Zuges befindet."""
        fen = self.get_fen_position().split(' ')[0]
        rows = fen.split('/')
        
        from_square = move[:2]
        col, row = ord(from_square[0]) - ord('a'), 8 - int(from_square[1])
        
        fen_row = rows[row]
        current_col = 0
        for char in fen_row:
            if char.isdigit():
                current_col += int(char)
            else:
                if current_col == col:
                    return char
                current_col += 1
        return None

'''# Beispiel für die Verwendung:
# Pfad zur Stockfish-Executable aktualisieren
stockfish_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"
stockfish_integration = StockfishIntegration(stockfish_path)

# Beispiel, wie man es in einem anderen Teil des Programms nutzen könnte
fen_position = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
stockfish_integration.set_fen_position(fen_position)
best_move = stockfish_integration.get_best_move()
print(f"Der beste Zug ist: {best_move}")'''
