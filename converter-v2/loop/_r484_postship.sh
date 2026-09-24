#!/usr/bin/env bash
# ROUND 484 (session 44 Round 9 — KB c38 for the quiz types, TPLAUTOQUIZ_OFF; scoped ship #2 since the r482 FULL backstop) — post-ship proofs.
# post-ship proofs after scoped_ship.sh --commit: run_all_gates.sh, the skeleton state + delta vs r483, the gatecheck verdict
# (cs bc FIRST — the cached-row trap), the ledger check, the 17 selftests, the feature index, the DIFF MINER.
# reference/tests under WSL: bash ../../outputs/_r484_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_r484_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY breakdown|CLEAN pages|leak|REAL FAILURES|divergence" $O/_r484_gates.log | head -30 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r483"
python3 _skeleton_compare.py --json $O/_r484_sk_final.json > $O/_r484_sk_full.log 2>&1; echo "  rc=$?"
python3 $O/_s29_skdelta.py $O/_r483_sk_final.json $O/_r484_sk_final.json --affected $O/_affected_r484.txt > $O/_r484_skdelta.log 2>&1; head -n 20 $O/_r484_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck: cs bc FIRST (never trust a cached row), then skeleton defect"
python3 _gatecheck.py cs bc > $O/_r484_gatecheck_csbc.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|compare|body" $O/_r484_gatecheck_csbc.log | head -8
python3 _gatecheck.py skeleton defect > $O/_r484_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|defect|RESULT" $O/_r484_gatecheck.log | head -10
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -2
echo "  (the scoped ship already patched the fast-loop baseline and refreshed the content manifest)"
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo typing; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_r484_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_r484_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_r484_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r484_index.log 2>&1; echo "  rc=$?"; tail -1 $O/_r484_index.log
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r484.md
python3 _diff_miner.py > $O/_diff_miner_r484.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_r484.log | cut -c1-200
echo "[$(date +%T)] POSTSHIP_DONE"
