#!/usr/bin/env bash
# Session 46 Round 2 — why the r278 D2 table reading (#accTablePanels) refuses each declined accordion table, corpus-wide. WSL.
export WHY_TYPE=accordion WHY_OUT=_s46_r2_why2
export WHY_LINES='3361:"D2 IMGNAME | " + String(url).slice(0, 60) ;; 3362:"D2 TWOIMG | " + cells.length + " cells" ;; 3371:"D2 EMPTYROW | " + JSON.stringify(row).slice(0, 80) ;; 3380:"D2 NOLEAD | " + kept.map((c) => String(c).replace(/\s+/g, " ").slice(0, 50)).join(" || ") ;; 3388:"D2 NOHEADBODY | " + JSON.stringify(kept).slice(0, 80) ;; 3389:"D2 TAGHEAD | " + String(head).slice(0, 60) ;; 3349:"D2 FEWROWS | " + rows.length'
bash "$(dirname "$0")/_s46_shardrun.sh" _s46_whynull.cjs 8
cd "$(dirname "$0")/../reference/tests" && node ../../outputs/_s46_whynull.cjs --merge 8
