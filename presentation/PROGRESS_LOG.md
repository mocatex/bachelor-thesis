# Presentation — Progress Log / Handoff

**Status: COMPLETE and building cleanly.** This log lets a fresh chat resume instantly.

## What this is
The Bachelor-thesis defense talk for **"Quantum Machine Learning for Analyzing
Astronomical Objects"** (authors: Moritz Feuchter & Shpetim Veseli). ZHAW bold-modern
Beamer theme, pdfLaTeX. Brief from the professor: 30 min talk + 15 min Q&A — describe the
problem, main approaches, most important results, conclusions, next steps.

Final build: **58 pages** = 41 main slides + **17 backup/appendix slides**.
0 overfull boxes, 0 undefined citations, all figures resolve.

## Build command  ⚠ IMPORTANT
The **repo root** (`bachelor-thesis/`) has the THESIS `main.tex`. Always build from
inside `presentation/`:
```bash
cd /Users/moritz/ZHAW-code/bachelor-thesis/presentation
latexmk -pdf main.tex          # -> presentation/main.pdf  (run from THIS dir!)
```
VS Code LaTeX Workshop (build-on-save) works too, with the file open from this folder.
To render slides to images for review:
`pdftoppm -png -r 60 main.pdf /tmp/slides/s` (use absolute paths; cwd can reset).

## File map (all under presentation/)
- `main.tex` — metadata (title/authors/school), section `\input`s, closing slide.
- `content/01-intro.tex` — **The Problem** (4 slides).
- `content/02-background.tex` — **Background & Approaches** (2 slides).
- `content/03-baseline.tex` — **Data & Classical Baseline / the Beast** (4 slides).
- `content/04-exp1.tex` — **Exp 1 · Binary VQC** (3 slides).
- `content/05-exp2.tex` — **Exp 2 · Frozen-feature heads** (4 slides).
- `content/06-exp345.tex` — **Exp 3/4/5** kernels, quanvolution, true QCNN (3 slides).
- `content/07-conclusion.tex` — **Conclusions & Outlook** (5 incl. statement frame).
- `content/90-references.tex` — auto bibliography (`allowframebreaks`).
- `content/99-appendix.tex` — **17 backup slides** (numbered separately, "n/17").
- `references.bib` — copied from thesis root (35 entries; all `\cite` keys resolve).
- `assets/` — all thesis `Figures/*.png` + `*.pdf` were copied here (theme resolves
  `\includegraphics` from `assets/`; reference WITHOUT folder/extension).
- `beamerthemezhaw.sty` — theme (CONFIG block editable; MACHINERY don't touch).

## Narrative spine (the thesis story)
Problem: SDSS has ~2M spectra; coarse star/galaxy/quasar is solved (~99%), fine-grained
subclasses are hard. Can QML help where classical struggles? → **Fair-comparison discipline**:
every quantum model matched (params + pipeline) to a classical twin. Baseline "Beast" (14M
params, 84.5% / 92.5% GaSNet-II) → 5 experiments → **parity, never advantage**. Two apparent
advantages dissolved (under-built baseline; dead-ReLU artefact). The methodology is the
contribution. Outlook: quantum-native data, real hardware, more qubits, geometric pre-screening.

## Backup slides cover (for Q&A "surprise")
barren plateaus (and why our spiky curves aren't one), data re-uploading + Fourier view,
dead-ReLU mechanism, parameter-matching philosophy, Fisher-discriminant "why", geometric
difference g(C‖Q), fidelity vs projected kernels, amplitude vs angle encoding, quanvolution
circuit + Jacobian, QCNN barren-plateau immunity + Caro bound, compute cost / noiseless caveat,
62×62 confusion analysis, data choices (leakage/imbalance/augmentation), full result tables
(Exp 1, 4, 5).

## Key facts/numbers (for editing accuracy)
- Dataset: 642,588 spectra, 62 classes, SDSS DR19; redshift withheld (leakage).
- Baseline: 84.50% (62-class), 92.51% (13-class GaSNet-II replica).
- Exp 1 hardest pair: STAR_BROWN_DWARF_L vs STAR_M8; best Q 0.869 ≈ best C 0.868.
- Exp 2: A(5058p), B quantum(556p), C ReLU(556p, ~79% collapse), D tanh(556p, ~96%).
- Exp 3: g_fidelity=1.89, g_projected=12.01; classical RBF wins for n≥50.
- Exp 4: only Adv-Light significant (p=0.014), favours classical.
- Exp 5: Huge CNN wins when scaling allowed; QCNN dominates Tiny CNN at parity / few-shot.

## Decisions made (confirmed by Moritz)
- Title: "Quantum Machine Learning for Analyzing Astronomical Objects".
- Authors on title slide: Moritz Feuchter & Shpetim Veseli.
- Depth: balanced (circuits shown, heavy math in backup).

## Fixes applied (round 2)
- **First-render crash + persistent "failed to resolve citations"**: ONE root cause, in the
  progress bar of `beamerthemezhaw.sty` §2m. On pass 1 `\inserttotalframenumber` is 0. Dividing
  by it gives "Dimension too large"; and PGF's ternary `cond ? a : b` evaluates BOTH branches,
  so even `total<1 ? 0 : n/total` still runs `n/0` → "divide by 0". Either way pdflatex exits 1
  on pass 1, so latexmk stops BEFORE biber and citations never resolve (that's why a rerun
  "fixed" it — the aux then had the frame total). Real fix: guard at the TeX level with
  `\ifnum\inserttotalframenumber<1 \def... \else \pgfmathsetmacro... \fi`, so the division is
  never reached until the total is known. Verified: first pdflatex pass exits 0, a single
  `latexmk` resolves all citations, 0 overfull boxes. (Do NOT reintroduce a PGF-level ternary
  guard here — PGF evaluates both branches and the div-by-zero returns.)
- **Duplicate "Bachelor Thesis Defense"**: it was in both `\date{}` and `\zhawevent{}`; the
  title slide prints `event • date`. `\date{}` is now just `\today`.
- **Title/subtitle too big**: sizes live in `beamerthemezhaw.sty` §2h `\zhawmaketitle`
  (`\fontsize{24}{28}` title, `\fontsize{13}{17}` subtitle) — adjust there.
- **Overflow fixes** (figure+text taller than the frame; tcolorboxes don't trigger vbox
  warnings, so check visually): p13 Beast blocks, p32 gradcam (square 2400×2400 image → now
  `height=5cm`, callout replaced by inline bold), appendix-1 barren plateau boxes.

## Structure update (resolved with Moritz)
- **Exp 3/4/5 now each their own section** (2 slides each): `06-exp3.tex` (Quantum Kernels),
  `07-exp4.tex` (Quanvolution), `08-exp5.tex` (True QCNN). Conclusion moved to `09-conclusion.tex`.
  Old combined `06-exp345.tex` deleted. Deck is now **64 pages** (46 main + 18 backup).
- **Jacobian slopegraphs**: added as backup slide 15 ("Jacobian smoothness slopegraphs",
  appendix 18/18) using `jacobian_slope_QCNN_vs_CNN_Huge/Tiny`. Backup index updated.
- Watch the wide arch figures: `qcnn_model` is only 3.06:1 (taller than the others), so it is
  set to `width=0.72\textwidth` on the Exp 5 setup slide to leave room for the blocks below.

## Possible future tweaks (optional, not required)
- Add presenter notes (`\note{}`) if a notes-handout is wanted.
- Tighten timing by trimming Exp 3/4/5 to 1 slide if the talk runs long in rehearsal.
- Swap dark-background result PNGs for light versions if projector contrast is poor.
- The Plan file: `/Users/moritz/.claude/plans/merry-gliding-milner.md`.
