import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from PIL import Image, ImageTk

from core.video_capture import VideoSource
from core.preprocessing import preprocess_frame
from core.motion_detection import MotionDetector
from core.motion_analysis import MotionAnalyzer
from core.event_logger import EventLogger
from utils.validation import is_valid_video_path, is_valid_frame, is_valid_threshold, is_valid_min_area
from utils.visualization import draw_motion_boxes, draw_status_overlay, convert_frame_for_tkinter


class SecurityDashboard:
    def __init__(self, root):
        self.root = root
        self.root.title("Security Motion Detector")
        self.root.geometry("980x680")

        self.video_source = VideoSource()
        self.detector = MotionDetector(threshold=25, min_area=800)
        self.analyzer = MotionAnalyzer(640, 480, area_percent_threshold=0.5)
        self.logger = EventLogger()

        self.prev_gray = None
        self.monitoring = False
        self.running_feed = False
        self.video_path = None

        self.build_layout()
        self.update_loop()

    def build_layout(self):
        top_frame = tk.Frame(self.root)
        top_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.video_label = tk.Label(self.root, bg="black")
        self.video_label.pack(side=tk.TOP, padx=10, pady=10)

        control_frame = tk.Frame(self.root)
        control_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Button(control_frame, text="Start Camera", command=self.start_camera).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Select Video", command=self.select_video).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Stop Camera", command=self.stop_camera).grid(row=0, column=2, padx=5)
        tk.Button(control_frame, text="Start Monitoring", command=self.start_monitoring).grid(row=0, column=3, padx=5)
        tk.Button(control_frame, text="Stop Monitoring", command=self.stop_monitoring).grid(row=0, column=4, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_all).grid(row=0, column=5, padx=5)
        tk.Button(control_frame, text="Save Detection Log", command=self.save_log).grid(row=0, column=6, padx=5)

        param_frame = tk.Frame(self.root)
        param_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        tk.Label(param_frame, text="Threshold:").grid(row=0, column=0, padx=5)
        self.threshold_var = tk.IntVar(value=25)
        tk.Scale(param_frame, from_=1, to=100, orient=tk.HORIZONTAL, variable=self.threshold_var,
                 command=self.on_threshold_change, length=150).grid(row=0, column=1, padx=5)

        tk.Label(param_frame, text="Min Area:").grid(row=0, column=2, padx=5)
        self.min_area_var = tk.IntVar(value=800)
        tk.Scale(param_frame, from_=100, to=5000, orient=tk.HORIZONTAL, variable=self.min_area_var,
                 command=self.on_min_area_change, length=150).grid(row=0, column=3, padx=5)

        status_frame = tk.Frame(self.root)
        status_frame.pack(side=tk.TOP, fill=tk.X, padx=10, pady=5)

        self.status_label = tk.Label(status_frame, text="NO MOTION", font=("Arial", 16, "bold"), fg="green")
        self.status_label.grid(row=0, column=0, padx=15)

        self.area_label = tk.Label(status_frame, text="Motion Area: 0.0%", font=("Arial", 11))
        self.area_label.grid(row=0, column=1, padx=15)

        self.events_label = tk.Label(status_frame, text="Motion Events: 0", font=("Arial", 11))
        self.events_label.grid(row=0, column=2, padx=15)

        self.frame_label = tk.Label(status_frame, text="Current Frame: 0", font=("Arial", 11))
        self.frame_label.grid(row=0, column=3, padx=15)

        log_frame = tk.Frame(self.root)
        log_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True, padx=10, pady=5)

        tk.Label(log_frame, text="Detection Log").pack(anchor="w")

        columns = ("event", "frame", "time", "area")
        self.log_tree = ttk.Treeview(log_frame, columns=columns, show="headings", height=8)
        self.log_tree.heading("event", text="Event #")
        self.log_tree.heading("frame", text="Frame #")
        self.log_tree.heading("time", text="Detection Time")
        self.log_tree.heading("area", text="Motion Area %")
        self.log_tree.pack(fill=tk.BOTH, expand=True)

    def on_threshold_change(self, value):
        if is_valid_threshold(value):
            self.detector.set_threshold(int(value))

    def on_min_area_change(self, value):
        if is_valid_min_area(value):
            self.detector.set_min_area(int(value))

    def start_camera(self):
        if not self.video_source.open_camera(0):
            messagebox.showerror("Camera Error", "Unable to access the camera.")
            return
        self.video_path = None
        self.prev_gray = None
        self.running_feed = True

    def select_video(self):
        path = filedialog.askopenfilename(
            filetypes=[("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv")]
        )
        if not path:
            return
        if not is_valid_video_path(path):
            messagebox.showerror("Invalid File", "Please select a valid video file.")
            return
        if not self.video_source.open_video(path):
            messagebox.showerror("Video Error", "Unable to open the selected video.")
            return
        self.video_path = path
        self.prev_gray = None
        self.running_feed = True

    def stop_camera(self):
        self.running_feed = False
        self.monitoring = False
        self.video_source.release()
        self.video_label.config(image="")

    def start_monitoring(self):
        if not self.video_source.is_opened():
            messagebox.showwarning("No Source", "Start a camera or select a video first.")
            return
        self.monitoring = True

    def stop_monitoring(self):
        self.monitoring = False

    def reset_all(self):
        self.analyzer.reset()
        self.logger.clear()
        self.prev_gray = None
        for row in self.log_tree.get_children():
            self.log_tree.delete(row)
        self.status_label.config(text="NO MOTION", fg="green")
        self.area_label.config(text="Motion Area: 0.0%")
        self.events_label.config(text="Motion Events: 0")
        self.frame_label.config(text="Current Frame: 0")

    def save_log(self):
        if not self.logger.get_events():
            messagebox.showinfo("No Events", "There are no motion events to save.")
            return
        path = filedialog.asksaveasfilename(defaultextension=".csv",
                                             filetypes=[("CSV files", "*.csv")])
        if not path:
            return
        self.logger.save_to_csv(path)
        messagebox.showinfo("Saved", "Detection log saved successfully.")

    def process_frame(self, frame):
        height, width = frame.shape[0], frame.shape[1]
        self.analyzer.set_frame_size(width, height)

        gray = preprocess_frame(frame)

        if self.prev_gray is None:
            self.prev_gray = gray
            return frame, {"status": "NO MOTION", "motion_percent": 0.0,
                            "event": None, "event_count": self.analyzer.event_count}

        boxes, _ = self.detector.detect(self.prev_gray, gray)
        self.prev_gray = gray

        result = self.analyzer.evaluate(boxes, self.video_source.frame_count)
        self.logger.add_event(result["event"])

        frame = draw_motion_boxes(frame, boxes)
        frame = draw_status_overlay(frame, result["status"], result["motion_percent"], result["event_count"])

        return frame, result

    def update_log_table(self, event):
        if event is None:
            return
        self.log_tree.insert("", tk.END, values=(
            event["event_number"], event["frame_number"],
            event["detection_time"], event["motion_area_percent"]
        ))

    def update_loop(self):
        if self.running_feed and self.video_source.is_opened():
            ok, frame = self.video_source.read_frame()
            if ok and is_valid_frame(frame):
                if self.monitoring:
                    frame, result = self.process_frame(frame)
                    self.status_label.config(
                        text=result["status"],
                        fg="red" if result["status"] == "MOTION DETECTED" else "green"
                    )
                    self.area_label.config(text="Motion Area: " + str(result["motion_percent"]) + "%")
                    self.events_label.config(text="Motion Events: " + str(result["event_count"]))
                    self.frame_label.config(text="Current Frame: " + str(self.video_source.frame_count))
                    self.update_log_table(result["event"])

                rgb_frame = convert_frame_for_tkinter(frame)
                image = Image.fromarray(rgb_frame)
                image.thumbnail((900, 500))
                photo = ImageTk.PhotoImage(image=image)
                self.video_label.config(image=photo)
                self.video_label.image = photo
            else:
                if self.video_path is not None:
                    self.running_feed = False
                    self.monitoring = False

        self.root.after(30, self.update_loop)
