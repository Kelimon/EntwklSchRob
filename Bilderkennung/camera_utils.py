import numpy as np
import cv2

def init_camera(frame_width, frame_height, exposure, brightness=0.5):
    """
    Initializes the camera with specified frame width, height, and exposure.
    """
    print("Initializing camera with frame width: {}, frame height: {}, exposure: {}".format(frame_width, frame_height, exposure))

    cap = cv2.VideoCapture(1)
    print("hello?")
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    
    return cap

def capture_frame(cap):
    """
    Captures a single frame from the camera.
    """
    ret, frame = cap.read()
    if not ret:
        raise IOError("Failed to capture image")
    frame =adjust_brightness_and_contrast(frame, brightness=0, contrast=0)
    return frame

def adjust_brightness_and_contrast(frame, brightness=0, contrast=0):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow
        
        buf = cv2.addWeighted(frame, alpha_b, frame, 0, gamma_b)
    else:
        buf = frame.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)
        
        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf

def find_chessboard(frame, chessboard_size=(7, 7)):
    """
    Finds the corners of the chessboard in the frame.
    """
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(frame, chessboard_size, None)


    
    

    print("Found chessboard: {}".format(ret))
    if ret:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        return True, corners2
    return False, None

def release_camera(cap):
    """
    Releases the camera resource.
    """
    cap.release()

