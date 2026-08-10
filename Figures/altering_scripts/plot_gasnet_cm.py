"""Redraw the 13-class GaSNet-II replica confusion matrix on a light background.

The original figure was rendered on a dark theme and was flagged as unreadable in
print. Inverting the pixels is not an option here, because that would also invert
the colour map and break the "darker cell = larger value" reading. The matrix is
therefore redrawn from the stored row-normalised numbers.

Input : cm_norm_GasNet_II_Replica.csv (row-normalised, rows = true class)
Output: ../gasnet_confusion_matrix.png (overwrites the dark version)

Usage (from the repository root):
    python Figures/altering_scripts/plot_gasnet_cm.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "cm_norm_GasNet_II_Replica.csv"
OUT_PATH = SCRIPT_DIR.parent / "gasnet_confusion_matrix.png"


def load_matrix(path: Path) -> tuple[np.ndarray, list[str]]:
    with path.open(newline="") as handle:
        rows = list(csv.reader(handle))
    header = rows[0][1:]
    body = [r for r in rows[1:] if r and r[0].strip()]
    labels = [r[0] for r in body]
    matrix = np.array([[float(v) for v in r[1:]] for r in body], dtype=float)

    if labels != header:
        raise ValueError("row and column labels disagree; refusing to plot a transposed matrix")
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError(f"confusion matrix is not square: {matrix.shape}")

    row_sums = matrix.sum(axis=1)
    if not np.allclose(row_sums, 1.0, atol=1e-6):
        raise ValueError(f"rows are not normalised to 1: {row_sums}")

    return matrix, labels


def pretty(label: str) -> str:
    """SDSS class names carry underscores; make them readable and TeX-safe."""
    return label.replace("_", " ")


def main() -> None:
    matrix, labels = load_matrix(CSV_PATH)
    n = len(labels)

    fig, ax = plt.subplots(figsize=(9.0, 7.6), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    im = ax.imshow(matrix, cmap="Blues", vmin=0.0, vmax=1.0, interpolation="nearest")

    ax.set_xticks(np.arange(n))
    ax.set_yticks(np.arange(n))
    ax.set_xticklabels([pretty(l) for l in labels], rotation=45, ha="right", fontsize=9)
    ax.set_yticklabels([pretty(l) for l in labels], fontsize=9)
    ax.set_xlabel("Predicted class", fontsize=11, labelpad=8)
    ax.set_ylabel("True class", fontsize=11, labelpad=8)

    # Thin white grid between the cells, drawn on the minor ticks.
    ax.set_xticks(np.arange(-0.5, n, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, n, 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=1.0)
    ax.tick_params(which="minor", length=0)
    for spine in ax.spines.values():
        spine.set_edgecolor("#999999")

    # Annotate every cell that is not essentially zero. Text flips to white on the
    # dark diagonal cells so it stays legible.
    for i in range(n):
        for j in range(n):
            value = matrix[i, j]
            if value < 0.005:
                continue
            ax.text(
                j,
                i,
                f"{value * 100:.1f}",
                ha="center",
                va="center",
                fontsize=8.5 if i == j else 8,
                fontweight="bold" if i == j else "normal",
                color="white" if value > 0.55 else "#1a1a1a",
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("Fraction of true class (row-normalised)", fontsize=10)
    cbar.outline.set_edgecolor("#999999")

    ax.set_title(
        "GaSNet-II replica: 13-class normalised confusion matrix",
        fontsize=12,
        pad=12,
    )

    fig.tight_layout()
    fig.savefig(OUT_PATH, facecolor="white", bbox_inches="tight")
    plt.close(fig)

    diagonal = np.diag(matrix)
    print(f"wrote {OUT_PATH}")
    print(f"  {n} classes, recall min={diagonal.min():.3f} max={diagonal.max():.3f} mean={diagonal.mean():.3f}")
    off = matrix.copy()
    np.fill_diagonal(off, 0.0)
    i, j = np.unravel_index(off.argmax(), off.shape)
    print(f"  largest off-diagonal: {labels[i]} -> {labels[j]} = {off[i, j]:.3f}")


if __name__ == "__main__":
    main()
