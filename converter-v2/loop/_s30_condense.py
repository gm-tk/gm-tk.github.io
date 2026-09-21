#!/usr/bin/env python3
"""Session 30 stop — the §5d condense: LOOP_STATE.md crossed 100 KB; the session-29 'instruments re-measured' and 'Round 10 PICK pass'
sections move verbatim to the archive (one-line pointers stay); the Round 3 / 6 PICK-pass sections likewise; the STOPPED entry is
trimmed under 1,500 chars. Run under WSL."""
import os, io, re
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
def section(prefix):
    a = idx(prefix); b = a + 1
    while b < len(lines) and not lines[b].startswith("## "): b += 1
    return a, b
moved = []
for prefix, pointer, title in (
    ("## Session 29 — instruments re-measured on the post-intake corpus", "## Session 29 — instruments re-measured on the post-intake corpus (20 Sept ≈15:05 → 15:15, after r410) → LOOP_STATE_ARCHIVE.md 'Session 29 — instruments re-measured (archived at the session 30 stop)': the ceiling 90.9 % (2290 pairs, `_ceiling_r410`), the coverage dashboard (interactive coverage 50.5 %, no builder: infoTrigger / selfCheck / slider).", "Session 29 — instruments re-measured (archived at the session 30 stop)"),
    ("## Session 29 — Round 10 PICK pass", "## Session 29 — Round 10 PICK pass (no engine change; 20 Sept ≈22:05 → 22:43, ended by `/loop-stop`) — four censuses on the r418 corpus, nothing at the floor → LOOP_STATE_ARCHIVE.md 'Session 29 — Round 10 PICK pass (archived at the session 30 stop)'; the one-line summary is the s29-r10 Round-log line.", "Session 29 — Round 10 PICK pass (archived at the session 30 stop)"),
    ("## Session 30 — Round 6 PICK pass", "## Session 30 — Round 6 PICK pass (no engine change; 21 Sept ≈18:50 → 19:05) — the D10-3 widget lane re-read by CONTENT from the disk boxes, nothing at the floor → LOOP_STATE_ARCHIVE.md 'Session 30 — Round 6 PICK pass (archived at the session 30 stop)'; the one-line summary is the s30-r6 Round-log line below.", "Session 30 — Round 6 PICK pass (archived at the session 30 stop)"),
):
    a, b = section(prefix)
    moved.append((title, lines[a:b]))
    lines[a:b] = [pointer, ""]
# trim the STOPPED entry
s = idx("## >>> STOPPED 2026-09-21")
e = lines[s]
e = e.replace(" (the s29 record + this session: F23 decomposed, the title rows class C, the module-menu rows the r110 needs-Chris repeat, the footer rows the r360 sets)", "")
e = e.replace(" (D10-3's selfCheck kickoff shape 1; the NEW gate `_verify_bingo.cjs` 52 grids / defect 0; still-a-box 215 → 163; −0.0005pp named)", " (D10-3's selfCheck shape 1; NEW gate `_verify_bingo.cjs` 52 grids / defect 0; −0.0005pp named)")
e = e.replace(" (CHWHA / GEWHA / ANZHFUN05 / PWYWHA1 reach their registry rows; −0.0002pp named)", " (4 modules reach their registry rows; −0.0002pp named)")
lines[s] = e
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    for title, body in moved:
        f.write("\n## " + title + "\n\n" + "\n".join(body).rstrip("\n") + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; STOPPED", len(e), "chars; archive", os.path.getsize(ARCH))
