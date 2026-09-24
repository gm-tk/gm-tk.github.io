#!/usr/bin/env bash
# _s46_shardrun.sh — run an engine-loading probe in N parallel shards under WSL and wait for all of them.
#   bash _s46_shardrun.sh <probe.cjs relative to outputs/> <N> [extra args…]
# Runs from reference/tests (the engine loader's home); each shard's stdout/stderr → /tmp/<probe>_<k>.log.
set -u
PROBE="$1"; N="$2"; shift 2
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
TAG=$(basename "$PROBE" .cjs)
pids=()
for ((k = 0; k < N; k++)); do
	STUB_OEMBED=1 timeout 1500 node --require ./_deflate_raw_polyfill.cjs "../../outputs/$PROBE" --shard "$k" "$N" "$@" > "/tmp/${TAG}_$k.log" 2>&1 &
	pids+=($!)
done
rc=0
for p in "${pids[@]}"; do wait "$p" || rc=$?; done
for ((k = 0; k < N; k++)); do tail -n 2 "/tmp/${TAG}_$k.log"; done
exit $rc
