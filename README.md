# Security Motion Detector

## Overview

Security Motion Detector is a desktop Computer Vision application built with Python, OpenCV and Tkinter. It monitors a fixed camera feed or a recorded video file and detects motion by comparing consecutive frames. It does not perform any face or person identification — it only reports whether movement occurred and where.

## Problem Statement

Traditional CCTV setups require a person to constantly watch a live feed to notice movement, which is impractical for continuous monitoring. This project automates that task using basic image processing techniques taught in a Computer Vision course, without relying on deep learning models.

## Objectives

- Detect motion in a fixed-camera video stream using classical CV techniques
- Highlight the region where motion occurred with a bounding box
- Report motion status, motion area percentage, and event count in real time
- Log motion events with timestamps for later review
- Keep the system lightweight enough to run on a normal laptop without a GPU

## Features

- Live webcam or recorded video input
- Real-time motion detection using frame differencing
- Adjustable detection threshold and minimum motion area
- Bounding boxes drawn around moving regions
- On-screen "MOTION DETECTED" / "NO MOTION" status
- Motion area percentage calculation
- Motion event counter and detection log table
- Export detection log to CSV
- No face, person or license plate recognition

## Computer Vision Techniques

- Grayscale conversion
- Gaussian blur for noise removal
- Frame differencing between consecutive frames
- Binary thresholding
- Morphological operations (dilation, erosion, opening)
- Contour detection
- Bounding rectangle extraction
- Region of interest based filtering using minimum area

## Technologies Used

- Python 3
- OpenCV (opencv-python)
- NumPy
- Tkinter (GUI)
- Pillow (frame rendering in Tkinter)
- pytest (testing)

## Project Structure

```
security-motion-detector/
├── main.py
├── gui/
│   └── app.py
├── core/
│   ├── video_capture.py
│   ├── preprocessing.py
│   ├── motion_detection.py
│   ├── motion_analysis.py
│   └── event_logger.py
├── utils/
│   ├── validation.py
│   └── visualization.py
├── tests/
│   ├── test_preprocessing.py
│   └── test_motion_detection.py
├── requirements.txt
├── .gitignore
├── README.md
├── statement.md
└── REPORT.md
```

## Installation

1. Ensure Python 3.9+ is installed
2. Create and activate a virtual environment (optional but recommended)
3. Install dependencies:

```
pip install -r requirements.txt
```

## How to Run

```
python main.py
```

This opens the Security Dashboard. From there you can:

1. Click **Start Camera** to use your webcam, or **Select Video** to load a video file
2. Click **Start Monitoring** to begin motion detection
3. Watch the live feed, status label, motion area, and event count update
4. Click **Stop Monitoring** or **Stop Camera** to pause
5. Click **Save Detection Log** to export events as a CSV file
6. Click **Reset** to clear all counters and the log table

## How Motion Detection Works

1. A frame is captured from the camera or video
2. It is converted to grayscale and smoothed with a Gaussian blur
3. The absolute difference between the current and previous smoothed frame is computed
4. The difference image is thresholded into a binary mask
5. Morphological dilation, opening and erosion clean up noise in the mask
6. Contours are extracted from the cleaned mask
7. Contours smaller than the minimum area setting are discarded as noise
8. Remaining contours are converted into bounding boxes and drawn on the frame
9. The total motion area is compared against the frame size to get a motion percentage
10. If the motion percentage exceeds the configured threshold, a motion event is logged

## Testing

Run all tests with:

```
pytest tests/
```

Tests cover preprocessing output, no-motion frames, small noise rejection, genuine motion detection, motion area calculation, event creation, and input validation.

## Screenshots

*(Add screenshots of the running application here — dashboard idle state, motion detected state, and saved CSV log.)*

## Future Enhancements

- Support multiple camera inputs simultaneously
- Add a configurable region-of-interest mask editable from the GUI
- Add email or notification alerts on motion events
- Add a live motion-area graph over time
- Add background-subtraction based detection as an alternative mode
