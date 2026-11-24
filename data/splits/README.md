# Data splits

**Generated** by `scripts/export_splits.py` from the frozen protocol (`configs/research_protocol.yaml`) and `src/int4096/data/split.py`. Do not edit by hand.

Every model on an asset uses exactly these rows. Tuning only ever sees the training block, through the expanding-window folds below. The validation block is used once, for reporting. The test block is sealed.

## AAPL (1,224 modelling rows)

| Block | First day | Last day | Rows |
|---|---|---|---:|
| Train (60%) | 2021-12-10 | 2024-11-08 | 733 |
| Validation (20%) | 2024-11-12 | 2025-11-03 | 244 |
| Test (20%, sealed) | 2025-11-05 | 2026-10-27 | 245 |

Purged boundary rows: 2024-11-11, 2025-11-04.

| Tuning fold | Fit on | Score on |
|---:|---|---|
| 1 | 2021-12-10 – 2022-10-25 (220) | 2022-10-27 – 2023-03-24 (102) |
| 2 | 2021-12-10 – 2023-03-23 (322) | 2023-03-27 – 2023-08-21 (102) |
| 3 | 2021-12-10 – 2023-08-18 (424) | 2023-08-22 – 2024-01-17 (102) |
| 4 | 2021-12-10 – 2024-01-16 (526) | 2024-01-18 – 2024-06-12 (102) |
| 5 | 2021-12-10 – 2024-06-11 (628) | 2024-06-13 – 2024-11-08 (104) |

## BTC (1,797 modelling rows)

| Block | First day | Last day | Rows |
|---|---|---|---:|
| Train (60%) | 2021-11-27 | 2024-11-07 | 1,077 |
| Validation (20%) | 2024-11-09 | 2025-11-01 | 358 |
| Test (20%, sealed) | 2025-11-03 | 2026-10-28 | 360 |

Purged boundary rows: 2024-11-08, 2025-11-02.

| Tuning fold | Fit on | Score on |
|---:|---|---|
| 1 | 2021-11-27 – 2022-10-15 (323) | 2022-10-17 – 2023-03-15 (150) |
| 2 | 2021-11-27 – 2023-03-14 (473) | 2023-03-16 – 2023-08-12 (150) |
| 3 | 2021-11-27 – 2023-08-11 (623) | 2023-08-13 – 2024-01-09 (150) |
| 4 | 2021-11-27 – 2024-01-08 (773) | 2024-01-10 – 2024-06-07 (150) |
| 5 | 2021-11-27 – 2024-06-06 (923) | 2024-06-08 – 2024-11-07 (153) |
