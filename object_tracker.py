import torch
import cv2
import serial
import time
from deep_sort_realtime.deepsort_tracker import DeepSort

# Load YOLOv5 model (Pre-trained model)
model = torch.hub.load('ultralytics/yolov5', 'yolov5s', pretrained=True)

# Setup serial communication with Arduino
arduino = serial.Serial('COM3', 9600)  # Adjust COM port for your setup
time.sleep(2)

# Setup DeepSORT tracker (for continuous tracking)
tracker = DeepSort(max_age=30)

# Define the object categories to sort
CATEGORY_1 = 'red'
CATEGORY_2 = 'blue'

# Initialize camera
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # YOLOv5 object detection
    results = model(frame)
    detections = results.pandas().xyxy[0]

    dets_for_sort = []
    for _, row in detections.iterrows():
        if row['confidence'] > 0.6:
            xmin, ymin, xmax, ymax = row['xmin'], row['ymin'], row['xmax'], row['ymax']
            dets_for_sort.append(([xmin, ymin, xmax - xmin, ymax - ymin], row['confidence'], row['name']))

    # Update the tracker
    tracks = tracker.update_tracks(dets_for_sort, frame=frame)

    for track in tracks:
        if not track.is_confirmed():
            continue

        track_id = track.track_id
        ltrb = track.to_ltrb()
        label = track.get_det_class()

        if label == CATEGORY_1:  # Sorting based on object color or label
            # Send sorting command to Arduino for Category 1
            arduino.write(b'SORT_1\n')
        elif label == CATEGORY_2:
            # Send sorting command to Arduino for Category 2
            arduino.write(b'SORT_2\n')

    # Show the output frame
    cv2.imshow("Object Sorting", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
