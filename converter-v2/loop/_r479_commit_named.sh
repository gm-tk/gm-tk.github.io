#!/usr/bin/env bash
# ROUND 479 (session 44 Round 2 — KB 07B the bilingual proverb table is the whakatauki box, PROVERBBOX_OFF) — commit the fast-loop baseline
# with the NAMED KB-override crossing: TRR108_0_0 50.9 -> 49.5 (>=50 -1) — TRR108 is the ONE Bilingual gold (1 / 23) that keeps the writer's
# "Whakataukī | Whakatauākī: / Proverb" heading row (as two h2s) above its box; KB 07B's component has no heading and 22 / 23 golds drop it.
# Also down: TRR114_0_0 63.9 -> 63.0 (the gold holds TRR114's proverb on page 1.0 — OTHER-PAGE). Mean +0.0144pp (20 up / 2 down), cs exact +12,
# missing -31. §1b "Gates and KB overrides"; the r470 / r475 / r477 --accept-named pattern. WSL: bash _r479_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r479.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "skeleton pages >=50%" --commit > $O/_r479_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r479_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r479.txt 2>&1 | tail -2
