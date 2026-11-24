"""Every repository location the code reads or writes, in one place.

Layout (see README.md, "Repository layout"):

    data/raw/                       immutable snapshots + SHA-256 manifests
    data/cards/                     generated dataset cards
    data/splits/                    generated split boundaries and tuning folds
    experiments/models/<model_id>/<run_id>/   one folder per model, one per run
    experiments/models/registry.jsonl         append-only registry of every run
    experiments/analysis/           cross-run analysis (bootstrap, autocorrelation)
    experiments/figures/            figures regenerated from the runs
    experiments/supplementary/      add-on experiments outside the main matrix
    deliverables/presentation/      final deck, slide sources, script, planning
    deliverables/report/            final report and its LaTeX sources
    deliverables/notebook/          Colab notebooks
    deliverables/lesson/            lesson plan, tasks, teacher notes
"""

from __future__ import annotations

from pathlib import Path
from typing import Iterator

REPO_ROOT = Path(__file__).resolve().parents[2]

DATA_RAW = REPO_ROOT / "data" / "raw"
DATA_CARDS = REPO_ROOT / "data" / "cards"
DATA_SPLITS = REPO_ROOT / "data" / "splits"

EXPERIMENTS = REPO_ROOT / "experiments"
RUNS_ROOT = EXPERIMENTS / "models"
ANALYSIS = EXPERIMENTS / "analysis"
FIGURES = EXPERIMENTS / "figures"
SUPPLEMENTARY = EXPERIMENTS / "supplementary"

DELIVERABLES = REPO_ROOT / "deliverables"
PRESENTATION = DELIVERABLES / "presentation"
SLIDES = PRESENTATION / "slides"
REPORT = DELIVERABLES / "report"
REPORT_LATEX = REPORT / "latex"
NOTEBOOKS = DELIVERABLES / "notebook"

DOCS_RESEARCH = REPO_ROOT / "docs" / "research"


def run_dirs(root: Path | None = None) -> Iterator[Path]:
    """Every run folder, ``<root>/<model_id>/<run_id>/``, in sorted order."""
    base = Path(root) if root is not None else RUNS_ROOT
    for model_dir in sorted(p for p in base.iterdir() if p.is_dir()):
        yield from sorted(p for p in model_dir.iterdir() if p.is_dir())


def run_files(name: str, pattern: str = "*", root: Path | None = None) -> list[Path]:
    """Files called ``name`` inside run folders whose id matches ``pattern``."""
    base = Path(root) if root is not None else RUNS_ROOT
    return sorted(base.glob(f"*/{pattern}/{name}"))
