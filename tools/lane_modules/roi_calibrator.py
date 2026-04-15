import cv2
import numpy as np

def auto_calibrate(cap):
    # Analyzes first 10 frames to auto detect road/bonnet boundary
    # Bonnet = low variance (uniform dark color)
    # Road   = high variance (lane markings, texture)
    # Scans rows bottom to top, finds transition point
    # Returns roi_top and roi_bottom as frame height percentages

    print("  Auto-calibrating ROI from video frames...")
    roi_tops = []
    frame_count = 0

    while frame_count < 10:
        ret, frame = cap.read()
        if not ret:
            break

        height, width = frame.shape[:2]
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Calculate variance row by row from bottom up
        variances = []
        for y in range(height - 1, height // 2, -1):
            row = blur[y, int(width*0.2):int(width*0.8)]
            variances.append((y, np.var(row.astype(float))))

        # Find transition from low variance (bonnet) to high variance (road)
        threshold   = np.mean([v for _, v in variances]) * 0.5
        sorted_vars = sorted(variances, key=lambda x: x[0])
        road_start_y = height
        for y, var in sorted_vars:
            if var > threshold:
                road_start_y = y
                break

        roi_tops.append(road_start_y / height)
        frame_count += 1

    # Average across 10 frames for stability
    avg_roi_top = float(np.mean(roi_tops))

    # Clamp to reasonable values
    roi_top    = max(0.45, min(0.70, avg_roi_top - 0.18))
    roi_bottom = max(0.65, min(0.80, avg_roi_top - 0.05))

    print(f"  ROI auto-calibrated:")
    print(f"    Road starts at : {avg_roi_top*100:.1f}% from top")
    print(f"    ROI top        : {roi_top*100:.1f}% from top")
    print(f"    ROI bottom     : {roi_bottom*100:.1f}% from top")

    # Reset video to beginning after calibration
    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    return roi_top, roi_bottom
