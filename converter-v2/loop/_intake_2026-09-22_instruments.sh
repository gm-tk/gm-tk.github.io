#!/usr/bin/env bash
# ROUND 0d (session 33 Round 3, 22 Sept 2026) — LOOP §1f Phase 5, the instruments the intake voids: the ceiling, the coverage
# dashboard, the DIFF MINER (full + scoped over the 38), the feature index. reference/tests under WSL: bash ../../outputs/_intake_2026-09-22_instruments.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs; T=_intake_2026-09-22
echo "[$(date +%T)] ceiling"
( cd $O && timeout 1500 python3 _measure_ceiling.py --baseline ${T}_sk_final.json --json _ceiling_intake_2026-09-22.json --md _ceiling_intake_2026-09-22.md > _ceiling_intake_2026-09-22.log 2>&1; echo "  rc=$?"; tail -n 4 _ceiling_intake_2026-09-22.log | cut -c1-200 )
echo "[$(date +%T)] dashboard"
bash $O/${T}_dashboard_run.sh 2>&1 | tail -n 5
echo "[$(date +%T)] DIFF MINER full"
cp ../../../DIFF_QUEUE.md $O/_diff_queue_pre_intake_2026-09-22.md
python3 _diff_miner.py > $O/_diff_miner_${T}.log 2>&1; echo "  rc=$?"; tail -n 3 $O/_diff_miner_${T}.log | cut -c1-200
echo "[$(date +%T)] DIFF MINER scoped (the 38)"
python3 _diff_miner.py $(cat $O/${T}_codes.txt | tr '\n' ' ') > $O/_diff_miner_${T}_scoped.log 2>&1; echo "  rc=$?"; tail -n 3 $O/_diff_miner_${T}_scoped.log | cut -c1-200
ls -la $O/_diff_miner_scoped.* 2>/dev/null | cut -c30-
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/${T}_index.log 2>&1; echo "  rc=$?"; tail -1 $O/${T}_index.log
echo "[$(date +%T)] INSTRUMENTS_DONE"
