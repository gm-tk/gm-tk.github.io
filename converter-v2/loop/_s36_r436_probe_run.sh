#!/usr/bin/env bash
# SESSION 36 / ROUND 1 (ROUND 436 — the lesson continuation page inherits its lesson's menu; OFF = CONTMENU_OFF=1, must equal the disk = the r435 corpus) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = the dialect off — every module must be identical to disk (the harness null test)
#   ON  = the live data — the round's changed set (expected: 10 modules / 21-26 continuation pages); pages saved under outputs/_s36_r436_on for inspection
# Usage (WSL, from anywhere): bash _s36_r436_probe_run.sh OFF|ON
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s36_r436_codes.txt
N=$(wc -l < $O/_s36_r436_codes.txt)
split -n l/4 -d $O/_s36_r436_codes.txt $O/_s36_r436_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
if [ "$MODE" = "ON" ]; then rm -rf $O/_s36_r436_on; mkdir -p $O/_s36_r436_on; fi
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( CONTMENU_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s36_r436_probe.cjs --quiet $(cat $O/_s36_r436_codes_$i) > $O/_s36_r436_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s36_r436_probe.cjs --quiet --save $O/_s36_r436_on $(cat $O/_s36_r436_codes_$i) > $O/_s36_r436_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s36_r436_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_s36_r436_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sed 's#/.*##' | sort -u > $O/_s36_r436_${MODE}_modules.txt
echo "changed modules ($MODE): $(wc -l < $O/_s36_r436_${MODE}_modules.txt)"
