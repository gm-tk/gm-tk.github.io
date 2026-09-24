#!/usr/bin/env bash
# SESSION 43 — the media-aware widget text-loss census (`_s43_widgetloss2.cjs`: every lost PART tagged media-label vs learner text,
# with its source), 8 shards over every scored module. WSL: bash _s43_wl2_run.sh [TAG]
cd "$(dirname "$0")/../reference/tests"; O=../../outputs
TAG="${1:-}"
python3 -c "import _corpus,os; r=os.path.join('..','..','..','01-Claude_Modules_'); print('\n'.join(_corpus.gate_mods(r)))" > $O/_s43_wl_modules.txt
rm -f $O/_s43_wl2_shard*.json
for k in 0 1 2 3 4 5 6 7; do
  STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs $O/_s43_widgetloss2.cjs --shard $k 8 $(cat $O/_s43_wl_modules.txt) > $O/_s43_wl2_shard$k.log 2>&1 &
done; wait
node $O/_s43_widgetloss2.cjs --merge
if [ -n "$TAG" ]; then mv $O/_s43_widgetloss2.json $O/_s43_widgetloss2_$TAG.json; fi
tail -q -n 1 $O/_s43_wl2_shard*.log | head -2
echo "[$(date +%T)] WL2_DONE"
