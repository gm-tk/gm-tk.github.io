#!/usr/bin/env bash
# session 40 — dump every bundle of one quiz type (QTYPE=typing …) whole, 4 shards → outputs/_s40_<QTYPE>.jsonl
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs; T="${QTYPE:-multiChoiceQuiz}"
for i in 00 01 02 03; do
  ( QTYPE="$T" STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s40_quizdump.cjs --quiet $(cat $O/_r447_codes_$i) > $O/_s40_${T}_dump_$i.log 2>&1 ) &
done
wait
grep -h '^QDUMP ' $O/_s40_${T}_dump_0*.log | sed 's/^QDUMP //' > $O/_s40_${T}.jsonl
wc -l < $O/_s40_${T}.jsonl
