#!/usr/bin/env python3
"""Session 27 Round 3 (PICK pass, no engine change) — LOOP_STATE.md: the pass section (before '## Round log'), the Round-log line,
the plateau window 1 of 3. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r3 (no engine change)" in s:
    print("already applied"); sys.exit(0)
sec = rd(os.path.join(HERE, "_s27_r3_pass.md")).replace("\r\n", "\n").rstrip("\n") + "\n\n"
i = s.index("## Round log")
s = s[:i] + sec + s[i:]
line = ("- s27-r3 (no engine change) · PICK PASS on the r399 corpus — eight classes measured (`_s27_r3_alerttag.py` / `_sidepad.py` / `_imgside.py` / `_headprefix.py` / "
        "`_grid2.py` / `_h4.py` / `_emptyalert.py` / `_alerthead.py`), none at the floor: `[important]` → solid is KB-correct (the ConnectED gold's plain form a KB-over-gold delta); "
        "the right-column image editorial; the heading digits per prefix all under 20 pages (HPFUN H2 0.77 / 14 pages the best); the soft-break `<br>` registry (ENGJ 0.97 / HIS 0.65) "
        "recorded as the engine-risky follow-up; the padded side column +0.01pp not taken · 12:40 · plateau 1 of 3\n")
anchor = "- s27-r2 (engine r399)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = "- Plateau window (§4): **1 of 3** — r399 +0.103pp RESET it; s27-r3 a PICK pass with no ship (0.000pp) counts 1.\n"
s = s.replace(old, new, 1)
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
