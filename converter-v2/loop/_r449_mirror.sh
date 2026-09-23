#!/usr/bin/env bash
# ROUND 449 (session 40 Round 4 — D13-4, the typing quiz shape 1) — the loop mirror:
# README row + the round's artefacts + the NEW verifier + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r448 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r449_{probe_run,regen,postship,checksums,mirror}.sh` / `_r449_{prescore,wordloss,typingwords}.py` / `_s40_quizdump.cjs` / `_s40_quizdump_run.sh` / `_s40_r450_{typingshapes,typingred}.py` / `_s40_r450_typwhy.cjs` / `_s40_r449_dashboard_run.sh` / `_r449_{prescore,typingwords,typing_family,scoped_ship,fastloop_named,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,spotcheck_plan,probe_SAVE,ON_diffs}.log` / `_s40_r450_{typingshapes,typingred,typwhy}.log` / `_r449_probe_{OFF,ON}_0*.log` / `_r449_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules,regen_codes,typing_family}.txt` / `_r449_sk_final.json` / `_affected_r449.txt` / `_diff_miner_r449.log` / `_verify_typing.cjs` (the NEW verifier, reference/tests) | `CONVERTER_V2/outputs/` + `reference/tests/` | **Round 449 (session 40 Round 4, 2026-09-24) — THE TYPING QUIZ, shape 1 (D13-4, `TYPING_OFF`)** — the typing dump and shape census (270 un-built; the red-answer family 26 / 15, 77 % gold-matched), the decline recorder, the OFF / ON probe, the word check, the new verifier (selftest GREEN; the whole 85-module family defect 0), the scoped regeneration + spot-check, the named-mover commit (FRFUN08_3_0), the post-ship gates / selftests (50) / index / miner (195), the dashboard rebuild (no typing row), the checksums and this mirror. |'
ANCHOR='| `_s40_r449_{mcqdiag,mcqwhy}.cjs`'
if grep -qF '`_r449_{probe_run,regen' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r449_* _s40_r450_* _s40_quizdump.cjs _s40_quizdump_run.sh _s40_r449_dashboard_run.sh _affected_r449.txt _diff_miner_r449.log 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
cp "$O/_r448_postship.sh" "$L/_r448_postship.sh"; n=$((n+1))   # its stale miner-tail line fixed at r448
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cp "$f" "$L/$f"; n=$((n+1)); done
cp "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md"; n=$((n+1))
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md" || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
for f in gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
