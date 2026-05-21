import cv2
from detector import WeaponDetector
import config

print("==========================================")
print(" WEAPON DETECTION IMAGE TEST ")
print("==========================================")

# Initialize the detector
detector = WeaponDetector(model_path=config.MODEL_PATH, conf_thresh=config.CONFIDENCE_THRESHOLD)

# Load the test image
image_path = "threat_snapshot.jpg"
frame = cv2.imread(image_path)

if frame is None:
    print(f"[ERROR] Could not load '{image_path}'. Ensure the file exists.")
    exit(1)

print(f"[INFO] Processing '{image_path}'...")
annotated_frame, threat_detected, threat_details = detector.process_frame(frame)

if threat_detected:
    print(f"[ALERT] Threat detected: {threat_details}")
else:
    print("[INFO] No threat detected.")

# Save the annotated image instead of displaying it (useful for automated testing)
output_path = "threat_snapshot_annotated.jpg"
cv2.imwrite(output_path, annotated_frame)
print(f"[INFO] Annotated image saved to '{output_path}'.")
print("==========================================")
