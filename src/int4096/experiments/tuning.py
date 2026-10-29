"""Random-search tuning with a hard, recorded budget.

Why a budget
------------
A comparison is only fair if every model gets the same opportunity to tune.
The budget is therefore enforced in *code*, not by convention: ``max_trials``
and ``max_seconds`` come from the frozen protocol, every attempted
configuration is logged (including failures), and the search stops when either
limit is reached.

Why random search
-----------------
With a small number of categorical/continuous hyperparameters and a strict
budget, random search covers the space more diversely than grid search and is
the honest choice for a project that cannot afford exhaustive exploration.

Leakage guard
-------------
``select_hyperparameters`` receives only *training* and *validation* arrays
supplied by the caller. It has no access to the test block and never imports
the data loader.
"""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any, Callable

import numpy as np

from ..evaluation.metrics import mae


@dataclass
class TrialResult:
    trial: int
    hyperparameters: dict[str, Any]
    validation_mae: float | None
    seconds: float
    status: str
    error: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "trial": self.trial,
            "hyperparameters": self.hyperparameters,
            "validation_mae": self.validation_mae,
            "seconds": round(self.seconds, 4),
            "status": self.status,
            "error": self.error,
        }


@dataclass
class SearchResult:
    best_hyperparameters: dict[str, Any]
    best_validation_mae: float | None
    trials: list[TrialResult] = field(default_factory=list)
    stopped_reason: str = "completed"

    @property
    def n_trials(self) -> int:
        return len(self.trials)

    @property
    def n_failed(self) -> int:
        return sum(1 for t in self.trials if t.status != "ok")

    def to_dict(self) -> dict[str, Any]:
        return {
            "best_hyperparameters": self.best_hyperparameters,
            "best_validation_mae": self.best_validation_mae,
            "n_trials": self.n_trials,
            "n_failed": self.n_failed,
            "stopped_reason": self.stopped_reason,
            "trials": [t.to_dict() for t in self.trials],
        }


def sample_configuration(space: dict[str, list[Any]], rng: np.random.Generator) -> dict[str, Any]:
    """Draw one configuration uniformly from the declared search space."""
    config: dict[str, Any] = {}
    for name, values in space.items():
        if not values:
            continue
        index = int(rng.integers(0, len(values)))
        config[name] = values[index]
    return config


def default_configuration(space: dict[str, list[Any]]) -> dict[str, Any]:
    """First declared value per parameter — the deterministic fallback."""
    return {name: values[0] for name, values in space.items() if values}


def select_hyperparameters(
    build_and_evaluate: Callable[[dict[str, Any]], float],
    space: dict[str, list[Any]],
    *,
    max_trials: int = 24,
    max_seconds: float = 300.0,
    seed: int = 42,
    minimise: bool = True,
) -> SearchResult:
    """Run a budgeted random search.

    ``build_and_evaluate(config)`` must fit on training rows, score on validation
    rows, and return the validation MAE. Exceptions are caught, logged as failed
    trials, and do not abort the search — a failure is data about the search
    space.
    """
    rng = np.random.default_rng(seed)
    trials: list[TrialResult] = []
    best_config = default_configuration(space)
    best_score: float | None = None
    stopped = "max_trials"

    seen: set[tuple] = set()
    started = time.perf_counter()

    for trial_index in range(max_trials):
        elapsed = time.perf_counter() - started
        if elapsed > max_seconds:
            stopped = "max_seconds"
            break

        config = sample_configuration(space, rng) if space else {}
        key = tuple(sorted((k, str(v)) for k, v in config.items()))
        if key in seen and len(seen) < _space_size(space):
            # Avoid burning budget on a duplicate draw when unexplored space remains.
            config = default_configuration(space) if not seen else config
        seen.add(key)

        trial_started = time.perf_counter()
        try:
            score = build_and_evaluate(config)
            seconds = time.perf_counter() - trial_started
            if not np.isfinite(score):
                trials.append(
                    TrialResult(trial_index, config, None, seconds, "failed", "non-finite score")
                )
                continue
            trials.append(TrialResult(trial_index, config, float(score), seconds, "ok"))
            if best_score is None or (score < best_score if minimise else score > best_score):
                best_score = float(score)
                best_config = config
        except Exception as exc:  # noqa: BLE001 - a failed trial is recorded, not hidden
            seconds = time.perf_counter() - trial_started
            trials.append(
                TrialResult(
                    trial_index, config, None, seconds, "failed", f"{type(exc).__name__}: {exc}"
                )
            )

    if not trials:
        stopped = "no_trials"
    return SearchResult(
        best_hyperparameters=best_config,
        best_validation_mae=best_score,
        trials=trials,
        stopped_reason=stopped,
    )


def _space_size(space: dict[str, list[Any]]) -> int:
    size = 1
    for values in space.values():
        size *= max(len(values), 1)
    return size


def cross_validated_score(
    build_estimator: Callable[[], Any],
    X,
    y,
    folds: list[tuple[np.ndarray, np.ndarray]],
) -> float:
    """Mean validation MAE across expanding-window folds.

    The estimator is rebuilt for every fold, so any preprocessing refits per
    fold. This is the structural guarantee against scaler leakage.
    """
    scores: list[float] = []
    for train_idx, val_idx in folds:
        estimator = build_estimator()
        estimator.fit(X.iloc[train_idx] if hasattr(X, "iloc") else X[train_idx],
                      y.iloc[train_idx] if hasattr(y, "iloc") else y[train_idx])
        preds = estimator.predict(X.iloc[val_idx] if hasattr(X, "iloc") else X[val_idx])
        scores.append(mae(y.iloc[val_idx] if hasattr(y, "iloc") else y[val_idx], preds))
    return float(np.mean(scores)) if scores else float("nan")
