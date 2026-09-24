#!/usr/bin/env python3
"""Session 45 Round 6 — record the PICK pass (no engine change; a prototype saved as a ride-along patch) in LOOP_STATE.md. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r6.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 6 (25 Sept ≈07:30 → 08:05 real clock) — a PICK pass on the hand-off-box lane, no engine change.** (1) **The "
         "accordion's BULLETED bold-lead panels** (WHY_UNBUILT__accordion item 1 / reason 2b — `• **Weed suppression** – If there are…`): "
         "prototyped as a D4 FALLBACK read only after the r278 reading yields no panels (a first version that widened the shared pattern broke "
         "XLP04 4.0's five built Materials / Activity accordions — a bulleted bold line INSIDE a panel became a new panel; the fallback order "
         "fixed it); probe OFF 0 changed, ON **9 pages / 4 modules, +8 accordions, 0 lost** (MXEX302 1 → 6, ENGS101 / XGF9003 / XLP05 +1) — "
         "under the 20-site shape floor alone → **saved as the ride-along patch `outputs/_r489_accbullet_declined.patch`** and reversed off "
         "the tree (the corpus was never regenerated). AGH1009 6.0 (the document's own example) is not reached — its bundle is not all-text, "
         "so it never enters D4; the doc's items 4 / 5 / 6 (empty trailing panel 9, an ordinary `[button]` 10, a one-row-table heading 8) are "
         "the natural batch to ride with it. (2) **The carousel's `Image #N:` banner list** (WHY_UNBUILT__carousel 4a — HPFUN103 / 203 / 302 "
         "/ 303 / 403 / 901 golds build the rotateBanner from it): 9 activities / 9 modules, under the floor — recorded. (3) **The gathering "
         "lever** (WHY_UNBUILT__INDEX A — two activities collected as one bundle: carousel + dropdown 18 / + flip card 16 …; modal 51; accordion "
         "46): three different situations with different answers (BLL110's banner + flip card the gold resolves three ways) — a multi-round "
         "gathering change, scoped not started. (4) clickDrop's refusals (350 'no item structure' across 589 records) and the ENFUN overview "
         "Te Reo title halves (not in the WT, class C) — recorded.")
k = find("## Round log")
L.insert(k + 1, "- s45-r6 (no engine change, 25 Sept ≈07:30 → 08:05) · a PICK pass on the hand-off boxes: the accordion bulleted bold lead "
         "prototyped (+8 accordions / 4 modules, 0 lost after the fallback-order fix) — under the floor → ride-along patch "
         "`_r489_accbullet_declined.patch`; the carousel `Image #N:` banner list 9 modules (below floor); the gathering lever scoped · plateau "
         "0 of 3 (neither).")
k = find("- **No round in flight** (25 Sept 2026 ≈07:25, session 45 Round 5")
L[k] = L[k].replace("Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages)",
                    "Ride-along patches `outputs/_r489_accbullet_declined.patch` (the accordion bulleted bold lead, 9 pages / +8 accordions), "
                    "`outputs/_r469_declined.patch` (alerts, 7 pages)", 1)
assert "_r489_accbullet_declined.patch" in L[k]
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
