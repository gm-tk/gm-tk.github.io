#!/usr/bin/env bash
# Session 49 — regenerate a code list in batches of <= 10 with 4 parallel workers (WSL). Usage: bash _s49_regen_par.sh TAG CODE...
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs; TAG="$1"; shift
printf '%s\n' "$@" | sort -u | xargs -n 10 > $O/_${TAG}_batches.txt
n=0; : > $O/_${TAG}_regen.log
while IFS= read -r line; do n=$((n+1)); echo "STUB_OEMBED=1 timeout 900 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs $line --force" > $O/_${TAG}_b$n.sh; done < $O/_${TAG}_batches.txt
seq 1 $n | xargs -P 4 -I{} bash -c 'bash '"$O"'/_'"$TAG"'_b{}.sh > '"$O"'/_'"$TAG"'_b{}.log 2>&1; echo "batch {} rc=$?" >> '"$O"'/_'"$TAG"'_regen.log'
echo "batches $n: $(grep -c 'rc=0' $O/_${TAG}_regen.log) rc 0"; grep -v 'rc=0' $O/_${TAG}_regen.log || true
