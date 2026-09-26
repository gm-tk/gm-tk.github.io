#!/usr/bin/env python3
"""s52 §5d condense #2 — archive verbatim: the s51 Round-log lines (s51-r1…r13 + its compaction line) and the Declined-classes
entries of sessions 40–51; one pointer line each stays. Asserts every anchor. WSL."""
import io, os, re
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
S = os.path.join(R, "LOOP_STATE.md"); A = os.path.join(R, "LOOP_STATE_ARCHIVE.md")
t = io.open(S, encoding="utf-8", newline="").read(); n0 = len(t.encode("utf-8"))
L = t.split("\n"); arch = []

# 1. the s51 round-log lines
idx = [i for i, l in enumerate(L) if re.match(r"^- s51-r\d+ \(", l) or l.startswith("- compaction at 13:54 during s51-r12")]
assert len(idx) == 14 and idx == list(range(idx[0], idx[0] + 14)), idx
arch.append("## Round log s51-r1…r13 (verbatim, s52 §5d condense #2)\n\n" + "\n".join(L[i] for i in idx) + "\n")
L[idx[0]:idx[-1] + 1] = ["- s51-r1…r13 round-log lines (14 lines, session 51: engine r522 / r523 / r525 / r526 shipped, r524 / r527 / r527 v2 "
                         "declined, the s51-r12 FULL backstop, r528 built and toggled OFF at the stop; one compaction) → LOOP_STATE_ARCHIVE.md "
                         "'Round log s51-r1…r13 (verbatim, s52 §5d condense #2)'."]

# 2. the declined-class entries of sessions 40–51
heads = ("- **Session 51 Round 11", "- **Session 51 Round 10", "- **Session 51 Round 4", "- **Session 50 declined classes",
         "- **Session 46 Round 6 / Session 44", "- **Session 45 Round 11", "- **Session 45 declined classes", "- **Session 43 declined classes",
         "- **Session 42 declined classes, Rounds 9", "- **Session 42 declined classes, Rounds 5", "- **Session 41 declined classes",
         "- **Session 40 declined classes")
idx = []
for h in heads:
    k = [i for i, l in enumerate(L) if l.startswith(h)]
    assert len(k) == 1, (h, k)
    idx.append(k[0])
assert idx == list(range(idx[0], idx[0] + len(heads))), idx
arch.append("## Declined classes — sessions 40–51 entries (verbatim, s52 §5d condense #2)\n\n" + "\n".join(L[i] for i in idx) + "\n")
L[idx[0]:idx[-1] + 1] = ["- **Sessions 40–51 declined-class entries** (12 entries: s51 r524 the callout + heading co-tag, r527 / r527 v2 the journal "
                         "walk terminator; s50 r516 / r512; s46 / s45 / s44 / s43 / s42 / s41 / s40 PICK-pass declines — each with its class, "
                         "measure, verdict and patch) → LOOP_STATE_ARCHIVE.md 'Declined classes — sessions 40–51 entries (verbatim, s52 §5d "
                         "condense #2)'. Every verdict stands; grep the engine number there before re-opening any."]

out = "\n".join(L)
a0 = os.path.getsize(A)
with io.open(A, "a", encoding="utf-8", newline="") as f: f.write("\n" + "\n".join(arch))
assert os.path.getsize(A) > a0
tmp = S + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as f: f.write(out)
assert os.path.getsize(tmp) > 60000
os.replace(tmp, S)
print("LOOP_STATE", n0, "->", os.path.getsize(S), "; archive +", os.path.getsize(A) - a0)
