#!/usr/bin/env bash
# ROUND 341 — the in-memory probe over all 416 modules in 4 shards (from reference/tests under WSL).
# Leg 1 ALL-OFF (NEARRED_OFF + DEFPAREN_OFF) must equal disk 2102/2102; leg 2 NEARRED_OFF alone isolates the
# weave refinement's own standard-red reach; leg 3 ON = the round; ON pages saved to outputs/_r341_on.
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
mkdir -p $O/_r341_on
for i in 00 01 02 03; do
  NEARRED_OFF=1 DEFPAREN_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r341_probe.cjs --quiet $(cat $O/_r341_shard_$i) > $O/_r341_probe_alloff_$i.log 2>&1 &
done; wait
echo "[$(date +%T)] ALL-OFF done"
for i in 00 01 02 03; do
  NEARRED_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r341_probe.cjs --quiet $(cat $O/_r341_shard_$i) > $O/_r341_probe_off_$i.log 2>&1 &
done; wait
echo "[$(date +%T)] NEARRED-OFF done"
for i in 00 01 02 03; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r341_probe.cjs --save $O/_r341_on $(cat $O/_r341_shard_$i) > $O/_r341_probe_on_$i.log 2>&1 &
done; wait
echo "[$(date +%T)] PROBE_DONE"
