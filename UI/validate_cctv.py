from PySide6.QtCore import QObject, Signal, QThread
import cv2

class RTSPValidator(QObject):
    validation_finished = Signal(bool, str)  # Signal to notify validation result

    def __init__(self, rtsp_url):
        super().__init__()
        self.rtsp_url = rtsp_url

    def run(self):
        """Perform RTSP validation."""
        try:
            cap = cv2.VideoCapture(self.rtsp_url)
            is_valid = cap.isOpened()
            cap.release()
            if is_valid:
                self.validation_finished.emit(True, "")
            else:
                self.validation_finished.emit(False, "Invalid RTSP credentials. Please check your input.")
        except Exception as e:
            self.validation_finished.emit(False, f"Validation error: {str(e)}")
