"""The report figures must show the same numbers as the report tables."""

from __future__ import annotations

import pandas as pd
import pytest

from int4096.config import load_protocol
from int4096.evaluation.figures import skill_chart_rows, split_spans
from int4096.experiments.run import prepare_dataset


@pytest.mark.parametrize("asset", ["AAPL", "BTC"])
def test_split_figure_dates_match_the_split_table(asset):
    prepared = prepare_dataset(asset, load_protocol())
    dates, split = prepared["X"].index, prepared["split"]
    spans = split_spans(split, dates)
    described = split.describe(dates)
    for block in ("train", "validation", "test"):
        first, last = spans[block]
        assert described[f"{block}_period"] == f"{first.date()}..{last.date()}"


def _row(run_id, model_id, variant, skill):
    return {"run_id": run_id, "status": "SUCCESS", "asset": "AAPL", "model_id": model_id,
            "preprocess_variant": variant, "validation_skill_mae": skill}


def test_skill_chart_draws_one_bar_per_asset_and_model():
    registry = pd.DataFrame([
        _row("1", "ridge", "P0", 0.9),
        _row("2", "ridge", "P2", 0.1),
        _row("3", "svr", "P2", -0.2),
        _row("4", "ridge", "P2", 0.3),   # a later re-run replaces run 2
    ])
    rows = skill_chart_rows(registry, "P2")
    assert list(rows["model_id"]) == ["ridge", "svr"]
    assert list(rows["validation_skill_mae"]) == [0.3, -0.2]
