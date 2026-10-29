"""Train-fitted preprocessing variants P0–P4.

The rule this module exists to enforce: **every transformation that learns a
parameter is fitted on training rows only**, inside a scikit-learn ``Pipeline``,
so it is refitted per CV fold and can never see validation or test values.

Variant meanings are defined in ``configs/research_protocol.yaml`` and mirrored
in ``docs/research/protocol.md`` §6:

====  ==================================================================
P0    minimal causal feature set, no scaling, train-fitted median impute
P1    P0 + missingness indicators (only meaningful if values are missing)
P2    P0 + StandardScaler fitted on training rows
P3    reduced feature set (feature-engineering ablation)
P4    P0 + robust scaling + train-quantile winsorization
====  ==================================================================

P2 applied to a tree model is a deliberate **negative control**: trees are
invariant to monotone per-feature scaling, so a large P2 delta for a forest
would indicate a bug rather than a discovery.
"""

from __future__ import annotations

from typing import Any

import numpy as np

from .build import REDUCED_FEATURES

FULL_FEATURES_PLACEHOLDER = None  # resolved from the design matrix at runtime


def select_feature_columns(variant: dict[str, Any], all_columns: list[str]) -> list[str]:
    """Return the ordered feature subset for a variant.

    ``variant['features']`` is either ``'full'`` or ``'reduced'``.
    """
    spec = str(variant.get("features", "full"))
    if spec == "full":
        return list(all_columns)
    if spec == "reduced":
        return [c for c in REDUCED_FEATURES if c in all_columns]
    raise ValueError(f"Unknown feature spec {spec!r}; expected 'full' or 'reduced'")


def build_preprocessor(variant: dict[str, Any]):
    """Build an *unfitted* sklearn transformer for a preprocessing variant.

    Returns ``None`` when the variant needs no transformation (P0 on clean
    data), in which case the caller uses the raw numeric matrix.
    """
    from sklearn.impute import SimpleImputer
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import RobustScaler, StandardScaler

    steps = []

    if variant.get("missing_indicators"):
        # Genuine missingness indicators: one binary column per input that
        # records whether the value was absent *before* imputation. With no
        # missing inputs these columns are constant zero, which is exactly why
        # the P1 ablation is reported as NOT_RUN rather than as a result.
        steps.append(("indicators", _MissingIndicator()))

    imputer_strategy = variant.get("imputer")
    if imputer_strategy:
        steps.append(("impute", SimpleImputer(strategy=str(imputer_strategy))))

    winsor = variant.get("winsorize_quantiles")
    if winsor:
        lower, upper = float(winsor[0]), float(winsor[1])
        steps.append(("winsorize", _QuantileClipper(lower=lower, upper=upper)))

    scaler = variant.get("scaler")
    if scaler == "standard":
        steps.append(("scale", StandardScaler()))
    elif scaler == "robust":
        steps.append(("scale", RobustScaler()))
    elif scaler not in (None, "none"):
        raise ValueError(f"Unknown scaler {scaler!r}")

    if not steps:
        return None
    return Pipeline(steps)


class _MissingIndicator:
    """Append a 0/1 column per feature recording pre-imputation missingness."""

    def fit(self, X, y=None):  # noqa: N803 - sklearn API
        arr = _as_2d(X)
        self.n_features_in_ = arr.shape[1]
        self.missing_seen_ = np.asarray(np.isnan(arr).any(axis=0), dtype=bool)
        return self

    def transform(self, X):  # noqa: N803 - sklearn API
        arr = _as_2d(X)
        return np.hstack([arr, np.isnan(arr).astype("float64")])

    def fit_transform(self, X, y=None):  # noqa: N803
        return self.fit(X, y).transform(X)

    def get_params(self, deep: bool = True):  # noqa: ARG002
        return {}

    def set_params(self, **params):  # noqa: ARG002
        return self


def _as_2d(X) -> np.ndarray:
    if hasattr(X, "to_numpy"):
        return X.to_numpy(dtype="float64")
    return np.asarray(X, dtype="float64")


class _QuantileClipper:
    """Clip each feature to quantiles learned on the training rows only.

    Implemented as a tiny sklearn-compatible transformer so that the clipping
    bounds are stored with the fitted pipeline and are therefore auditable.
    """

    def __init__(self, lower: float = 0.01, upper: float = 0.99):
        self.lower = lower
        self.upper = upper

    def fit(self, X, y=None):  # noqa: N803 - sklearn API
        arr = np.asarray(X, dtype="float64")
        self.lower_bounds_ = np.nanquantile(arr, self.lower, axis=0)
        self.upper_bounds_ = np.nanquantile(arr, self.upper, axis=0)
        self.n_features_in_ = arr.shape[1]
        return self

    def transform(self, X):  # noqa: N803 - sklearn API
        arr = np.asarray(X, dtype="float64")
        return np.clip(arr, self.lower_bounds_, self.upper_bounds_)

    def fit_transform(self, X, y=None):  # noqa: N803
        return self.fit(X, y).transform(X)

    def get_params(self, deep: bool = True):  # noqa: ARG002 - sklearn API
        return {"lower": self.lower, "upper": self.upper}

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self


VARIANT_BUILDERS = {
    "P0": build_preprocessor,
    "P1": build_preprocessor,
    "P2": build_preprocessor,
    "P3": build_preprocessor,
    "P4": build_preprocessor,
}


def variant_is_applicable(variant: dict[str, Any], X) -> tuple[bool, str]:
    """Decide whether a variant is meaningful for this design matrix.

    Returns ``(applicable, reason_if_not)``. A variant that cannot change
    anything is reported as NOT_RUN instead of being published as a result that
    silently duplicates another cell (see decision D13).
    """
    if variant.get("missing_indicators"):
        if not bool(np.isnan(_as_2d(X)).any()):
            return False, "no missing inputs in snapshot: imputation is a no-op"
    return True, ""


def build_variant_matrix(
    X_train,
    X_apply,
    variant: dict[str, Any],
    all_columns: list[str],
) -> tuple[np.ndarray, np.ndarray, list[str]]:
    """Fit a variant's preprocessing on ``X_train`` and apply it to ``X_apply``.

    This helper exists for diagnostics and tests. Real model runs must use
    :func:`int4096.models.base.make_pipeline`, which puts the same transformer
    *inside* the estimator pipeline so that CV refits it per fold.

    Returns the transformed matrices and the feature names retained.
    """
    columns = select_feature_columns(variant, all_columns)
    train_matrix = X_train[columns].to_numpy(dtype="float64")
    apply_matrix = X_apply[columns].to_numpy(dtype="float64")

    preprocessor = build_preprocessor(variant)
    if preprocessor is not None:
        train_matrix = preprocessor.fit_transform(train_matrix)
        apply_matrix = preprocessor.transform(apply_matrix)
    return train_matrix, apply_matrix, columns
