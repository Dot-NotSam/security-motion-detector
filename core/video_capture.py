import cv2


class VideoSource:
    def __init__(self):
        self.cap = None
        self.source_type = None
        self.frame_count = 0

    def open_camera(self, camera_index=0):
        self.release()
        self.cap = cv2.VideoCapture(camera_index)
        if not self.cap.isOpened():
            self.cap = None
            return False
        self.source_type = "camera"
        self.frame_count = 0
        return True

    def open_video(self, path):
        self.release()
        self.cap = cv2.VideoCapture(path)
        if not self.cap.isOpened():
            self.cap = None
            return False
        self.source_type = "video"
        self.frame_count = 0
        return True

    def read_frame(self):
        if self.cap is None:
            return False, None
        ok, frame = self.cap.read()
        if ok:
            self.frame_count += 1
        return ok, frame

    def is_opened(self):
        return self.cap is not None and self.cap.isOpened()

    def release(self):
        if self.cap is not None:
            self.cap.release()
        self.cap = None
        self.source_type = None
        self.frame_count = 0
