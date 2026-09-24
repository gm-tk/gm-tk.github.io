#!/usr/bin/env python3
"""ROUND 469 / 469b decline record (session 42 Round 7) — two never-sized r447 follow-ups built, probed and backed out on the floor;
plus the loss-ledger / per-family lane results. LOOP_STATE.md: marker cleared, a Declined-classes entry, the two r447 follow-up lines
struck to it, the round-log line; the marker → archive. .bak kept. Run under WSL."""
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
shutil.copyfile(S, S + ".pre-r469-decline.bak")
i = find("- **ROUND 469 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈17:15, session 42 Round 7 — r469 / r469b BUILT, PROBED, DECLINED on the floor, backed "
        "out (`outputs/_r469_declined.patch`, `_r469b_declined.patch` — RIDE-ALONG candidates); `git status` clean). LAST SHIPPED **r467** "
        "(260620.34); **LAST FULL = r460**; ledger **scoped #3**.")
k = find("- **Before r469: no round in flight**"); prior = L[k]; del L[k]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 42 Round 7 (24 Sept ≈17:00 → 17:15) — the two never-sized r447 follow-ups (engine r469 / r469b — BUILT, PROBED, "
         "DECLINED on the 20-page body floor, REVERTED; the patches are RIDE-ALONG candidates for the next round in their area, §2) + the "
         "loss-ledger / per-family lanes.** (r469) `#alertTitleHeading` may not cross a `</p>` (`alert_title_heading.no_cross_p`, "
         "`ALERTHCROSS_OFF`): OFF 3217 identical, ON **7 pages / 3 modules** (ANZH301_3 / _6, ANZH302_3 / _6, ENGC403_7 / _9 / _11). "
         "(r469b) the button's following-URL absorb skips a MEDIA tag's URL (`absorb_following_url.skip_media_tags`, `BTNURLMEDIA_OFF` — "
         "the image line no longer vanishes into the button): ON **10 pages / 9 modules** (CEDK401_0, HIS1002_9, HPRE203_3, MXDI201_6, "
         "MXDI202_1 / _2, MXEX302_7, SSOG105_7, TWHA906_0, XGF9004_14). Both are content / correctness fixes with no over-reach risk — ship "
         "either with the next round that touches alerts or buttons. Loss ledger on r467 (`_s42_r7_lossfam.log`): BLL2 5.2 % / BLL1 4.9 % "
         "/ HIS1 3.5 % / TRR1 3.3 % of the loss; HIS1's scoped miner (`_s42_r7_miner_his.md`) → the lesson-menu column (gold `col-12` "
         "vs Claude `col-md-8 col-12`, 51 pages / 7 modules corpus-wide, HIS1003 / 1004 on the KB 01B example's `col-md-8`) DECLINED "
         "(a 7-module dialect split within HIS, the KB example on Claude's side); TRR1's (`_s42_r7_miner_trr.md`) → the bilingual "
         "section box swallows the section (gold: title + instruction + widgets in the box, the teaching content outside) — the r455 / "
         "r453 follow-up, each TRR module its own form, not a one-round class.")
for pre in ("- **(r447) The following-URL absorb takes an `[Image]` line's URL.**", "- **(r447) The r61 alert-title regex backtracks across elements.**"):
    k = find(pre)
    parts = L[k][2:].split("**", 2)
    L[k] = "- ~~**" + parts[1] + "**~~ → **MEASURED s42-r7: below the floor — a ride-along patch** (see Declined classes, Session 42 Round 7). Was:" + parts[2]
k = find("## Round log")
L.insert(k + 1, "- s42-r7 (engine r469 / r469b, 24 Sept ≈17:00 → 17:15) · the two r447 follow-ups sized: the alert-title regex no longer "
         "crosses `</p>` (7 pages / 3 modules) and a media tag's URL is never a button's href (10 pages / 9 modules) · BUILT, PROBED, "
         "DECLINED on the floor, reverted (ride-along patches kept) · also the loss-ledger lane (HIS1 lesson-menu column declined; TRR1 "
         "box boundary recorded) · plateau 2 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 42 — Round 7 PICK (engine r469 / r469b, DECLINED)\n\n" + marker + "\n" + prior + "\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
