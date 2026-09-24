#!/usr/bin/env bash
# SESSION 43 PICK — the r352 widget text-loss census re-run over EVERY scored module (every built bundle of every type:
# is each member text run of >= 3 words on some page of the module?). 8 shards, WSL, from reference/tests.
# Usage: bash _s43_wl_run.sh [TAG]   (TAG names the output json: _s43_widgetloss[_TAG].json; env vars pass through to node)
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
TAG="${1:-}"
python3 -c "import _corpus,os; r=os.path.join('..','..','..','01-Claude_Modules_'); print('\n'.join(_corpus.mods(r)))" > $O/_s43_fam_modules.txt
wc -l < $O/_s43_fam_modules.txt
rm -f $O/_s43_fam_shard*.json
for k in 0 1 2 3 4 5 6 7; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s43_family.cjs --shard $k 8 $(cat $O/_s43_fam_modules.txt) > $O/_s43_fam_shard$k.log 2>&1 &
done; wait
node $O/_s43_family.cjs --merge
if [ -n "$TAG" ]; then mv $O/_s43_family.json $O/_s43_family_$TAG.json; fi
tail -q -n 1 $O/_s43_fam_shard*.log
echo "[$(date +%T)] WL_DONE"
