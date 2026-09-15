#!/usr/bin/env bash
# ROUND 339 — the in-memory OFF/ON probe over all 416 modules in 4 shards (from reference/tests under WSL)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
for i in 00 01 02 03; do
  VIDBTN_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r339_probe.cjs --quiet $(cat $O/_r339_shard_$i) > $O/_r339_probe_off_$i.log 2>&1 &
done; wait
for i in 00 01 02 03; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r339_probe.cjs $(cat $O/_r339_shard_$i) > $O/_r339_probe_on_$i.log 2>&1 &
done; wait
echo PROBE_DONE
