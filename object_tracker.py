import torch
import cv2
import serial
import time
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv5 model
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Setup serial connection
arduino = serial.Serial('COM3', 9600)  # Change COM port as needed
time.sleep(2)

# Setup DeepSORT tracker
tracker = DeepSort(max_age=30)

# Define object to track
TARGET_OBJECT = 'bottle'
target_id = None

cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv5 detection
    results = model(frame)
    detections = results.pandas().xyxy[0]

    dets_for_sort = []
    for _, row in detections.iterrows():
        if row['confidence'] > 0.6:
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            dets_for_sort.append(([xmin, ymin, xmax - xmin, ymax - ymin], row['confidence'], row['name']))

    tracks = tracker.update_tracks(dets_for_sort, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()
        label = track.get_det_class()

        if label == TARGET_OBJECT:
            if target_id is None:
                target_id = track_id  # lock on the first matching object

            if track_id == target_id:
                x_center = (ltrb[0] + ltrb[2]) / 2
                width = frame.shape[1]

                if x_center < width / 3:
                    arduino.write(b'LEFT\n')
                elif x_center > width * 2 / 3:
                    arduino.write(b'RIGHT\n')
                else:
                    arduino.write(b'GRAB\n')
                break

    cv2.imshow("Tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
