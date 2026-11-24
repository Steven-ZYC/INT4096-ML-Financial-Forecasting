# Supplementary test: can neural networks call tomorrow's direction?

**Generated** by `scripts/summarize_models.py` from the newest complete run (`2026-11-24T005949Z/`). Experiment: `scripts/supplementary_direction_test.py`; decision D14.

How often does the model correctly predict whether the next close is higher than today's?

- Data: same snapshots, chronological split and purge as the main study; validation block only; test block not read.
- Inputs: MLP = today's 10 engineered features; LSTM = last 20 days of the same 10 features (a sequence; not identical inputs).
- Selection: grid {'hidden': (16, 32, 64), 'dropout': (0.0, 0.2), 'lr': (0.001, 0.003)} chosen by log-loss on the last 20% of the training block (gap 1); early stopping on the same hold-out; validation used once for reporting.
- Seeds [0, 1, 2, 3, 4] (probabilities averaged); device `cuda`, torch 2.9.1+cu130.
- Uncertainty: moving-block bootstrap, block 10, 1000 resamples, 95%, accuracy minus majority rule.

| Asset | Validation days | Majority rule | MLP | LSTM | Classical models |
|---|---:|---|---|---|---|
| AAPL | 244 | always up: 55.7% | 54.1% (seeds 48.4%–57.8%); vs majority -1.6 pp [-10.7, +7.0] | 52.0% (seeds 45.5%–55.7%); vs majority -3.7 pp [-11.9, +5.3] | 50.4%–58.6% |
| BTC | 358 | always down: 48.0% | 50.0% (seeds 48.9%–50.0%); vs majority +2.0 pp [-4.8, +7.3] | 53.3% (seeds 49.2%–52.0%); vs majority +5.3 pp [-0.3, +10.1] | 48.9%–53.1% |

Every interval includes zero: neither network calls the direction reliably better than the majority rule. Direction accuracy ignores costs and risk; this is not a trading signal.
