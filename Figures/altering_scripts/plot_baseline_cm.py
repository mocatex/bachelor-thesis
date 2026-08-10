"""Redraw the 62-class Baseline CNN confusion matrix as four readable quadrants.

The appendix originally carried the whole 62x62 matrix as a single image. At
that size the individual cells and their labels are unreadable in print, and the
figure surround (margins, tick labels, colourbar) was rendered on a dark theme.

This script redraws the matrix from the stored row-normalised numbers on a white
background and splits it into the four quadrants of a single cut at class index
`SPLIT`. Every one of the 62x62 cells is preserved: quadrants 1 and 4 hold the
two diagonal blocks, quadrants 2 and 3 hold the cross-block confusions. Each
panel is emitted as its own file so it can be placed at full page width.

Input : cm_norm_baseline_cnn.csv (row-normalised, rows = true class)
Output: ../cm_cnn_baseline_q1.png ... q4.png

Usage (from the repository root):
    python Figures/altering_scripts/plot_baseline_cm.py
"""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

SCRIPT_DIR = Path(__file__).resolve().parent
CSV_PATH = SCRIPT_DIR / "cm_norm_baseline_cnn.csv"
OUT_STEM = SCRIPT_DIR.parent / "cm_cnn_baseline"

# Single cut through the (alphabetically ordered) class list. 31 keeps the two
# halves equal in size, which keeps every panel at the same cell scale.
SPLIT = 31
ANNOT_MIN = 0.005  # annotate cells worth at least 0.5% of a row


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
        raise ValueError(f"rows are not normalised to 1: min {row_sums.min()}, max {row_sums.max()}")
    return matrix, labels


def pretty(label: str) -> str:
    return label.replace("_", " ")


def draw_block(matrix, labels, rows, cols, title, out_path) -> None:
    block = matrix[np.ix_(rows, cols)]
    row_labels = [labels[i] for i in rows]
    col_labels = [labels[j] for j in cols]

    fig, ax = plt.subplots(figsize=(14.0, 12.4), dpi=170)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    im = ax.imshow(block, cmap="Blues", vmin=0.0, vmax=1.0, interpolation="nearest")

    ax.set_xticks(np.arange(len(cols)))
    ax.set_yticks(np.arange(len(rows)))
    ax.set_xticklabels([pretty(l) for l in col_labels], rotation=90, fontsize=11)
    ax.set_yticklabels([pretty(l) for l in row_labels], fontsize=11)
    ax.set_xlabel("Predicted class", fontsize=14, labelpad=10)
    ax.set_ylabel("True class", fontsize=14, labelpad=10)
    ax.set_title(title, fontsize=15, pad=14)

    ax.set_xticks(np.arange(-0.5, len(cols), 1), minor=True)
    ax.set_yticks(np.arange(-0.5, len(rows), 1), minor=True)
    ax.grid(which="minor", color="white", linewidth=0.8)
    ax.tick_params(which="minor", length=0)
    for spine in ax.spines.values():
        spine.set_edgecolor("#999999")

    on_diagonal = rows is cols or list(rows) == list(cols)
    for a, i in enumerate(rows):
        for b, j in enumerate(cols):
            value = matrix[i, j]
            if value < ANNOT_MIN:
                continue
            ax.text(
                b,
                a,
                f"{value * 100:.0f}",
                ha="center",
                va="center",
                fontsize=10 if (on_diagonal and i == j) else 9,
                fontweight="bold" if (on_diagonal and i == j) else "normal",
                color="white" if value > 0.55 else "#1a1a1a",
            )

    cbar = fig.colorbar(im, ax=ax, fraction=0.030, pad=0.02)
    cbar.set_label("Fraction of true class (row-normalised)", fontsize=12)
    cbar.outline.set_edgecolor("#999999")

    fig.tight_layout()
    fig.savefig(out_path, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"  wrote {out_path.name}  ({len(rows)}x{len(cols)} cells, mass {block.sum():.2f})")


def main() -> None:
    matrix, labels = load_matrix(CSV_PATH)
    n = len(labels)
    first = list(range(SPLIT))
    second = list(range(SPLIT, n))

    a = f"{pretty(labels[0])}–{pretty(labels[SPLIT - 1])}"
    b = f"{pretty(labels[SPLIT])}–{pretty(labels[n - 1])}"
    print(f"{n} classes, split after index {SPLIT}")
    print(f"  block A ({len(first)}): {a}")
    print(f"  block B ({len(second)}): {b}\n")

    panels = [
        (first, first, f"Q1: true {a} $\\rightarrow$ predicted {a}", 1),
        (first, second, f"Q2: true {a} $\\rightarrow$ predicted {b}", 2),
        (second, first, f"Q3: true {b} $\\rightarrow$ predicted {a}", 3),
        (second, second, f"Q4: true {b} $\\rightarrow$ predicted {b}", 4),
    ]
    for rows, cols, title, idx in panels:
        draw_block(matrix, labels, rows, cols, title, Path(f"{OUT_STEM}_q{idx}.png"))

    # Summary statistics quoted in the appendix text.
    diag = np.diag(matrix)
    off = matrix.copy()
    np.fill_diagonal(off, 0.0)
    order = np.argsort(diag)
    flat = np.dstack(np.unravel_index(np.argsort(-off, axis=None), off.shape))[0]

    print(f"\nmacro-averaged recall (mean diagonal): {diag.mean():.3f}")
    print("worst recall:", ", ".join(f"{labels[i]} {diag[i]:.3f}" for i in order[:4]))
    print("best recall: ", ", ".join(f"{labels[i]} {diag[i]:.3f}" for i in order[-3:][::-1]))
    print("largest confusions:")
    for i, j in flat[:4]:
        print(f"  {labels[i]} -> {labels[j]}: {off[i, j]:.3f}")

    families = np.array([l.split("_")[0] for l in labels])
    print("mean cross-family leakage per true class:")
    for src in ("GALAXY", "QSO", "STAR"):
        for dst in ("GALAXY", "QSO", "STAR"):
            if src == dst:
                continue
            mass = matrix[np.ix_(families == src, families == dst)].sum() / (families == src).sum()
            print(f"  {src} -> {dst}: {mass:.4f}")


if __name__ == "__main__":
    main()
