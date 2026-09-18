import time


class MotionAnalyzer:
    def __init__(self, frame_width, frame_height, area_percent_threshold=0.5):
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.total_pixels = frame_width * frame_height
        self.area_percent_threshold = area_percent_threshold
        self.event_count = 0
        self.last_status = "NO MOTION"

    def set_frame_size(self, width, height):
        self.frame_width = width
        self.frame_height = height
        self.total_pixels = width * height

    def calculate_motion_percent(self, boxes):
        if self.total_pixels == 0:
            return 0.0
        motion_pixels = sum(w * h for (_, _, w, h, _) in boxes)
        percent = (motion_pixels / self.total_pixels) * 100
        return round(percent, 2)

    def evaluate(self, boxes, frame_number):
        motion_percent = self.calculate_motion_percent(boxes)
        is_motion = len(boxes) > 0 and motion_percent >= self.area_percent_threshold

        event = None
        if is_motion:
            self.event_count += 1
            event = {
                "event_number": self.event_count,
                "frame_number": frame_number,
                "detection_time": time.strftime("%Y-%m-%d %H:%M:%S"),
                "motion_area_percent": motion_percent,
            }
            self.last_status = "MOTION DETECTED"
        else:
            self.last_status = "NO MOTION"

        return {
            "status": self.last_status,
            "motion_percent": motion_percent,
            "event": event,
            "event_count": self.event_count,
        }

    def reset(self):
        self.event_count = 0
        self.last_status = "NO MOTION"
