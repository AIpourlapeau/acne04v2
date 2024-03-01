from ultralytics import YOLO
import pandas as pd
import numpy as np
import math

# Load a model
model = YOLO('runs/trained_acne_seg/yolov8x_1280_acne_detection_09022024_/weights/best.pt') 

# Run batched inference on a list of images
results = model(
    source='../ACNE04/Classification/JPEGImages',
    stream=True,
    imgsz=1280,
    conf=0.0,  # object confidence threshold for detection
    iou=0.6,  # intersection over union (IoU) threshold for NMS
    max_det=300, # maximum number of detections allowed per image
    )  


def bbox2circle(bbox):
    x1,y1,x2,y2=bbox
    X=int((x1+x2)/2)
    Y=int((y1+y2)/2)
    r=int(math.sqrt((X-x1)**2+(Y-y1)**2))
    return (X,Y), r

list_coord = []
paths = []
scores = []
# Process results list
for result in results:
    boxes = result.boxes # Boxes object for bbox outputs
    masks = result.masks  # Masks object for segmentation masks outputs
    keypoints = result.keypoints  # Keypoints object for pose outputs
    probs = result.probs  # Class probabilities for classification outputs
    path = result.path  # Contains the path to the input image
   
    
    coord = []
    for box in boxes: 
        x_center, y_center = box.xywh[0].cpu().numpy()[:2]
        width, height = box.xywh[0].cpu().numpy()[2:]
        radius = max(width/2, height/2)

        xmin, ymin = x_center-width/2, y_center-height/2
        xmax, ymax = x_center+width/2, y_center+height/2
        pre_pf = [xmin, ymin, xmax, ymax]
        cpf, rpf = bbox2circle(pre_pf)
        
        conf = box.conf.cpu().numpy().item()
        coord.append([cpf, rpf, conf])

    dict_coord = {'acne' : coord}
    
    if len(boxes) > 0:
        score = np.mean(boxes.conf.cpu().numpy())
    else:
        score = 0.0

    scores.append(score)
    paths.append(path)
    list_coord.append(dict_coord)
    

data = {'image name': paths,
        'score': scores,
        'group_acne_dict': list_coord}
    
df = pd.DataFrame.from_dict(data)
df.to_csv('Yolov8x_acne04_model1280_conf_0.csv', index=False)




