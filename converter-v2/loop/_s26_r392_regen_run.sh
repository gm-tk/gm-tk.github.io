#!/usr/bin/env bash
# ROUND 392 — run the scoped regeneration batches two at a time. Usage (WSL, from anywhere): bash _s26_r392_regen_run.sh 1 2 3 4
cd "$(dirname "$0")/../reference/tests" || exit 1 2 3 4
O=../../outputs
run() { bash -c "$(sed -n "${1}p" $O/_s26_r392_batches.sh)" > $O/_s26_r392_batch_$1.log 2>&1; echo "batch $1 rc=$?"; }
set -- "$@"
while [ $# -gt 0 ]; do
  a=$1; shift; b=$1; [ -n "$b" ] && shift
  run $a & [ -n "$b" ] && run $b & wait
done
echo "[$(date +%T)] REGEN_DONE"
