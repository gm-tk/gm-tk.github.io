#!/usr/bin/env bash
# ROUND 480 (session 44 Round 3 — KB 07B the MTK activity is ONE box, a §1d TRR family dialect, ACTLABELBOX_OFF) — commit the fast-loop
# baseline with the NAMED compare_structure pool shrink: exact chain 16771 -> 16691 (-80) = the matched pool 19533 -> 19453 (-80) — the intro
# elements now sit INSIDE div.activity, a subtree compare_structure excludes on both sides (`activity` is in its INTERACTIVE_CLASSES);
# EXTRA 208 / missing 872 EXACT. The r344 precedent (cs exact -8 = the pool shrink, accepted named). Skeleton +0.06pp, >=50 +4.
# WSL: bash _r480_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r480.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "compare_structure exact chain" --commit > $O/_r480_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r480_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r480.txt 2>&1 | tail -2
