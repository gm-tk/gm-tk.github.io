#!/usr/bin/env bash
# Session 28 / Task 1 — rebuild the legacy Scaffold_Consensus.json (read only under GRANULAR_SIG_OFF=1) over the
# current paired population (anchor_compare.all_codes() = Claude-dir modules minus compare_exclusions): 8 partials
# in parallel, built with GRANULAR_SIG_OFF=1 so the file keeps the LEGACY blind signature its only consumer reads (--build-consensus CODES --json partial), then --merge-consensus. WSL, from anywhere.
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
python3 -c "import anchor_compare as ac; print('\n'.join(ac.all_codes()))" > $O/_s28_t1_consensus_codes.txt
N=$(wc -l < $O/_s28_t1_consensus_codes.txt); echo "[$(date +%T)] consensus over $N modules, 8 partials"
split -n l/8 -d $O/_s28_t1_consensus_codes.txt $O/_s28_t1_consensus_codes_
for i in 00 01 02 03 04 05 06 07; do
  ( GRANULAR_SIG_OFF=1 python3 anchor_compare.py --build-consensus $(cat $O/_s28_t1_consensus_codes_$i) --json $O/_s28_t1_consensus_part_$i.json > $O/_s28_t1_consensus_part_$i.log 2>&1; echo "part $i rc=$?" ) &
done
wait
GRANULAR_SIG_OFF=1 python3 anchor_compare.py --merge-consensus $O/_s28_t1_consensus_part_0*.json
echo "[$(date +%T)] CONSENSUS_DONE"
