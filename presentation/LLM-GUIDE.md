# LLM-GUIDE — authoring a ZHAW scientific presentation

You are filling a **16:9 Beamer presentation** that uses the **ZHAW "bold-modern"**
theme (`\usetheme{zhaw}`). Optimise for a clear, confident scientific talk:
**one idea per slide**, generous whitespace, the brand blue used with intent.
Follow these rules exactly.

## Hard rules

1. **Engine is pdfLaTeX.** Build with `latexmk -pdf main.tex`. Do **not** use
   `fontspec`, `minted`, XeLaTeX/LuaLaTeX, or `-shell-escape`.
2. Write slide content **only** in `content/*.tex`. Register sections in `main.tex`
   via `\input`. Set talk metadata in `main.tex` (title block).
3. You **may** edit the **CONFIG block** at the top of `beamerthemezhaw.sty`
   (colours, toggles, logo paths, geometry). **Do not** edit anything under the
   **MACHINERY** banner unless explicitly asked.
4. **Any frame that contains code** (`codeblock`, `\lstinline`, `\verb`) **must**
   be declared `\begin{frame}[fragile]`. Forgetting this is the #1 build error.
5. **One idea per slide.** If content overflows (a build warning
   `Overfull \vbox ... too high`), split the frame or shorten — do not shrink fonts.
6. Keep the brand: don't recolour slides arbitrarily; use the provided components.

## File model

- One **section per file** in `content/`, e.g. `content/02-method.tex`.
- Each file begins with `\section{Title}` (this auto-generates a blue divider slide).
- Add the file to `main.tex` with `\input{content/02-method}` (no `.tex`).
- Reorder sections by reordering the `\input` lines.

## Metadata (in `main.tex`, before `\begin{document}`)

```latex
\title[Short title]{Full Title}   % [short] appears in the footer
\subtitle{One-line subtitle}
\author{Your Name}
\date{\today}
\zhawschool{School of Engineering}                  % the school
\zhawunit{Centre for Artificial Intelligence (CAI)} % dept / institute / centre
\zhawgroup{Machine Perception \& Cognition Group}   % research group (optional)
\zhawevent{Conference / Course name}                 % optional
```

These feed the title slide lock-up and the footer. Leave `\zhawgroup`/`\zhawevent`
empty (`{}`) if unused.

## Slides

```latex
\begin{frame}{Frame title}{Optional subtitle}
  ...content...
\end{frame}
```

- A `\section{...}` automatically inserts a full-bleed blue **divider** slide
  (numbered, e.g. "02"). Don't build dividers by hand.
- Title page: `\maketitle`. Agenda: `\zhawoutline` (optional; shows the TOC).

## Components (use these, classify by meaning)

### Bullet lists
Plain `itemize`/`enumerate` (blue square bullets are automatic). Keep to ~5 lines.

### Blocks — colour = meaning
```latex
\begin{block}{Title}        ...grouped points...     \end{block}        % blue
\begin{exampleblock}{Title} ...worked example...     \end{exampleblock} % green
\begin{alertblock}{Title}   ...caveat / pitfall...   \end{alertblock}   % red
```

### Callout — the signature box (tinted, blue accent bar)
```latex
\begin{callout}[Optional title]  The one thing to remember.  \end{callout}
```
Omit `[title]` for an untitled callout. Use sparingly — it's for emphasis.

### Theorem / Definition (numbered, blue)
```latex
\begin{definition}[Name] ... \end{definition}
\begin{theorem}[Name]    ... \end{theorem}
```

### Statement slide — one big idea, full-bleed
```latex
\statementframe{93\% accuracy — a +8 point gain over baseline.}
\statementframe[zhawblue]{Use blue instead of the default navy.}
```
This is its own slide; don't put it inside a `frame`.

### Two columns
```latex
\begin{columns}[T]
  \begin{column}{0.5\textwidth} ... \end{column}
  \begin{column}{0.5\textwidth} ... \end{column}
\end{columns}
```

### Figures / screenshots
Image files live in `assets/`; reference them **without** the folder or extension.
```latex
\centering
\includegraphics[height=4.4cm]{my-plot}\par      % keep height <= ~4.6cm
{\small\color{zhawgrey}\textbf{Figure:}~caption.}
```
Prefer a fixed `height` (≈ 4–4.6 cm) over `\textheight` fractions, and avoid the
floating `figure` environment on slides — both tend to overflow.

### Math
`amsmath` is loaded and math is sans-serif (matches the font). `\argmin`/`\argmax`
are predefined. Put a key equation on its own line with `\[ ... \]`.

### Tables
Use `booktabs` (`\toprule`/`\midrule`/`\bottomrule`). Bold the winning row.

## Code (this is a CS-friendly template)

```latex
\code{model.eval()}        % inline pill — ONLY for snippets without _ # % & { } \
\lstinline|loss = w_i*x_i| % inline WITH special chars (_ # % & { } \)

\begin{frame}[fragile]{...}       % <-- fragile REQUIRED
\begin{codeblock}[python]         % language optional; drives highlighting only
def f(x):
    return x * 2
\end{codeblock}
\end{frame}
```

- Use `\lstinline|...|` (not `\code{}`) whenever the snippet contains `_ # % & { } \`.
- `language` = any `listings` language (`python`, `bash`, `c`, `Java`, `SQL`, …).
- Code blocks are line-numbered; turn that off per-theme with `numbers=none`
  in the `codeblock` definition (CONFIG §2f).

## Optional features (keep or remove cleanly — the build never breaks)

- **References:** keep the `biblatex` lines + `\addbibresource{references.bib}` in
  `main.tex` and `\input{content/90-references}`. To remove references entirely,
  comment out **both** the biblatex block and that `\input`. Cite with `\cite{key}`.
- **Appendix / backup:** keep `\usepackage{appendixnumberbeamer}` + `\appendix` +
  `\input{content/99-appendix}`. To remove, comment out all three. Backup slides
  are numbered separately from the main talk.
- **Navigation / chrome (toggles in `main.tex`, after `\usetheme{zhaw}`):**
  `\zhawprogressfalse` (bottom bar), `\zhawfootlinefalse` (footer),
  `\zhawframenumfalse` (frame numbers), `\zhawframelogofalse` (corner logo).

## Pitfalls checklist

- Code/verbatim on a slide → the frame **must** be `[fragile]`.
- Don't start a `content/*.tex` file with `\documentclass`/preamble — it is
  `\input`-ed mid-document.
- Don't load packages in `content/*.tex`; add them to `main.tex`'s preamble.
- A `tikzpicture` placed directly inside a raw `\if...\fi` breaks the build — the
  theme already handles its own logos; you rarely need raw conditionals.
- Watch the log for `Overfull \vbox ... too high` → that slide overflows; split it.
- Balance every `\begin{...}` with `\end{...}`.
