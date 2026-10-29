#!/usr/bin/env bash
# Build the INT4096 presentation deck.
#
# Requirements: pdflatex + latexmk (TeX Live or TinyTeX, with `beamer` and
# `beamerthememetropolis`).
#
# Usage:
#   bash slides/build.sh            # regenerate assets, compile, copy to final
#   bash slides/build.sh --clean    # remove auxiliary files first
set -euo pipefail

cd "$(dirname "$0")/latex"   # main.tex lives here; slides/ is the parent
ROOT="$(cd ../.. && pwd)"

if [[ "${1:-}" == "--clean" ]]; then
  latexmk -C >/dev/null 2>&1 || true
fi

command -v latexmk >/dev/null || { echo "latexmk not found on PATH"; exit 1; }

# Deterministic metadata, same fixed epoch as the report build.
INT4096_SOURCE_DATE="${INT4096_SOURCE_DATE:-2026-10-29T00:00:00Z}"
if [[ -z "${SOURCE_DATE_EPOCH:-}" ]]; then
  SOURCE_DATE_EPOCH="$(date -u -d "$INT4096_SOURCE_DATE" +%s)"
fi
export SOURCE_DATE_EPOCH

echo "== 1/3 regenerate slide figures and number macros from run artifacts =="
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
else
  PY=python3
fi
( cd "$ROOT" && PYTHONPATH=src "$PY" scripts/build_slide_assets.py )

echo
echo "== 2/3 compile =="
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

echo
echo "== 3/3 inspect the log =="
overfull=$(grep -cE "Overfull|Underfull" main.log || true)
missing=$(grep -c "File .* not found" main.log || true)
echo "  overfull/underfull boxes: $overfull"
echo "  missing files:            $missing"
if [[ "$overfull" -gt 0 || "$missing" -gt 0 ]]; then
  echo "  NOTE: inspect main.log before presenting."
  grep -E "Overfull|Underfull|not found" main.log | head -20
fi

mkdir -p ../final
cp main.pdf ../final/INT4096_Presentation.pdf
echo
echo "PDF:   slides/final/INT4096_Presentation.pdf"
echo "pages: $(pdfinfo main.pdf 2>/dev/null | awk '/Pages/{print $2}')"
echo "sha256: $(sha256sum main.pdf | cut -d' ' -f1)"
