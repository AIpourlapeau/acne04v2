from ultralytics import YOLO
import os
os.environ["CUDA_VISIBLE_DEVICES"] = "0"
import torch
torch.backends.cudnn.enabled = False
from tqdm import tqdm

trained_model = YOLO('runs/yolov8x_1280_acne_detection_23022024_2/weights/best.pt')

for thresh in tqdm(range(10,55,5)):
    metrics = trained_model.val(
        data = 'acne_clinical_data.yaml',
        imgsz=1280,
        batch=6,
        conf=thresh/100,  # object confidence threshold for detection
        iou=0.6,   # intersection over union (IoU) threshold for NMS
        save_json = True,
        )
    
    print('conf', thresh/100)
    print('map50:', metrics.box.map50)  # mean average precision at iou=0.5
    print('sensitivity', metrics.box.r) # recall / sensitivity
