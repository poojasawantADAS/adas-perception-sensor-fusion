# ADAS Perception and Sensor Fusion Pipeline

> Real-time object detection, EKF tracking, and Lane Departure Warning validated on actual Michigan highway dashcam footage - C++20 and Python

![Python](https://img.shields.io/badge/Python-3.10-blue)
![C++](https://img.shields.io/badge/C++-20-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![YOLO](https://img.shields.io/badge/YOLOv8-ultralytics-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

## What This Project Does

A configurable open-source ADAS perception pipeline that processes dashcam video and performs:

- Object Detection - detects cars trucks pedestrians cyclists using YOLOv8
- EKF Tracking - tracks objects across frames using C++20 Extended Kalman Filter
- Lane Detection - sliding window algorithm detects left and right lane markings
- Lane Departure Warning - alerts when vehicle drifts from ego lane
- Auto ROI Calibration - automatically detects road boundary for any dashcam

Anyone can use this with their own dashcam by editing one config file.

## Quick Start

1. Clone the repo
2. Run: pip3 install opencv-python ultralytics pyyaml numpy
3. Add your video to data/ folder
4. Edit config.yaml - change video path
5. Run: python3 run_pipeline.py

Output video saved automatically with version numbering.

## Test Results

| Metric | Value |
|--------|-------|
| Resolution | 1920x1088 Full HD |
| Processing speed | 10-12 FPS on CPU |
| Object detections | 2887 in 30 seconds |
| Objects detected | Cars trucks pedestrians cyclists |
| Lane detection | Sliding window with auto ROI calibration |
| LDW | Ego lane departure warning with temporal persistence |

## Project Structure

- config.yaml - EDIT THIS ONLY
- run_pipeline.py - single entry point
- src/cpp/tracker/ - EKF tracker and timestamp sync (C++20)
- src/cpp/perception/ - camera frame classes
- src/cpp/lidar/ - LiDAR point cloud classes
- tools/lane_detector.py - main coordinator
- tools/lane_modules/color_filter.py - white and yellow pixel isolation
- tools/lane_modules/preprocessor.py - grayscale blur threshold pipeline
- tools/lane_modules/roi_calibrator.py - auto bonnet road detection
- tools/lane_modules/histogram.py - lane base detection
- tools/lane_modules/sliding_window.py - core lane finding algorithm
- tools/lane_modules/lane_fitter.py - polynomial fit and temporal persistence
- tools/lane_modules/ldw.py - departure warning logic

## Configuration

All settings controlled via config.yaml - no code changes needed:

- video path and max seconds to process
- detection model (yolov8n=fast, yolov8s=better, yolov8m=best)
- detection confidence threshold
- lane sensitivity (low, medium, high)
- auto calibrate road boundary
- ldw warning zone threshold
- output video path (auto-versioned)

## Why Sliding Window for Lane Detection

Chosen over deep learning approaches because:

- Runs on CPU without GPU matching low-cost ADAS ECU constraints
- Handles curved roads better than Hough Transform
- Fully explainable and every decision is traceable
- Production proven in entry-level ADAS systems
- Provides baseline for future CNN upgrade in roadmap

Known limitation: degrades in adverse weather consistent with classical CV systems.

## Roadmap

- pybind11 bridge to call C++ EKF directly from Python
- KITTI dataset integration for camera and LiDAR sensor fusion
- Multiple camera support
- ROS2 publisher node for vehicle integration
- CNN based lane detection upgrade
- Night and rain condition optimization

## Author

Pooja Sawant
Senior ADAS / Perception Engineer | Michigan, USA

## License

MIT License - free to use modify and distribute.
