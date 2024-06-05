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
    
    corners = np.array([[[ 674.9414, 132.0072 ]],

 [[ 784.16626,132.47375]],

 [[ 893.8419, 132.84785]],

 [[1003.1698, 133.9816 ]],

 [[1112.9513, 133.78336]],

 [[1219.3812, 135.33723]],

 [[1325.8892, 138.6396 ]],

 [[ 672.2646, 238.39056]],

 [[ 782.3657, 239.41882]],

 [[ 892.9576, 240.22894]],

 [[1002.8758, 240.52362]],

 [[1113.6095, 240.54573]],

 [[1220.8772, 241.9711 ]],

 [[1328.7294, 244.44255]],

 [[ 670.24695,347.3573 ]],

 [[ 780.60657,347.9345 ]],

 [[ 891.915,348.30582]],

 [[1002.6209, 349.46118]],

 [[1113.6495, 349.80408]],

 [[1221.5265, 351.02612]],

 [[1330.5553, 352.43802]],

 [[ 668.4793, 457.64517]],

 [[ 778.7615, 457.79797]],

 [[ 890.9153, 458.69824]],

 [[1002.301,459.6413 ]],

 [[1113.7141, 460.1171 ]],

 [[1222.152,460.6219 ]],

 [[1331.5875, 461.91208]],

 [[ 666.3489, 568.549]],

 [[ 777.6193, 569.2939 ]],

 [[ 889.8745, 570.06903]],

 [[1001.9109, 570.7284 ]],

 [[1113.8674, 571.25836]],

 [[1223.3599, 571.6416 ]],

 [[1332.9232, 572.4336 ]],

 [[ 664.6886, 680.9126 ]],

 [[ 776.53625,681.7787 ]],

 [[ 889.42084,682.5111 ]],

 [[1001.5617, 683.17993]],

 [[1114.3564, 683.9064 ]],

 [[1224.3041, 683.7701 ]],

 [[1334.1848, 684.05206]],

 [[ 663.2061, 793.73157]],

 [[ 775.7352, 794.5195 ]],

 [[ 888.6136, 795.4644 ]],

 [[1001.297,795.91473]],

 [[1114.3506, 796.8351 ]],

 [[1224.7628, 796.7002 ]],

 [[1335.8337, 796.316  ]]])
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
         
        
        

        whiteTurn = True
        count = 0
        stockfish.set_fen_position("rnbqk3/8/8/8/8/8/8/3QKBNR w KQkq - 0 1")
        while(True):
            
            print(stockfish.get_board_visual())
            best_move = stockfish.get_best_move()
            stockfish.make_move(best_move)
            print(stockfish.get_board_visual())
            print(f"Der beste Zug ist: {best_move}")
            input("Drücken Sie Enter, nachdem der von Stockfish genannte Zug gemacht wurde...")
            for _ in range(num_update_frames):
                for _ in range(5):
                    frame = capture_frame(cap)

            '''loop =True
            while loop:
                ret, corners = find_chessboard(frame)
                if ret:
                    loop = False
                else:
                    frame = capture_frame(cap)'''
            for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value} and piece {square.piece}")
            
            
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
            '''for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value}")'''

            changes = chess_board.find_most_significant_changes()  
            print("changes", changes)
            move_made = chess_board.update_chessboard(changes, whiteTurn)
            
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
