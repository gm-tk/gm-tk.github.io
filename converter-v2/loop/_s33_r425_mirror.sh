#!/usr/bin/env bash
# SESSION 33 ROUND 1 (engine r425 FINISHED) — the loop mirror: README row + the round's artefacts + the loop md files + the
# gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s33_r425_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s33_r425_{probe,b5vs7,bcdelta,finalise,finalise2,state}.{cjs,py}` / `_s33_r425_{probe_run,regen,fullship_par,postship,checksums,mirror}.sh` / `_s33_r425_{build6,build7,gates,gatecheck,scoped_ship,fastloop,fastloop_named,spotcheck_plan,batch_plan,regen_batch_1..2,fullship_regen,fastloop_snapshot,manifest_snapshot,selftests,index,postship,sk_final,skdelta}.log` / `_s33_r425_probe_{OFF,ON}_0*.log` / `_s33_r425_{codes,ON_modules,OFF_modules}.txt` / `_s33_r425_sk_final.json` / `_s33_r425_sk12_build7.json` / `_s33_r425_g04_worst.txt` / `_ceiling_r425.{json,md,log}` / `_diff_miner_s33_r425.log` / `_diff_queue_pre_r425.md` | `CONVERTER_V2/outputs/` | **Round 425 FINISHED (session 33 Round 1, 2026-09-22) — THE XOTP ACTIVITY-TABLE ADAPTER ENABLED + the "I can" success-criteria list; THE FULL-REGENERATION BACKSTOP**: the 12 rebuilt byte-identical to the parked build 5, the I-can list (12 pages up / 0 down, +36.5pp-sum), the A/B probe over all 507 modules (OFF = disk 2559 / 2559 with the 12 refused; ON = 2583 / 2583), the scoped ship (containment 12 ⊆ 12, the named body_compare +3), the FULL regeneration (39 batches, 0 stale, manifest byte-identical; ledger counter 0), the gates (skeleton 54.2320 % @ 2377 pairs, 0 movers) / 17 selftests / index / miner (184) logs, the re-measured ceiling (90.9 % → 59.7 % of achievable) and the r425 skeleton state. |'
ANCHOR='| `_s31_r425_{menu,menu2,questions,lead,family,titleflag,csline,goldcensus}.py`'
if grep -qF '_s33_r425_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _s33_r425_* _ceiling_r425.json _ceiling_r425.md _ceiling_r425.log _diff_miner_s33_r425.log _diff_queue_pre_r425.md _affected_r425.txt 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp "$f" "$L/$f" || echo "MIRROR DIFFERS: $f"; done
cmp CONVERTER_V2/reference/tests/gate_baseline.json $L/gate_baseline.json && cmp .claude/skills/loop-start/SKILL.md $L/_skills/loop-start.SKILL.md && echo "mirror byte-identical (cmp)"
