#!/usr/bin/env bash
cd "$(dirname "$0")/../reference/tests" || exit 1
STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs ../../outputs/_s42_r10_dd2dump.cjs $(cat ../../outputs/_s42_r10_codes.txt) > ../../outputs/_s42_r10_dd2dump.json 2> ../../outputs/_s42_r10_dd2dump.err
echo "rc=$? $(wc -c < ../../outputs/_s42_r10_dd2dump.json) bytes"
