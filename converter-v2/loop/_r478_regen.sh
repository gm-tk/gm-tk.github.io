#!/usr/bin/env bash
# ROUND 478 (session 43 Round 10 — KB c75 the activity lead keeps its links, LEADLINKS_OFF) — the scoped
# regeneration of the 13 modules the full-corpus in-memory ON probe changed (`_affected_r478.txt` — the complete set by construction)
# + the 12-module spot-check sample, WITH the fix ON, in batches of <= 11 codes, 4 batches in parallel (the r416 pattern), each
# WITH the fix ON, in batches of <= 11 codes, 4 batches in parallel (the r416 pattern — safe under WSL), each through
# _regen_safe.sh with REGEN_TIMEOUT=600.  Usage (WSL): bash _r478_regen.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
export REGEN_TIMEOUT=600
test -s $O/_affected_r478.txt || exit 2
echo "[$(date +%T)] spot-check plan"
python3 _scoped_spotcheck.py plan --affected $O/_affected_r478.txt --n 12 --seed 472 > $O/_r478_spotcheck_plan.log 2>&1
tail -4 $O/_r478_spotcheck_plan.log
SAMPLE=$(grep -o '_batch_plan.py --codes .*' $O/_r478_spotcheck_plan.log | head -1 | sed 's/_batch_plan.py --codes //')
echo "sample: $SAMPLE"
ALL="$(tr -d '\r' < $O/_affected_r478.txt | tr '\n' ' ') $SAMPLE"
echo $ALL | tr ' ' '\n' | grep -v '^$' | sort -u > $O/_r478_regen_codes.txt
echo "[$(date +%T)] $(wc -l < $O/_r478_regen_codes.txt) modules -> batches of 11"
rm -f $O/_r478_regen_batch_*
split -l 11 -d $O/_r478_regen_codes.txt $O/_r478_regen_batch_
ls $O/_r478_regen_batch_* | grep -v '\.log$' | xargs -P 4 -I{} bash -c 'b={}; ./_regen_safe.sh $(cat $b | tr "\n" " ") > $b.log 2>&1; echo "  $(basename $b) rc=$? $(tail -1 $b.log | cut -c1-120)"'
echo "[$(date +%T)] fresh check"
python3 _content_manifest.py fresh --affected $O/_affected_r478.txt 2>&1 | tail -4
python3 _scoped_spotcheck.py verify 2>&1 | tail -3
echo "[$(date +%T)] REGEN_DONE"
