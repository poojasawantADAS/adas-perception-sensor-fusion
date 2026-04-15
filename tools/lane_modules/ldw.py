import cv2

def check_departure(left_lane, right_lane, frame_width, warning_zone=0.35):
    # LDW decision logic - checks if vehicle drifted from ego lane center
    # Only triggers when BOTH lanes detected (ego lane confirmed)
    # Validates lane width is realistic before triggering warning

    if left_lane is None or right_lane is None:
        return False, None

    lx = left_lane[2]   # left lane x at bottom of road area
    rx = right_lane[2]  # right lane x at bottom of road area

    # Left must be left of right - reject swapped detections
    if lx >= rx:
        return False, None

    lane_width = rx - lx

    # Realistic lane width check in pixels
    # Too narrow = wrong detection (noise detected as lane)
    # Too wide = multiple lanes detected instead of ego lane
    if lane_width < 300 or lane_width > 1200:
        return False, None

    # Calculate vehicle offset from lane center
    center_x    = frame_width // 2
    lane_center = (lx + rx) // 2
    offset      = (center_x - lane_center) / frame_width

    # Trigger warning if offset exceeds threshold
    if abs(offset) > warning_zone:
        side = "LEFT" if offset > 0 else "RIGHT"
        return True, side

    return False, None

def draw_ldw_warning(frame, side):
    # Draws red warning banner at top of frame when departure detected
    import cv2
    h, w = frame.shape[:2]
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 0, 200), -1)
    cv2.putText(frame,
        f"LANE DEPARTURE WARNING - {side}!",
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4, (255, 255, 255), 3)
    return frame

def draw_lane_fill(frame, left_lane, right_lane):
    # Fills area between detected lanes with transparent green
    # Shows driver which lane the system has identified as ego lane
    if left_lane is None or right_lane is None:
        return frame
    overlay = frame.copy()
    pts = [
        (left_lane[0],  left_lane[1]),
        (right_lane[0], right_lane[1]),
        (right_lane[2], right_lane[3]),
        (left_lane[2],  left_lane[3]),
    ]
    import numpy as np
    cv2.fillPoly(overlay, [__import__('numpy').array(pts)], (0, 255, 0))
    return cv2.addWeighted(overlay, 0.2, frame, 0.8, 0)
