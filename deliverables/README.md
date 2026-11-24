# Deliverables

Everything the group presents or submits, in one place.

| Folder | Contents | Rebuild |
|---|---|---|
| `presentation/` | **`INT4096_Presentation.pdf`** (final deck) | `bash deliverables/presentation/slides/build.sh` |
| `presentation/slides/` | Beamer source `main.tex`, `figures/`, `generated/` (numbers and tables written from `experiments/`) | same |
| `presentation/script/` | **`speaker_script_bilingual.md` / `.pdf`**: the words each speaker says, English with Chinese translation | `python scripts/build_script_pdf.py` |
| `presentation/planning/` | `timing_plan.md` (speakers and clock), `storyboard.md`, `speaker_notes.md` (Q&A routing), `feature_extraction_story.md` (the narrative the deck follows) | — |
| `report/` | **`INT4096_Final_Report.pdf`**, `word_count.txt`, `report_draft.md`; LaTeX source in `latex/` | `bash deliverables/report/latex/build.sh` |
| `notebook/` | **`INT4096_Final_Colab.ipynb`** (rebuilds the results), `INT4096_Colab_Teaching_Template.ipynb` (student workbook) | `python scripts/build_notebook.py` |
| `lesson/` | Lesson plan, five formative tasks with worked answers, teacher notes | — |
| `website/` | **`index.html`**: interactive step-by-step explainer of the whole pipeline (data, split, features, tuning, evaluation, experimental neural nets, verdict). Opens straight from disk; `template.html` is the hand-written source | `python scripts/build_website.py` |

Speakers: Dong Yuankun slides 1–5 · Zhang Yancheng 6–12 · Zhang Haoyu 13–15 · Lau Pak Hei 16 · Lui Shing Lam 17.
