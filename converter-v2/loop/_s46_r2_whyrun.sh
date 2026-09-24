#!/usr/bin/env bash
# Session 46 Round 2 — which member defeats the accordion's r278 member walk (#accMemberParts), corpus-wide. WSL.
export WHY_TYPE=accordion WHY_OUT=_s46_r2_why
export WHY_LINES='2843:"FOREIGN " + tag + " | " + String(m.text ?? "").replace(/\s+/g, " ").slice(0, 70) + " || " + String(m.blackAfter ?? "").replace(/\s+/g, " ").slice(0, 50) ;; 2796:"DEFER " + tag + " | " + String(m.text ?? "").slice(0, 60) ;; 2674:"DELIMTEXT red/url | " + String(m.text ?? "").slice(0, 50) + " || " + text.slice(0, 50) ;; 2765:"BODYRED | " + raw.slice(0, 70) ;; 2701:"HEADRED " + tag + " | " + raw.slice(0, 60) ;; 2734:"IMGBAIL | " + url.slice(0, 60) ;; 2761:"MEDIABAIL " + tag + " | " + raw.slice(0, 50)'
bash "$(dirname "$0")/_s46_shardrun.sh" _s46_whynull.cjs 8
cd "$(dirname "$0")/../reference/tests" && node ../../outputs/_s46_whynull.cjs --merge 8
