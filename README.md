# Weapon Detection and Alert System

This is a real-time object detection system designed to identify threats (guns, knives, etc.) from live CCTV or webcam feeds and instantly alert authorities via Email or SMS. 

Built using **Python, PyTorch, YOLOv8 (ultralytics), OpenCV, and Twilio**.

## Installation

1. Create a virtual environment (optional but recommended).
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Place your trained YOLOv8 model in the root directory and name it `best.pt` (or update `config.py` with your model's name). If you don't have one, the script will automatically download the default COCO `yolov8n.pt` for testing.

## Configuration

Open `config.py` and set your desired configurations:
- `ENABLE_EMAIL_ALERTS = True` and fill in your Gmail App Password.
- `ENABLE_SMS_ALERTS = True` and fill in your Twilio Account SID and Auth Token.
- `CAMERA_INDEX`: 0 for external/default webcams, or an IP address for network cameras.

## Running the System

To start the detection system:
```bash
python main.py
```

To test if your camera works without YOLO:
```bash
python camera_test.py
```

---

## 🎤 Presentation Talking Points

If you are presenting this project, here is a structured way to explain the architecture and design decisions:

### 1. The Core Objective
> *"This project aims to bridge the gap between passive surveillance and active security. Currently, CCTV cameras just record crimes as they happen. This system acts as an AI watchman that actively analyzes frames and alerts authorities the second a threat is identified."*

### 2. The Model Architecture (PyTorch & YOLOv8)
> *"For the AI brain, I utilized the **YOLOv8** architecture built on **PyTorch**. YOLO stands for 'You Only Look Once'. Instead of scanning an image multiple times like older models, YOLO passes the image through a deep neural network exactly once, mapping bounding boxes and class probabilities simultaneously. This makes it incredibly fast and perfect for real-time video processing, achieving high frame rates without sacrificing accuracy."*

### 3. The Video Pipeline (OpenCV)
> *"To handle hardware interfacing, I'm using **OpenCV** (Open Source Computer Vision Library). It continuously captures raw pixel arrays from the video feed. Inside the main loop, we feed these NumPy arrays directly into PyTorch's memory space for instantaneous inference."*

### 4. The Multi-Threaded Alert System
> *"One of the technical challenges in real-time computer vision is network latency. If the system pauses to send an email or SMS, the video feed drops frames or freezes. To solve this, I designed a **multi-threaded Alert System**. When a weapon is recognized, the main thread spawns a background Daemon thread that handles formulating the email payload, attaching the snapshot image, and establishing the SMTP/Twilio API connection. The main camera feed remains butter-smooth."*

### 5. Configurable Constraints & Cooldowns
> *"The system is designed with state management in mind. To prevent spamming authorities with 30 emails a second while a weapon is in frame, I implemented an **Alert Cooldown** mechanism in `config.py` that throttles notifications while ensuring the threat status is persistently overlaid on the live feed."*

