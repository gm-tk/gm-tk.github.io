#!/usr/bin/env bash
# SESSION 42 — the loop mirror, ONE script for every round of the session (the r461 pattern, parametrised):
#   bash CONVERTER_V2/outputs/_s42_mirror.sh <TAG> <ROWFILE> <GLOB>...
# TAG      the README key that proves the row is present (e.g. `_r465_{run` — grep -F)
# ROWFILE  a file in CONVERTER_V2/outputs holding the ONE README table row for this round
# GLOB...  the round's artefacts in CONVERTER_V2/outputs (directories skipped)
# Copies the artefacts + the loop md files + the gate tooling copies + the command copies into
# pageforge-site/converter-v2/loop/ and proves every copy byte-identical (cmp). Run from anywhere (Git Bash or WSL).
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
TAG="$1"; ROWFILE="$2"; shift 2
ANCHOR='| `_r462_{pick,prescore,companion}.py`'
if grep -qF "$TAG" $L/README.md; then echo "README row already present"; else
  ROW=$(cat "$O/$ROWFILE")
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for g in "$@"; do
  for f in $(cd $O && ls -d $g 2>/dev/null); do
    [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1))
  done
done
MD="LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md KB_AMALGAMATION_STATUS.md DECISIONS__Pending_2026-09-24.md"
TOOLS="gate_baseline.json run_all_gates.sh _corpus.py _scoped_spotcheck.py _fastloop_diff.py _ship_ledger.py compare_gold_pages.txt compare_exclusions.txt _discrepancy_audit.py compare_structure.py body_compare.py _verify_typing.cjs _diff_miner.py _skeleton_compare.py"
for f in $MD; do cp "$f" "$L/$f"; n=$((n+1)); done
cp "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md"; n=$((n+1))
for f in $TOOLS; do cp "CONVERTER_V2/reference/tests/$f" "$L/$f"; n=$((n+1)); done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && cp ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" && n=$((n+1)); done
cp .claude/settings.json $L/_settings/settings.json; cp .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh; n=$((n+2))
echo "mirrored $n files"
bad=0
for f in $MD; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
cmp -s "$O/COVERAGE_DASHBOARD.md" "$L/COVERAGE_DASHBOARD.md" || { echo "MIRROR DIFFERS: COVERAGE_DASHBOARD.md"; bad=1; }
for f in $TOOLS; do cmp -s "CONVERTER_V2/reference/tests/$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
for s in loop-start loop-stop loop-review loop-decisions; do [ -f ".claude/skills/$s/SKILL.md" ] && { cmp -s ".claude/skills/$s/SKILL.md" "$L/_skills/$s.SKILL.md" || { echo "MIRROR DIFFERS: $s"; bad=1; }; }; done
cmp -s .claude/settings.json $L/_settings/settings.json || { echo "MIRROR DIFFERS: settings.json"; bad=1; }
cmp -s .claude/hooks/no_native_python.sh $L/_hooks/no_native_python.sh || { echo "MIRROR DIFFERS: hook"; bad=1; }
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
