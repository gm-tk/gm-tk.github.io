#!/usr/bin/env bash
# ROUND 392 (session 26 Round 6) — the in-memory A/B probe over all Claude-dir modules, 4 shards, OFF then ON.
# Usage: bash _s26_r392_probe_run.sh OFF|ON   (run from anywhere; paths resolved from this file)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s26_r392_codes.txt
N=$(wc -l < $O/_s26_r392_codes.txt)
split -n l/4 -d $O/_s26_r392_codes.txt $O/_s26_r392_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( ULMERGE_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s26_r392_probe.cjs --quiet $(cat $O/_s26_r392_codes_$i) > $O/_s26_r392_probe_OFF_$i.log 2>&1 ) &
  else
    mkdir -p $O/_s26_r392_on
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s26_r392_probe.cjs --save $O/_s26_r392_on $(cat $O/_s26_r392_codes_$i) > $O/_s26_r392_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s26_r392_probe_${MODE}_0*.log
