"""Chronological splitting.

Two things live here, and both are deliberately boring:

* :func:`chronological_split` — the single frozen 60/20/20 boundary rule.
* :func:`expanding_window_folds` — the inner CV used for hyperparameter search.

Neither function ever shuffles. Neither function looks at feature values; they
operate on row positions only, so a split cannot depend on the data it splits.
"""

from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class Split:
    """Row-position boundaries for train / validation / test."""

    train_start: int
    train_end: int          # exclusive
    validation_start: int
    validation_end: int     # exclusive
    test_start: int
    test_end: int           # exclusive

    @property
    def train(self) -> slice:
        return slice(self.train_start, self.train_end)

    @property
    def validation(self) -> slice:
        return slice(self.validation_start, self.validation_end)

    @property
    def test(self) -> slice:
        return slice(self.test_start, self.test_end)

    def to_dict(self) -> dict[str, int]:
        return {
            "train_start": self.train_start,
            "train_end": self.train_end,
            "validation_start": self.validation_start,
            "validation_end": self.validation_end,
            "test_start": self.test_start,
            "test_end": self.test_end,
        }

    def describe(self, index) -> dict[str, str]:
        """Human-readable date boundaries for manifests and dataset cards."""

        def stamp(pos: int, *, exclusive: bool = False) -> str:
            if exclusive:
                pos = pos - 1
            if pos < 0 or pos >= len(index):
                return "n/a"
            return str(index[pos].date())

        return {
            "train_period": f"{stamp(self.train_start)}..{stamp(self.train_end, exclusive=True)}",
            "validation_period": (
                f"{stamp(self.validation_start)}..{stamp(self.validation_end, exclusive=True)}"
            ),
            "test_period": f"{stamp(self.test_start)}..{stamp(self.test_end, exclusive=True)}",
            "train_rows": str(self.train_end - self.train_start),
            "validation_rows": str(self.validation_end - self.validation_start),
            "test_rows": str(self.test_end - self.test_start),
        }


def chronological_split(
    n_rows: int,
    train_fraction: float = 0.60,
    validation_fraction: float = 0.20,
    test_fraction: float = 0.20,
    min_rows: int = 60,
    horizon_gap: int = 1,
) -> Split:
    """Split row positions into contiguous, non-overlapping blocks.

    Fractions must sum to 1 (within floating point tolerance). The test block is
    exactly the tail of the series.

    Parameters
    ----------
    horizon_gap : int
        Number of boundary rows to **purge** at each split. With a one-step
        label ``y_t = Close_{t+1}``, the label of the last training row is a
        price from the validation block, and the label of the last validation
        row is a price from the sealed test block. Leaving those rows in place
        means (a) training supervises on a validation-block price and (b) the
        reported validation metric depends on one sealed test price. Purging one
        row at each boundary removes both channels. ``horizon_gap=0`` is
        available only for explicitly documented sensitivity analyses.
    """
    total = train_fraction + validation_fraction + test_fraction
    if abs(total - 1.0) > 1e-6:
        raise ValueError(f"Split fractions must sum to 1.0, got {total}")
    if n_rows < min_rows:
        raise ValueError(f"Need at least {min_rows} rows to split, got {n_rows}")

    if horizon_gap < 0:
        raise ValueError("horizon_gap must be >= 0")

    raw_train_end = int(round(n_rows * train_fraction))
    raw_validation_end = raw_train_end + int(round(n_rows * validation_fraction))

    # Guarantee a non-empty block for each split even on tiny inputs.
    raw_train_end = max(raw_train_end, 1)
    raw_validation_end = max(raw_validation_end, raw_train_end + 1)
    raw_validation_end = min(raw_validation_end, n_rows - 1)

    # Purge the boundary rows whose labels reach into the next block.
    train_end = raw_train_end - horizon_gap
    validation_end = raw_validation_end - horizon_gap
    if train_end < 1 or validation_end <= raw_train_end:
        raise ValueError(
            f"horizon_gap={horizon_gap} leaves an empty block "
            f"(n_rows={n_rows}, train_end={train_end}, validation_end={validation_end})"
        )

    split = Split(
        train_start=0,
        train_end=train_end,
        validation_start=raw_train_end,
        validation_end=validation_end,
        test_start=raw_validation_end,
        test_end=n_rows,
    )
    _assert_disjoint(split, n_rows)
    return split


def _assert_disjoint(split: Split, n_rows: int) -> None:
    if not (0 <= split.train_start < split.train_end <= n_rows):
        raise ValueError(f"Invalid train block: {split}")
    # A purge gap may leave a hole between blocks; overlap is still forbidden.
    if not (split.train_end <= split.validation_start < split.validation_end <= n_rows):
        raise ValueError(f"Invalid validation block: {split}")
    if not (split.validation_end <= split.test_start < split.test_end <= n_rows):
        raise ValueError(f"Invalid test block: {split}")
    if split.test_end != n_rows:
        raise ValueError("The test block must be the tail of the series.")


def expanding_window_folds(
    n_rows: int,
    n_splits: int = 5,
    gap: int = 1,
    min_train_fraction: float = 0.30,
) -> list[tuple[np.ndarray, np.ndarray]]:
    """Expanding-window (walk-forward) CV fold indices.

    Fold ``k`` trains on ``[0, cut_k)`` and validates on
    ``[cut_k + gap, cut_{k+1})``. The ``gap`` purges the boundary row whose
    label (``Close[t+1]``) overlaps the first validation row's feature window.

    Training indices are always a *prefix*, so a fold can never see a
    validation row.
    """
    if n_splits < 1:
        raise ValueError("n_splits must be >= 1")
    if gap < 0:
        raise ValueError("gap must be >= 0")

    first_train = max(int(round(n_rows * min_train_fraction)), 2)
    remaining = n_rows - first_train - gap
    if remaining < n_splits:
        raise ValueError(
            f"Not enough rows ({n_rows}) for {n_splits} folds with "
            f"min_train_fraction={min_train_fraction} and gap={gap}"
        )

    fold_size = remaining // n_splits
    folds: list[tuple[np.ndarray, np.ndarray]] = []
    for k in range(n_splits):
        val_start = first_train + gap + k * fold_size
        val_end = val_start + fold_size if k < n_splits - 1 else n_rows
        train_idx = np.arange(0, val_start - gap)
        val_idx = np.arange(val_start, val_end)
        if len(train_idx) == 0 or len(val_idx) == 0:
            continue
        folds.append((train_idx, val_idx))
    return folds


def assert_no_overlap(folds, n_rows: int) -> None:
    """Verify every fold's train prefix ends before its validation block."""
    for k, (train_idx, val_idx) in enumerate(folds):
        if train_idx.max() >= val_idx.min():
            raise AssertionError(f"Fold {k}: training index overlaps validation")
        if val_idx.min() <= train_idx.max():
            raise AssertionError(f"Fold {k}: validation starts inside training")
        if train_idx.min() < 0 or val_idx.max() >= n_rows:
            raise AssertionError(f"Fold {k}: index out of range")
