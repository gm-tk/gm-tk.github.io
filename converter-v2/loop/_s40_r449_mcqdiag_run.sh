#!/usr/bin/env bash
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
for i in 00 01 02 03; do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s40_r449_mcqdiag.cjs --quiet $(cat $O/_r447_codes_$i) > $O/_s40_r449_mcqdiag_$i.log 2>&1 ) &
done
wait
grep -h '^MCQDUMP ' $O/_s40_r449_mcqdiag_0*.log | sed 's/^MCQDUMP //' > $O/_s40_r449_mcq.jsonl
wc -l < $O/_s40_r449_mcq.jsonl
