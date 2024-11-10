import cv2
import torch
from ultralytics import YOLO
from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap

class VideoThread(QThread):
    change_pixmap_signal = Signal(QImage)
    
    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = True
        self.model = YOLO('yolov8.pt')

        # Check if CUDA is available and move the model to GPU
        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model.to(self.device)  # Move model to GPU
            print("Using CUDA for YOLOv8 inference.")
        else:
            self.device = 'cpu'
            print("CUDA not available, using CPU.")

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize the frame to a size that is divisible by 32
                resized_frame = cv2.resize(frame, (640, 640))
                
                # Convert the frame from HWC to BCHW format
                frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
                
                # Normalize the frame tensor
                frame_tensor /= 255.0
                
                # Perform YOLO inference
                results = self.model(frame_tensor)
                
                # Process results and draw bounding boxes
                for result in results:
                    for box in result.boxes:
                        xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        label = self.model.names[class_id]
                        
                        # Draw bounding box and label
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), (0, 255, 0), 2)
                        cv2.putText(frame, f"{label} {confidence:.2f}", 
                                  (xmin, ymin - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.5, (0, 255, 0), 2)
                
                # Convert frame to Qt format for display
                rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
                
                # UNCOMMENT THIS LINE  AND LINE BELOW TO SCALE THE IMAGE
                # scaled_image = qt_image.scaled(640, 480)
                
                # Emit the processed frame
                # CHANGE PARAMETER TO scaled_image TO SCALE THE IMAGE
                self.change_pixmap_signal.emit(qt_image)
        
        cap.release()

    def stop(self):
        """Stops the video thread"""
        self.running = False
        self.wait()

class DetectionManager:
    """Manages video detection threads for multiple feeds"""
    def __init__(self):
        self.threads = {}

    def start_detection(self, camera_id, callback):
        """Starts detection for a specific camera"""
        if camera_id not in self.threads:
            thread = VideoThread(camera_id)
            thread.change_pixmap_signal.connect(callback)
            thread.start()
            self.threads[camera_id] = thread

    def stop_detection(self, camera_id):
        """Stops detection for a specific camera"""
        if camera_id in self.threads:
            self.threads[camera_id].stop()
            del self.threads[camera_id]

    def stop_all(self):
        """Stops all detection threads"""
        for thread in self.threads.values():
            thread.stop()
        self.threads.clear()