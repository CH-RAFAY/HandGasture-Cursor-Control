# Hand Gesture Virtual Mouse Project Update

## Project Vision

This project uses computer vision to let a user's hand behave like a virtual mouse. Instead of moving a physical mouse, the user moves a hand in front of a webcam and the application maps finger positions to cursor movement, clicks, and scrolling actions. The goal is to make human-computer interaction feel more natural, futuristic, and touch-free while still staying practical and understandable.

## Current Progress

The application now has a solid first working version with these core capabilities:

- Real-time webcam capture
- Hand landmark detection with MediaPipe
- Cursor movement controlled by the index finger
- Left click detection with an index-thumb pinch
- Right click detection with a middle-thumb pinch
- Scroll control using a two-finger gesture
- Clean camera shutdown with a single `Q` press, `Esc` press, or one click on the window close button
- Visual overlay showing status and instructions

This is an optimistic and promising stage of the project because the most important interaction loop is already in place: camera input, landmark detection, gesture interpretation, and operating-system control are all connected.

## How The Project Works

The application follows a very clear pipeline:

1. `OpenCV` opens the webcam and reads video frames continuously.
2. Each frame is flipped horizontally so the movement feels like looking in a mirror.
3. The frame is converted from BGR to RGB because MediaPipe expects RGB input.
4. `MediaPipe Hands` detects the hand and returns 21 landmark points for the fingers and palm.
5. The program picks important landmarks such as the thumb tip, index tip, and middle tip.
6. Landmark positions are converted from camera coordinates into screen coordinates.
7. `PyAutoGUI` moves the operating system cursor and triggers clicks or scrolling when gesture conditions are met.
8. `OpenCV` draws the UI overlay and shows the live camera window.
9. When the user presses `Q`, presses `Esc`, or clicks the window close button, the app releases the camera and destroys all windows fully.

## Technologies Used

### 1. Python

Python is the main programming language for the project. It is a strong choice because it has excellent support for:

- Computer vision
- Machine learning integration
- Fast prototyping
- Cross-library compatibility

Python helps us combine webcam handling, landmark detection, and mouse automation in a single readable application.

### 2. OpenCV

`OpenCV` is responsible for:

- Opening the webcam
- Reading live frames
- Flipping frames
- Converting color spaces
- Drawing rectangles, text, and points
- Displaying the project window
- Handling keyboard input and window closing

Why it matters:
OpenCV acts as the real-time visual layer of the system. Without it, the program would not be able to see the hand or present feedback to the user.

### 3. MediaPipe Hands

`MediaPipe Hands` is the hand-tracking engine. It detects and tracks 21 landmarks on a hand, including:

- Fingertips
- Finger joints
- Palm points

Why it matters:
Instead of writing a complex hand-detection model from scratch, MediaPipe gives us reliable landmark positions in real time. This makes gesture recognition much easier and much faster to build.

### 4. PyAutoGUI

`PyAutoGUI` is the bridge from vision to desktop control. It lets the project:

- Move the mouse pointer
- Perform left clicks
- Perform right clicks
- Scroll up or down

Why it matters:
Once MediaPipe tells us where the fingers are, PyAutoGUI lets those positions affect the real operating system.

## Gesture Design

The project currently uses simple, understandable gestures:

### Cursor Movement

- The index fingertip is used as the main pointer.
- Its webcam coordinates are mapped to the screen size.
- Smoothing is applied so the pointer feels stable instead of shaky.

### Left Click

- The app measures the distance between the thumb tip and the index fingertip.
- If that distance becomes very small, it is treated as a left click.
- A cooldown prevents accidental rapid repeated clicks.

### Right Click

- The distance between the thumb tip and the middle fingertip is measured.
- A small distance triggers a right click.

### Scrolling

- The app checks whether the index and middle fingertips are close together.
- If they are close and positioned higher, the app scrolls up.
- If they are close and positioned lower, the app scrolls down.

## Why Smoothing Is Important

Hand tracking is naturally a little noisy because small changes in lighting, finger angle, or camera position can create jitter. The cursor smoothing logic blends the old position and the new position so motion looks more controlled and comfortable.

This improves:

- Accuracy
- Visual stability
- User confidence
- Overall usability

## Camera Shutdown Behavior

One of the key project requirements was that the camera should close completely with one action. The application now supports a full shutdown path:

- Press `Q` once
- Press `Esc` once
- Or click the OpenCV window close button once

When that happens, the app:

- Stops the main loop
- Releases the webcam
- Closes the MediaPipe hand tracker
- Destroys all OpenCV windows

This is important because partial shutdowns can leave the webcam busy or keep background windows alive. The current shutdown flow is designed to avoid that problem.

## Frontend Deliverable

A small frontend presentation page is included in `pipeline_showcase/index.html`. It is not the gesture engine itself. Instead, it acts as a project showcase page that explains:

- What the project does
- Which gestures are supported
- Which technologies are used
- Why the project is useful

This makes the project easier to present in a portfolio, college submission, hackathon demo, or GitHub repository.

## File Structure

```text
HandGasture-Cursor-Control/
|-- main.py
|-- gesture_mouse_pipeline.py
|-- models/
|   `-- hand_landmarker.task
|-- requirements.txt
|-- README.md
|-- cv_virtual_mouse_pipeline_update.md
`-- pipeline_showcase/
    |-- index.html
    `-- styles.css
```

## Future Improvements

The project is already useful, but there is plenty of room to grow:

- Add drag-and-drop gesture support
- Add double-click gesture support
- Add gesture calibration for different users and camera distances
- Support multiple hand modes
- Add a settings panel for sensitivity and smoothing
- Add gesture labels directly on screen
- Improve low-light performance

## Final Summary

This project is a strong example of combining computer vision with human-computer interaction. It shows how a webcam, hand landmark detection, and desktop automation can work together to create a touch-free virtual mouse system.

The current version is promising because it already demonstrates the full loop from vision input to real cursor control. The structure is clean, the technologies are well chosen, and the project is ready to be demonstrated, improved, and expanded.
