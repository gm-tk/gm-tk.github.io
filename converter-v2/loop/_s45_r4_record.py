#!/usr/bin/env python3
"""Session 45 Round 4 — record the PICK pass (no engine change: two classes DECLINED) in LOOP_STATE.md. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r4.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 4 (25 Sept ≈06:55 → 07:15) — a PICK pass, no engine change, two classes DECLINED.** (1) **The BARE lesson "
         "menu of the MX series** (`_s45_r4_menuwrap.py`; the MX scoped miner view `_s45_r4_mx.log`, row #59): the gold ships `#module-menu-content "
         "> h5 + ul` with no `row > col-md-8` on MXFU 44 / 44 lesson pages, MXEX 26 / 27, MXDB3 14 / 14, MXDI3 7 / 7 (91 pages / 12 modules — "
         "each ≥ 0.96; corpus lesson menus are row 0.92; MXEO / MXDB2 / MXDI2 row; MXFL a `div.item` form, 41 pages). **KB-correct as it stands:** "
         "KB 01B 'Key structural rules for lesson page simplified menus' — \"Content goes directly inside `<div class=\"row\"><div "
         "class=\"col-md-8 col-12\">`\" — and KB 10 §3's list of series lesson-menu deviations to PRESERVE does not name the MX bare form, so the "
         "gold's bare menus are NAMED overrides (§1b), never chased. Overturning it would take a KB 10 §3 series row (an Admin-Mode KB edit — "
         "Chris's lane, D13-1). (2) **The HIS untagged quote** (the r486 follow-up, `_s45_r4_hisquote.py`): a WT line wholly in quotation marks is "
         "`p.quoteText` in the HIS gold 26 / 38 = 0.68 on **18 pages** — under the 20-page body floor and not every page of the family "
         "(§1d exception 1 needs that), the rest plain p in tab panes / alerts / activities; the next-line `Source:` → `p.quoteAck` 5 sites. "
         "Recorded below floor.")
k = find("## Round log")
L.insert(k + 1, "- s45-r4 (no engine change, 25 Sept 06:55 → 07:15) · a PICK pass on the MX families (the loss ledger's mathematics group, 347 "
         "pages): the bare lesson menu (MXFU / MXEX / MXDB3 / MXDI3, 91 pages) DECLINED — KB 01B's lesson-menu rule is the row > col-md-8 form "
         "Claude ships (the gold a NAMED override; a KB 10 §3 series row would be needed); the HIS untagged quote 18 pages, below floor · plateau "
         "0 of 3 (neither).")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
print("ok", os.path.getsize(S))
