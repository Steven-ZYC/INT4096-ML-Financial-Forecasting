"""Regularized linear lane (Ridge) plus a deliberately simple linear baseline.

Scientific note
---------------
Ridge is the transparent reference. Its coefficients are interpretable *only*
when features are not strongly collinear — our return features are correlated
by construction, so coefficient magnitudes must not be read as importance.
Permutation importance or standardized coefficients are the honest options.

Scaling is required: penalty strength is not scale-invariant, so an unscaled
Ridge would penalize ``dow`` (0–6) and ``ret_1`` (~0.01) differently for reasons
that have nothing to do with predictive value.
"""

from __future__ import annotations

from typing import Any

import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.linear_model import Ridge


def build_ridge(hyperparams: dict[str, Any], seed: int) -> Ridge:
    """Ridge regression with a recorded, deterministic solver."""
    params = {"alpha": 1.0, "solver": "svd"}
    params.update({k: v for k, v in hyperparams.items() if v is not None})
    # ``random_state`` is irrelevant for the svd solver but harmless; recorded
    # for completeness so the manifest seed always maps to something real.
    params.setdefault("random_state", seed)
    return Ridge(**params)


def build_linear_baseline(hyperparams: dict[str, Any], seed: int) -> "LinearBaseline":
    """Factory matching the shared ``factory(hyperparams, seed)`` interface.

    The class itself takes a scalar ``alpha``; the factory adapts the protocol's
    dict-shaped search space to it so that every lane is constructed by the same
    call signature.
    """
    alpha = float(hyperparams.get("alpha", 1e-6) or 1e-6)
    return LinearBaseline(alpha=alpha)


class LinearBaseline(RegressorMixin, BaseEstimator):
    """Ordinary least squares with a fixed tiny ridge penalty.

    This is the *learned floor*: a model with essentially no capacity to overfit
    the feature set. If a complex model cannot beat this, the extra capacity is
    not buying generalization on this task.

    Implemented separately from :func:`build_ridge` so the report can state
    precisely that the baseline is a near-unregularized linear model rather than
    a tuned competitor.
    """

    def __init__(self, alpha: float = 1e-6):
        self.alpha = alpha

    def fit(self, X, y):  # noqa: N803 - sklearn API
        self.model_ = Ridge(alpha=self.alpha, solver="svd")
        self.model_.fit(np.asarray(X, dtype="float64"), np.asarray(y, dtype="float64"))
        self.coef_ = self.model_.coef_
        self.intercept_ = self.model_.intercept_
        if hasattr(X, "columns"):
            self.feature_names_in_ = np.asarray(X.columns, dtype=object)
        return self

    def predict(self, X):  # noqa: N803 - sklearn API
        return self.model_.predict(np.asarray(X, dtype="float64"))

    def get_params(self, deep: bool = True):  # noqa: ARG002
        return {"alpha": self.alpha}

    def set_params(self, **params):
        for key, value in params.items():
            setattr(self, key, value)
        return self
