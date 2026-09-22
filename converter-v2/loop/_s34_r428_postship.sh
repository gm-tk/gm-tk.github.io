#!/usr/bin/env bash
# SESSION 34 ROUND 2 (r428 — the Inquiry-template fallback shell; SCOPED ship #3 since the intake FULL) — post-ship
# housekeeping after the fast-loop --commit: run_all_gates.sh, skeleton state + delta vs r427, gatecheck verdict, 17 selftests,
# the feature index, the ledger check, the DIFF MINER. reference/tests under WSL: bash ../../outputs/_s34_r428_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_s34_r428_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY breakdown|CLEAN pages|leak|REAL FAILURES|divergence" $O/_s34_r428_gates.log | head -40 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r427"
python3 _skeleton_compare.py --json $O/_s34_r428_sk_final.json > $O/_s34_r428_sk_full.log 2>&1; echo "  rc=$?"
cp $O/_s34_r428_sk_final.json $O/_r428_sk_final.json
python3 $O/_s29_skdelta.py $O/_s33_r427_sk_final.json $O/_s34_r428_sk_final.json --affected $O/_affected_r428.txt > $O/_s34_r428_skdelta.log 2>&1; head -n 20 $O/_s34_r428_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck verdict vs gate_baseline.json (intake values)"
python3 _gatecheck.py > $O/_s34_r428_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|compare|body|defect|RESULT" $O/_s34_r428_gatecheck.log | head -14
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s34_r428_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s34_r428_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s34_r428_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s34_r428_index.log 2>&1; echo "  rc=$?"; tail -1 $O/_s34_r428_index.log
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -1
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r428.md
python3 _diff_miner.py > $O/_diff_miner_s34_r428.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s33_r422.log | cut -c1-200
echo "[$(date +%T)] POSTSHIP_DONE"
