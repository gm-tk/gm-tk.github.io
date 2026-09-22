#!/usr/bin/env bash
# SESSION 34 ROUND 2 (engine r428 — the Inquiry-template fallback shell) — the loop mirror: README row + the round's artefacts + the
# loop md files + the gate tooling copies (gate_baseline.json, run_all_gates.sh, _corpus.py + the three tools this round corrected:
# _scoped_spotcheck.py, _fastloop_diff.py, _ship_ledger.py) + the command copies into pageforge-site/converter-v2/loop/.
# Run from anywhere (Git Bash or WSL): bash CONVERTER_V2/outputs/_s34_r428_mirror.sh
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s34_r428_{probe,shellprobe}.cjs` / `_s34_r428_{finalise,decomp,ledger_fix}.py` / `_s34_r428_{probe_run,regen,postship,checksums,mirror}.sh` / `_s34_r428_{gates,scoped_ship,spotcheck_plan,batch_plan,regen_batch_1..4,selftests,index,postship,sk_full,skdelta,gatecheck,decomp}.log` / `_s34_r428_probe_{OFF,ON}_0*.log` / `_s34_r428_{codes,ON_modules,OFF_modules}.txt` / `_s34_r428_sk_final.json` / `_affected_r428.txt` / `_s34_r2_{img6,inqshell,inqdialects}.{py,log}` / `_s34_r2_items.cjs` / `_s34_condense.py` / `_ship_ledger.pre-r428fix.json` | `CONVERTER_V2/outputs/` | **Round 428 (session 34 Round 2, 2026-09-22) — THE INQUIRY-TEMPLATE FALLBACK SHELL (`inquiry_tabs.template_fallback`, `INQFALLBACK_OFF`)**: the PICK-pass censuses (the half-column image declined; the inquiry shell completeness census 72 gold pages / 40 missing; the dialect census), the in-memory shell probe, the OFF probe (2699 / 2699 identical) and ON probe (exactly 17 pages / 17 modules) over all 545, the scoped regeneration + spot-checks, the scoped-ship / per-module decomposition (17 up / 0 down, +513.6pp-sum), the gates (skeleton 54.3468 % @ 2491, +0.2062pp) / 49 selftests / index / miner (196) logs, the finalise script, the ledger correction. |'
ANCHOR='| `_s33_r427_{probe,patch_sar,finalise}.{cjs,py}`'
if grep -qF '_s34_r428_finalise' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
n=0
for f in $(cd $O && ls _s34_r428_* _s34_r2_*.py _s34_r2_*.log _s34_r2_items.cjs _s34_condense.py _affected_r428.txt _ship_ledger.pre-r428fix.json 2>/dev/null); do
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
