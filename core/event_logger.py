import csv


class EventLogger:
    def __init__(self):
        self.events = []

    def add_event(self, event):
        if event is None:
            return
        self.events.append(event)

    def get_events(self):
        return self.events

    def clear(self):
        self.events = []

    def save_to_csv(self, filepath):
        if not self.events:
            return False
        fieldnames = ["event_number", "frame_number", "detection_time", "motion_area_percent"]
        with open(filepath, "w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for event in self.events:
                writer.writerow(event)
        return True
