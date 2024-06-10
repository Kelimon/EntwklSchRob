import cv2
from camera_utils import init_camera, capture_frame, find_chessboard
from chess_logic import ChessBoard
from stockfish_integration import StockfishIntegration
import utilities
import numpy as np
import serial
import time


arduino = serial.Serial(port='/dev/ttyACM0', baudrate=9600, timeout=.1)
time.sleep(2)  # Warte, bis die serielle Verbindung hergestellt ist

def write_read(command):
    arduino.write(bytes(command + '\n', 'utf-8'))
    while True:
        data = arduino.readline().decode('utf-8').rstrip()
        print("data", data)
        if data == "done":
            break
    return data

def main(skill_level, elo_rating):
 
    # Kameraeinstellungen (Diese Werte sollten angepasst werden)
    frame_width = 1920
    frame_height = 1080
    exposure = 6

    # Pfad zu Stockfish aktualisieren
    stockfish_path = "./stockfish/stockfish-windows-x86-64-avx2.exe"
    stockfish = StockfishIntegration(stockfish_path, skill_level=skill_level, elo_rating=elo_rating)
    

    # Kamera initialisieren
    cap = init_camera(frame_width, frame_height, exposure)
    
    # Schachbrett initialisieren
    chess_board = ChessBoard()
    chess_board.initialize_board()

    # Anzahl der Frames zum Sammeln von Durchschnittswerten
    num_initial_frames = 10
    num_update_frames = 3
   
    sorted_outer_corners = None
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
        sort_and_extrapolate_corners(frame, cap)


        input("Figuren platzieren und Enter um fortzusetzen...")        

        update_RGB_values(cap, sorted_outer_corners, chess_board) 
        
        whiteTurn = True
        count =0
        stockfish.set_fen_position("rnbqk3/8/8/8/8/8/8/3QKBNR w KQkq - 0 1")
        while(True):
            input("Drücken Sie Enter, nachdem ein Zug gemacht wurde...")

            update_RGB_values(cap, sorted_outer_corners, chess_board) 
            changes = chess_board.find_most_significant_changes()  

            move_made = chess_board.update_chessboard(changes, whiteTurn)
            stockfish.make_move(move_made)
            best_move = stockfish.get_best_move()
            stockfish.make_move(best_move)
            write_read(best_move)

            update_RGB_values(cap, sorted_outer_corners, chess_board) 

            count+=1


    except Exception as e:
        print(f"Ein Fehler ist aufgetreten: {e}")
    finally:
        # Kamera freigeben
        #cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    main()



def update_RGB_values(cap, sorted_outer_corners, chess_board):
    for _ in range(4):
        for _ in range(3):
            frame = capture_frame(cap)   

            cv2.drawChessboardCorners(frame, (9,9), sorted_outer_corners,  True)
            cv2.imshow('Schachbrett Detektor from Main.py', frame)
            cv2.waitKey(1)
            chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)

        chess_board.calculate_mean() 

      
def sort_and_extrapolate_corners(frame, cap):
    loop =True
    while loop:
        ret, corners = find_chessboard(frame)
        if ret:
            sorted_corners = utilities.sort_corners(corners)
            #print("outercoernsers",utilities.find_outer_corners(inner_corners=sorted_corners)).reshape(-1, 1, 2)
            outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
            outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
            sorted_outer_corners = utilities.sort_corners(outer_corners_np)
            loop = False
        else:
            ret, frame = capture_frame(cap)
    return sorted_outer_corners





'''for square in chess_board.squares:
                print(f"position {square.position} has mean rgb {square.mean_rgb_value} and last rgb {square.last_rgb_value} and piece {square.piece}")'''