import tkinter as tk
from tkinter import messagebox
import cv2
from camera_utils import init_camera, capture_frame, find_chessboard
from chess_logic import ChessBoard
import utilities

import numpy as np


class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Robot Control")

        self.stockfish_path = tk.StringVar(value="./stockfish/stockfish-windows-x86-64-avx2.exe")

        tk.Label(root, text="Stockfish Path:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(root, textvariable=self.stockfish_path, width=50).grid(row=0, column=1, padx=10, pady=10)
        tk.Button(root, text="Start Game", command=self.start_game).grid(row=1, column=0, columnspan=2, padx=10, pady=10)

        self.console = tk.Text(root, width=100, height=20)
        self.console.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

    def start_game(self):
        self.log("Starting game...")
       

        # Kameraeinstellungen (Diese Werte sollten angepasst werden)
        frame_width = 1920
        frame_height = 1080
        exposure = 6

        # Kamera initialisieren
        cap = init_camera(frame_width, frame_height, exposure)
        self.log("Camera initialized")

        # Schachbrett initialisieren
        chess_board = ChessBoard()
        chess_board.initialize_board()
        self.log("Chessboard initialized")

        # Anzahl der Frames zum Sammeln von Durchschnittswerten
        num_initial_frames = 10
        num_update_frames = 3
        
        try:
            while True:
                ret, frame = capture_frame(cap)  # Read a frame from the camera
                if not ret:
                    self.log("Failed to capture image")
                    break
                
                cv2.imshow('Schachbrett Detektor from Main.py', frame)  # Display the frame
                k = cv2.waitKey(1)  # Wait for 1 ms
                
                if k == 13:  # Check if 'Enter' key (which has ASCII code 13) is pressed
                    self.log("Enter pressed, continuing...")
                    break

            loop = True
            while loop:
                ret, corners = find_chessboard(frame)
                if ret:
                    sorted_corners = utilities.sort_corners(corners)
                    outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                    outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                    sorted_outer_corners = utilities.sort_corners(outer_corners_np)
                    loop = False
                else:
                    ret, frame = capture_frame(cap)
            self.log("Sorted outer corners found")
            messagebox.showinfo("Info", "Place pieces and press OK to continue...")

            for _ in range(num_initial_frames):
                for _ in range(5):
                    ret, frame = capture_frame(cap)
                
                cv2.drawChessboardCorners(frame, (9, 9), sorted_outer_corners, True)
                cv2.waitKey(100)
                cv2.imshow('Schachbrett Detektor from Main.py', frame)
                cv2.waitKey(100)
                if True:
                    chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)
        
            chess_board.calculate_mean()
            messagebox.showinfo("Info", "Press OK after a move is made...")

            whiteTurn = True
            count = 0
         

            while True:
                for _ in range(num_update_frames):
                    ret, frame = capture_frame(cap)

                    cv2.drawChessboardCorners(frame, (9, 9), sorted_outer_corners, True)
                    cv2.imshow('Schachbrett Detektor from Main.py', frame)
                    cv2.waitKey(1)
                    if True:
                        chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)

                    chess_board.calculate_mean()

                    changes = chess_board.find_most_significant_changes()
                    self.log(f"Changes: {changes}")
                    messagebox.showinfo("Info", "Press OK after a move is made...")
                    whiteTurn = not whiteTurn

                for square in chess_board.squares:
                    self.log(f"Position {square.position} has mean RGB {square.mean_rgb_value} and last RGB {square.last_rgb_value} and piece {square.piece}")

                messagebox.showinfo("Info", "Press OK after a move is made...")
                whiteTurn = not whiteTurn

                for _ in range(num_update_frames):
                    for _ in range(5):
                        frame = capture_frame(cap)

                    sorted_corners = utilities.sort_corners(corners)
                    outer_corners = utilities.find_outer_corners(inner_corners=sorted_corners)
                    outer_corners_np = np.array(outer_corners, dtype=np.float32).reshape(-1, 1, 2)
                    sorted_outer_corners = utilities.sort_corners(outer_corners_np)

                    cv2.drawChessboardCorners(frame, (9, 9), sorted_outer_corners, True)
                    cv2.imshow('Schachbrett Detektor from Main.py', frame)
                    cv2.waitKey(1)
                    if True:
                        chess_board.calculate_average_rgb_for_each_square(frame, corners=sorted_outer_corners)

                chess_board.calculate_mean()

                for square in chess_board.squares:
                    self.log(f"Position {square.position} has mean RGB {square.mean_rgb_value} and last RGB {square.last_rgb_value} and piece {square.piece}")

                changes = chess_board.find_most_significant_changes()

                move_made = chess_board.update_chessboard(changes, whiteTurn)
                self.log(f"Move made: {move_made}")
              

                count += 1

        except Exception as e:
            self.log(f"An error occurred: {e}")
        finally:
            cv2.destroyAllWindows()

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
