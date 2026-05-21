import os

# ==========================================
# WEAPON DETECTION SYSTEM CONFIGURATION
# ==========================================

# --- Model Settings ---
# Path to the trained YOLOv8 PyTorch model (.pt file)
MODEL_PATH = "best.pt"  # swapped for testing
# Confidence threshold for detections (e.g., 0.5 means 50%)
CONFIDENCE_THRESHOLD = 0.5

# --- Camera / Video Source Settings ---
# 0 for default webcam, 1 for external USB camera, or an IP Camera feed URL
CAMERA_INDEX = 0 
# Desired camera resolution
FRAME_WIDTH = 640
FRAME_HEIGHT = 480
# Throttle setting to prevent 100% CPU/GPU usage (burnout protection)
# 15-30 FPS is plenty for security cameras.
TARGET_FPS = 20 

# --- Alert System Settings ---
# Cooldown between alerts (in seconds) to prevent spamming
ALERT_COOLDOWN = 10 

# Enable/Disable Alert Methods
ENABLE_EMAIL_ALERTS = True
ENABLE_SMS_ALERTS = False

# Email Configuration (Requires an App Password for Gmail)
EMAIL_SENDER = "kannikaranibn2004@gmail.com"
EMAIL_PASSWORD = "ajaxjjiihbvgkays"
EMAIL_RECEIVER = "udayramesh45@gmail.com"
EMAIL_SUBJECT = "ALERT: Weapon Detected!"

# Twilio SMS Configuration (Sign up for Twilio to get these)
TWILIO_ACCOUNT_SID = "your_twilio_account_sid"
TWILIO_AUTH_TOKEN = "your_twilio_auth_token"
TWILIO_PHONE_NUMBER = "+1234567890"  # Your Twilio provided number
TARGET_PHONE_NUMBER = "+0987654321"  # Phone number to receive SMS
