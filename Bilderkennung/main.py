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

            frame = capture_frame(cap)

            loop =True
            while loop:
                ret, corners = find_chessboard(frame)
                if ret:
                    loop = False
                else:
                    frame = capture_frame(cap)

            print("corers", corners)
            corners = np.array([[[ 701.8246,   173.36533]],

                        [[ 806.8595,173.47919]],

                        [[ 912.3768,173.65321]],

                        [[1017.284, 173.23338]],

                        [[1122.6084,172.30168]],

                        [[1222.1971,173.49107]],

                        [[1323.7113,176.29523]],

                        [[ 700.35657 , 275.71436]],

                        [[ 806.50543 , 276.63226]],

                        [[ 912.4277,276.48804]],

                        [[1017.8852,276.38388]],

                        [[1124.243, 275.34583]],

                        [[1224.4879,276.81076]],

                        [[1326.7607,278.45776]],

                        [[ 699.7207,381.30164]],

                        [[ 805.8928,380.91342]],

                        [[ 912.6859,381.30862]],

                        [[1018.64545 , 380.95102]],

                        [[1125.8291,379.27478]],

                        [[1226.5292,381.6042 ]],

                        [[1329.7765,382.26358]],

                        [[ 699.0343,487.15573]],

                        [[ 805.38464 , 486.47314]],

                        [[ 912.66547 , 486.7469 ]],

                        [[1019.4409,486.56635]],

                        [[1126.8643,485.69348]],

                        [[1228.9943,487.11768]],

                        [[1332.6669,487.1694 ]],

                        [[ 697.70166,  593.8747 ]],

                        [[ 804.9876,593.79626]],

                        [[ 912.8128,593.5829 ]],

                        [[1020.20416  ,593.4082 ]],

                        [[1128.164, 592.7953 ]],

                        [[1231.5466,593.64984]],

                        [[1335.6433,592.95483]],

                        [[ 696.49133 , 702.21466]],

                        [[ 804.7134,701.8104 ]],

                        [[ 913.19037 , 701.5051 ]],

                        [[1020.93713 , 701.33136]],

                        [[1129.6667,701.3689 ]],

                        [[1233.3845,701.4188 ]],

                        [[1338.5085,699.9574 ]],

                        [[ 695.683, 811.3356 ]],

                        [[ 804.6088,810.62103]],

                        [[ 913.39545 , 810.3163 ]],

                        [[1021.77344 , 810.24414]],

                        [[1130.7031,809.9695 ]],

                        [[1235.7031,809.82336]],

                        [[1341.1024,807.63086]]])
            print("corners", corners)
            sorted_corners = utilities.sort_corners(corners)
            #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
            outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
            outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
            sorted_outer_corners = utilities.sort_corners(outer_corners_np)
            
            #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
            cv2.imshow('Schachbrett Detektor', frame)
            cv2.waitKey(1)
            if True:
                chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
                pass
        
        
        chess_board.calculate_mean()   
         
        
        

        whiteTurn = True
        count =0
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
            corners = np.array([[[ 701.8246,   173.36533]],

                        [[ 806.8595,173.47919]],

                        [[ 912.3768,173.65321]],

                        [[1017.284, 173.23338]],

                        [[1122.6084,172.30168]],

                        [[1222.1971,173.49107]],

                        [[1323.7113,176.29523]],

                        [[ 700.35657 , 275.71436]],

                        [[ 806.50543 , 276.63226]],

                        [[ 912.4277,276.48804]],

                        [[1017.8852,276.38388]],

                        [[1124.243, 275.34583]],

                        [[1224.4879,276.81076]],

                        [[1326.7607,278.45776]],

                        [[ 699.7207,381.30164]],

                        [[ 805.8928,380.91342]],

                        [[ 912.6859,381.30862]],

                        [[1018.64545 , 380.95102]],

                        [[1125.8291,379.27478]],

                        [[1226.5292,381.6042 ]],

                        [[1329.7765,382.26358]],

                        [[ 699.0343,487.15573]],

                        [[ 805.38464 , 486.47314]],

                        [[ 912.66547 , 486.7469 ]],

                        [[1019.4409,486.56635]],

                        [[1126.8643,485.69348]],

                        [[1228.9943,487.11768]],

                        [[1332.6669,487.1694 ]],

                        [[ 697.70166,  593.8747 ]],

                        [[ 804.9876,593.79626]],

                        [[ 912.8128,593.5829 ]],

                        [[1020.20416  ,593.4082 ]],

                        [[1128.164, 592.7953 ]],

                        [[1231.5466,593.64984]],

                        [[1335.6433,592.95483]],

                        [[ 696.49133 , 702.21466]],

                        [[ 804.7134,701.8104 ]],

                        [[ 913.19037 , 701.5051 ]],

                        [[1020.93713 , 701.33136]],

                        [[1129.6667,701.3689 ]],

                        [[1233.3845,701.4188 ]],

                        [[1338.5085,699.9574 ]],

                        [[ 695.683, 811.3356 ]],

                        [[ 804.6088,810.62103]],

                        [[ 913.39545 , 810.3163 ]],

                        [[1021.77344 , 810.24414]],

                        [[1130.7031,809.9695 ]],

                        [[1235.7031,809.82336]],

                        [[1341.1024,807.63086]]])
            
            sorted_corners = utilities.sort_corners(corners)
            #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
            outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
            outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
            sorted_outer_corners = utilities.sort_corners(outer_corners_np)

            #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
            cv2.imshow('Schachbrett Detektor', frame)
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
                
                corners = np.array([[[ 701.8246,   173.36533]],

                        [[ 806.8595,173.47919]],

                        [[ 912.3768,173.65321]],

                        [[1017.284, 173.23338]],

                        [[1122.6084,172.30168]],

                        [[1222.1971,173.49107]],

                        [[1323.7113,176.29523]],

                        [[ 700.35657 , 275.71436]],

                        [[ 806.50543 , 276.63226]],

                        [[ 912.4277,276.48804]],

                        [[1017.8852,276.38388]],

                        [[1124.243, 275.34583]],

                        [[1224.4879,276.81076]],

                        [[1326.7607,278.45776]],

                        [[ 699.7207,381.30164]],

                        [[ 805.8928,380.91342]],

                        [[ 912.6859,381.30862]],

                        [[1018.64545 , 380.95102]],

                        [[1125.8291,379.27478]],

                        [[1226.5292,381.6042 ]],

                        [[1329.7765,382.26358]],

                        [[ 699.0343,487.15573]],

                        [[ 805.38464 , 486.47314]],

                        [[ 912.66547 , 486.7469 ]],

                        [[1019.4409,486.56635]],

                        [[1126.8643,485.69348]],

                        [[1228.9943,487.11768]],

                        [[1332.6669,487.1694 ]],

                        [[ 697.70166,  593.8747 ]],

                        [[ 804.9876,593.79626]],

                        [[ 912.8128,593.5829 ]],

                        [[1020.20416  ,593.4082 ]],

                        [[1128.164, 592.7953 ]],

                        [[1231.5466,593.64984]],

                        [[1335.6433,592.95483]],

                        [[ 696.49133 , 702.21466]],

                        [[ 804.7134,701.8104 ]],

                        [[ 913.19037 , 701.5051 ]],

                        [[1020.93713 , 701.33136]],

                        [[1129.6667,701.3689 ]],

                        [[1233.3845,701.4188 ]],

                        [[1338.5085,699.9574 ]],

                        [[ 695.683, 811.3356 ]],

                        [[ 804.6088,810.62103]],

                        [[ 913.39545 , 810.3163 ]],

                        [[1021.77344 , 810.24414]],

                        [[1130.7031,809.9695 ]],

                        [[1235.7031,809.82336]],

                        [[1341.1024,807.63086]]])
                sorted_corners = utilities.sort_corners(corners)
                #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
                outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                sorted_outer_corners = utilities.sort_corners(outer_corners_np)

                #print("outercorenrsreshape", outer_corners.reshape(-1, 1, 2))
                cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
                cv2.imshow('Schachbrett Detektor', frame)
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
