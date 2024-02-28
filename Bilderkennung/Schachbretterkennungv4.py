import sys
import cv2
import numpy as np
import time
import utilities

# init camera 
cap = utilities.init_camera(frame_width=1920, frame_height=1080, exposure=-6.5)

while True:
    ret, frame = utilities.capture_frame(cap)
    if not ret:
        print("Fehler beim Erfassen des Bildes")
        break

    ret, corners = utilities.find_chessboard(frame)
    is_occupied = utilities.calc_average_colors(ret, frame, corners)

    utilities.display_frame()
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
