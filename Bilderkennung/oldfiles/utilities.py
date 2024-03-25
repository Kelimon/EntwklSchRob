import numpy as np
import cv2

def find_outer_corners(inner_corners, chessboard_size=(7,7)):
    # Reshape the inner corners array for convenience
    inner_corners = inner_corners.reshape(chessboard_size[0], chessboard_size[1], 2)
    
    # Calculate average distances between corners horizontally and vertically
    horizontal_distances = np.diff(inner_corners[:, :, 0], axis=1)
    vertical_distances = np.diff(inner_corners[:, :, 1], axis=0)
    
    avg_horizontal_distance = np.mean(horizontal_distances)
    avg_vertical_distance = np.mean(vertical_distances)
    
    # Initialize an array to store the full set of corners
    full_corners = np.zeros((chessboard_size[0] + 2, chessboard_size[1] + 2, 2))
    
    # Place the inner corners into the full corners array
    full_corners[1:-1, 1:-1] = inner_corners
    
    # Extrapolate the top and bottom row of corners
    full_corners[0, 1:-1] = inner_corners[0] - np.array([[0, avg_vertical_distance]])
    full_corners[-1, 1:-1] = inner_corners[-1] + np.array([[0, avg_vertical_distance]])
    
    # Extrapolate the leftmost and rightmost corners
    full_corners[:, 0] = full_corners[:, 1] - np.array([[avg_horizontal_distance, 0]])
    full_corners[:, -1] = full_corners[:, -2] + np.array([[avg_horizontal_distance, 0]])
    
    # Handle the four corners
    full_corners[0, 0] = full_corners[1, 0] - np.array([[0, avg_vertical_distance]])
    full_corners[-1, 0] = full_corners[-2, 0] + np.array([[0, avg_vertical_distance]])
    full_corners[0, -1] = full_corners[0, -2] - np.array([[avg_horizontal_distance, 0]])
    full_corners[-1, -1] = full_corners[-1, -2] + np.array([[avg_horizontal_distance, 0]])
    
    return full_corners.reshape(-1, 2)

# Example usage:
# inner_corners should be a numpy array of shape (49, 1, 2)
# containing the 49 inner corner positions detected by cv2.findChessboardCorners()



def is_point_in_list(point, points_list):
    return any((point == p).all() for p in points_list)


def sort_corners(corners):
    sorted_rows = []
    
    while len(corners) > 0:
        # Finde den obersten linken Punkt
        corners = corners.reshape(-1, 2)

        sums = corners[:, 0] + corners[:, 1]
        top_left_index = np.argmin(sums)
        top_left_point = corners[top_left_index]
        
        # Finde alle Punkte in der gleichen Reihe
        row_points = [point for point in corners if abs(point[1] - top_left_point[1]) <= 15]
        
        # Sortiere die Punkte in der Reihe nach ihrer X-Koordinate
        row_points_sorted = sorted(row_points, key=lambda x: x[0])
        
        # Füge die sortierte Reihe zu `sorted_rows` hinzu
        sorted_rows.append(row_points_sorted)
        
        # Entferne die verarbeiteten Punkte
        corners = np.array([point for point in corners if not is_point_in_list(point, row_points_sorted)])

    
    # Konvertiere `sorted_rows` in ein einziges Array für die Ausgabe
    sorted_corners = np.vstack(sorted_rows)
    return sorted_corners


def is_occupied(color_value, color_range):
    return not(color_range['b'][0] <= color_value[0] <= color_range['b'][1] and
               color_range['g'][0] <= color_value[1] <= color_range['g'][1] and
               color_range['r'][0] <= color_value[2] <= color_range['r'][1])



def calc_average_colors(ret, frame, corners, framecount, framecounter):
    
    
    cumulative_avg_rgb_values = np.zeros((6, 6, 3), dtype=float) # Summe der durchschnittlichen RGB-Werte
    is_occupied = np.zeros((6, 6), dtype=bool) # Besetzt-Array initalisieren 
    cornersForDrawing = corners
    if ret:
        simplified_corners = sort_corners(corners)  # Now each element is [x, y]

        # Initialize an array to hold the average RGB values for the 49 inner fields
        avg_rgb_values = np.zeros((6, 6, 3), dtype=float)
        final_avg_rgb_values = np.zeros((6, 6, 3), dtype=float)
        for i in range(6):
                for j in range(6):
                    # Define the four corners of the current field using simplified corners
                    top_left = simplified_corners[i * 7 + j]
                    top_right = simplified_corners[i * 7 + (j + 1)]
                    bottom_left = simplified_corners[(i + 1) * 7 + j]
                    bottom_right = simplified_corners[(i + 1) * 7 + (j + 1)]

                    # Compute the bounding rectangle of the current field
                    x_min = int(min(top_left[0], bottom_left[0], top_right[0], bottom_right[0]))
                    x_max = int(max(top_left[0], bottom_left[0], top_right[0], bottom_right[0]))
                    y_min = int(min(top_left[1], bottom_left[1], top_right[1], bottom_right[1]))
                    y_max = int(max(top_left[1], bottom_left[1], top_right[1], bottom_right[1]))

                    # Extract the region of interest (ROI) from the frame
                    field_roi = frame[y_min:y_max, x_min:x_max]

                    # Calculate the average color within this ROI
                    avg_color = np.mean(field_roi, axis=(0, 1))
            
                    if(framecounter>=0):
                        avg_rgb_values[i, j] = avg_color
                        print("avgrgbvalues", avg_rgb_values)
                        print("avgcolor is", avg_color)
                        print("framecounter", framecounter)
                    else:
                        difference = np.abs(avg_color - final_avg_rgb_values[i, j])
                        
                        if np.any(difference > 20):
                            is_occupied[i, j] = True  # Mark the field as occupied
                        else:
                            is_occupied[i, j] = False

        print("avgrgbvalues", avg_rgb_values)
        print("isoccupied", is_occupied)
        print("framecounter", framecounter)
        print("framecount", framecount)
        print("cumulative_avg_rgb_values", cumulative_avg_rgb_values)
        print("final_avg_rgb_values", final_avg_rgb_values)
        if(framecounter>=0):
            cumulative_avg_rgb_values += avg_rgb_values
        if(framecounter==0):
            final_avg_rgb_values = cumulative_avg_rgb_values / (framecount +1)

        
        

        cv2.drawChessboardCorners(frame, (7, 7), cornersForDrawing, ret)

    return is_occupied


def display_frame(frame):
    cv2.imshow('Schachbrett Detektor', frame)


class ChessSquare:
    def __init__(self, position, piece='-', mean_rgb_value=None, status='empty'):
        self.position = position        # The position on the board, e.g., 'a1', 'd4', etc.
        self.piece = piece              # The piece on the square: 'P', 'p', 'R', 'r', etc., or '-' for empty
        self.mean_rgb_value = mean_rgb_value  # The mean RGB value of the square
        self.status = status            # The status of the square: 'empty', 'occupied', etc.

# Initialize a dictionary with the starting piece positions
starting_pieces = {
    'a1': 'R', 'b1': 'N', 'c1': 'B', 'd1': 'Q', 'e1': 'K', 'f1': 'B', 'g1': 'N', 'h1': 'R',
    'a2': 'P', 'b2': 'P', 'c2': 'P', 'd2': 'P', 'e2': 'P', 'f2': 'P', 'g2': 'P', 'h2': 'P',
    'a7': 'p', 'b7': 'p', 'c7': 'p', 'd7': 'p', 'e7': 'p', 'f7': 'p', 'g7': 'p', 'h7': 'p',
    'a8': 'r', 'b8': 'n', 'c8': 'b', 'd8': 'q', 'e8': 'k', 'f8': 'b', 'g8': 'n', 'h8': 'r'
}

# Create a list of all board positions
chess_positions = [f"{chr(file)}{rank}" for rank in range(1, 9) for file in range(ord('a'), ord('h')+1)]

# Initialize the board with ChessSquare objects
board = [ChessSquare(position, starting_pieces.get(position, '-')) for position in chess_positions]
print(board)