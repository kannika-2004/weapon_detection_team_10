import cv2
import config
import os
import sys

try:
    from ultralytics import YOLO
except ImportError:
    print("[ERROR] ultralytics package not found. Please run: pip install -r requirements.txt")
    print("If you are running in restricted environment, YOLO won't import without ultralytics.")
    # Exit gracefully if missing dependencies to prevent cryptic errors
    sys.exit(1)

class WeaponDetector:
    """
    Wrapper class around the YOLOv8 model for weapon detection.
    Responsible for loading the model and performing inference on video frames.
    """
    def __init__(self, model_path=config.MODEL_PATH, conf_thresh=config.CONFIDENCE_THRESHOLD):
        self.conf_thresh = conf_thresh
        print(f"[INFO] Loading YOLO model from {model_path}...")
        
        # Load the PyTorch YOLOv8 model.
        # Ensure the model exists before trying to load it
        if not os.path.exists(model_path):
            print(f"[WARNING] Model file '{model_path}' not found!")
            print("Please ensure you have placed your trained YOLOv8 model in the project directory.")
            print("For now, we will attempt to download the default 'yolov8n.pt' just to verify the system works.")
            self.model = YOLO("yolov8n.pt")
        else:
            self.model = YOLO(model_path)
            
        print("[INFO] Model loaded successfully.")

    def process_frame(self, frame):
        """
        Runs object detection on a single camera frame.
        
        Args:
            frame: A NumPy array representing an image frame from OpenCV.
            
        Returns:
            annotated_frame: The frame with drawn bounding boxes.
            threat_detected: Boolean indicating if a weapon was detected.
            threat_details: String containing the names of detected weapons.
        """
        
        # Run inference using YOLO object tracking/detection
        # stream=True is efficient for video feeds
        results = self.model(frame, conf=self.conf_thresh, verbose=False)
        
        threat_detected = False
        detected_weapons = []
        
        # The result object contains the bounding boxes and classes
        for r in results:
            # We draw the boxes directly using the YOLO builtin plotter
            annotated_frame = r.plot()
            
            # Check if any detections were made in this frame
            boxes = r.boxes
            if len(boxes) > 0:
                for box in boxes:
                    # Get class ID
                    cls_id = int(box.cls[0].item())
                    # Get class name
                    cls_name = self.model.names[cls_id]
                    
                    # For a presentation, normally your model will ONLY have classes 
                    # like 'gun', 'knife', etc. If you are using the default yolov8n model
                    # for testing, it has 80 COCO classes. Let's assume ANY detection
                    # by your custom model is a threat. 
                    
                    # If using standard COCO model just for demo, you might want to only 
                    # trigger on specific classes like person, knife, etc.
                    # Since this is a custom WEAPON model, we assume all detections are threats:
                    detected_weapons.append(cls_name)
                    threat_detected = True
                    
        # Remove duplicates
        detected_weapons = list(set(detected_weapons))
        threat_details = ", ".join(detected_weapons) if detected_weapons else "Unknown"

        return annotated_frame, threat_detected, threat_details
