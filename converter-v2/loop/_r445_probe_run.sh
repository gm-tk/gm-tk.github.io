#!/usr/bin/env bash
# ROUND 445 (session 39 Round 7 — D13-2, the two-column comparison table) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = TBLCOMPARE_OFF=1 — every page must be identical to the disk (the null test; the disk is the r444 state)
#   ON  = the live data — the changed set = the pages with a two-column opposite-pair table
#   SAVE = the ON pages of the changed modules (outputs/_r445_ON_modules.txt), under outputs/_r445_on (for the pre-score)
# Usage (WSL, from anywhere): bash _r445_probe_run.sh OFF|ON|SAVE      (the r440 harness, _r440_probe.cjs)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
if [ "$MODE" = "SAVE" ]; then
  rm -rf $O/_r445_on; mkdir -p $O/_r445_on
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet --save $O/_r445_on $(cat $O/_r445_ON_modules.txt) > $O/_r445_probe_SAVE.log 2>&1
  grep -h "^TOTAL" $O/_r445_probe_SAVE.log; exit 0
fi
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_r445_codes.txt
split -n l/4 -d $O/_r445_codes.txt $O/_r445_codes_
echo "[$(date +%T)] $MODE probe over $(wc -l < $O/_r445_codes.txt) modules, 4 shards"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( TBLCOMPARE_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet $(cat $O/_r445_codes_$i) > $O/_r445_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet $(cat $O/_r445_codes_$i) > $O/_r445_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_r445_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_r445_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sort -u > $O/_r445_${MODE}_pages.txt
sed 's#/.*##' $O/_r445_${MODE}_pages.txt | sort -u > $O/_r445_${MODE}_modules.txt
echo "changed ($MODE): $(wc -l < $O/_r445_${MODE}_pages.txt) pages / $(wc -l < $O/_r445_${MODE}_modules.txt) modules — $(tr '\n' ' ' < $O/_r445_${MODE}_modules.txt)"
