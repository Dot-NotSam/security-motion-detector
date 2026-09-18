import cv2


def draw_motion_boxes(frame, boxes):
    for (x, y, w, h, area) in boxes:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    return frame


def draw_status_overlay(frame, status, motion_percent, event_count):
    color = (0, 0, 255) if status == "MOTION DETECTED" else (0, 200, 0)
    cv2.putText(frame, status, (15, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, color, 2)
    cv2.putText(frame, "Area: " + str(motion_percent) + "%", (15, 60),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    cv2.putText(frame, "Events: " + str(event_count), (15, 85),
                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
    return frame


def convert_frame_for_tkinter(frame):
    import cv2 as cv
    rgb_frame = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
    return rgb_frame
