<p align="center">
  <img src="assets/logo.png" width="100%"/>
</p>

<h1 align="center">StrokeSegNet</h1>

<p align="center">
  <b>Automated Acute Ischemic Stroke Lesion Segmentation using Diffusion MRI</b><br>
  <i>DWI + ADC | nnU-Net v2 | ISLES-2022</i>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/GPU-CUDA%2012.1-green?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Python-3.10-blue?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Framework-nnU--Net%20v2-orange?style=for-the-badge"/>
  <img src="https://img.shields.io/badge/Model-2D%20U--Net-purple?style=for-the-badge"/>
</p>

---

## 🧠 Tagline

> **“Less noise, more signal — why fewer MRI modalities can outperform more.”**

---

## 📌 Table of Contents
- [Overview](#overview)
- [Clinical Motivation](#clinical-motivation)
- [Dataset](#dataset)
- [MRI Modalities Explained](#mri-modalities-explained)
- [Methodology](#methodology)
- [Architecture](#architecture)
- [Experiments](#experiments)
- [Results](#results)
- [Why Bimodal Beats Trimodal](#why-bimodal-beats-trimodal)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Citations](#citations)
- [Acknowledgements](#acknowledgements)

---

## 🧩 Overview

**StrokeSegNet** is a deep-learning system designed to automatically segment **acute ischemic stroke lesions** from brain MRI scans using **diffusion-based imaging**.

The project leverages:
- **DWI (Diffusion Weighted Imaging)**
- **ADC (Apparent Diffusion Coefficient)**

and evaluates whether adding **FLAIR** improves or degrades segmentation performance.

We use **nnU-Net v2**, a self-configuring medical image segmentation framework, trained and evaluated on the **ISLES-2022** multi-center dataset.

---

## 🏥 Clinical Motivation

- Stroke is a **time-critical medical emergency**
- Early lesion identification is essential for:
  - Thrombolysis
  - Mechanical thrombectomy
- Manual lesion segmentation:
  - Is slow
  - Is observer-dependent
  - Is impractical in emergency settings

👉 **Goal:** Fast, accurate, automated lesion segmentation.

---

## 📊 Dataset

**ISLES-2022 (MICCAI Challenge)**  
- 250 acute ischemic stroke cases  
- Multi-center, multi-scanner  
- Ground-truth expert annotations  

### Modalities Provided:
- DWI
- ADC
- FLAIR

---

## 🩻 MRI Modalities Explained

<p align="center">
  <img src="assets/dwi.png" width="250"/>
  <img src="assets/adc.png" width="250"/>
  <img src="assets/flair.png" width="250"/>
</p>

| Modality | What it Shows | Role |
|--------|---------------|------|
| DWI | Restricted water diffusion | Stroke core detection |
| ADC | Confirms true diffusion restriction | Reduces false positives |
| FLAIR | Edema / tissue changes (late) | Often misaligned in acute stroke |

---

## 🧪 Methodology

- Framework: **nnU-Net v2**
- Configuration: **2D U-Net**
- Validation: **5-fold cross-validation**
- Hardware: RTX 3050 (4GB VRAM)
- Training optimizations for low VRAM:
  - Reduced workers
  - Epoch-level checkpointing
  - CUDA-enabled PyTorch

---

## 🏗 Architecture

<p align="center">
  <img src="assets/architecture.png" width="700"/>
</p>

**5-Stage Encoder–Decoder with Skip Connections**
- Encoder: Feature extraction at increasing abstraction
- Bottleneck: Context aggregation
- Decoder: Precise spatial reconstruction
- Skip connections preserve fine-grained lesion details

---

## 🧪 Experiments

### Experiment A — **Bimodal (Proposed)**
- Input: **DWI + ADC**
- Fully aligned diffusion information

### Experiment B — **Trimodal (Baseline)**
- Input: **DWI + ADC + FLAIR**
- Introduces spatial misalignment noise

All other variables were kept identical.

---

## 📈 Results

<p align="center">
  <img src="assets/results.png" width="700"/>
</p>

| Metric | Bimodal (DWI+ADC) | Trimodal |
|------|------------------|---------|
| Mean Dice | **0.7564** | 0.7501 |
| Lesion-wise F1 | **0.8343** | 0.8305 |
| Recall | **0.7945** | 0.7777 |
| Median AVD (ml) | **1.39** | 1.63 |
| False Negatives | **Lower** | Higher |

---

## 🧠 Why Bimodal Beats Trimodal

- nnU-Net assumes **perfect voxel alignment**
- DWI + ADC are:
  - Acquired together
  - Diffusion-consistent
- FLAIR:
  - Often in native space
  - Captures delayed pathology
  - Introduces spatial noise

📌 **Key Insight:**  
> *More modalities ≠ better performance*

---

## ⚙ Installation

```bash
conda create -n nnunet-gpu python=3.10
conda activate nnunet-gpu
pip install numpy==1.26.4
pip install nnunetv2
pip install torch==2.5.1 --index-url https://download.pytorch.org/whl/cu121
