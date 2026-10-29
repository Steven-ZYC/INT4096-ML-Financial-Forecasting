"""Notebook execution test.

The submission requires a Colab-compatible notebook. A notebook that only shows
cached outputs is not evidence that it runs, so this test extracts every code
cell, executes them in order in a fresh namespace, and fails on the first
exception.

`display()` is shimmed because it exists in IPython/Colab but not in a plain
interpreter. Matplotlib runs on the Agg backend so no display is needed.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

import nbformat
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "notebooks" / "INT4096_Final_Colab.ipynb"




@pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook not built yet")
def test_notebook_is_valid_and_well_formed():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    nbformat.validate(notebook)

    assert len(notebook.cells) > 10
    code_cells = [c for c in notebook.cells if c.cell_type == "code"]
    assert len(code_cells) >= 10

    # No cached outputs may be committed: the notebook must rebuild them.
    for index, cell in enumerate(code_cells):
        assert not cell.get("outputs"), (
            f"code cell {index} carries stored outputs; the notebook must be "
            "executed fresh rather than committed with cached results"
        )


@pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook not built yet")
def test_notebook_executes_end_to_end(monkeypatch):
    """Execute every code cell in order in this process."""
    import matplotlib

    matplotlib.use("Agg")

    notebook = nbformat.read(NOTEBOOK, as_version=4)
    namespace: dict[str, object] = {"__name__": "__notebook__"}

    # The notebook honours this flag: with every dependency present it already
    # skips installation, but the flag makes the test independent of the machine.
    monkeypatch.setenv("INT4096_SKIP_INSTALL", "1")

    def display(*args, **kwargs):  # noqa: ARG001 - Colab/IPython builtin
        return None

    namespace["display"] = display

    cwd = Path.cwd()
    monkeypatch.chdir(REPO_ROOT)
    sys.path.insert(0, str(REPO_ROOT / "src"))
    try:
        for index, cell in enumerate(notebook.cells):
            if cell.cell_type != "code":
                continue
            source = cell.source
            try:
                exec(compile(source, f"<notebook cell {index}>", "exec"), namespace)
            except Exception as exc:  # noqa: BLE001 - report which cell failed
                pytest.fail(f"notebook code cell {index} raised {type(exc).__name__}: {exc}")
    finally:
        monkeypatch.chdir(cwd)


@pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook not built yet")
def test_notebook_has_no_hardcoded_absolute_paths():
    text = NOTEBOOK.read_text(encoding="utf-8")
    forbidden = ["/home/steven", "/Users/", "C:\\\\Users", "api_key", "password"]
    for pattern in forbidden:
        assert pattern not in text, f"notebook contains forbidden string {pattern!r}"


@pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook not built yet")
def test_notebook_never_releases_the_test_block():
    """A submission notebook must not unblind the sealed test set."""
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    for cell in notebook.cells:
        source = cell.source
        assert "allow_test=True" not in source, (
            "the notebook must not release the sealed test block"
        )
        assert "--allow-test" not in source
