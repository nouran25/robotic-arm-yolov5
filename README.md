# Robotic Arm with Object Tracking using YOLOv5 + Deep SORT + Arduino Uno

## Overview
This project integrates a robotic arm (Arduino Uno) with object detection and tracking using YOLOv5 and Deep SORT. The system detects and locks onto a specific object (e.g., bottle) and sends commands to the robotic arm to move and grab it.

## Components
- Arduino Uno
- Servo motors (base + gripper)
- USB camera
- Python with YOLOv5 + Deep SORT
- Serial communication (pyserial)

## Setup Instructions
1. Upload `arduino/arm_control.ino` to your Arduino Uno.
2. Connect servos to pins 9 and 10 and power supply.
3. Install Python requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Install Deep SORT module:
   ```bash
   pip install deep_sort_realtime
   ```
5. Run the Python tracker:
   ```bash
   python detection/object_tracker.py
   ```
6. Place a bottle in front of the camera — the robotic arm will track and attempt to grab it!
