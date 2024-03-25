import numpy as np
import cv2

def init_camera(frame_width, frame_height, exposure):
    """
    Initializes the camera with specified frame width, height, and exposure.
    """
    print("Initializing camera with frame width: {}, frame height: {}, exposure: {}".format(frame_width, frame_height, exposure))

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
    cv2.imshow('Schachbrett Detektor', frame)

    return frame

def find_chessboard(frame, chessboard_size=(7, 7)):
    """
    Finds the corners of the chessboard in the frame.
    """
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)
    print("Found chessboard: {}".format(ret))
    if ret:
        criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        corners2 = cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)
        cv2.drawChessboardCorners(frame, chessboard_size, corners2, ret)
        cv2.imshow('Schachbrett Detektor', frame)
        cv2.waitKey(1)
        return True, corners2
    return False, None

def release_camera(cap):
    """
    Releases the camera resource.
    """
    cap.release()

