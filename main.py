import cv2
import config
from detector import WeaponDetector
from alert_system import AlertSystem
import sys
import time

def main():
    print("==========================================")
    print(" WEAPON DETECTION & ALERT SYSTEM STARTING ")
    print("==========================================")

    # Initialize Modules
    detector = WeaponDetector(model_path=config.MODEL_PATH, conf_thresh=config.CONFIDENCE_THRESHOLD)
    alert_system = AlertSystem()

    # Initialize Hardware Camera
    print(f"[INFO] Initializing Camera at index: {config.CAMERA_INDEX}")
    cap = cv2.VideoCapture(config.CAMERA_INDEX)
    
    # Set camera resolution 
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.FRAME_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.FRAME_HEIGHT)

    # Verify camera opened successfully
    if not cap.isOpened():
        print(f"[ERROR] Could not open camera {config.CAMERA_INDEX}.")
        print("Please check your camera drivers and hardware connections.")
        sys.exit(1)

    print("[INFO] System ready. Press 'q' to quit the stream.")
    
    # Calculate target frame time for throttling
    target_frame_time = 1.0 / getattr(config, 'TARGET_FPS', 30)

    try:
        # Main video processing loop
        while True:
            loop_start = time.time()
            
            # Read a frame from the camera
            success, frame = cap.read()
            
            if not success:
                print("[WARNING] Failed to grab frame from camera. Exiting...")
                break
                
            # Process the frame through our YOLO model
            annotated_frame, threat_detected, threat_details = detector.process_frame(frame)
            
            # If a weapon is detected, trigger the alert system
            if threat_detected:
                # We pass the original clean frame to the alert system, or the annotated one.
                # Usually, authorities prefer to see the bounding box directly.
                alert_system.trigger_alert(annotated_frame, detection_info=threat_details)

            # Overlay a system status text on the frame
            status_text = f"Status: {'THREAT DETECTED' if threat_detected else 'SECURE'}"
            color = (0, 0, 255) if threat_detected else (0, 255, 0)
            cv2.putText(annotated_frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                        1, color, 2, cv2.LINE_AA)

            # Display the resulting frame
            cv2.imshow('Weapon Detection System - Live Feed', annotated_frame)
            
            # Listen for keyboard interrupts
            # Wait 1ms and check if the 'q' key was pressed to exit
            if cv2.waitKey(1) & 0xFF == ord('q'):
                print("[INFO] 'q' pressed. Shutting down system...")
                break
                
            # --- HARDWARE BURN PROTECT: FPS THROTTLING ---
            processing_time = time.time() - loop_start
            sleep_time = target_frame_time - processing_time
            if sleep_time > 0:
                time.sleep(sleep_time)

    except KeyboardInterrupt:
        print("\n[INFO] Manual interruption detected. Shutting down securely...")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] Application crashed: {e}")
    finally:
        # --- HARDWARE SAFEGUARD: GUARANTEED RELEASE ---
        # This block ALWAYS runs, even if the code crashes, preventing locked drivers/burned hardware.
        print("[INFO] Releasing hardware resources to prevent driver lockups...")
        if cap.isOpened():
            cap.release()
        cv2.destroyAllWindows()
        print("==========================================")
        print(" SYSTEM OFFLINE ")
        print("==========================================")

if __name__ == "__main__":
    main()
