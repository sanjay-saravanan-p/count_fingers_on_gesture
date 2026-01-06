# Finger Counting Model using MediaPipe and OpenCV

This project is a Python-based real-time finger counting system that uses a webcam
and hand landmark detection to count the number of open fingers.


## Features
- Real-time hand detection and tracking
- Supports one or two hands simultaneously
- Accurate finger counting using geometric rules
- Separate thumb and finger logic
- Visual feedback using hand landmarks and text overlay


## Technologies Used
- Python
- OpenCV
- MediaPipe
- Math module


## Project Structure
count_fingers_on_gestures/
- README.md
- codes/
  - finger_counter.py


## How to Run
1. Install required libraries
2. Connect a webcam
3. Run the finger counting script


## Finger Counting Logic (Important)

This project does NOT use machine learning training.
Finger counting is done using geometric reasoning on hand landmarks.

Thumb:
- The palm center is calculated using MCP joints.
- The distance between the thumb tip and the palm center is measured.
- If the distance exceeds a threshold, the thumb is considered open.

Other Fingers (Index, Middle, Ring, Pinky):
- Each finger tip is compared with its joint.
- If the finger tip is above the joint (y-axis comparison), the finger is considered open.

The total finger count is calculated per hand and summed for all detected hands.


## Usage Notes

To get accurate results:
- Keep the full hand visible to the camera.
- Use a well-lit environment.
- Avoid extreme hand rotations.
- Maintain a reasonable distance from the camera.



<!-- -------------------------------------------------- -->

## Privacy Notice

This repository does NOT store or collect any personal data.

Webcam frames are processed only in real time and are NOT saved.
No images, videos, or hand data are stored on disk.

Do NOT upload recorded camera frames, screenshots, or personal images
to GitHub to protect user privacy.
