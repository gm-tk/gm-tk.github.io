#!/usr/bin/env bash
# SESSION 28 / TASK 3 (ROUND 410) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = TILEPAGE_OFF=1 (the tile-page dialect off; first_heading_level's WJFUN entry is inert without a panel)
#         — expect identical to disk on every page (the harness null test)
#   ON  = the live data — the round's changed set; pages saved under outputs/_s28_t3_on for inspection
# Usage (WSL, from anywhere): bash _s28_t3_probe_run.sh OFF|ON
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s28_t3_codes.txt
N=$(wc -l < $O/_s28_t3_codes.txt)
split -n l/4 -d $O/_s28_t3_codes.txt $O/_s28_t3_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
if [ "$MODE" = "ON" ]; then rm -rf $O/_s28_t3_on; mkdir -p $O/_s28_t3_on; fi
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( TILEPAGE_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t3_probe.cjs --quiet $(cat $O/_s28_t3_codes_$i) > $O/_s28_t3_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t3_probe.cjs --save $O/_s28_t3_on $(cat $O/_s28_t3_codes_$i) > $O/_s28_t3_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s28_t3_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_s28_t3_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sed 's#/.*##' | sort -u > $O/_s28_t3_${MODE}_modules.txt
echo "changed modules ($MODE): $(wc -l < $O/_s28_t3_${MODE}_modules.txt)"
