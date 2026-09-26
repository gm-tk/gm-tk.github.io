#!/usr/bin/env bash
# s52 — run _s52_items_dump.cjs over every Claude-dir module in 4 shards (WSL); `wait`, never pgrep.
cd /mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests || exit 1
O=../../outputs
rm -rf $O/_s52_items; mkdir -p $O/_s52_items
split -n l/4 -d $O/_s52_allcodes.txt /tmp/_s52_items_sh_
for s in 00 01 02 03; do
  ( STUB_OEMBED=1 timeout 1500 node --require ./_deflate_raw_polyfill.cjs $O/_s52_items_dump.cjs $(cat /tmp/_s52_items_sh_$s) > $O/_s52_items_$s.log 2>&1 ) &
done
wait
echo "tsv files: $(ls $O/_s52_items | wc -l); errors: $(cat $O/_s52_items_0?.log | grep -c 'ASSEMBLE ERROR')"
