#!/bin/bash
# Session 29 Round 3 PICK — the empty-task-bundle headwalk census over every Claude-dir module (4 shards, WSL).
set -u
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
O=../../outputs
cp $O/_s29_r411_codes.txt $O/_s29_r3_codes.txt
split -n l/4 -d $O/_s29_r3_codes.txt $O/_s29_r3_codes_
for i in 00 01 02 03; do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s29_r3_headwalk.cjs $(cat $O/_s29_r3_codes_$i) > $O/_s29_r3_headwalk_$i.log 2>&1 ) &
done
wait
cat $O/_s29_r3_headwalk_0?.log | grep -v '^SUMMARY\|^BY \|^  ' > $O/_s29_r3_headwalk_rows.tsv
echo "rows $(wc -l < $O/_s29_r3_headwalk_rows.tsv)"
grep -h '^SUMMARY' $O/_s29_r3_headwalk_0?.log
grep -h 'ASSEMBLE ERROR\|^ERR' $O/_s29_r3_headwalk_0?.log | head -5
