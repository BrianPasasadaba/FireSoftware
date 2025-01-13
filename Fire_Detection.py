from PySide6.QtCore import QThread, Signal
from PySide6.QtGui import QImage, QPixmap
import cv2
import torch
import time
from ultralytics import YOLO
import queue
import numpy as np

class FrameStreamThread(QThread):
    """Handles video capture and streaming"""
    frame_available_signal = Signal(QImage)
    
    def __init__(self, camera_id=0):
        super().__init__()
        self.camera_id = camera_id
        self.running = True
        self.frame_queue = queue.Queue(maxsize=1)  # Only keep the latest frame
        
    def run(self):
        cap = cv2.VideoCapture(self.camera_id)
        
        while self.running and cap.isOpened():
            ret, frame = cap.read()
            if ret:
                # Resize the frame
                resized_frame = cv2.resize(frame, (1120, 640))
                
                # Convert to QImage
                rgb_image = cv2.cvtColor(resized_frame, cv2.COLOR_BGR2RGB)
                h, w, ch = rgb_image.shape
                bytes_per_line = ch * w
                qt_image = QImage(rgb_image.data.tobytes(), w, h, bytes_per_line, QImage.Format_RGB888)
                
                # Emit the frame
                self.frame_available_signal.emit(qt_image)
                
                # Update queue with latest frame
                try:
                    # Clear the queue if full
                    if self.frame_queue.full():
                        self.frame_queue.get_nowait()
                    self.frame_queue.put_nowait(resized_frame)
                except queue.Full:
                    pass  # Skip frame if queue is full
                
                # Optional: Limit frame rate if needed
                time.sleep(0.03)  # ~30 FPS
        
        cap.release()

    def stop(self):
        self.running = False
        self.wait()

class DetectionThread(QThread):
    """Handles object detection on frames"""
    fire_detected_signal = Signal(str)
    smoke_detected_signal = Signal(str)
    
    def __init__(self, frame_queue, feed_id='main'):
        super().__init__()
        self.frame_queue = frame_queue
        self.feed_id = feed_id
        self.running = True
        
        # Initialize YOLO model
        self.model = YOLO('yolov8.pt')
        
        # Add cooldown tracking to prevent spam
        self.last_alert = 0
        self.alert_cooldown = 30  # Seconds between alerts
        
        # Check if CUDA is available
        if torch.cuda.is_available():
            self.device = 'cuda'
            self.model.to(self.device)
            print("Using CUDA for YOLOv8 inference.")
        else:
            self.device = 'cpu'
            print("CUDA not available, using CPU.")

    def run(self):
        while self.running:
            try:
                # Try to get the latest frame quickly without blocking
                frame = self.frame_queue.get_nowait()
                
                # Convert frame for YOLO
                frame_tensor = torch.from_numpy(frame).permute(2, 0, 1).unsqueeze(0).float()
                frame_tensor /= 255.0
                
                # Perform detection
                current_time = time.time()
                fire_detected = False
                smoke_detected = False
                
                results = self.model(frame_tensor, stream=True)
                
                for result in results:
                    for box in result.boxes:
                        confidence = float(box.conf[0])
                        class_id = int(box.cls[0])
                        label = self.model.names[class_id]

                        # Check for fire or smoke detections
                        if (label == 'Fire' or label == 'Fires') and confidence > 0.4:
                            fire_detected = True
                            print(f"Fire detected with confidence {confidence:.2f}")
                        elif (label == 'smoke' or label == 'smokes') and confidence > 0.5:
                            smoke_detected = True
                            print(f"Smoke detected with confidence {confidence:.2f}")
                
                # Emit detection signals with cooldown
                if smoke_detected and (current_time - self.last_alert) > self.alert_cooldown:
                    self.smoke_detected_signal.emit(self.feed_id)
                    self.last_alert = current_time
                
                if fire_detected and (current_time - self.last_alert) > self.alert_cooldown:
                    self.fire_detected_signal.emit(self.feed_id)
                    self.last_alert = current_time
                
            except queue.Empty:
                # No frame available, sleep briefly
                time.sleep(0.01)
            except Exception as e:
                print(f"Detection error: {e}")

    def stop(self):
        self.running = False
        self.wait()

class DetectionManager:
    """Manages video detection for multiple feeds"""
    def __init__(self):
        self.stream_threads = {}
        self.detection_threads = {}
        self.feed_to_camera_map = {}  # Map feed_ids to camera_ids

    def start_detection(self, camera_id, frame_callback, fire_callback=None, smoke_callback=None, feed_id='main'):
        """
        Starts detection for a specific camera
        
        Args:
            camera_id: Camera identifier
            frame_callback: Frame update callback
            fire_callback: Fire detection callback
            smoke_callback: Smoke detection callback
            feed_id: Unique identifier for the feed
        """
        # Store mapping between feed_id and camera_id
        self.feed_to_camera_map[feed_id] = camera_id

        if camera_id not in self.stream_threads:
            # Create frame queue
            frame_queue = queue.Queue(maxsize=1)
            
            # Create and start streaming thread
            stream_thread = FrameStreamThread(camera_id)
            stream_thread.frame_queue = frame_queue
            stream_thread.frame_available_signal.connect(frame_callback)
            stream_thread.start()
            
            # Create and start detection thread
            detection_thread = DetectionThread(frame_queue, feed_id)
            if fire_callback:
                detection_thread.fire_detected_signal.connect(
                    lambda detected_feed_id=feed_id: fire_callback(detected_feed_id)
                )
            if smoke_callback:
                detection_thread.smoke_detected_signal.connect(
                    lambda detected_feed_id=feed_id: smoke_callback(detected_feed_id)
                )
            detection_thread.start()
            
            # Store threads
            self.stream_threads[camera_id] = stream_thread
            self.detection_threads[camera_id] = detection_thread

    def stop_detection(self, feed_id):
        """Stops detection for a specific feed"""
        if feed_id in self.feed_to_camera_map:
            camera_id = self.feed_to_camera_map[feed_id]
            print(f"Stopping detection for feed {feed_id} (camera: {camera_id})")
            
            if camera_id in self.stream_threads:
                self.stream_threads[camera_id].stop()
                self.detection_threads[camera_id].stop()
                del self.stream_threads[camera_id]
                del self.detection_threads[camera_id]
            
            del self.feed_to_camera_map[feed_id]

    def stop_all(self):
        """Stops all detection threads"""
        for thread in self.stream_threads.values():
            thread.stop()
        for thread in self.detection_threads.values():
            thread.stop()
        self.stream_threads.clear()
        self.detection_threads.clear()