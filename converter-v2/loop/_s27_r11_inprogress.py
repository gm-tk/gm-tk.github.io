#!/usr/bin/env python3
"""Round 11 PICK -> LOOP_STATE.md (before the code): insert the Round-11 PICK section before '## Round log'. Idempotent, LF."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "Round 11 PICK (engine r406" in s: print("already"); sys.exit(0)
sec = rd(os.path.join(HERE, "_s27_r11_pick.md")).replace("\r\n", "\n").rstrip("\n") + "\n\n"
i = s.index("## Round log"); s = s[:i] + sec + s[i:]
wr(LS, s); print("ok", len(s.encode("utf-8")))
