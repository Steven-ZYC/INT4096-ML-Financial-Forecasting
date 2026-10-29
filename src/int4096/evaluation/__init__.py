"""Evaluation layer: baselines, metrics and figures.

Kept deliberately small and independently testable. The metrics module is the
single source of truth for every number that reaches the report.
"""

from .baselines import naive_persistence
from .metrics import (
    mae,
    rmse,
    r2,
    skill_score,
    normalized_mae,
    direction_accuracy,
    evaluate_predictions,
    moving_block_bootstrap,
)

__all__ = [
    "plot_ablation_delta",
    "plot_coverage_and_splits",
    "plot_model_vs_naive",
    "plot_observed_vs_predicted",
    "plot_train_vs_validation",
    "direction_accuracy",
    "evaluate_predictions",
    "mae",
    "moving_block_bootstrap",
    "naive_persistence",
    "normalized_mae",
    "r2",
    "rmse",
    "skill_score",
]
