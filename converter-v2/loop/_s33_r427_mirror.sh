#!/usr/bin/env bash
# SESSION 33 ROUND 5 / SESSION 34 ROUND 1 (engine r427) — the loop mirror: README row + the round's artefacts + the loop md files + the
# gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s33_r427_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s33_r427_{probe,patch_sar,finalise}.{cjs,py}` / `_s33_r427_{probe_run,regen,postship,checksums,mirror}.sh` / `_s33_r427_pre/Style_Anchor_Registry.json` / `_s33_r427_{gates,scoped_ship,fastloop,spotcheck_plan,batch_plan,regen_batch_1..4,selftests,index,postship,sk_full,skdelta,gatecheck}.log` / `_s33_r427_probe_{OFF,ON}_0*.log` / `_s33_r427_{codes,ON_modules,OFF_modules}.txt` / `_s33_r427_sk_final.json` / `_affected_r427.txt` / `_s33_r5_labelled_openers.{py,log}` | `CONVERTER_V2/outputs/` | **Round 427 (session 33 Round 5, crashed after its post-ship suite; finished by session 34 Round 1, 2026-09-22) — THE CODE-PREFIX CHIP DELTAS (`prefix_deltas`, the sixth Style-Anchor cascade tier; BLL14 / 15 / 16 decimal, BLL26 / 27 padded; `PREFIXDELTA_OFF`)**: the patch script, the OFF probe (2699 / 2699 identical) and ON probe (exactly 67 pages / 33 modules) over all 545, the scoped regeneration + 12 spot-checks, the scoped-ship / decomposition (every gate HELD exact), the gates (skeleton 54.1406 % @ 2491, 0 movers) / 49 selftests / index / miner (196, the four chip facts −60 pages) logs, the finalise script; the `[Tab N]` labelled-opener census (3 modules — declined). |'
ANCHOR='| `_s33_r426_{probe,patch_sar,finalise}.{cjs,py}`'
if grep -qF '_s33_r427_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
mkdir -p $L/_s33_r427_pre; cp $O/_s33_r427_pre/Style_Anchor_Registry.json $L/_s33_r427_pre/; for f in $(cd $O && ls _s33_r427_* _s33_r5_labelled_openers.py _s33_r5_labelled_openers.log _affected_r427.txt 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
