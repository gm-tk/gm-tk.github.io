#!/usr/bin/env bash
# ROUND 0d (session 33 Round 3 — the 38 pre-intake never-converted modules; LOOP §1f Phase 3 — the FULL regeneration on UNCHANGED registries) —
# the FULL regeneration of all 545 gated dirs (507 + the 38): `_batch_plan.py`'s plan (weights-aware batches) run as batch_convert.cjs calls,
# 4 parallel workers under WSL, a 900 s wall each (the r405 recipe). Run under WSL from anywhere: bash _intake_2026-09-22_fullship_par.sh
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs
python3 _batch_plan.py | grep '^\./_regen_safe.sh' | sed 's#^\./_regen_safe.sh #STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs #; s#$# --force#' > $O/_intake_2026-09-22_fullship_run.sh
: > $O/_intake_2026-09-22_fullship_regen.log
n=0
while IFS= read -r line; do
  n=$((n+1)); printf '%s\n' "$line" > $O/_intake_2026-09-22_batch_$n.sh
done < $O/_intake_2026-09-22_fullship_run.sh
echo "[$(date +%T)] full regeneration: $n batches, 4 parallel workers"
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_intake_2026-09-22_batch_{}.sh > '"$O"'/_intake_2026-09-22_batch_{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_intake_2026-09-22_fullship_regen.log'
echo "[$(date +%T)] REGEN_DONE"; grep -c "rc=0" $O/_intake_2026-09-22_fullship_regen.log; grep -v "rc=0" $O/_intake_2026-09-22_fullship_regen.log || echo "all rc 0"
