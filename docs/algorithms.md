# Algorithms Used in ADAS

This document provides an overview of the key algorithms commonly used in Advanced
Driver Assistance Systems (ADAS). The focus is on explaining where each algorithm
fits in the perception, tracking, and filtering pipeline, rather than on detailed
mathematical implementation.

---

## 1. Object Detection Algorithms

Object detection algorithms are used in the perception stage to identify vehicles,
pedestrians, lanes, and other road objects from sensor data, primarily camera images.

### Common Real-Time Detection Algorithms (ADAS-Focused)
- **YOLO (You Only Look Once)**: A single-stage, real-time object detection algorithm
  widely used in ADAS due to its low latency and efficiency.
- **SSD (Single Shot Detector)**: A lightweight detection algorithm suitable for
  embedded automotive platforms.
- **CenterNet**: An anchor-free detection method that offers a good balance between
  speed and accuracy.

### Two-Stage Detection Algorithms (Higher Accuracy, Higher Latency)
- **R-CNN**
- **Fast R-CNN**
- **Faster R-CNN**

These methods provide high detection accuracy but are generally not preferred for
real-time ADAS due to computational cost.

### Emerging Detection Approaches (Awareness Level)
- **DETR (Detection Transformer)**
- **Deformable DETR**
- **BEVFormer / PETR**

Transformer-based approaches are actively researched for higher levels of autonomy
but are not yet common in production ADAS systems.

---

## 2. Tracking Algorithms

Tracking algorithms ensure temporal consistency by maintaining object identity
across frames and estimating motion parameters such as velocity and acceleration.

### Kalman-Based Tracking (Industry Standard)
- **Kalman Filter (KF)**: Used for linear motion tracking with Gaussian noise.
- **Extended Kalman Filter (EKF)**: Applied when motion or measurement models are
  non-linear.
- **Unscented Kalman Filter (UKF)**: Provides improved estimation for highly
  non-linear systems.

These filters form the backbone of object tracking in most ADAS applications.

### Multi-Object Tracking Algorithms
- **SORT (Simple Online and Realtime Tracking)**
- **Deep SORT**
- **ByteTrack**

These methods combine object detection with Kalman-based prediction and data
association to track multiple objects simultaneously.

### Advanced Probabilistic Tracking (Contextual Awareness)
- **Particle Filter**
- **Multiple Hypothesis Tracking (MHT)**
- **Joint Probabilistic Data Association (JPDA)**

These approaches are used in complex scenarios with high uncertainty or dense traffic.

---

## 3. Filtering and Signal Conditioning Algorithms

Filtering algorithms are used to reduce noise and improve the stability of sensor
measurements and intermediate signals.

### Common Automotive Filters
- **Moving Average Filter**
- **Exponential Moving Average (EMA)**
- **Butterworth Filter**
- **Low-Pass and High-Pass Filters**

These filters are widely used to smooth signals such as vehicle speed, steering angle,
and radar measurements.

### Temporal Smoothing Techniques
- **Sliding Window Filtering**
- **Median Filter**

These methods improve stability of perception outputs across consecutive frames.

### Additional Estimation Filters
- **Savitzky–Golay Filter**
- **Complementary Filter**

These are used in specific scenarios requiring additional signal smoothing or fusion.

---

## 4. Classical Computer Vision Techniques (Contextual)

In addition to deep learning-based methods, classical computer vision techniques are
still used in certain ADAS functions:

- **Canny Edge Detection**
- **Hough Transform** (lane detection)
- **Optical Flow (Lucas–Kanade)**
- **ORB / SIFT / SURF** (feature extraction)

These techniques are typically combined with learning-based methods or used as
supporting algorithms.

---

## 5. Sensor Fusion Algorithms (Conceptual Overview)

Sensor fusion combines information from multiple sensors to improve robustness and
accuracy.

- **Kalman Filter-based Fusion**
- **Extended / Unscented Kalman Filter Fusion**
- **Track-to-Track Fusion**
- **Object-Level Fusion**

Sensor fusion outputs provide stable and reliable inputs for planning and control
modules.

---

## Summary

In this project, real-time object detection and Kalman-based tracking form the core
of the perception pipeline. Additional algorithms are discussed to demonstrate
awareness of industry practices and emerging trends in ADAS and autonomous driving.
