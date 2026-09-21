#!/usr/bin/env python3
"""Session 31 §5d condense: the s27-r1..r12, s28-t1 and s29-r1..r10 Round-log lines move VERBATIM to LOOP_STATE_ARCHIVE.md
(append-only) and one pointer line stays in LOOP_STATE.md. Run under WSL."""
import io, datetime
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
start = next(i for i, l in enumerate(lines) if l.startswith("## Round log"))
end = next(i for i, l in enumerate(lines) if i > start and l.startswith("## "))
moved, kept = [], []
for i in range(start, end):
    l = lines[i]
    if l.startswith("- s27-r") or l.startswith("- s28-t1") or l.startswith("- s29-r"):
        moved.append(l)
    else:
        kept.append(l)
assert len(moved) == 23, len(moved)
stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
pointer = ("- s27–s29 round-log lines (23 lines, sessions 27–29: engine r398–r407, the s28 r408 registry rebuild, r410–r418 + the s27 / s29 PICK passes) "
           "→ LOOP_STATE_ARCHIVE.md 'Round-log lines s27–s29 (archived from LOOP_STATE.md " + stamp + " NZST, session 31 §5d condense)' — grep the engine number there; every verdict stands.")
# insert the pointer right after the existing s21–s26 pointer line
out = []
for l in kept:
    out.append(l)
    if l.startswith("- s21–s26 round-log lines"):
        out.append(pointer)
assert any(l.startswith("- s27–s29 round-log lines") for l in out)
lines[start:end] = out
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
arch = io.open(ARCH, encoding="utf-8").read()
if not arch.endswith("\n"): arch += "\n"
arch += "\n## Round-log lines s27–s29 (archived from LOOP_STATE.md " + stamp + " NZST, session 31 §5d condense)\n" + "\n".join(moved) + "\n"
io.open(ARCH, "w", encoding="utf-8", newline="\n").write(arch)
print("moved", len(moved), "lines; LOOP_STATE.md now", len("\n".join(lines).encode("utf-8")), "bytes")
