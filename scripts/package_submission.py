"""Build the two files uploaded to Moodle, with the required names.

    python scripts/package_submission.py

writes, into ``submission/``:

    INT4096 <Group ID> - Group Project Report.pdf
    INT4096 <Group ID> - Group Project Deliverables.zip

The group ID defaults to this group's, 06. Run the script again after changing
the report, slides, notebook, data or lesson files.
"""

from __future__ import annotations

import argparse
import shutil
import sys
import zipfile
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = REPO_ROOT / "submission"
REPORT = "deliverables/report/INT4096_Final_Report.pdf"
GROUP_ID = "06"

# (folder in the zip, repository file, one-line description)
CONTENTS = [
    ("Presentation", "deliverables/presentation/INT4096_Presentation.pdf",
     "Presentation slides"),
    ("Notebook", "deliverables/notebook/INT4096_Final_Colab.ipynb",
     "Self-contained notebook: code and data inside"),
    ("Notebook", "deliverables/notebook/INT4096_Final_Colab_executed.ipynb",
     "The same notebook with saved outputs from a full run"),
    ("Dataset", "data/raw/aapl_daily.json", "Original Apple (AAPL) daily data"),
    ("Dataset", "data/raw/aapl_daily.manifest.json", "AAPL source record and fingerprint"),
    ("Dataset", "data/raw/btc_daily.json", "Original Bitcoin (BTC/USDT) daily data"),
    ("Dataset", "data/raw/btc_daily.manifest.json", "BTC source record and fingerprint"),
    ("Lesson", "deliverables/lesson/lesson_plan.md", "60-minute lesson plan"),
    ("Lesson", "deliverables/lesson/formative_tasks.md", "Five formative tasks with answers"),
    ("Lesson", "deliverables/lesson/teacher_notes.md", "Teacher notes"),
]


def zip_readme() -> str:
    rows = "\n".join(
        f"| `{folder}/{Path(source).name}` | {description} |"
        for folder, source, description in CONTENTS
    )
    return f"""# INT4096 Group Project Deliverables

Learning Machine Learning Through Financial Time-Series Forecasting.
The report is uploaded separately as a PDF.

| File | What it is |
|---|---|
{rows}

## Run the notebook

Open `Notebook/INT4096_Final_Colab.ipynb` in Jupyter or VS Code and choose
**Run All**. It needs no other files. The first cell installs missing Python
packages. The neural-network section also needs PyTorch and is skipped without it.
The saved outputs can be read in the executed copy without running anything.

Repository: https://github.com/Steven-ZYC/INT4096-ML-Financial-Forecasting

Educational and historical only. Not investment advice.
"""


def add(archive: zipfile.ZipFile, name: str, data: bytes) -> None:
    # A fixed timestamp keeps rebuilt archives identical.
    info = zipfile.ZipInfo(name, date_time=(2026, 11, 28, 0, 0, 0))
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    archive.writestr(info, data)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--group-id", default=GROUP_ID, help="group ID used in the file names")
    group = parser.parse_args(argv).group_id.strip()
    if not group or any(ch in group for ch in '/\\:*?"<>|'):
        raise SystemExit("the group ID must be non-empty and valid in a file name")

    missing = [s for s in [REPORT, *(c[1] for c in CONTENTS)] if not (REPO_ROOT / s).is_file()]
    if missing:
        raise SystemExit(f"missing files: {missing}")

    OUTPUT.mkdir(exist_ok=True)
    for old in OUTPUT.glob("INT4096 * - Group Project *"):
        old.unlink()   # only this script's own earlier outputs

    report = OUTPUT / f"INT4096 {group} - Group Project Report.pdf"
    shutil.copyfile(REPO_ROOT / REPORT, report)

    bundle = OUTPUT / f"INT4096 {group} - Group Project Deliverables.zip"
    with zipfile.ZipFile(bundle, "w") as archive:
        add(archive, "README.md", zip_readme().encode("utf-8"))
        for folder, source, _ in CONTENTS:
            add(archive, f"{folder}/{Path(source).name}", (REPO_ROOT / source).read_bytes())

    for path in (report, bundle):
        print(f"{path.relative_to(REPO_ROOT)}  ({path.stat().st_size / 1024:.0f} KB)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
