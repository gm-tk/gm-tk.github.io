#!/usr/bin/env python3
"""Session 45 — §5d condense #3: the session-45 Round 3 / 4 / 6 / 7 / 8 declined-class entries move VERBATIM to the archive. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s45-condense3.bak")
ss = io.open(S, encoding="utf-8", newline="").read(); L = ss.split("\n")
TAG = "(verbatim, s45 §5d condense #3)"
idx = [i for i, l in enumerate(L) if l.startswith("- **Session 45 Round ") and "PICK pass" in l]
assert len(idx) == 5, idx
moved = [L[i] for i in idx]
first = min(idx)
for i in sorted(idx, reverse=True): del L[i]
L.insert(first, "- **Session 45 declined classes, Rounds 3 / 4 / 6 / 7 / 8 (PICK passes, no engine change: R3 the r487 hover residue decomposed "
         "(no mechanism at the floor), KB c66 verified by construction, the placement census re-run; R4 the MX bare lesson menu DECLINED — KB 01B's "
         "row > col-md-8 rule, the HIS untagged quote 18 pages below floor; R6 the accordion bulleted bold lead → ride-along patch "
         "`_r489_accbullet_declined.patch` (+8 accordions / 4 modules), the carousel `Image #N:` banner list 9 modules, the gathering lever scoped; "
         "R7 Claude's empty lesson menu vs the gold's — 66 pages / 23 modules in-body across six writer forms, the WALT-lead placement has no "
         "consensus (body 70 / menu 46 / absent 73), HIS1003 / 1004's `[Alert box]` form a 19-page dialect; R8 the Bilingual lesson-title half "
         "class C, KB c27 verified LIVE)** → LOOP_STATE_ARCHIVE.md 'Declined classes — session 45 Rounds 3 / 4 / 6 / 7 / 8 " + TAG + "'; every "
         "verdict stands.")
ns = "\n".join(L)
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(ns); os.replace(S + ".tmp", S)
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Declined classes — session 45 Rounds 3 / 4 / 6 / 7 / 8 " + TAG + "\n\n" + "\n".join(moved) + "\n")
print("LOOP_STATE", len(ss.encode()), "->", len(ns.encode()))
