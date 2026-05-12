# Reproducing and Stress-Testing PerSAM

## 1. Introduction

This repository contains our CS 4782 final project re-implementation of **Personalize Segment Anything Model with One Shot** by Zhang et al. The paper proposes PerSAM, a one-shot method that personalizes the Segment Anything Model (SAM) using one reference image and one reference mask.

PerSAM converts SAM from a manually prompted segmentation model into a personalized segmenter that can identify the same target object across new images. We reproduce the main PerSeg result and add a robustness experiment on imperfect reference masks.

## 2. Chosen Result

We reproduce the paper's personalized segmentation result on the **PerSeg** dataset, comparing **PerSAM** and **PerSAM-F** using mean Intersection-over-Union (mIoU) and mean accuracy (mAcc).

This result was chosen because it directly tests the paper's main contribution: whether SAM can be personalized from a single reference image-mask pair. In the original paper, this corresponds to the main PerSeg evaluation comparing training-free PerSAM with the fine-tuned PerSAM-F variant.

## 3. GitHub Contents

Repository structure:

    code/      Colab notebook and scripts for reproduction and robustness testing
    data/      instructions for obtaining PerSeg and the SAM checkpoint
    results/   result tables, plots, and generated figures
    poster/    final poster PDF
    report/    final 2-page report PDF

The dataset, SAM checkpoint, perturbed data folders, and full generated outputs are not included because they are large.

## 4. Re-implementation Details

We use the official PerSAM codebase with the **SAM ViT-H** checkpoint and evaluate on the **PerSeg** dataset. Experiments were run in Google Colab using an L4 GPU.

We reproduce two methods:

- **PerSAM**: training-free one-shot personalized segmentation.
- **PerSAM-F**: a lightweight fine-tuning variant that freezes SAM and tunes mask-scale weights.

We also implement an additional robustness experiment by perturbing only the reference mask while keeping evaluation ground-truth masks unchanged. The perturbations are erosion, dilation, spatial shift, and random noise.

A key implementation issue was that some PerSeg masks use foreground value `38` rather than `255`; therefore, our mask perturbation script binarizes masks using `mask > 0`.

## 5. Reproduction Steps

### Step 1: Clone official PerSAM

    git clone https://github.com/ZrrSkywalker/Personalize-SAM.git
    cd Personalize-SAM

### Step 2: Install dependencies

    pip install matplotlib tqdm numpy opencv-python
    pip install git+https://github.com/facebookresearch/segment-anything.git

### Step 3: Download data and checkpoint

Download the PerSeg dataset and the SAM ViT-H checkpoint `sam_vit_h_4b8939.pth`.

Expected directory structure:

    Personalize-SAM/
    ├── data/
    │   ├── Images/
    │   └── Annotations/
    └── sam_vit_h_4b8939.pth

### Step 4: Run PerSAM

    python persam.py --outdir persam_repro_vith
    python eval_miou.py --pred_path persam_repro_vith

### Step 5: Run PerSAM-F

    python persam_f.py --outdir persam_f_repro_vith
    python eval_miou.py --pred_path persam_f_repro_vith

### Step 6: Run robustness experiment

First generate perturbed reference-mask datasets:

    python code/perturb_reference_masks.py \
      --src_data data_original_backup \
      --dst_data data_ref_erode \
      --mode erode

    python code/perturb_reference_masks.py \
      --src_data data_original_backup \
      --dst_data data_ref_dilate \
      --mode dilate

    python code/perturb_reference_masks.py \
      --src_data data_original_backup \
      --dst_data data_ref_shift \
      --mode shift

    python code/perturb_reference_masks.py \
      --src_data data_original_backup \
      --dst_data data_ref_noise \
      --mode noise

Then run:

    bash code/run_persam_robustness.sh

Expected compute: one Google Colab L4 GPU or similar CUDA GPU.

## 6. Results/Insights

### Main reproduction result

| Method | mIoU | mAcc |
|---|---:|---:|
| PerSAM | 89.32 | 92.19 |
| PerSAM-F | 95.18 | 95.57 |

PerSAM-F improves PerSAM by **+5.86 mIoU** in our reproduction. The largest improvements occur on several PerSAM failure cases, including `can`, `rc_car`, `teapot`, and `robot_toy`.

### Robustness experiment

| Reference Mask Condition | mIoU | mAcc |
|---|---:|---:|
| Original | 89.32 | 92.19 |
| Erode | 88.45 | 92.18 |
| Dilate | 87.33 | 90.23 |
| Shift | 73.84 | 82.28 |
| Noise | 89.32 | 92.19 |

The main insight is that PerSAM is relatively robust to boundary imperfections such as erosion, dilation, and sparse noise, but is sensitive to spatially shifted reference masks. This suggests that correct reference-mask alignment matters more than perfect boundary quality.

Relevant output files:

- `results/main_miou_bar_chart.png`
- `results/per_category_improvement.png`
- `results/reference_mask_perturbations_stronger.png`
- `results/persam_reference_mask_robustness.png`

## 7. Conclusion

Our reproduction supports the main claim of PerSAM: SAM can be personalized from a single reference image and mask. PerSAM-F improves average segmentation quality by correcting several difficult cases where PerSAM selects an incorrect mask scale.

Our additional robustness experiment shows that one-shot personalization depends strongly on the quality of the reference representation. Boundary noise is usually tolerable, but spatial misalignment can contaminate the target embedding and sharply reduce performance.

## 8. References

- Renrui Zhang, Zhengkai Jiang, Ziyu Guo, Shilin Yan, Junting Pan, Xianzheng Ma, Hao Dong, Peng Gao, and Hongsheng Li. **Personalize Segment Anything Model with One Shot**. arXiv:2305.03048, 2023.
- Alexander Kirillov et al. **Segment Anything**. ICCV, 2023.
- PerSAM official repository: https://github.com/ZrrSkywalker/Personalize-SAM
- Segment Anything official repository: https://github.com/facebookresearch/segment-anything

## 9. Acknowledgements

This project was completed as part of **CS 4782**.

We thank the authors of PerSAM and Segment Anything for releasing their paper, dataset, code, and model resources.

Group members: **Ian Yang** and **Yawen Lin**.
