#!/usr/bin/env bash
# SESSION 33 ROUND 2 (engine r422 ENABLED) — the loop mirror: README row + the round's artefacts + the loop md files + the
# gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s33_r422_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s33_r422_probe.cjs` / `_s33_r422_{probe_run,regen,postship,mirror}.sh` / `_s33_r422_finalise.py` / `_s33_r422_{gates,scoped_ship,fastloop,spotcheck_plan,batch_plan,regen_batch_1..2,selftests,index,postship,sk_full,skdelta,gatecheck}.log` / `_s33_r422_probe_{OFF,ON}_0*.log` / `_s33_r422_{codes,ON_modules,OFF_modules}.txt` / `_s33_r422_sk_final.json` / `_diff_miner_s33_r422.log` / `_diff_queue_pre_r422.md` / `_affected_r422.txt` | `CONVERTER_V2/outputs/` | **Round 422 ENABLED (session 33 Round 2, 2026-09-22) — THE SIDE-TAB-NAVIGATION FUNDAMENTALS DIALECT GOES LIVE on FRFUN06** (LOOP §1d exception 1 / D12-1): the A/B probe over all 507 modules (OFF = disk 2583 / 2583; ON = the 10 FRFUN06 pages alone), the scoped regeneration of the 1 + 12 spot-checks, the exact decomposition (8 up / 2 down, +34.7pp-sum, 0 movers outside the set), the gates / 17 selftests / index / miner (184) logs and the r422e skeleton state (54.2466 % @ 2377). |'
ANCHOR='| `_s33_r425_{probe,b5vs7,bcdelta,finalise,finalise2,state}.{cjs,py}`'
if grep -qF '_s33_r422_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _s33_r422_* _diff_miner_s33_r422.log _diff_queue_pre_r422.md _affected_r422.txt 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp "$f" "$L/$f" || echo "MIRROR DIFFERS: $f"; done
cmp CONVERTER_V2/reference/tests/gate_baseline.json $L/gate_baseline.json && cmp .claude/skills/loop-start/SKILL.md $L/_skills/loop-start.SKILL.md && echo "mirror byte-identical (cmp)"
