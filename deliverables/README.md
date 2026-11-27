# Deliverables

Everything the group presents or submits, in one place.

| Folder | Contents | Rebuild |
|---|---|---|
| `presentation/` | **`INT4096_Presentation.pdf`** (final deck) | `bash deliverables/presentation/slides/build.sh` |
| `presentation/slides/` | Beamer source `main.tex`, `figures/`, `generated/` (numbers and tables written from `experiments/`) | same |
| `presentation/script/` | **`speaker_script_bilingual.md` / `.pdf`** contains the English script and Chinese translation for every speaker. `zhang_yancheng_slides_6-12.md` / `.pdf` puts the English script and short Chinese cues together for each slide. | `python scripts/build_script_pdf.py` |
| `presentation/planning/` | `timing_plan.md` (speakers and clock), `storyboard.md`, `speaker_notes.md` (Q&A routing), `feature_extraction_story.md` (the narrative the deck follows) | — |
| `report/` | **`INT4096_Final_Report.pdf`**, `word_count.txt`, `report_draft.md`; LaTeX source in `latex/` | `bash deliverables/report/latex/build.sh` |
| `notebook/` | **`INT4096_Final_Colab.ipynb`** (self-contained, rebuilds the results), `INT4096_Final_Colab_executed.ipynb` (same notebook with saved outputs), `INT4096_Colab_Teaching_Template.ipynb` (student workbook) | `python scripts/build_notebook.py`, then `python scripts/execute_notebook.py` (setup: [`notebook/README.md`](notebook/README.md)) |
| `lesson/` | Lesson plan, five formative tasks with worked answers, teacher notes | — |
| `website/` | **`index.html`**: interactive step-by-step explainer of the whole pipeline (data, split, features, tuning, evaluation, experimental neural nets, verdict). Opens straight from disk and is published at https://steven-zyc.github.io/INT4096-ML-Financial-Forecasting/ by `.github/workflows/pages.yml`; `template.html` is the hand-written source | `python scripts/build_website.py` |

Speakers: Dong Yuankun slides 1–5 · Zhang Yancheng 6–12 · Zhang Haoyu 13–15 · Lau Pak Hei 16–17 · Lui Shing Lam 18.

## Moodle submission

Two uploads, built into [`../submission/`](../submission/) by
`python scripts/package_submission.py --group-id <ID>`:

| Upload | File name |
|---|---|
| Report | `INT4096 [Group ID] - Group Project Report.pdf` |
| Deliverables | `INT4096 [Group ID] - Group Project Deliverables.zip` |

Replace `[Group ID]` with the group's ID. The zip contains:

| In the zip | Contents |
|---|---|
| `README.md` | List of files and how to run the notebook |
| `Presentation/` | `INT4096_Presentation.pdf` |
| `Notebook/` | `INT4096_Final_Colab.ipynb` and its executed copy with saved outputs |
| `Dataset/` | The two original data files (AAPL, BTC) and their manifests |
| `Lesson/` | Lesson plan, formative tasks with answers, teacher notes |

The report is not repeated inside the zip. Rebuild after any change to these files.

