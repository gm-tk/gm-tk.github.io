#!/usr/bin/env python3
"""Session 27 Round 4 (PICK pass, no engine change) — LOOP_STATE.md: the pass section (before '## Round log'), the Round-log line,
the plateau window 2 of 3, the s27-r3 line's wrong clock (12:40 → 11:30, the commit time). LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r4 (no engine change)" in s:
    print("already applied"); sys.exit(0)
sec = rd(os.path.join(HERE, "_s27_r4_pass.md")).replace("\r\n", "\n").rstrip("\n") + "\n\n"
i = s.index("## Round log")
s = s[:i] + sec + s[i:]
line = ("- s27-r4 (no engine change) · PICK PASS on the r399 corpus — the D10-3 build lane measured to its floor (the census rebuilt fresh: dragAndDrop 795 declines over 663 signatures; "
        "the title-led form `_s27_r4_ddhead.cjs` 25 bundles / 24 pages, gold DD 0.40, ≈ 10 buildable; no type has an un-built dialect ≥ 20 sites), the `<br>` follow-up CLOSED "
        "(`_s27_r4_brseries.py` — the writer's soft break as `<br>` is ≈ 8 pages; `_s27_r4_goldbr.py` / `_s27_r4_brjoin.py` — the gold's br are developer joins with no feature at the floor outside 2 poem modules), "
        "the Empty [Hn] flags (2 derivable sites), the `col-12 col-md-12` widget wrapper re-declined (`_s27_r4_col12md12.py`), the missing `<p>` decomposed (`_s27_r4_pkinds.py`) · 12:35 · plateau 2 of 3\n")
anchor = "- s27-r3 (no engine change)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
# the s27-r3 line's clock was wrong (the commit is 3ec59bc at 11:30)
r3 = s[k:k2]
if "· 12:40 · plateau 1 of 3" in r3:
    s = s[:k] + r3.replace("· 12:40 · plateau 1 of 3", "· 11:30 · plateau 1 of 3") + s[k2:]
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = "- Plateau window (§4): **2 of 3** — r399 +0.103pp RESET it; s27-r3 and s27-r4 PICK passes with no ship (0.000pp) count 1 and 2; one more sub-0.02pp round with no other gate moving = the §4 plateau stop.\n"
s = s.replace(old, new, 1)
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
