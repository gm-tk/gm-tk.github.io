#!/usr/bin/env bash
# ROUND 473 (session 43 Round 2 — the modal single-link button text fence, MODALBTNTEXT_OFF) — the scoped
# regeneration of the WHOLE modal family (OPERATING_GUIDE §0a: every module carrying the type — `_r473_family.txt`,
# 110 modules; the ON probe's 14 changed modules all inside it → `_affected_r473.txt`) + the 12-module spot-check sample,
# WITH the fix ON, in batches of <= 11 codes, 4 batches in parallel (the r416 pattern — safe under WSL), each through
# _regen_safe.sh with REGEN_TIMEOUT=600.  Usage (WSL): bash _r473_regen.sh
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
export REGEN_TIMEOUT=600
test -s $O/_affected_r473.txt || exit 2
echo "[$(date +%T)] spot-check plan"
python3 _scoped_spotcheck.py plan --affected $O/_affected_r473.txt --n 12 --seed 472 > $O/_r473_spotcheck_plan.log 2>&1
tail -4 $O/_r473_spotcheck_plan.log
SAMPLE=$(grep -o '_batch_plan.py --codes .*' $O/_r473_spotcheck_plan.log | head -1 | sed 's/_batch_plan.py --codes //')
echo "sample: $SAMPLE"
ALL="$(tr -d '\r' < $O/_affected_r473.txt | tr '\n' ' ') $SAMPLE"
echo $ALL | tr ' ' '\n' | grep -v '^$' | sort -u > $O/_r473_regen_codes.txt
echo "[$(date +%T)] $(wc -l < $O/_r473_regen_codes.txt) modules -> batches of 11"
rm -f $O/_r473_regen_batch_*
split -l 11 -d $O/_r473_regen_codes.txt $O/_r473_regen_batch_
ls $O/_r473_regen_batch_* | grep -v '\.log$' | xargs -P 4 -I{} bash -c 'b={}; ./_regen_safe.sh $(cat $b | tr "\n" " ") > $b.log 2>&1; echo "  $(basename $b) rc=$? $(tail -1 $b.log | cut -c1-120)"'
echo "[$(date +%T)] fresh check"
python3 _content_manifest.py fresh --affected $O/_affected_r473.txt 2>&1 | tail -4
python3 _scoped_spotcheck.py verify 2>&1 | tail -3
echo "[$(date +%T)] REGEN_DONE"
