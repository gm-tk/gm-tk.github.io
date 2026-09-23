#!/usr/bin/env python3
"""ROUND 456 finalise — LOOP_STATE.md edits (the r454 pattern): clear the in-flight marker, LAST SHIPPED, plateau, AppVersion
history, round-log line, next-session line; append the round record to the archive. A .pre-r456-finalise.bak is kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(P, P + ".pre-r456-finalise.bak")
s = io.open(P, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 456 IN FLIGHT — NOT PROVEN**"); j = find("- Before r456: **no round in flight**"); assert j == i + 1
marker = L[i]
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈10:05, session 41 Round 4 — r456 SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r456** (260620.26); **LAST FULL = the r452 state**; ledger **scoped #3** since it (5 of headroom)."]
k = find("- LAST SHIPPED: **r454**")
L[k] = L[k].replace("- LAST SHIPPED: **r454**", "- Before it: **r454**", 1)
L.insert(k, "- LAST SHIPPED: **r456** (build 260620.26, 24 Sept ≈09:55, session 41 Round 4 — THE MID-PAGE LESSON HEADING OPENS ITS LESSON PAGE, `MIDLESSON_OFF`; 22 modules, Claude pages 2676 → 2717; SCOPED, **scoped #3 since the r452 FULL**; **skeleton 54.7680 % @ 2487 → 54.8705 % @ 2520 (+0.1025pp; the pre-existing population +0.1177pp)**, **≥50 1575** (+26), **≥75 270** (+5), ≥90 24, RAW 38.878 %; cs 16024 / 199 / 840 / 24 (exact +169); body 61 / 5 / 176 / 239 (+1 NAMED); clean 2663 / 2709 (NAMED); leak 75 / 46 (pages +1 NAMED); re-pairing dips MXDI301_02.0 / GEO1004_1_0 / MXDB301_6.0 / COM1005_3_0 / MXFL202_5.0 and 4 lost pairs NAMED; `gate_baseline.json` at r456; `outputs/_r456_sk_final.json`; the miner 196 CANDIDATE @ 2520).")
k = find("- Plateau window (§4): **0 of 3** — r454")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r454", "- Plateau window (§4): **0 of 3** — r456 predicted a move and delivered +0.1025pp; r455 declined (neither); r454", 1)
k = find("- Standing facts: AppVersion 260620.25")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.25 (r454", "- Standing facts: AppVersion 260620.26 (r456 the mid-page lesson heading — session 41 Round 4, 24 Sept); before it 260620.25 (r454", 1)
k = find("## Round log")
L.insert(k + 1, "- s41-r4 (engine r456, build 260620.26, 24 Sept ≈09:35 → ≈10:05) · THE MID-PAGE LESSON HEADING OPENS ITS LESSON PAGE (the recognition lane — Round 1's under-split census; `[H1] Lesson Four: …` / `[H2] Lesson 2 …` / black `[LESSON 5]` with no `[End page]`) · `MIDLESSON_OFF`, 22 modules, +41 pages · SHIPPED · scaffold 54.7680 @ 2487 → 54.8705 @ 2520 (+0.1025pp; pre-existing +0.1177pp), ≥50 +26, ≥75 +5, cs exact +169 · three gate movers NAMED (flags / a leak moving with split pages) · scoped #3.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("census 552 / 545 / **2,676** pages / **2,487** pairs", "census 552 / 545 / **2,717** pages / **2,520** pairs", 1).replace("LAST SHIPPED **r454** (260620.25); LAST FULL = the **r452 state**; ledger scoped #2;", "LAST SHIPPED **r456** (260620.26); LAST FULL = the **r452 state**; ledger scoped #3;", 1)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 41 — Round 4 PICK (engine r456) + what shipped\n\n" + marker + "\n- **What shipped (r456, 260620.26):** PageSplitter pre-scan + run-time opener (`page_split.mid_page_lesson_heading`); OFF 3218 / 3218; ON 102 pages / 22 modules + 42 new; pre-score with re-pairing +2065.7 pp-sum in the 22 (the pre-existing pairs +245.2, 25 up / 5 down; 37 new at 53.9; 4 lost); scoped regen 22 + 12; disk = probe 216 / 216; scoped_ship decomposition: skeleton +0.10 / ≥50 +26 / ≥75 +5 / cs exact +169 IMPROVED, body ANY +1 / clean −0.01 / leak pages +1 NAMED (content moving with split pages; leak occurrences 75 held); post-ship suite green.\n")
out = "\n".join(L); tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(P))
