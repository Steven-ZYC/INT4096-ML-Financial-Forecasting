"""Model layer: one consistent estimator interface for every lane.

All model lanes share the same construction path (:func:`make_pipeline`), the
same feature contract and the same evaluation interface. That is what makes the
comparison fair. A lane that needs a different data path is a defect.
"""

from .base import MODEL_REGISTRY, build_estimator, make_pipeline, resolve_model_class
from .ridge import LinearBaseline, build_linear_baseline, build_ridge
from .svr import build_svr
from .random_forest import build_random_forest
from .hist_gradient_boosting import build_hist_gradient_boosting

__all__ = [
    "MODEL_REGISTRY",
    "LinearBaseline",
    "build_estimator",
    "build_hist_gradient_boosting",
    "build_random_forest",
    "build_linear_baseline",
    "build_ridge",
    "build_svr",
    "make_pipeline",
    "resolve_model_class",
]

try:  # optional lane; requires explicit owner approval (protocol decision D2)
    from .mlp import build_mlp  # noqa: F401

    __all__.append("build_mlp")
except ImportError:  # pragma: no cover
    pass
