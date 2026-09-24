#!/usr/bin/env bash
# ROUND 486 (session 45 Round 1 — KB 01F the writer's quote is p.quoteText + p.quoteAck, QUOTEFORM_OFF) — commit the fast-loop
# baseline with the NAMED compare_structure reclassification: missing container 872 -> 878 (+6) alongside exact 16691 -> 16701 (+10)
# and EXTRA 208 -> 198 (-10), matched 19453 -> 19459 (+6). Proven block by block (outputs/_r486_csblocks.py / .log, the OFF render in
# outputs/_r486_off vs the disk): 0 blocks left EXACT; the +6 = 4 blocks that were ALREADY mismatched moving EXTRA -> MISSING (SSCI104_4's
# quote + its two explanation paragraphs, which the gold keeps inside the writer's preceding [alert] box; TWHA906's Mandela quote, which
# the gold sets in a whakatauki box) + 2 newly matched blocks inside that same TWHA906 whakatauki box (the Hillary quote + its ack).
# Skeleton +0.0021pp (pre-score), >=50 / >=75 EXACT. WSL: bash _r486_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r486.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "compare_structure missing container" --commit > $O/_r486_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r486_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r486.txt 2>&1 | tail -2
