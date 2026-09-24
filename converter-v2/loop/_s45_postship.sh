#!/usr/bin/env bash
# SESSION 45 — the post-ship proofs, parametrised (the r485 _r485_postship.sh form), run after scoped_ship.sh --commit:
# run_all_gates.sh, the skeleton state + delta vs the previous round, the gatecheck verdict (cs bc FIRST — the cached-row trap),
# the ledger check, the 17 selftests, the feature index, the DIFF MINER (§1d — after every regeneration).
# Usage (WSL): bash _s45_postship.sh <R e.g. 486> <PREV e.g. 485>
R="$1"; P="$2"; [ -n "$R" ] && [ -n "$P" ] || { echo "need R and PREV"; exit 2; }
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_r${R}_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY breakdown|CLEAN pages|leak|REAL FAILURES|divergence" $O/_r${R}_gates.log | head -30 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r$P"
python3 _skeleton_compare.py --json $O/_r${R}_sk_final.json > $O/_r${R}_sk_full.log 2>&1; echo "  rc=$?"
python3 $O/_s29_skdelta.py $O/_r${P}_sk_final.json $O/_r${R}_sk_final.json --affected $O/_affected_r$R.txt > $O/_r${R}_skdelta.log 2>&1; head -n 20 $O/_r${R}_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck: cs bc FIRST (never trust a cached row), then skeleton defect"
python3 _gatecheck.py cs bc > $O/_r${R}_gatecheck_csbc.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|compare|body" $O/_r${R}_gatecheck_csbc.log | head -8
python3 _gatecheck.py skeleton defect > $O/_r${R}_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|defect|RESULT" $O/_r${R}_gatecheck.log | head -10
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo typing; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_r${R}_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_r${R}_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_r${R}_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r${R}_index.log 2>&1; echo "  rc=$?"; tail -1 $O/_r${R}_index.log
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r$R.md
python3 _diff_miner.py > $O/_diff_miner_r$R.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_r$R.log | cut -c1-200
echo "[$(date +%T)] POSTSHIP_DONE"
