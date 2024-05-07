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
    num_initial_frames = 20
    num_update_frames = 5
    
    corners = np.array([[[ 647.0712,232.02425]],

 [[ 739.4819,228.35521]],

 [[ 834.1669,224.77872]],

 [[ 929.33923,  220.82657]],

 [[1026.0697,215.3635 ]],

 [[1126.8667,212.31221]],

 [[1224.2217,212.54715]],

 [[ 646.01074 , 324.5525 ]],

 [[ 739.31604,  321.4727 ]],

 [[ 834.45685 , 318.68585]],

 [[ 930.07025 , 315.68277]],

 [[1027.5708,311.4062 ]],

 [[1127.8978,309.3516 ]],

 [[1226.7626,308.17816]],

 [[ 645.6104,419.0477 ]],

 [[ 738.89935 , 416.74258]],

 [[ 834.08575,  414.222  ]],

 [[ 931.23486 , 412.25342]],

 [[1029.1982,409.3813 ]],

 [[1128.7009,408.11462]],

 [[1228.6074,406.1022 ]],

 [[ 645.82513 , 514.8506 ]],

 [[ 738.70044 , 513.07227]],

 [[ 835.2613,511.5421 ]],

 [[ 932.1856,509.59543]],

 [[1030.5969,508.1064 ]],

 [[1129.3817,505.882  ]],

 [[1229.8591,505.74414]],

 [[ 644.89496 , 609.60815]],

 [[ 739.23987 , 609.169  ]],

 [[ 835.5949,608.40234]],

 [[ 932.7306,607.5327 ]],

 [[1031.7302,606.06885]],

 [[1131.0094,604.78064]],

 [[1232.2039,605.54236]],

 [[ 645.171, 706.92096]],

 [[ 739.8678,706.66187]],

 [[ 836.57434 , 706.26794]],

 [[ 932.89734 , 707.2751 ]],

 [[1032.3875,706.8548 ]],

 [[1133.187, 706.3839 ]],

 [[1233.9265,706.4007 ]],

 [[ 645.3948,803.7289 ]],

 [[ 741.34515 , 804.50104]],

 [[ 836.7894,805.4356 ]],

 [[ 933.8482,806.77563]],

 [[1033.7184,808.10614]],

 [[1133.2488,807.34515]],

 [[1235.4996,808.04584]]])
    
    sorted_corners = utilities.sort_corners(corners)
    #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
    outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
    outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
    sorted_outer_corners = utilities.sort_corners(outer_corners_np)
    try:
        # Durchschnittliche RGB-Werte für jedes Feld am Anfang sammeln
        for _ in range(num_initial_frames):

            for _ in range(5):
                frame = capture_frame(cap)

            '''loop =True
            while loop:
                ret, corners = find_chessboard(frame)
                if ret:
                    loop = False
                else:
                    frame = capture_frame(cap)'''

            print("corners", corners)
            
            #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
            cv2.imshow('Schachbrett Detektor from Main.py', frame)
            cv2.waitKey(1)
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
                    frame = capture_frame(cap)

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
                move_made = chess_board.update_chessboard(changes, whiteTurn)
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
