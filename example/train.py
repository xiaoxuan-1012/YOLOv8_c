
from ultralytics import YOLO
import torch 
if __name__ == "__main__":
    device = 0 if torch.cuda.is_available() else 'cpu'
    model = YOLO(r"ultralytics/models/v8/yolov8n_c.yaml") 

    model.train(data="data.yaml",
                epochs=5,         #example
                batch=2,          #example  
                lr0=0.01,
                optimizer="SGD",
                momentum=0.9,
                weight_decay=0.01,
                workers=0,
                device=device,
                augment=True,
                hsv_h=0.01,
                hsv_s=0.01,
                hsv_v=0.01,
                degrees=5,
                flipud=0.0,
                fliplr=0.5
                )
