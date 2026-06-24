# ZHAW Scientific Presentation Template

A modern, reusable **Beamer** template in the **ZHAW corporate design** — built for
Computer Science / scientific talks at the **ZHAW School of Engineering**. Bold-modern
look (full-bleed ZHAW-blue title & section slides, clean white content, thin accent
rules), first-class code support, and a clean separation of **styling** from **content**.

> Writing slides with an AI? Point it at **[`LLM-GUIDE.md`](LLM-GUIDE.md)**.

![Style: bold-modern · Engine: pdfLaTeX · Brand: ZHAW blue #0064A6](assets/zhaw-logo-blue.svg)

---

## Quick start

```bash
latexmk -pdf main.tex        # engine: pdfLaTeX  ->  main.pdf
```

Or just **save in VS Code** (LaTeX Workshop builds on save with its default
pdfLaTeX/latexmk recipe — no extra config). Needs a normal TeX Live / MacTeX install:
uses `beamer`, **Fira Sans/Mono** (`FiraSans`, `FiraMono`), `newtxsf` (sans math),
`tcolorbox`, `listings`, `tikz`/`pgfplots`, `biblatex`, `fontawesome5`,
`appendixnumberbeamer` — all standard. Works on Overleaf with compiler = **pdfLaTeX**.

To start a real talk:

1. Edit the **metadata block** in `main.tex` (title, author, school, unit, group).
2. Replace the demo files in `content/` with your own (one section per file).
3. Drop figures/screenshots into `assets/` and `\includegraphics{name}` them.
4. Tweak colours/toggles in the **CONFIG block** of `beamerthemezhaw.sty` if you like.

---

## File map

| File                                  | What it is                                             | Edit it? |
| ------------------------------------- | ------------------------------------------------------ | -------- |
| `main.tex`                            | Metadata, feature toggles, list of sections (`\input`) | ✅ yes    |
| `content/*.tex`                       | One section per file — your slides                     | ✅ yes    |
| `assets/`                             | Logos (generated) + your figures/screenshots           | ✅ yes    |
| `references.bib`                      | Bibliography (optional)                                | ✅ yes    |
| `beamerthemezhaw.sty` → **CONFIG**    | Colours, toggles, logos, geometry                      | ✅ yes    |
| `beamerthemezhaw.sty` → **MACHINERY** | The implementation                                     | ⛔ rarely |

Add a section = drop a file in `content/` (start it with `\section{...}`) and add one
`\input{content/...}` line in `main.tex`. Each `\section` auto-creates a blue divider slide.

---

## Authoring reference (short)

| You want…                              | Use                                                     |
| -------------------------------------- | ------------------------------------------------------- |
| Title slide                            | `\maketitle`                                            |
| Agenda                                 | `\zhawoutline`                                          |
| A slide                                | `\begin{frame}{Title}{Subtitle} … \end{frame}`          |
| Section + divider                      | `\section{Name}`                                        |
| Grouped points / example / caveat      | `block` / `exampleblock` / `alertblock`                 |
| Emphasis box                           | `\begin{callout}[Title] … \end{callout}`                |
| Theorem / definition                   | `theorem` / `definition` (numbered)                     |
| One big takeaway slide                 | `\statementframe{…}`                                    |
| Two columns                            | `columns` + `column`                                    |
| Inline code                            | `\code{plain}` · `\lstinline                            | with_specials | ` |
| Code block (frame must be `[fragile]`) | `\begin{codeblock}[python] … \end{codeblock}`           |
| Figure                                 | `\includegraphics[height=4.4cm]{file}` (from `assets/`) |
| Citation                               | `\cite{key}` (+ references slide)                       |

Full details and rules → **[`LLM-GUIDE.md`](LLM-GUIDE.md)**.

---

## Configuration (top of `beamerthemezhaw.sty`)

| Want to change…                               | Edit (in CONFIG)                       |
| --------------------------------------------- | -------------------------------------- |
| Brand / accent colours                        | §1a `\definecolor{...}`                |
| Progress bar / footer / frame numbers / logos | §1b toggles                            |
| Logo files (e.g. official print assets)       | §1c `\zhawlogolight` / `\zhawlogodark` |
| Page margins                                  | §1d `\zhawhmargin`                     |
| Code colours / line numbers                   | §2f `lstdefinestyle{zhaw}`             |

### Feature toggles (set in `main.tex`, after `\usetheme{zhaw}`)

```latex
\zhawprogressfalse    % hide the bottom progress bar
\zhawfootlinefalse    % hide the footer
\zhawframenumfalse    % hide frame numbers
\zhawframelogofalse   % hide the small corner logo on content slides
```

### Optional sections (build still works if removed)

- **References:** comment out the `biblatex` block in `main.tex` **and**
  `\input{content/90-references}`.
- **Appendix:** comment out `appendixnumberbeamer`, `\appendix`, and
  `\input{content/99-appendix}`.

---

## Branding & logos

The logos in `assets/` are generated from the official ZHAW SVG (the stacked **ZHAW**
monogram in corporate blue `#0064A6`, source: Wikimedia Commons, CC BY-SA 4.0) as
crisp vector PDFs — a blue version for white slides and a white version for the blue
title/section slides. The ZHAW name and logo are trademarks of the Zurich University of
Applied Sciences; use this template for ZHAW-affiliated presentations, and for official
print contexts swap in the print-quality assets ZHAW provides on request
(`zhaw.ch/…/engineering/about-us/media`). The corporate typeface is *Theinhardt*
(proprietary); this template uses **Fira Sans**, a close free alternative.

---

## Tips & troubleshooting

- **Build error on a code slide?** The frame needs `[fragile]`.
- **`Overfull \vbox ... too high`?** That slide overflows — split it or trim; don't shrink fonts.
- **Citations not showing?** Run the build twice (latexmk handles biber automatically).
- **Fonts missing?** `tlmgr install fira newtx` (or use a full MacTeX install).
- **Different default look?** This ships "bold-modern"; tweak colours/toggles in CONFIG.
