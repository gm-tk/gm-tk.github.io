#!/usr/bin/env bash
# ROUND 336 (session 6) — the proof suite: fast-loop decomposition, full protected gates,
# fresh skeleton --json state, the 13 selftests. Run from reference/tests under WSL.
set -u
cd "$(dirname "$0")/../reference/tests"
O=../../outputs
echo "[$(date +%T)] fastloop diff on the 28"
python3 _fastloop_diff.py $(xargs < $O/_r336_affected.txt) > $O/_r336_fastloop.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] full gate suite"
bash run_all_gates.sh > $O/_r336_gates.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] fresh skeleton --json"
python3 _skeleton_compare.py --json $O/_r336_sk_final.json > $O/_r336_sk_full.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_r336_selftests.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] DONE"
