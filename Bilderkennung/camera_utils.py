import numpy as np
import cv2
import time

def init_camera(frame_width, frame_height, exposure, brightness=0.5):
    start_time = time.time()
    """
    Initializes the camera with specified frame width, height, and exposure.
    """
    print("Initializing camera with frame width: {}, frame height: {}, exposure: {}".format(frame_width, frame_height, exposure))
    print("0 Camera initialized in {} seconds".format(time.time() - start_time))
    cap = cv2.VideoCapture(1,  cv2.CAP_DSHOW)
    print("hello?")
    if not cap.isOpened():
        raise IOError("Cannot open webcam")
    print("1  Camera initialized in {} seconds".format(time.time() - start_time))
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, frame_width)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, frame_height)
    cap.set(cv2.CAP_PROP_EXPOSURE, 6)  # Manchmal funktioniert automatische Belichtung besser

    # cap.set(cv2.CAP_PROP_EXPOSURE, exposure)
    # cap.set(cv2.CAP_PROP_BRIGHTNESS, brightness)
    print("2  Camera initialized in {} seconds".format(time.time() - start_time))
    
    return cap

def capture_frame(cap, blue_enhance_factor=2):
    """
    Captures a single frame from the camera and enhances the blue channel.
    """
    ret, frame = cap.read()
    if not ret:
        raise IOError("Failed to capture image")
    print("frame davor", frame)
    cv2.imshow('Schachbrett Detektor from camerautils before blue.py', frame)
    cv2.waitKey(1)  # Wait indefinitely until a key is pressed
    # Enhance blue channel
    if blue_enhance_factor != 1:
        frame[:, :, 0] = cv2.multiply(frame[:, :, 0], np.array([blue_enhance_factor], dtype=np.float32))
        frame[:, :, 0] = np.clip(frame[:, :, 0], 0, 255)  # Ensure the pixel values are valid
    print("frame danach,", frame)
    return ret, frame

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

