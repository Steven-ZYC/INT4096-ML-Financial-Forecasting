"""Optional small MLP lane.

**Status: gated.** Including a neural model requires a recorded decision
(protocol decision D2) because the course handout discourages deep learning and
the instructor's oral guidance must be documented rather than assumed.

Justification (for the decision record, not an assertion of approval)
---------------------------------------------------------------------
A single hidden layer MLP over the same ten engineered features tests whether
*learned nonlinear feature interactions* add anything beyond kernel SVR and
boosted trees. It does **not** test sequence modelling; an LSTM would answer a
different question (temporal representation learning) and is deliberately out of
scope for a five-person project with a ~2,500-word report.

If this lane is enabled, the report must state that it is a shallow neural
network over engineered features, not "deep learning on raw sequences".
"""

from __future__ import annotations

from typing import Any

from sklearn.neural_network import MLPRegressor

REQUIRES_OWNER_APPROVAL = True
APPROVAL_REFERENCE = "docs/research/decision_log.md (decision D2)"


def build_mlp(hyperparams: dict[str, Any], seed: int) -> MLPRegressor:
    """Shallow MLP. Requires standardized inputs — supplied by variant P2."""
    params: dict[str, Any] = {
        "hidden_layer_sizes": (32,),
        "activation": "relu",
        "solver": "adam",
        "alpha": 1e-4,
        "learning_rate_init": 1e-3,
        "max_iter": 500,
        "early_stopping": True,
        "validation_fraction": 0.1,
        "n_iter_no_change": 20,
    }
    params.update({k: v for k, v in hyperparams.items() if v is not None})
    if isinstance(params.get("hidden_layer_sizes"), list):
        params["hidden_layer_sizes"] = tuple(params["hidden_layer_sizes"])
    params["random_state"] = seed
    return MLPRegressor(**params)
