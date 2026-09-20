#!/usr/bin/env bash
# SESSION 29 ROUND 7 (engine r416 — the embedded activity title; THE FULL-SHIP BACKSTOP) — post-regeneration housekeeping,
# the ship.sh sequence run piecewise: skeleton state + delta, gatecheck verdict, ledger record-full, fast-loop baseline
# re-snapshot, content-manifest snapshot, feature index, 16 selftests, the DIFF MINER. reference/tests under WSL:
# bash ../../outputs/_s29_r416_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] skeleton state (--json) + delta vs r415"
python3 _skeleton_compare.py --json $O/_s29_r416_sk_final.json > $O/_s29_r416_sk_full.log 2>&1; echo "  rc=$?"
cp $O/_s29_r416_sk_final.json $O/_r416_sk_final.json
python3 $O/_s29_skdelta.py $O/_s29_r415_sk_final.json $O/_s29_r416_sk_final.json --affected $O/_affected_r416.txt > $O/_s29_r416_skdelta.log 2>&1; head -3 $O/_s29_r416_skdelta.log
echo "[$(date +%T)] gatecheck verdict vs gate_baseline.json (r415 values)"
python3 _gatecheck.py > $O/_s29_r416_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|compare|body|defect" $O/_s29_r416_gatecheck.log | head -12
echo "[$(date +%T)] ship ledger: record-full (the backstop after scoped #7)"
python3 _ship_ledger.py record-full --round 416 --build 260619.87 2>&1 | tail -2
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] fast-loop baseline re-snapshot"
python3 _fastloop_snapshot.py > $O/_s29_r416_fastloop_snapshot.log 2>&1; echo "  rc=$?"; tail -2 $O/_s29_r416_fastloop_snapshot.log
echo "[$(date +%T)] content manifest snapshot"
python3 _content_manifest.py snapshot > $O/_s29_r416_manifest_snapshot.log 2>&1; echo "  rc=$?"; tail -1 $O/_s29_r416_manifest_snapshot.log
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s29_r416_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s29_r416_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s29_r416_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s29_r416_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_s29_r416_index.log
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r416.md
python3 _diff_miner.py > $O/_diff_miner_s29_r416.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s29_r416.log
echo "[$(date +%T)] POSTSHIP_DONE"
