#!/usr/bin/env bash
# SESSION 35 / ROUND 1 (ROUND 430 — the Inquiry panel opener robustness, part 2; OFF = INQOPENER2_OFF=1, must equal the disk = the r429 corpus) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = the round's three mechanisms off — every module must be identical to disk (the harness null test)
#   ON  = the live data — the round's changed set; pages saved under outputs/_s35_r430_on for inspection
# Usage (WSL, from anywhere): bash _s35_r430_probe_run.sh OFF|ON
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s35_r430_codes.txt
N=$(wc -l < $O/_s35_r430_codes.txt)
split -n l/4 -d $O/_s35_r430_codes.txt $O/_s35_r430_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
if [ "$MODE" = "ON" ]; then rm -rf $O/_s35_r430_on; mkdir -p $O/_s35_r430_on; fi
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( INQOPENER2_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s35_r430_probe.cjs --quiet $(cat $O/_s35_r430_codes_$i) > $O/_s35_r430_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s35_r430_probe.cjs --quiet --save $O/_s35_r430_on $(cat $O/_s35_r430_codes_$i) > $O/_s35_r430_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_s35_r430_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_s35_r430_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sed 's#/.*##' | sort -u > $O/_s35_r430_${MODE}_modules.txt
echo "changed modules ($MODE): $(wc -l < $O/_s35_r430_${MODE}_modules.txt)"
