"""Histogram gradient boosting lane.

Scientific note
---------------
Boosting fits trees sequentially to the residual of the previous ensemble, so it
can fit fine structure that bagging averages away — including noise. On noisy
financial labels the practical risk is overfitting, controlled here by:

* a bounded ``max_iter`` from the protocol search space,
* ``early_stopping`` driven by an **inner** validation split taken from the
  training rows only (never the project validation block, never the test set),
* a fixed ``l2_regularization`` search range.

We use scikit-learn's histogram implementation instead of XGBoost so the
submission has no extra binary dependency and the Colab notebook installs
faster. This choice is documented in the decision log; it does not change the
model family being compared.
"""

from __future__ import annotations

from typing import Any

from sklearn.ensemble import HistGradientBoostingRegressor


def build_hist_gradient_boosting(
    hyperparams: dict[str, Any], seed: int
) -> HistGradientBoostingRegressor:
    params: dict[str, Any] = {
        "learning_rate": 0.05,
        "max_iter": 300,
        "max_depth": 3,
        "min_samples_leaf": 20,
        "l2_regularization": 0.0,
        # Early stopping uses an inner split carved out of the *training* rows
        # passed to fit(). The project's validation block is never passed to
        # fit(), so this cannot leak.
        "early_stopping": True,
        "validation_fraction": 0.1,
        "n_iter_no_change": 20,
    }
    params.update({k: v for k, v in hyperparams.items() if v is not None})
    if "max_depth" in hyperparams:
        params["max_depth"] = hyperparams["max_depth"]
    params["random_state"] = seed
    return HistGradientBoostingRegressor(**params)
