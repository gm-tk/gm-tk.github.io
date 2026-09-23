#!/usr/bin/env bash
# ROUND 440 (session 39 Round 2 — D13-6, the dual-build page model) — the in-memory A/B probe over every Claude-dir module, 4 shards.
#   OFF = the pre-round registry swapped in (--pre outputs/_r440_pre) — every page must be identical to the disk (the null test)
#   ON  = the live registry — the changed set must be exactly MXFUN01 / BLL240 / CEDT207 (CEDT301 kept split — the D13-6 caveat); pages saved under outputs/_r440_on
# Usage (WSL, from anywhere): bash _r440_probe_run.sh OFF|ON      (the r426 pattern)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
MODE="$1"
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_r440_codes.txt
N=$(wc -l < $O/_r440_codes.txt)
split -n l/4 -d $O/_r440_codes.txt $O/_r440_codes_
echo "[$(date +%T)] $MODE probe over $N modules, 4 shards"
if [ "$MODE" = "ON" ]; then rm -rf $O/_r440_on; mkdir -p $O/_r440_on; fi
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet --pre $O/_r440_pre $(cat $O/_r440_codes_$i) > $O/_r440_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r440_probe.cjs --quiet --save $O/_r440_on $(cat $O/_r440_codes_$i) > $O/_r440_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_r440_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_r440_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sed 's#/.*##' | sort -u > $O/_r440_${MODE}_modules.txt
echo "changed modules ($MODE): $(wc -l < $O/_r440_${MODE}_modules.txt) — $(tr '\n' ' ' < $O/_r440_${MODE}_modules.txt)"
