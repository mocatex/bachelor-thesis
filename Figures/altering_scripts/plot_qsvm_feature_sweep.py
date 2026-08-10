"""Plot the Experiment 3 feature-dimensionality sweep on a light background.

The thesis claims that the QSVM classification metrics plateau at
N_features = 12, but the figure that carried that caption was in fact a
few-shot scaling curve at a fixed f = 12, so the claim had no supporting plot.
This script builds the real sweep from the five runs that were actually
executed (f = 4, 6, 8, 12, 16), each over the same four classes, the same seven
training-set sizes and the same eight seeds.

Left panel : accuracy averaged over all sample sizes, with a 95% CI over runs.
Right panel: accuracy at the largest budget (n = 200 per class), where the
             curves are furthest apart.

Input : data/qsvm_sweep_f{4,6,8,12,16}.csv
        (copied from QML-AnalyzingGalaxies/experiment_results/
         experiment3_fewshot/results_sweep/f*/results_*.csv)
Output: ../qsvm_feature_sweep.png

Usage (from the repository root):
    python Figures/altering_scripts/plot_qsvm_feature_sweep.py
"""

from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import t as student_t

SCRIPT_DIR = Path(__file__).resolve().parent
DATA_DIR = SCRIPT_DIR / "data"
OUT_PATH = SCRIPT_DIR.parent / "qsvm_feature_sweep.png"

FEATURES = [4, 6, 8, 12, 16]
SELECTED = 12
LARGEST_N = 200

METHODS = {
    "classical_rbf": ("Classical SVM (RBF, tuned)", "#d95f02", "s", "-"),
    "qsvm_fidelity": ("QSVM (fidelity kernel)", "#1b6ca8", "*", "-"),
    "qsvm_projected": ("QSVM (projected / PQK)", "#2e8b3d", "D", "-"),
}


def load(f: int) -> dict[tuple[int, str], list[float]]:
    path = DATA_DIR / f"qsvm_sweep_f{f}.csv"
    out: dict[tuple[int, str], list[float]] = defaultdict(list)
    with path.open(newline="") as handle:
        for row in csv.DictReader(handle):
            out[(int(row["n_per_class"]), row["method"])].append(float(row["accuracy"]))
    return out


def mean_ci(values) -> tuple[float, float]:
    """Mean and half-width of a 95% confidence interval.

    Uses the Student-t critical value for the given number of seeds, matching the
    intervals produced by the experiment runner and quoted in the results tables.
    A normal approximation would understate them by about 20% at eight seeds.
    """
    values = np.asarray(values, dtype=float)
    if values.size < 2:
        return float(values.mean()), 0.0
    crit = float(student_t.ppf(0.975, values.size - 1))
    return float(values.mean()), float(crit * values.std(ddof=1) / np.sqrt(values.size))


def main() -> None:
    runs = {f: load(f) for f in FEATURES}

    # Every run must cover the same grid, otherwise the sweep is not comparable.
    grids = {f: sorted({k[0] for k in runs[f]}) for f in FEATURES}
    reference = grids[FEATURES[0]]
    for f, grid in grids.items():
        if grid != reference:
            raise ValueError(f"f={f} covers sample sizes {grid}, expected {reference}")
    seed_counts = {len(v) for run in runs.values() for v in run.values()}
    if len(seed_counts) != 1:
        raise ValueError(f"inconsistent number of seeds per cell: {seed_counts}")
    n_seeds = seed_counts.pop()
    print(f"sample sizes {reference}, {n_seeds} seeds per cell, features {FEATURES}")

    fig, axes = plt.subplots(1, 2, figsize=(11.0, 4.4), dpi=200)
    fig.patch.set_facecolor("white")

    panels = [
        (axes[0], None, f"Averaged over all training-set sizes"),
        (axes[1], LARGEST_N, f"At $n = {LARGEST_N}$ samples per class"),
    ]

    for ax, only_n, title in panels:
        ax.set_facecolor("white")
        for method, (label, colour, marker, style) in METHODS.items():
            means, errs = [], []
            for f in FEATURES:
                if only_n is None:
                    # Average over the sample sizes *within* each seed first. Pooling
                    # all (n, seed) cells directly would make the error bars report
                    # the spread between the n = 2 and n = 200 regimes rather than
                    # the run-to-run uncertainty we want to show.
                    per_seed = np.array(
                        [
                            np.mean([runs[f][(n, method)][s] for n in reference])
                            for s in range(n_seeds)
                        ]
                    )
                    vals = per_seed
                else:
                    vals = np.array(runs[f][(only_n, method)])
                mu, ci = mean_ci(vals)
                means.append(mu)
                errs.append(ci)
            ax.errorbar(
                FEATURES,
                means,
                yerr=errs,
                label=label,
                color=colour,
                marker=marker,
                markersize=7,
                linestyle=style,
                linewidth=2.0,
                capsize=3,
                elinewidth=1.0,
            )

        # The selected width is marked by the dashed line only. An in-plot label
        # would either sit on the curves or under the legend, so the line is
        # explained in the figure caption instead.
        ax.axvline(
            SELECTED,
            color="#666666",
            linestyle="--",
            linewidth=1.2,
            zorder=0,
            label="_nolegend_",
        )

        ax.set_xticks(FEATURES)
        ax.set_xlabel("$N_{\\mathrm{features}}$ (= number of qubits)", fontsize=11)
        ax.set_ylabel(
            "Mean test accuracy" if only_n is None else "Test accuracy", fontsize=11
        )
        ax.set_title(title, fontsize=11)
        ax.grid(True, linestyle=":", linewidth=0.8, color="#cccccc")
        ax.set_axisbelow(True)
        for spine in ax.spines.values():
            spine.set_edgecolor("#999999")

    axes[0].legend(fontsize=9, framealpha=0.95, loc="lower right")
    fig.tight_layout()
    fig.savefig(OUT_PATH, facecolor="white", bbox_inches="tight")
    plt.close(fig)

    print(f"wrote {OUT_PATH}\n")
    for method, (label, *_rest) in METHODS.items():
        pooled = {
            f: np.mean([v for (n, m), lst in runs[f].items() if m == method for v in lst])
            for f in FEATURES
        }
        trail = "  ".join(f"f{f}={pooled[f]:.4f}" for f in FEATURES)
        print(f"{label:28s} {trail}   (12->16: {pooled[16] - pooled[12]:+.4f})")


if __name__ == "__main__":
    main()
