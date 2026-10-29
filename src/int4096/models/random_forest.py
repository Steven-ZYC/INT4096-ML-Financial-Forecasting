"""Random Forest lane.

Scientific note
---------------
Bagging many deep trees reduces variance but cannot extrapolate: every
prediction is an average of training-set leaf values, so the forest cannot
predict a price outside the range it saw. On a trending price series this is a
structural limitation worth showing to learners.

Trees are also **invariant to monotone per-feature scaling**, which makes them
the natural negative control for the P2 ablation: if scaling changes forest
error materially, suspect a bug rather than a discovery.

Multi-threading is fixed to one worker so that runtimes and results are
comparable across lanes and reproducible on a small machine.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.ensemble import RandomForestRegressor


def build_random_forest(hyperparams: dict[str, Any], seed: int) -> RandomForestRegressor:
    params: dict[str, Any] = {
        "n_estimators": 200,
        "max_depth": None,
        "min_samples_leaf": 1,
        "max_features": 1.0,
        "n_jobs": 1,
        "bootstrap": True,
    }
    params.update({k: v for k, v in hyperparams.items() if v is not None})
    # ``max_depth=None`` must survive the None-filter above.
    if "max_depth" in hyperparams:
        params["max_depth"] = hyperparams["max_depth"]
    params["random_state"] = seed
    return RandomForestRegressor(**params)


def feature_importance(estimator, feature_names: list[str] | None = None):
    """Impurity-based importances, clearly labelled as not causal."""
    model = estimator
    if hasattr(estimator, "named_steps"):
        model = estimator.named_steps.get("model", estimator)
    importances = getattr(model, "feature_importances_", None)
    if importances is None:
        raise AttributeError("Estimator is not fitted or has no feature_importances_")
    names = feature_names or [f"f{i}" for i in range(len(importances))]
    order = np.argsort(importances)[::-1]
    return [{"feature": names[i], "importance": round(float(importances[i]), 6)} for i in order]
