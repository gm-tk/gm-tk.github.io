#!/usr/bin/env bash
# ROUND 447 (session 40 Round 1 — D13-5, the journal-button variants) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = JOURNALVAR_OFF=1 — every page must be identical to the disk (the null test; the disk is the r446 state)
#   ON  = the live data — the changed set = pages with a journal-label variant button
#   SAVE = the ON pages of the changed modules (outputs/_r447_ON_modules.txt), under outputs/_r447_on (for the pre-score)
# Usage (WSL, from anywhere): bash _r447_probe_run.sh OFF|ON|SAVE      (the r440 harness, _r440_probe.cjs)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
if [ "$MODE" = "SAVE" ]; then
  rm -rf $O/_r447_on; mkdir -p $O/_r447_on
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet --save $O/_r447_on $(cat $O/_r447_ON_modules.txt) > $O/_r447_probe_SAVE.log 2>&1
  grep -h "^TOTAL" $O/_r447_probe_SAVE.log; exit 0
fi
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_r447_codes.txt
split -n l/4 -d $O/_r447_codes.txt $O/_r447_codes_
echo "[$(date +%T)] $MODE probe over $(wc -l < $O/_r447_codes.txt) modules, 4 shards"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( JOURNALVAR_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet $(cat $O/_r447_codes_$i) > $O/_r447_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet $(cat $O/_r447_codes_$i) > $O/_r447_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_r447_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_r447_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sort -u > $O/_r447_${MODE}_pages.txt
sed 's#/.*##' $O/_r447_${MODE}_pages.txt | sort -u > $O/_r447_${MODE}_modules.txt
echo "changed ($MODE): $(wc -l < $O/_r447_${MODE}_pages.txt) pages / $(wc -l < $O/_r447_${MODE}_modules.txt) modules — $(tr '\n' ' ' < $O/_r447_${MODE}_modules.txt)"
