#!/usr/bin/env bash
# SESSION 50 Round 5 — THE LEDGER FULL-SHIP BACKSTOP at build 260620.75 (scoped #7 since the r505 FULL), NO engine change —
# the FULL regeneration of all 545 gated dirs: `_batch_plan.py`'s plan run as batch_convert.cjs calls, 4 parallel workers under WSL, a 900 s wall each.
# 4 parallel workers under WSL, a 900 s wall each (the r405 / r416 / r425 recipe). Run under WSL from anywhere: bash _s50b_full_fullship_par.sh
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs
python3 _batch_plan.py | grep '^\./_regen_safe.sh' | sed 's#^\./_regen_safe.sh #STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs #; s#$# --force#' > $O/_s50b_full_fullship_run.sh
: > $O/_s50b_full_fullship_regen.log
n=0
while IFS= read -r line; do
  n=$((n+1)); printf '%s\n' "$line" > $O/_s50b_full_batch_$n.sh
done < $O/_s50b_full_fullship_run.sh
echo "[$(date +%T)] full regeneration: $n batches, 4 parallel workers"
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_s50b_full_batch_{}.sh > '"$O"'/_s50b_full_batch_{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_s50b_full_fullship_regen.log'
echo "[$(date +%T)] REGEN_DONE"; grep -c "rc=0" $O/_s50b_full_fullship_regen.log; grep -v "rc=0" $O/_s50b_full_fullship_regen.log || echo "all rc 0"
echo "[$(date +%T)] stale check"; ./_stalecheck.sh 2>&1 | tail -3
echo "[$(date +%T)] content manifest: fresh (affected = _affected_s50b_full.txt) / changed"
python3 _content_manifest.py fresh --affected $O/_affected_s50b_full.txt 2>&1 | tail -4
python3 _content_manifest.py changed 2>&1 | tail -6
echo "[$(date +%T)] FULLSHIP_DONE"
