import sys
import cv2
import numpy as np
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QImage, QPixmap
from ultralytics import YOLO
import torch

class YOLOv8App(QMainWindow):
    def __init__(self):
        super().__init__()

        # Load YOLOv8 model and move to GPU if available
        self.model = YOLO('yolov8.pt')

        # Check if CUDA is available and move the model to GPU
        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model.to(self.device)  # Move model to GPU
            print("Using CUDA for YOLOv8 inference.")
        else:
            self.device = 'cpu'
            print("CUDA not available, using CPU.")

        # Set up the video capture (webcam)
        self.cap = cv2.VideoCapture(0)

        # Create a timer to update the frame periodically
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        # Set up the UI
        self.label = QLabel(self)
        layout = QVBoxLayout()
        layout.addWidget(self.label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # Start the timer (30 frames per second, adjust as needed)
        self.timer.start(33)

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Convert frame to RGB (OpenCV uses BGR)
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            # Move frame to GPU if CUDA is available
            if self.device == 'cuda':
                frame_rgb = torch.from_numpy(frame_rgb).to(self.device).float()  # Send frame to GPU

            # Run YOLOv8 inference on the frame
            results = self.model(frame_rgb)

            # Post-process the results
            for result in results:
                for box in result.boxes:
                    xmin, ymin, xmax, ymax = box.xyxy[0]
                    confidence = box.conf[0]
                    class_id = box.cls[0]

                    new_box = {
                        'xmin': int(xmin.item()),
                        'ymin': int(ymin.item()),
                        'xmax': int(xmax.item()),
                        'ymax': int(ymax.item()),
                        'confidence': float(confidence.item()),
                        'class': int(class_id.item()),
                        'label': self.model.names[int(class_id.item())]
                    }

                    # Draw bounding box
                    cv2.rectangle(frame, (new_box['xmin'], new_box['ymin']), (new_box['xmax'], new_box['ymax']), (0, 255, 0), 2)
                    cv2.putText(frame, f"{new_box['label']} {new_box['confidence']:.2f}", 
                                (new_box['xmin'], new_box['ymin'] - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

            # Convert frame back to display in QLabel
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame_rgb.shape
            bytes_per_line = ch * w
            qimg = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
            self.label.setPixmap(QPixmap.fromImage(qimg))

    def closeEvent(self, event):
        self.cap.release()  # Release the video capture when closing the window
        super().closeEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = YOLOv8App()
    window.setWindowTitle("YOLOv8 Object Detection with CUDA and PySide6")
    window.show()
    sys.exit(app.exec())
