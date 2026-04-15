import cv2
import numpy as np
from lane_modules.color_filter import apply_color_filter

def preprocess(frame, thresh=180):
    # Full preprocessing pipeline before sliding window
    # Color filter -> Grayscale -> Blur -> Binary threshold -> Morphological closing
    # Output: clean binary image with lane pixels white, everything else black

    # Step 1: Color filter - isolate white and yellow lane pixels only
    filtered = apply_color_filter(frame)

    # Step 2: Grayscale - remove color, keep brightness structure
    gray = cv2.cvtColor(filtered, cv2.COLOR_BGR2GRAY)

    # Step 3: Gaussian blur - smooths noise before thresholding
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    # Step 4: Binary threshold - pure black and white output
    # Lane markings = bright = white, everything else = black
    # Cleaner input for sliding window than Canny alone
    _, binary = cv2.threshold(blur, thresh, 255, cv2.THRESH_BINARY)

    # Step 5: Morphological closing - fills small gaps in dashed lane lines
    # Connects broken dashes into more continuous lines
    # Helps sliding window find enough pixels per window
    kernel = np.ones((3, 3), np.uint8)
    binary = cv2.morphologyEx(binary, cv2.MORPH_CLOSE, kernel)

    return binary
