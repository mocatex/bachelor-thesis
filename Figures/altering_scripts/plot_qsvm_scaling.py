"""Plot the Experiment 3 few-shot scaling sweep at the reported encoding bandwidth.

The thesis reports the scaling comparison at the bandwidth that is most
favourable to the quantum kernels, so that the negative result is stated at the
challenger's best setting rather than at an arbitrary one. This script draws
that comparison on a light background and also prints the full bandwidth sweep
that motivates the choice.

Input : data/qsvm_bw_c{0.1,0.25,0.5,0.75,1.0,1.5}.csv
        (copied from QML-AnalyzingGalaxies/experiment_results/
         experiment3_fewshot/results_bw/c*/results_*.csv)
Output: ../qsvm_scaling_sweep.png

Usage (from the repository root):
    python Figures/altering_scripts/plot_qsvm_scaling.py
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
OUT_PATH = SCRIPT_DIR.parent / "qsvm_scaling_sweep.png"

BANDWIDTHS = ["0.1", "0.25", "0.5", "0.75", "1.0", "1.5"]
REPORTED = "0.5"          # bandwidth shown in the figure and in the results table
FEW_SHOT = [2, 5, 10, 20]  # the regime this experiment is about

METHODS = {
    "classical_rbf": ("Classical SVM (RBF, tuned)", "#d95f02", "s"),
    "qsvm_fidelity": ("QSVM (fidelity kernel)", "#1b6ca8", "*"),
    "qsvm_projected": ("QSVM (projected / PQK)", "#2e8b3d", "D"),
}


def load(bandwidth: str) -> dict[tuple[int, str], list[float]]:
    out: dict[tuple[int, str], list[float]] = defaultdict(list)
    with (DATA_DIR / f"qsvm_bw_c{bandwidth}.csv").open(newline="") as handle:
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
    runs = {b: load(b) for b in BANDWIDTHS}
    reported = runs[REPORTED]
    ns = sorted({k[0] for k in reported})

    # The classical baseline never touches the quantum encoding, so its accuracy
    # must be identical across bandwidths. If it is not, the runs are not
    # comparable and the figure would be misleading.
    ref = [np.mean(runs[BANDWIDTHS[0]][(n, "classical_rbf")]) for n in ns]
    for b in BANDWIDTHS[1:]:
        got = [np.mean(runs[b][(n, "classical_rbf")]) for n in ns]
        if not np.allclose(ref, got, atol=1e-9):
            raise ValueError(f"classical baseline differs between c={BANDWIDTHS[0]} and c={b}")

    fig, ax = plt.subplots(figsize=(7.2, 4.6), dpi=200)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for method, (label, colour, marker) in METHODS.items():
        means, los, his = [], [], []
        for n in ns:
            mu, ci = mean_ci(reported[(n, method)])
            means.append(mu)
            los.append(mu - ci)
            his.append(mu + ci)
        ax.plot(ns, means, label=label, color=colour, marker=marker, markersize=7, linewidth=2.0)
        ax.fill_between(ns, los, his, color=colour, alpha=0.15, linewidth=0)

    ax.set_xscale("log")
    ax.set_xticks(ns)
    ax.set_xticklabels([str(n) for n in ns])
    ax.minorticks_off()
    ax.set_xlabel("Training samples per class $n$", fontsize=11)
    ax.set_ylabel("Test accuracy", fontsize=11)
    ax.set_title(
        f"Few-shot scaling at encoding bandwidth $c = {REPORTED}$\n"
        "(mean $\\pm$ 95% CI over 8 seeds)",
        fontsize=11,
    )
    ax.grid(True, linestyle=":", linewidth=0.8, color="#cccccc")
    ax.set_axisbelow(True)
    for spine in ax.spines.values():
        spine.set_edgecolor("#999999")
    ax.legend(fontsize=9, framealpha=0.95, loc="lower right")

    fig.tight_layout()
    fig.savefig(OUT_PATH, facecolor="white", bbox_inches="tight")
    plt.close(fig)
    print(f"wrote {OUT_PATH}\n")

    # Bandwidth sweep summary, used to justify the reported bandwidth in the text.
    print("bandwidth sweep (mean accuracy):")
    header = f"{'c':>6} {'fid few-shot':>13} {'fid n=200':>10} {'pqk few-shot':>13} {'pqk n=200':>10}"
    print(header)
    for b in BANDWIDTHS:
        r = runs[b]
        fid_fs = np.mean([v for n in FEW_SHOT for v in r[(n, "qsvm_fidelity")]])
        pqk_fs = np.mean([v for n in FEW_SHOT for v in r[(n, "qsvm_projected")]])
        fid_hi = np.mean(r[(200, "qsvm_fidelity")])
        pqk_hi = np.mean(r[(200, "qsvm_projected")])
        star = "  <-- reported" if b == REPORTED else ""
        print(f"{b:>6} {fid_fs:13.4f} {fid_hi:10.4f} {pqk_fs:13.4f} {pqk_hi:10.4f}{star}")
    cls_fs = np.mean([v for n in FEW_SHOT for v in reported[(n, "classical_rbf")]])
    print(f"{'classical':>6} {cls_fs:13.4f} {np.mean(reported[(200, 'classical_rbf')]):10.4f}")


if __name__ == "__main__":
    main()
