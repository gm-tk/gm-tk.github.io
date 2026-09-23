#!/usr/bin/env python3
"""Session 41 §5d condense #1 — LOOP_STATE.md 99.1 KB at the session start, at the 100 KB target before the
session's own notes. Moves, VERBATIM, to LOOP_STATE_ARCHIVE.md (append-only) and leaves a pointer line in place:
(1) the session-40 start note; (2) the s37-r1…r4 and s39-r1…r8 Round-log lines; (3) the stray truncated duplicate
'- **Session 40 Round 5 (24 Sept ≈03:50)' line under Declined classes (the full line follows it).
Nothing is deleted. Writes LF, UTF-8. Run under WSL from anywhere."""
import io, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
src = io.open(P, encoding="utf-8").read()
lines = src.split("\n")
moved = []
def take(pred, title, pointer):
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if not idx: print("NOT FOUND:", title); return
    block = [lines[i] for i in idx]
    moved.append((title, block))
    if pointer is None:
        for i in reversed(idx): del lines[i]
    else:
        lines[idx[0]] = pointer
        for i in reversed(idx[1:]): del lines[i]
    print(f"moved {len(block)} line(s), {sum(len(b) for b in block)} chars: {title}")
take(lambda l: l.startswith("**Session 40 started:**"),
     "Session start note 40 (verbatim, s41 §5d condense #1)",
     "**Session 40 started:** 24 Sept 00:27 (Opus 5.5) — clean start at af49b2d, miner re-run (197 CANDIDATE, byte-identical to r445's queue), Round 1 = D13-5; §5d condense #1 at ≈03:30; compaction #1 at 03:33; a clock correction (the ≈ times on s40-r5 → r7 ran ≈ 1 h 15 min ahead). Verbatim → LOOP_STATE_ARCHIVE.md 'Session start note 40 (verbatim, s41 §5d condense #1)'.")
rl = re.compile(r"^- s(37-r[0-9]+|39-r[0-9]+) \(")
take(lambda l: bool(rl.match(l)),
     "Round-log lines s37 / s39 (verbatim, s41 §5d condense #1)",
     "- s37-r1…r4 and s39-r1…r8 round-log lines (12 lines: the s37 four DECLINED PICK passes incl. the r438 built-and-reverted probe; engine r439–r446 shipped — writeFont, the dual-build golds, the language labels, the twelve menu repeaters, the XOTP flagged gaps, consecutive activity numbers (LAST FULL r444), the comparison table, the bubble placeholder) → LOOP_STATE_ARCHIVE.md 'Round-log lines s37 / s39 (verbatim, s41 §5d condense #1)'.")
take(lambda l: l.rstrip() == "- **Session 40 Round 5 (24 Sept ≈03:50)",
     "Declined classes — a stray truncated duplicate line (verbatim, s41 §5d condense #1)", None)
out = "\n".join(lines)
tmp = P + ".tmp"
io.open(tmp, "w", encoding="utf-8", newline="\n").write(out)
assert os.path.getsize(tmp) > 50000
arch = io.open(A, encoding="utf-8").read()
add = []
for title, block in moved:
    add.append("\n## " + title + "\n\n" + "\n".join(block) + "\n")
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(add))
os.replace(tmp, P)
print("LOOP_STATE.md", len(src.encode("utf-8")), "->", os.path.getsize(P))
