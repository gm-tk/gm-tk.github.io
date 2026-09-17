#!/usr/bin/env bash
# ROUND 357 (session 19 Round 1 — the chip presence class) — the 89-module family regeneration (BLL1 / CEDT / CEDK / CEDO / EXPFUN / PNR / OSSC / SCFUN), 4 parallel workers under WSL (the r356 runner).
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
: > $O/_r357_regen.log
n=0
while IFS= read -r line; do
  n=$((n+1)); printf '%s\n' "$line" > $O/_r357_batch_$n.sh
done < $O/_r357_regen_run.sh
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_r357_batch_{}.sh > '"$O"'/_r357_batch_{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_r357_regen.log'
echo "[$(date +%T)] REGEN_DONE"; grep -c "rc=0" $O/_r357_regen.log; grep -v "rc=0" $O/_r357_regen.log || echo "all rc 0"
