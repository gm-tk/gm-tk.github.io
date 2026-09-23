#!/usr/bin/env bash
# ROUND 439 (session 39 Round 1 — the claude-audit Phase 2 writeFont round, finished under the crashed-round rule) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r436 pattern. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r439_{postship,offproof,checksums,mirror}.sh` / `_r439_{gates,gates_extra,scoped_ship,spotcheck_plan,postship,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,offproof_regen_off,offproof_regen_on}.log` / `_r439_sk_final.json` / `_affected_r439.txt` / `_s39_condense.py` / `_diff_miner_r439.log` | `CONVERTER_V2/outputs/` | **Round 439 (Chris'"'"'s claude-audit kickoff Phase 2, built and scoped-shipped by a Cowork session outside the loop; FINISHED by session 39 Round 1 under the crashed-round rule, 2026-09-23) — THE WRITING FONT IS `writeFont` (`WRITEFONT_OFF`; KB CL-0109 / constraint 93)**: the Cowork session'"'"'s scoped ship + spot-check + its cut-off post-ship; session 39'"'"'s toggle-OFF proof (OFF = ON with the class swapped on every page, ON deterministic), the complete gate run, the gatecheck (declined after a scoped ship, as at r430–r436), the miner (196), the feature index, the checksum refresh and this mirror; plus the session-39 §5d condense script. |'
ANCHOR='| `_s36_r436_{probe,probe_run,regen,postship,checksums,mirror}.{cjs,sh}`'
if grep -qF '`_r439_{postship,offproof' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls _r439_* _s39_* _affected_r439.txt _diff_miner_r439.log 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
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
