#!/usr/bin/env bash
# SESSION 29 ROUND 9 (engine r418 — the first tile panel takes the row form + the title-pin repair; SCOPED ship #2 since the r416 FULL)
# — post-ship housekeeping after scoped_ship.sh --commit (which patched the fast-loop baseline, refreshed the content
# manifest and recorded the scoped ship): run_all_gates.sh, skeleton state + delta vs r417, gatecheck verdict, 16
# selftests, the feature index, the ledger check, the DIFF MINER. reference/tests under WSL:
# bash ../../outputs/_s29_r418_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_s29_r418_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY-breakdown|clean|leak|REAL FAILURES|divergence|defect" $O/_s29_r418_gates.log | head -40 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r417"
python3 _skeleton_compare.py --json $O/_s29_r418_sk_final.json > $O/_s29_r418_sk_full.log 2>&1; echo "  rc=$?"
cp $O/_s29_r418_sk_final.json $O/_r418_sk_final.json
python3 $O/_s29_skdelta.py $O/_s29_r417_sk_final.json $O/_s29_r418_sk_final.json --affected $O/_affected_r418.txt > $O/_s29_r418_skdelta.log 2>&1; head -3 $O/_s29_r418_skdelta.log
echo "[$(date +%T)] gatecheck verdict vs gate_baseline.json (r417 values)"
python3 _gatecheck.py > $O/_s29_r418_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|compare|body|defect" $O/_s29_r418_gatecheck.log | head -12
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s29_r418_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s29_r418_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s29_r418_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s29_r418_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_s29_r418_index.log
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r418.md
python3 _diff_miner.py > $O/_diff_miner_s29_r418.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s29_r418.log
echo "[$(date +%T)] POSTSHIP_DONE"
