# Algorithms Used in ADAS

This document describes the key algorithms commonly used in ADAS systems and
their role in perception, tracking, and decision support.

Detection → Tracking → Filtering → Planning


## Object Detection

### YOLO
YOLO is a real-time object detection algorithm used to detect vehicles and pedestrians
from camera images. It is suitable for ADAS applications due to its low latency and
single-stage detection approach.

### R-CNN and Fast R-CNN
R-CNN based approaches provide accurate object detection but are computationally
expensive, making them less suitable for real-time ADAS systems.

## Tracking and Filtering

### Kalman Filter
The Kalman Filter is used to track detected objects over time by estimating their
position and velocity, reducing noise from frame-by-frame detections.

### Sliding Window
Sliding window techniques use information from multiple consecutive frames to
improve temporal stability of detections.

### Butterworth Filter
Butterworth filters are low-pass filters used to smooth noisy signals such as speed
or steering measurements in vehicle systems.
