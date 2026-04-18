# Hand Gesture Cursor Control

This project turns your hand into a virtual mouse using computer vision. A webcam watches your hand, MediaPipe finds your finger landmarks, and Python translates those landmarks into real cursor movement, clicks, and scroll actions.

## Features

- Move the cursor with your index finger
- Left click by pinching your thumb and index finger
- Right click by pinching your thumb and middle finger
- Scroll by keeping index and middle fingers close together and moving them up or down
- Close the camera cleanly with one press of `Q`, `Esc`, or by clicking the window close button once

## Tech Stack

- `OpenCV` for camera capture, image frames, and the live preview window
- `MediaPipe Hands` for hand landmark detection
- `PyAutoGUI` for controlling the system mouse and scroll events
- `Python` for the application logic and gesture rules

## Quick Start

```bash
pip install -r requirements.txt
python main.py
```

## Gesture Guide

- Cursor move: point with your index finger
- Left click: bring thumb tip and index tip together
- Right click: bring thumb tip and middle tip together
- Scroll up: keep index and middle fingertips close, then raise them
- Scroll down: keep index and middle fingertips close, then lower them

## Project Notes

- The webcam feed is mirrored so movement feels natural
- Cursor movement is smoothed to reduce shaking
- Clicks use a short cooldown so one pinch does not fire repeatedly
- The app releases the camera and destroys OpenCV windows during shutdown

## Pipeline-Oriented Files

- `main.py` is the launcher entrypoint
- `gesture_mouse_pipeline.py` contains the computer-vision interaction pipeline
- `cv_virtual_mouse_pipeline_update.md` contains the detailed project write-up
- `pipeline_showcase/index.html` is the lightweight frontend presentation page
