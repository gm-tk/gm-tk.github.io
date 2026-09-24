#!/usr/bin/env bash
# ROUND 475 (session 43 Round 7 — KB c75 the menu keeps the writer's inline links, MENULINKS_OFF) — commit the fast-loop baseline with the NAMED KB-override dips
# (GEO1005_1_0 −0.3, XLP03_0_0 −0.3, ENGI405_0_0 −0.4, XLP04_0_0 −0.5 — the writer's resource links the gold drops; §1b "Gates and KB overrides"; the r470 --accept-named pattern).
# WSL: bash _r475_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r475.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "skeleton SCAFFOLD mean" --commit > $O/_r475_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r475_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r475.txt 2>&1 | tail -2
