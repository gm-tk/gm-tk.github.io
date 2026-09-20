#!/usr/bin/env bash
# SESSION 29 ROUND 1 (engine r410, the WJFUN tile-page dialect) — post-regeneration housekeeping (the r408 sequence minus what
# scoped_ship.sh --commit already did: the fast-loop baseline patch, the content-manifest refresh and the ledger record-scoped).
# reference/tests under WSL: bash ../../outputs/_s29_r410_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s29_r410_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s29_r410_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s29_r410_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s29_r410_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_s29_r410_index.log
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r410.md
python3 _diff_miner.py > $O/_diff_miner_s29_r410.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s29_r410.log
echo "[$(date +%T)] POSTSHIP_DONE"
