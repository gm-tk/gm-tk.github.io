#!/usr/bin/env bash
# SESSION 40 ROUND 6 (no engine change — D13-4's remaining quiz types, DECLINED on measurement) — the loop mirror.
# Written with the Write tool (a sed-derived copy broke its own quoting).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s40_r6_ddwhy.cjs` / `_s40_r6_quizsignals.py` / `_s40_r6_ddwhy.log` / `_s40_r6_quizsignals.log` / `_s40_r6_mirror.sh` (the per-type `_s40_<type>.jsonl` dumps stay in outputs/) | `CONVERTER_V2/outputs/` | **Session 40 Round 6 (2026-09-24) — D13-4 remaining quiz types (dropDown / reorder / radioQuiz / selectionBox), DECLINED on measurement** — the largest explicit / announced shape is 10; the unannounced-highlight lever (about 190 boxes) goes to Chris (DECISIONS__Pending_2026-09-24.md section 2, Needs Chris 19). |'
ANCHOR='| `_rhsalert_measure.py`'
if grep -qF '_s40_r6_ddwhy.cjs' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in _s40_r6_ddwhy.cjs _s40_r6_ddwhy.log _s40_r6_quizsignals.py _s40_r6_quizsignals.log _s40_r6_mirror.sh; do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
cp DECISIONS__Pending_2026-09-24.md "$L/DECISIONS__Pending_2026-09-24.md"; n=$((n+1))
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
