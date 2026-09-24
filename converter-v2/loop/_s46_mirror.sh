#!/usr/bin/env bash
# SESSION 46 — mirror the loop artefacts + one round's tools / logs into pageforge-site/converter-v2/loop/ and prove each copy
# byte-identical (cmp); append the round's README row once. Usage (Git Bash or WSL): bash _s46_mirror.sh <TAG> <ROWFILE> [EXTRA outputs/ files…]
#   TAG e.g. r491 — mirrors outputs/_TAG_* files (not dirs), outputs/_affected_TAG.txt, plus the EXTRA names given (relative to outputs/).
set -u
TAG="$1"; ROWF="$2"; shift 2
[ -n "$ROWF" ] && [ -f "$ROWF" ] && ROWF="$(cd "$(dirname "$ROWF")" && pwd)/$(basename "$ROWF")"   # resolve before the cd
cd "$(dirname "$0")/../.." || exit 1          # FINAL_MODULE_DATA
LOOP=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
files=(LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md
       $O/COVERAGE_DASHBOARD.md CONVERTER_V2/reference/tests/gate_baseline.json)
for f in $O/_${TAG}_* $O/_affected_${TAG}.txt; do [ -f "$f" ] && files+=("$f"); done
for x in "$@"; do [ -f "$O/$x" ] && files+=("$O/$x") || echo "MISSING extra: $x"; done
bad=0
for f in "${files[@]}"; do
	cp "$f" "$LOOP/$(basename "$f")" && cmp -s "$f" "$LOOP/$(basename "$f")" || { echo "CMP FAIL $f"; bad=1; }
done
if [ -n "$ROWF" ] && [ -f "$ROWF" ]; then
	row=$(head -1 "$ROWF")
	grep -qF "$row" $LOOP/README.md || { printf '%s\n' "$row" >> $LOOP/README.md; echo "README row appended"; }
fi
echo "mirrored ${#files[@]} files; cmp failures: $bad"
exit $bad
