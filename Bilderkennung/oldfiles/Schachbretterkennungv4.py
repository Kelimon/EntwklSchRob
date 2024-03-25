import sys
import cv2
import numpy as np
import time
import utilities
import subprocess
from stockfish import Stockfish

stockfish = Stockfish(path="./../stockfish/stockfish-windows-x86-64-avx2.exe")
print(stockfish.is_fen_valid("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"))
stockfish.set_fen_position("rnbqkbnr/pppp1ppp/4p3/8/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2")
print(stockfish.get_board_visual())
print(stockfish.get_best_move_time(1000))
stockfish.make_moves_from_current_position(["b2b4"])
print(stockfish.get_board_visual())
stockfish.make_moves_from_current_position(["b7b5"])
print(stockfish.get_board_visual())

# init camera 
cap = utilities.init_camera(frame_width=1920, frame_height=1080, exposure=-6.5)


framecount = framecounter = 15
while True:
    image_path = './chessboard.jpg'  # Update this to the path of your image
    frame = cv2.imread(image_path)
    #ret, frame = utilities.capture_frame(cap)
    #if not ret:
     #   print("Fehler beim Erfassen des Bildes")
      #  break

    ret, corners = utilities.find_chessboard(frame)
    
    is_occupied = utilities.calc_average_colors(ret, frame, corners, framecount, framecounter)
    framecounter -=1
    utilities.display_frame(frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
