"""Feature layer: strictly causal features and train-fitted preprocessing.

The single most important property of this module is the **as-of contract**:
a feature row at time ``t`` may use bars ``<= t`` and nothing later. Every
function below uses only trailing windows, and ``build_features`` returns a
frame aligned to the input index without any backward fill.
"""

from .build import FEATURE_FUNCTIONS, build_features, feature_dictionary
from .pipeline import (
    VARIANT_BUILDERS,
    build_preprocessor,
    build_variant_matrix,
    select_feature_columns,
    variant_is_applicable,
)

__all__ = [
    "FEATURE_FUNCTIONS",
    "VARIANT_BUILDERS",
    "build_features",
    "build_preprocessor",
    "build_variant_matrix",
    "feature_dictionary",
    "select_feature_columns",
    "variant_is_applicable",
]
