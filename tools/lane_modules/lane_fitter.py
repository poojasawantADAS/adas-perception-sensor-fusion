import numpy as np

def fit_polynomial(x_pts, y_pts):
    # Fits 2nd degree polynomial through detected lane pixels
    # 2nd order polynomial handles road curves properly
    # Returns polynomial coefficients [a, b, c] for ax^2 + bx + c
    if len(x_pts) < 10:
        return None
    try:
        return np.polyfit(y_pts, x_pts, 2)
    except:
        return None

def poly_to_line(fit, height, roi_top, roi_bottom):
    # Converts polynomial coefficients to drawable line coordinates
    # Evaluates polynomial at road top and road bottom only
    # Rejects lines outside visible frame boundaries
    if fit is None:
        return None

    # Evaluate at road top and road bottom
    y1 = int(height * roi_top)
    y2 = int(height * roi_bottom)
    x1 = int(fit[0]*y1**2 + fit[1]*y1 + fit[2])
    x2 = int(fit[0]*y2**2 + fit[1]*y2 + fit[2])

    # Reject lines outside visible frame
    if not (0 < x1 < 2000 and 0 < x2 < 2000):
        return None

    return (x1, y1, x2, y2)

def apply_temporal_persistence(new_fit, prev_fit, is_valid):
    # Temporal persistence logic
    # Confident new detection -> use new fit and update stored
    # Weak or failed detection -> fall back to previous frame fit
    # Prevents flickering lanes when detection temporarily fails
    if new_fit is not None and is_valid:
        return new_fit, new_fit  # (current, updated_prev)
    elif prev_fit is not None:
        return prev_fit, prev_fit  # use previous, keep previous
    return None, None
