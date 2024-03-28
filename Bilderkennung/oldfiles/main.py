import cv2
from camera_utils import init_camera, capture_frame, find_chessboard
from chess_logic import ChessBoard
from stockfish_integration import StockfishIntegration
import utilities
import numpy as np

def main():
    # Kameraeinstellungen (Diese Werte sollten angepasst werden)
    frame_width = 1920
    frame_height = 1080
    exposure = -6.5

    # Pfad zu Stockfish aktualisieren
    stockfish_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"
    stockfish = StockfishIntegration(stockfish_path)

    # Kamera initialisieren
    #cap = init_camera(frame_width, frame_height, exposure)
    
    # Schachbrett initialisieren
    chess_board = ChessBoard()
    chess_board.initialize_board()

    # Anzahl der Frames zum Sammeln von Durchschnittswerten
    num_initial_frames = 20
    num_update_frames = 5
    
    try:
        # Durchschnittliche RGB-Werte für jedes Feld am Anfang sammeln
        for _ in range(num_initial_frames):
            image_path = './images/chessboard3.1.jpg'  # Update this to the path of your image
            frame = cv2.imread(image_path)

            '''frame = capture_frame(cap)

            loop =True
            while loop:
                ret, corners = find_chessboard(frame)
                if ret:
                    loop = False
                else:
                    frame = capture_frame(cap)'''
            
            ret, corners = find_chessboard(frame)
            sorted_corners = utilities.sort_corners(corners)
            #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
            outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
            outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
            sorted_outer_corners = utilities.sort_corners(outer_corners_np)
            
            #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  ret)
            cv2.imshow('Schachbrett Detektor', frame)
            cv2.waitKey(1)
            if ret:
                chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                pass
        
        
        chess_board.calculate_mean()   
         
        
        

        whiteTurn = True
        count =0
        stockfish.set_fen_position("rnbqk3/8/8/8/8/8/8/3QKBNR w KQkq - 0 1")
        while(True):
            
            print(stockfish.get_board_visual())
            best_move = stockfish.get_best_move()
            for square in chess_board.squares:
                print(f"position {square.position} piece is {square.piece}")

            stockfish.make_move(best_move)
            print(stockfish.get_board_visual())
            print(f"Der beste Zug ist: {best_move}")

            for _ in range(num_update_frames):
                frame=None
                if count==0:
                    image_path = './images/chessboard3.2.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)
                if count==1:
                    image_path = './images/chessboard3.4.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)
                if count==2:
                    image_path = './images/chessboard3.2.5.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path) 
                if count==3:
                    image_path = './images/chessboard3.3.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)
                    
                ret, corners = find_chessboard(frame)
                sorted_corners = utilities.sort_corners(corners)
                #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
                outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                sorted_outer_corners = utilities.sort_corners(outer_corners_np)

                #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
                cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  ret)
                cv2.imshow('Schachbrett Detektor', frame)
                cv2.waitKey(1)
                if ret:
                    chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                    pass

            chess_board.calculate_mean() 
            '''for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value}")'''

            changes = chess_board.find_most_significant_changes()  
            print("changes", changes)
            move_made = chess_board.update_chessboard(changes, whiteTurn)
            


            input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")
            whiteTurn = not whiteTurn
            for _ in range(num_update_frames):
                frame=None
                if count==0:
                    image_path = './images/chessboard3.3.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)
                if count==1:
                    image_path = './images/chessboard3.2.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)
                if count==2:
                    image_path = './images/chessboard3.2.5.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path) 
                if count==3:
                    image_path = './images/chessboard3.3.jpg'  # Update this to the path of your image
                    frame = cv2.imread(image_path)   
                ret, corners = find_chessboard(frame)
                sorted_corners = utilities.sort_corners(corners)
                #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
                outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                sorted_outer_corners = utilities.sort_corners(outer_corners_np)

                #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
                cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  ret)
                cv2.imshow('Schachbrett Detektor', frame)
                cv2.waitKey(1)
                if ret:
                    chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                    pass

            chess_board.calculate_mean() 
            '''for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value}")'''

            changes = chess_board.find_most_significant_changes()  
            
            move_made = chess_board.update_chessboard(changes, whiteTurn)
            print("movemade", move_made)
            stockfish.make_move(move_made)
            stockfish.get_board_visual()
            # Basierend auf erkannten Änderungen das Schachbrett aktualisieren und den neuen FEN-String an Stockfish senden
            # Beispiel: chess_board.update_board(new_rgb_values) und Änderungen erkennen
            # Beispiel: stockfish.set_fen_position(chess_board.to_fen())
            
            # Den besten Zug von Stockfish bekommen und ausgeben
            
            count+=1


    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # Kamera freigeben
        #cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
