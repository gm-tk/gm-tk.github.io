#!/usr/bin/env python3
"""Session 45 Round 8 — record the PICK pass (no engine change) in LOOP_STATE.md + KB row 27. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r8.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 8 (25 Sept ≈08:40 → 08:55 real clock) — a PICK pass, no engine change.** (1) **The chrome title row's "
         "Bilingual group** (DIFF_QUEUE F1: Bilingual lesson pages carry two `h1` spans in the gold 1.00, Claude 0.64): the 27 pages are "
         "PMT101 / TRR114 / 115 / 116 / 203 / 301 / 304 lessons shipping only the Māori module title; the gold's English half (TRR116 'Sight "
         "Words', TRR115 'Sounds') is NOT in the Writers Template (class C — decision 2 / r321 already gives both titles where the WT has them); "
         "PMT101's 'genealogy' is one module's `[H2] Genealogy: ║ Whakapapa:` heading pair. (2) **KB c27 VERIFIED LIVE** (`_s45_r8_c27.py`): "
         "every Claude `dropQuiz layout=\"paragraph\"` item (74 in 13 roots) is a sentence the dropdown completes — the KB's paragraph case — "
         "and the 10 no-layout roots are the list form; no standalone Q&A pair ships as paragraph. (3) The KB 01F / 01E tag tables re-read: "
         "`rhetorical_question` has no writer tag and no gold class; the rest captured.")
k = find("## Round log")
L.insert(k + 1, "- s45-r8 (no engine change, 25 Sept ≈08:40 → 08:55) · a PICK pass: the Bilingual lesson-title half (27 pages / 7 MTK modules — the "
         "English title not in the WT, class C); KB c27 verified LIVE (74 paragraph items all sentence completions; `KB_AMALGAMATION_STATUS.md` "
         "row 27); the 01F / 01E tag tables re-read · plateau 0 of 3 (neither).")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
K = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); shutil.copyfile(K, K + ".pre-s45-r8.bak")
KL = io.open(K, encoding="utf-8").read().split("\n")
i = [j for j, l in enumerate(KL) if l.startswith("| 27 | DropQuiz standalone pairs use list layout")]; assert len(i) == 1
KL[i[0]] = KL[i[0]].replace("| **PARTIAL — measured 2026-09-25 (session 44 Round 10):**",
    "| **LIVE — VERIFIED 2026-09-25 (session 45 Round 8, `outputs/_s45_r8_c27.py`): every one of the 74 items in Claude's 13 "
    "`layout=\"paragraph\"` roots is a sentence the dropdown completes (the KB 03C paragraph case); the 10 no-layout roots are the list form — "
    "no standalone Q&A pair ships as paragraph.** Was: **PARTIAL — measured 2026-09-25 (session 44 Round 10):**", 1)
assert "VERIFIED 2026-09-25 (session 45 Round 8" in KL[i[0]]
io.open(K + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(KL)); os.replace(K + ".tmp", K)
print("ok", os.path.getsize(S))
