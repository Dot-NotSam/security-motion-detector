import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.motion_detection import MotionDetector
from core.motion_analysis import MotionAnalyzer
from utils.validation import is_valid_video_path, is_valid_frame, is_valid_threshold, is_valid_min_area


def make_flat_frame(value=100):
    return np.full((200, 200), value, dtype=np.uint8)


def make_frame_with_motion_block():
    frame = np.full((200, 200), 100, dtype=np.uint8)
    frame[50:150, 50:150] = 250
    return frame


def make_frame_with_tiny_noise():
    frame = np.full((200, 200), 100, dtype=np.uint8)
    frame[10:13, 10:13] = 250
    return frame


def test_no_motion_between_identical_frames():
    detector = MotionDetector(threshold=25, min_area=500)
    frame = make_flat_frame()
    boxes, _ = detector.detect(frame, frame)
    assert len(boxes) == 0


def test_motion_detected_for_large_change():
    detector = MotionDetector(threshold=25, min_area=500)
    prev = make_flat_frame()
    curr = make_frame_with_motion_block()
    boxes, _ = detector.detect(prev, curr)
    assert len(boxes) > 0


def test_small_noise_is_ignored():
    detector = MotionDetector(threshold=25, min_area=500)
    prev = make_flat_frame()
    curr = make_frame_with_tiny_noise()
    boxes, _ = detector.detect(prev, curr)
    assert len(boxes) == 0


def test_motion_area_percent_calculation():
    analyzer = MotionAnalyzer(200, 200, area_percent_threshold=0.5)
    boxes = [(50, 50, 100, 100, 10000)]
    percent = analyzer.calculate_motion_percent(boxes)
    assert percent == 25.0


def test_motion_event_created_when_above_threshold():
    analyzer = MotionAnalyzer(200, 200, area_percent_threshold=0.5)
    boxes = [(50, 50, 100, 100, 10000)]
    result = analyzer.evaluate(boxes, frame_number=5)
    assert result["status"] == "MOTION DETECTED"
    assert result["event"] is not None
    assert result["event"]["frame_number"] == 5


def test_no_event_when_no_motion():
    analyzer = MotionAnalyzer(200, 200, area_percent_threshold=0.5)
    result = analyzer.evaluate([], frame_number=3)
    assert result["status"] == "NO MOTION"
    assert result["event"] is None


def test_invalid_video_path_rejected():
    assert is_valid_video_path("not_a_real_file.mp4") is False
    assert is_valid_video_path("") is False


def test_invalid_frame_rejected():
    assert is_valid_frame(None) is False
    assert is_valid_frame(np.zeros((0, 0))) is False


def test_valid_frame_accepted():
    frame = np.zeros((10, 10), dtype=np.uint8)
    assert is_valid_frame(frame) is True


def test_threshold_validation():
    assert is_valid_threshold(25) is True
    assert is_valid_threshold(0) is False
    assert is_valid_threshold(300) is False
    assert is_valid_threshold("abc") is False


def test_min_area_validation():
    assert is_valid_min_area(500) is True
    assert is_valid_min_area(-10) is False
    assert is_valid_min_area("xyz") is False
