#!/usr/bin/env bash
# ROUND 347 (session 12, D10-5 tables + the math-alpha fix) — the FULL regeneration of all 416 gated dirs (the r335 batch list, 36 batches) with 4 parallel workers under WSL.
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
: > $O/_r347_fullship_regen.log
n=0
while IFS= read -r line; do
  n=$((n+1)); printf '%s\n' "$line" > $O/_r347_batch_$n.sh
done < $O/_r347_fullship_run.sh
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_r347_batch_{}.sh > '"$O"'/_r347_batch_{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_r347_fullship_regen.log'
echo "[$(date +%T)] REGEN_DONE"; grep -c "rc=0" $O/_r347_fullship_regen.log; grep -v "rc=0" $O/_r347_fullship_regen.log || echo "all rc 0"
