#!/usr/bin/env bash
# ROUND 353 — the in-memory probe over all 416 modules in 4 shards (from reference/tests under WSL): OFF (WIDGETMEMBERS_OFF) must equal disk; ON saved to _r353_on
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
mkdir -p $O/_r353_on
for i in 00 01 02 03; do
  WIDGETMEMBERS_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r353_probe.cjs --quiet $(cat $O/_r342_shard_$i) > $O/_r353_probe_off_$i.log 2>&1 &
done; wait
echo "[$(date +%T)] OFF done"
for i in 00 01 02 03; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r353_probe.cjs --save $O/_r353_on $(cat $O/_r342_shard_$i) > $O/_r353_probe_on_$i.log 2>&1 &
done; wait
echo "[$(date +%T)] PROBE_DONE"
