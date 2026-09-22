#!/usr/bin/env python3
"""Session 35 §5d condense #2 (22 Sept 2026, before r432): the two longest Declined-classes entries (the session-24 and the
session-27 Round 2 PICK-pass records, 3.2 KB + 2.2 KB) move VERBATIM to LOOP_STATE_ARCHIVE.md; a one-line pointer stays.
No decision deleted. Idempotent."""
import io, os, sys, datetime
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
STATE = os.path.join(ROOT, "LOOP_STATE.md"); ARCH = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
MARK = "s35 §5d condense #2"
def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
state = rd(STATE)
if MARK in state: print("already condensed"); sys.exit(0)
lines = state.split("\n"); moved = []
targets = [
    ("- **Session 24 (18 Sept 2026, ≈13:20 → 19:30) — the classes measured and DECLINED",
     "- **Session 24 (18 Sept 2026) — three classes measured and DECLINED** (the colon-ended short lead as a heading 0.23; the activity box's extra sub-heading — no derivable slice; the body-image gap = the D10-3 build backlog): verbatim in LOOP_STATE_ARCHIVE.md 'Declined classes — the s24 and s27-r2 entries (" + MARK + ")'."),
    ("- **Session 27 Round 2 PICK pass (19 Sept ≈10:00, the classes measured before the wānanga box was taken",
     "- **Session 27 Round 2 PICK pass (19 Sept) — the gold's `<br>` (the r357 decline stands; the per-prefix soft-break form later CLOSED by measurement, s27-r4), `div.col-12.col-md-12` DIFFUSE, and the rest of that pass**: verbatim in LOOP_STATE_ARCHIVE.md 'Declined classes — the s24 and s27-r2 entries (" + MARK + ")'."),
]
for tag, summary in targets:
    i = next(k for k, l in enumerate(lines) if l.startswith(tag))
    moved.append(lines[i]); lines[i] = summary
new_state = "\n".join(lines)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
block = ["", "## Declined classes — the s24 and s27-r2 entries (" + MARK + ", archived from LOOP_STATE.md " + now + " NZST — verbatim)", ""] + [m + "\n" for m in moved]
arch = rd(ARCH)
if not arch.endswith("\n"): arch += "\n"
wr(ARCH, arch + "\n".join(block)); wr(STATE, new_state)
print("LOOP_STATE.md %d -> %d bytes" % (len(state.encode("utf-8")), len(new_state.encode("utf-8"))))
