import cv2
import numpy as np

def apply_color_filter(frame):
    # Keeps only white and yellow pixels from frame
    # White and yellow are the only colors used for lane markings
    # HSV color space used because it handles lighting changes better than BGR
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # White lane markings - high brightness low saturation
    white_mask  = cv2.inRange(hsv, np.array([0, 0, 180]),  np.array([255, 35, 255]))

    # Yellow lane markings - hue between 15-35
    yellow_mask = cv2.inRange(hsv, np.array([15, 80, 80]), np.array([35, 255, 255]))

    # Combine both masks
    combined = cv2.bitwise_or(white_mask, yellow_mask)

    # Apply to original frame - only lane colors remain
    return cv2.bitwise_and(frame, frame, mask=combined)
