#!/usr/bin/env python3
"""_s53_condense1.py — session 53 §5d condense #1 (LOOP_STATE.md 96.7 KB → under the 100 KB target with headroom): moves VERBATIM to
LOOP_STATE_ARCHIVE.md (1) the plateau readings r526 and older, (2) the AppVersion history 260620.86 and older, (3) the (s51-r1)
follow-up entry, (4) the Session 52 start note — each replaced by a one-line pointer. WSL."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
os.makedirs(os.path.join(ROOT, "_Backups", "loop_state"), exist_ok=True)
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s53-condense1.bak"))
arch = []
def one(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
# (1) plateau: cut at "; r526 +0.0550pp"
i = one("- Plateau window (§4): **"); cut = L[i].find("; r526 +0.0550pp")
assert cut > 0
arch.append(("Position — plateau readings r526 → r505 pointer tail (verbatim, s53 §5d condense #1)", L[i][cut + 2:]))
L[i] = L[i][:cut] + "; r526 and every older reading → LOOP_STATE_ARCHIVE.md 'Position — plateau readings r526 → r505 pointer tail (verbatim, s53 §5d condense #1)'. Read every delta on the post-intake population (§1e)."
# (2) standing facts: cut at "; before it 260620.86 ("
i = one("- Standing facts: AppVersion **"); cut = L[i].find("; before it 260620.86 (")
assert cut > 0
arch.append(("Position — Standing facts AppVersion history 260620.86 and older (verbatim, s53 §5d condense #1)", L[i][cut + 2:]))
L[i] = L[i][:cut] + "; 260620.86 and older → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.86 and older (verbatim, s53 §5d condense #1)'; every toggle is listed in OPERATING_GUIDE.md §11; the engine + gate checksum manifests (`_MIGRATION/CHECKSUMS__engine.txt` / `CHECKSUMS__gates.txt`) are refreshed at every ship (a `.pre-rNNN.bak` copy kept)."
# (3) the s51-r1 follow-up
i = one("- **(s51-r1) the PICK pass, every lane below the floor or class C:**")
arch.append(("Follow-up candidates — s51-r1 (verbatim, s53 §5d condense #1)", L[i]))
L[i] = ("- The (s51-r1) PICK-pass follow-up (the r366 lead-free misfire ≈ 13 modules, slider ≈ 15 sites, activity-number sequences, the `[RHS …]` box inside an "
        "open activity ≈ 10 pages, over-capture 60 pages diffuse, the placement / recognition / per-family re-runs) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — "
        "s51-r1 (verbatim, s53 §5d condense #1)'. None is struck.")
# (4) the Session 52 start note
i = one("**Session 52 started:**")
arch.append(("Session start note 52 (verbatim, s53 §5d condense #1)", L[i]))
L[i] = ("**Session start note 52** -> LOOP_STATE_ARCHIVE.md 'Session start note 52 (verbatim, s53 §5d condense #1)'. One line: 26 Sept 15:01, started DIRTY with "
        "s51's toggled-OFF r528 (named in Position), finished it as Round 1; r528–r534 + the s52-r11 FULL backstop; §4 BUDGET stop at 19:41. Every figure in it is "
        "superseded by the Position section below.")
out = "\n".join(L)
tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(f"\n## {h}\n\n{b}\n" for h, b in arch))
print("LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S))
