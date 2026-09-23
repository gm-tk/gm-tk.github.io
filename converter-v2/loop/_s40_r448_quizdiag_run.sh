#!/usr/bin/env bash
# session 40 r448 — the quiz-bundle member diag over every Claude-dir module, 4 shards (the r447 codes split)
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs
for i in 00 01 02 03; do
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s40_r448_quizdiag.cjs --quiet $(cat $O/_r447_codes_$i) > $O/_s40_r448_quizdiag_$i.log 2>&1 ) &
done
wait
cat $O/_s40_r448_quizdiag_0*.log > $O/_s40_r448_quizdiag_all.log
grep -c '^BUNDLE' $O/_s40_r448_quizdiag_all.log
