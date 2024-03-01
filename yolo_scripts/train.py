from ultralytics import YOLO
from datetime import date
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import torch
torch.backends.cudnn.enabled = False
 
# Load the model.
model = YOLO('yolov8x.pt')
 
# Training.
"""
- data: Path to the dataset YAML file.
- imgsz: The image size.pyth The default resolution is 640.
- epochs: Number of epochs we want to train for.
- patience: Number of epochs to wait without improvement in validation metrics before early stopping the training.
- batch: The batch size for data loader. You may increase or decrease it according to your GPU memory availability.
- name: Name of the results directory for runs/detect.
"""
results = model.train(
    data='acne_detection.yaml',
    imgsz=1280,
    epochs=600, 
    patience=200,
    batch=6,
    name='yolov8x_1280_acne_detection_'+date.today().strftime("%d%m%Y")+'_')
