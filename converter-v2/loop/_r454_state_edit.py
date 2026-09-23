#!/usr/bin/env python3
"""ROUND 454 finalise — LOOP_STATE.md edits (the r453 pattern): clear the in-flight marker, the LAST SHIPPED row, the plateau
line, the AppVersion history, the round-log line, the next-session line, and MOVE the round's PICK section to the archive.
A .pre-r454-finalise.bak is kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(P, P + ".pre-r454-finalise.bak")
s = io.open(P, encoding="utf-8").read(); L = s.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
i = find("- **ROUND 454 IN FLIGHT — NOT PROVEN**"); j = find("- Before r454: **no round in flight**"); assert j == i + 1
L[i:j + 1] = ["- **No round in flight** (24 Sept 2026 ≈09:25, session 41 Round 2 — r454 SHIPPED and committed; the in-flight marker is cleared). LAST SHIPPED **r454** (260620.25); **LAST FULL = the r452 state**; ledger **scoped #2** since it (6 of headroom)."]
k = find("- LAST SHIPPED: **r453**")
L[k] = L[k].replace("- LAST SHIPPED: **r453**", "- Before it: **r453**", 1)
L.insert(k, "- LAST SHIPPED: **r454** (build 260620.25, 24 Sept ≈09:15, session 41 Round 2 — THE RED-WRAPPED `[Activity: Embedded]` MARKER, KB 07B, `ACTMARKRED_OFF`; 15 pages / 4 TRR modules; SCOPED, **scoped #2 since the r452 FULL**, scoped_ship PASS; **skeleton 54.7079 → 54.7680 % @ 2487 (+0.0600pp; 14 up / 1 down — TRR102_1.0 NAMED, letter ids vs the KB decimal)**, ≥50 1549, ≥75 265, ≥90 23, RAW 38.726 %; cs 15855 / 199 / 840 / 24; body 59 / 5 / 176 / 238; clean 2623 / 2668; leak 75 / 45 — all EXACT; `gate_baseline.json` at r454; `outputs/_r454_sk_final.json`; the miner 196 CANDIDATE).")
k = find("- Plateau window (§4): **0 of 3 — RESET by r453**")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3 — RESET by r453**", "- Plateau window (§4): **0 of 3** — r454 predicted a move and delivered +0.0600pp (the window stays reset); r453 RESET it", 1)
k = find("- Standing facts: AppVersion 260620.24")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.24 (r453", "- Standing facts: AppVersion 260620.25 (r454 the red-wrapped [Activity: Embedded] marker — session 41 Round 2, 24 Sept); before it 260620.24 (r453", 1)
k = find("## Round log")
L.insert(k + 1, "- s41-r2 (engine r454, build 260620.25, 24 Sept 08:58 → ≈09:25) · THE RED-WRAPPED `[Activity: Embedded]` MARKER (the r453 follow-up; KB 07B — `activityMarkerRe` anchored at the cell start never saw the red-run marker, so the bilingual activity gather was dead code) · `ACTMARKRED_OFF`, 15 pages / 4 modules · SHIPPED (scoped_ship PASS) · scaffold 54.7079 → 54.7680 (+0.0600pp; 14 up / 1 down named) · in-round repair: the bare box went all-down until the KB 07D row wrapper + decimal number · scoped #2.")
k = find("**Next session starts with:**")
L[k] = L[k].replace("LAST SHIPPED **r453** (260620.24); LAST FULL = the **r452 state**; ledger scoped #1; plateau **0 of 3**.", "LAST SHIPPED **r454** (260620.25); LAST FULL = the **r452 state**; ledger scoped #2; plateau **0 of 3**.", 1)
k = find("## Session 41 — Round 2 PICK (engine r454)")
e = k + 1
while e < len(L) and not L[e].startswith("## "): e += 1
block = L[k:e]
title = "Session 41 — Round 2 PICK (engine r454) + what shipped"
L[k:e] = ["## Session 41 — Round 2 (engine r454, build 260620.25) — THE RED-WRAPPED `[Activity: Embedded]` MARKER — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md '" + title + "'; the one-line summary is the s41-r2 Round-log line below.", ""]
shipped = "\n- **What shipped (r454, 260620.25):** `BilingualBuilder.isActivityMarker` strips the red-run markers; `isRedOnlyActivityMarker` scopes the new behaviour; `ContentConverter` wraps such a box in `row > col-md-8 col-12` and numbers it `<lesson>.<k>`; the marker row ships as a `cv2-note`. Data `dual_language.activity_marker_red` {enabled, wrap, number}. OFF 3208 / 3208; ON 15 pages / 4 modules; the first probe (marker alone) 15 / 15 DOWN → with wrap + number 14 up / 1 down (+149.2 pp-sum); scoped_ship PASS; post-ship gates EXACT but the skeleton (+0.0600pp)."
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## " + title + "\n\n" + "\n".join(block[1:]) + shipped + "\n")
out = "\n".join(L); tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("LOOP_STATE.md", len(s.encode("utf-8")), "->", os.path.getsize(P))
