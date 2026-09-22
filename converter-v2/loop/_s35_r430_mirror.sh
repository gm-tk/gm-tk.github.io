#!/usr/bin/env bash
# SESSION 35 ROUND 1 (engine r430 — the Inquiry panel opener robustness, part 2) — the loop mirror: README row + the round's artefacts + the
# loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. Run from anywhere (Git Bash or WSL).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s35_r430_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}` / `_s35_r430_{finalise,decomp,pagescore}.py` / `_s35_r430_{gates,scoped_ship,spotcheck_plan,batch_plan,regen_batch_1..2,selftests,index,postship,sk_full,skdelta,gatecheck,decomp,pagescore,verify_carousel,verify_image_carousel}.log` / `_s35_r430_probe_{OFF,ON}_0*.log` / `_s35_r430_{codes,ON_modules,OFF_modules,carousel_family}.txt` / `_s35_r430_sk_final.json` / `_affected_r430.txt` / `_s35_r1_{inqshell,crumbdiff,swallowtab}.log` / `_s35_r1_{crumbdiff,swallowtab,dbg}.py` / `_s35_r1_items_*.log` / `_s35_condense.py` | `CONVERTER_V2/outputs/` | **Round 430 (session 35 Round 1, 2026-09-22) — THE INQUIRY PANEL OPENER ROBUSTNESS, PART 2 (`INQOPENER2_OFF`; §1d exception 1)** + the Round 1 PICK census (the shell census re-run on r429, the crumb diff, the swallowed-opener census, ten item streams): the OFF probe (2699 / 2699 identical) and ON probe (exactly 6 pages / 6 modules, pre-scored), the scoped regeneration + spot-checks, the scoped-ship / decomposition (2 up / 1 down named), the gates (skeleton 54.3617 % @ 2491, +0.0015pp; ≥50 +1; cs exact +18) / 49 selftests / index / miner (196) / the carousel family (301 modules) logs, the finalise script, the session-start condense. |'
ANCHOR='| `_s34_r429_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF '_s35_r430_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _s35_r430_* _s35_r1_* _s35_condense.py _affected_r430.txt 2>/dev/null); do
  [ -f "$O/$f" ] && mkdir -p "$L/$(dirname $f)" && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
