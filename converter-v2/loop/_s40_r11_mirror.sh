#!/usr/bin/env bash
# SESSION 40 ROUND 11 (DECLINED on measurement — the stock image's own words as a caption; no engine change) — the loop mirror:
# README row + the round's scripts / logs + the loop md files. The r452 pattern. Run from anywhere.
cd "$(dirname "$0")/../.." || exit 1
L=pageforge-site/converter-v2/loop
O=CONVERTER_V2/outputs
ROW='| `_s40_r11_{trace,stockcap}.cjs` / `_s40_r11_stockcap_run.sh` / `_s40_r11_{state_edit,condense}.py` / `_s40_r11_mirror.sh` / `_s40_r11_stockcap.log` / `_s40_r11_codes.txt` | `CONVERTER_V2/outputs/` | **Session 40 Round 11 (2026-09-24) — THE STOCK IMAGE'"'"'S OWN WORDS AS A CAPTION — DECLINED on measurement** — the item trace (TEDC402 "avatar Tina": the `[Image]` item'"'"'s own words beside its iStock hyperlink), the stock-caption census over all 545 (869 captions; the gold keeps 533 of the 842 own-word ones; no length bucket reaches 0.60 lacking), the LOOP_STATE record + the §5d condense #5, and this mirror. |'
ANCHOR='| `_measure_r271_variations.cjs` (the census'
if grep -qF '`_s40_r11_{trace,stockcap}.cjs`' $L/README.md; then echo "README row already present"; else
  awk -v row="$ROW" -v anchor="$ANCHOR" 'BEGIN{done=0} { if (!done && index($0, anchor)==1) { print row; done=1 } print } END{ if(!done) exit 3 }' $L/README.md > $L/README.md.new && mv $L/README.md.new $L/README.md && echo "README row inserted"
fi
[ -f $L/README.md.new ] && { echo "ANCHOR MISSED — README.md.new left behind"; rm -f $L/README.md.new; }
n=0
for f in _s40_r11_trace.cjs _s40_r11_stockcap.cjs _s40_r11_stockcap_run.sh _s40_r11_state_edit.py _s40_r11_condense.py _s40_r11_mirror.sh _s40_r11_stockcap.log _s40_r11_codes.txt; do [ -f "$O/$f" ] && cp "$O/$f" "$L/$f" && n=$((n+1)); done
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md; do cp "$f" "$L/$f"; n=$((n+1)); done
echo "mirrored $n files"
bad=0
for f in LOOP_STATE.md LOOP_STATE_ARCHIVE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md; do cmp -s "$f" "$L/$f" || { echo "MIRROR DIFFERS: $f"; bad=1; }; done
[ $bad = 0 ] && echo "mirror byte-identical (cmp)"
