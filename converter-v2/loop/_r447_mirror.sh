#!/usr/bin/env bash
# ROUND 447 (session 40 Round 1 — D13-5, the journal button) — the loop mirror:
# README row + the round's artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/. The r445 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r447_{probe_run,regen,postship,checksums,mirror}.sh` / `_r447_{prescore,wordloss,moverform,companion,pairdelta,decompose,sk_dump}.py` / `_s40_r447_journal_census.py` / `_s40_r447_itemdiag.cjs` / `_r447_{prescore,wordloss,moverform,companion,decompose,scoped_ship,fastloop_named,postship,gates,sk_full,skdelta,selftests,index,gatecheck,gatecheck_csbc,spotcheck_plan,probe_SAVE,ON_diffs}.log` / `_s40_r447_{journal_census,itemdiag}.log` / `_r447_probe_{OFF,ON}_0*.log` / `_r447_{codes,OFF_pages,ON_pages,OFF_modules,ON_modules,regen_codes}.txt` / `_r447_sk_final.json` / `_affected_r447.txt` / `_diff_miner_r447.log` / `_s40_miner.log` | `CONVERTER_V2/outputs/` | **Round 447 (session 40 Round 1, 2026-09-24) — THE JOURNAL BUTTON (D13-5, `JOURNALVAR_OFF`)** — the widened census and the engine item diag, the OFF / ON probe (three in-round repairs), the word-loss check, the pre-score and its split by the gold'"'"'s journal form, the companion numbers, the scoped regeneration + spot-check, the named-mover commit and its decomposition (the PWY1002 pair, the HES1005 re-pair), the post-ship gates / selftests / index / miner (195), the checksums and this mirror. |'
ANCHOR='| `_r446_{probe_run,regen,checksums,mirror}.sh`'
if grep -qF '`_r447_{probe_run,regen' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r447_* _s40_r447_* _affected_r447.txt _diff_miner_r447.log _s40_miner.log 2>/dev/null); do
  [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
done
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
