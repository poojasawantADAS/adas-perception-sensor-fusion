import cv2
from ultralytics import YOLO
import os

VIDEO_IN  = os.path.expanduser("~/adas-perception-sensor-fusion/data/dashcam.avi")
VIDEO_OUT = os.path.expanduser("~/adas-perception-sensor-fusion/data/output_tracked.avi")
MAX_FRAMES = 750

CLASSES = {0:"pedestrian", 1:"cyclist", 2:"car", 3:"motorcycle", 5:"bus", 7:"truck"}
COLORS  = {"pedestrian":(0,0,255), "cyclist":(0,165,255), "car":(255,0,0),
           "motorcycle":(0,255,255), "bus":(128,0,128), "truck":(0,255,0)}

class SimpleTracker:
    def __init__(self):
        self.tracks = {}
        self.next_id = 0

    def update(self, detections):
        updated = {}
        for cx, cy, label in detections:
            matched = False
            for tid, track in self.tracks.items():
                dx = track["cx"] - cx
                dy = track["cy"] - cy
                if (dx**2 + dy**2)**0.5 < 80:
                    track["cx"] = int(0.7*track["cx"] + 0.3*cx)
                    track["cy"] = int(0.7*track["cy"] + 0.3*cy)
                    track["hits"] += 1
                    track["label"] = label
                    updated[tid] = track
                    matched = True
                    break
            if not matched:
                updated[self.next_id] = {"cx":cx,"cy":cy,"label":label,"hits":1}
                self.next_id += 1
        self.tracks = updated
        return self.tracks

def main():
    print("Loading YOLO model...")
    model = YOLO("yolov8n.pt")
    print("Opening video...")
    cap = cv2.VideoCapture(VIDEO_IN)
    if not cap.isOpened():
        print("ERROR: Cannot open video!")
        return
    fps    = cap.get(cv2.CAP_PROP_FPS)
    width  = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    out    = cv2.VideoWriter(VIDEO_OUT, fourcc, fps, (width, height))
    tracker = SimpleTracker()
    frame_count = 0
    total_detections = 0
    print(f"Processing first {MAX_FRAMES} frames...")
    while cap.isOpened() and frame_count < MAX_FRAMES:
        ret, frame = cap.read()
        if not ret:
            break
        results = model(frame, verbose=False)[0]
        detections = []
        for box in results.boxes:
            cls_id = int(box.cls[0])
            conf   = float(box.conf[0])
            if cls_id in CLASSES and conf > 0.4:
                x1,y1,x2,y2 = map(int, box.xyxy[0])
                cx,cy = (x1+x2)//2, (y1+y2)//2
                label = CLASSES[cls_id]
                detections.append((cx,cy,label))
                total_detections += 1
                color = COLORS.get(label,(255,255,255))
                cv2.rectangle(frame,(x1,y1),(x2,y2),color,2)
                cv2.putText(frame,f"{label} {conf:.2f}",(x1,y1-8),
                    cv2.FONT_HERSHEY_SIMPLEX,0.6,color,2)
        tracks = tracker.update(detections)
        for tid, track in tracks.items():
            cx,cy  = track["cx"],track["cy"]
            label  = track["label"]
            hits   = track["hits"]
            color  = COLORS.get(label,(255,255,255))
            cv2.circle(frame,(cx,cy),5,color,-1)
            cv2.putText(frame,f"ID:{tid} hits:{hits}",(cx+8,cy),
                cv2.FONT_HERSHEY_SIMPLEX,0.5,color,2)
        cv2.putText(frame,f"Frame:{frame_count} Tracks:{len(tracks)}",
            (20,40),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        out.write(frame)
        frame_count += 1
        if frame_count % 50 == 0:
            print(f"  Processed {frame_count}/{MAX_FRAMES} frames...")
    cap.release()
    out.release()
    print(f"DONE!")
    print(f"Frames processed : {frame_count}")
    print(f"Total detections : {total_detections}")
    print(f"Output saved to  : {VIDEO_OUT}")

if __name__ == "__main__":
    main()
