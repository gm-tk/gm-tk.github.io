#!/usr/bin/env bash
# ROUND 470 (session 42 Round 8 — TRR115 converts, TABLETBWT_OFF) — commit the fast-loop baseline with the NEW MODULE's movers NAMED
# (the r453 precedent: the four new TRR115 pairs enter below the mean; every pre-existing page is byte-identical — the probe's 0 changed).
# WSL: bash _r470_commit_named.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
U=$(cat $O/_affected_r470.txt $O/_scoped_spotcheck_sample.txt | tr -d '\r' | sort -u | grep . | tr '\n' ' ')
echo "union: $U"
python3 _fastloop_diff.py $U --accept-named "skeleton SCAFFOLD mean,compare_structure missing,structurally-clean,literal-[tag] leak" --commit > $O/_r470_fastloop_named.log 2>&1
echo "rc=$?"
grep -E "RESULT|commit|manifest|REGRESS|IMPROVED|HELD" $O/_r470_fastloop_named.log | head -16 | cut -c1-180
python3 _content_manifest.py fresh --affected $O/_affected_r470.txt 2>&1 | tail -2
