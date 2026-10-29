"""Support Vector Regression lane (RBF kernel).

Scientific note
---------------
SVR is the project's clearest demonstration that **preprocessing is part of the
model**. An RBF kernel compares distances in feature space, so a feature whose
numerical range is 100x larger dominates the kernel. Scaling therefore changes
SVR's behaviour qualitatively, while a random forest is unaffected.

The epsilon-insensitive tube also means SVR ignores residuals smaller than
``epsilon``, which interacts with the price scale: the same ``epsilon`` is a
very different tolerance for AAPL (~$300) than for BTC (~$80,000).
"""

from __future__ import annotations

from typing import Any

from sklearn.svm import SVR


def build_svr(hyperparams: dict[str, Any], seed: int) -> SVR:
    """RBF-kernel SVR.

    ``cache_size`` is raised modestly; runtime is bounded by the tuning budget,
    not by an unbounded search.
    """
    params: dict[str, Any] = {
        "kernel": "rbf",
        "C": 1.0,
        "epsilon": 0.01,
        "gamma": "scale",
        "cache_size": 256,
        "max_iter": -1,
    }
    params.update({k: v for k, v in hyperparams.items() if v is not None})
    # SVR has no random_state; determinism comes from the deterministic solver.
    return SVR(**params)
