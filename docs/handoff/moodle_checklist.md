# Moodle Submission Checklist — 28 November 2026, 23:59 HKT

**GitHub is not a submission.** A successful push proves nothing about Moodle.
Each item below must be ticked by a named human who actually saw the upload
confirmation. Do not mark anything complete on the basis of a local file.

Deadlines from the course specification (transcribed; verify against the
official handout, which is not archived in this repository):
draft slides **18 Nov 2026 18:00**, presentations **19 and/or 26 Nov**,
final submission **28 Nov 2026 23:59 HKT**, with a **10% per day** late penalty.

---

## Required uploads (all four)

| # | Deliverable | Source file | Format | Owner | Uploaded | Verified |
|---|---|---|---|---|---|---|
| 1 | Final report | `reports/final/INT4096_Final_Report.pdf` | PDF | | ☐ | ☐ |
| 2 | Presentation slides | `docs/presentation/` → exported deck (see note) | PPTX or PDF | | ☐ | ☐ |
| 3 | Original dataset | `data/raw/aapl_daily.json`, `data/raw/btc_daily.json` (+ manifests) | JSON/CSV | | ☐ | ☐ |
| 4 | Colab-compatible notebook | `notebooks/INT4096_Final_Colab.ipynb` | `.ipynb` | | ☐ | ☐ |

**Note on slides:** the storyboard exists (`docs/presentation/storyboard.md`) but
an exported PPTX/PDF has **not been produced** in this repository. Exporting it
is outstanding work; do not tick item 2 until a real deck file exists and was
opened to confirm it renders.

---

## Pre-upload checks

- [ ] **Word count confirmed.** 2,399 body + 100 headings = 2,499 narrative words
      (`reports/word_count.txt`). If the instructor's counter includes figure
      captions, the figure rises to about 2,990 and must be discussed with them
      *before* submission.
- [ ] **PDF opens and renders** on a machine that is not this one (fonts, figures,
      references).
- [x] **Members named in the PDF.** The title block lists all five members:
      Zhang Yancheng, Dong Yuankun, Zhang Haoyu, Lau Pak Hei, Lui Shing Lam.
- [ ] **Student IDs entered in Moodle.** IDs are personal data and are *not* in
      this repository; each member enters their own at submission.
- [ ] **Contribution statement** confirmed by every member in
      `docs/management/responsibilities.md` (roster + lane ownership are filled
      in; each owner should confirm they can defend their lane).
- [ ] **AI-use acknowledgement** reviewed and kept (it is in the report).
- [ ] **Topic-confirmation status** checked: the uploaded form in
      `int4096/` is a blank template, not evidence of approval.
- [ ] **No personal data** beyond what the course requires (no student IDs in the
      public repository).
- [ ] **Notebook runs from a fresh Colab runtime** and prints asserted outputs
      (it does in local tests; Colab's package versions differ — allow time).
- [ ] **Dataset licence/terms** permit redistribution to Moodle.

## Presentation checks (20% of the mark)

- [ ] Assigned session confirmed (19 or 26 November).
- [ ] Deck rehearsed twice with a timer; content ≤ 18:00, hard limit 20:00.
- [ ] **All five members speak**, each with substantive technical content.
- [ ] Q&A appendix covers: random-walk baseline, raw vs adjusted prices, model
      fairness, scaling sensitivity, leakage, significance, educational relevance.
- [ ] Every slide number traces to a run ID in the speaker notes.
- [ ] Non-advisory disclaimer visible.

## After upload

- [ ] Screenshot or receipt of the Moodle confirmation retained by the group.
- [ ] Each member independently confirms the files are visible on Moodle.
- [ ] Final commit SHA recorded with the submission receipt.
- [ ] GitHub push completed separately (see `github_push.md`) — arc hive only.

---

## Outstanding items in this repository

| Item | Status | Where |
|---|---|---|
| Slide deck export (PPTX/PDF) | **NOT DONE** | `docs/presentation/storyboard.md` only |
| Contribution statement confirmation | roster filled; owners must confirm | `docs/management/responsibilities.md` |
| Official course specification archived | PENDING owner | `docs/course/README.md` |
| GitHub push | BLOCKED on auth | `docs/handoff/github_push.md` |
| Sealed test-set release | DELIBERATELY NOT DONE | `docs/research/decision_log.md` D7 |
| Six protocol decisions (D1, D2, D5–D8) | PENDING owner sign-off | `docs/research/decision_log.md` |
