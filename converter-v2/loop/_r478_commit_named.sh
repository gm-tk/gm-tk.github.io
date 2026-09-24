#!/usr/bin/env bash
# ROUND 478 (session 43 Round 10, finished session 44 Round 1 — KB c75 the activity's lead keeps its links, LEADLINKS_OFF) — commit the
# fast-loop baseline with the NAMED KB-override mean dip (−0.0027pp, 16 down / 5 up, no crossing; worst HES1007_8_0 53.0 → 51.3,
# MXFL203_10_0 40.9 → 39.4, ENO2060_2_0 41.2 → 40.0 — HES1007's gold keeps the reading links but as a <ul><li> list, the others
# drop the writer's public link; 43 of the 63 added hrefs are gold-carried; §1b "Gates and KB overrides"; the r470 / r475 / r477 pattern).
# WSL: bash _r478_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r478.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "skeleton SCAFFOLD mean" --commit > $O/_r478_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r478_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r478.txt 2>&1 | tail -2
