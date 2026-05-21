import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from twilio.rest import Client
import threading
import time
import cv2
import config

class AlertSystem:
    """
    Handles sending asynchronous SMS and Email notifications.
    Uses multi-threading to prevent the video stream from freezing while sending alerts over the network.
    """
    
    def __init__(self):
        self.last_alert_time = 0.0
        if config.ENABLE_SMS_ALERTS:
            self.twilio_client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            
    def trigger_alert(self, frame, detection_info="Weapon"):
        """
        Triggers an alert if the cooldown time has passed.
        Spawns background threads so the OpenCV camera doesn't freeze.
        """
        current_time = time.time()
        
        if (current_time - self.last_alert_time) > config.ALERT_COOLDOWN:
            print(f"[ALERT] Threat Detected ({detection_info})! Initiating alert sequence...")
            
            # Save the frame temporarily to attach to email
            image_path = "threat_snapshot.jpg"
            cv2.imwrite(image_path, frame)
            
            # Start Email Thread
            if config.ENABLE_EMAIL_ALERTS:
                # daemon=True ensures this thread is killed immediately if the main script stops
                email_thread = threading.Thread(target=self._send_email, args=(detection_info, image_path), daemon=True)
                email_thread.start()
                
            # Start SMS Thread
            if config.ENABLE_SMS_ALERTS:
                # daemon=True ensures this thread is killed immediately if the main script stops
                sms_thread = threading.Thread(target=self._send_sms, args=(detection_info,), daemon=True)
                sms_thread.start()
                
            # Update the cooldown timestamp
            self.last_alert_time = current_time

    def _send_email(self, detection_info, image_path):
        """Internal method to send email via SMTP."""
        try:
            print("[INFO] Preparing Email...")
            msg = MIMEMultipart()
            msg['From'] = config.EMAIL_SENDER
            msg['To'] = config.EMAIL_RECEIVER
            msg['Subject'] = config.EMAIL_SUBJECT
            
            body_text = f"CRITICAL ALERT: A potential threat ({detection_info}) was detected by the security system. See attached image."
            msg.attach(MIMEText(body_text, 'plain'))
            
            # Attach the snapshot image
            with open(image_path, 'rb') as f:
                img_data = f.read()
                image = MIMEImage(img_data, name="snapshot.jpg")
                msg.attach(image)
                
            # Connect to Gmail SMTP server
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(config.EMAIL_SENDER, config.EMAIL_PASSWORD)
            server.send_message(msg)
            server.quit()
            
            print("[SUCCESS] Email Alert Sent successfully!")
        except Exception as e:
            print(f"[ERROR] Failed to send email: {e}")

    def _send_sms(self, detection_info):
        """Internal method to send SMS via Twilio API."""
        try:
            print("[INFO] Preparing SMS...")
            message = self.twilio_client.messages.create(
                body=f"SECURITY ALERT: A potential threat ({detection_info}) has been detected by camera feeds! Please check the premises immediately.",
                from_=config.TWILIO_PHONE_NUMBER,
                to=config.TARGET_PHONE_NUMBER
            )
            print(f"[SUCCESS] SMS Alert Sent successfully! SID: {message.sid}")
        except Exception as e:
            print(f"[ERROR] Failed to send SMS: {e}")
