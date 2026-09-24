#!/usr/bin/env bash
# ROUND 465 (session 42 Round 1 — Chris's D14-21: CHI1003 / CHI1004 / CHI1005 / JPN1004 leave the scored population;
# a GATE-CONFIGURATION round, the r343 precedent — no engine change, no regeneration). The proofs on the new population:
# run_all_gates.sh, the skeleton state fresh + the delta vs r461 (every kept page must be identical), gatecheck cs bc FIRST,
# the fast-loop snapshot, the ceiling re-measured, the DIFF MINER re-run.
# reference/tests under WSL: bash ../../outputs/_r465_run.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] run_all_gates.sh"
bash ./run_all_gates.sh > $O/_r465_gates.log 2>&1; echo "  rc=$?"
grep -nE "RESULT|REGRESS|FAIL|SCAFFOLD mean|>=50|pairs skipped|exact chain|EXTRA container|missing container|ANY breakdown|CLEAN pages|leak|REAL FAILURES|divergence" $O/_r465_gates.log | head -30 | cut -c1-160
echo "[$(date +%T)] skeleton state (--json) + delta vs r461"
python3 _skeleton_compare.py --json $O/_r465_sk_final.json > $O/_r465_sk_full.log 2>&1; echo "  rc=$?"
python3 $O/_s29_skdelta.py $O/_r461_sk_final.json $O/_r465_sk_final.json > $O/_r465_skdelta.log 2>&1; head -n 20 $O/_r465_skdelta.log | cut -c1-160
echo "[$(date +%T)] gatecheck: cs bc FIRST (never trust a cached row), then skeleton defect"
python3 _gatecheck.py cs bc > $O/_r465_gatecheck_csbc.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|compare|body" $O/_r465_gatecheck_csbc.log | head -8
python3 _gatecheck.py skeleton defect > $O/_r465_gatecheck.log 2>&1; echo "  rc=$?"; grep -E "VERDICT|REGRESS|HELD|IMPROVED|skeleton|defect|RESULT" $O/_r465_gatecheck.log | head -10
echo "[$(date +%T)] fast-loop snapshot (the new population)"
python3 _fastloop_snapshot.py > $O/_r465_fastloop_snapshot.log 2>&1; echo "  rc=$?"; tail -2 $O/_r465_fastloop_snapshot.log
echo "[$(date +%T)] ceiling (re-measured on the new population)"
( cd $O && timeout 1500 python3 _measure_ceiling.py --baseline _r465_sk_final.json --json _ceiling_r465.json --md _ceiling_r465.md > _ceiling_r465.log 2>&1; echo "  rc=$?"; tail -n 4 _ceiling_r465.log | cut -c1-200 )
echo "[$(date +%T)] DIFF MINER (§1d)"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_r465.md
python3 _diff_miner.py > $O/_diff_miner_r465.log 2>&1; echo "  miner rc=$?"; tail -3 $O/_diff_miner_r465.log | cut -c1-200
echo "[$(date +%T)] R465_RUN_DONE"
