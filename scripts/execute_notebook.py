"""Run the submission notebook in a fresh kernel and save a copy with its outputs.

The copy, ``INT4096_Final_Colab_executed.ipynb``, is the run log submitted next
to the notebook. Needs nbclient and ipykernel; PyTorch for the neural section.
Run it on the machine whose outputs you want to submit:

    python scripts/execute_notebook.py
"""

from __future__ import annotations

import sys
import tempfile
import time
from pathlib import Path

import nbformat
from jupyter_client.kernelspec import KernelSpecManager
from nbclient import NotebookClient

REPO_ROOT = Path(__file__).resolve().parents[1]
SOURCE = REPO_ROOT / "deliverables" / "notebook" / "INT4096_Final_Colab.ipynb"
OUTPUT = SOURCE.with_name(SOURCE.stem + "_executed.ipynb")


def main() -> int:
    notebook = nbformat.read(SOURCE, as_version=4)
    if "python3" not in KernelSpecManager().find_kernel_specs():
        raise SystemExit("No python3 kernel: pip install ipykernel")
    started = time.perf_counter()
    with tempfile.TemporaryDirectory() as scratch:
        # The notebook must work from an empty folder, so it runs in one.
        NotebookClient(
            notebook, timeout=3600, kernel_name="python3",
            resources={"metadata": {"path": scratch}},
        ).execute()
        text = nbformat.writes(notebook)
        # Do not publish machine-specific temporary paths in the saved outputs.
        text = text.replace(str(Path(scratch).resolve()), ".").replace(scratch, ".")
    OUTPUT.write_text(text, encoding="utf-8")
    print(f"wrote {OUTPUT.relative_to(REPO_ROOT)} in {time.perf_counter() - started:.0f} s")
    return 0


if __name__ == "__main__":
    sys.exit(main())
