import os


def is_valid_video_path(path):
    if not path:
        return False
    if not os.path.isfile(path):
        return False
    valid_extensions = (".mp4", ".avi", ".mov", ".mkv", ".wmv")
    return path.lower().endswith(valid_extensions)


def is_valid_frame(frame):
    if frame is None:
        return False
    if not hasattr(frame, "shape"):
        return False
    if len(frame.shape) < 2:
        return False
    if frame.shape[0] == 0 or frame.shape[1] == 0:
        return False
    return True


def is_valid_threshold(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False
    return 0 < value <= 255


def is_valid_min_area(value):
    try:
        value = int(value)
    except (ValueError, TypeError):
        return False
    return value >= 0
