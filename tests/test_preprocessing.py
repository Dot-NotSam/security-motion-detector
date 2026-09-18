import numpy as np
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.preprocessing import to_grayscale, remove_noise, preprocess_frame


def make_dummy_frame():
    return np.random.randint(0, 255, (100, 150, 3), dtype=np.uint8)


def test_to_grayscale_shape():
    frame = make_dummy_frame()
    gray = to_grayscale(frame)
    assert gray.shape == (100, 150)


def test_remove_noise_shape_preserved():
    frame = make_dummy_frame()
    gray = to_grayscale(frame)
    blurred = remove_noise(gray)
    assert blurred.shape == gray.shape


def test_remove_noise_even_kernel_handled():
    frame = make_dummy_frame()
    gray = to_grayscale(frame)
    blurred = remove_noise(gray, kernel_size=10)
    assert blurred.shape == gray.shape


def test_preprocess_frame_returns_2d_array():
    frame = make_dummy_frame()
    result = preprocess_frame(frame)
    assert len(result.shape) == 2
