#!/usr/bin/env bash
# Session 54 — restore the modules a FAILED scoped ship left on disk: regenerate every module of outputs/_rN_batches.txt with the
# round's *_OFF toggles set (the shipped state), 4 workers, then prove the corpus against the shipped manifest.
# Under WSL:  bash _s54_restore.sh N TOGGLE=1 [TOGGLE2=1 ...]
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
O=../../outputs; N="$1"; shift; ENVS="$*"
[ -s $O/_r${N}_batches.txt ] || { echo "no $O/_r${N}_batches.txt"; exit 2; }
n=0; : > $O/_r${N}_restore.log
while IFS= read -r line; do n=$((n+1)); echo "env $ENVS STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $line --force" > $O/_r${N}_rb$n.sh; done < $O/_r${N}_batches.txt
echo "[$(date +%T)] restore $n batches with $ENVS"
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_r'"$N"'_rb{}.sh > '"$O"'/_r'"$N"'_rb{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_r'"$N"'_restore.log'
echo "  batches rc 0: $(grep -c 'rc=0' $O/_r${N}_restore.log) of $n"
python3 _content_manifest.py diff 2>&1 | tail -3
echo "[$(date +%T)] RESTORE_DONE"
