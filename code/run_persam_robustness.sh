#!/bin/bash

set -e

cd /content/drive/MyDrive/cs4782_persam_project/Personalize-SAM
mkdir -p /content/drive/MyDrive/cs4782_persam_project/final_results

for mode in erode dilate shift noise
do
    echo "=============================="
    echo "Running PerSAM with ${mode} reference mask"
    echo "=============================="

    rm -rf data
    cp -r data_ref_${mode} data

    rm -rf outputs/persam_${mode}_ref_vith

    python persam.py --outdir persam_${mode}_ref_vith

    python eval_miou.py \
      --pred_path persam_${mode}_ref_vith \
      --gt_path ./data_original_backup/Annotations \
      | tee /content/drive/MyDrive/cs4782_persam_project/final_results/persam_${mode}_ref_eval.txt
done

rm -rf data
cp -r data_original_backup data

echo "Finished all PerSAM robustness experiments."
