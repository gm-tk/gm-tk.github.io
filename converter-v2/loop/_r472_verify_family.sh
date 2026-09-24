#!/usr/bin/env bash
# ROUND 472 — the flipCard verifier over the WHOLE flipCard family (OPERATING_GUIDE §0a — every module carrying the type,
# `_r472_family.txt`, 246 modules), guard OFF and ON, 4 shards each. WSL: bash _r472_verify_family.sh
cd "$(dirname "$0")/../reference/tests" || exit 1; O=../../outputs
rm -f $O/_r472_vf_*
split -n l/4 -d $O/_r472_family.txt $O/_r472_vf_codes_
for i in 00 01 02 03; do
  ( FLIPTEXTGUARD_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_flipcard.cjs $(cat $O/_r472_vf_codes_$i) > $O/_r472_vf_OFF_$i.log 2>&1 ) &
  ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs _verify_flipcard.cjs $(cat $O/_r472_vf_codes_$i) > $O/_r472_vf_ON_$i.log 2>&1 ) &
done; wait
for m in OFF ON; do
  echo "== $m"; grep -h '^TOTAL' $O/_r472_vf_${m}_0*.log
  awk '/^TOTAL/{for(i=1;i<=NF;i++){if($i~/^[0-9]+[:,.]?$/){gsub(/[:,.]/,"",$i); a[$(i+1)]+=$i}}} END{for(k in a) printf "  sum %s %d\n", k, a[k]}' $O/_r472_vf_${m}_0*.log
  grep -h 'RESULT' $O/_r472_vf_${m}_0*.log | sort | uniq -c
done
echo "[$(date +%T)] VF_DONE"
