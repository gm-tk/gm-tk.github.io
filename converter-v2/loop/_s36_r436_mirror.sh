#!/usr/bin/env bash
# SESSION 36 ROUND 4 (engine r436 — the lesson continuation page inherits its lesson menu) — the loop mirror: README row + the round's artefacts
# + the loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s36_r436_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}` / `_s36_r436_{finalise,pagescore}.py` / `_s36_r436_{gates,scoped_ship,fastloop_accept,offregen,onregen,cs_off,selftests,index,postship,sk_full,skdelta,gatecheck,gatecheck_csbc,spotcheck_plan,batch_plan,regen_batch_1..3}.log` / `_s36_r436_probe_{OFF,ON}_0*.log` / `_s36_r436_{codes,ON_modules,OFF_modules}.txt` / `_s36_r436_{sk_final,onscore,cs_before,cs_after}.json` / `_affected_r436.txt` / `_s36_r4_{bodylead,bodylead2,dips}.{py,log}` | `CONVERTER_V2/outputs/` | **Round 435 (session 36 Round 3, 2026-09-23) — THE LESSON CONTINUATION PAGE INHERITS ITS LESSON MENU (`CONTMENU_OFF`; KB 01B; the corpus at 0.66 / 0.77) + the DECLINED repeated-module-overview class**: the corpus-wide placement census and its page-count refinement, the OFF probe (2699 / 2699 identical) and ON probe (17 modules / 47 pages, 37 up / 4 down — it caught the XDLS901 lead-less case), the dip decomposition, the scoped regeneration + spot-checks, the scoped ship and the named acceptance of compare_structure missing +1 (MXS1004 OFF/ON A/B of compare_structure.py), the gates / 49 selftests / index / miner (197) logs, the finalise script. |'
ANCHOR='| `_s36_r435_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF "_s36_r436_{finalise" $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls _s36_r436_* _s36_r4_* _affected_r436.txt 2>/dev/null); do
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
