"""Shared estimator interface.

Every model lane returns an object satisfying:

1. ``fit(X, y)`` / ``predict(X)`` — scikit-learn estimator protocol.
2. Accepts a ``pandas.DataFrame`` with named columns and records
   ``feature_names_in_`` so that a mismatch is detectable.
3. Any learned preprocessing lives **inside** the returned ``Pipeline``, so
   refitting per CV fold is automatic and leakage-free by construction.

:func:`make_pipeline` is the only sanctioned way to assemble a model. It wraps
the variant's transformer with the estimator, which guarantees the scaling
statistic is computed from the training rows passed to ``fit``.
"""

from __future__ import annotations

from typing import Any, Callable

from sklearn.pipeline import Pipeline

from ..features.pipeline import build_preprocessor

# Registry maps protocol ``model_id`` -> factory. Factories are imported lazily
# by name to keep optional lanes (mlp) genuinely optional.
MODEL_REGISTRY: dict[str, str] = {
    "ridge": "int4096.models.ridge:build_ridge",
    "linear_baseline": "int4096.models.ridge:build_linear_baseline",
    "svr": "int4096.models.svr:build_svr",
    "random_forest": "int4096.models.random_forest:build_random_forest",
    "hist_gradient_boosting": (
        "int4096.models.hist_gradient_boosting:build_hist_gradient_boosting"
    ),
    "mlp": "int4096.models.mlp:build_mlp",
}


def resolve_model_class(dotted: str) -> Callable[..., Any]:
    """Import ``package.module:attr``."""
    module_name, _, attr = dotted.partition(":")
    if not attr:
        raise ValueError(f"Malformed registry entry {dotted!r}; expected 'module:attr'")
    import importlib

    module = importlib.import_module(module_name)
    try:
        return getattr(module, attr)
    except AttributeError as exc:
        raise ImportError(f"{module_name} has no attribute {attr!r}") from exc


def make_pipeline(
    estimator,
    variant: dict[str, Any],
    *,
    feature_columns: list[str] | None = None,
    reduce_features: bool = True,
):
    """Assemble ``[preprocessor] -> estimator``.

    ``feature_columns`` narrows the design matrix (used by the P3 ablation)
    via a column selector that records the retained names.
    """
    steps: list[tuple[str, Any]] = []

    if feature_columns is not None and reduce_features:
        steps.append(("select", _ColumnSelector(feature_columns)))

    preprocessor = build_preprocessor(variant)
    if preprocessor is not None:
        steps.append(("preprocess", preprocessor))

    steps.append(("model", estimator))
    return Pipeline(steps)


class _ColumnSelector:
    """Select a fixed list of columns from a DataFrame by name."""

    def __init__(self, columns: list[str]):
        self.columns = list(columns)

    def fit(self, X, y=None):  # noqa: N803 - sklearn API
        missing = [c for c in self.columns if c not in getattr(X, "columns", [])]
        if missing:
            raise KeyError(f"Column selector: missing columns {missing}")
        self.feature_names_in_ = list(X.columns)
        self.n_features_in_ = len(self.columns)
        return self

    def transform(self, X):  # noqa: N803 - sklearn API
        if hasattr(X, "loc"):
            return X.loc[:, self.columns]
        import numpy as np

        idx = [list(self.feature_names_in_).index(c) for c in self.columns]
        return np.asarray(X)[:, idx]

    def fit_transform(self, X, y=None):  # noqa: N803
        return self.fit(X, y).transform(X)

    def get_params(self, deep: bool = True):  # noqa: ARG002
        return {"columns": self.columns}

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self


def build_estimator(
    model_id: str,
    hyperparams: dict[str, Any],
    seed: int,
    variant: dict[str, Any],
    feature_columns: list[str] | None = None,
):
    """Build a complete, unfitted pipeline for one model lane.

    For the ``reduced`` feature variant the column subset is resolved here, so a
    caller cannot accidentally give one lane the full feature set while another
    lane gets the reduced set — that would silently break the comparison.
    """
    from ..features.build import REDUCED_FEATURES

    factory = resolve_model_class(MODEL_REGISTRY[model_id])
    estimator = factory(hyperparams, seed)

    if variant.get("features") == "reduced" and feature_columns is None:
        feature_columns = list(REDUCED_FEATURES)

    return make_pipeline(estimator, variant, feature_columns=feature_columns)
