#!/usr/bin/env bash
# Session 51 — run any in-memory probe script over every module (or a list) in 4 parallel shards (WSL).
# Usage: bash _s51_par.sh SCRIPT.cjs TAG [LISTFILE] [ENV=VAL ...]  → outputs/_TAG.log (the shards concatenated, sorted)
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs; S="$1"; TAG="$2"; LIST="${3:-$O/_s50_par_codes.txt}"; shift 3 2>/dev/null || shift $#
grep -v '^\s*$' "$LIST" | tr -d '\r' | sort -u > $O/_${TAG}_codes.txt
split -n l/4 -d $O/_${TAG}_codes.txt $O/_${TAG}_codes_
for s in 00 01 02 03; do
  ( env "$@" STUB_OEMBED=1 timeout 1500 node --require ./_deflate_raw_polyfill.cjs $O/$S $(cat $O/_${TAG}_codes_$s) > $O/_${TAG}_$s.part 2>&1 ) &
done
wait
cat $O/_${TAG}_0?.part > $O/_${TAG}.log; rm -f $O/_${TAG}_0?.part $O/_${TAG}_codes_0?
echo "lines $(wc -l < $O/_${TAG}.log); errors $(grep -c 'ASSEMBLE ERROR' $O/_${TAG}.log)"
