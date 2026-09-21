#!/usr/bin/env bash
# SESSION 33 ROUND 1 (engine r425 FINISHED — the XOTP activity-table adapter enabled; THE FULL-SHIP BACKSTOP, scoped #8 since r416)
# — post-regeneration housekeeping after run_all_gates.sh / the skeleton state / skdelta / gatecheck (already run and logged as
# _s33_r425_gates.log / _s33_r425_sk_final.json / _s33_r425_gatecheck.log): ledger record-full, fast-loop baseline re-snapshot,
# content-manifest snapshot, the 17 selftests, the feature index, the DIFF MINER. reference/tests under WSL:
# bash ../../outputs/_s33_r425_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
cp $O/_s33_r425_sk_final.json $O/_r425_sk_final.json
echo "[$(date +%T)] ship ledger: record-full (the backstop after scoped #8)"
python3 _ship_ledger.py record-full --round 425 --build 260619.97 2>&1 | tail -2
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] fast-loop baseline re-snapshot"
python3 _fastloop_snapshot.py > $O/_s33_r425_fastloop_snapshot.log 2>&1; echo "  rc=$?"; tail -2 $O/_s33_r425_fastloop_snapshot.log
echo "[$(date +%T)] content manifest snapshot"
python3 _content_manifest.py snapshot > $O/_s33_r425_manifest_snapshot.log 2>&1; echo "  rc=$?"; tail -1 $O/_s33_r425_manifest_snapshot.log
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s33_r425_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s33_r425_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s33_r425_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s33_r425_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_s33_r425_index.log
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r425.md
python3 _diff_miner.py > $O/_diff_miner_s33_r425.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s33_r425.log
echo "[$(date +%T)] POSTSHIP_DONE"
