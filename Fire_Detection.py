from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap
import cv2
import torch
import time
from ultralytics import YOLO

class VideoThread(QThread):
    change_pixmap_signal = Signal(QImage)
    fire_detected_signal = Signal()  # New signal for fire detection
    smoke_detected_signal = Signal()  # New signal for smoke detection
    
    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = True
        self.model = YOLO('yolov8.pt')
        
        # Add cooldown tracking to prevent spam
        self.last_fire_alert = 0
        self.last_smoke_alert = 0
        self.alert_cooldown = 1000  # Seconds between alerts
        
        # Check if CUDA is available
        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model.to(self.device)
            print("Using CUDA for YOLOv8 inference.")
        else:
            self.device = 'cpu'
            print("CUDA not available, using CPU.")

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize the frame
                resized_frame = cv2.resize(frame, (1024, 576))
                
                # Convert frame for YOLO
                frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
                frame_tensor /= 255.0
                
                # Perform YOLO inference
                results = self.model(frame_tensor)
                
                current_time = time.time()
                fire_detected = False
                smoke_detected = False
                
                # Process results and draw bounding boxes
                for result in results:
                    for box in result.boxes:
                        xmin, ymin, xmax, ymax = map(int, box.xyxy[0])
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        label = self.model.names[class_id]
                        
                        # Check for fire or smoke detections
                        if label.lower() == 'fire' and confidence > 0.5:
                            fire_detected = True
                            color = (0, 0, 255)  # Red for fire
                        elif label.lower() == 'smoke' and confidence > 0.5:
                            smoke_detected = True
                            color = (128, 128, 128)  # Gray for smoke
                        else:
                            color = (0, 255, 0)  # Green for other objects
                        
                        # Draw bounding box and label
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                        cv2.putText(frame, f"{label} {confidence:.2f}", 
                                  (xmin, ymin - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.5, color, 2)
                
                # Emit detection signals with cooldown
                if fire_detected and (current_time - self.last_fire_alert) > self.alert_cooldown:
                    self.fire_detected_signal.emit()
                    self.last_fire_alert = current_time
                    
                if smoke_detected and (current_time - self.last_smoke_alert) > self.alert_cooldown:
                    self.smoke_detected_signal.emit()
                    self.last_smoke_alert = current_time
                
                # Convert and emit frame
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

    def start_detection(self, camera_id, callback, fire_callback=None, smoke_callback=None):
        """
        Starts detection for a specific camera
        
        Args:
            camera_id: Camera identifier
            callback: Frame update callback
            fire_callback: Fire detection callback
            smoke_callback: Smoke detection callback
        """
        if camera_id not in self.threads:
            thread = VideoThread(camera_id)
            thread.change_pixmap_signal.connect(callback)
            if fire_callback:
                thread.fire_detected_signal.connect(fire_callback)
            if smoke_callback:
                thread.smoke_detected_signal.connect(smoke_callback)
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