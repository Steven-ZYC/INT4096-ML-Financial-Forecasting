"""Notebook tests.

The submission requires a Colab-compatible notebook. These tests check that the
committed notebook is current, carries no cached outputs, and runs top to bottom
in an empty folder, with none of the repository available to it.
"""

from __future__ import annotations

import importlib.util
import os
import subprocess
import sys
from pathlib import Path

import nbformat
import pytest

REPO_ROOT = Path(__file__).resolve().parents[1]
NOTEBOOK = REPO_ROOT / "deliverables" / "notebook" / "INT4096_Final_Colab.ipynb"

pytestmark = pytest.mark.skipif(not NOTEBOOK.exists(), reason="notebook not built yet")


def _code_cells():
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    return [c for c in notebook.cells if c.cell_type == "code"]


def test_notebook_is_valid_and_has_no_cached_outputs():
    nbformat.validate(nbformat.read(NOTEBOOK, as_version=4))
    for index, cell in enumerate(_code_cells()):
        assert not cell.get("outputs"), (
            f"code cell {index} carries stored outputs; the committed notebook must "
            "be executed fresh (the executed copy is a separate file)"
        )


def test_notebook_matches_the_repository():
    """Embedded code, data and published numbers must not go stale."""
    spec = importlib.util.spec_from_file_location(
        "build_notebook", REPO_ROOT / "scripts" / "build_notebook.py"
    )
    builder = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(builder)

    expected = [c.source for c in builder.build_notebook().cells]
    actual = [c.source for c in nbformat.read(NOTEBOOK, as_version=4).cells]
    assert actual == expected, "notebook is stale: run python scripts/build_notebook.py"


def _as_script(cells) -> str:
    """Plain-Python version of the notebook; ``%%writefile`` becomes a file write."""
    parts = []
    for cell in cells:
        source = cell.source
        if source.startswith("%%writefile "):
            header, _, body = source.partition("\n")
            path = header.split(maxsplit=1)[1]
            parts.append(
                "__import__('pathlib').Path({!r}).write_text({!r}, encoding='utf-8')".format(
                    path, body + "\n"
                )
            )
        else:
            parts.append(source)
    return "\n\n".join(parts) + "\n"


def test_notebook_executes_end_to_end_in_an_empty_folder(tmp_path):
    script = _as_script(_code_cells())
    # The neural experiment needs PyTorch and minutes of CPU; it is exercised by
    # the executed copy, not by the unit tests.
    assert "RUN_NEURAL = True" in script
    script = script.replace("RUN_NEURAL = True", "RUN_NEURAL = False")
    path = tmp_path / "notebook_as_script.py"
    path.write_text(script, encoding="utf-8")

    env = {k: v for k, v in os.environ.items() if k != "PYTHONPATH"}
    done = subprocess.run(
        [sys.executable, str(path)], cwd=tmp_path, env=env, capture_output=True, text=True
    )
    assert done.returncode == 0, done.stdout[-4000:] + done.stderr[-4000:]
    assert "MATCH: all 20 experiments agree" in done.stdout, done.stdout[-4000:]


def test_notebook_has_no_hardcoded_absolute_paths():
    text = NOTEBOOK.read_text(encoding="utf-8")
    for pattern in ["/home/steven", "/Users/", "C:\\\\Users"]:
        assert pattern not in text, f"notebook contains forbidden string {pattern!r}"


def test_notebook_never_releases_the_test_block():
    """The cells that run experiments must not unblind the sealed test set."""
    for cell in _code_cells():
        if cell.source.startswith("%%writefile "):
            continue  # library source defines the parameter; defaults keep it sealed
        assert "allow_test" not in cell.source
        assert "--allow-test" not in cell.source
