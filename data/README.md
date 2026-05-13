# Data Instructions

This project uses the PerSeg dataset released with the PerSAM paper and the SAM ViT-H checkpoint used by Segment Anything.

The dataset, model checkpoint, generated outputs, and perturbed datasets are **not included** in this repository because they are large.

## Required Files

1. **PerSeg dataset**
   - Used for personalized segmentation evaluation.
   - Download from the official PerSAM repository:
     - Google Drive: see the PerSeg link in the official PerSAM README.
     - Baidu Yun: see the official PerSAM README; extraction code is `222k`.
   - Official repository: https://github.com/ZrrSkywalker/Personalize-SAM

2. **SAM ViT-H checkpoint**
   - File name: `sam_vit_h_4b8939.pth`
   - Download command:

    wget -nc https://dl.fbaipublicfiles.com/segment_anything/sam_vit_h_4b8939.pth

## Expected Directory Structure

After downloading the data and checkpoint, organize the official PerSAM repository as follows:

    Personalize-SAM/
    ├── data/
    │   ├── Images/
    │   │   ├── can/
    │   │   ├── dog/
    │   │   └── ...
    │   └── Annotations/
    │       ├── can/
    │       ├── dog/
    │       └── ...
    └── sam_vit_h_4b8939.pth

Each object category should contain a reference image and reference mask indexed by `00`, for example:

    data/Images/can/00.jpg
    data/Annotations/can/00.png

## Notes on PerSeg Extraction

In our setup, the downloaded PerSeg zip file extracted into a folder named:

    data 3

We renamed it to:

    data

Example command:

    mv "data 3" data

After renaming, the folder should contain:

    data/Images/
    data/Annotations/

## Files Not Uploaded to GitHub

We intentionally do not upload the following files or folders:

    PerSeg.zip
    sam_vit_h_4b8939.pth
    Personalize-SAM/data/
    Personalize-SAM/data_original_backup/
    Personalize-SAM/data_ref_erode/
    Personalize-SAM/data_ref_dilate/
    Personalize-SAM/data_ref_shift/
    Personalize-SAM/data_ref_noise/
    Personalize-SAM/outputs/

These files are either large datasets, model checkpoints, or generated experiment outputs.

## Reproduction Reminder

To reproduce our results:

1. Clone the official PerSAM repository.
2. Download PerSeg from the official PerSAM README.
3. Download `sam_vit_h_4b8939.pth`.
4. Put the dataset and checkpoint in the expected structure above.
5. Follow the commands in the root `README.md`.
