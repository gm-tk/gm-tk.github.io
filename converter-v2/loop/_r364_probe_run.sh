#!/bin/bash
# usage: _r364_probe_run.sh OFF|ON   — runs the 4 shards in parallel under WSL, logs to outputs/_r364_probe_<mode>_<k>.log
cd "$(dirname "$0")/../reference/tests" || exit 1
mode=$1
for k in 0 1 2 3; do
  codes=$(tr '\n' ' ' < ../../outputs/_r364_shard$k.txt)
  if [ "$mode" = "OFF" ]; then
    ( IDHEAD_OFF=1 STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_r364_probe.cjs $codes --quiet > ../../outputs/_r364_probe_${mode}_$k.log 2>&1 ) &
  else
    ( STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_r364_probe.cjs $codes > ../../outputs/_r364_probe_${mode}_$k.log 2>&1 ) &
  fi
done
wait
echo "done $mode"
