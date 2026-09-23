#!/usr/bin/env bash
# SESSION 40 ROUND 12 (no engine change — the ledger's FULL backstop) + THE SESSION-40 STOP (§4 BUDGET) — the loop mirror: README row +
# the round's scripts / logs + the loop md files + COVERAGE_DASHBOARD.md + the gate tooling copies (the ledger + manifest tools included)
# + the command copies. The r452 pattern (written with the Write tool). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s40_r12_{fullship_par,postship,mirror}.sh` / `_s40_r12_fullship_run.sh` / `_s40_stop_state.py` / `_s40_stop_condense.py` / `_s40_r12_{fullship,fullship_regen,postship,gates,sk_full,skdelta,gatecheck,gatecheck_csbc,fastloop_snapshot,manifest_snapshot,selftests,index}.log` / `_s40_r12_sk_final.json` / `_affected_s40_r12.txt` / `_diff_miner_s40_r12.log` | `CONVERTER_V2/outputs/` | **Session 40 Round 12 (2026-09-24) — THE LEDGER'"'"'S FULL-SHIP BACKSTOP (no engine change) + the session-40 STOP (§4 BUDGET, 12 of 12 rounds)** — the full regeneration of all 545 with the r452 engine (42 batches, 542 / 542 byte-identical), the post-ship suite (every gate EXACT; ledger record-full → scoped #0; fast-loop + manifest snapshots), the STOPPED record + the §5d condense #6, the checksums and this mirror. |'
ANCHOR='| `_s40_r11_{trace,stockcap}.cjs`'
if grep -qF '`_s40_r12_{fullship_par,postship,mirror}.sh`' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _s40_r12_* _s40_stop_* _affected_s40_r12.txt _diff_miner_s40_r12.log 2>/dev/null); do
  case "$f" in _s40_r12_batch_*) continue;; esac
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cp "$f" "$L/$f"; n=$((n+1)); done
cp "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md"; n=$((n+1))
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md" || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
