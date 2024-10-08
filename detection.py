import ultralytics
from ultralytics import YOLO
import cv2

# Load model
model = YOLO('yolov8.pt')

# Inference
cap = cv2.VideoCapture(0)
while cap.isOpened():
    ret, frame = cap.read()
    if ret:
        results = model(frame)
        boxes = []

        for result in results:
            for box in result.boxes:
                # Extract box coordinates and other attributes
                xmin, ymin, xmax, ymax = box.xyxy[0]  # Assuming box.xyxy gives you the coordinates
                confidence = box.conf[0]  # Assuming box.conf gives you the confidence score
                class_id = box.cls[0]  # Assuming box.cls gives you the class ID
                
                new_box = {
                    'xmin': int(xmin.item()),  # Convert to integer
                    'ymin': int(ymin.item()),  # Convert to integer
                    'xmax': int(xmax.item()),  # Convert to integer
                    'ymax': int(ymax.item()),  # Convert to integer
                    'confidence': float(confidence.item()),  # Convert to float
                    'class': int(class_id.item()),  # Convert to integer
                    'label': model.names[int(class_id.item())]  # Get the class label
                }
                boxes.append(new_box)

                # Draw bounding box
                cv2.rectangle(frame, (new_box['xmin'], new_box['ymin']), (new_box['xmax'], new_box['ymax']), (0, 255, 0), 2)
                cv2.putText(frame, f"{new_box['label']} {new_box['confidence']:.2f}", (new_box['xmin'], new_box['ymin'] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        
        cv2.imshow('frame', frame)
        
    if cv2.waitKey(1) == ord('q'):
        break