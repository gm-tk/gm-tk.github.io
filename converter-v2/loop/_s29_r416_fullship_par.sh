#!/usr/bin/env bash
# ROUND 416 (session 29 Round 7 — the embedded activity title; THE LEDGER'S FULL-SHIP BACKSTOP, scoped #7 since the 19 Sept FULL) —
# the FULL regeneration of all 494 gated dirs: `_batch_plan.py`'s plan (weights-aware batches) run as batch_convert.cjs calls,
# 4 parallel workers under WSL, a 900 s wall each (the r405 recipe). Run under WSL from anywhere: bash _s29_r416_fullship_par.sh
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs
python3 _batch_plan.py | grep '^\./_regen_safe.sh' | sed 's#^\./_regen_safe.sh #STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs #; s#$# --force#' > $O/_s29_r416_fullship_run.sh
: > $O/_s29_r416_fullship_regen.log
n=0
while IFS= read -r line; do
  n=$((n+1)); printf '%s\n' "$line" > $O/_s29_r416_batch_$n.sh
done < $O/_s29_r416_fullship_run.sh
echo "[$(date +%T)] full regeneration: $n batches, 4 parallel workers"
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_s29_r416_batch_{}.sh > '"$O"'/_s29_r416_batch_{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_s29_r416_fullship_regen.log'
echo "[$(date +%T)] REGEN_DONE"; grep -c "rc=0" $O/_s29_r416_fullship_regen.log; grep -v "rc=0" $O/_s29_r416_fullship_regen.log || echo "all rc 0"
