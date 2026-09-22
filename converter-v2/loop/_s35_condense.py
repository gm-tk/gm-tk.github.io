#!/usr/bin/env python3
"""Session 35 §5d condense of LOOP_STATE.md (22 Sept 2026, session start).

Moves three over-cap lines VERBATIM to LOOP_STATE_ARCHIVE.md and leaves a short
summary in place:
  * the Position section's LAST SHIPPED bullet — keeps the r429 record, archives the
    "Before it r428 / r427 / r426 / LAST FULL" tail;
  * the session-31 and session-33 start notes (2.4 KB / 2.7 KB) — summarised to one
    line each (the session-34 note was already condensed at the s34 stop).
No decision is deleted. Idempotent: refuses to run twice (looks for its own marker).
"""
import io, os, re, sys, datetime

ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
STATE = os.path.join(ROOT, "LOOP_STATE.md")
ARCH = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
MARK = "s35 §5d condense"

def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f:
        return f.read()

def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f:
        f.write(s)

state = rd(STATE)
if MARK in state:
    print("already condensed — nothing to do"); sys.exit(0)

lines = state.split("\n")
moved = []

# 1. the LAST SHIPPED bullet
idx = next(i for i, l in enumerate(lines) if l.startswith("- LAST SHIPPED: **r429**"))
full = lines[idx]
cut = full.find(" Before it **r428**")
assert cut > 0, "r428 tail not found"
head, tail = full[:cut], full[cut:]
moved.append(("Position — LAST SHIPPED tail (r428 / r427 / r426 / LAST FULL), verbatim", tail.strip()))
lines[idx] = (head + " Before it **r428** (260620.01, +0.2062pp, the Inquiry-template fallback shell), "
              "**r427** (260620.00, gate-neutral chip deltas), **r426** (260619.99, the single-page Inquiry "
              "page-model rows, +0.0234pp); LAST FULL: **ROUND 0d — the 22 Sept 2026 intake of the 38** "
              "(session 33 Round 3, build 260619.98, ledger `intake-2026-09-22`, counter 0). The verbatim "
              "r426–r428 gate rows + the LAST FULL record: LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail "
              "(" + MARK + ")'.")

# 2. the session-31 and session-33 start notes
for tag, summary in (
    ("**Session 31 started:** 2026-09-21 19:15 NZST",
     "**Session 31 started:** 2026-09-21 19:15 NZST (Opus 5; 12 rounds / 10 h). Health check clean at 4472204; census 552 / 494 / 2555 / 2993 / 762 / 24; the miner's queue (r421 corpus) current, 182 CANDIDATE rows; KB HEAD 44c7c8e (no module rule). The s30 exhaustion verdict judged INCOMPLETE (the intake §7's PMT101 + XOTP items undispositioned) → Round 1 = PMT101 recognition (r423), Round 2 = XOTP recognition (r424), Round 3 = the XOTP adapter (r425). Verbatim: LOOP_STATE_ARCHIVE.md 'Session 31 / 33 start notes (verbatim, " + MARK + ")'."),
    ("**Session 33 started:** 2026-09-22 09:56 NZST",
     "**Session 33 started:** 2026-09-22 09:56 NZST (Opus 5; 12 rounds / 10 h; the first session on the review-rewritten kickoff). Health check clean at 36b4272; census 552 / 495 / 2559 / 2993 / 762 / 24 (no intake trigger); the miner's queue (r421 corpus) current, 184 CANDIDATE rows; KB HEAD 44c7c8e. Recorded the 38 gold-only dirs WITH a Writers Template (the r285 ghost-directory class) as a recognition-lane item → became the 22 Sept Round 0d (38 / 38 converted). Plan: r425 finished, r422 enabled, Round 0d, r426, r427 (crashed after its post-ship suite). Verbatim: LOOP_STATE_ARCHIVE.md 'Session 31 / 33 start notes (verbatim, " + MARK + ")'."),
):
    i = next(k for k, l in enumerate(lines) if l.startswith(tag))
    moved.append(("Session start note " + tag.split("**")[1].rstrip(":"), lines[i]))
    lines[i] = summary

new_state = "\n".join(lines)

# archive block (append-only)
now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
block = ["", "## Position — LAST SHIPPED tail (" + MARK + ", archived from LOOP_STATE.md " + now + " NZST — verbatim)", "",
         moved[0][1], "",
         "## Session 31 / 33 start notes (verbatim, " + MARK + ", archived " + now + " NZST)", ""]
for title, text in moved[1:]:
    block += [text, ""]
arch = rd(ARCH)
if not arch.endswith("\n"):
    arch += "\n"
wr(ARCH, arch + "\n".join(block))
wr(STATE, new_state)
print("LOOP_STATE.md %d -> %d bytes; archive +%d bytes" % (len(state.encode("utf-8")), len(new_state.encode("utf-8")), len("\n".join(block).encode("utf-8"))))
