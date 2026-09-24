#!/usr/bin/env python3
"""Session 45 Round 3 — record the PICK pass (no engine change) in LOOP_STATE.md + KB_AMALGAMATION_STATUS.md row 66. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-s45-r3.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
k = find("## Declined classes")
L.insert(k + 1, "- **Session 45 Round 3 (25 Sept ≈06:35 → 06:55) — a PICK pass, no engine change.** (1) **The hover markers with no named term** "
         "(`word [hover definition: DEF] …`, the r487 residue — `_s45_r3_colon.py`, `_s45_r3_hoverparse.cjs`): of 117 the gold builds and Claude "
         "does not, 40 are DROPPED and 77 LEAK — 31 inside un-built widget hand-off boxes (the marker is a widget MEMBER, consumed before the "
         "scanner's weave runs: SCES201's flip cards, AGH1007 / CEDR203 / CEDT501 tables), 20 as red Writers Notes, 18 visible in student prose "
         "over 13 modules (AGH1009 4, TEFUN05 3 — split red runs / an unclosed head with the def in the next span), 8 unplaced; the engine's "
         "TagNormaliser resolves the heads six ways (`[hover:` / `[hover-over:` / `[hover information:` / `[hover –` = class instruction with no "
         "tag; `[hover definition` / `[roll-over definition` = info trigger; `[rollover text` / `[hover text` = body) — no mechanism at the "
         "floor; recorded. (2) **KB c66** (acks titles verbatim, incl. \". stock photo\"): honoured BY CONSTRUCTION — with no `*istock-acks*.txt` "
         "API file (none in the corpus) the AcksBuilder writes an `ACK-TODO[istock-name]` / `[OFFICIAL ISTOCK TITLE REQUIRED]` line and never "
         "invents a title (c53); the gold's 3,060 \"stock photo\" titles are API data the corpus lacks — not derivable. (3) **The placement census "
         "re-run** (`_placement_census_s45.{md,json}`, 163,771 gold blocks): its largest heading rows are decided or class C — `menu:flat → "
         "ABSENT-inWT` \"We are learning to:\" (293 pages) is D10-9's KB colon form (`We are learning:` + \"to …\" bullets, r349); \"You will show "
         "your understanding by:\" / \"Want to know where to start?\" are developer text not in the WT; `header:other → ABSENT-notWT` lesson "
         "titles not in the WT.")
k = find("## Round log")
L.insert(k + 1, "- s45-r3 (no engine change, 25 Sept 06:35 → 06:55) · a PICK pass: the r487 hover residue decomposed (117 gold-only; 18 "
         "visible in prose over 13 modules, the rest inside hand-off boxes / notes / dropped — no mechanism at the floor); KB c66 verified by "
         "construction (no iStock API file → ACK-TODO, never invented); the placement census re-run (top rows decided: D10-9, class C) · "
         "plateau 0 of 3 (neither).")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(L)); os.replace(S + ".tmp", S)
K = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); shutil.copyfile(K, K + ".pre-s45-r3.bak")
KL = io.open(K, encoding="utf-8").read().split("\n")
i = [j for j, l in enumerate(KL) if l.startswith("| 66 | Acks titles verbatim")]; assert len(i) == 1
KL[i[0]] = KL[i[0]].replace("| **UNVERIFIED** (compare Claude acks entry titles with the API map) |",
    "| **LIVE BY CONSTRUCTION — VERIFIED 2026-09-25 (session 45 Round 3):** the official title comes only from the module's iStock API file "
    "(`*istock-acks*.txt`, c53); with none supplied (no corpus module has one) AcksBuilder writes `ACK-TODO[istock-name]` + `[OFFICIAL ISTOCK "
    "TITLE REQUIRED]` and never invents or re-cases a title. The gold's 3,060 \". stock photo\" titles are API data the corpus lacks. |", 1)
assert "LIVE BY CONSTRUCTION" in KL[i[0]]
io.open(K + ".tmp", "w", encoding="utf-8", newline="").write("\n".join(KL)); os.replace(K + ".tmp", K)
print("ok", os.path.getsize(S))
