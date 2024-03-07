import numpy as np
import cv2

def init_camera(frame_width, frame_height, exposure):
    """
    Initializes the camera with specified frame width, height, and exposure.
    """
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    
    return cap

def capture_frame(cap):
    """
    Captures a single frame from the camera.
    """
    ret, frame = cap.read()
    if not ret:
        raise IOError("Failed to capture image")
    return frame

def find_chessboard(frame, chessboard_size=(7, 7)):
    """
    Finds the corners of the chessboard in the frame.
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    
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

