# ADAS Perception & Sensor Fusion Pipeline

> Real-time object detection, EKF tracking, and Lane Departure Warning
> validated on actual Michigan highway dashcam footage — C++20 & Python

![Python](https://img.shields.io/badge/Python-3.10-blue)
![C++](https://img.shields.io/badge/C++-20-blue)
![OpenCV](https://img.shields.io/badge/OpenCV-4.x-green)
![YOLO](https://img.shields.io/badge/YOLOv8-ultralytics-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What This Project Does

A configurable open-source ADAS perception pipeline that processes
dashcam video and performs:

- **Object Detection** — detects cars trucks pedestrians cyclists using YOLOv8
- **EKF Tracking** — tracks objects across frames using C++20 Extended Kalman Filter
- **Lane Detection** — sliding window algorithm detects left and right lane markings
- **Lane Departure Warning** — alerts when vehicle drifts from ego lane
- **Auto ROI Calibration** — automatically detects road boundary for any dashcam

Anyone can use this with their own dashcam by editing one config file.

---

## Quick Start

### 1. Clone
```bash
git clone https://github.com/poojasawantADAS/adas-perception-sensor-fusion.git
cd adas-perception-sensor-fusion
```

### 2. Install dependencies
```bash
pip3 install opencv-python ultralytics pyyaml numpy
```

### 3. Add your dashcam video
```bash
mkdir -p data
cp /path/to/your/video.avi data/dashcam.avi
```

### 4. Edit config.yaml
```yaml
video:
  path: "data/dashcam.avi"
  max_seconds: 30
```

### 5. Run
```bash
python3 run_pipeline.py
```

Output video saved automatically with version numbering.

---

## Architecture
Dashcam Video (any resolution, any FPS)
|
v
Auto ROI Calibration
(variance analysis detects road/bonnet boundary)
|
+-----------------+-----------------+
|                                   |
v                                   v
YOLO Object Detection            Sliding Window Lane Detection
EKF Tracking (C++20)             Color Filter -> Binary Threshold
Ego Vehicle Filter               Histogram -> Sliding Window
Polynomial Fit -> Temporal Persistence
|                                   |
+-----------------+-----------------+
|
v
LDW Decision Engine
(ego lane + departure check)
|
v
Output Video
(tracked objects + lanes + LDW warning)
---

## Configuration

All settings in config.yaml — no code changes needed:

```yaml
video:
  path: "data/dashcam.avi"     # your video path
  max_seconds: 30               # seconds to process

detection:
  enabled: true
  model: "yolov8n"              # n=fast s=better m=best
  confidence: 0.4               # detection threshold
  classes:
    - car
    - pedestrian
    - truck
    - cyclist

lane_detection:
  enabled: true
  sensitivity: medium           # low medium high
  auto_calibrate: true          # auto detect road boundary

ldw:
  enabled: true
  warning_zone: 0.35            # departure sensitivity

output:
  save_video: true
  show_ids: true
  show_confidence: true
  path: "data/output.avi"       # auto-versioned
```

---

## Project Structure
adas-perception-sensor-fusion/
|
+-- config.yaml              <- EDIT THIS ONLY
+-- run_pipeline.py          <- single entry point
|
+-- src/cpp/                 <- C++20 core algorithms
|   +-- tracker/
|   |   +-- ekf_tracker.hpp/cpp       <- Extended Kalman Filter
|   |   +-- timestamp_sync.hpp/cpp    <- sensor time synchronization
|   +-- perception/
|   |   +-- image_frame.hpp/cpp       <- camera frame class
|   +-- lidar/
|       +-- lidar_frame.hpp/cpp       <- LiDAR point cloud class
|
+-- tools/
|   +-- lane_detector.py     <- coordinator
|   +-- lane_modules/        <- modular algorithm library
|       +-- color_filter.py       <- white/yellow pixel isolation
|       +-- preprocessor.py       <- grayscale blur threshold
|       +-- roi_calibrator.py     <- auto bonnet detection
|       +-- histogram.py          <- lane base detection
|       +-- sliding_window.py     <- core lane finding
|       +-- lane_fitter.py        <- polynomial fit and persistence
|       +-- ldw.py                <- departure warning logic
|
+-- docs/                    <- architecture and documentation
+-- data/                    <- add your dashcam video here
---

## C++ Core — EKF Tracker

```cpp
// 5-state Extended Kalman Filter
// State vector: [x, y, z, vx, vy]
// Predict: extrapolate using velocity
// Update: blend with new sensor detection

EKFTracker tracker;
Detection det{5.0f, 10.0f, 0.0f, timestamp};
Track track = tracker.update(det);
tracker.predict(dt);
```

Build and test:
```bash
mkdir build && cd build && cmake .. && make
./src/adas_perception_app
```

---

## Why Sliding Window?

Chosen over deep learning approaches because:

- Runs on CPU without GPU — matches low-cost ADAS ECU constraints
- Handles curved roads better than Hough Transform
- Fully explainable — every decision traceable
- Production proven — used in entry-level ADAS systems
- Baseline for future CNN upgrade (in roadmap)

Limitation: degrades in adverse weather — consistent with classical CV systems.

---

## Test Results

Validated on real Michigan highway dashcam footage:

| Metric | Value |
|--------|-------|
| Resolution | 1920x1088 Full HD |
| Processing speed | 10-12 FPS on CPU |
| Object detections | 2887 in 30 seconds |
| Objects detected | Cars trucks pedestrians cyclists |
| Lane detection | Sliding window with auto ROI calibration |
| LDW | Ego lane departure warning with temporal persistence |

---

## Roadmap

- [ ] pybind11 bridge — Python calls C++ EKF directly
- [ ] KITTI dataset — camera and LiDAR sensor fusion
- [ ] Multiple camera support
- [ ] ROS2 publisher node for vehicle integration
- [ ] CNN-based lane detection upgrade
- [ ] Night and rain condition optimization

---

## Author

**Pooja Sawant**
Senior ADAS / Perception Engineer | Michigan, USA

---

## License

MIT License — free to use modify and distribute.
