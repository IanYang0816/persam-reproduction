import argparse
import shutil
from pathlib import Path

import cv2
import numpy as np


def to_binary_255(mask):
    """
    Convert annotation mask to binary {0, 255}.
    PerSeg masks may use foreground value 38, so use mask > 0.
    """
    return ((mask > 0).astype(np.uint8) * 255)


def perturb(mask, mode):
    mask = to_binary_255(mask)

    if mode == "original":
        return mask

    if mode == "erode":
        # Stronger erosion: visibly shrinks the reference mask
        kernel = np.ones((41, 41), np.uint8)
        return cv2.erode(mask, kernel, iterations=1)

    if mode == "dilate":
        # Stronger dilation: visibly enlarges the reference mask
        kernel = np.ones((41, 41), np.uint8)
        return cv2.dilate(mask, kernel, iterations=1)

    if mode == "shift":
        # Stronger shift: visibly moves the reference mask
        h, w = mask.shape[:2]
        matrix = np.float32([[1, 0, 120], [0, 1, 120]])
        return cv2.warpAffine(mask, matrix, (w, h), borderValue=0)

    if mode == "noise":
        # Add visible salt-and-pepper noise
        rng = np.random.default_rng(0)
        noisy = mask.copy()
        flip = rng.random(mask.shape[:2]) < 0.03
        noisy[flip] = 255 - noisy[flip]
        return noisy

    raise ValueError(f"Unknown mode: {mode}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--src_data", required=True)
    parser.add_argument("--dst_data", required=True)
    parser.add_argument("--mode", required=True, choices=["original", "erode", "dilate", "shift", "noise"])
    parser.add_argument("--ref_idx", default="00")
    args = parser.parse_args()

    src_data = Path(args.src_data)
    dst_data = Path(args.dst_data)

    if dst_data.exists():
        shutil.rmtree(dst_data)

    shutil.copytree(src_data, dst_data)

    ann_root = dst_data / "Annotations"
    category_dirs = sorted([p for p in ann_root.iterdir() if p.is_dir()])

    changed = 0
    missing = []

    for category_dir in category_dirs:
        mask_path = category_dir / f"{args.ref_idx}.png"

        if not mask_path.exists():
            missing.append(category_dir.name)
            continue

        mask = cv2.imread(str(mask_path), cv2.IMREAD_GRAYSCALE)
        if mask is None:
            missing.append(category_dir.name)
            continue

        out = perturb(mask, args.mode)
        cv2.imwrite(str(mask_path), out)
        changed += 1

    print(f"Categories found: {len(category_dirs)}")
    print(f"Reference masks changed: {changed}")
    print(f"Missing/unreadable: {missing}")
    print(f"Saved perturbed dataset to: {dst_data}")
    print(f"Perturbation mode: {args.mode}")


if __name__ == "__main__":
    main()
