#!/usr/bin/env python3
"""Session 44 Round 10 — the KB-verification pass (no engine change): KB_AMALGAMATION_STATUS rows 7 / 15 / 27 updated from UNVERIFIED;
LOOP_STATE.md round log. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
K = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); shutil.copyfile(K, K + ".pre-s44-r10.bak")
s = io.open(K, encoding="utf-8").read()
reps = [
 ("**UNVERIFIED** — the sweep's `<hN><span>` hits (360 Claude pages) are dominated by the canonical overview-menu `<h4><span>` (67); a body-region probe would settle it",
  "**LIVE — VERIFIED 2026-09-25 (session 44 Round 10, `outputs/_s44_r10_kbverify.py`, the #body region only):** every Claude body-heading `<span>` is either a Languages script span (`ch-text` / `jp-text` — the c92 CJK rule, CHFUN05 / JPFUN01 / JPN1004) or the writer's `infoTrigger` hover (18 occ); no generic span. (Was: UNVERIFIED — the sweep's `<hN><span>` hits (360 Claude pages) were the canonical overview-menu `<h4><span>`.)"),
 ("**UNVERIFIED** (mcq builder r305 — check its shuffle default)",
  "**LIVE — VERIFIED 2026-09-25 (session 44 Round 10):** Claude emits `noShuffle` on 0 widget roots (the gold 26: dragAndDrop 22 / memoryGame 4) — never without a request."),
 ("**UNVERIFIED** (dropDown builder r294 — check its layout choice)",
  "**PARTIAL — measured 2026-09-25 (session 44 Round 10):** the builder ships BOTH forms by shape — 13 `layout=\"paragraph\"` and ≈ 10 list (no-layout, KB 03C's standalone Q–A form) roots; the per-shape check (is every standalone pair a list?) not done — the gold ships 152 paragraph / 3 standard / 4 scatter."),
]
for a, b in reps:
    assert s.count(a) == 1, a[:50]
    s = s.replace(a, b)
io.open(K, "w", encoding="utf-8", newline="\n").write(s); print("KB status ok")
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s44-r10.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("## Round log")]; assert len(k) == 1
L.insert(k[0] + 1, "- s44-r10 (no engine change, 25 Sept 03:00 → 03:10) · a KB-VERIFICATION pass over the UNVERIFIED rows (`_s44_r10_kbverify.py`): "
         "c7 (no span in body h2–h5) LIVE — every body-heading span is a c92 script span or an infoTrigger; c15 (noShuffle only on request) LIVE — "
         "0 Claude roots; c27 (dropQuiz standalone pairs → list) PARTIAL — the builder ships both forms by shape; c66 (acks titles verbatim) not "
         "measured · `KB_AMALGAMATION_STATUS.md` rows 7 / 15 / 27 updated · plateau 0 of 3 (neither).")
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("LOOP_STATE ok", os.path.getsize(S))
