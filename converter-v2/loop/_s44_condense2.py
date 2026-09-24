#!/usr/bin/env python3
"""Session 44 §5d condense #2 (after Round 3, 95.8 KB): MOVE verbatim to LOOP_STATE_ARCHIVE.md (1) the per-round POINTER headers of
sessions 31 / 33 / 34 / 35 / 36 / 37-r2 / 41-r12 / 40–41 / 43 (lines 221–258, every one already a pointer into the archive; the s37-r1
section with its two do-not-re-derive findings STAYS), (2) the s43-r1…r10 round-log lines. Pointer lines left. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s44-condense2.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8")); arch = []
starts = ("## Session 43 — Round 10 PICK (engine r478)", "## Session 43 — every shipped round", "## Session 31 — Round 1 (engine r423)",
          "## Session 41 — Round 12 PICK (engine r464", "## Sessions 40 / 41 — every shipped round", "## Session 31 — Round 2 (engine r424",
          "## Session 37 — Round 2 (engine r438", "## Session 36 — Round 5 (no engine change", "## Session 36 — Round 4 (engine r436",
          "## Session 36 — Round 3 (engine r435", "## Session 36 — Round 2 (engine r434", "## Session 36 — Round 1 (engine r433",
          "## Session 35 — Round 3 (engine r432", "## Session 35 — Round 2 (engine r431", "## Session 35 — Round 1 (engine r430",
          "## Session 34 — Round 3 PICK pass", "## Session 34 — Round 2 (engine r428", "## Session 33 — Round 5 (engine r427",
          "## Session 31 — Round 3 (engine r425")
moved = []; drop = set()
for pre in starts:
    idx = [i for i, l in enumerate(L) if l.startswith(pre)]
    assert len(idx) == 1, (pre, idx)
    i = idx[0]; j = i + 1
    while j < len(L) and not L[j].startswith("## "): j += 1
    moved.append("\n".join(L[i:j]).rstrip()); drop.update(range(i, j))
arch.append(("Per-round pointer headers, sessions 31 / 33 / 34 / 35 / 36 / 37-r2 / 40 / 41 / 43 (verbatim, s44 §5d condense #2)", moved))
first = min(drop)
rl = [i for i, l in enumerate(L) if l.startswith("- s43-r")]
assert len(rl) == 10, rl
arch.append(("Round log s43-r1…r10 (verbatim, s44 §5d condense #2)", [L[i] for i in rl]))
keep = []
for i, l in enumerate(L):
    if i == first:
        keep.append("## Per-round pointer headers, sessions 31 / 33 / 34 / 35 / 36 / 37-r2 / 40 / 41 / 43 (engine r423–r438, r447–r464, "
                    "r472–r478) — each pointed at its PICK + what-shipped record in LOOP_STATE_ARCHIVE.md; the 19 headers themselves → "
                    "LOOP_STATE_ARCHIVE.md 'Per-round pointer headers, sessions 31 / 33 / 34 / 35 / 36 / 37-r2 / 40 / 41 / 43 (verbatim, s44 §5d "
                    "condense #2)'. Grep the engine number there. (The s37-r1 section below stays: its two findings must not be re-derived.)")
        keep.append("")
    if i in drop: continue
    if i == rl[0]:
        keep.append("- s43-r1…r10 round-log lines (10 lines, session 43: engine r472 / r473 / r474 / r475 / r476 / r477 shipped, r478 built and "
                    "toggled OFF at the stop — finished as s44-r1 — and the R3 / R4 / R6 PICK passes) → LOOP_STATE_ARCHIVE.md 'Round log "
                    "s43-r1…r10 (verbatim, s44 §5d condense #2)'.")
        continue
    if i in rl: continue
    keep.append(l)
s2 = "\n".join(keep)
io.open(S, "w", encoding="utf-8", newline="\n").write(s2)
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, blocks in arch:
        f.write("\n## " + title + "\n\n" + "\n\n".join(blocks) + "\n")
print("LOOP_STATE.md", n0, "->", len(s2.encode("utf-8")))
