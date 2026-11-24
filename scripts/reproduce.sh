#!/usr/bin/env bash
# Reproduce the INT4096 analysis from scratch.
#
# This script is the single entry point referenced by README.md. It is designed
# to be safe to re-run: it never overwrites an immutable data snapshot, and it
# never releases the sealed test block.
#
# Usage:
#   bash scripts/reproduce.sh              # full pipeline (needs network once)
#   bash scripts/reproduce.sh --offline    # use existing snapshots only
#   bash scripts/reproduce.sh --quick      # smaller tuning budget, for a smoke test
set -euo pipefail

cd "$(dirname "$0")/.."
ROOT="$(pwd)"

OFFLINE=0
QUICK=0
for arg in "$@"; do
  case "$arg" in
    --offline) OFFLINE=1 ;;
    --quick)   QUICK=1 ;;
    *) echo "unknown option: $arg" >&2; exit 2 ;;
  esac
done

if [[ -x .venv/bin/python ]]; then
  PY=.venv/bin/python
elif command -v python3 >/dev/null; then
  PY=python3
else
  echo "No python interpreter found." >&2; exit 1
fi

export PYTHONPATH="$ROOT/src"

echo "== 0. Environment =="
"$PY" --version
"$PY" -c "import numpy, pandas, sklearn, matplotlib; print('numpy', numpy.__version__, '| pandas', pandas.__version__, '| sklearn', sklearn.__version__, '| matplotlib', matplotlib.__version__)"

echo
echo "== 1. Unit tests (temporal integrity first) =="
"$PY" -m pytest tests -q

echo
echo "== 2. Leakage-suite mutation check =="
"$PY" scripts/mutation_check.py

if [[ "$OFFLINE" -eq 0 ]]; then
  echo
  echo "== 3. Immutable data snapshots (skipped if already present) =="
  for asset in AAPL BTC; do
    file="data/raw/$(echo "$asset" | tr '[:upper:]' '[:lower:]')_daily.json"
    if [[ -f "$file" ]]; then
      echo "  $asset snapshot already present: $file (not overwritten)"
    else
      "$PY" -m int4096.data.snapshot --asset "$asset"
    fi
  done
else
  echo
  echo "== 3. Snapshots: offline mode, using existing files =="
fi

echo
echo "== 4. Dataset cards and feature dictionary =="
"$PY" -m int4096.data.cards

echo
echo "== 5. Experiment matrix (validation only; test block stays sealed) =="
TRIALS=10
SECONDS_BUDGET=90
if [[ "$QUICK" -eq 1 ]]; then
  TRIALS=3
  SECONDS_BUDGET=30
  echo "  quick mode: max_trials=$TRIALS max_seconds=$SECONDS_BUDGET"
fi

for asset in AAPL BTC; do
  for model in linear_baseline ridge svr random_forest hist_gradient_boosting; do
    for variant in P0 P2; do
      echo "  -> $asset / $model / $variant"
      "$PY" -m int4096.experiments.run \
        --asset "$asset" --model "$model" --variant "$variant" \
        --max-trials "$TRIALS" --max-seconds "$SECONDS_BUDGET" \
        --human-owner "team" > /dev/null
    done
  done
done

echo
echo "== 6. Figures and registry report =="
"$PY" - <<'PYEOF'
from pathlib import Path
from int4096.config import load_protocol
from int4096.evaluation import figures
from int4096.experiments.run import prepare_dataset

protocol = load_protocol()
frames, splits = {}, {}
for asset in ("AAPL", "BTC"):
    prepared = prepare_dataset(asset, protocol)
    frames[asset] = prepared["frame"]
    splits[asset] = prepared["split"]

registry = figures.load_registry()
print(" ", figures.plot_coverage_and_splits(frames, splits))
print(" ", figures.plot_model_vs_naive(registry))
print(" ", figures.plot_ablation_delta(registry))

run_dirs = sorted((d for d in Path("experiments/models").glob("*/*") if d.is_dir()), key=lambda d: d.name)
print(" ", figures.plot_train_vs_validation(run_dirs))

success = registry[(registry.status == "SUCCESS") & (registry.asset == "AAPL")]
if not success.empty:
    run_id = success.iloc[0]["run_id"]
    print(" ", figures.plot_observed_vs_predicted(run_id))
PYEOF
"$PY" -m int4096.experiments.registry_report
"$PY" scripts/export_splits.py
"$PY" scripts/summarize_models.py

echo
echo "== 7. Audit-fix verification probes =="
"$PY" scripts/verify_fixes.py

echo
echo "Done. Runs: experiments/models/<model>/, figures: experiments/figures"
echo "Registry:  docs/research/run_registry.md · splits: data/splits/ · per-model summaries: experiments/models/*/README.md"
echo "The sealed test block was NOT released by this script."
