#!/usr/bin/env bash
# ROUND 360 — the post-regeneration housekeeping (the r347 sequence): the 16 selftests, the fast-loop baseline re-snapshot,
# the content-manifest snapshot, the ship ledger (FULL), the feature index (--rehtml + --merge + --selftest). Run from
# reference/tests under WSL: bash ../../outputs/_r360_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_r360_selftests.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] fast-loop baseline re-snapshot"
python3 _fastloop_snapshot.py > $O/_r360_fastloop_snapshot.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] content manifest snapshot"
python3 _content_manifest.py snapshot > $O/_r360_manifest_snapshot.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] ship ledger — FULL"
python3 _ship_ledger.py record-full --round 360 --build 260619.31 > $O/_r360_ledger.log 2>&1; echo "  rc=$?"; cat $O/_r360_ledger.log | tail -3
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r360_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_r360_index.log
echo "[$(date +%T)] POSTSHIP_DONE"
