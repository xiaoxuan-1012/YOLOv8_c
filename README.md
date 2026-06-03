# Intelligent Recognition of Shale Laminae Based on an Improved YOLOv8n Model(YOLOv8_c)

## Project Overview
**YOLOv8_c** is a deep learning model built upon the YOLOv8 architecture, specifically designed for the detection and classification of laminae in shale thin-section images. The model introduces targeted improvements  to enhance the recognition capability for fine laminae structures and laminae under complex backgrounds.
## Installation

### Requirements
- Conda 4.12.0
- python 3.8+
- PyTorch/CUDA support (optional)

### set up 

```bash
# Clone the repository
git clone https://github.com/xiaoxuan-1012/YOLOV8_c
cd YOLOV8_c

# Install dependencies (adjust based on your environment)
pip install -r requirements.txt

```

## Dataset

Our experiments use a proprietary dataset of shale thin‑section images from the Lower Silurian Longmaxi Formation (Sichuan Basin), containing 1,412 images with YOLO‑format labels for three laminae types (dark, bright, shell).

**Due to repository size limitations and institutional data policies, only 100 example image‑label pairs are included in this repository** for code testing and format reference`dataset_org`.

- Each `.txt` label follows YOLO format: `class id x_center y_center width height`
- The dataset is split into **train/valid/test** sets with a radio of **8:1:1** using `data_split.py`
- Class names are defined in `data.yaml`

For access to the complete dataset, please contact the corresponding author.



## Training

We compare two models: **original YOLOv8n**(baseline)  and  **YOLOv8_c** (improved).  Both models are trained using the exact same hyperparameters for a fair comparison.

### Hyperparameters (common for both)

| Parameter | Value |
|-----------|-------|
| Epochs | 500 |
| Batch size | 4 |
| Optimizer | SGD |
| Learning rate | 0.01 |
| Momentum | 0.9 |
| Weight decay | 0.01 |
| Input size | 640×640 |
| Data augmentation | HSV (h=0.01, s=0.01, v=0.01), rotation (±5°), flip (0.5) |

### Model configuration files

- **Original YOLOv8n**: uses the default `ultralytics/models/v8/yolov8n.yaml` 
- **YOLOv8_c** (our model): uses `ultralytics/models/v8/yolov8n_c.yaml`
### Training commands

All training is done via `train.py`. Below are the two commands:

```bash
# Train original YOLOv8n
python train.py --model ultralytics/models/v8/yolov8n.yaml


# Train YOLOv8_c
python train.py --model ultralytics/models/v8/yolov8n_c.yaml
```

To verify everything works, run a short training on the provided example dataset (in example/):

```bash
python train.py --model ultralytics/models/v8/yolov8n_c.yaml --data data.yaml --epochs 5 --batch 2 

```
This will run 5 epochs on a few images and produce a weight file in `example/runs/train/`
 
### Trained Weights

We provide the final model weights for both baseline and our improved model, trained on our proprietary dataset (see paper for exact mAP values).

| Model | Weight file | Description |
|-------|-------------|-------------|
| Original YOLOv8n | `runs/train/yolov8n weights/best.pt` | Baseline model  |
| YOLOv8_c (ours) | `runs/train/yolov8_c weights/best.pt` | Our improved model |

You can directly use these weights for inference or resume training:

```bash
# Inference with our improved model
python predict.py --weights yolov8_c weights/best.pt --source /path/to/images

```


## CAM Visualization

We provide a heatmap generation tool (`heatmap.py`) to visualize the model's attention regions using Grad-CAM. This helps interpret which parts of the shale thin‑section image contribute most to the laminae classification.

The script `heatmap.py` supports multiple CAM variants:

- `gradCAM` – Gradient‑weighted CAM (default)
- `gradCAMpp` – Improved gradient weighting
- `XGradCAM` – Another variant

### Usage

```bash
python heatmap.py --weights /path/to/model.pt --source /path/to/image.jpg --method gradCAM

```

## License

This project is under the AGPL-3.0 licence. See the LICENSE file for more information.

## Acknowledgments

We thank the contributors of YOLOv8 for their open‑source work:

> Glenn Jocher, Ayush Chaurasia, Jing Qiu. (2023). **Ultralytics YOLO (Version 8.0.0)** [Computer software]. https://github.com/ultralytics/ultralytics

























