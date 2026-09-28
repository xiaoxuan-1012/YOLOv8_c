# Intelligent Recognition of Shale Laminae Based on an Improved YOLOv8n Model (YOLOv8_c)

This repository contains the code accompanying the paper *"Intelligent Recognition of Shale Laminae Based on an Improved YOLOv8n Model"* (submitted to *Computers & Geosciences*).

## Project Overview

**YOLOv8_c** is a task-oriented object-detection framework built on YOLOv8n for the automated recognition of laminae in shale thin-section images. Shale laminae are thin, elongated targets with weak or gradational boundaries, and different lamina types may show similar colours and textures, so the baseline detector is modified in three ways that each address a specific failure mode:

| Modification | Location | Purpose |
|---|---|---|
| **CBAM** | Backbone (P3, P4) + neck | Enhances discriminative lamina features and suppresses background interference |
| **C2f_Faster** | Neck | Improves fine-scale feature extraction for thin, closely spaced laminae at lower computational cost |
| **EIoU loss** | Detection head | Strengthens bounding-box regression for targets with high aspect ratios |

Three lamina categories are detected: **dark laminae** (class_0), **bright laminae** (class_1) and **shell laminae** (class_2).

## Main Results

Evaluated on the held-out test set. All models were trained on the same dataset partition with identical settings.

| Model | Precision (%) | Recall (%) | mAP@0.5 (%) | Params (M) | GFLOPs | FPS |
|---|---|---|---|---|---|---|
| Mask R-CNN | 62.5 | 63.2 | 65.7 | 44.40 | 134.4 | 8 |
| YOLOv5n | 64.7 | 65.2 | 67.8 | 1.93 | 4.5 | 32 |
| YOLOv8n (baseline) | 73.1 | 73.8 | 72.2 | 3.04 | 8.7 | 25 |
| **YOLOv8_c (ours)** | **79.4** | **80.3** | **81.1** | **2.75** | **8.1** | **23** |

YOLOv8_c improves mAP@0.5 by 8.9 percentage points (12.3% relative) over the baseline while using 9.3% fewer parameters and 6.9% fewer GFLOPs. Per-class AP@0.5 is 78.0% (dark), 81.5% (bright) and 83.8% (shell).

Module ablation (each added individually to YOLOv8n):

| Configuration | mAP@0.5 (%) |
|---|---|
| YOLOv8n (baseline) | 72.2 |
| + CBAM | 76.8 |
| + C2f_Faster | 76.1 |
| + EIoU | 73.3 |
| **YOLOv8_c (all three)** | **81.1** |

## Installation

### Requirements

- Python 3.8.8, Conda 4.12.0
- PyTorch 2.8.0
- Ultralytics 8.3.180
- PyQt5 5.15.11

Development and evaluation were performed on an Intel Core i5-1135G7 (2.40 GHz) with 16 GB RAM and an NVIDIA GeForce MX450 (2 GB).

### Setup

```bash
git clone https://github.com/xiaoxuan-1012/YOLOv8_c
cd YOLOv8_c
pip install -r requirements.txt
```

## Dataset

Thin-section images were collected from three shale-bearing units of the Sichuan Basin: the Lower Silurian **Longmaxi** Formation, the Lower Jurassic **Ziliujing** Formation and the Middle Jurassic **Lianggaoshan** Formation. All images were acquired under **plane-polarized light** on a Nikon Eclipse LV100ND polarizing microscope with constant imaging settings; cross-polarized images were excluded so that lamina identification and annotation remain consistent.

The dataset contains **2,957 annotated lamina instances**:

| Class | Name | Instances | Share |
|---|---|---|---|
| 0 | Dark lamina | 1,076 | 36.4% |
| 1 | Bright lamina | 1,032 | 34.9% |
| 2 | Shell lamina | 849 | 28.7% |

Annotation notes:

- Labels follow the YOLO format: `class_id x_center y_center width height` (normalized).
- Classification was not based on brightness alone, but on the combined assessment of brightness, texture, continuity, morphology and petrographic characteristics; all annotations were reviewed by experienced geologists.
- Partitioning into **train / val / test = 8:1:1** is performed at the level of thin-section images (not annotation instances) using `data_split.py`, so that no image contributes to more than one subset.
- Class names are defined in `data.yaml`.

**Availability.** Owing to the 100 MB file-size limit of this repository, **120 example image–label pairs** are provided in `dataset_org/` as a format reference and for testing the code. The complete dataset is available from the corresponding author upon reasonable request.

## Training

### Hyperparameters

The same settings are used for every model and every ablation configuration, so that differences in performance are attributable to the network configuration rather than to hyperparameter tuning. The values follow those reported by Tang et al. (2025) for YOLOv8-based mineral recognition in optical images and were adopted empirically rather than through systematic optimization.

| Parameter | Value |
|---|---|
| Epochs | 500 |
| Batch size | 4 |
| Optimizer | SGD |
| Learning rate | 0.01 |
| Momentum | 0.9 |
| Weight decay | 0.01 |
| Input size | 640 × 640 |

### Data augmentation

Augmentation is applied **after partitioning and to the training subset only**, so that evaluation rests entirely on original thin-section images. The operations were chosen so that the sedimentological meaning of the laminae is preserved:

| Operation | Setting | Rationale |
|---|---|---|
| Rotation | ±5° | Accommodates slight tilt of laminae relative to the image frame without altering their bedding-parallel orientation |
| Hue / saturation | h = 0.01, s = 0.01 | Simulates variation in illumination and image acquisition while preserving the relative brightness relationships that define the three classes |
| Vertical flip | **not used** | Reverses the stratigraphic younging direction |

### Model configuration files

- **YOLOv8n (baseline)**: `ultralytics/models/v8/yolov8n.yaml`
- **YOLOv8_c (ours)**: `ultralytics/models/v8/yolov8_c.yaml`

### Commands

```bash
# Baseline
python train.py --model ultralytics/models/v8/yolov8n.yaml

# YOLOv8_c
python train.py --model ultralytics/models/v8/yolov8_c.yaml
```

To check that the environment works, run a short training on the bundled example data:

```bash
python train.py --model ultralytics/models/v8/yolov8_c.yaml --data data.yaml --epochs 5 --batch 2
```

This produces a weight file under `runs/train/`.

### Ablation experiments

The ablation studies reported in the paper are reproduced by training with the corresponding configuration file; all other settings remain unchanged.


```bash
python train.py --model ultralytics/models/ablation_module/yolov8n_cbam.yaml

```
| Experiment | Configuration |
|---|---|
| Individual modules | `ultralytics/models/ablation_module/yolov8n_cbam.yaml`, `yolov8n_c2ff.yaml`, `yolov8n_eiou.yaml` |
| Augmentation | `yolov8n_c.yaml` with the relevant augmentation parameters disabled |
| CBAM placement (A1–A6) | `yolov8n_cbam_a1.yaml` … `yolov8n_cbam_a6.yaml` |

## Trained Weights

All model configuration files are located under `ultralytics/models/`.

| Experiment | Configuration file |
|---|---|
| Individual modules | `ablation_module/yolov8n_cbam.yaml`,`ablation_module/yolov8n_c2ff.yaml`,`ablation_module/yolov8n_eiou.yaml` |
| Augmentation | `v8/yolov8_c.yaml`, with the relevant augmentation parameters disabled |
| CBAM placement (A1–A6) | `ablation_cbam/yolov8n_cbam_a1.yaml` … `ablation_cbam/yolov8n_cbam_a6.yaml` |

Inference:

```bash
python predict.py --weights runs/train/yolov8_c/weights/best.pt --source /path/to/images
```

## Grad-CAM Visualization

`heatmap.py` generates attention heatmaps that show which parts of a thin-section image contribute most to the detection result. Supported variants: `gradCAM` (default), `gradCAMpp`, `XGradCAM`.

```bash
python heatmap.py --weights runs/train/yolov8_c/weights/best.pt --source /path/to/image.jpg --method gradCAM
```

## Citation

If you use this code, please cite:

```bibtex
@article{ouyang2026yolov8c,
  title   = {Intelligent Recognition of Shale Laminae Based on an Improved YOLOv8n Model},
  author  = {Ouyang, Xiaoxuan and Huang, Zisang and Ma, Xinghua and Tang, Ruifeng and Li, Yue and Lin, Ze},
  journal = {Computers \& Geosciences},
  year    = {2026}
}
```

## License

This project is released under the AGPL-3.0 licence. See the LICENSE file for details.

## Acknowledgments

Built on Ultralytics YOLOv8:

> Glenn Jocher, Ayush Chaurasia, Jing Qiu (2023). **Ultralytics YOLO (Version 8.0.0)** [Computer software]. https://github.com/ultralytics/ultralytics

This study was financially supported by the National Major Science and Technology Projects of China (Nos. 2025ZD1400405 and 2025ZD1007802) and the Sichuan Science and Technology Program (No. 2025NSFJQ0004).

## Contact

Zisang Huang, Chengdu University of Technology, Chengdu 610059, China — hzs515@163.com
