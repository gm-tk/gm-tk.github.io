#!/usr/bin/env bash
# SESSION 35 ROUND 2 (engine r431 — the overview menu's inner-word label over-fire) — the loop mirror: README row + the round's artefacts + the
# loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. Run from anywhere (Git Bash or WSL).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s35_r431_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}` / `_s35_r431_{finalise,decomp,pagescore,pairdiff}.py` / `_s35_r431_{gates,scoped_ship,fastloop_accept,spotcheck_plan,batch_plan,regen_batch_1..4,selftests,index,postship,sk_full,skdelta,gatecheck,decomp,pagescore}.log` / `_s35_r431_probe_{OFF,ON}_0*.log` / `_s35_r431_{codes,ON_modules,OFF_modules}.txt` / `_s35_r431_sk_final.json` / `_affected_r431.txt` / `_s35_r2_{menudup,menuover}.{py,log}` | `CONVERTER_V2/outputs/` | **Round 431 (session 35 Round 2, 2026-09-22) — THE OVERVIEW MENU’S INNER-WORD LABEL OVER-FIRE (`MENUWORD_OFF`; the miner’s module-menu rows #48 / #49; the r359 queued class measured)** + the Round 2 PICK census (the menu-region duplication and overrun censuses): the OFF probe (2699 / 2699 identical) and ON probe (exactly 23 pages / 23 modules, pre-scored twice — the first repair 8 up / 18 down, the second 16 up / 3 down), the scoped regeneration + spot-checks, the scoped-ship (missing +3 accepted as named, decomposed), the gates (skeleton 54.4248 % @ 2491, +0.0630pp; ≥50 +3; ≥75 +1) / 49 selftests / index / miner (198) logs, the finalise script. |'
ANCHOR='| `_s35_r430_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF '_s35_r431_{finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls _s35_r431_* _s35_r2_* _affected_r431.txt 2>/dev/null); do
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
