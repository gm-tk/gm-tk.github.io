#!/usr/bin/env bash
# s52 Round 1 — r528 v2: the full-corpus in-memory ON probe (FLAGON), pages saved for the pre-score; then the pre-score.
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs || exit 1
ls -d ../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > _s52_allcodes.txt
rm -rf /tmp/r528b_on; mkdir -p /tmp/r528b_on
echo "[$(date +%T)] ON probe over $(wc -l < _s52_allcodes.txt) modules"
PROBE_QUIET=1 PROBE_SAVE=/tmp/r528b_on bash _s51_probe_par.sh r528b_ON "$PWD/_s52_allcodes.txt" FLAGON="EmitTemplates:callouts.untagged_proverb" > _r528b_ON_summary.log 2>&1
tail -3 _r528b_ON_summary.log
echo "ASSEMBLE ERROR: $(grep -c 'ASSEMBLE ERROR' _r528b_ON_0?.log | awk -F: '{s+=$2} END {print s}')"
grep -h '^CHANGED' _r528b_ON_0?.log | tr ' ' '\n' | grep -v '^CHANGED' | grep -v '^$' | sort -u > _r528b_ON_pages.txt
sed 's#/.*##' _r528b_ON_pages.txt | sort -u > _affected_r528b.txt
echo "changed: $(wc -l < _r528b_ON_pages.txt) pages / $(wc -l < _affected_r528b.txt) modules"
rm -rf /tmp/r528b_onc; mkdir -p /tmp/r528b_onc
for c in $(cat _affected_r528b.txt); do cp -r /tmp/r528b_on/$c /tmp/r528b_onc/; done
rm -rf _r528b_ON_pages; cp -r /tmp/r528b_onc _r528b_ON_pages
cd ../reference/tests && echo "[$(date +%T)] prescore" && python3 ../../outputs/_s51_prescore.py /tmp/r528b_onc > ../../outputs/_r528b_prescore.log 2>&1; tail -1 ../../outputs/_r528b_prescore.log
echo "[$(date +%T)] done"
