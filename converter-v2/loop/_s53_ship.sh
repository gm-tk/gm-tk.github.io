#!/usr/bin/env bash
# Session 53 — ONE scoped ship after the ON probe (_s52_on.sh TAG): the OFF probe over every module (must be 0 changed),
# the spot-check plan, the regeneration of the affected set + the sample (batches of <= 10, 4 workers, fix ON), then
# scoped_ship.sh --no-regen --commit --round N, then the gate suite (_s52_gates.sh). Under WSL:
#   bash _s53_ship.sh N TOGGLE [--accept-named M1,M2]      (reads outputs/_affected_rN.txt)
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs || exit 1
N="$1"; TG="$2"; shift 2; NAMED="${1:-}"; [ "$NAMED" = "--accept-named" ] && NAMED="--accept-named $2" || NAMED=""
AFF=_affected_r$N.txt; [ -s "$AFF" ] || { echo "no $AFF"; exit 2; }
echo "[$(date +%T)] OFF probe ($TG=1) over every module"
PROBE_QUIET=1 bash _s51_probe_par.sh r${N}_OFF "$PWD/_s52_allcodes.txt" $TG=1 > _r${N}_OFF_summary.log 2>&1
tail -1 _r${N}_OFF_summary.log; echo "  OFF ASSEMBLE ERROR: $(cat _r${N}_OFF_0?.log | grep -c 'ASSEMBLE ERROR')"
grep -q 'TOTAL identical [0-9]* / changed 0$' _r${N}_OFF_summary.log || { echo "OFF PROBE NOT IDENTICAL — stop"; exit 1; }
cd ../reference/tests || exit 1; O=../../outputs
echo "[$(date +%T)] spot-check plan"
python3 _scoped_spotcheck.py plan --affected $O/$AFF --n 12 --manifest $O/_content_manifest.txt > $O/_r${N}_spotcheck_plan.log 2>&1
SAMPLE=$(cat $O/_scoped_spotcheck_sample.txt | tr '\n' ' '); echo "  sample: $SAMPLE"
CODES="$(cat $O/$AFF | tr '\n' ' ') $SAMPLE"
printf '%s\n' $CODES | sort -u | xargs -n 10 > $O/_r${N}_batches.txt
n=0; : > $O/_r${N}_regen.log
while IFS= read -r line; do n=$((n+1)); echo "STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $line --force" > $O/_r${N}_b$n.sh; done < $O/_r${N}_batches.txt
echo "[$(date +%T)] regenerate $(printf '%s\n' $CODES | sort -u | wc -l) modules in $n batches (4 workers)"
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_r'"$N"'_b{}.sh > '"$O"'/_r'"$N"'_b{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_r'"$N"'_regen.log'
echo "  batches rc 0: $(grep -c 'rc=0' $O/_r${N}_regen.log) of $n"; grep -v 'rc=0' $O/_r${N}_regen.log || true
echo "[$(date +%T)] scoped ship"
./scoped_ship.sh --affected $O/$AFF --toggle $TG --no-regen --commit --round $N $NAMED > $O/_r${N}_ship.log 2>&1; echo "  ship rc=$?"
grep -E 'SCOPED SHIP:|OK —|!!|FAIL|mean|>=50|>=75|>=90|exact|EXTRA|missing|ANY' $O/_r${N}_ship.log | head -30
echo "[$(date +%T)] SHIP_DONE"
