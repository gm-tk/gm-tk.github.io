#!/usr/bin/env bash
# ROUND 449 (session 40 Round 4 — D13-4, the typing quiz shape 1) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = TYPING_OFF=1 — every page must be identical to the disk (the null test; the disk is the r448 state)
#   ON  = the live data — the changed set = typing bundles whose red answers build
#   SAVE = the ON pages of the changed modules (outputs/_r449_ON_modules.txt), under outputs/_r449_on (for the pre-score)
# Usage (WSL, from anywhere): bash _r449_probe_run.sh OFF|ON|SAVE      (the r440 harness, _r448_probe.cjs)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
if [ "$MODE" = "SAVE" ]; then
  rm -rf $O/_r449_on; mkdir -p $O/_r449_on
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet --save $O/_r449_on $(cat $O/_r449_ON_modules.txt) > $O/_r449_probe_SAVE.log 2>&1
  grep -h "^TOTAL" $O/_r449_probe_SAVE.log; exit 0
fi
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_r449_codes.txt
split -n l/4 -d $O/_r449_codes.txt $O/_r449_codes_
echo "[$(date +%T)] $MODE probe over $(wc -l < $O/_r449_codes.txt) modules, 4 shards"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( TYPING_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet $(cat $O/_r449_codes_$i) > $O/_r449_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet $(cat $O/_r449_codes_$i) > $O/_r449_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_r449_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_r449_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sort -u > $O/_r449_${MODE}_pages.txt
sed 's#/.*##' $O/_r449_${MODE}_pages.txt | sort -u > $O/_r449_${MODE}_modules.txt
echo "changed ($MODE): $(wc -l < $O/_r449_${MODE}_pages.txt) pages / $(wc -l < $O/_r449_${MODE}_modules.txt) modules — $(tr '\n' ' ' < $O/_r449_${MODE}_modules.txt)"
