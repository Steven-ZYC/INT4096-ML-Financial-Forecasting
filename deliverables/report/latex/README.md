# LaTeX Report — Build and Provenance

Compiled output: [`../INT4096_Final_Report.pdf`](../INT4096_Final_Report.pdf)
(10 pages, A4).
Word count: [`../word_count.txt`](../word_count.txt) — **2,136 body + 102 headings = 2,238**.

## Build

```bash
# once per machine: a TeX distribution with latexmk, bibtex, texcount
# (TeX Live, or TinyTeX: sh install-bin-unix.sh then tlmgr install <packages>)

bash deliverables/report/latex/build.sh          # regenerate assets, compile, count, copy PDF
bash deliverables/report/latex/build.sh --clean  # remove aux files first
```

The script fails loudly if `latexmk` or `texcount` is missing, and it reports
overfull boxes and warnings rather than glossing over them. A clean build prints
`overfull/underfull boxes: 0` and `LaTeX/package warnings: 0`.

Engine: `pdflatex` via `latexmk`, bibliography via `bibtex` with `plainnat`
(natbib). No biber/biblatex, to keep the dependency surface small.

### Byte-reproducible builds

The build pins `SOURCE_DATE_EPOCH` to a fixed project constant
(`2026-10-29T00:00:00Z`, overridable with `INT4096_SOURCE_DATE`) and passes the
same fixed metadata to matplotlib. Without this, every build differed: pdfTeX
embeds its own timestamp and matplotlib stamps `CreationDate` into each figure.

SHA-256 of the committed PDF:

```
032f285c91ba820c96ccb52ee6c5a252600deccd3e010dace20fd21d31507f88  INT4096_Final_Report.pdf
```

The epoch must not be derived from `HEAD`: committing the rebuilt PDF would move
`HEAD`, change the epoch, and change the PDF — a circular dependency.

## Nothing empirical is typed by hand

Run `python scripts/build_latex_assets.py` (the build script does it) and the
following are regenerated from `experiments/models/`:

| File | Source |
|---|---|
| `generated/results_table.tex` | every `metrics.json` (validation split only) |
| `generated/ablation_table.tex` | matched P0/P2 runs per model and asset |
| `generated/dataset_table.tex` | snapshot manifests + validation report |
| `generated/splits_table.tex` | `prepare_dataset()` on the frozen protocol |
| `generated/numbers.tex` | measured values used in prose, as LaTeX macros |
| `figures/*.pdf` | matplotlib, vector output, one `.caption.txt` per figure with run IDs |

Prose therefore cites `\SkillAAPLRandomForest` rather than a literal number: a
re-run that changes a result changes the sentence, and the report cannot drift
from the artifacts.

## Word-count policy

The written specification allows **2,000 words excluding figures, tables and
references**. The instructor separately allowed approximately **500 more in
face-to-face consultation**, reported by the project owner. That is recorded as
oral guidance, not as a published rule, so the report states both.

The team limits the narrative to 2,300 words.
`texcount -inc -sum main.tex` is the measurement:

- **Words in text: 2,136** — body prose across `main.tex` and every `\input` section.
- **Words in headers: 102** — section and paragraph headings.
- **Narrative total: 2,238.**
- **Words outside text: 480** — figure captions and float content, excluded from
  the narrative figure, consistent with the specification's exclusion of figures
  and tables. Captions are still counted and reported here so nothing is hidden.

Not counted as narrative: bibliography entries, table bodies, the title block,
LaTeX markup and citation keys.

This is a reproducible count, not a claim about the instructor's own tool. If
their counter includes captions, the figure would be about 2,720 and the owner
should discuss it; `deliverables/report/word_count.txt` records the exact configuration used.

## Layout checks performed

- A4, 10 pages.
- Log: 0 overfull boxes, 0 warnings; 2 underfull boxes in the generated neural-network
  table (`generated/dl_table.tex`).
- `pdftotext`: 0 unresolved `??` references; all 7 figures and 4 tables present;
  10 citations rendered.

## Author block

The title block reads `INT4096 Group Project` with a footnote pointing at
`docs/project/responsibilities.md`. Individual names are deliberately not
committed to a public-facing repository. Override without editing the source:

```bash
pdflatex "\def\GroupAuthors{ZHANG Yancheng \and Member Two \and ...}\input{main.tex}"
```
