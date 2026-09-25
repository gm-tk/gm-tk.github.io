#!/usr/bin/env python3
"""Session 50 §5d condense #3 (WSL): the (s42-r3) placement-census and (s43) widget text-loss follow-up entries move to the archive
verbatim; one pointer line stays hot."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
s = io.open(S, encoding="utf-8", newline="").read()
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s50-condense3.bak"))
L = s.split("\n")
idx = [i for i, l in enumerate(L) if l.startswith("- **(s42-r3) THE PLACEMENT CENSUS — the standing §1g probe") or l.startswith("- **(s43) THE WIDGET TEXT-LOSS CENSUS")]
assert len(idx) == 2, idx
moved = [L[i] for i in idx]
first = min(idx)
for i in sorted(idx, reverse=True):
    del L[i]
L.insert(first, "- The (s42-r3) placement-census entry (the standing §1g probe `outputs/_placement_census.py`, its first run and finds P1–P8 — "
         "P1 SHIPPED r467, P2 DECIDED D15-22 / SHIPPED r503, P3 KB-correct, P4–P7 DECLINED class C / floor, P8 the D13-4 lane) and the (s43) "
         "widget text-loss census entry (the standing hand-off-box instrument `outputs/_s43_widgetloss2.cjs` + its report; r472 / r473 "
         "shipped from it; the residue below the floor) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — s42-r3 placement census / s43 "
         "widget text-loss (verbatim, s50 §5d condense #3)'. Both instruments stay standing; re-run them in a PICK pass.")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Follow-up candidates — s42-r3 placement census / s43 widget text-loss (verbatim, s50 §5d condense #3)\n\n" + "\n".join(moved) + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); os.replace(tmp, S)
print("LOOP_STATE", len(s.encode()), "->", os.path.getsize(S))
