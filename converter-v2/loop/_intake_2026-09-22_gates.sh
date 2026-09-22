#!/usr/bin/env bash
# ROUND 0d (session 33 Round 3, 2026-09-22) — Phase 3 proofs after the FULL regeneration: run_all_gates.sh, the skeleton state +
# delta vs r422e (0 movers expected, 161 new-only), gatecheck (cs bc then skeleton defect), the ledger record-full, the fast-loop
# baseline + manifest snapshots, selftests, the feature index. reference/tests under WSL: bash ../../outputs/_intake_2026-09-22_gates.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs; T=_intake_2026-09-22
echo "[$(date +%T)] run_all_gates.sh"; bash ./run_all_gates.sh > $O/${T}_gates.log 2>&1; echo "  rc=$?"
grep -nE "^RESULT|SCAFFOLD match \(widgets|pages >=  50|pages >=  75|pages >=  90|pairs skipped|exact wrapper chain|EXTRA container|MISSING container|row wrap|ANY breakdown|EMPTY interactive|OVER-CAPTURE \(|RUNAWAY|CLEAN pages|A_literal_tag_leak  |TOTAL 9557" $O/${T}_gates.log | cut -c1-150
echo "[$(date +%T)] skeleton state + delta vs r422e"
python3 _skeleton_compare.py --json $O/${T}_sk_final.json > $O/${T}_sk_full.log 2>&1; echo "  rc=$?"
python3 $O/_s29_skdelta.py $O/_s33_r422_sk_final.json $O/${T}_sk_final.json --affected $O/${T}_codes.txt > $O/${T}_skdelta.log 2>&1; head -n 8 $O/${T}_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck cs bc, then skeleton defect"
python3 _gatecheck.py cs bc > $O/${T}_gatecheck_csbc.log 2>&1; python3 _gatecheck.py skeleton defect > $O/${T}_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "^  [a-z]|RESULT" $O/${T}_gatecheck.log | head -14
echo "[$(date +%T)] ledger record-full + snapshots"
python3 _ship_ledger.py record-full --round intake-2026-09-22 --build 260619.98 2>&1 | tail -1
python3 _fastloop_snapshot.py > $O/${T}_fastloop_snapshot.log 2>&1; echo "  snapshot rc=$?"; tail -1 $O/${T}_fastloop_snapshot.log
python3 _content_manifest.py snapshot > $O/${T}_manifest_snapshot.log 2>&1; echo "  manifest rc=$?"; tail -1 $O/${T}_manifest_snapshot.log
echo "[$(date +%T)] selftests"
{ python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"; done
} > $O/${T}_selftests.log 2>&1; echo "  PASS/GREEN: $(grep -c 'PASS\|GREEN' $O/${T}_selftests.log)  FAIL: $(grep -c 'FAIL' $O/${T}_selftests.log)"
echo "[$(date +%T)] GATES_DONE"
