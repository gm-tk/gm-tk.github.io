#!/usr/bin/env bash
# SESSION 36 ROUND 1 (engine r433 — the MXFUN code-content phase dialect + the FULL backstop) — the loop mirror: README row + the round's artefacts + the
# loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. Run from anywhere (Git Bash or WSL).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s36_r433_{probe,probe_run,fullship_par,postship,checksums,mirror}.{cjs,sh}` / `_s36_r433_{finalise,pagescore}.py` / `_s36_r433_{fullship,fullship_regen,gates,selftests,index,postship,sk_full,skdelta,gatecheck,gatecheck_csbc,fastloop_snapshot,manifest_snapshot}.log` / `_s36_r433_probe_{OFF,ON}_0*.log` / `_s36_r433_{codes,ON_modules,OFF_modules}.txt` / `_s36_r433_sk_final.json` / `_s36_r433_onscore.json` / `_affected_r433.txt` / `_s36_r1_{lessonmenu,menuwhat,lomarker,menuover}.{py,log}` / `_s36_r1_items_*.log` | `CONVERTER_V2/outputs/` | **Round 433 (session 36 Round 1, 2026-09-22) — THE MXFUN CODE-CONTENT PHASE DIALECT (`CODEPHASE_OFF`; LOOP 1d exception 1) + THE FULL-REGENERATION BACKSTOP (scoped #7 to 0)** + the Round 1 PICK pass (the lesson-menu residue re-measured and read by content — the HIS lead-in form declined under constraint 70; the menu-overrun census): the OFF probe (2699 / 2699 identical) and ON probe (exactly MXFUN02 + MXFUN03, pre-scored +22.5pp-sum), the full regeneration (42 batches, 0 stale, 540 byte-identical), the gates (skeleton 54.5311 % @ 2491, +0.0090pp; cs exact +56) / 49 selftests / index / miner (198) logs, the finalise script. |'
ANCHOR='| `_s35_r432_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF "_s36_r433_{finalise" $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls _s36_r433_* _s36_r1_* _affected_r433.txt 2>/dev/null); do
  [ -f "$O/$f" ] && mkdir -p "$L/$(dirname $f)" && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
cp CONVERTER_V2/outputs/COVERAGE_DASHBOARD.md $L/COVERAGE_DASHBOARD.md; n=$((n+1))
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s CONVERTER_V2/outputs/COVERAGE_DASHBOARD.md $L/COVERAGE_DASHBOARD.md || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
