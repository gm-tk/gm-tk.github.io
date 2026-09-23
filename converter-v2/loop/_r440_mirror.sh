#!/usr/bin/env bash
# ROUND 440 (session 39 Round 2 — D13-6, the dual-build golds) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r436 pattern. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r440_{probe_run,regen,postship,checksums,mirror}.sh` / `_r440_probe.cjs` / `_r440_{pairs_probe,prescore,decompose}.py` / `_r440_{pairs_before,prescore,decompose,scoped_ship,fastloop_named,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,spotcheck_plan,batch_plan,regen_batch_1,regen_batch_2}.log` / `_r440_probe_{OFF,ON}_0*.log` / `_r440_{codes,ON_modules,OFF_modules}.txt` / `_r440_sk_final.json` / `_affected_r440.txt` / `_diff_miner_r440.log` / `_r440_pre/Style_Anchor_Registry.json` | `CONVERTER_V2/outputs/` | **Round 440 (session 39 Round 2, 2026-09-23) — THE DUAL-BUILD GOLDS (Chris'"'"'s D13-6; `GOLDPAGES_OFF` for the gate half, the pre-round registry for the engine half)**: the before-pairing census (41 pairs), the OFF / ON in-memory probe (2699 / 2699 identical; ON exactly 3 modules), the pre-score that fired the CEDT301 caveat (45.0 vs 57.7), the scoped regeneration + spot-check, the scoped ship and the per-module decomposition of the four NAMED movers, the post-ship gates / selftests / index / miner (195), the checksums and this mirror. The gate files it changed (`compare_gold_pages.txt` NEW, `_corpus.py`, `_discrepancy_audit.py`, `compare_structure.py`, `body_compare.py`) are mirrored at the loop root. |'
ANCHOR='| `_r439_{postship,offproof,checksums,mirror}.sh`'
if grep -qF '`_r440_{probe_run,regen' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r440_* _affected_r440.txt _diff_miner_r440.log 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
mkdir -p $L/_r440_pre && cp $O/_r440_pre/Style_Anchor_Registry.json $L/_r440_pre/ && n=$((n+1))
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
