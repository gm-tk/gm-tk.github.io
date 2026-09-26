#!/usr/bin/env bash
# Session 51 (a copy of _s50_probe_par.sh + the _s51_flagon.cjs preload: FLAGON=… turns one parked data flag ON) — the in-memory probe (_r448_probe.cjs) over a code list in 4 parallel shards (WSL).
# Usage: bash _s50_probe_par.sh TAG LISTFILE [ENV=VAL ...]   → outputs/_TAG_{00..03}.log + a TOTAL line
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs; TAG="$1"; LIST="$2"; shift 2
grep -v '^\s*$' "$LIST" | tr -d '\r' | sort -u > $O/_${TAG}_codes.txt
split -n l/4 -d $O/_${TAG}_codes.txt $O/_${TAG}_codes_
for s in 00 01 02 03; do
  ( env "$@" STUB_OEMBED=1 timeout 1500 node --require ./_deflate_raw_polyfill.cjs --require $O/_s51_flagon.cjs $O/_r448_probe.cjs ${PROBE_QUIET:+--quiet} ${PROBE_SAVE:+--save $PROBE_SAVE} $(cat $O/_${TAG}_codes_$s) > $O/_${TAG}_$s.log 2>&1 ) &
done
wait
awk '/: identical [0-9]+ \/ changed [0-9]+/ { split($0,a,"identical "); split(a[2],b," / changed "); i+=b[1]; c+=b[2]+0; if (b[2]+0>0) print "CHANGED:", $0 } END { print "TOTAL identical " i " / changed " c }' $O/_${TAG}_0?.log
grep -h -i 'error\|no gold dir' $O/_${TAG}_0?.log | head -5
