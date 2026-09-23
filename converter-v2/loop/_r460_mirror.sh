#!/usr/bin/env bash
# ROUND 460 (session 41 Round 8 — KB c67 the Knowledge / Practices overview tabs, KPTABS_OFF; THE FULL BACKSTOP) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r451 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r460_{probe_run,fullship_par,fullship_run,postship,checksums,mirror}.sh` / `_r460_{pick,prescore,rawmenu,menudiff,finalise,state}.py` / `_s41_r8_{lost,overcap,kptabs,kppop,kppane}.py` + their `.log` / `_r460_{fullship_regen,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,fastloop_snapshot,manifest_snapshot,probe_SAVE,prescore,rawmenu}.log` / `_r460_probe_{OFF,ON}_0*.log` / `_r460_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules,changed19}.txt` / `_r460_sk_final.json` / `_affected_r460.txt` / `_diff_miner_r460.log` | `CONVERTER_V2/outputs/` | **Round 460 (session 41 Round 8, 2026-09-24) — KNOWLEDGE / PRACTICES ARE THEIR OWN OVERVIEW TABS (KB c67 / CL-0040, `KPTABS_OFF`) — THE FULL BACKSTOP** — the dropped-content census (3.0 % of WT∩gold text on no Claude page), the over-capture tally, the K / P tab population + pane census, the OFF / ON probe (28 pages / 19 modules), the menu-only evidence (20 up / 7 down; the skeleton SCAFFOLD collapses the menu to one WIDGET), the FULL regeneration (42 batches, 523 unaffected byte-identical), the post-ship gates (all EXACT) / selftests (50) / index / miner (197 @ 2524), the finalise scripts, the checksums and this mirror. |'
ANCHOR='| `_r459_{probe_run,regen'
if grep -qF '`_r460_{probe_run,fullship_par' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r460_* _s41_r8_* 2>/dev/null); do
  case "$f" in _r460_on|_r460_batch_*) continue;; esac
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cp "$f" "$L/$f"; n=$((n+1)); done
cp "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md"; n=$((n+1))
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md" || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
