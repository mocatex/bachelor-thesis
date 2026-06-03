# Sweep Results — Binary Task (30 epochs, 3 seeds each)

Task: `STAR_BROWN_DWARF_L` vs `STAR_M8`
Setup: shared CNN extractor (trainable), parameter-matched bottleneck/VQC head, dead-ReLU-fixed classical mirror.

## The numbers that matter

| Model | Config | Acc μ±σ | Macro F1 μ±σ | BROWN rec | M8 rec | **Gap** | ROC AUC |
|---|---|---|---|---|---|---|---|
| Quantum | 2q × 12L | 0.863 ±0.005 | 0.830 ±0.005 | 0.701 ±0.006 | 0.933 ±0.008 | **0.232** | 0.910 |
| Quantum | 3q × 8L  | 0.865 ±0.012 | 0.835 ±0.009 | 0.722 ±0.046 | 0.927 ±0.034 | 0.205 | 0.913 |
| Quantum | **4q × 6L** | **0.869 ±0.008** | **0.840 ±0.005** | 0.729 ±0.058 | 0.930 ±0.036 | 0.200 | 0.927 |
| Quantum | 6q × 4L  | 0.860 ±0.012 | 0.833 ±0.013 | 0.762 ±0.039 | 0.903 ±0.022 | 0.140 | 0.924 |
| Quantum | 8q × 3L  | 0.860 ±0.013 | 0.837 ±0.014 | **0.802 ±0.005** | 0.885 ±0.017 | **0.083** | **0.927** |
| Classical | 4 features | **0.868 ±0.016** | **0.843 ±0.016** | 0.774 ±0.080 | 0.909 ±0.047 | 0.136 | **0.933** |
| Classical | 8 features | 0.862 ±0.004 | 0.836 ±0.006 | 0.774 ±0.026 | 0.900 ±0.008 | 0.127 | 0.922 |

*Gap = M8 recall − BROWN recall. Smaller = more balanced.*
*All configs have ~24.5K total params (the CNN extractor dominates; the VQC/MLP head is the small piece).*

## Best of the best

Different metrics crown different winners — and the spread between them is small (mostly within 1σ):

- **Highest accuracy & macro F1:** Quantum 4q×6L vs Classical 4-features — statistical **tie** (0.869 vs 0.868 acc, 0.840 vs 0.843 macro F1).
- **Highest ROC AUC:** Classical 4-features (0.933) — small but consistent edge.
- **Best class balance:** **Quantum 8q×3L wins clearly** — only 8.3pp gap between BROWN and M8 recall, ~half of any other configuration. It also has the smallest std on BROWN recall (0.005), so it's reliably balanced across seeds.
- **Most consistent (lowest seed variance):** Classical 8-features — std on every metric is 1pp or less.

## What this actually says

1. **Quantum and classical are tied on top-line metrics.** Within seed noise, no configuration meaningfully outperforms another. The original "91% vs 46%" gap is dead.

2. **The "narrow and deep" intuition holds for accuracy** — 4q×6L > 8q×3L on overall acc — **but not for balance.** As you go from narrow+deep to wide+shallow, BROWN recall steadily climbs (0.70 → 0.80) while M8 recall drops (0.93 → 0.88). Wide+shallow models naturally balance the two classes.

3. **For a thesis claim:** the most defensible quantum-specific finding here is *"VQC at 8q×3L produces the most balanced classifier, even though wider quantum architectures are usually expected to suffer barren-plateau effects."* That's a small but real and surprising result.

4. **Classical features4 is the strongest overall baseline.** It quietly takes ROC AUC and ties macro F1. Any quantum-advantage claim must explain why it doesn't beat this.

## Would 150 epochs change anything?

**Probably not enough to matter.** Two reasons:

- The original 150-epoch ClassicalMirror log shows training plateaus around epoch 20–30 and then oscillates between ~40% and ~85% val acc for the next 120 epochs without further improvement. More epochs ≠ more learning — they just expose instability.
- The 150-epoch binary quantum reached 0.894 best val acc (per the resume log) vs ~0.87 here. That's a ~2–3pp ceiling, not a regime change.

For the **quantum side specifically**, you'd likely gain ~2pp accuracy and a small ROC AUC bump — won't change rankings or the balance story.
For the **classical side**, basically no change.

**Better use of 5× the compute:** add more seeds (5–10) at 30 epochs. That sharpens the error bars enough to defend significant differences between configs. Right now most of the apparent rankings are within 1σ.

## Suggested thesis framing

> *"Across a parameter-matched architecture sweep (5 quantum shapes, 2 classical bottleneck widths, 3 seeds each), the VQC and the classical mirror achieve statistically indistinguishable top-line performance (best macro F1: 0.840 quantum vs 0.843 classical). However, an architectural pattern emerges within the VQC family: wide-shallow circuits (8 qubits × 3 layers) produce significantly better-balanced per-class recall (gap 8.3pp) than narrow-deep circuits (2 qubits × 12 layers, gap 23.2pp), at a small cost to overall accuracy. This challenges the standard 'narrow and deep' heuristic when minority-class recall is the priority."*

Defensible, novel, and supported by the data. It doesn't claim quantum advantage — it claims a quantum **architectural insight**, which is a more honest thesis.
