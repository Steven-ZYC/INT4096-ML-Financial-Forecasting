"""Generate `deliverables/notebook/INT4096_Final_Colab.ipynb`.

The notebook is self-contained: this builder copies the repository's own source,
configuration, tests and data snapshots into its cells. Run top to bottom in a
fresh kernel, it writes them into a new workspace folder, repeats the experiments
with the submitted settings, checks the results against the submitted ones and
draws the report's figures with the same code.

Rebuild after changing any embedded file (a test fails if the notebook is stale):

    python scripts/build_notebook.py
"""

from __future__ import annotations

import base64
import json
import textwrap
import zlib
from pathlib import Path

import nbformat as nbf

REPO_ROOT = Path(__file__).resolve().parents[1]
OUT = REPO_ROOT / "deliverables" / "notebook" / "INT4096_Final_Colab.ipynb"

# Embedded source files, grouped in reading order. Every .py under
# src/int4096 must appear exactly once (checked in build()).
CODE_GROUPS = [
    ("Configuration (the research protocol)", [
        "configs/research_protocol.yaml", "pyproject.toml",
        "src/int4096/__init__.py", "src/int4096/paths.py", "src/int4096/config.py",
    ]),
    ("Data: providers, snapshots, validation and chronological splits", [
        "src/int4096/data/__init__.py", "src/int4096/data/load.py",
        "src/int4096/data/validate.py", "src/int4096/data/split.py",
        "src/int4096/data/providers.py", "src/int4096/data/snapshot.py",
        "src/int4096/data/cards.py",
    ]),
    ("Features and preprocessing", [
        "src/int4096/features/__init__.py", "src/int4096/features/build.py",
        "src/int4096/features/pipeline.py",
    ]),
    ("Models", [
        "src/int4096/models/__init__.py", "src/int4096/models/base.py",
        "src/int4096/models/ridge.py", "src/int4096/models/svr.py",
        "src/int4096/models/random_forest.py",
        "src/int4096/models/hist_gradient_boosting.py", "src/int4096/models/mlp.py",
    ]),
    ("Experiment runner and tuning", [
        "src/int4096/experiments/__init__.py", "src/int4096/experiments/manifest.py",
        "src/int4096/experiments/tuning.py", "src/int4096/experiments/run.py",
        "src/int4096/experiments/registry_report.py",
    ]),
    ("Evaluation, analysis and figures", [
        "src/int4096/evaluation/__init__.py", "src/int4096/evaluation/baselines.py",
        "src/int4096/evaluation/metrics.py", "src/int4096/evaluation/analysis.py",
        "src/int4096/evaluation/figures.py",
    ]),
    ("Scripts: report tables and figures, neural experiment, mutation check", [
        "scripts/build_latex_assets.py", "scripts/supplementary_direction_test.py",
        "scripts/mutation_check.py",
    ]),
    ("Tests", [
        "tests/conftest.py", "tests/test_data_contract.py",
        "tests/test_metrics_and_manifest.py", "tests/test_model_lanes.py",
        "tests/test_temporal_integrity.py", "tests/test_figures.py",
    ]),
]

DATA_FILES = [
    "data/raw/aapl_daily.json", "data/raw/aapl_daily.manifest.json",
    "data/raw/btc_daily.json", "data/raw/btc_daily.manifest.json",
]


def md(text: str):
    return nbf.v4.new_markdown_cell(textwrap.dedent(text).strip("\n"))


def code(text: str):
    return nbf.v4.new_code_cell(textwrap.dedent(text).strip("\n"))


def file_cell(relative: str):
    content = (REPO_ROOT / relative).read_text(encoding="utf-8")
    return nbf.v4.new_code_cell(f"%%writefile {relative}\n{content.rstrip(chr(10))}")


def data_cell():
    blobs = {
        name: base64.b64encode(zlib.compress((REPO_ROOT / name).read_bytes(), 9)).decode()
        for name in DATA_FILES
    }
    lines = ["#@title Embedded data snapshots (compressed; verified by SHA-256 below)",
             "import base64, zlib", "from pathlib import Path", "", "SNAPSHOTS = {"]
    for name, blob in blobs.items():
        lines.append(f'    "{name}": (')
        lines += [f'        "{chunk}"' for chunk in textwrap.wrap(blob, 100)]
        lines.append("    ),")
    lines += [
        "}",
        "for name, blob in SNAPSHOTS.items():",
        "    path = Path(name)",
        "    path.parent.mkdir(parents=True, exist_ok=True)",
        "    path.write_bytes(zlib.decompress(base64.b64decode(blob)))",
        '    print(f"wrote {name}  ({path.stat().st_size:,} bytes)")',
    ]
    cell = nbf.v4.new_code_cell("\n".join(lines))
    cell.metadata["cellView"] = "form"
    return cell


def published_results() -> dict:
    """The submitted numbers, read from experiments/ at build time."""
    runs = {}
    for path in sorted((REPO_ROOT / "experiments" / "models").glob("*/*/metrics.json")):
        blob = json.loads(path.read_text(encoding="utf-8"))
        key = f"{blob['asset']}|{blob['model_id']}|{blob['preprocess_variant']}"
        metrics = blob["metrics"]
        runs[key] = [metrics["validation_mae"], metrics["validation_skill_mae"]]
    neural = {}
    root = REPO_ROOT / "experiments" / "supplementary" / "direction_test"
    for path in sorted(root.glob("*/results.json"), reverse=True):
        blob = json.loads(path.read_text(encoding="utf-8"))
        if blob.get("status") == "COMPLETE":
            for asset, result in blob["results"].items():
                for kind in ("mlp", "lstm"):
                    neural[f"{asset}|{kind}"] = result[kind]["accuracy_ensemble"]
            neural["device"] = f"{blob['device']}, torch {blob['torch']}"
            break
    return {"runs": runs, "neural": neural}


def submitted_environment() -> str:
    """Markdown table of the environments recorded with the submitted results."""
    def recorded(pattern: str, key: str) -> str:
        files = sorted((REPO_ROOT / "experiments").glob(pattern))
        values = {json.loads(f.read_text(encoding="utf-8"))[key] for f in files}
        return ", ".join(sorted(values))

    runs = "models/*/*/environment.json"
    neural = "supplementary/direction_test/*/results.json"
    pins = pinned_versions()
    libraries = ", ".join(
        f"{name} {pins[name]}" for name in ("numpy", "pandas", "scipy", "scikit-learn", "matplotlib")
    )
    return "\n".join([
        "| | 20 main experiments | Neural experiment (section 9) |",
        "|---|---|---|",
        f"| Python | {recorded(runs, 'python_version')} | {recorded(neural, 'python')} |",
        f"| Platform | {recorded(runs, 'platform')} | |",
        f"| Libraries | {libraries} (`requirements.txt`) | torch {recorded(neural, 'torch')} |",
        f"| Device | CPU | {recorded(neural, 'device')} |",
    ])


def pinned_versions() -> dict:
    versions = {}
    for line in (REPO_ROOT / "requirements.txt").read_text(encoding="utf-8").splitlines():
        if "==" in line and not line.startswith("#"):
            name, version = line.split("==")
            versions[name.strip()] = version.strip()
    return versions


def build_cells() -> list:
    cells = [
        md("""
        # Learning Machine Learning Through Financial Time-Series Forecasting

        **INT4096: Artificial Intelligence and Machine Learning in Education**
        The Education University of Hong Kong, Semester 1, 2026–27. Group project.

        A comparison of model families and preprocessing strategies for next-session
        close prediction on **AAPL** and **BTC**.

        ### How to run

        `Runtime → Run all`. The notebook needs no other files and no downloads of data:
        the project code and the data snapshots are inside it.

        | Section | What it produces |
        |---|---|
        | 1–2 | Environment, project code and data, written to a new workspace folder |
        | 3–5 | Data check, features, leakage tests |
        | 6–7 | All 20 experiments, checked against the submitted results |
        | 8–9 | Bootstrap intervals; experimental MLP and LSTM |
        | 10 | The report's tables and data figures |
        | 11–12 | Examples for learners; limitations |

        The five main models are scikit-learn models and run on the CPU. Only the neural
        experiment in section 9 can use a GPU. The final 20% of each series (the test
        block) is never scored. **This is not investment advice.**
        """),
        md("## 1. Setup\n\n### Environment behind the submitted results\n\n"
           + submitted_environment()
           + "\n\nThe next cells print the environment of **this** run."),
        code(f"""
        import importlib.util, os, subprocess, sys
        from datetime import datetime
        from importlib.metadata import version
        from pathlib import Path

        PINNED = {pinned_versions()!r}
        INSTALL_PINNED = False   # True: install the exact versions behind the submitted results

        MODULES = {{"numpy": "numpy", "pandas": "pandas", "scipy": "scipy", "scikit-learn": "sklearn",
                   "matplotlib": "matplotlib", "PyYAML": "yaml", "pytest": "pytest"}}
        wanted = [f"{{n}}=={{v}}" for n, v in PINNED.items() if n in MODULES] if INSTALL_PINNED else [
            name for name, module in MODULES.items() if importlib.util.find_spec(module) is None]
        if wanted:
            print("Installing:", wanted)
            subprocess.run([sys.executable, "-m", "pip", "install", "-q", *wanted], check=True)

        print(f"{{'python':14s}}{{sys.version.split()[0]}}")
        for name in MODULES:
            note = "" if PINNED.get(name) in (None, version(name)) else f"   (submitted results used {{PINNED[name]}})"
            print(f"{{name:14s}}{{version(name)}}{{note}}")
        """),
        code("""
        import platform

        print("operating system:", platform.system(), platform.release(), platform.machine())
        print("CPU threads     :", os.cpu_count())
        if importlib.util.find_spec("torch") is None:
            print("PyTorch         : not installed (section 9 will be skipped)")
        else:
            import torch
            print("PyTorch         :", torch.__version__, "| CUDA build:", torch.version.cuda)
            if torch.cuda.is_available():
                gpu = torch.cuda.get_device_properties(0)
                print(f"GPU             : {gpu.name}, {gpu.total_memory / 2**30:.1f} GiB")
            else:
                print("GPU             : none detected (section 9 runs on the CPU)")
        """),
        code("""
        # A new, empty workspace for this session. Nothing existing is overwritten.
        if "WORKSPACE" not in globals():
            WORKSPACE = Path(f"int4096_workspace_{datetime.now():%Y%m%d_%H%M%S}").resolve()
        for folder in ("configs", "data/raw", "scripts", "tests", "src/int4096/data",
                       "src/int4096/features", "src/int4096/models", "src/int4096/experiments",
                       "src/int4096/evaluation"):
            (WORKSPACE / folder).mkdir(parents=True, exist_ok=True)
        os.chdir(WORKSPACE)
        sys.path.insert(0, str(WORKSPACE / "src"))
        os.environ["PYTHONPATH"] = str(WORKSPACE / "src")
        os.environ["MPLBACKEND"] = "Agg"
        os.environ["PYTHONUTF8"] = "1"      # same text encoding on every system

        def run(*args):
            \"\"\"Run a project command in the workspace and show its output.\"\"\"
            done = subprocess.run([sys.executable, *args], capture_output=True,
                                  text=True, encoding="utf-8", errors="replace")
            print((done.stdout + done.stderr).replace(str(WORKSPACE), "."))
            if done.returncode != 0:
                raise RuntimeError(f"command failed with exit code {done.returncode}: {args}")

        print("workspace:", WORKSPACE.name)
        """),
        md("""
        ## 2. Project code and data

        Each `%%writefile` cell saves one file of the project, unchanged, into the
        workspace. The cells can be collapsed; sections 3 onwards use them.
        """),
        data_cell(),
    ]
    for title, files in CODE_GROUPS:
        cells.append(md(f"### 2 · {title}"))
        cells += [file_cell(name) for name in files]

    cells += [
        md("""
        ## 3. Load the snapshots and verify integrity

        Each file's SHA-256 is compared with the value recorded when it was downloaded.
        The two assets are **separate datasets**: AAPL follows exchange sessions, BTC
        trades every day. They are never aligned row by row.
        """),
        code("""
        import numpy as np
        import pandas as pd
        try:
            from IPython.display import Image, display
        except ImportError:                      # plain Python (used by the repository test)
            display, Image = print, lambda filename: filename

        import int4096
        from int4096.config import load_protocol
        from int4096.data.load import load_snapshot, read_manifest, resolve_snapshot_path
        from int4096.data.snapshot import sha256_file
        from int4096.data.validate import validate_frame

        protocol = load_protocol()
        print("protocol version:", protocol.version)
        frames, rows = {}, []
        for asset in ("AAPL", "BTC"):
            frames[asset] = load_snapshot(asset)
            manifest = read_manifest(asset)
            actual = sha256_file(resolve_snapshot_path(asset))
            assert actual == manifest["sha256"], f"{asset}: snapshot hash mismatch"
            frame = frames[asset]
            rows.append({"asset": asset, "provider": manifest["source"]["provider"], "rows": len(frame),
                         "first": frame.index[0].date(), "last": frame.index[-1].date(),
                         "quality": "PASS" if validate_frame(frame, asset=asset).passed else "ISSUES",
                         "sha256 prefix": actual[:12]})
        display(pd.DataFrame(rows))
        """),
        md("""
        ## 4. Features and the chronological split

        All ten features use only bars up to and including day `t`. The split is by
        time (60% train, 20% validation, 20% sealed test) with one row dropped at each
        boundary, because the label of day `t` is the close of day `t+1`.

        The second cell appends absurd *future* prices and checks that no earlier
        feature changes.
        """),
        code("""
        from int4096.features.build import build_features, feature_dictionary
        from int4096.experiments.run import prepare_dataset

        display(pd.DataFrame(feature_dictionary()))
        for asset in ("AAPL", "BTC"):
            prepared = prepare_dataset(asset, protocol)
            info = prepared["split"].describe(prepared["X"].index)
            print(asset)
            for part in ("train", "validation", "test"):
                print(f"   {part:11s}{info[part + '_period']}   rows: {info[part + '_rows']}")
        """),
        code("""
        frame = frames["AAPL"]
        settings = dict(lookback=protocol.lookback, min_periods=protocol.min_periods, mode=protocol.label_mode)
        X, _ = build_features(frame, **settings)

        future = frame.iloc[[-1]].copy()
        future.index = pd.DatetimeIndex([frame.index[-1] + pd.Timedelta(days=1)], name=frame.index.name)
        for column in ("open", "high", "low", "close", "volume", "adj_close"):
            future[column] = future[column].to_numpy() * 50.0
        X_extended, _ = build_features(pd.concat([frame, future]), **settings)

        difference = (X - X_extended.loc[X.index]).abs().max().max()
        print(f"largest change in any historical feature: {difference:.3e}")
        assert difference < 1e-12, "features depend on future data: this is a leak"
        print("PASS: features cannot see the future.")
        """),
        md("""
        ## 5. Tests

        Unit and leakage tests, followed by a mutation check: six leakage bugs are
        injected one at a time and the tests must catch every one.
        """),
        code('run("-m", "pytest", "tests", "-q", "--color=no", "-p", "no:cacheprovider")'),
        code('run("scripts/mutation_check.py")'),
        md("""
        ## 6. All 20 experiments

        Two assets × five models × two preprocessing variants (P0 unscaled, P2
        standardised), with the settings used for the submitted results: seed 42 and a
        budget of 10 random-search trials (at most 90 s) per experiment. Tuning uses
        time-ordered cross-validation inside the training block only.
        """),
        code("""
        import shutil
        from int4096.experiments.run import run_cell
        from int4096.paths import RUNS_ROOT

        TRIALS, SECONDS = 10, 90
        MODELS = ["linear_baseline", "ridge", "svr", "random_forest", "hist_gradient_boosting"]

        shutil.rmtree(RUNS_ROOT, ignore_errors=True)   # only this workspace's own runs
        for asset in ("AAPL", "BTC"):
            for model_id in MODELS:
                for variant in ("P0", "P2"):
                    result = run_cell(asset, model_id, variant, protocol, max_trials=TRIALS,
                                      max_seconds=SECONDS, human_owner="notebook")
                    assert result.status == "SUCCESS", result.error
                    print(f"{asset:5s}{model_id:24s}{variant}  MAE {result.metrics['validation_mae']:10.3f}"
                          f"  skill {result.metrics['validation_skill_mae'] * 100:+.2f}%"
                          f"  ({result.execution_seconds:.1f} s)")
        """),
        md("""
        ## 7. Do the new results match the submitted ones?

        The submitted values below were copied from the project's run records when this
        notebook was built. Small differences can appear with other library versions or
        hardware. In a check with older libraries (scikit-learn 1.6.1), only the four
        gradient-boosting experiments differed, by less than 0.1% in MAE. Setting
        `INSTALL_PINNED = True` in section 1 installs the original versions (restart
        the session afterwards if the environment had already loaded these libraries).
        """),
        code(f"""
        import json
        PUBLISHED = json.loads(r'''{json.dumps(published_results())}''')

        rows = []
        for path in sorted(RUNS_ROOT.glob("*/*/metrics.json")):
            blob = json.loads(path.read_text(encoding="utf-8"))
            key = f"{{blob['asset']}}|{{blob['model_id']}}|{{blob['preprocess_variant']}}"
            mae_new, skill_new = blob["metrics"]["validation_mae"], blob["metrics"]["validation_skill_mae"]
            mae_old, skill_old = PUBLISHED["runs"][key]
            same = f"{{mae_new:.3f}}" == f"{{mae_old:.3f}}" and f"{{skill_new * 100:.2f}}" == f"{{skill_old * 100:.2f}}"
            rows.append({{"experiment": key.replace("|", " "), "MAE submitted": mae_old, "MAE now": mae_new,
                         "skill % submitted": skill_old * 100, "skill % now": skill_new * 100,
                         "match": same}})
        check = pd.DataFrame(rows)
        display(check.round(4))
        assert len(check) == len(PUBLISHED["runs"])
        if check["match"].all():
            print(f"MATCH: all {{len(check)}} experiments agree with the submitted results at reported precision.")
        else:
            gap = (check["MAE now"] / check["MAE submitted"] - 1).abs().max()
            print(f"DIFFERENCE: {{(~check['match']).sum()}} of {{len(check)}} experiments differ "
                  f"(largest relative MAE change {{gap:.2e}}). Check the versions printed in section 1.")
        """),
        md("""
        ## 8. How certain are these results?

        Moving-block bootstrap (1,000 resamples of 10 consecutive days) of each
        experiment's skill. An interval that contains zero means the data cannot
        separate that model from "copy today's close". The intervals are indicative.
        """),
        code("""
        from int4096.evaluation import figures
        from int4096.evaluation.analysis import write_summary
        from int4096.paths import FIGURES

        analysis = json.loads(write_summary().read_text(encoding="utf-8"))
        print("intervals containing zero:", analysis["summary"]["ci_includes_zero"], "of", analysis["summary"]["runs"])
        for asset, values in analysis["return_autocorrelation"].items():
            print(f"{asset}: lag-1 autocorrelation of daily returns {values['lag1_autocorrelation']:+.4f}")
        forest = figures.plot_skill_intervals(analysis["skill_intervals"], block_length=10,
                                              n_resamples=1000, figure_root=FIGURES)
        display(Image(filename=str(forest)))
        """),
        md("""
        ## 9. Experimental neural networks (MLP and LSTM)

        An add-on outside the main comparison: predict whether the next close is higher
        than today's. Each network is trained for at most 300 epochs and stops after 20
        epochs without improvement on a hold-out taken from the end of the training
        block. A GPU is used if one is present; a CPU also works but is slower.
        Neural-network results can differ slightly between devices.
        """),
        code("""
        RUN_NEURAL = True
        if RUN_NEURAL and importlib.util.find_spec("torch") is not None:
            run("scripts/supplementary_direction_test.py")
            latest = sorted((WORKSPACE / "experiments/supplementary/direction_test").glob("*/results.json"))[-1]
            neural = json.loads(latest.read_text(encoding="utf-8"))
            submitted = PUBLISHED["neural"]
            print("submitted results used:", submitted.get("device"))
            display(pd.DataFrame([
                {"asset": a, "network": k, "accuracy submitted": submitted.get(f"{a}|{k}"),
                 "accuracy now": neural["results"][a][k]["accuracy_ensemble"],
                 "majority rule": neural["results"][a][k]["majority_accuracy"],
                 "95% interval vs majority": neural["results"][a][k]["diff_vs_majority_ci95"]}
                for a in ("AAPL", "BTC") for k in ("mlp", "lstm")]))
        else:
            print("Neural experiment skipped (RUN_NEURAL is False or PyTorch is not installed).")
        """),
        md("""
        ## 10. The report's tables and figures

        Generated from the experiments run above, with the same code that builds the
        report. Table and figure numbers follow the report. Figure 3 in the report is a
        hand-drawn pipeline diagram, so it has no data to regenerate.
        """),
        code("""
        run("scripts/build_latex_assets.py")
        """),
        code("""
        results = []
        for path in sorted(RUNS_ROOT.glob("*/*/metrics.json")):
            blob = json.loads(path.read_text(encoding="utf-8"))
            results.append({"asset": blob["asset"], "model": figures.model_label(blob["model_id"]),
                            "variant": blob["preprocess_variant"],
                            "MAE": blob["metrics"]["validation_mae"], "RMSE": blob["metrics"]["validation_rmse"],
                            "R2": blob["metrics"]["validation_r2"],
                            "skill %": blob["metrics"]["validation_skill_mae"] * 100})
        results = pd.DataFrame(results)

        print("Table 3. Preprocessing ablation: validation MAE, P0 (unscaled) against P2 (standardised)")
        ablation = results.pivot_table(index=["asset", "model"], columns="variant", values="MAE")
        ablation["change %"] = (ablation["P2"] / ablation["P0"] - 1) * 100
        display(ablation.round(4))

        print("Table 4. Validation performance, standardised inputs (P2). Dollar errors are not comparable across assets.")
        table4 = results[results["variant"] == "P2"].set_index(["asset", "model"])[["MAE", "RMSE", "R2", "skill %"]].sort_index()
        display(table4.round(4))
        """),
        code("""
        report_figures = WORKSPACE / "deliverables/report/latex/figures"
        for number, pattern in [(1, "fig01_*.png"), (2, "fig02_*.png"), (4, "fig06_*.png"),
                                (5, "fig04_*.png"), (6, "fig03_*.png"), (7, "fig07_*.png")]:
            path = sorted(report_figures.glob(pattern))[-1]
            print(f"Figure {number}")
            print(path.with_suffix(".caption.txt").read_text(encoding="utf-8").split("run_ids:")[0].strip())
            display(Image(filename=str(path)))
        """),
        md("""
        ## 11. Examples for learners

        ### A. Why R² can look impressive without any skill

        R² compares the error with the spread of prices around their average. Prices
        wander far from their average, so even "copy today's close" scores a high R².
        """),
        code("""
        from int4096.evaluation.baselines import naive_persistence
        from int4096.evaluation.metrics import evaluate_predictions

        for asset in ("AAPL", "BTC"):
            prepared = prepare_dataset(asset, protocol)
            X, y, split = prepared["X"], prepared["y"], prepared["split"]
            dates = X.index[split.validation_start:split.validation_end]
            today = prepared["frame"].loc[dates, protocol.label_field].to_numpy()
            truth = today + y.loc[dates].to_numpy()
            naive = naive_persistence(today)
            scores = evaluate_predictions(truth, naive, naive, reference=today)
            print(f"{asset}: copying today's close gives R2 = {scores['r2']:.4f}, skill = 0")
        """),
        md("""
        ### B. Spot the leakage

        One feature below is **deliberately leaky**. Find it before running the cell.
        """),
        code("""
        close = frames["AAPL"]["close"]
        leaky = pd.DataFrame({"ret_1": close.pct_change(1, fill_method=None),
                              "tomorrow_ret": close.pct_change(1, fill_method=None).shift(-1)})
        target = close.pct_change(1, fill_method=None).shift(-1)
        for column in leaky:
            print(f"{column:14s} correlation with the next-day return: {leaky[column].corr(target):+.3f}")
        print("'tomorrow_ret' uses shift(-1): it is the answer itself and is unknown at prediction time.")
        """),
        md("""
        ## 12. Limitations and responsible interpretation

        1. **Not investment advice.** Forecast error says nothing about profit, risk or
           trading costs.
        2. **One-day horizon.** Copying today's close is a strong forecast here.
        3. **Two assets, one period.** The conclusions may not hold elsewhere.
        4. **BTC is one exchange's USDT price**, not a global USD index.
        5. **Raw close prices** are used; dividends are ignored.
        6. **No learner study** was run; the lesson is a designed resource.
        7. **The test block is sealed.** All numbers here are validation numbers.

        The last cell packs the tables, figures and run records into one zip file.
        """),
        code("""
        bundle = WORKSPACE / "bundle"
        for folder in ("experiments", "deliverables"):
            shutil.copytree(WORKSPACE / folder, bundle / folder, dirs_exist_ok=True)
        archive = shutil.make_archive(str(WORKSPACE / "int4096_outputs"), "zip", bundle)
        shutil.rmtree(bundle)
        print("outputs:", Path(archive).relative_to(WORKSPACE.parent))
        print(int4096.DISCLAIMER)
        """),
    ]
    return cells


def check_coverage() -> None:
    listed = [name for _, files in CODE_GROUPS for name in files]
    actual = {p.relative_to(REPO_ROOT).as_posix() for p in (REPO_ROOT / "src" / "int4096").rglob("*.py")}
    missing = sorted(actual - set(listed))
    if missing or len(listed) != len(set(listed)):
        raise SystemExit(f"notebook file list is incomplete or duplicated; missing: {missing}")


def build_notebook():
    check_coverage()
    notebook = nbf.v4.new_notebook()
    notebook["cells"] = build_cells()
    for index, cell in enumerate(notebook["cells"]):
        cell["id"] = f"cell-{index:03d}"       # fixed ids keep rebuilds identical
    notebook["metadata"] = {
        "kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
        "language_info": {"name": "python", "version": "3.10"},
        "colab": {"provenance": [], "toc_visible": True},
    }
    nbf.validate(notebook)
    return notebook


def build() -> Path:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(build_notebook(), indent=1) + "\n", encoding="utf-8")
    return OUT


if __name__ == "__main__":
    path = build()
    notebook = nbf.read(path, as_version=4)
    print(f"wrote {path.relative_to(REPO_ROOT)}")
    print(f"cells: {len(notebook.cells)} ({sum(c.cell_type == 'code' for c in notebook.cells)} code), "
          f"{path.stat().st_size / 1024:.0f} KB")
