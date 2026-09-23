#!/usr/bin/env bash
# SESSION 40 ROUND 5 (no engine change — the claude-audit Phase 3 [RHS alert] family, DECLINED on measurement) — the loop mirror.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_rhsalert_measure.py` / `.log` / `.json` / `_s40_r5_{alerttitle,istockbtn}.py` / `.log` / `_s40_r5_mirror.sh` / `DECISIONS__Pending_2026-09-24.md` | `CONVERTER_V2/outputs/` + the folder root | **Session 40 Round 5 (2026-09-24) — the claude-audit Phase 3 `[RHS alert]` family, MEASURED and DECLINED** (no shape ≥ 0.60 — side column 0.58 together, Standard 0.62; the shares for Chris), plus the two r447 follow-ups measured below floor (the r61 alert-title misses; the iStock-URL buttons). |'
ANCHOR='| `_r449_{probe_run,regen,postship,checksums,mirror}.sh`'
if grep -qF '`_rhsalert_measure.py`' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in _rhsalert_measure.py _rhsalert_measure.log _rhsalert_measure.json _s40_r5_alerttitle.py _s40_r5_alerttitle.log _s40_r5_istockbtn.py _s40_r5_istockbtn.log _s40_r5_mirror.sh; do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
cp DECISIONS__Pending_2026-09-24.md "$L/DECISIONS__Pending_2026-09-24.md"; n=$((n+1))
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
