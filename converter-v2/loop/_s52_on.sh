#!/usr/bin/env bash
# s52 — the full-corpus in-memory ON probe with the pages saved, the changed set, the ASSEMBLE ERROR count and the pre-score.
# Usage (WSL): bash _s52_on.sh TAG [ENV=VAL ...]   → outputs/_TAG_ON_pages.txt, _affected_TAG.txt, _TAG_ON_pages/, _TAG_prescore.log
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs || exit 1
T="$1"; shift
ls -d ../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > _s52_allcodes.txt
rm -rf /tmp/${T}_on; mkdir -p /tmp/${T}_on
echo "[$(date +%T)] ON probe over $(wc -l < _s52_allcodes.txt) modules ($*)"
PROBE_QUIET=1 PROBE_SAVE=/tmp/${T}_on bash _s51_probe_par.sh ${T}_ON "$PWD/_s52_allcodes.txt" "$@" > _${T}_ON_summary.log 2>&1
tail -1 _${T}_ON_summary.log
echo "ASSEMBLE ERROR: $(cat _${T}_ON_0?.log | grep -c 'ASSEMBLE ERROR')"
grep -h '^CHANGED' _${T}_ON_0?.log | tr ' ' '\n' | grep '/' | sort -u > _${T}_ON_pages.txt
sed 's#/.*##' _${T}_ON_pages.txt | sort -u > _affected_${T}.txt
echo "changed: $(wc -l < _${T}_ON_pages.txt) pages / $(wc -l < _affected_${T}.txt) modules"
rm -rf /tmp/${T}_onc; mkdir -p /tmp/${T}_onc
for c in $(cat _affected_${T}.txt); do cp -r /tmp/${T}_on/$c /tmp/${T}_onc/; done
rm -rf _${T}_ON_pages; cp -r /tmp/${T}_onc _${T}_ON_pages
cd ../reference/tests && python3 ../../outputs/_s51_prescore.py /tmp/${T}_onc > ../../outputs/_${T}_prescore.log 2>&1; tail -1 ../../outputs/_${T}_prescore.log
echo "[$(date +%T)] done"
