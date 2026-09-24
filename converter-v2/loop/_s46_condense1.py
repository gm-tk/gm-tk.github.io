#!/usr/bin/env python3
"""Session 46 §5d condense #1 — move verbatim to LOOP_STATE_ARCHIVE.md: the s45-r1…r12 Round-log lines, the s45 Round-11 declined entry,
and the oldest Follow-up entries (r437 / r436 / r435 / r434 / r433 / r429 / r428 ×2 / r370); leave one pointer line for each group. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
rd = lambda p: io.open(p, encoding="utf-8", newline="").read()
ss = rd(S); L = ss.split("\n"); shutil.copyfile(S, S + ".pre-s46-condense1.bak")
out = []
def take(pred, label, pointer):
    idx = [i for i, l in enumerate(L) if pred(l)]
    assert idx, label
    moved = [L[i] for i in idx]
    first = idx[0]
    for i in reversed(idx): del L[i]
    L.insert(first, pointer)
    out.append(f"\n## {label}\n\n" + "\n".join(moved) + "\n")
    return len(moved)
n1 = take(lambda l: l.startswith("- s45-r") and " · " in l, "Round log s45-r1…r12 (verbatim, s46 §5d condense #1)",
          "- s45-r1…r12 round-log lines (12 lines, session 45: engine r486 / r487 / r488 / r490 shipped, the r490 FULL backstop (Round 10), the R3 / R4 / R6 / R7 / R8 / R11 / R12 PICK passes) → LOOP_STATE_ARCHIVE.md 'Round log s45-r1…r12 (verbatim, s46 §5d condense #1)'.")
n2 = take(lambda l: l.startswith("- **Session 45 Round 11 (25 Sept 08:35"), "Declined classes — session 45 Round 11 (verbatim, s46 §5d condense #1)",
          "- **Session 45 Round 11 (a PICK pass, no engine change: the absent lesson LIs class C, the WT LI tables, the MTK drop-down three-tab header recorded)** → LOOP_STATE_ARCHIVE.md 'Declined classes — session 45 Round 11 (verbatim, s46 §5d condense #1)'; every verdict stands.")
old = ("- **(r437) CEDR302", "- **(r436) The REPEATED", "- **(r435) The body's ROW", "- **(r434) The lesson-menu", "- **(r433) The MXFUN",
       "- **(r429, DECLINED", "- **(r428) The `[Side Tabs]`", "- **(r428) The r100 mode", "- **(r370) MXEX101")
n3 = take(lambda l: l.startswith(old), "Follow-up candidates — r437 / r436 / r435 / r434 / r433 / r429 / r428 ×2 / r370 (verbatim, s46 §5d condense #1)",
          "- The r428–r437 and r370 follow-up entries (CEDR302's menu overrun; the r436 repeated overview menu — DECLINED as a KB override, never re-measure without a KB decision; the r435 body row composition; the r434 lesson-menu `[Body]` lead-in; the r433 MXFUN heading levels; the r429 panel first-heading level (DECLINED); the r428 `[Side Tabs]` inquiry shell and `[New side tab]` openers; MXEX101's repeated media sections) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — r437 / r436 / r435 / r434 / r433 / r429 / r428 ×2 / r370 (verbatim, s46 §5d condense #1)'.")
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(out))
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print(f"moved {n1} + {n2} + {n3} lines; LOOP_STATE {len(ss.encode('utf-8'))} -> {os.path.getsize(S)}")
