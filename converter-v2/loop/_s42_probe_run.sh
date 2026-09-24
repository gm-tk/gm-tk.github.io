#!/usr/bin/env bash
# SESSION 42 — the in-memory A/B probe over every Claude-dir module, 4 shards (the r461 harness, parametrised; _r448_probe.cjs).
#   OFF  = <TOGGLE>=1 — every page must be identical to the disk (the null test)
#   ON   = the live data — the changed set
#   SAVE = the ON pages of the changed modules (outputs/_<TAG>_ON_modules.txt), under outputs/_<TAG>_on (for the pre-score)
# Usage (WSL, from anywhere): bash _s42_probe_run.sh <TAG e.g. r466> OFF|ON|SAVE <TOGGLE e.g. COURSECODE_OFF> [MORE_TOGGLES...]
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
T="$1"; MODE="$2"; shift 2; TOGGLES=""; for x in "$@"; do TOGGLES="$TOGGLES $x=1"; done
if [ "$MODE" = "SAVE" ]; then
  rm -rf $O/_${T}_on; mkdir -p $O/_${T}_on
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet --save $O/_${T}_on $(cat $O/_${T}_ON_modules.txt) > $O/_${T}_probe_SAVE.log 2>&1
  grep -h "^TOTAL" $O/_${T}_probe_SAVE.log; exit 0
fi
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_${T}_codes.txt
split -n l/4 -d $O/_${T}_codes.txt $O/_${T}_codes_
echo "[$(date +%T)] $MODE probe over $(wc -l < $O/_${T}_codes.txt) modules, 4 shards (toggles:$TOGGLES)"
for i in 00 01 02 03; do
  if [ "$MODE" = "OFF" ]; then
    ( env $TOGGLES STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet $(cat $O/_${T}_codes_$i) > $O/_${T}_probe_OFF_$i.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_r448_probe.cjs --quiet $(cat $O/_${T}_codes_$i) > $O/_${T}_probe_ON_$i.log 2>&1 ) &
  fi
done
wait
echo "[$(date +%T)] done"
grep -h "^TOTAL" $O/_${T}_probe_${MODE}_0*.log
grep -h "^CHANGED" $O/_${T}_probe_${MODE}_0*.log | tr ' ' '\n' | grep -v '^CHANGED' | sort -u > $O/_${T}_${MODE}_pages.txt
sed 's#/.*##' $O/_${T}_${MODE}_pages.txt | sort -u > $O/_${T}_${MODE}_modules.txt
echo "changed ($MODE): $(wc -l < $O/_${T}_${MODE}_pages.txt) pages / $(wc -l < $O/_${T}_${MODE}_modules.txt) modules — $(tr '\n' ' ' < $O/_${T}_${MODE}_modules.txt)"
