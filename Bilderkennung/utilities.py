import numpy as np
import cv2

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

def init_camera(frame_width, frame_height, exposure):
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)  # Belichtung einstellen, Wertebereich abhängig von der Kamera
    return cap


def find_chessboard(frame):
    chessboard_size = (7, 7)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    return ret, corners

def capture_frame(cap):
    ret, frame = cap.read()
    return ret, frame

def calc_average_colors(ret, frame, corners):
    framecount = framecounter = 15
    
    cumulative_avg_rgb_values = np.zeros((6, 6, 3), dtype=float) # Summe der durchschnittlichen RGB-Werte
    is_occupied = np.zeros((6, 6), dtype=bool) # Besetzt-Array initalisieren 
    cornersForDrawing = corners
    if ret:
        simplified_corners = sort_corners(corners)  # Now each element is [x, y]

        # Initialize an array to hold the average RGB values for the 49 inner fields
        avg_rgb_values = np.zeros((6, 6, 3), dtype=float)
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
                    else:
                        difference = np.abs(avg_color - final_avg_rgb_values[i, j])
                        print(difference)
                        if np.any(difference > 20):
                            is_occupied[i, j] = True  # Mark the field as occupied
                        else:
                            is_occupied[i, j] = False


        if(framecounter>=0):
            cumulative_avg_rgb_values += avg_rgb_values
        else:
            print("occupied fields")
            print(is_occupied)
        if(framecounter==0):
            final_avg_rgb_values = cumulative_avg_rgb_values / (framecount +1)
            print("final")
            print(final_avg_rgb_values)
        framecounter -=1
        

        cv2.drawChessboardCorners(frame, (7, 7), cornersForDrawing, ret)

    return is_occupied


def display_frame(frame):
    cv2.imshow('Schachbrett Detektor', frame)