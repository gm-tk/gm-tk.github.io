#!/usr/bin/env bash
# Session 50 — run an in-memory engine probe (.cjs in outputs/) over a code list in 4 parallel shards (WSL), wait for all
# (PIDs, never pgrep), and concatenate the shard outputs.  Usage: bash _s50_par.sh PROBE.cjs LISTFILE OUTLOG [ENV=VAL ...]
cd "$(dirname "$0")/../reference/tests" || exit 1
O=../../outputs; PROBE="$1"; LIST="$2"; OUT="$3"; shift 3
grep -v '^\s*$' "$LIST" | tr -d '\r' | sort -u > "$O/_s50_par_codes.txt"
split -n l/4 -d "$O/_s50_par_codes.txt" "$O/_s50_par_codes_"
pids=()
for s in 00 01 02 03; do
  env "$@" STUB_OEMBED=1 timeout 1500 node --require ./_deflate_raw_polyfill.cjs "$O/$PROBE" $(cat "$O/_s50_par_codes_$s") > "$O/_s50_par_$s.log" 2>&1 &
  pids+=($!)
done
for p in "${pids[@]}"; do wait "$p"; done
cat "$O"/_s50_par_0?.log > "$OUT"
echo "done: $(wc -l < "$OUT") lines -> $OUT"
