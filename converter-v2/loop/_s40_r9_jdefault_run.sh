#!/usr/bin/env bash
# SESSION 40 ROUND 9 — run the journal-default recorder over every Claude-dir module, 4 shards (WSL). Output: _s40_r9_jdefault.log
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
ls -d ../../../01-Claude_Modules_/*/*/ | xargs -n1 basename | sort -u > $O/_s40_r9_codes.txt
split -n l/4 -d $O/_s40_r9_codes.txt $O/_s40_r9_codes_
for i in 00 01 02 03; do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s40_r9_jdefault.cjs $(cat $O/_s40_r9_codes_$i) > $O/_s40_r9_jdefault_$i.log 2>&1 ) &
done
wait
cat $O/_s40_r9_jdefault_0*.log > $O/_s40_r9_jdefault.log
echo "JDEF lines: $(grep -c '^JDEF' $O/_s40_r9_jdefault.log)  errors: $(grep -c 'ERR\|ASSEMBLE ERROR' $O/_s40_r9_jdefault.log)"
