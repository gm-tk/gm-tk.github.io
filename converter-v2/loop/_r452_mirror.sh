#!/usr/bin/env bash
# ROUND 452 (session 40 Round 9 — a writer instruction that mentions a button is not a journal button, JDEFGUARD_OFF) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r451 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r452_{probe_run,regen,postship,checksums,mirror}.sh` / `_r452_{prescore,state_edit}.py` / `_s40_r9_journalbtn.py` / `_s40_r9_jdefault.cjs` / `_s40_r9_jdefault_run.sh` / `_s40_r9_edit.cjs` / `_r452_{scoped_ship,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,spotcheck_plan,probe_SAVE,prescore,regen}.log` / `_s40_r9_{journalbtn,jdefault}.log` / `_s40_r9_jdefault_0*.log` / `_s40_r9_jd_journal.tsv` / `_r452_probe_{OFF,ON}_0*.log` / `_r452_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules,regen_codes}.txt` / `_s40_r9_codes.txt` / `_r452_sk_final.json` / `_affected_r452.txt` / `_diff_miner_r452.log` | `CONVERTER_V2/outputs/` | **Round 452 (session 40 Round 9, 2026-09-24) — A WRITER INSTRUCTION THAT MENTIONS A BUTTON IS NOT A JOURNAL BUTTON (Chris'"'"'s D13-5, `JDEFGUARD_OFF`)** — the journal-button placement census (0 inside bundles; 170 pure-label green buttons free / in activities), the journal-default recorder (a patched ContentConverter copy: 178 shipped defaults, 117 "Go to your journal"), the OFF / ON probe (3208 / 3208; 43 files / 29 modules), the pre-score (35 up / 5 down), the scoped regeneration + spot-check, the scoped ship (+0.0077pp, ≥50 +2), the post-ship gates / selftests (50) / index / miner (195), the LOOP_STATE edits + the §5d archive move, the checksums and this mirror. |'
ANCHOR='| `_r451_{probe_run,regen'
if grep -qF '`_r452_{probe_run,regen' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r452_* _s40_r9_* _affected_r452.txt _diff_miner_r452.log 2>/dev/null); do
  case "$f" in _s40_r9_CC_patched_*) continue;; esac
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
