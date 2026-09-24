#!/usr/bin/env python3
"""Session 45 Round 7 — record the PICK pass (no engine change; the §1g placement lane) in LOOP_STATE.md. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r7.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 7 (25 Sept ≈08:05 → 08:40 real clock) — a PICK pass on the §1g placement lane + the family-dialect lane, no "
         "engine change.** (1) **The lesson menu Claude leaves EMPTY where the gold's has text** (`_s45_r7_emptymenu.py`): 312 lesson pages / "
         "72 modules — 246 'absent' (mostly the r436-declined repeated overview menu: KB 01B makes the empty lesson menu correct there) and **66 "
         "pages / 23 modules where the gold's menu text sits in Claude's BODY** (HIS1003 / HIS1004 9 each, XGF9006 7, COM1005 7, COM1006 5, "
         "TEDC401 5, MXEX101 4, CBI1008 / CBI1009 3 each …). Each family writes it differently (`_s45_r7_wtform.py`): HIS `[Lesson Overview] "
         "<title>` → `[Alert box] In this lesson you are…` → `[Lesson content]` (the gold drops the alert and keeps the sentence in the menu; "
         "r147 ends the menu section at an alert because the CED `[alert.top]` resources stay in the body — CEDO501); TEDC `[Lesson content]` → "
         "`[Overview]` → a one-cell LI / SC table; COM `[A fancy looking box]` + `[Body] We are learning…` + the writer's 'a similar box at the "
         "start of each lesson'; CBI `[Alert solid] Blue box` + `[H4] We are learning about:`; XGF9006 `[H3] Learning Intentions and Success "
         "Criteria` + `[Insert accordion]`; MXEX101 `[Lesson Overview]` → `[H2] Understand` (the heading ends the section). (2) **The unifying "
         "rule is NOT supported** (`_s45_r7_waltbody.py`): every lesson page with an empty Claude menu and a WALT lead in its body — the gold "
         "keeps the sentence in the BODY 70, the MENU 46, drops it 73 (80 modules); the only clean sub-form is HIS1003 / HIS1004's `[Alert box]` "
         "(19 pages, all menu) — a two-module family dialect under the floor, against SSOG105's alert-early form (6, body) — recorded. (3) "
         "TEDC4's own view (`_s45_r7_tedc4.log`, 16 pages at 41.9 %): the in-body LI block above; its title row `h1>span «Clickwise: …»` is the "
         "module title the gold repeats on lessons.")
k = find("## Round log")
L.insert(k + 1, "- s45-r7 (no engine change, 25 Sept ≈08:05 → 08:40) · a PICK pass on the placement + family lanes: Claude's empty lesson menu vs "
         "the gold's (312 pages; 66 / 23 modules with the text in Claude's BODY — six different writer forms); the gold's placement of a WALT "
         "lead found in Claude's body has no consensus (body 70 / menu 46 / absent 73) — no rule; HIS1003 / 1004's `[Alert box]` form 19 pages, "
         "a family dialect under the floor · plateau 0 of 3 (neither).")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
