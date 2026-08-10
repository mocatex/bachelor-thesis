"""Invert the colours of the dark-background result plots.

The reviewers flagged the dark training-history and robustness plots as unreadable
in print. This script flips them to a light background by inverting the RGB
channels, which is the same treatment already applied to the Experiment 1 and 2
training histories (`*_inverted.png`).

The original of every figure is copied into `originals/` the first time it is
touched, and every later run re-inverts *from that backup*. Running this script
twice therefore produces the same result instead of flipping the figures back to
dark, and deleting a file from `originals/` is enough to restore it.

Usage (from the repository root):
    python Figures/altering_scripts/invert_figures.py
    python Figures/altering_scripts/invert_figures.py --restore
"""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import numpy as np
from PIL import Image

SCRIPT_DIR = Path(__file__).resolve().parent
FIGURES_DIR = SCRIPT_DIR.parent
ORIGINALS_DIR = SCRIPT_DIR / "originals"

# Dark-background plots that belong to the baseline, Experiment 3, 4 and 5 sections.
# The GaSNet-II confusion matrix is deliberately absent: inverting a heatmap
# destroys its colour map, so it is regenerated from the raw numbers instead
# (see plot_gasnet_cm.py).
TARGETS = [
    # Classical baseline and GaSNet-II replica
    "classical_training_history.png",
    "gasnet_training_history.png",
    # Experiment 3 (QSVM) has no entry here: both of its figures are redrawn
    # from the raw run outputs on a light background by plot_qsvm_feature_sweep.py
    # and plot_qsvm_scaling.py. Inverting them would turn them dark again.
    # Experiment 4 (quanvolution)
    "quanv_ood_heavy_robustness.png",
    "quanv_ood_light_robustness.png",
    "quanv_adv_heavy_robustness.png",
    "quanv_adv_light_robustness.png",
    "quanv_ood_heavy_jacobian.png",
    "quanv_ood_light_jacobian.png",
    "quanv_adv_heavy_jacobian.png",
    "quanv_adv_light_jacobian.png",
    # Experiment 5 (QCNN)
    "qcnn_robustness_HighData_Clean.png",
    "qcnn_robustness_HighData_Adv.png",
    "qcnn_robustness_FewShot_Clean.png",
    "qcnn_robustness_FewShot_Adv.png",
    "jacobian_slope_QCNN_vs_CNN_Huge.png",
    "jacobian_slope_QCNN_vs_CNN_Tiny.png",
]


def mean_luminance(img: Image.Image) -> float:
    arr = np.asarray(img.convert("RGB"), dtype=float)
    return float((0.299 * arr[..., 0] + 0.587 * arr[..., 1] + 0.114 * arr[..., 2]).mean())


def invert(img: Image.Image) -> Image.Image:
    """Invert RGB, leave alpha untouched so transparent margins stay transparent."""
    has_alpha = img.mode in ("RGBA", "LA") or "transparency" in img.info
    img = img.convert("RGBA" if has_alpha else "RGB")
    arr = np.asarray(img).copy()
    arr[..., :3] = 255 - arr[..., :3]
    return Image.fromarray(arr, mode=img.mode)


def restore() -> None:
    if not ORIGINALS_DIR.is_dir():
        print("nothing to restore: no originals/ directory")
        return
    for backup in sorted(ORIGINALS_DIR.glob("*.png")):
        shutil.copy2(backup, FIGURES_DIR / backup.name)
        print(f"restored {backup.name}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--restore",
        action="store_true",
        help="copy the backed-up originals back over the inverted figures",
    )
    args = parser.parse_args()

    if args.restore:
        restore()
        return

    ORIGINALS_DIR.mkdir(exist_ok=True)

    for name in TARGETS:
        target = FIGURES_DIR / name
        if not target.is_file():
            print(f"[skip]    {name}: not found")
            continue

        backup = ORIGINALS_DIR / name
        if not backup.is_file():
            shutil.copy2(target, backup)

        # Always invert the pristine original, never the current file, so that
        # repeated runs are idempotent.
        with Image.open(backup) as src:
            before = mean_luminance(src)
            out = invert(src)

        after = mean_luminance(out)
        out.save(target)
        print(f"[inverted] {name}: mean luminance {before:5.1f} -> {after:5.1f}")

    print(f"\nOriginals kept in {ORIGINALS_DIR.relative_to(FIGURES_DIR.parent)}")
    print("Re-run to refresh, or pass --restore to undo.")


if __name__ == "__main__":
    main()
