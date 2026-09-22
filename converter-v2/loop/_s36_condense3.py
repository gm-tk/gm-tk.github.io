#!/usr/bin/env python3
"""Session 36 §5d condense #3 (LOOP_STATE.md 100.4 KB after r435's finalise): the per-round POINTER lines for sessions 25–30
(each already just a pointer into LOOP_STATE_ARCHIVE.md) collapse into two pointer lines, one per session block. Nothing is
archived here — the records they point at are already in the archive; only the pointers are merged. Run under WSL."""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md")
lines = st.split("\n")
def block(prefixes):
    idx = [i for i, l in enumerate(lines) if any(l.startswith(p) for p in prefixes)]
    assert idx, prefixes
    return min(idx), max(idx)
# sessions 25–27 pointer lines
a, b = block(["## Session 25 — Round 1 DECLINED", "## Session 25 — Round 2 PICK pass", "## Session 26 — Round 12 PICK pass", "## Session 27 — Round 3 + Round 4 PICK passes"])
# sessions 29–30 pointer lines (r411–r422 + the PICK passes + the instruments note)
c, d = block(["## Session 29 — instruments re-measured", "## Session 29 — Round", "## Session 30 — Round"])
assert a < b < c < d
p1 = ("## Session 25 / 26 / 27 per-round records (the s25 minor-heading DECLINE and loss ledger, the s26 Round-12 PICK pass, the s27 Round 3 / 4 PICK passes) "
      "→ LOOP_STATE_ARCHIVE.md — grep the session number and round there; every verdict stands. (Pointer lines merged at the 2026-09-23 session 36 §5d condense #3.)")
p2 = ("## Session 29 / 30 per-round records (the s29 post-intake instrument re-measurements and engine r411–r418 with its Round-10 PICK pass; the s30 engine "
      "r419–r422 with its Round-3 and Round-6 PICK passes) → LOOP_STATE_ARCHIVE.md — grep the engine number there; every verdict stands. (Pointer lines "
      "merged at the 2026-09-23 session 36 §5d condense #3.)")
out = lines[:a] + [p1, ""] + lines[b + 1:c] + [p2, ""] + lines[d + 1:]
wr(R + "LOOP_STATE.md", "\n".join(out))
print("condense #3 OK — %d lines -> %d" % (len(lines), len(out)))
