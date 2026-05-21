# How to Train the Weapon Detection Model on Google Colab

Since training a deep learning model requires a strong GPU, it's highly recommended you use Google Colab (which provides free T4 GPUs). 

Follow these steps to train your model and get the `best.pt` file for this project.

### Step 1: Prepare your Dataset
You need images of guns, knives, etc., with bounding box annotations in YOLO format. You can easily find these on **Roboflow Universe** (search for "Weapon Detection" or "Gun Detection"). Export the dataset in "YOLOv8" format, which usually gives you a download link or snippet.

### Step 2: Open Google Colab
Go to [Google Colab](https://colab.research.google.com/) and create a "New Notebook".
Go to **Runtime > Change runtime type** and set the Hardware Accelerator to **T4 GPU**.

### Step 3: Run the Training Code
Create a new code cell in Colab, paste the following code, and run it:

```python
# 1. Install ultralytics (YOLOv8)
!pip install ultralytics

# 2. Check GPU availability
import torch
print(f"Is GPU available? {torch.cuda.is_available()}")

# 3. Download the dataset from Roboflow (replace with your specific snippet)
# Example (Do not run this exact sub-step if you don't have the key, get your own from roboflow):
# !pip install roboflow
# from roboflow import Roboflow
# rf = Roboflow(api_key="YOUR_API_KEY")
# project = rf.workspace("workspace-name").project("weapon-detection")
# version = project.version(1)
# dataset = version.download("yolov8")

# 4. Train the Model! 
# data='path/to/data.yaml' is the file inside your downloaded dataset folder.
# epochs=50 is a good starting point. You can increase to 100 for better accuracy.
from ultralytics import YOLO

# Load a pretrained Nano model (fastest)
model = YOLO('yolov8n.pt') 

# Start training. 
# Make sure to replace dataset/data.yaml with the actual path Colab downloaded it to!
results = model.train(data='dataset/data.yaml', epochs=50, imgsz=640)

# 5. The trained weights will be saved in a specific directory.
# Usually: runs/detect/train/weights/best.pt
print("Training Complete! Download 'best.pt' from the folder icon on the left.")
```

### Step 4: Download and Deploy
After training finishes, open the file explorer on the left sidebar in Colab.
Navigate to `runs` -> `detect` -> `train` -> `weights`.
Right-click `best.pt` and click **Download**.

Place this `best.pt` file into your local `WeaponDetectionSystem` folder, and the system is ready!
