# LaTeX Writing Guide

This guide provides instructions and examples for writing this thesis using LaTeX, including how to include code snippets, images, citations, and custom commands.

## 0. General Writing

### 0.1 Needed Plugins in VSCode

- You need the `LaTeX Workshop` extension for VSCode.
- Nice-to-have: `Formula Editor` for a quick WYSIWYG math editor.

### 0.2 Settings in LaTeX Workshop

In the LaTeX Workshop settings, set:

- `Formatting>LaTeX` to `latexindent` for auto-formatting.
- `LaTeX>Auto Clean : Run` to `onBuilt` or `onSucceeded` to auto-clean auxiliary files.

### 0.3 Compiling

Change the out-dir in `settings.json` to:

```json
"latex-workshop.latex.outDir": "./build",
```

The Clean-Method to `glob`,
And the clean patterns to:

```json
"latex-workshop.latex.clean.patterns": [
    ...,
    "*.aux",
    "*.synctex.gz",
],
```

So auxiliary in `build/` are cleaned automatically.

After that, per default you build when saving the file (Ctrl+S).
You can also manually build with `Ctrl+Alt+B`.
Or change it to `onFileChange` to build on every change.

### 0.4 How to write chapters

You write your chapters in the `Chapters/` folder as `.tex` files and include them in `main.tex` using:

```latex
\include{Chapters/chapter1}
```

## 1. Code snippets

We use the **`listings`** package (no Python/Pygments needed).

### 1.1 Inline code

Use this for short snippets you write directly in `.tex`:

```latex
\begin{lstlisting}[language=Python, caption={Simple Python function}]
def square(x):
    return x * x
\end{lstlisting}
```

- `language=Python` → choose language (`Java`, `C++`, etc.).
- `caption={...}` → adds a title under the code block.
- Add `label={lst:mysnippet}` if you want to reference it with `\ref{lst:mysnippet}`.

### 1.2 Import external file

For longer code, save it in `Code/` and import:

```latex
\lstinputlisting[language=Python, caption={Example from external file}]{Code/example.py}
```

---

## 2. Images

Images go into the `Figures/` folder. Use:

```latex
\begin{figure}[ht]
  \centering
  \includegraphics[width=0.7\textwidth]{Figures/mydiagram.png}
  \caption{System architecture overview.}
  \label{fig:system-arch}
\end{figure}
```

- `width=0.7\textwidth` → scales the image.
- `\label{fig:...}` → allows referencing with `Figure~\ref{fig:system-arch}`.
- Formats supported: `.png`, `.jpg`, `.pdf`.

---

## 3. Citations and References

We use **`biblatex` with biber**.

1. Add sources in `example.bib`:

    ```bibtex
    @book{knuth1984,
    author = {Donald E. Knuth},
    title = {The TeXbook},
    year = {1984},
    publisher = {Addison-Wesley}
    }
    ```

2. Cite in text:

    ```latex
    As shown by Knuth \cite{knuth1984}, typesetting is an art.
    ```

3. Print the bibliography at the end is already done via:

    ```latex
    \printbibliography
    ```

---

## 4. Info Boxes (Custom Environments)

You can create **info boxes** to highlight tips, warnings, or examples.
Add this to `preamble.tex`:

```latex
\usepackage{tcolorbox}
\tcbset{colback=blue!5!white, colframe=blue!75!black, boxrule=0.8pt, arc=4pt}

\newtcolorbox{infobox}[1][]{title=Note,#1}
```

Now you can write:

```latex
\begin{infobox}[title=Important]
Always compile with **biber** (not bibtex) for references!
\end{infobox}
```

👉 This produces a nice blue info box.

---

## 5. Custom Commands

To avoid repeating long LaTeX code, you can define shortcuts in `preamble.tex`.

Examples:

```latex
% Commonly used terms
\newcommand{\AI}{Artificial Intelligence}
\newcommand{\ZHAW}{Zurich University of Applied Sciences}

% Shorthand for figure refs
\newcommand{\figref}[1]{Figure~\ref{#1}}
```

Usage in text:

```latex
At \ZHAW, research in \AI{} is growing rapidly.
As shown in \figref{fig:system-arch}, the system scales well.
```

---

## 6. Tables

Use the `booktabs` package (already loaded). Example:

```latex
\begin{table}[ht]
  \centering
  \begin{tabular}{l c r}
    \toprule
    Method & Accuracy & Runtime \\
    \midrule
    Baseline & 75\% & 10s \\
    Improved & 89\% & 7s \\
    \bottomrule
  \end{tabular}
  \caption{Comparison of methods.}
  \label{tab:methods}
\end{table}
```

Reference it with `Table~\ref{tab:methods}`.

---

## 7. Cross-references

Use labels + refs consistently:

- `\label{fig:xyz}` for figures → `Figure~\ref{fig:xyz}`
- `\label{lst:xyz}` for code → `Listing~\ref{lst:xyz}`
- `\label{tab:xyz}` for tables → `Table~\ref{tab:xyz}`

---

## 8. Math

### 8.1 Inline math

For formulas **inside text**:

```latex
The function $f(x) = x^2$ grows quadratically.
```

-> Use **`$ ... $`** (or `\(...\)` if you prefer).

---

### 8.2 Display math (no number)

For formulas **on their own line**:

```latex
\[
E = mc^2
\]
```

-> Use **`\[ ... \]`** for unnumbered equations.

---

### 9.3 Numbered equations

For important equations you want to reference:

```latex
\begin{equation}
E = mc^2
\label{eq:einstein}
\end{equation}

Einstein's formula is shown in Equation~\eqref{eq:einstein}.
```

-> Use **`equation`** with `\label` + `\eqref{...}`.
This makes your references consistent and clickable.

---

### 9.4 Aligned equations

For multi-line derivations:

```latex
\begin{align}
a &= b + c \\
  &= d + e
\end{align}
```

-> Use **`align`**

- `&` marks alignment points.
- Each line is auto-numbered (use `align*` for no numbers).
