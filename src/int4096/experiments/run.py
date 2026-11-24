"""End-to-end experiment runner.

One call = one cell of the matrix ``(asset x model x preprocessing variant)``.

Order of operations (fixed, and the reason the comparison is fair):

1. Load the immutable snapshot for the asset, verify its SHA256.
2. Build causal features and the next-close label.
3. Split chronologically into train / validation / test.
4. Tune hyperparameters using **expanding-window CV inside train only**.
5. Fit on train, score on validation (the only reported tuning signal).
6. If and only if the test set has been released, score once on test.
7. Write ``manifest.json``, ``metrics.json``, ``predictions.csv`` and ``config.json``.

The test block is never passed to ``fit`` or to the tuner. ``allow_test=False``
is the default and requires an explicit, logged human decision to change.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import hashlib
import json
import time
import traceback
from pathlib import Path
from typing import Any

import numpy as np

from ..config import REPO_ROOT, Protocol, load_protocol
from ..data.load import load_snapshot, read_manifest
from ..data.split import Split, chronological_split, expanding_window_folds
from ..evaluation.baselines import naive_persistence
from ..evaluation.metrics import evaluate_predictions
from ..features.build import build_features
from ..features.pipeline import select_feature_columns, variant_is_applicable
from ..models.base import build_estimator
from .manifest import (
    RunManifest,
    RunStatus,
    environment_manifest,
    make_run_id,
)
from .tuning import select_hyperparameters

from ..paths import RUNS_ROOT

ARTIFACT_ROOT = RUNS_ROOT  # experiments/models/<model_id>/<run_id>/


def _display_path(path: Path) -> str:
    """Repo-relative when possible, absolute otherwise.

    Manifests must never crash because an output root lives outside the
    repository (audit LEAK-009); they simply record an absolute path and the run
    is flagged with a comparability warning.
    """
    try:
        return str(Path(path).relative_to(REPO_ROOT))
    except ValueError:
        return str(Path(path).resolve())


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prepare_dataset(
    asset: str,
    protocol: Protocol,
    snapshot_path: str | Path | None = None,
) -> dict[str, Any]:
    """Load → validate → features → label → split. Pure and deterministic."""
    frame = load_snapshot(asset, path=snapshot_path)
    cfg = protocol.asset(asset)

    X, y = build_features(
        frame,
        feature_columns=None,
        label_field=protocol.label_field,
        horizon=1,
        lookback=protocol.lookback,
        min_periods=protocol.min_periods,
        mode=protocol.label_mode,
    )

    split = chronological_split(
        len(X),
        train_fraction=protocol.train_fraction,
        validation_fraction=protocol.validation_fraction,
        test_fraction=protocol.test_fraction,
        horizon_gap=protocol.purge_gap,
    )

    return {
        "frame": frame,
        "X": X,
        "y": y,
        "split": split,
        "asset_config": cfg,
    }


def run_cell(
    asset: str,
    model_id: str,
    variant_name: str,
    protocol: Protocol,
    *,
    seed: int | None = None,
    allow_test: bool = False,
    max_trials: int | None = None,
    max_seconds: float | None = None,
    human_owner: str = "",
    snapshot_path: str | Path | None = None,
    output_root: str | Path | None = None,
    notes: str = "",
) -> RunManifest:
    """Execute one experiment cell and write its artifacts."""
    tuning_cfg = protocol.tuning
    seed = int(tuning_cfg.get("seed", 42) if seed is None else seed)
    max_trials = int(tuning_cfg.get("max_trials", 24) if max_trials is None else max_trials)
    max_seconds = float(tuning_cfg.get("max_seconds", 300) if max_seconds is None else max_seconds)

    variant = protocol.variant(variant_name)
    model_cfg = protocol.model(model_id)
    out_root = Path(output_root) if output_root is not None else ARTIFACT_ROOT

    snapshot_file = Path(snapshot_path) if snapshot_path else None
    hash_warning: str | None = None
    if snapshot_file is None:
        from ..data.load import resolve_snapshot_path

        manifest_sidecar = read_manifest(asset)
        snapshot_sha = manifest_sidecar["sha256"]
        source_name = manifest_sidecar["source"]["provider"]
        source_coverage = f"{manifest_sidecar['first_date']}..{manifest_sidecar['last_date']}"

        # LEAK-003: a recorded hash that is never checked proves nothing. Verify
        # the bytes on disk still match before any number is produced from them.
        actual_sha = _hash_file(resolve_snapshot_path(asset))
        if actual_sha != snapshot_sha:
            raise RuntimeError(
                f"Snapshot integrity failure for {asset}: manifest records "
                f"{snapshot_sha[:12]}... but the file hashes to {actual_sha[:12]}... . "
                "Refusing to run on unverified data. Re-create the snapshot with a "
                "recorded decision, or restore the original bytes."
            )
    else:
        snapshot_sha = _hash_file(snapshot_file)
        source_name = "fixture"
        source_coverage = "fixture"
        hash_warning = (
            "explicit snapshot path supplied: metrics are not comparable to runs on "
            "the recorded project snapshot"
        )

    run_id = make_run_id(asset, model_id, variant_name, seed)
    run_dir = out_root / model_id / run_id
    run_dir.mkdir(parents=True, exist_ok=True)

    manifest = RunManifest(
        run_id=run_id,
        status=RunStatus.NOT_RUN.value,
        protocol_version=protocol.version,
        asset=asset,
        prediction_target=protocol.target,
        source_snapshot_sha256=snapshot_sha,
        model_id=model_id,
        preprocess_variant=variant_name,
        seed=seed,
        source_name=source_name,
        source_coverage=source_coverage,
        human_owner=human_owner,
        config_path=f"configs/research_protocol.yaml#{model_id}/{variant_name}",
        config_hash=hashlib.sha256(
            json.dumps(
                {"model": model_cfg, "variant": variant, "seed": seed}, sort_keys=True
            ).encode("utf-8")
        ).hexdigest(),
        cv_policy=(
            f"expanding_window n_splits={protocol.cv['n_splits']} gap={protocol.cv['gap']}"
        ),
    )

    started = time.perf_counter()
    try:
        prepared = prepare_dataset(asset, protocol, snapshot_path)
        X, y, split = prepared["X"], prepared["y"], prepared["split"]

        split_desc = split.describe(X.index)
        manifest.train_period = split_desc["train_period"]
        manifest.validation_period = split_desc["validation_period"]
        manifest.test_period = ""
        manifest.notes = notes
        if hash_warning:
            manifest.warnings.append(hash_warning)

        columns = select_feature_columns(variant, list(X.columns))

        # A variant that cannot change anything must be reported as NOT_RUN, not
        # published as a duplicate cell (decision D13 / audit LEAK-005).
        applicable, not_applicable_reason = variant_is_applicable(variant, X[columns])
        if not applicable:
            manifest.status = RunStatus.NOT_RUN.value
            manifest.warnings.append(f"variant not applicable: {not_applicable_reason}")
            manifest.execution_seconds = round(time.perf_counter() - started, 3)
            manifest_path = run_dir / "manifest.json"
            manifest.write(manifest_path)
            (run_dir / "not_run.json").write_text(
                json.dumps(
                    {
                        "run_id": run_id,
                        "status": manifest.status,
                        "reason": not_applicable_reason,
                    },
                    indent=2,
                )
                + "\n",
                encoding="utf-8",
            )
            manifest.artifacts = [_display_path(run_dir / "not_run.json")]
            manifest.write(manifest_path)
            _append_registry(manifest, manifest_path, out_root)
            return manifest

        train_idx = np.arange(split.train_start, split.train_end)
        val_idx = np.arange(split.validation_start, split.validation_end)

        X_train, y_train = X.iloc[train_idx], y.iloc[train_idx]
        X_val, y_val = X.iloc[val_idx], y.iloc[val_idx]

        folds = expanding_window_folds(
            len(X_train),
            n_splits=int(protocol.cv["n_splits"]),
            gap=int(protocol.cv["gap"]),
            min_train_fraction=float(protocol.cv["min_train_fraction"]),
        )

        def score_config(config: dict[str, Any]) -> float:
            """CV score using VALIDATION-but-train-only folds (inside X_train)."""
            scores = []
            for fold_train, fold_val in folds:
                est = build_estimator(
                    model_id,
                    config,
                    seed,
                    variant,
                    feature_columns=columns if variant.get("features") == "reduced" else None,
                )
                est.fit(X_train.iloc[fold_train], y_train.iloc[fold_train])
                preds = est.predict(X_train.iloc[fold_val])
                scores.append(float(np.mean(np.abs(y_train.iloc[fold_val].to_numpy() - preds))))
            return float(np.mean(scores))

        search = select_hyperparameters(
            score_config,
            dict(model_cfg.get("search_space") or {}),
            max_trials=max_trials,
            max_seconds=max_seconds,
            seed=seed,
        )
        manifest.hyperparameters = search.best_hyperparameters

        final = build_estimator(
            model_id,
            search.best_hyperparameters,
            seed,
            variant,
            feature_columns=columns if variant.get("features") == "reduced" else None,
        )
        final.fit(X_train, y_train)

        val_pred = np.asarray(final.predict(X_val), dtype="float64")
        # The decision-time price (Close_t) is both the naive forecast, the
        # reference for the direction diagnostic, and (in delta mode) the base
        # that reconstructs a price forecast. One array, one meaning.
        val_reference = prepared["frame"].loc[
            X_val.index, protocol.label_field
        ].to_numpy(dtype="float64")
        val_naive = naive_persistence(val_reference)
        naive_by_date = dict(zip(X_val.index, val_naive, strict=True))

        # Delta mode: the model predicts the CHANGE; add it to the known price.
        if protocol.label_mode == "delta":
            val_pred = val_reference + val_pred
            val_target = val_reference + y_val.to_numpy(dtype="float64")
        else:
            val_target = y_val.to_numpy(dtype="float64")

        val_metrics = evaluate_predictions(
            val_target,
            val_pred,
            val_naive,
            reference=val_reference,
        )
        manifest.metrics = {f"validation_{k}": v for k, v in val_metrics.items()}
        manifest.baseline_metrics = {
            "validation_mae": val_metrics["baseline_mae"],
            "validation_rmse": val_metrics["baseline_rmse"],
            "validation_r2": val_metrics["baseline_r2"],
        }

        predictions = [
            {
                "date": str(ts.date()),
                "split": "validation",
                "y_true": float(true),
                "y_pred": float(pred),
                "y_naive": float(naive_by_date[ts]),
            }
            for ts, true, pred in zip(
                X_val.index, val_target, val_pred, strict=True
            )
        ]

        if allow_test:
            # Single, human-approved release. Recorded so the report can state
            # exactly when the seal was broken.
            test_idx = np.arange(split.test_start, split.test_end)
            X_test, y_test = X.iloc[test_idx], y.iloc[test_idx]
            test_pred = np.asarray(final.predict(X_test), dtype="float64")
            test_ref = prepared["frame"].loc[X_test.index, protocol.label_field].to_numpy(dtype="float64")
            test_naive = naive_persistence(test_ref)
            if protocol.label_mode == "delta":
                test_pred = test_ref + test_pred
                test_target = test_ref + y_test.to_numpy(dtype="float64")
            else:
                test_target = y_test.to_numpy(dtype="float64")
            test_metrics = evaluate_predictions(
                test_target, test_pred, test_naive, reference=test_ref
            )
            manifest.metrics.update({f"test_{k}": v for k, v in test_metrics.items()})
            manifest.baseline_metrics.update(
                {
                    "test_mae": test_metrics["baseline_mae"],
                    "test_rmse": test_metrics["baseline_rmse"],
                    "test_r2": test_metrics["baseline_r2"],
                }
            )
            manifest.test_period = split_desc["test_period"]
            naive_by_date.update(dict(zip(X_test.index, test_naive, strict=True)))
            predictions.extend(
                {
                    "date": str(ts.date()),
                    "split": "test",
                    "y_true": float(true),
                    "y_pred": float(pred),
                    "y_naive": float(naive_by_date[ts]),
                }
                for ts, true, pred in zip(
                    X_test.index, test_target, test_pred, strict=True
                )
            )
        else:
            manifest.warnings.append(
                "test set sealed: no test metrics produced in this run"
            )

        # These are inner-CV scores inside the TRAIN block, not validation-block
        # scores. Naming them "validation_mae" would misrepresent the tuning
        # protocol (audit LEAK-004), so the field is renamed explicitly.
        manifest.fold_metrics = [
            {**t.to_dict(), "stage": "inner_cv_train_block"} for t in search.trials
        ]

        metrics_path = run_dir / "metrics.json"
        predictions_path = run_dir / "predictions.csv"
        config_path = run_dir / "config.json"
        env_path = run_dir / "environment.json"

        metrics_blob = {
            "run_id": run_id,
            "asset": asset,
            "model_id": model_id,
            "preprocess_variant": variant_name,
            "seed": seed,
            "protocol_version": protocol.version,
            "metrics": manifest.metrics,
            "baseline_metrics": manifest.baseline_metrics,
            "search": search.to_dict(),
            "split": split_desc,
        }
        metrics_path.write_text(json.dumps(metrics_blob, indent=2) + "\n", encoding="utf-8")

        with predictions_path.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=["date", "split", "y_true", "y_pred", "y_naive"])
            writer.writeheader()
            writer.writerows(predictions)

        config_path.write_text(
            json.dumps(
                {
                    "model_id": model_id,
                    "model_config": model_cfg,
                    "variant": variant_name,
                    "variant_config": variant,
                    "features_used": columns,
                    "seed": seed,
                    "max_trials": max_trials,
                    "max_seconds": max_seconds,
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        env_path.write_text(
            json.dumps(environment_manifest(), indent=2) + "\n", encoding="utf-8"
        )

        manifest.artifacts = [
            _display_path(metrics_path),
            _display_path(predictions_path),
            _display_path(config_path),
            _display_path(env_path),
        ]
        manifest.execution_seconds = round(time.perf_counter() - started, 3)

        # Only the core regression metrics must be finite for a run to count as
        # complete. Some diagnostics are legitimately null: e.g. the naive
        # baseline makes no directional call, so its direction accuracy is
        # undefined. Reporting those as NaN is correct; treating them as a
        # failure would push us to invent a number.
        core_keys = (
            "validation_mae",
            "validation_rmse",
            "validation_r2",
            "validation_skill_mae",
        )
        missing_core = [
            key for key in core_keys if not np.isfinite(manifest.metrics.get(key, float("nan")))
        ]
        null_diagnostics = sorted(
            key
            for key, value in manifest.metrics.items()
            if isinstance(value, float) and not np.isfinite(value) and key not in core_keys
        )
        if null_diagnostics:
            manifest.warnings.append(
                "undefined (NaN) diagnostics retained as null: " + ", ".join(null_diagnostics)
            )
        if missing_core:
            manifest.warnings.append(
                "core metrics non-finite: " + ", ".join(missing_core)
            )
            manifest.status = RunStatus.INCOMPLETE.value
        else:
            manifest.status = RunStatus.SUCCESS.value

    except Exception as exc:  # noqa: BLE001 - a failed run must be recorded as failed
        manifest.status = RunStatus.FAILED.value
        manifest.error = f"{type(exc).__name__}: {exc}\n{traceback.format_exc()}"
        manifest.execution_seconds = round(time.perf_counter() - started, 3)
        (run_dir / "error.log").write_text(manifest.error, encoding="utf-8")
        manifest.artifacts = [_display_path(run_dir / "error.log")]

    manifest_path = run_dir / "manifest.json"
    manifest.write(manifest_path)
    _append_registry(manifest, manifest_path, out_root)
    return manifest


def _registry_path(output_root: Path) -> Path:
    return output_root / "registry.jsonl"


def _append_registry(manifest: RunManifest, manifest_path: Path, output_root: Path) -> None:
    """Append a compact line to the machine-readable run registry.

    Append-only: failed runs are never removed, so coverage claims in the report
    can be checked against the registry.
    """
    registry = _registry_path(output_root)
    registry.parent.mkdir(parents=True, exist_ok=True)
    row = {
        "run_id": manifest.run_id,
        "status": manifest.status,
        "asset": manifest.asset,
        "model_id": manifest.model_id,
        "preprocess_variant": manifest.preprocess_variant,
        "seed": manifest.seed,
        "protocol_version": manifest.protocol_version,
        "manifest": _display_path(manifest_path),
        "validation_mae": manifest.metrics.get("validation_mae"),
        "validation_skill_mae": manifest.metrics.get("validation_skill_mae"),
        "test_mae": manifest.metrics.get("test_mae"),
        "review_state": manifest.review_state,
        "recorded_utc": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    with registry.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(row) + "\n")


def run_model_across_variants(
    asset: str,
    model_id: str,
    variants: list[str],
    protocol: Protocol,
    **kwargs: Any,
) -> list[RunManifest]:
    """Convenience wrapper: one model lane across preprocessing variants."""
    return [
        run_cell(asset, model_id, variant, protocol, **kwargs) for variant in variants
    ]


def _main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run one INT4096 experiment cell.")
    parser.add_argument("--config", default=None, help="protocol YAML path")
    parser.add_argument("--asset", required=True, choices=["AAPL", "BTC"])
    parser.add_argument("--model", required=True)
    parser.add_argument("--variant", default="P0")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--max-trials", type=int, default=None)
    parser.add_argument("--max-seconds", type=float, default=None)
    parser.add_argument("--human-owner", default="")
    parser.add_argument(
        "--allow-test",
        action="store_true",
        help="Release the sealed test block for this run (requires a recorded decision).",
    )
    args = parser.parse_args(argv)

    protocol = load_protocol(args.config)
    manifest = run_cell(
        args.asset,
        args.model,
        args.variant,
        protocol,
        seed=args.seed,
        allow_test=args.allow_test,
        max_trials=args.max_trials,
        max_seconds=args.max_seconds,
        human_owner=args.human_owner,
    )
    print(json.dumps({k: v for k, v in manifest.to_dict().items() if k != "fold_metrics"}, indent=2))
    return 0 if manifest.status == RunStatus.SUCCESS.value else 1


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(_main())
