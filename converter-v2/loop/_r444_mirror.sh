#!/usr/bin/env bash
# ROUND 444 (session 39 Round 6 — D13-7, the activity numbers + the FULL backstop) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r436 pattern. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r444_{probe_run,fullship_par,fullship_run,postship,checksums,mirror}.sh` / `_r444v2_probe_run.sh` / `_r444_prescore.py` / `_r444v2_prescore.py` / `_r444_{prescore,fullship,fullship_regen,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,fastloop_snapshot,manifest_snapshot}.log` / `_r444v2_prescore.log` / `_r444_probe_{OFF,ON,SAVE}*.log` / `_r444_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules}.txt` / `_r444_sk_final.json` / `_affected_r444.txt` / `_diff_miner_r444.log` / `_s39_condense3.py` | `CONVERTER_V2/outputs/` | **Round 444 (session 39 Round 6, 2026-09-23) — THE ACTIVITY NUMBERS FULLY CONSECUTIVE (D13-7, r369 ON, `NUMNORM_OFF`) + THE FULL-REGENERATION BACKSTOP** — the OFF / ON probe (2666 / 2666 identical; ON 297 pages / 142 modules), the pre-score naming every mover, the rejected letters-only variant (v2), the 42-batch full regeneration, the post-ship gates / gatecheck / ledger record-full / snapshots / selftests / index / miner (197), the checksums and this mirror. The per-batch scripts and logs (_r444_batch_*) stay in outputs/ only. |'
ANCHOR='| `_r443_{probe_run,regen,postship,checksums,mirror}.sh`'
if grep -qF '`_r444_{probe_run,fullship_par' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r444_[a-z]* _r444v2_* _s39_condense3.py _affected_r444.txt _diff_miner_r444.log | grep -v "_r444_batch_" 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
