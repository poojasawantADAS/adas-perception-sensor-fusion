import numpy as np
from lane_modules.histogram import get_histogram_peaks

def run_sliding_window(binary, roi_top, roi_bottom, n_windows, margin, minpix):
    # Core sliding window algorithm - finds all lane pixels
    # Confined to road area only - bonnet never processed
    # Starts at histogram peaks, slides upward recentering each step

    height, width = binary.shape

    # Get starting positions from histogram - road area only
    left_x, right_x, left_peak, right_peak = get_histogram_peaks(
        binary, roi_top, roi_bottom)

    # Minimum peak height to consider as valid lane detection
    min_peak    = 300
    left_valid  = left_peak  > min_peak
    right_valid = right_peak > min_peak

    # Define road boundaries in pixels
    road_top    = int(height * roi_top)
    road_bottom = int(height * roi_bottom)
    road_height = road_bottom - road_top

    # Find all non-zero pixels in road area only
    road_binary = binary[road_top:road_bottom, :]
    nonzero     = road_binary.nonzero()
    nonzero_y   = np.array(nonzero[0]) + road_top
    nonzero_x   = np.array(nonzero[1])

    window_height   = road_height // n_windows
    left_lane_inds  = []
    right_lane_inds = []

    # Slide windows from road bottom to road top
    for window in range(n_windows):
        y_low  = road_bottom - (window + 1) * window_height
        y_high = road_bottom - window * window_height

        xl_low,  xl_high = left_x  - margin, left_x  + margin
        xr_low,  xr_high = right_x - margin, right_x + margin

        good_left  = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                     (nonzero_x >= xl_low) & (nonzero_x < xl_high)).nonzero()[0]
        good_right = ((nonzero_y >= y_low) & (nonzero_y < y_high) &
                     (nonzero_x >= xr_low) & (nonzero_x < xr_high)).nonzero()[0]

        left_lane_inds.append(good_left)
        right_lane_inds.append(good_right)

        if len(good_left)  > minpix:
            left_x  = int(np.mean(nonzero_x[good_left]))
        if len(good_right) > minpix:
            right_x = int(np.mean(nonzero_x[good_right]))

    left_lane_inds  = np.concatenate(left_lane_inds)
    right_lane_inds = np.concatenate(right_lane_inds)

    lx = nonzero_x[left_lane_inds]
    ly = nonzero_y[left_lane_inds]
    rx = nonzero_x[right_lane_inds]
    ry = nonzero_y[right_lane_inds]

    return lx, ly, rx, ry, left_valid, right_valid
