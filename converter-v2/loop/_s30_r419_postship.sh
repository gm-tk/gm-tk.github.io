#!/usr/bin/env bash
# SESSION 30 ROUND 1 (engine r419 — the language-font wrap, KB constraint 92; SCOPED ship #3 since the r416 FULL)
# — post-ship housekeeping after scoped_ship.sh --commit (which patched the fast-loop baseline, refreshed the content
# manifest and recorded the scoped ship): run_all_gates.sh, skeleton state + delta vs r418, gatecheck verdict, 16
# selftests, the feature index, the ledger check, the DIFF MINER. reference/tests under WSL:
# bash ../../outputs/_s30_r419_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
echo "  (run_all_gates.sh already run before scoped_ship — _s30_r419_gates.log; re-running for the post-commit record)"; bash ./run_all_gates.sh > $O/_s30_r419_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY-breakdown|clean|leak|REAL FAILURES|divergence|defect" $O/_s30_r419_gates.log | head -40 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r418"
python3 _skeleton_compare.py --json $O/_s30_r419_sk_final.json > $O/_s30_r419_sk_full.log 2>&1; echo "  rc=$?"
cp $O/_s30_r419_sk_final.json $O/_r419_sk_final.json
python3 $O/_s29_skdelta.py $O/_s29_r419_sk_final.json $O/_s30_r419_sk_final.json --affected $O/_affected_r419.txt > $O/_s30_r419_skdelta.log 2>&1; head -3 $O/_s30_r419_skdelta.log
echo "[$(date +%T)] gatecheck verdict vs gate_baseline.json (r418 values)"
python3 _gatecheck.py > $O/_s30_r419_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|compare|body|defect" $O/_s30_r419_gatecheck.log | head -12
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s30_r419_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s30_r419_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s30_r419_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s30_r419_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_s30_r419_index.log
echo "[$(date +%T)] ship ledger check"
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r419.md
python3 _diff_miner.py > $O/_diff_miner_s30_r419.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s30_r419.log
echo "[$(date +%T)] POSTSHIP_DONE"
