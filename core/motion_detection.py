import cv2
import numpy as np


class MotionDetector:
    def __init__(self, threshold=25, min_area=800):
        self.threshold = threshold
        self.min_area = min_area

    def set_threshold(self, threshold):
        self.threshold = threshold

    def set_min_area(self, min_area):
        self.min_area = min_area

    def compute_difference(self, prev_gray, curr_gray):
        return cv2.absdiff(prev_gray, curr_gray)

    def apply_threshold(self, diff_frame):
        _, thresh = cv2.threshold(diff_frame, self.threshold, 255, cv2.THRESH_BINARY)
        return thresh

    def apply_morphology(self, thresh_frame):
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        dilated = cv2.dilate(thresh_frame, kernel, iterations=2)
        opened = cv2.morphologyEx(dilated, cv2.MORPH_OPEN, kernel)
        eroded = cv2.erode(opened, kernel, iterations=1)
        return eroded

    def find_motion_contours(self, mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        valid_boxes = []
        for c in contours:
            area = cv2.contourArea(c)
            if area < self.min_area:
                continue
            x, y, w, h = cv2.boundingRect(c)
            valid_boxes.append((x, y, w, h, area))
        return valid_boxes

    def detect(self, prev_gray, curr_gray):
        diff = self.compute_difference(prev_gray, curr_gray)
        thresh = self.apply_threshold(diff)
        mask = self.apply_morphology(thresh)
        boxes = self.find_motion_contours(mask)
        return boxes, mask
