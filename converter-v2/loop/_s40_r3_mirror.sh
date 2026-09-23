#!/usr/bin/env bash
# SESSION 40 ROUND 3 (no engine change — the D13-4 multiChoiceQuiz kickoff, DECLINED on measurement) — the loop mirror:
# README row + the round's instruments + the loop md files into pageforge-site/converter-v2/loop/. Written with the Write tool.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s40_r449_{mcqdiag,mcqwhy}.cjs` / `_s40_r449_mcqdiag_run.sh` / `_s40_r449_{mcqshapes,mcqcross,mcqtables}.py` / `_s40_r449_{mcqshapes,mcqcross,mcqtables}.log` / `_s40_r449_mcqwhy.log` / `_s40_r449_mcq_codes.txt` / `_s40_r3_mirror.sh` | `CONVERTER_V2/outputs/` | **Session 40 Round 3 (2026-09-24) — the D13-4 multiChoiceQuiz kickoff, DECLINED on measurement** — every mcq bundle dumped whole (the 413 JSON lines themselves stay in outputs/), every decline recorded at its own return site (one patched builder copy per process), the answer-signal / announcement / table-layout census: no shape reaches the 20-site floor under the r309 announcement guard; the kickoff moves to typing. |'
ANCHOR='| `_r448_{probe_run,regen,postship,checksums,mirror}.sh`'
if grep -qF '`_s40_r449_{mcqdiag,mcqwhy}.cjs`' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in _s40_r449_mcqdiag.cjs _s40_r449_mcqwhy.cjs _s40_r449_mcqdiag_run.sh _s40_r449_mcqshapes.py _s40_r449_mcqcross.py _s40_r449_mcqtables.py _s40_r449_mcqshapes.log _s40_r449_mcqcross.log _s40_r449_mcqtables.log _s40_r449_mcqwhy.log _s40_r449_mcq_codes.txt _s40_r3_mirror.sh; do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
