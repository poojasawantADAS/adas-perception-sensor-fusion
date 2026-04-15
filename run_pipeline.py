import cv2
import yaml
import os
import time
from ultralytics import YOLO
import sys
sys.path.insert(0, "/home/pooja/adas-perception-sensor-fusion/tools")
from lane_detector import LaneDetector

# ── Load config file ─────────────────────────────
# Reads user settings from config.yaml
# User only edits config.yaml — never this file
def load_config(config_path="config.yaml"):
    with open(config_path, "r") as f:
        return yaml.safe_load(f)

# ── Auto configure video properties ─────────────
# Reads video and returns all properties automatically
# No manual input needed — works with any dashcam format
def get_video_properties(cap):
    return {
        "fps":    cap.get(cv2.CAP_PROP_FPS),
        "width":  int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
        "height": int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)),
        "total":  int(cap.get(cv2.CAP_PROP_FRAME_COUNT)),
    }

# ── Simple EKF style tracker ─────────────────────
# Tracks detected objects across frames using Kalman blend
# Assigns unique ID to each object and maintains track history
class SimpleTracker:
    def __init__(self):
        self.tracks  = {}
        self.next_id = 0

    def update(self, detections):
        # Match new detections to existing tracks by distance
        # New object = distance > 80px from all existing tracks
        updated = {}
        for cx, cy, label in detections:
            matched = False
            for tid, track in self.tracks.items():
                dx   = track["cx"] - cx
                dy   = track["cy"] - cy
                dist = (dx**2 + dy**2) ** 0.5
                if dist < 80:
                    # Kalman blend: 70% old position + 30% new detection
                    track["cx"]    = int(0.7 * track["cx"] + 0.3 * cx)
                    track["cy"]    = int(0.7 * track["cy"] + 0.3 * cy)
                    track["hits"] += 1
                    track["label"] = label
                    updated[tid]   = track
                    matched        = True
                    break
            if not matched:
                # New track — assign new ID
                updated[self.next_id] = {
                    "cx": cx, "cy": cy,
                    "label": label, "hits": 1
                }
                self.next_id += 1
        self.tracks = updated
        return self.tracks

# ── YOLO class mappings ───────────────────────────
# Maps COCO dataset class IDs to ADAS relevant labels
CLASSES = {
    0: "pedestrian",
    1: "cyclist",
    2: "car",
    3: "motorcycle",
    5: "bus",
    7: "truck"
}

# Colors per object type in BGR format
COLORS = {
    "pedestrian": (0, 0, 255),
    "cyclist":    (0, 165, 255),
    "car":        (255, 0, 0),
    "motorcycle": (0, 255, 255),
    "bus":        (128, 0, 128),
    "truck":      (0, 255, 0),
}

# ── Draw LDW warning on frame ─────────────────────
# Shows red warning banner when lane departure detected
def draw_ldw_warning(frame, side):
    h, w = frame.shape[:2]
    # Red warning banner at top of frame
    cv2.rectangle(frame, (0, 0), (w, 80), (0, 0, 200), -1)
    cv2.putText(frame,
        f"LANE DEPARTURE WARNING — {side}!",
        (20, 55),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.4, (255, 255, 255), 3)
    return frame

# ── Main pipeline ─────────────────────────────────
# Ties everything together — reads config, processes video,
# runs detection + tracking + lane detection + LDW
def main():
    # Load user config
    config     = load_config()
    video_cfg  = config["video"]
    det_cfg    = config["detection"]
    lane_cfg   = config["lane_detection"]
    ldw_cfg    = config["ldw"]
    out_cfg    = config["output"]

    video_path = video_cfg["path"]
    max_frames = int(video_cfg["max_seconds"] * 25)

    print("=" * 50)
    print("  ADAS Perception Pipeline")
    print("=" * 50)
    print(f"  Video      : {video_path}")
    print(f"  Detection  : {det_cfg['enabled']}")
    print(f"  Lanes      : {lane_cfg['enabled']}")
    print(f"  LDW        : {ldw_cfg['enabled']}")
    print("=" * 50)

    # Load YOLO model from config
    print(f"Loading {det_cfg['model']} model...")
    model = YOLO(f"{det_cfg['model']}.pt")

    # Open video
    print(f"Opening video...")
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print(f"ERROR: Cannot open {video_path}")
        return

    # Auto configure from video properties
    props  = get_video_properties(cap)
    fps    = props["fps"]
    width  = props["width"]
    height = props["height"]
    total  = props["total"]

    print(f"Auto-configured:")
    print(f"  Resolution : {width}x{height}")
    print(f"  FPS        : {fps}")
    print(f"  Duration   : {total/fps:.1f} seconds")

    # Auto-versioned output file
    # Saves as output_tracked.avi, output_tracked_1.avi, output_tracked_2.avi etc
    import os
    base_path = out_cfg["path"].replace(".avi", "")
    out_path  = out_cfg["path"]
    version   = 1
    while os.path.exists(out_path):
        out_path = f"{base_path}_{version}.avi"
        version += 1
    print(f"  Output file      : {out_path}")

    # Setup output video writer
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out    = cv2.VideoWriter(out_path, fourcc, fps, (width, height))

    # Initialize modules
    tracker      = SimpleTracker()
    lane_detector = LaneDetector(
        sensitivity=lane_cfg["sensitivity"])

    # Auto calibrate ROI if enabled in config
    if lane_cfg.get("auto_calibrate", True):
        lane_detector.auto_calibrate(cap)

    # Counters for summary
    frame_count      = 0
    total_detections = 0
    ldw_warnings     = 0
    start_time       = time.time()

    print(f"Processing {max_frames} frames...")
    print("-" * 50)

    while cap.isOpened() and frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # ── Object Detection ──────────────────────
        detections = []
        if det_cfg["enabled"]:
            results = model(frame, verbose=False)[0]
            for box in results.boxes:
                cls_id = int(box.cls[0])
                conf   = float(box.conf[0])
                if cls_id in CLASSES and conf > det_cfg["confidence"]:
                    x1,y1,x2,y2 = map(int, box.xyxy[0])
                    # Filter ego vehicle — own car always at bottom center of frame
                    box_center_y = (y1 + y2) // 2
                    box_center_x = (x1 + x2) // 2
                    if box_center_y > height * 0.80 and abs(box_center_x - width//2) < width * 0.3:
                        continue
                    x1,y1,x2,y2 = map(int, box.xyxy[0])
                    cx,cy = (x1+x2)//2, (y1+y2)//2
                    label = CLASSES[cls_id]
                    detections.append((cx, cy, label))
                    total_detections += 1
                    color = COLORS.get(label, (255,255,255))

                    # Draw bounding box
                    cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)

                    # Show label and confidence if enabled
                    if out_cfg["show_confidence"]:
                        cv2.putText(frame,
                            f"{label} {conf:.2f}",
                            (x1, y1-8),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            0.6, color, 2)

        # ── EKF Tracking ─────────────────────────
        tracks = tracker.update(detections)
        if out_cfg["show_ids"]:
            for tid, track in tracks.items():
                cx,cy  = track["cx"], track["cy"]
                label  = track["label"]
                color  = COLORS.get(label,(255,255,255))
                cv2.circle(frame,(cx,cy),5,color,-1)
                cv2.putText(frame,
                    f"ID:{tid}",
                    (cx+8, cy),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.5, color, 2)

        # ── Lane Detection ────────────────────────
        if lane_cfg["enabled"]:
            lane_detector.detect(frame)
            frame = lane_detector.draw_lanes(frame)

            # ── LDW Warning ───────────────────────
            if ldw_cfg["enabled"]:
                departed, side = lane_detector.check_departure(
                    frame, ldw_cfg["warning_zone"])
                if departed:
                    frame = draw_ldw_warning(frame, side)
                    ldw_warnings += 1

        # ── HUD Overlay ───────────────────────────
        # Shows frame count and active tracks on screen
        if out_cfg["show_fps"]:
            elapsed = time.time() - start_time
            fps_actual = frame_count / elapsed if elapsed > 0 else 0
            cv2.putText(frame,
                f"Frame:{frame_count} Tracks:{len(tracks)} FPS:{fps_actual:.1f}",
                (20, height - 20),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7, (255,255,255), 2)

        out.write(frame)
        frame_count += 1

        if frame_count % 50 == 0:
            print(f"  Processed {frame_count}/{max_frames} frames...")

    cap.release()
    out.release()

    # Print summary
    elapsed = time.time() - start_time
    print("-" * 50)
    print(f"DONE!")
    print(f"  Frames processed : {frame_count}")
    print(f"  Total detections : {total_detections}")
    print(f"  LDW warnings     : {ldw_warnings}")
    print(f"  Time taken       : {elapsed:.1f} seconds")
    print(f"  Output saved to  : {out_path}")
    print("=" * 50)

if __name__ == "__main__":
    main()
