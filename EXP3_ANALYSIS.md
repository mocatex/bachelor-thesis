# Experiment 3 — Complex Correlation Showdown: VQC vs. Classical Heads on Frozen Features

**Status:** Complete (2026-05-31)
**One-line result:** At matched parameter count, the variational quantum classifier (VQC) and a classical head reach the *same* accuracy (~96%). This is **quantum–classical parity, not a quantum advantage.** The apparent quantum win observed earlier was a **dead-ReLU training artifact**, proven by a Tanh control.

---

## 1. Purpose of the experiment

The goal was to test whether a quantum head is **more parameter-efficient** than a classical head at the same task: i.e. can a VQC reach high accuracy with fewer trainable parameters than a classical neural network?

A secondary goal — prompted by supervisor feedback — was to **not rely on parameter count alone** (since one cannot fairly equate a quantum rotation angle with a classical weight), and instead also examine **convergence speed, training/loss stability, per-class behavior, and computational cost.**

## 2. Common setup (all models share this)

- **Task:** 4-class spectral classification.
  - Classes: `STAR_BROWN_DWARF_L`, `STAR_M8`, `GALAXY_STARBURST`, `GALAXY_STARFORMING`.
  - Balanced subsampling: 1000 samples/class, split 70/15/15 train/val/test.
- **Frozen feature extractor ("the Beast"):** a pretrained `SpectraClassifier` (CNN+Transformer) whose final classification layer is replaced with `Identity` and whose every parameter is frozen (kept in eval mode so BatchNorm stats don't drift). Output: a **128-dim feature vector** per spectrum.
- **What differs between models:** *only the small trainable head* that maps the 128-d frozen features → 4 class logits.
- **Training:** 100 epochs (final clean runs), Adam, lr 1e-3, weight decay 1e-4, batch size 256. Seed 42.

This design isolates the head: any performance difference comes from the head architecture, not from feature learning.

## 3. The models compared

| # | Model | Head architecture | Trainable params |
|---|-------|-------------------|------------------|
| A | **Dense classical** (`FrozenBeastDenseClassifier`) | `Linear(128,38)→ReLU→Dropout→Linear(38,4)` | **5058** |
| B | **Quantum** (`FrozenBeastVQCClassifier`) | `Linear(128,4)→tanh·π→ data-reuploading VQC (4 qubits, 5 layers)→Linear(4,4)` | **556** |
| C | **Classical mirror, ReLU** (`FrozenBeastTinyClassicalClassifier`) | `Linear(128,4)→Tanh→Linear(4,4)→ReLU→Linear(4,4)` | **556** |
| D | **Classical mirror, Tanh** (`FrozenBeastTinyClassicalTanhClassifier`) | `Linear(128,4)→Tanh→Linear(4,4)→Tanh→Linear(4,4)` | **556** |

**Why the mirror exists.** Model C/D is a *structural control* for the quantum model B. It has the same pipeline shape — a `Linear(128→4)` bottleneck, a middle transform, and a readout — but the quantum circuit is replaced by a classical `Linear(4,4)`. The parameter counts are matched to 556 **by construction**, which sidesteps the "you can't compare angles to weights" objection: instead of equating units, we hold the architecture fixed and swap only the head's internals.

Parameter breakdown of the quantum head (556):
- `Linear(128→4)` bottleneck: 128·4 + 4 = **516**
- VQC weights (1 RY angle per qubit per layer, 4×5): **20**
- `Linear(4→4)` readout: 4·4 + 4 = **20**

The classical mirror matches this exactly: 516 + 20 + 20 = 556.

### Quantum circuit detail (model B)
Per layer (5 layers on 4 qubits):
1. **Data re-upload:** `RY(x_q)` on each qubit (encodes the 4 bottleneck values).
2. **Trainable rotation:** `RY(θ_{layer,q})` on each qubit (the 20 quantum parameters).
3. **Entanglement:** CNOT ring `q → (q+1) mod 4`.

Readout: `⟨Z⟩` expectation per qubit → 4 values → trainable `Linear(4,4)` → logits.
The classical readout decouples "qubit i = class i" and lets logits escape the `[-1,1]` expectation range so softmax confidence isn't capped.

## 4. Results

### 4.1 Headline numbers (test set, 100 epochs)

| Model | Params | Overall acc | Brown-dwarf-L recall | Other 3 classes | Converges by | Val-loss floor |
|-------|--------|-------------|----------------------|-----------------|--------------|----------------|
| A — Dense classical | 5058 | ~96% | 0.95 | 0.96–0.97 | ~ep 7 | ~0.04 |
| B — Quantum (Linear→VQC) | 556 | ~96% | 0.93 | 0.96–0.97 | ~ep 25 | ~0.07 |
| C — Classical mirror, **ReLU** | 556 | **~79%** | **0.18** ❌ | 0.92–0.97 | stalled to ~ep 25 | (high) |
| D — Classical mirror, **Tanh** | 556 | **~96%** | **0.94** ✅ | 0.95–0.97 | ~ep 20 | ~0.08 |

(Accuracies read from confusion-matrix / per-class plots; treat as ±1pp.)

### 4.2 The key comparison: B vs. C vs. D at 556 params

- **B (quantum)** classifies the hardest class, `STAR_BROWN_DWARF_L`, well: **0.93 recall**, ~96% overall.
- **C (ReLU mirror)** *fails* on that class: **0.18 recall** — it dumps ~75% of brown dwarfs into `GALAXY_STARFORMING` — capping at ~79% overall.
- **D (Tanh mirror)** — identical to C except the inner `ReLU` is swapped for `Tanh` — **fully recovers**: 0.94 brown-dwarf recall, ~96% overall.

**Interpretation.** B beating C looked like a quantum advantage. But D shows the C failure was **not a capacity limit** — it was a **dead-ReLU artifact**. With only 4 neurons in the middle layer, a ReLU unit that gets pushed negative outputs zero and receives zero gradient, so it never recovers ("dies"). Losing even one or two of four units destroys the decision boundary for the minority/hardest class. The tell is visible in C's training curve: accuracy sits flat at ~0.50 from epoch ~5 to ~13 (a stuck plateau) before partially escaping. Tanh cannot die this way (it always has nonzero gradient), so D trains cleanly.

Once the confound is removed, **B (quantum) and D (classical) are equal on every measured axis.**

## 5. What can and cannot be claimed

### ✅ Legitimate, defensible claims
1. **Quantum–classical parity at matched parameters.** A 556-param VQC and a 556-param classical head reach the same accuracy and the same per-class behavior. *(Consistent with the Experiment 1 binary finding, which was also parity.)*
2. **Tiny heads suffice on good frozen features.** Both 556-param heads (B and D) match the 9× larger 5058-param dense head (A) at ~96%. This is a real ~9× parameter-efficiency result — **but it is a property of the frozen feature extractor, not of quantum computing.** The features are already linearly separable enough that a tiny head is plenty.
3. **Activation choice dominated at this width.** The single largest accuracy swing in the whole experiment — ReLU 79% vs Tanh 96% at *identical* parameters — came from an activation function, not from quantum mechanics. This directly supports the supervisor's point that parameter count alone is the wrong lens.
4. **No quantum advantage on the "other axes" either:** the classical head converges *faster* (~ep 7–20 vs ~ep 25), reaches a *lower/equal* validation-loss floor, and is *orders of magnitude cheaper* to train (a plain matrix multiply vs a state-vector simulation of the circuit).

### ❌ Claims to avoid
- "Quantum is more parameter-efficient than classical." — Refuted by D.
- "The VQC solved a class the classical model couldn't." — That was the dead ReLU; D solves it too.
- Attributing the ~9× saving vs the dense head to quantum — it's the frozen extractor; the Tanh-classical mirror gets the same saving.
- Over-reading the pure-PCA quantum number (see §6) as evidence about qubit count.

## 6. Supporting ablation — why the encoding, not the qubit count, is the bottleneck

A separate quantum variant feeds the circuit via a **frozen PCA(128→4)** projection instead of a trainable `Linear(128→4)`:

| Quantum input encoding | Params | Overall acc |
|------------------------|--------|-------------|
| Frozen PCA(128→4) → VQC (pure quantum) | ~40 | ~76% (capped) |
| Frozen PCA(128→64) → trainable Linear(64→4) → VQC (hybrid) | ~300 | ~76% (capped) |
| Trainable Linear(128→4) → VQC (model B) | 556 | **~96%** |

Widening the PCA (32 / 64 / 128) did **not** help — all PCA variants plateau near 76%. Yet the trainable-Linear model B, encoding into the *same 4 qubits*, reaches 96%.

**Conclusion:** the bottleneck was never the 4-qubit count or the "4-number door" into the circuit — it was **which 4 numbers go through it.** PCA picks maximum-*variance* directions (unsupervised); variance ≠ class separability, so it wastes the 4 encoding slots. A learned `Linear` picks maximum-*discriminative* directions (supervised, end-to-end through the loss). The quantum encoding is only as good as the classical projection feeding it; an unsupervised compression starves the VQC, a learned one does not.

(This is a quantum-relevant insight worth including, but note it's about *encoding/data-loading*, a known central issue in QML, not about a quantum speedup.)

## 7. Training dynamics (the supervisor's "look at other things" axis)

- **Convergence speed:** classical (A ~ep7, D ~ep20) ≥ quantum (B ~ep25). Quantum is no faster, somewhat slower.
- **Loss stability:** all models show spiky *train* loss late (stochastic gradients on small batches) but smooth, monotonic *validation* loss — i.e. the noise is in the optimizer, not in generalization. The Tanh-classical val loss is the lowest/smoothest (~0.04–0.08).
- **Generalization gap:** essentially zero for B and D (val tracks train tightly, no overfitting) despite 556 trainable params — expected, since the backbone is frozen.
- **Compute cost:** the VQC forward/backward pass is a `default.qubit` state-vector simulation (seconds/epoch on CPU) vs. milliseconds for the classical heads — the same accuracy at far higher training cost. On real NISQ hardware one would additionally face shot noise and decoherence.

## 8. Methodological takeaway (a strength to highlight)

The headline lesson is a **scientific-integrity win**: an apparent quantum advantage survived only until a proper control was run. Building the param-matched mirror with a non-dying activation (Tanh) is exactly what exposed the dead-ReLU confound. The recommendation that follows — and that should be stated in the thesis — is:

> **Never report a VQC result without a parameter-matched classical control using a robust activation.** A naive width-limited ReLU baseline can fail for reasons unrelated to capacity and create a false advantage.

## 9. Suggested thesis framing (paste-ready)

> *On a 4-class spectral classification task using a frozen pretrained feature extractor, a variational quantum classifier with a learned classical encoding (556 trainable parameters) achieved ~96% test accuracy, matching a parameter-matched classical head and a 9×-larger dense classical network. We find no quantum advantage in accuracy, parameter efficiency, convergence speed, or training stability, and the quantum model incurs substantially higher computational cost. An initial apparent advantage over the classical baseline was traced to a dead-ReLU artifact in a width-4 layer: replacing ReLU with Tanh in the classical control restored parity. The dominant performance factor at this scale was therefore the choice of activation function, not the quantum versus classical nature of the head. A supporting ablation showed that an unsupervised PCA encoding into the quantum circuit caps performance (~76%) regardless of its width, whereas a learned linear encoding reaches ~96% — indicating that the limiting factor is the data-encoding strategy feeding the qubits, not the qubit count. We conclude that, for this task and hardware-simulated setting, the VQC is competitive with but not superior to classical methods, and we emphasize the necessity of carefully constructed, parameter-matched classical controls when evaluating quantum machine-learning claims.*

## 10. Result artifacts (file locations)

- Quantum (B), 100 ep: `results_exp3_quantum_4class_100epochs/` (`cm_test.png`, `per_class_accuracy.png`, `training_history.png`)
- Classical ReLU mirror (C): `results_exp3_tiny_classical_4class/`
- Classical Tanh mirror (D), 100 ep: `results_exp3b_tiny_classical_tanh_4class_100epochs/`
- Dense classical (A): `results_exp3_classical_4class/`
- PCA-hybrid quantum: `results_exp3_quantum_hybrid_4class_PCA64_4qubits_5layers/`
- Pure-PCA quantum: `results_exp3_quantum_4class/`
- Model definitions: `src/models/exp3_models.py`
- Training scripts: `experiments/train_exp3_quantum.py`, `train_exp3_classical.py`, `train_exp3b_classical_tiny.py`, `train_exp3b_classical_tiny_tanh.py`

> ⚠️ **Reproducibility note:** the older result directories contain only PNG plots (no `history.json`), so the numbers above are read from the figures. The Tanh-mirror run now dumps `history.json`. For fully citable thesis numbers, consider re-running A/B/C at 100 epochs with the same `history.json` export so all four models sit on identical footing. The exact accuracies should be transcribed from the confusion matrices when quoting in the thesis.
