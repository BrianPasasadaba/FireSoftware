from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap
import cv2
import torch
import time
from ultralytics import YOLO

class VideoThread(QThread):
    change_pixmap_signal = Signal(QImage)
    fire_detected_signal = Signal(str)  # Now includes feed identifier
    smoke_detected_signal = Signal(str)  # Now includes feed identifier
    
    def __init__(self, camera_id=0, feed_id='main'):
        super().__init__()
        self.camera_id = camera_id
        self.feed_id = feed_id
        self.running = True
        self.model = YOLO('yolov8.pt')
        
        # Add cooldown tracking to prevent spam
        self.last_alert = 0
        self.alert_cooldown = 300  # Seconds between alerts
        
        # Check if CUDA is available
        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model.to(self.device)
            print("Using CUDA for YOLOv8 inference.")
        else:
            self.device = 'cpu'
            print("CUDA not available, using CPU.")

        print("Available classes:", self.model.names)

    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        frame_count = 0
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize the frame
                resized_frame = cv2.resize(frame, (1120, 640))
                
                # Convert frame for YOLO
                frame_tensor = torch.from_numpy(resized_frame).permute(2, 0, 1).unsqueeze(0).float()
                frame_tensor /= 255.0
                
                # Perform YOLO inference
                results = self.model(frame_tensor, stream=True)
                
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
                        if (label == 'Fire' or label == 'Fires') and confidence > 0.4:
                            fire_detected = True
                            color = (0, 0, 255)  # Red for fire
                            print(f"Fire detected with confidence {confidence:.2f}")
                        elif (label == 'smoke' or label == 'smokes') and confidence > 0.5:
                            smoke_detected = True
                            color = (128, 128, 128)  # Gray for smoke
                            print(f"Smoke detected with confidence {confidence:.2f}")
                        else:
                            color = (0, 255, 0)

                        
                        # Draw bounding box and label
                        cv2.rectangle(frame, (xmin, ymin), (xmax, ymax), color, 2)
                        cv2.putText(frame, f"{label} {confidence:.2f}", 
                                  (xmin, ymin - 10), 
                                  cv2.FONT_HERSHEY_SIMPLEX, 
                                  0.5, color, 2)
                
                # Emit detection signals with cooldown
                # Emit detection signals
                if smoke_detected and (current_time - self.last_alert) > self.alert_cooldown:
                    print("Attempting to emit smoke signal...")
                    try:
                        self.smoke_detected_signal.emit(self.feed_id)
                        self.last_alert = current_time
                        print("Smoke signal emitted successfully")
                    except Exception as e:
                        print(f"Error emitting smoke signal: {e}")
                
                if fire_detected and (current_time - self.last_alert) > self.alert_cooldown:
                    print("Attempting to emit fire signal...")
                    try:
                        self.fire_detected_signal.emit(self.feed_id)
                        self.last_alert = current_time
                        print("Fire signal emitted successfully")
                    except Exception as e:
                        print(f"Error emitting fire signal: {e}")
                
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

    def start_detection(self, camera_id, callback, fire_callback=None, smoke_callback=None, feed_id='main'):
        """
        Starts detection for a specific camera
        
        Args:
            camera_id: Camera identifier
            callback: Frame update callback
            fire_callback: Fire detection callback
            smoke_callback: Smoke detection callback
        """
        if camera_id not in self.threads:
            thread = VideoThread(camera_id, feed_id)
            thread.change_pixmap_signal.connect(callback)
            if fire_callback:
                # Modify connection to handle feed_id
                thread.fire_detected_signal.connect(
                    lambda detected_feed_id=feed_id: fire_callback(detected_feed_id)
                )
            if smoke_callback:
                # Modify connection to handle feed_id
                thread.smoke_detected_signal.connect(
                    lambda detected_feed_id=feed_id: smoke_callback(detected_feed_id)
                )
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