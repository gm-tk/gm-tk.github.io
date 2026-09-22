#!/usr/bin/env bash
# ROUND 0d (session 33 Round 3) — the loop mirror: README row + the intake's artefacts + the loop md files + the handovers +
# the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/. bash CONVERTER_V2/outputs/_intake_2026-09-22_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop; O=CONVERTER_V2/outputs
ROW='| `_intake_2026-09-22_{delta,codes,results}.txt` / `_intake_2026-09-22_{convert,fullship_par,gates,instruments,dashboard_run,checksums,mirror}.sh` / `_intake_2026-09-22_{finalise,state}.py` / **`_intake_split.py`** / `_intake_2026-09-22_batch_0{0..3}.log` / `_intake_2026-09-22_{fullship_regen,gates,gates_run,sk_full,skdelta,gatecheck,gatecheck_csbc,fastloop_snapshot,manifest_snapshot,selftests,split,instruments,dashboard,dashboard2,index}.log` / `_intake_2026-09-22_sk_final.json` / `_ceiling_intake_2026-09-22.{json,md,log}` / `_diff_miner__intake_2026-09-22.log` / `_diff_miner__intake_2026-09-22_scoped.log` / `_diff_miner_scoped.{md,json}` / `_diff_queue_pre_intake_2026-09-22.md` | `CONVERTER_V2/outputs/` | **ROUND 0d — the 22 Sept 2026 intake of the 38 pre-intake never-converted modules (session 33 Round 3; LOOP §1f, the first unattended intake)**: the delta list, the four conversion batches (38 / 38, 0 refused), the FULL regeneration on the unchanged registries, the gates, the population split (pre-existing EXACT; the new batch 51.42 %), the re-measured ceiling (91.2 %), the dashboard, the miner full (190) + scoped (11), the re-base and the handovers. |'
ANCHOR='| `_s33_r422_probe.cjs`'
if grep -qF '_intake_2026-09-22_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _intake_2026-09-22_* _intake_split.py _ceiling_intake_2026-09-22.* _diff_miner__intake_2026-09-22*.log _diff_miner_scoped.md _diff_queue_pre_intake_2026-09-22.md 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
cp $O/COVERAGE_DASHBOARD.md $L/COVERAGE_DASHBOARD.md; n=$((n+1))
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md LOOP_INTAKE__2026-09-22_38_Modules.md NEW_MODULES__Intake_2026-09-22.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md LOOP_INTAKE__2026-09-22_38_Modules.md; do cmp "$f" "$L/$f" || echo "MIRROR DIFFERS: $f"; done
cmp CONVERTER_V2/reference/tests/gate_baseline.json $L/gate_baseline.json && echo "mirror byte-identical (cmp)"
