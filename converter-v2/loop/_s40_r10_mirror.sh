#!/usr/bin/env bash
# SESSION 40 ROUND 10 (the measurement-tool round — the coverage dashboard gains the D13-4 quiz rows; no engine change) — the loop
# mirror: README row + the round's artefacts (the census tool itself included) + the loop md files + COVERAGE_DASHBOARD.md + the gate
# tooling copies. The r452 pattern (written with the Write tool). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_measure_r271_variations.cjs` (the census, now + the D13-4 quiz types, `CENSUS_QUIZ_OFF`) / `_s40_r10_{dashboard_run,mirror}.sh` / `_s40_r10_{bubbledesc,imgdesc,imgdesc2,state_edit,condense}.py` / `_s40_r10_{imgown,edit}.cjs` / `_s40_r10_imgown_run.sh` / `_s40_r10_{dashboard_run,dashboard,var_OFF_merge,var_ON_merge,dec_merge,bubbledesc,imgdesc,imgdesc2,imgown}.log` / `_s40_r10_codes.txt` | `CONVERTER_V2/outputs/` | **Session 40 Round 10 (2026-09-24) — THE COVERAGE DASHBOARD GAINS THE D13-4 QUIZ ROWS (a measurement-tool round, no engine change)** — the census OFF / ON proof (5732 = ON minus quiz, record for record), the dashboard rebuild (headline coverage re-based 50.8 % → 44.9 %), and the PICK pass before it: the TEDC in-bubble avatar leak (8, below floor), the `[Image] <description>` caption census (177; gold lacks 131) and the r240 own-text recorder (1 site — not the mechanism). |'
ANCHOR='| `_r452_{probe_run,regen'
if grep -qF '`_s40_r10_{dashboard_run,mirror}.sh`' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _s40_r10_* 2>/dev/null); do
  case "$f" in _s40_r10_MB_patched_*|_s40_r10_var_*_shard*|_s40_r10_dec_shard*|_s40_r10_var_OFF.json|_s40_r10_var_ON.json|_s40_r10_imgown_0*) continue;; esac
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
cp "$O/_measure_r271_variations.cjs" "$L/_measure_r271_variations.cjs"; n=$((n+1))
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cp "$f" "$L/$f"; n=$((n+1)); done
cp "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md"; n=$((n+1))
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md" || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
cmp -s "$O/_measure_r271_variations.cjs" "$L/_measure_r271_variations.cjs" || { echo "MIRROR DIFFERS: census"; bad=1; }
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
