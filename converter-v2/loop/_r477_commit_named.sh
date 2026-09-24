#!/usr/bin/env bash
# ROUND 477 (session 43 Round 9 — KB c75 the gathered body text keeps its links, GATHERLINKS_OFF) — commit the fast-loop baseline with the NAMED KB-override crossing
# (HIS1008_5_0 75.9 → 74.9 — the writer's citation link "Garrow, David," the gold drops; mean +0.0042pp, cs exact +1; §1b "Gates and KB overrides"; the r470 / r475 --accept-named pattern).
# WSL: bash _r477_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r477.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "skeleton pages >=75%" --commit > $O/_r477_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r477_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r477.txt 2>&1 | tail -2
