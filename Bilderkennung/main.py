import cv2
from camera_utils import init_camera, capture_frame, find_chessboard
from chess_logic import ChessBoard
from stockfish_integration import StockfishIntegration

def main():
    # Kameraeinstellungen (Diese Werte sollten angepasst werden)
    frame_width = 1920
    frame_height = 1080
    exposure = -6.5

    # Pfad zu Stockfish aktualisieren
    stockfish_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"
    stockfish = StockfishIntegration(stockfish_path)

    # Kamera initialisieren
    cap = init_camera(frame_width, frame_height, exposure)
    
    # Schachbrett initialisieren
    chess_board = ChessBoard()
    chess_board.initialize_board()

    # Anzahl der Frames zum Sammeln von Durchschnittswerten
    num_initial_frames = 20
    num_update_frames = 5
    
    try:
        # Durchschnittliche RGB-Werte für jedes Feld am Anfang sammeln
        for _ in range(num_initial_frames):
            image_path = './chessboard.jpg'  # Update this to the path of your image
            frame = cv2.imread(image_path)
            
            ret, corners = find_chessboard(frame)
            corners_reshaped = corners.reshape((7, 7, 2))
            print("corners are", corners_reshaped)
            if ret:
                # Hier Logik zum Berechnen und Aktualisieren der durchschnittlichen RGB-Werte einfügen
                pass

        # Warten auf Benutzereingabe, um mit der Verarbeitung fortzufahren
        input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")

        # Durchschnittliche RGB-Werte erneut sammeln und Änderungen erkennen
        for _ in range(num_update_frames):
            image_path = './chessboard.jpg'  # Update this to the path of your image
            frame = cv2.imread(image_path)
            print("ok")
            
            ret, corners = find_chessboard(frame)
            if ret:
                chess_board.calculate_average_rgb_for_each_square(frame, corners)
                pass

        # Basierend auf erkannten Änderungen das Schachbrett aktualisieren und den neuen FEN-String an Stockfish senden
        # Beispiel: chess_board.update_board(new_rgb_values) und Änderungen erkennen
        # Beispiel: stockfish.set_fen_position(chess_board.to_fen())
        
        # Den besten Zug von Stockfish bekommen und ausgeben
        best_move = stockfish.get_best_move()
        print(f"Der beste Zug ist: {best_move}")

    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # Kamera freigeben
        cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
