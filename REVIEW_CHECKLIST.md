# Thesis Revision Checklist — Reviewer Feedback Consolidated

Sources:
- **[S] = Reviewer 1 (Stockinger)** — digital PDF, 59 text comments + 124 highlights. Grade: **5.5**.
- **[B] = Reviewer 2 (Baglio)** — scanned PDF with handwritten margin notes (pages 2–11, 18, 30).

Page numbers are the **thesis page** where possible (Baglio scan page = thesis page + 1).
Legend: 🔴 must-fix · 🟠 should-fix · 🟢 suggestion / optional.

---

## 0. Meta-themes (from Stockinger's grade summary — highest priority)

These shape the whole document and are the main reason for the 5.5.

- [ ] 🔴 **AI vs. science / missing citations.** "Major problem: not clear which parts are AI hallucinations, great scientific ideas (without backing) or something in between." → Every factual/scientific claim needs a citation; state explicitly that methodology and ideas are the authors' own. [S p1]
- [ ] 🔴 **Astrophysics backing for all "scientific" claims / augmentations.** Data-augmentation justifications and astro statements must cite astrophysics literature or be reframed as engineering choices. [S p1, p5–7] [B p5]
- [ ] 🔴 **Remove the "IEEE Access" logo/branding.** Comes from `ieeeaccess.cls`. Switch class or strip the logo. [S p1]
- [ ] 🟠 **Condense.** Explanations are long; reader gets lost. Aim to cut main ideas to ~half with proper citing. [S p1]
- [ ] 🟠 **Fix figure legibility across the document** (see §7). Both reviewers repeatedly flag unreadable numbers/axes/dark plots.

---

## 1. Abstract & Introduction

### Abstract — ✅ DONE (rewritten in `Front/abstract.tex`)
- [x] 🔴 **Experiment count fixed: "four" → "five"**, QCNN (Experiment 5) now included.
- [x] 🟠 **Blanket "None shows a quantum advantage" nuanced** to "parity at best and no scalable quantum advantage" + QCNN few-shot inductive-bias caveat (no longer contradicts the discussion).
- [x] 🟠 **"most favourable setting for quantum hardware" → "for the variational methods studied here"** (neutralises Baglio's QRC/noise point). [B p30]
- [x] 🟠 **First sentence tightened** to the coarse star–galaxy–quasar task with near-perfect accuracy.
- [x] 🟢 **Two-episode framing** of the dissolved advantages made explicit.
- [x] 🟢 **Keyword "Benchmarking" added.** [B p2]

### Introduction — in progress
- [x] 🔴 **Fifth experiment (QCNN) added** to the second-contribution paragraph (was only four; now all five, with QCNN framed as negative control + few-shot nuance matching the abstract).
- [x] 🟢 **"the contribution is the comparison itself"** (highlighted by [S p3]) reworded to "our contribution is the fair-comparison methodology itself" — concrete + parallel to the other two contributions; long `, and` sentence split.

### Introduction — still TODO
- [x] 🟠 **Cite the M-dwarf / L-brown-dwarf spectral similarity.** ✅ Added Kirkpatrick (1999) `kirkpatrick1999ldwarfs` on the continuous-sequence / M→L transition clause, plus own-data Figure `fig:ml_similarity` (`Figures/brown_dwarf_L_vs_M8_mean.png`) for the near-identity. Citation deliberately not attached to the "near-identical" claim (that paper is about distinguishing them). [S highlight p2]
- [x] 🟠 **Back / soften "essentially solved / ~99% / even modest classical networks."** ✅ Attributed 99% to GaSNet-II `zhong2024gasnet`, replaced the unbacked "modest networks" flourish with a cited statement (`sharma2020cnn`). [S highlight p2–3] [B p2]
- [x] 🔴 **"the Beast" naming.** ✅ Intro now reads "which we nickname the \emph{Beast}" (own coinage, italicised). Note: soften the methodology "internally referred to as the Beast" so it doesn't re-introduce. [S highlight p3, p6] [B p3, p6]
- [x] 🟠 **"exponentially large state space / Hilbert space."** ✅ Replaced with "Hilbert space of dimension $2^n$" and dropped the "exploiting" overclaim. [B p2, p3]
- [ ] 🟠 **Fourier-series framing is not unique to quantum.** Baglio notes a classical NN can also be analysed "with the lens of FT." Qualify the data-reuploading/Fourier point. [B p3]
- [x] 🟢 **13-class subset phrasing mirrored into intro.** ✅ First contribution now reads "the same 13-class subset used in that study~\cite{zhong2024gasnet}". (Deeper "robustness to changing the subset" question is a results/methodology item, not intro.) [B p2]
- [x] 🟢 **"citation needed" near contributions.** ✅ Added `\cite{zhong2024gasnet}` on the "competitive with published state of the art" claim (the first-contribution sentence previously had no citation). [B scan p3]
- [~] 🟠 **"other work" / citations feel thin — mostly addressed for the intro.** ✅ Intro now cites 8 distinct refs (york, zhong ×2, sharma, kirkpatrick, perezsalinas, mcclean, henderson, bergholm). REMAINING (needs user input, better in `related_work.tex`): acknowledge fair-comparison is not unique and cite benchmarking literature incl. Baglio's own paper — need the reference. Also consider softening "our contribution is the fair-comparison methodology itself" so it doesn't overclaim novelty. [B p2, p4]
- [ ] 🟠 **Ensure every number matches final results tables** (84.5%, 92.5%, 96%, param counts). Reviewer highlights all of them. Abstract numbers verified ✅; still check intro/body. [S highlights p2–3]

---

## 2. Data & Augmentation

- [ ] 🔴 **"Scientific Augmentation" — astrophysics backing + naming.**
  - Each justification needs a reference or reframing: "simulate instrument read noise", "variations in object distance and apparent magnitude", "atmospheric seeing variations / lower-resolution instrument states." [S highlights p5–6, S comments p5–6]
  - Baglio: **title "Scientific Augmentation" is misleading** — "data augmentation means enlarging the dataset." Consider renaming. [B p5]
  - Baglio: **"why does this prevent overfitting?"** — justify the overfitting claim. [B p5]
- [ ] 🟠 **Flux value ranges vs. 4K bins.** State the flux ranges and relate to the 4096 bins. [S p6]
- [ ] 🟠 **Dataset generation questions.** "How did you generate the 642,588 dataset?" and "How was the subclass chosen for the capping (25k)?" [B p4]
- [ ] 🟢 **Figure 1 (spectral subclasses) is hard to read.** [B p5]
- [ ] 🟠 **Unfinished text — class-imbalance section.** "Sentence not finished / paragraphs missing / Incomplete!!" [S p6] [B p6]

---

## 3. Methodology — Baseline CNN ("the Beast")

- [ ] 🔴 **Architecture figure + provenance of the CNN.** "There should be an architecture figure of this CNN. Was it designed by you or based on related work? What is the best CNN in the astrophysics literature for this problem?" [S p6]
- [ ] 🟠 **Justify kernel sizes 5/15/31.** Both reviewers: "Why 5,15,31 and not 8,16,32?" / "What drives the choice of kernel sizes?" [S p6–7] [B p6]
- [ ] 🟠 **Justify other hyperparameters** (8 heads, 2048, OneCycle rate, weight decay). "What drives the hyperparameter choice? Hyper-tuning?" [B p6]
- [ ] 🟠 **"requires both fine-grained local + global receptive field" is not rigorous** — Baglio: claim is about *your sampled dataset*, not full SDSS. [B p6]
- [ ] 🟢 **Focal Loss — "nice idea"**; consider stating its aim explicitly. [B p6–7]
- [ ] 🟠 **Typo: 4069 → 4096.** [S p7] (Baglio also marks the 4096 bins.)
- [ ] 🟠 **Fig 2 (architecture) too small.** [B p7]

---

## 4. Methodology — Quantum Models & Fair Comparison

### Experiment 1 (Binary) — ✅ text done
- [x] Hard-pair choice justified: cross-refs baseline confusion matrix (Appendix A, `fig:cnn_baseline_confusion_matrix`), intro similarity figure (`fig:ml_similarity`), related work.
- [x] R_Y collapse (Baglio) defused: trainable gate is a general `Rot = R_Z·R_Y·R_Z`, does not commute with the R_Y upload, so no collapse; CNOT ring entangles.
- [x] "classical mirror" defined; "quantum model" + "classical mirror" named explicitly (fixes "both models" / "two binary models").
- [x] "three-angle Rot" written out; "qubit-against-depth" reworded plainly; "small quantum circuit" → "≤ 8 qubits".
- [x] "essentially trivial" / "principle of simplicity" wording removed.
- [x] Provenance: `SpectralFeatureExtractor` stated as own design, distinct from the 14M baseline (Fig 2).
- [x] Angle-vs-amplitude encoding justified (principled + points to Exp 5 ablation for evidence).
- STILL OPEN (Exp1): "why feature-width = qubits" micro-justification; redundancy pinpoint; figure sizing/legibility (figure pass).

### Experiment 2 (Frozen Extractor / four heads) — ✅ text done
- [x] **Parameter-equivalence reconciled** (A): dropped "angle and weight are not equivalent units"; now leads with structural matching ("not to the units we happen to count"). Fixes Baglio "matrices in both cases" + Stockinger "unclear". [S p8][B p8]
- [x] **AI-ish "Design Principles" reframed** (B): dropped "two principles / a third principle prompted by supervisor feedback"; practices kept as "standard practice". [S p8]
- [x] **Exp1↔Exp2 circuit difference explained** (C): single R_Y (Exp2) vs 3-angle Rot (Exp1) = 556-param budget; single-axis collapse defused via CNOT ring. Answers "difference Fig 5 vs 10?", "why three angles?", "where is the sweep?". [S p9][B p9,p10]
- [x] **Dimensionality "what is n?"** (D): 4096→128→4→4 qubits, n=4 stated. [S p11]
- [x] **Four classes / four qubits** (H): four hardest from confusion matrix; 4 qubits = one per class. [B p9]
- [x] **Beast redundancy / "same as Fig 2?"** (E): trimmed re-description, cross-refs baseline + Fig 2, "we do not repeat its architecture here". [S p8]
- [x] **Clarity** (G): "basic idea" opener + four-head roadmap; "why 'second experiment'?" bug fixed; Fig 5 caption (re-uploading/three-angles/pairs/L=n_layers); encoding-ablation purpose stated upfront. [S p9,p10]
- STILL OPEN (Exp2): **F provenance sentence** → deferred to §3 baseline; "where is the readout/channels shown?" → figure-labeling pass; **x̃ vs x_q** → Exp3.

### Cross-cutting (write ONCE as shared methodology note)
- [x] 🔴 **Parameter-count comparability.** ✅ Handled in Exp2 (A) — structural matching, no reliance on angle=weight. [S p8] [B p8]
- [ ] 🟠 **Cost/compute unfair.** Simulating quantum is exponentially hard. Address or drop. [B p8, p30]

- [x] 🔴 **Show baseline results BEFORE the hard classes / "haven't identified them experimentally."** ✅ Exp1 Design Principles now states the baseline's 62-class confusion matrix (Appendix A) identified the hard pair, with the similarity figure. Addressed via cross-reference (thesis stays method-then-results; no full reorder needed). [S p7]
- [x] 🔴 **Justify the hard pair choice IN THE THESIS.** ✅ Exp1 now cross-refs Appendix A confusion matrix + intro figure + related work. [S p7] [B p7, p30]
- [x] 🔴 **R_y(x)·R_y(θ) = R_y(θ + x).** ✅ Defused in Exp1 — trainable gate is a general 3-angle Rot (non-commuting with R_Y upload) + CNOT ring; no collapse. [B p9, p10]
- [~] 🟠 **Encoding choices — angle vs amplitude, qubit count.**
  - [x] "Why not amplitude?" ✅ Justified in Exp1 (principled reason + points to Exp5 ablation). [B p7]
  - [x] "Why 4 qubits?" → Exp2 (open). [B p9]
  - [x] "Why not data reuploading where n_features ≠ n_qubits?" → feature-width justification (open). [B p8]
  - [ ] Stockinger: "Maybe more qubits would have been better." → discussion/outlook. [S p30]
- [x] 🟠 **"Why 4 classes only?"** ✅ Exp2 — four hardest classes from the baseline confusion matrix; 4 qubits = one per class. [B p9]
- [x] 🔴 **Parameter-count comparability — reconcile the two reviewers.** ✅ Done in Exp2 (A). (See cross-cutting note above.) [S p8] [B p8]
- [ ] 🟠 **Cost/compute argument is unfair.** Simulating quantum is exponentially hard, so the compute-cost comparison is unfair. Address or drop. [B p8, p30]
- [x] 🟢 **Try R_x / more entangling gates.** ✅ Answered in Exp1 D-fix — the trainable `Rot` already contains `R_Z` (non-commuting with the R_Y upload) and the CNOT ring entangles; 3-axis variant also tried in Exp2 without benefit. [B p9]

### Undefined terms / inconsistent notation (all [S])
- [x] 🟠 Define **"classical mirror"** ✅ (defined at first use in Exp1). [S p7, p8]
- [ ] 🟠 Define **B, L, ch, n** (blocks, layers, channels, qubits). [S p7, p11]
- [ ] 🟠 Reconcile **x̃ vs x_q** notation (Fig 11 vs Fig 10). [S p12]
- [~] 🟠 **"three-angle rotation"** ✅ + **"qubit-against-depth"** ✅ done in Exp1. STILL: **"hardware-efficient"** (Exp2/other). [S p7, p12]
- [x] 🟠 Clarify **"two binary models"** / **"both models"** ✅ (named quantum model + classical mirror). [S p7, p8]
- [ ] 🟠 **"Black Holes"** naming — clarify it's unrelated to real black holes; discuss. [S p7]
- [x] 🟠 Rephrase **"trivial"** ✅ (removed in Exp1). [S p7]
- [ ] 🟠 Explain **data re-uploading / "sweep" / feature-per-qubit / pairs** — where shown? [S p9]
- [ ] 🟠 **Which figure shows which architecture?** Several "Is this the architecture in Figure 2/5/10/11?" [S p8, p9, p15, p16]
- [ ] 🟠 **Redundant section** — one methodology section repeats earlier content. [S p8]
- [ ] 🟠 **"is this from supervisors, rest from AI?"** — clarify sourcing of design principles. [S p8]
- [ ] 🟠 Clarify the 4K-flux → n-qubit mapping ("what is n?"). [S p11]

---

## 5. Results

- [ ] 🟠 **"Number of epochs too few?"** for the binary/quantum experiments. [B p18]
- [ ] 🟢 **"These findings are interesting"** (positive). [S p24]
- [ ] 🟠 **Combine Fig 8 & 9** for readability. [B p11]
- [ ] 🟠 **Where is the trainable linear readout shown?** [S p11]

---

## 6. Discussion & Conclusion

- [ ] 🟠 **Define "Huge CNN" and "Tiny CNN"** — informal names, undefined; "What are the Huge and Tiny CNNs?" [S p29]
- [ ] 🟠 **"101-gate quantum core" — what is it, and where shown experimentally?** [S p29]
- [ ] 🟠 **"How would you change the problem?"** — outlook expects a concrete answer. [S p30]
- [ ] 🟠 **"Not sure what this means"** — clarify final-paragraph statement. [S p30]
- [ ] 🟢 **Move QSVM/kernel theory to the discussion?** Baglio suggests shifting kernel material directly to discussion. [B p4]
- [ ] 🟢 **Noise can be useful in QML (QRC).** Baglio (re: presentation slide 17) — beware blanket "noiseless = most favourable" framing; quantum reservoir computing benefits from noise. Consider nuancing the "noiseless is the most favourable setting" claim. [B p30]

---

## 7. Figures (document-wide legibility)

- [ ] 🔴 **Training-history figures — axes/numbers unreadable.** [S p18 ×2] [B p18 "axis unreadable"]
- [ ] 🟠 **Confusion matrix hard to read — highlight the hard pair on it.** [B p7]
- [ ] 🟠 **Dark/low-contrast plots** (Figs ~20, 25–28) — hard to read on print. [B p18; visual p23, p25]
- [ ] 🔴 **Appendix A confusion matrix needs descriptive TEXT.** "Text describing it is missing. Having a figure is not enough." [B p30]
- [ ] 🟢 Fig 1, Fig 2 too small (see §2, §3).

---

## Quick "definitely must-fix" shortlist (🔴)

1. Remove IEEE Access logo (class change).
2. Add citations everywhere / disambiguate AI vs. science.
3. Astrophysics backing for augmentations (+ rename "Scientific Augmentation").
4. "the Beast" — mark as your own invented name.
5. Justify the hard-pair choice in the thesis text (not just the talk).
6. Address the R_y(x)·R_y(θ) = R_y(θ+x) collapse (encoding/entanglement).
7. Defend the parameter-matching argument (reconcile with Baglio's "it's matrices in both cases").
8. Add architecture figure + provenance for the baseline CNN.
9. Fix unreadable figures; add descriptive text to Appendix A confusion matrix.
10. Finish the incomplete class-imbalance section.
