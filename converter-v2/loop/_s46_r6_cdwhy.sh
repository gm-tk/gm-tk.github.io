#!/usr/bin/env bash
# Session 46 Round 6 — why the clickDrop builder refuses each declined clickDrop bundle (every return null in #clickDropItems and the
# shared member walk recorded with a short label; the member walk's foreign-tag guard records the tag). WSL.
export WHY_TYPE=clickDrop WHY_OUT=_s46_r6_cdwhy
L=""
for ln in 11027 11031 11033 11043 11046 11051 11066 11075 11082 11107 11144 11156 11258 11289 11301 11331 11365 11373 11375; do L="$L ;; $ln:\"L$ln\""; done
export WHY_LINES="2843:\"FOREIGN \" + tag + \" | \" + String(m.text ?? \"\").replace(/\\s+/g, \" \").slice(0, 50) ;; 11276:\"ROLE \" + String(sub ?? \"\").slice(0, 30)$L"
bash "$(dirname "$0")/_s46_shardrun.sh" _s46_whynull.cjs 8
cd "$(dirname "$0")/../reference/tests" && node ../../outputs/_s46_whynull.cjs --merge 8
