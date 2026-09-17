#!/usr/bin/env bash
# ROUND 366 — the post-regeneration housekeeping (the r347 sequence): the 16 selftests, the fast-loop baseline re-snapshot,
# reference/tests under WSL: bash ../../outputs/_r366_postship.sh
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
echo "[$(date +%T)] selftests"
{
python3 _skeleton_compare.py --selftest
for v in flipcard speechbubble accordion tabs clickdrop dropdown modal mtkquiz hintslider image_carousel carousel intextract math menulabels dragdrop; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_$v.cjs --selftest 2>&1 | grep -E "SELFTEST|GREEN|FAIL|Error"
done
} > $O/_r366_selftests.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] fast-loop baseline re-snapshot"
python3 _fastloop_snapshot.py > $O/_r366_fastloop_snapshot.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] content manifest snapshot"
python3 _content_manifest.py snapshot > $O/_r366_manifest_snapshot.log 2>&1; echo "  rc=$?"
echo "[$(date +%T)] feature index"
{ node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --rehtml; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --merge; node --require ./_deflate_raw_polyfill.cjs build_feature_index.cjs --selftest; } > $O/_r366_index.log 2>&1; echo "  rc=$?"; tail -3 $O/_r366_index.log
echo "[$(date +%T)] POSTSHIP_DONE"
