#!/usr/bin/env bash
# Session 46 Round 2 — why the explicit [accordion N] panel reading (D1 in #accResolvePanels) refuses, corpus-wide. WSL.
export WHY_TYPE=accordion WHY_OUT=_s46_r2_why3
export WHY_LINES='2927:"D1 OVERLONG" ;; 2938:"D1 LEADBEFORE | " + p.role + " " + String(p.text ?? p.filename ?? "").slice(0, 50) ;; 2941:"D1 PUSHFAIL | " + p.role'
export WHY_INJECT='2945:"D1 FINAL | " + panels.map((p) => (p.head ? "H" : "-") + p.parts.length).join(",") + " | " + panels.map((p) => String(p.head).slice(0, 20)).join(" / ")'
bash "$(dirname "$0")/_s46_shardrun.sh" _s46_whynull.cjs 8
cd "$(dirname "$0")/../reference/tests" && node ../../outputs/_s46_whynull.cjs --merge 8
