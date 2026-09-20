#!/usr/bin/env bash
# SESSION 29 ROUND 2 (engine r411) — the in-memory A/B probe over every Claude-dir module, 4 shards (the r410 harness).
#   OFF = TILEMENUROW_OFF=1 — expect identical to disk on every page (the null test: disk == the r410 shipped state)
#   ON  = the live data — expect exactly the 21 WJFUN overviews; ON pages saved under outputs/_s29_r411_on
# Usage (WSL, from anywhere): bash _s29_r411_probe_run.sh OFF|ON
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s29_r411_codes.txt
N=$(wc -l < $O/_s29_r411_codes.txt)
split -n l/4 -d $O/_s29_r411_codes.txt $O/_s29_r411_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
if [ "$MODE" = "ON" ]; then rm -rf $O/_s29_r411_on; mkdir -p $O/_s29_r411_on; fi
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( TILEMENUROW_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t3_probe.cjs --quiet $(cat $O/_s29_r411_codes_$i) > $O/_s29_r411_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t3_probe.cjs --save $O/_s29_r411_on $(cat $O/_s29_r411_codes_$i) > $O/_s29_r411_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s29_r411_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_s29_r411_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sed 's#/.*##' | sort -u > $O/_s29_r411_${MODE}_modules.txt
echo "changed modules ($MODE): $(wc -l < $O/_s29_r411_${MODE}_modules.txt)"
