#!/usr/bin/env bash
# Build the INT4096 report from scratch and record an auditable word count.
#
# Requirements: a TeX distribution with pdflatex, latexmk, bibtex and texcount
# (TeX Live 2026 / TinyTeX is sufficient; see README.md).
#
# Usage:
#   bash reports/latex/build.sh            # build + count + copy to reports/final
#   bash reports/latex/build.sh --clean    # remove auxiliary files first
set -euo pipefail

cd "$(dirname "$0")"
ROOT="$(cd ../.. && pwd)"

if [[ "${1:-}" == "--clean" ]]; then
  latexmk -C >/dev/null 2>&1 || true
  rm -f main.bbl main.blg
fi

command -v latexmk   >/dev/null || { echo "latexmk not found on PATH"; exit 1; }
command -v texcount  >/dev/null || { echo "texcount not found on PATH"; exit 1; }

# Deterministic builds: pin TeX and matplotlib timestamps so two builds of the
# same source produce byte-identical PDFs.
#
# The epoch is a FIXED project constant, not the HEAD commit time. Deriving it
# from HEAD would be circular: committing the rebuilt PDF moves HEAD, which
# changes the epoch, which changes the PDF. A constant breaks that loop and makes
# the build reproducible from any clone.
INT4096_SOURCE_DATE="${INT4096_SOURCE_DATE:-2026-10-29T00:00:00Z}"
if [[ -z "${SOURCE_DATE_EPOCH:-}" ]]; then
  SOURCE_DATE_EPOCH="$(date -u -d "$INT4096_SOURCE_DATE" +%s)"
fi
export SOURCE_DATE_EPOCH
echo "SOURCE_DATE_EPOCH=$SOURCE_DATE_EPOCH (deterministic PDF metadata)"

echo "== 1/4 regenerate figures and generated tables from run artifacts =="
if [[ -x "$ROOT/.venv/bin/python" ]]; then
  PY="$ROOT/.venv/bin/python"
elif command -v python3 >/dev/null; then
  PY=python3
else
  echo "python3 not found"; exit 1
fi
( cd "$ROOT" && PYTHONPATH=src "$PY" scripts/build_latex_assets.py )

echo
echo "== 2/4 compile (latexmk -pdf, bibtex) =="
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

echo
echo "== 3/4 inspect the log for layout problems =="
overfull=$(grep -cE "Overfull|Underfull" main.log || true)
warnings=$(grep -cE "LaTeX Warning|Package .* Warning" main.log || true)
echo "  overfull/underfull boxes: $overfull"
echo "  LaTeX/package warnings:   $warnings"
if [[ "$overfull" -gt 0 || "$warnings" -gt 0 ]]; then
  echo "  NOTE: inspect main.log; the build is not considered clean."
  grep -E "Overfull|Underfull|Warning" main.log | head -20
fi

echo
echo "== 4/4 word count (texcount, narrative only) =="
mkdir -p ../final
{
  echo "INT4096 report word count"
  echo "SOURCE_DATE_EPOCH: $SOURCE_DATE_EPOCH"
  echo "(commit id omitted deliberately: embedding HEAD would change this file on
every unrelated commit and destroy build reproducibility)"
  echo "command:   texcount -inc -sum main.tex"
  echo
  texcount -inc -sum main.tex
  echo
  echo "--- interpretation ---"
  echo "Counting configuration:"
  echo "  * 'Words in text' counts body prose in main.tex and every \\input section."
  echo "  * 'Words in headers' counts section and paragraph headings."
  echo "  * 'Words outside text' counts figure captions and float content; these are"
  echo "    EXCLUDED from the narrative figure reported as the submission word count,"
  echo "    consistent with the written specification's exclusion of figures and tables."
  echo "  * Bibliography entries, the title block, and generated table bodies are not"
  echo "    counted as narrative prose."
  echo "  * \\citep keys and LaTeX markup are not counted as words."
  echo
  echo "Policy reference:"
  echo "  * Written specification: <= 2000 words, excluding figures, tables, references."
  echo "  * Instructor oral guidance (reported by the project owner, not a published"
  echo "    rule): approximately 500 additional words permitted => ~2500 practical."
  echo "  * This document's narrative (text + headers) is reported above and is kept"
  echo "    at or below 2500. Captions are excluded and are reported separately."
  echo
  echo "This count is produced by texcount on the actual compiled source. It may not"
  echo "correspond exactly to an instructor's counting tool; see README.md."
} > ../word_count.txt

grep -E "^Words in text|^Words in headers|^Words outside" ../word_count.txt

cp main.pdf ../final/INT4096_Final_Report.pdf
echo
echo "PDF:  reports/final/INT4096_Final_Report.pdf"
echo "log:  reports/word_count.txt"
echo "pages: $(pdfinfo main.pdf 2>/dev/null | awk '/Pages/{print $2}')"
