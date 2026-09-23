#!/usr/bin/env bash
# ROUND 453 (session 41 Round 1 — the table-cell title bar + the MTK overview-table tabs, TABLETB_OFF / REOOVTABS_OFF) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r451 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r453_{probe_run,regen,postship,checksums,mirror}.sh` / `_r453_{prescore,popsplit,split,raw,baseline_edit,state_edit}.py` / `_s41_condense.py` / `_s41_lossfam.py` / `_s41_r1_{undersplit,unpaired}.py` / `_s41_r1_{split,items,trim,blocks,openers,tbgap,where,rows,tabcensus}.cjs` / `_s41_r1_{undersplit,unpaired,trim,tbgap,tabcensus,openers_all}.log` / `_r453_{scopedship_dry,scopedship_dry2,scopedship_dry3,fastloop_named,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,spotcheck_plan,probe_SAVE,prescore,prescore2,prescore3,prescore4,split,split2,split3,popsplit,offsave}.log` / `_r453_probe_{OFF,ON,OVOFF}_0*.log` / `_r453_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules,changed13,regen_codes}.txt` / `_r453_sk_final.json` / `_affected_r453.txt` / `_diff_miner_r453.log` | `CONVERTER_V2/outputs/` | **Round 453 (session 41 Round 1, 2026-09-24) — THE TABLE-CELL TITLE BAR OPENS THE DOCUMENT + THE MTK OVERVIEW-TABLE TABS (KB 07A §4 / 07D §19.1, `TABLETB_OFF` / `REOOVTABS_OFF`)** — the family loss ledger (TRR1 38.3 %), the under-split / unpaired-gold census (353 unpaired, mostly duplicate gold copies), the TRR116 item-stream trace (138 blocks → 63), the opener census over 529 WTs (TRR / PNR only), the trimmed-gap census + its gold location (0.43–0.90 of each table on `0.0`), the WT-table × gold-tab census, the OFF / ON probe (3208 / 3208; the 13), four pre-scores (the opener alone −0.179pp → with the tabs composer → the untagged role → the introduction unfold), the scoped regeneration + spot-check, the §1e population split (pre-existing +0.0211pp), the named fast-loop commit, the post-ship gates / selftests (50) / index / miner (195 @ 2487), the gate-baseline and LOOP_STATE edits, the checksums and this mirror. |'
ANCHOR='| `_r452_{probe_run,regen'
if grep -qF '`_r453_{probe_run,regen' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r453_* _s41_* _affected_r453.txt _diff_miner_r453.log 2>/dev/null); do
  case "$f" in _r453_on|_r453_offsave) continue;; esac
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
