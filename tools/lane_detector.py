import sys
import os
sys.path.insert(0, os.path.dirname(__file__))
from lane_modules.preprocessor    import preprocess
from lane_modules.roi_calibrator  import auto_calibrate
from lane_modules.sliding_window  import run_sliding_window
from lane_modules.lane_fitter     import fit_polynomial, poly_to_line, apply_temporal_persistence
from lane_modules.ldw             import check_departure, draw_ldw_warning, draw_lane_fill
import cv2
import numpy as np

class LaneDetector:
    # Main coordinator class - ties all lane detection modules together
    # Each algorithm lives in its own module file
    # This class only contains function calls and state management
    # Modular design allows swapping any algorithm without touching others

    def __init__(self, sensitivity="medium"):
        # Initializes detector with tunable sensitivity settings
        sensitivity_map = {
            "low":    {"n_windows": 9,  "margin": 100, "minpix": 50,  "thresh": 200},
            "medium": {"n_windows": 12, "margin": 80,  "minpix": 30,  "thresh": 180},
            "high":   {"n_windows": 15, "margin": 60,  "minpix": 15,  "thresh": 150},
        }
        params = sensitivity_map.get(sensitivity, sensitivity_map["medium"])
        self.n_windows  = params["n_windows"]
        self.margin     = params["margin"]
        self.minpix     = params["minpix"]
        self.thresh     = params["thresh"]

        # Lane state
        self.left_fit    = None
        self.right_fit   = None
        self.left_lane   = None
        self.right_lane  = None

        # Temporal persistence state
        self.prev_left_fit   = None
        self.prev_right_fit  = None

        # ROI boundaries - set by auto_calibrate
        self.roi_top    = 0.55
        self.roi_bottom = 0.92

    def auto_calibrate(self, cap):
        # Calls roi_calibrator module to auto detect road/bonnet boundary
        self.roi_top, self.roi_bottom = auto_calibrate(cap)

    def detect(self, frame):
        # Runs full detection pipeline - coordinates all modules
        # 1. Preprocess frame
        # 2. Run sliding window on road area only
        # 3. Fit polynomials
        # 4. Apply temporal persistence
        # 5. Convert to drawable lines
        height = frame.shape[0]

        # Step 1: Preprocess using Embitel pipeline
        binary = preprocess(frame, self.thresh)

        # Step 2: Sliding window on road area only - bonnet excluded
        lx, ly, rx, ry, left_valid, right_valid = run_sliding_window(
            binary, self.roi_top, self.roi_bottom,
            self.n_windows, self.margin, self.minpix
        )

        # Step 3: Fit 2nd order polynomial through lane pixels
        new_left_fit  = fit_polynomial(lx, ly)
        new_right_fit = fit_polynomial(rx, ry)

        # Step 4: Temporal persistence - use previous if current weak
        self.left_fit,  self.prev_left_fit  = apply_temporal_persistence(
            new_left_fit,  self.prev_left_fit,  left_valid)
        self.right_fit, self.prev_right_fit = apply_temporal_persistence(
            new_right_fit, self.prev_right_fit, right_valid)

        # Step 5: Convert polynomials to drawable line coordinates
        self.left_lane  = poly_to_line(self.left_fit,  height, self.roi_top, self.roi_bottom)
        self.right_lane = poly_to_line(self.right_fit, height, self.roi_top, self.roi_bottom)

        return self.left_lane, self.right_lane

    def draw_lanes(self, frame):
        # Draws yellow lane lines and green ego lane fill
        frame = draw_lane_fill(frame, self.left_lane, self.right_lane)
        overlay = frame.copy()
        if self.left_lane:
            x1,y1,x2,y2 = self.left_lane
            cv2.line(overlay,(x1,y1),(x2,y2),(0,255,255),4)
        if self.right_lane:
            x1,y1,x2,y2 = self.right_lane
            cv2.line(overlay,(x1,y1),(x2,y2),(0,255,255),4)
        return cv2.addWeighted(overlay, 0.8, frame, 0.2, 0)

    def check_departure(self, frame, warning_zone=0.35):
        # Calls LDW module to check if vehicle departed from ego lane
        return check_departure(
            self.left_lane, self.right_lane,
            frame.shape[1], warning_zone)

    def draw_warning(self, frame, side):
        # Calls LDW module to draw warning banner
        return draw_ldw_warning(frame, side)
