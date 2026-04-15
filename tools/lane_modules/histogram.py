import numpy as np

def get_histogram_peaks(binary, roi_top, roi_bottom):
    # Histogram analysis on ROAD AREA ONLY
    # Bonnet area completely excluded from calculation
    # Sums pixel intensities along x-axis within road section
    # Peaks = left and right lane base positions

    height = binary.shape[0]

    # Extract road section only - bonnet never enters calculation!
    road_top    = int(height * roi_top)
    road_bottom = int(height * roi_bottom)
    road_section = binary[road_top:road_bottom, :]

    # Sum pixels along x-axis - bright lane pixels create peaks
    histogram = np.sum(road_section, axis=0)

    # Split into left and right halves
    midpoint = len(histogram) // 2

    # Left lane peak in left half, right lane peak in right half
    left_base  = np.argmax(histogram[:midpoint])
    right_base = np.argmax(histogram[midpoint:]) + midpoint

    # Peak height indicates how many lane pixels found
    # Low peak = weak detection, high peak = strong detection
    left_peak  = histogram[left_base]
    right_peak = histogram[right_base]

    return left_base, right_base, left_peak, right_peak
