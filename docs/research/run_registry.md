# Run Registry

**Generated** by `python -m int4096.experiments.registry_report` from
`artifacts/experiments/registry.jsonl`. Do not edit by hand.

The registry is **append-only**. A failed run is never deleted: failures are
evidence, and the coverage table below depends on them being visible.

## Coverage

| Status | Count |
|---|---|
| SUCCESS | 20 |
| FAILED | 0 |
| INCOMPLETE | 0 |
| NOT_RUN | 0 |
| **Total attempted** | **20** |

## Cells

| run_id | status | asset | model | variant | val MAE | skill_MAE | test | review |
|---|---|---|---|---|---|---|---|---|
| `2026-10-29T134801Z_aapl_hist_gradient_boosting_P0_seed42` | SUCCESS | AAPL | hist_gradient_boosting | P0 | 2.8985 | 0.0025 | n/a | UNREVIEWED |
| `2026-10-29T134805Z_aapl_hist_gradient_boosting_P2_seed42` | SUCCESS | AAPL | hist_gradient_boosting | P2 | 2.8985 | 0.0025 | n/a | UNREVIEWED |
| `2026-10-29T134733Z_aapl_linear_baseline_P0_seed42` | SUCCESS | AAPL | linear_baseline | P0 | 2.8986 | 0.0024 | n/a | UNREVIEWED |
| `2026-10-29T134734Z_aapl_linear_baseline_P2_seed42` | SUCCESS | AAPL | linear_baseline | P2 | 2.9202 | -0.0050 | n/a | UNREVIEWED |
| `2026-10-29T134741Z_aapl_random_forest_P0_seed42` | SUCCESS | AAPL | random_forest | P0 | 2.9283 | -0.0078 | n/a | UNREVIEWED |
| `2026-10-29T134751Z_aapl_random_forest_P2_seed42` | SUCCESS | AAPL | random_forest | P2 | 2.9283 | -0.0078 | n/a | UNREVIEWED |
| `2026-10-29T134735Z_aapl_ridge_P0_seed42` | SUCCESS | AAPL | ridge | P0 | 2.8983 | 0.0025 | n/a | UNREVIEWED |
| `2026-10-29T134737Z_aapl_ridge_P2_seed42` | SUCCESS | AAPL | ridge | P2 | 2.8971 | 0.0029 | n/a | UNREVIEWED |
| `2026-10-29T134738Z_aapl_svr_P0_seed42` | SUCCESS | AAPL | svr | P0 | 2.8907 | 0.0051 | n/a | UNREVIEWED |
| `2026-10-29T134739Z_aapl_svr_P2_seed42` | SUCCESS | AAPL | svr | P2 | 2.8904 | 0.0052 | n/a | UNREVIEWED |
| `2026-10-29T134843Z_btc_hist_gradient_boosting_P0_seed42` | SUCCESS | BTC | hist_gradient_boosting | P0 | 1605.0165 | -0.0004 | n/a | UNREVIEWED |
| `2026-10-29T134847Z_btc_hist_gradient_boosting_P2_seed42` | SUCCESS | BTC | hist_gradient_boosting | P2 | 1605.0165 | -0.0004 | n/a | UNREVIEWED |
| `2026-10-29T134809Z_btc_linear_baseline_P0_seed42` | SUCCESS | BTC | linear_baseline | P0 | 1600.2052 | 0.0026 | n/a | UNREVIEWED |
| `2026-10-29T134810Z_btc_linear_baseline_P2_seed42` | SUCCESS | BTC | linear_baseline | P2 | 1603.5868 | 0.0005 | n/a | UNREVIEWED |
| `2026-10-29T134818Z_btc_random_forest_P0_seed42` | SUCCESS | BTC | random_forest | P0 | 1603.3734 | 0.0006 | n/a | UNREVIEWED |
| `2026-10-29T134831Z_btc_random_forest_P2_seed42` | SUCCESS | BTC | random_forest | P2 | 1603.3734 | 0.0006 | n/a | UNREVIEWED |
| `2026-10-29T134812Z_btc_ridge_P0_seed42` | SUCCESS | BTC | ridge | P0 | 1601.8739 | 0.0015 | n/a | UNREVIEWED |
| `2026-10-29T134813Z_btc_ridge_P2_seed42` | SUCCESS | BTC | ridge | P2 | 1602.3879 | 0.0012 | n/a | UNREVIEWED |
| `2026-10-29T134814Z_btc_svr_P0_seed42` | SUCCESS | BTC | svr | P0 | 1604.1858 | 0.0001 | n/a | UNREVIEWED |
| `2026-10-29T134816Z_btc_svr_P2_seed42` | SUCCESS | BTC | svr | P2 | 1603.1314 | 0.0008 | n/a | UNREVIEWED |

## Explicit gaps

Cells that were planned but not executed are listed here rather than omitted,
so the report cannot imply coverage that does not exist.

None: every asset x model x variant cell in the registry succeeded.

## What this registry does not prove

- It does not prove the runs are correct; that is the leakage auditor's job.
- `test` is `n/a` for every row until a single human-approved release occurs
  (decision D7). Absence of test metrics is deliberate, not missing work.
- `review_state` is `UNREVIEWED` until an independent auditor signs off.
