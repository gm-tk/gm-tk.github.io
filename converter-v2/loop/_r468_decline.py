#!/usr/bin/env python3
"""ROUND 468 decline record (session 42 Round 5) — LOOP_STATE.md: marker cleared, a Declined-classes entry (P4's r432 heading-member
gap below the floor; P5 class C), the follow-up line updated, the round-log line; the marker → archive. .bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-r468-decline.bak")
i = find("- **ROUND 468 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈15:55, session 42 Round 5 — r468 BUILT, PROBED, DECLINED on the floor and backed out "
        "(`outputs/_r468_declined.patch`); `git status` clean). LAST SHIPPED **r467** (260620.34); **LAST FULL = r460**; ledger **scoped "
        "#3**. Next: Round 6 PICK.")
k = find("- **Before r468: no round in flight**"); prior = L[k]; del L[k]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 5 (24 Sept 15:40 → 15:55) — THE LESSON MENU's WALT BLOCK TYPED AS A TOP-LEVEL HEADING (engine r468 — "
         "BUILT, PROBED, DECLINED on the floor, REVERTED; `outputs/_r468_declined.patch`) + the census P5 (`body:alert → body:free`) "
         "DECLINED as class C.** P4 (`menu:flat → body:free`, 313 blocks / 44 modules) split by `outputs/_s42_wtctx.py` "
         "(`_s42_wtctx_flatmenu.log`) into sub-shapes, each under the 10-module chrome floor: (a) the r432 implicit block refuses a lead "
         "typed as `[H2] We are learning about:` as a MEMBER (isMember takes body / sub head / h3–h5 only) — the fix "
         "(`lesson_overview_implicit.lead_heading_members` {h1, h2, h6}, `LESSONWALTH2_OFF`) moves exactly CBI1008 lessons 1 / 2 + "
         "PES1004 (3 pages / 2 modules; OFF 3217 identical) — the writer's ✅ tick is NOT a cause (stripped upstream); (b) TEDC401 / 402 "
         "write the lesson overview as a TABLE after an `[Overview]` alias (65 blocks / 7 pages / 2 modules — the alias path's buildSet "
         "sees one table item); (c) 152 blocks are the gold's generated labels (\"We are learning about:\", \"Whāinga Ako | Learning "
         "Intentions\") not in the WT (CBI / MXEX / HIS / COM / ENFUN). Re-open (a) + (b) together only if a later census finds the "
         "lesson-menu forms reach 10 modules. P5 (`_s42_wtctx_alert.log`, 1,292 blocks / 167 modules): 639 not in the WT, 222 plain "
         "`[body]`, 62 untagged — the developer's own boxing (class C); the tagged remainder is single-module forms (XGF9003 `[alert] "
         "[h2]` 31, XGF9001 `[alert rhs]` 15, XGF9006 `[alert.solid]` 11).")
k = find("- **(s42-r3) THE PLACEMENT CENSUS")
L[k] = L[k].replace("(P4) `menu:flat → body:free`", "(P4 — DECLINED s42-r5, sub-shapes under the floor) `menu:flat → body:free`", 1)
L[k] = L[k].replace("(P5) `body:alert → body:free`", "(P5 — DECLINED s42-r5, class C) `body:alert → body:free`", 1)
assert "DECLINED s42-r5, class C" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s42-r5 (engine r468, 24 Sept 15:40 → 15:55) · THE LESSON MENU's WALT BLOCK AS A TOP-LEVEL HEADING (the census P4 split: the r432 "
         "member test refuses `[H2]` leads) · BUILT, PROBED (OFF 3217 identical; ON 3 pages / 2 modules), DECLINED on the chrome floor, "
         "reverted · P5 (`body:alert → body:free`) DECLINED as class C · plateau 2 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 42 — Round 5 PICK (engine r468, DECLINED)\n\n" + marker + "\n" + prior + "\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
