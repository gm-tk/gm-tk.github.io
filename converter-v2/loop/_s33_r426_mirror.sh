#!/usr/bin/env bash
# SESSION 33 ROUND 4 (data r426) — the loop mirror: README row + the round's artefacts + the loop md files + the
# gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s33_r426_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s33_r426_{probe,patch_sar,finalise}.{cjs,py}` / `_s33_r426_{probe_run,regen,postship,checksums,mirror}.sh` / `_s33_r426_pre/Style_Anchor_Registry.json` / `_s33_r426_{gates,scoped_ship,fastloop_named,spotcheck_plan,batch_plan,regen_batch_1..2,selftests,index,postship,sk_full,skdelta,gatecheck}.log` / `_s33_r426_probe_ON_0*.log` / `_s33_r426_{codes,ON_modules}.txt` / `_s33_r426_sk_final.json` / `_s33_r426_sk8.json` / `_diff_miner_s33_r426.log` / `_diff_queue_pre_r426.md` / `_affected_r426.txt` | `CONVERTER_V2/outputs/` | **Round 426 (session 33 Round 4, 2026-09-22) — THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight over-split golds (Style_Anchor_Registry rows only; the pre-round file is the reversal)**: the patch script, the ON probe over all 545 (exactly the 8), the scoped regeneration + 12 spot-checks, the named decomposition (cs pool +277), the gates (skeleton 54.1406 % @ 2491, 7 up / 1 down) / 17 selftests / index / miner (196) logs. |'
ANCHOR='| `_intake_2026-09-22_{delta,codes,results}.txt`'
if grep -qF '_s33_r426_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
mkdir -p $L/_s33_r426_pre; cp $O/_s33_r426_pre/Style_Anchor_Registry.json $L/_s33_r426_pre/; for f in $(cd $O && ls _s33_r426_* _diff_miner_s33_r426.log _diff_queue_pre_r426.md _affected_r426.txt 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp "$f" "$L/$f" || echo "MIRROR DIFFERS: $f"; done
cmp CONVERTER_V2/reference/tests/gate_baseline.json $L/gate_baseline.json && cmp .claude/skills/loop-start/SKILL.md $L/_skills/loop-start.SKILL.md && echo "mirror byte-identical (cmp)"
