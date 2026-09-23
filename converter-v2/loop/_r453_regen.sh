#!/usr/bin/env bash
# ROUND 453 (session 41 Round 1 — the table-cell title bar opens the document + the MTK overview-table tabs) — the scoped regeneration: the 23 Bilingual-template modules
# (the whole-type family, §0a — the ON probe changed 13 of them; _affected_r453.txt) + the 12-module spot-check sample, WITH the fix ON, in batches of <= 11
# codes, 4 batches in parallel (the r416 pattern — safe under WSL), each through _regen_safe.sh with REGEN_TIMEOUT=600.
# Usage (WSL): bash _r453_regen.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
export REGEN_TIMEOUT=600
test -s $O/_affected_r453.txt || exit 2
echo "[$(date +%T)] spot-check plan"
python3 _scoped_spotcheck.py plan --affected $O/_affected_r453.txt --n 12 --seed 453 > $O/_r453_spotcheck_plan.log 2>&1
tail -4 $O/_r453_spotcheck_plan.log
SAMPLE=$(grep -o '_batch_plan.py --codes .*' $O/_r453_spotcheck_plan.log | head -1 | sed 's/_batch_plan.py --codes //')
echo "sample: $SAMPLE"
ALL="$(tr -d '\r' < $O/_affected_r453.txt | tr '\n' ' ') $SAMPLE"
echo $ALL | tr ' ' '\n' | grep -v '^$' | sort -u > $O/_r453_regen_codes.txt
echo "[$(date +%T)] $(wc -l < $O/_r453_regen_codes.txt) modules -> batches of 11"
rm -f $O/_r453_regen_batch_*
split -l 11 -d $O/_r453_regen_codes.txt $O/_r453_regen_batch_
ls $O/_r453_regen_batch_* | xargs -P 4 -I{} bash -c 'b={}; ./_regen_safe.sh $(cat $b | tr "\n" " ") > $b.log 2>&1; echo "  $(basename $b) rc=$? $(tail -1 $b.log | cut -c1-120)"'
echo "[$(date +%T)] fresh check"
python3 _content_manifest.py fresh --affected $O/_affected_r453.txt 2>&1 | tail -4
python3 _scoped_spotcheck.py verify 2>&1 | tail -3
echo "[$(date +%T)] done"
