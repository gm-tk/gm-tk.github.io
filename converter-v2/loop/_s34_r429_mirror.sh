#!/usr/bin/env bash
# SESSION 34 ROUND 2 (engine r428 — the Inquiry-template fallback shell) — the loop mirror: README row + the round's artefacts + the
# loop md files + the gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py + the three tools this round corrected:
# _scoped_spotcheck.py, _fastloop_diff.py, _ship_ledger.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s34_r429_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s34_r429_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}` / `_s34_r429_{finalise,decomp}.py` / `_s34_r429_pre/Style_Anchor_Registry.json` / `_s34_r429_{gates,scoped_ship,spotcheck_plan,batch_plan,regen_batch_1..3,selftests,index,postship,sk_full,skdelta,gatecheck,decomp}.log` / `_s34_r429_probe_{OFF,ON}_0*.log` / `_s34_r429_{codes,ON_modules,OFF_modules}.txt` / `_s34_r429_sk_final.json` / `_affected_r429.txt` / `_s34_r3_{dashboard_run.sh,ledger.out,imgrow.py,imgrow.log}` / `_s34_r3r4_pick.md` | `CONVERTER_V2/outputs/` | **Round 429 (session 34 Round 4, 2026-09-22) — THE r100 INQUIRY MODE’S OPENER ROBUSTNESS + the TWHR9 row (`INQCONSUMED_OFF` / `INQEMPTYINTRO_OFF`; §1d exception 1)** + the Round 3 PICK pass (the dashboard rebuilt on r428, the loss ledger, the image row): the pre-round registry, the OFF probe (2699 / 2699 identical) and ON probe (exactly 11 pages / 11 modules), the scoped regeneration + spot-checks, the scoped-ship / decomposition (6 up / 1 down named), the gates (skeleton 54.3603 % @ 2491, +0.0135pp) / 49 selftests / index / miner (196) logs, the finalise script. |'
ANCHOR='| `_s34_r428_{probe,shellprobe}.cjs`'
if grep -qF '_s34_r429_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _s34_r429_* _s34_r429_pre/Style_Anchor_Registry.json _s34_r3_*.py _s34_r3_*.log _s34_r3_*.sh _s34_r3_*.out _s34_r3r4_pick.md _affected_r429.txt 2>/dev/null); do
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
