# Reproducing and Stress-Testing PerSAM

This repository contains our CS 4782 final project re-implementation of **Personalize Segment Anything Model with One Shot**. We reproduce PerSAM and PerSAM-F on the PerSeg dataset and add a robustness experiment that tests how PerSAM responds to imperfect reference masks.

## Paper

**Personalize Segment Anything Model with One Shot**  
Renrui Zhang, Zhengkai Jiang, Ziyu Guo, Shilin Yan, Junting Pan, Xianzheng Ma, Hao Dong, Peng Gao, Hongsheng Li.

Paper: https://arxiv.org/abs/2305.03048  
Official code: https://github.com/ZrrSkywalker/Personalize-SAM

## Chosen Result

We reproduce the paper's personalized segmentation result on the PerSeg dataset. The main evaluation metric is mean Intersection-over-Union (mIoU).

We compare:

| Method | mIoU | mAcc |
|---|---:|---:|
| PerSAM | 89.32 | 92.19 |
| PerSAM-F | 95.18 | 95.57 |

PerSAM-F improves PerSAM by **+5.86 mIoU** in our reproduction.

## GitHub Contents

```text
code/      Colab notebook and scripts for our re-implementation and robustness experiment
data/      instructions for obtaining PerSeg and the SAM checkpoint
results/   result tables and generated figures
poster/    final poster PDF
report/    final 2-page report PDF
