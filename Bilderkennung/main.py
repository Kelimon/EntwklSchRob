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
    exposure = 6

    # Pfad zu Stockfish aktualisieren
    stockfish_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"
    stockfish = StockfishIntegration(stockfish_path)
    

    # Kamera initialisieren
    cap = init_camera(frame_width, frame_height, exposure)
    
    # Schachbrett initialisieren
    chess_board = ChessBoard()
    chess_board.initialize_board()

    # Anzahl der Frames zum Sammeln von Durchschnittswerten
    num_initial_frames = 10
    num_update_frames = 3
    
    corners = np.array([[[ 658.5039 ,304.37497]],

 [[ 720.90546,304.15814]],

 [[ 783.3413, 303.84518]],

 [[ 845.9845, 303.32153]],

 [[ 908.43915,302.86517]],

 [[ 970.82025,302.819]],

 [[1033.0961, 302.73743]],

 [[ 659.7971, 367.34088]],

 [[ 722.0644, 367.06445]],

 [[ 784.2212, 366.5902 ]],

 [[ 846.79456,366.46075]],

 [[ 908.9427, 366.24954]],

 [[ 971.01965,365.97467]],

 [[1033.0374, 365.429]],

 [[ 661.34045,429.67065]],

 [[ 722.9752, 429.0975 ]],

 [[ 784.7633, 428.82614]],

 [[ 846.53436,428.0052 ]],

 [[ 908.38824,427.95358]],

 [[ 970.27966,427.35077]],

 [[1031.7573, 426.7821 ]],

 [[ 663.79443,491.27243]],

 [[ 724.8407, 490.73492]],

 [[ 786.10095,490.3452 ]],

 [[ 847.3418, 490.16492]],

 [[ 908.8806, 489.52182]],

 [[ 970.3716, 489.1594 ]],

 [[1031.0383, 488.14993]],

 [[ 665.76697,551.9146 ]],

 [[ 726.3908, 551.70026]],

 [[ 787.1125, 551.8192 ]],

 [[ 848.03314,550.24524]],

 [[ 909.35425,550.42676]],

 [[ 970.3378, 549.5271 ]],

 [[1030.6948, 549.1129 ]],

 [[ 667.4523, 612.58203]],

 [[ 728.1356, 612.20715]],

 [[ 788.8524, 611.8425 ]],

 [[ 849.2287, 610.5089 ]],

 [[ 909.5147, 609.7383 ]],

 [[ 970.14404,609.01715]],

 [[1029.9763, 608.1199 ]],

 [[ 669.1043, 672.4522 ]],

 [[ 729.39294,671.88434]],

 [[ 789.84375,670.2831 ]],

 [[ 849.9975, 669.6963 ]],

 [[ 910.1094, 668.78796]],

 [[ 969.8227, 667.6552 ]],

 [[1029.511,  667.2147 ]]])
    
    sorted_corners = utilities.sort_corners(corners)
    #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
    outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
    outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
    sorted_outer_corners = utilities.sort_corners(outer_corners_np)
    try:
        for _ in range(5):
            ret, frame = capture_frame(cap)
        while True:
            ret, frame = capture_frame(cap) # Read a frame from the camera
            if not ret:
                print("Failed to capture image")
                break
            
            cv2.imshow('Schachbrett Detektor from Main.py', frame)  # Display the frame
            k = cv2.waitKey(1)  # Wait for 1 ms
            
            if k == 13:  # Check if 'Enter' key (which has ASCII code 13) is pressed
                print("Enter pressed, continuing...")
                break
        loop =True
        while loop:
            ret, corners = find_chessboard(frame)
            
            
            print("cornersasd", corners)
            if ret:
                sorted_corners = utilities.sort_corners(corners)
                #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
                outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                sorted_outer_corners = utilities.sort_corners(outer_corners_np)
                loop = False
            else:
                ret, frame = capture_frame(cap)
        print("sorted outer conrenrs", sorted_outer_corners)
        input("Figuren platzieren und Enter um fortzusetzen...")        
        # Durchschnittliche RGB-Werte für jedes Feld am Anfang sammeln

        for _ in range(num_initial_frames):

            for _ in range(5):
                ret, frame = capture_frame(cap)
            
            
            
            
            #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
            cv2.waitKey(100)
            cv2.imshow('Schachbrett Detektor from Main.py', frame)
            cv2.waitKey(100)
            if True:
                chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                pass
        
        
        chess_board.calculate_mean()   
         
        
        input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")

        whiteTurn = True
        count =0
        stockfish.set_fen_position("rnbqk3/8/8/8/8/8/8/3QKBNR w KQkq - 0 1")
        while(True):
            while(True):
                for _ in range(num_update_frames):
                    ret, frame = capture_frame(cap)

                '''loop =True
                while loop:
                    ret, corners = find_chessboard(frame)
                    if ret:
                        loop = False
                    else:
                        frame = capture_frame(cap)'''
                
                #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
                cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
                cv2.imshow('Schachbrett Detektor from Main.py', frame)
                cv2.waitKey(1)
                if True:
                    chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                    pass

                chess_board.calculate_mean() 

                changes = chess_board.find_most_significant_changes()  
                print("changes", changes)
                #move_made = chess_board.update_chessboard(changes, whiteTurn)
                input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")
                whiteTurn = not whiteTurn
            
            for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value} and piece {square.piece}")

            input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")
            whiteTurn = not whiteTurn
            for _ in range(num_update_frames):
                for _ in range(5):
                    frame = capture_frame(cap)
                '''loop =True
                while loop:
                    ret, corners = find_chessboard(frame)
                    if ret:
                        loop = False
                    else:
                        frame = capture_frame(cap)  '''
                
                
                sorted_corners = utilities.sort_corners(corners)
                #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
                outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                sorted_outer_corners = utilities.sort_corners(outer_corners_np)

                #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
                cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
                cv2.imshow('Schachbrett Detektor from Main.py', frame)
                cv2.waitKey(1)
                if True:
                    chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                    pass

            chess_board.calculate_mean() 
            for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value} and piece {square.piece}")

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
