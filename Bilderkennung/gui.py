import tkinter as tk
from tkinter import messagebox
from chess_logic import ChessBoard
from camera_utils import init_camera, capture_frame, find_chessboard
from main_with_stockfish import main

class ChessApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Chess Robot Control")
        self.create_widgets()

    def create_widgets(self):
        # Eingabefeld für das Elo-Rating
        self.elo_rating = tk.StringVar(value="1200")
        tk.Label(self.root, text="Elo Rating:").grid(row=0, column=0, padx=10, pady=10)
        tk.Entry(self.root, textvariable=self.elo_rating, width=50).grid(row=0, column=1, padx=10, pady=10)

        # Dropdown-Menü für den Skilllevel
        self.skill_level = tk.IntVar(value=1)
        skill_levels = list(range(1, 21))  # Erstellt eine Liste von 1 bis 20
        tk.Label(self.root, text="Skill Level:").grid(row=1, column=0, padx=10, pady=10)
        skill_menu = tk.OptionMenu(self.root, self.skill_level, *skill_levels)
        skill_menu.grid(row=1, column=1, padx=10, pady=10)

        # Button zum Starten des Spiels
        tk.Button(self.root, text="Start Game", command=self.start_game).grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # Konsolentextfeld für Ausgaben
        self.console = tk.Text(self.root, width=100, height=20)
        self.console.grid(row=3, column=0, columnspan=2, padx=10, pady=10)


    def start_game(self):
        elo_rating = self.elo_rating.get()  # Retrieve the Elo rating from the entry widget
        skill_level = self.skill_level.get()  # Retrieve the skill level from the option menu
        main(skill_level=int(skill_level), elo_rating=int(elo_rating))  # Call main with parameters


    def log(self, message):
        self.console.insert(tk.END, message + "\n")
        self.console.see(tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = ChessApp(root)
    root.mainloop()
