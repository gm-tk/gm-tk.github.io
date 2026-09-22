#!/usr/bin/env python3
"""Session 36 §5d condense #2 (LOOP_STATE.md 99.9 KB — no headroom for the next PICK): the s27 / s29 / s30 STOPPED entries + the
s28 HANDOVER block (lines 29–36) move verbatim to LOOP_STATE_ARCHIVE.md behind ONE pointer line; the three stale Position narrative
bullets (the RESOLVED r425 stop, the s30 and s25 exhaustion stops) move verbatim to the archive behind one pointer bullet.
No decision deleted. Run under WSL."""
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)
st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
lines = st.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(lines) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
a = find("## >>> STOPPED 2026-09-21 ≈19:10 NZST (session 30) on §4 EXHAUSTION")
b = find("## STOPPED entries, sessions 19 / 21 / 22 / 23 / 24 / 25 → LOOP_STATE_ARCHIVE.md")
block = lines[a:b]   # s30 STOPPED, the s28 HANDOVER, s29 STOPPED, s27 STOPPED (+ their blank lines)
assert any(l.startswith("## HANDOVER of 2026-09-20") for l in block) and any(l.startswith("## >>> STOPPED 2026-09-19 ≈16:40 NZST (session 27)") for l in block)
pointer = ("## STOPPED entries, sessions 27 / 29 / 30 + the session-28 HANDOVER (resolved) → LOOP_STATE_ARCHIVE.md 'STOPPED entries sessions 27–30 (verbatim, s36 §5d "
           "condense #2)' — s27 BUDGET (12 rounds, 19 Sept), s29 `/loop-stop` (9 shipped r410–r418), s30 EXHAUSTION (the first post-intake, miner quoted), the "
           "r410 handover RESOLVED by s29 Round 1. Every verdict stands; grep the session number there.")
lines[a:b] = [pointer, ""]
# the Position's stale narrative bullets
p1 = find("- (RESOLVED 22 Sept by session 33 Round 1 — r425 finished.) **THE LOOP STOPPED 2026-09-21 ≈22:00 (session 31)")
p2 = find("- **THE LOOP STOPPED 2026-09-21 ≈19:10 (session 30) on §4 EXHAUSTION**")
p3 = find("- **THE LOOP STOPPED 2026-09-18 ≈20:40 (session 25) on §4 EXHAUSTION**")
assert p2 == p1 + 1 and p3 == p2 + 1
pos = lines[p1:p3 + 1]
lines[p1:p3 + 1] = [("- Earlier stop narratives (the s31 `/loop-stop` with r425 inert — RESOLVED by s33 Round 1; the s30 and s25 exhaustion stops, both superseded by "
                     "later shipped rounds) → LOOP_STATE_ARCHIVE.md 'Position — stop narratives s25 / s30 / s31 (verbatim, s36 §5d condense #2)'.")]
ar = (ar.rstrip("\n") + "\n\n## STOPPED entries sessions 27–30 (verbatim, s36 §5d condense #2 — archived from LOOP_STATE.md 2026-09-22 ≈23:12 NZST)\n\n"
      + "\n".join(block).strip("\n") + "\n\n## Position — stop narratives s25 / s30 / s31 (verbatim, s36 §5d condense #2)\n\n" + "\n".join(pos) + "\n")
wr(R + "LOOP_STATE_ARCHIVE.md", ar); wr(R + "LOOP_STATE.md", "\n".join(lines))
print("condense #2 OK")
