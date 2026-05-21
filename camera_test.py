import cv2
import config

def test_camera():
    """
    A simple script to verify your OpenCV installation and camera drivers 
    are working before layering YOLOv8 on top.
    """
    print(f"[INFO] Testing Camera Index: {config.CAMERA_INDEX}")
    
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)
    
    if not cap.isOpened():
        print(f"[ERROR] Cannot open camera {config.CAMERA_INDEX}")
        print("Ensure no other application (like Zoom or Teams) is using the camera.")
        return
        
    print("[SUCCESS] Camera initialized successfully!")
    print("[INFO] Press 'q' to close the test window.")
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to grab frames.")
            break
            
        cv2.putText(frame, "Hardware Test Pass. Press 'q' to quit.", (20, 40), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
                    
        cv2.imshow("Hardware Test", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
            
    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Test complete.")

if __name__ == "__main__":
    test_camera()
