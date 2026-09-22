#!/usr/bin/env bash
# ROUND 0d (session 33 Round 3, 2026-09-22) — Phase 2: convert the 38 pre-intake never-converted modules by explicit code
# list, 4 batches of <= 11, the r410 batch_convert form under WSL. bash _intake_2026-09-22_convert.sh
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs
split -l 10 -d $O/_intake_2026-09-22_codes.txt $O/_intake_2026-09-22_batch_
for b in $O/_intake_2026-09-22_batch_0?; do
  n=$(basename $b)
  echo "[$(date +%T)] $n: $(cat $b | tr '\n' ' ')"
  STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $(cat $b | tr '\n' ' ') --force > $O/${n}.log 2>&1
  echo "  rc=$?"
done
echo "[$(date +%T)] CONVERT_DONE"
