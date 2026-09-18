# Project Report: Security Motion Detector

## 1. Introduction

Security Motion Detector is a desktop Computer Vision application that monitors a fixed camera or a pre-recorded video and detects motion by comparing consecutive frames. The system is built using classical image processing techniques taught in an undergraduate Computer Vision syllabus — no deep learning models are used. The application is presented through a Tkinter-based desktop dashboard that shows the live feed, current motion status, motion area percentage, and a log of detection events.

## 2. Problem Statement

Continuously watching a static camera feed to catch movement is impractical for a human observer over long durations. This project addresses that problem by automatically comparing consecutive frames from a fixed camera, identifying regions of significant pixel-level change, and reporting them as motion events in real time, while deliberately avoiding any identification of people or objects.

## 3. Objectives

- Implement a frame-differencing based motion detection pipeline
- Apply preprocessing (grayscale conversion, Gaussian blur) to reduce noise-driven false positives
- Use thresholding and morphological operations to isolate meaningful motion regions
- Extract contours and bounding boxes for detected motion
- Compute a motion area percentage and use it to decide motion state
- Log each motion event with frame number, timestamp and area percentage
- Present all of this through a simple, functional Tkinter GUI
- Ensure the application runs on a standard laptop without a GPU

## 4. Functional Requirements

- The system shall accept input from either a webcam or a video file
- The system shall preprocess each frame (grayscale + blur) before comparison
- The system shall compute the absolute difference between consecutive preprocessed frames
- The system shall threshold the difference image into a binary motion mask
- The system shall apply morphological operations to clean the mask
- The system shall extract contours and filter out those below a minimum area
- The system shall draw bounding boxes around valid motion regions
- The system shall calculate and display the motion area as a percentage of the frame
- The system shall display "MOTION DETECTED" or "NO MOTION" based on the current state
- The system shall count and display the number of motion events
- The system shall log each motion event with event number, frame number, detection time and motion area percentage
- The system shall allow exporting the event log as a CSV file
- The system shall allow the user to adjust the detection threshold and minimum motion area from the GUI

## 5. Non-Functional Requirements

- **Performance**: The pipeline should process frames fast enough for smooth near real-time feedback on a typical laptop CPU
- **Usability**: Controls (Start/Stop Camera, Select Video, Start/Stop Monitoring, Reset, Save Log) should be clearly labeled and require no technical knowledge to operate
- **Reliability**: The application should keep running even if a frame read fails or the camera disconnects mid-session
- **Error Handling**: Invalid video files, unavailable cameras, and invalid parameter values must be handled gracefully without crashing the application
- **Maintainability**: The codebase is split into small, single-responsibility modules (capture, preprocessing, detection, analysis, logging, GUI) to make it easy to modify or extend
- **Privacy**: No facial, personal or identity data is captured, processed or stored; only anonymous motion metadata (frame number, timestamp, area percentage) is logged, and all processing happens locally

## 6. System Architecture

The application follows a simple layered pipeline architecture:

```
[Video Source] -> [Preprocessing] -> [Motion Detection] -> [Motion Analysis] -> [Event Logger]
                                                                   |
                                                                   v
                                                            [Tkinter GUI]
```

- `core/video_capture.py` manages the OpenCV video source (camera index or file path)
- `core/preprocessing.py` converts frames to grayscale and applies Gaussian blur
- `core/motion_detection.py` performs frame differencing, thresholding, morphology and contour extraction
- `core/motion_analysis.py` converts detected regions into a motion percentage and event decision
- `core/event_logger.py` stores and exports motion events
- `gui/app.py` ties all modules together and renders the dashboard
- `utils/validation.py` and `utils/visualization.py` provide supporting helper functions

## 7. Workflow

1. User starts the camera or selects a video file through the GUI
2. The GUI polls the video source on a fixed interval using Tkinter's `after()` scheduler
3. Each frame is preprocessed (grayscale + blur)
4. The current preprocessed frame is compared with the previous one via absolute differencing
5. The difference image is thresholded and cleaned using morphological operations
6. Contours are extracted and filtered by minimum area
7. Remaining contours become bounding boxes, drawn on the display frame
8. The motion area percentage is calculated and compared against the configured threshold
9. If motion is significant, an event is recorded and the status changes to "MOTION DETECTED"
10. The GUI updates the video panel, status label, motion percentage, event counter and log table
11. The user may save the accumulated log as a CSV file at any point

## 8. UML / Design Description

**Class: VideoSource** — manages `cv2.VideoCapture`, exposes `open_camera`, `open_video`, `read_frame`, `is_opened`, `release`.

**Class: MotionDetector** — holds `threshold` and `min_area` parameters; exposes `compute_difference`, `apply_threshold`, `apply_morphology`, `find_motion_contours`, and the combined `detect` method.

**Class: MotionAnalyzer** — holds frame dimensions and the area-percentage threshold; exposes `calculate_motion_percent` and `evaluate`, which produces the status, motion percentage, and optional event dictionary.

**Class: EventLogger** — holds an in-memory list of event dictionaries; exposes `add_event`, `get_events`, `clear`, and `save_to_csv`.

**Class: SecurityDashboard** — the Tkinter GUI controller; owns one instance of each of the above classes and wires user actions (button clicks, slider changes) to pipeline calls, and updates on-screen widgets each polling cycle.

## 9. Computer Vision Methodology

### 9.1 Frame Differencing

Motion is detected by computing the absolute pixel-wise difference between two consecutive preprocessed (grayscale, blurred) frames using `cv2.absdiff`. Large differences indicate regions where the scene content changed between frames, which — for a fixed camera — usually corresponds to movement.

### 9.2 Preprocessing

Each frame is converted from BGR to grayscale to reduce the data to a single channel and simplify comparison. A Gaussian blur is then applied to suppress small-scale sensor noise and minor lighting flicker that would otherwise be misread as motion.

### 9.3 Thresholding

The difference image is converted into a binary mask using `cv2.threshold` with `THRESH_BINARY`. Pixels whose difference exceeds the configurable threshold value are marked as "changed" (white); all others are set to black.

### 9.4 Morphological Operations

The binary mask is refined using dilation (to merge nearby motion pixels into connected regions), followed by an opening operation and erosion (to remove small, isolated noise blobs that survive thresholding). This produces cleaner, more reliable contours.

### 9.5 Contour Detection

`cv2.findContours` is used on the cleaned mask to identify connected regions of change. Each contour's area is computed with `cv2.contourArea`, and contours smaller than the configured minimum area are discarded as noise rather than genuine motion.

### 9.6 Motion Analysis

For each remaining contour, a bounding rectangle is computed with `cv2.boundingRect`. The combined area of all valid bounding boxes is compared against the total frame area to produce a motion area percentage. If this percentage meets or exceeds the configured threshold, the frame is classified as containing motion and an event is recorded.

## 10. Implementation

The system is implemented in Python using OpenCV for all image processing steps and Tkinter with Pillow for the GUI. The pipeline modules are intentionally decoupled from the GUI so that the detection logic could be reused in a script or a different interface without modification. Detection parameters (threshold, minimum area) are exposed as GUI sliders and applied directly to the `MotionDetector` instance at runtime.

## 11. GUI

The dashboard is built with Tkinter and includes:

- A live video/frame display panel
- Buttons: Start Camera, Stop Camera, Select Video, Start Monitoring, Stop Monitoring, Reset, Save Detection Log
- Sliders for adjusting the detection threshold and minimum motion area
- Status indicators: motion status text (MOTION DETECTED / NO MOTION), motion area percentage, event count, and current frame number
- A scrollable table showing the detection log (event number, frame number, detection time, motion area percentage)

## 12. Testing

Testing is done with `pytest`. Test cases cover:

- Preprocessing output shape and type correctness
- Motion detection returning no boxes for identical frames (no motion)
- Motion detection returning boxes for a frame pair with a large synthetic change (motion present)
- Small, noise-sized changes being correctly ignored
- Motion area percentage calculation correctness
- Motion event creation when the area threshold is exceeded
- No event creation when there is no significant motion
- Validation helpers correctly rejecting invalid video paths, invalid frames, invalid threshold values, and invalid minimum area values

*(Add actual pytest console output here after running the test suite locally.)*

## 13. Results

*(Add actual results here after running the application — e.g., screenshots of the dashboard in idle and motion-detected states, and observations from testing with a real webcam or sample video. No results are fabricated in this report; this section is intentionally left as a placeholder for real data.)*

## 14. Challenges

- Balancing the threshold and minimum area parameters to avoid both false positives (from lighting changes, camera noise) and false negatives (missing slow or small movements)
- Keeping the GUI responsive while continuously reading and processing video frames
- Handling camera/video failures without crashing the application

## 15. Learnings

- Practical application of frame differencing, thresholding, and morphological operations for a real detection task
- Understanding how parameter tuning directly affects detection sensitivity and robustness
- Structuring a Computer Vision project into clean, testable, single-responsibility modules
- Building a functional desktop GUI around a live video processing pipeline

## 16. Future Enhancements

- Support for multiple simultaneous camera feeds
- User-configurable region-of-interest masking from within the GUI
- Alerting via email, SMS, or desktop notification on motion events
- A live chart of motion area percentage over time
- An alternative detection mode using background subtraction (e.g., MOG2) for comparison against frame differencing

## 17. References

- OpenCV Documentation: https://docs.opencv.org/
- Python `tkinter` Documentation: https://docs.python.org/3/library/tkinter.html
- Course Computer Vision syllabus material on frame differencing, thresholding, morphological operations, and contour detection
