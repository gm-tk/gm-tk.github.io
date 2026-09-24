#!/usr/bin/env bash
# SESSION 41 /loop-stop — the loop mirror: README row + the declined / unfinished rounds' artefacts (r462, r463, r464) + the
# session's late probes + the loop md files + the gate tooling copies + the command copies into pageforge-site/converter-v2/loop/.
# The r451 pattern (written with the Write tool — never derived by sed). Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_r462_{pick,prescore,companion}.py` + `_r462_{probe_run}.sh` + `_r462_declined.patch` + `_r462_{BB_pre.js,ET_pre.json}` / `_r463_{prescore,companion}.py` + `_r463_probe_run.sh` + `_r463_declined.patch` / `_r462_decline_r463_pick.py` / `_r463_decline_r464_pick.py` / `_r464_{prescore,companion}.py` + `_r464_probe_run.sh` + `_r464_wip.patch` / `_s41_r10_{boxhead,boxtitle,boxtitle2,outh}.py` + logs / `_s41_r12_crosspair.py` + log / `_s41_condense3.py` / `_s41_stop.py` / this mirror + their `.log`s | `CONVERTER_V2/outputs/` | **Session 41 Rounds 10–12 + the stop (2026-09-24)** — r462 (the audio-image unit in place) DECLINED (pp-sum −5.1); r463 (the WJFUN tile "Year N" learning leads) DECLINED on the floor (1 page); r464 (the untagged `Merge item N` line) BUILT, NOT SHIPPED — data flag OFF, its two files uncommitted (`_r464_wip.patch`); the activity-box title census, the crossed-pairs census, the §5d condense #3 and the `/loop-stop` state write. |'
ANCHOR='| `_r461_{probe_run,regen'
if grep -qF '`_r462_{pick,prescore,companion}' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in $(cd $O && ls -d _r462_* _r463_* _r464_* _s41_r10_* _s41_r12_* _s41_condense3.py _s41_stop.py _s41_stop_mirror.sh 2>/dev/null); do
  case "$f" in _r46[234]_on|_r46[234]_codes_0*) continue;; esac
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
