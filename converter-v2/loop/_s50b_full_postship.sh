#!/usr/bin/env bash
# SESSION 50 Round 5 — THE FULL-SHIP BACKSTOP at 260620.75 (scoped #7 → 0 since the r505 FULL; no engine change) — post-regeneration
# proofs after _s50b_full_fullship_par.sh: run_all_gates.sh, skeleton state + delta vs r520, the gatecheck verdict (cs bc FIRST), ledger record-full,
# fast-loop baseline re-snapshot, content-manifest snapshot, the selftests, the feature index, the DIFF MINER.
# reference/tests under WSL: bash ../../outputs/_s50b_full_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_s50b_full_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY breakdown|CLEAN pages|leak|REAL FAILURES|divergence" $O/_s50b_full_gates.log | head -40 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r520"
python3 _skeleton_compare.py --json $O/_s50b_full_sk_final.json > $O/_s50b_full_sk_full.log 2>&1; echo "  rc=$?"
python3 $O/_s29_skdelta.py $O/_s50b_full_sk_pre.json $O/_s50b_full_sk_final.json --affected $O/_affected_s50b_full.txt > $O/_s50b_full_skdelta.log 2>&1; head -n 20 $O/_s50b_full_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck: cs bc FIRST (never trust a cached row), then skeleton defect"
python3 _gatecheck.py cs bc > $O/_s50b_full_gatecheck_csbc.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|compare|body" $O/_s50b_full_gatecheck_csbc.log | head -8
python3 _gatecheck.py skeleton defect --commit --round 520 > $O/_s50b_full_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|defect|RESULT" $O/_s50b_full_gatecheck.log | head -10
echo "[$(date +%T)] ship ledger: record-full (the backstop at what would have been scoped #8)"
python3 _ship_ledger.py record-full --round 520 --build 260620.81 2>&1 | tail -2
python3 _ship_ledger.py check 2>&1 | tail -2
echo "[$(date +%T)] fast-loop baseline re-snapshot"
python3 _fastloop_snapshot.py > $O/_s50b_full_fastloop_snapshot.log 2>&1; echo "  rc=$?"; tail -2 $O/_s50b_full_fastloop_snapshot.log
echo "[$(date +%T)] content manifest snapshot"
python3 _content_manifest.py snapshot > $O/_s50b_full_manifest_snapshot.log 2>&1; echo "  rc=$?"; tail -1 $O/_s50b_full_manifest_snapshot.log
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop bingo typing; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_s50b_full_selftests.log 2>&1; echo "  rc=$?  PASS/GREEN lines: $(grep -c 'PASS\|GREEN' $O/_s50b_full_selftests.log)  FAIL lines: $(grep -c 'FAIL' $O/_s50b_full_selftests.log)"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_s50b_full_index.log 2>&1; echo "  rc=$?"; tail -1 $O/_s50b_full_index.log
echo "[$(date +%T)] DIFF MINER (§1d — after every regeneration)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_s50_full.md
python3 _diff_miner.py > $O/_diff_miner_s50_full.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_s50_full.log | cut -c1-200
echo "[$(date +%T)] POSTSHIP_DONE"
