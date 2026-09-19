#!/usr/bin/env bash
# SESSION 28 / TASK 1 — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = the pre-rebuild registries (outputs/_s28_t1_pre swapped in) — expect identical to disk (the harness null test)
#   ON  = the live (rebuilt) data — the round's changed set; pages saved under outputs/_s28_t1_on for inspection
# Usage (WSL, from anywhere): bash _s28_t1_probe_run.sh OFF|ON
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s28_t1_codes.txt
N=$(wc -l < $O/_s28_t1_codes.txt)
split -n l/4 -d $O/_s28_t1_codes.txt $O/_s28_t1_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t1_probe.cjs --quiet --pre $O/_s28_t1_pre $(cat $O/_s28_t1_codes_$i) > $O/_s28_t1_probe_OFF_$i.log 2>&1 ) &
  else
    mkdir -p $O/_s28_t1_on
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s28_t1_probe.cjs --save $O/_s28_t1_on $(cat $O/_s28_t1_codes_$i) > $O/_s28_t1_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s28_t1_probe_${MODE}_0*.log
