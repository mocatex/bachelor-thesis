# Writing Guide - IEEE Access Modular Template

Welcome to your new modular IEEE Access template! This structure is designed to be organized, easy to maintain, and similar to your previous thesis setup.

## 📁 Project Structure

The project is divided into several folders to keep things clean:

- **`main.tex`**: The main entry point. You usually only touch this to add or reorder chapters.
- **`Settings/`**:
    - `preamble.tex`: Load packages and global configurations here.
    - `metadata.tex`: Define your paper title, authors, affiliations, and DOI information.
- **`Front/`**:
    - `abstract.tex`: Contains the abstract and index terms (keywords).
- **`Chapters/`**:
    - Individual `.tex` files for each section of your paper.
- **`Appendices/`**:
    - `appendices.tex`: Put your appendix content here.
- **`Back/`**:
    - `references.tex`: Manual bibliography using `thebibliography` (if not using BibTeX).
    - `biographies.tex`: Author biographies and photos.
- **`references.bib`**: BibTeX file for managing citations (recommended).

---

## 🚀 How to use

### 1. Adding or Reordering Chapters

To add a new chapter, create a new `.tex` file in the `Chapters/` folder. Then, include it in `main.tex` using the `\input{}` command:

```latex
% In main.tex
\input{Chapters/01_introduction}
\input{Chapters/06_my_new_chapter} % Add your new chapter here
```

To reorder, simply swap the lines in `main.tex`.

### 2. Including Graphics

Use the `\Figure` command (provided by the `ieeeaccess` class) or the standard `\begin{figure}`.

**Example using `\Figure`:**

```latex
\Figure[t!](topskip=0pt, botskip=0pt, midskip=0pt){fig1.png}
{Caption of your figure.\label{fig:my_label}}
```

**Example using standard LaTeX:**

```latex
\begin{figure}[htbp]
    \centering
    \includegraphics[width=\linewidth]{logo.png}
    \caption{Description of the logo.}
    \label{fig:logo}
\end{figure}
```

*Note: All images should be placed in the root directory or you can specify a path.*

### 3. Citations

You have two options for citations:

#### Option A: BibTeX (Recommended)

1. Add your sources to `references.bib`.
2. In `main.tex`, replace `\input{Back/references}` with:

    ```latex
    \bibliographystyle{IEEEtran}
    \bibliography{references}
    ```

3. Use `\cite{key}` in your text.

#### Option B: Manual (Template Default)

Edit `Back/references.tex` and add `\bibitem{key}` entries.

### 4. Metadata (Title & Authors)

Open `Settings/metadata.tex` to change the title, authors, and contact information. Use `\uppercase` for author names as per IEEE standards.

### 5. Compiling

You can compile the project using `latexmk`:

```bash
latexmk -pdf main.tex
```

Or in VSCode, just save `main.tex` and it should auto-compile if you have the LaTeX Workshop extension installed.

---

## 💡 Tips

- **Labels:** Use descriptive labels like `\label{sec:intro}` or `\label{fig:results}` to make cross-referencing easy with `\ref{}` or `\eqref{}`.
- **Math:** Use `\begin{equation}` for numbered equations.
- **Tables:** Use `\begin{table}` and `\begin{tabular}`. There is an example in `Chapters/04_graphics.tex`.

Happy writing! 📝
