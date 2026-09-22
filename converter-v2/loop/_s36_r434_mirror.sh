#!/usr/bin/env bash
# SESSION 36 ROUND 2 (engine r434 — the ARFUN phase-tile labels + the title-bar payload ownership) — the loop mirror: README row + the round's
# artefacts + the loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. Run from anywhere (Git Bash or WSL).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s36_r434_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}` / `_s36_r434_{finalise,pagescore}.py` / `_s36_r434_{gates,scoped_ship,selftests,index,postship,sk_full,skdelta,gatecheck,gatecheck_csbc,spotcheck_plan,batch_plan,regen_batch_1..3}.log` / `_s36_r434_probe_{OFF,ON}_0*.log` / `_s36_r434_{codes,ON_modules,ON_modules_all,OFF_modules}.txt` / `_s36_r434_sk_final.json` / `_s36_r434_onscore.json` / `_affected_r434.txt` / `_s36_r2_{overwhat,headpayload,parse}.{py,cjs,log}` / `_s36_r2_items_*.log` / `_s36_condense{,2}.py` | `CONVERTER_V2/outputs/` | **Round 434 (session 36 Round 2, 2026-09-22) — THE ARFUN PHASE-TILE LABELS + THE TITLE-BAR PAYLOAD OWNERSHIP (`PHASETILELABEL_OFF` / `TITLEPAYLOAD_OFF`; LOOP 1d exception 1)** + the Round 2 PICK pass (the menu-overrun census read by content; the head-matched colon-span measurement, 139 spans / 42 modules): the OFF probe (2699 / 2699 identical — it caught the `HEADPAYLOAD_OFF` name collision with round 303) and ON probe (exactly ARFUN02 / 03 / 05, pre-scored 3 up / 0 down; it caught the ENFUN menu regression twice), the scoped regeneration + spot-checks, the scoped ship (skeleton IMPROVED, >=50 +1, cs exact +33), the gates / 49 selftests / index / miner (198) logs, the finalise script, and the session-36 5d condense scripts. |'
ANCHOR='| `_s36_r433_{probe,probe_run,fullship_par,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF "_s36_r434_{finalise" $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls _s36_r434_* _s36_r2_* _s36_condense.py _s36_condense2.py _affected_r434.txt 2>/dev/null); do
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
