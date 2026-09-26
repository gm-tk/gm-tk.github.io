#!/usr/bin/env python3
"""_s51_condense2.py — session 51 §5d condense #2: move the three session-49 Follow-up entries (s49-r4 black side-tab list,
s49-r9 placement census on the r507 corpus, s49-r10/r11 recorded) verbatim to LOOP_STATE_ARCHIVE.md, leaving one pointer. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
os.makedirs(os.path.join(ROOT, "_Backups", "loop_state"), exist_ok=True)
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s51-condense2.bak"))
L = io.open(S, encoding="utf-8", newline="").read().split("\n")
heads = ["- **(s49-r4) the writer's BLACK side-tab list elsewhere", "- **(s49-r9) the placement census on the r507 corpus**",
         "- **(s49-r10 / r11) recorded, each below the floor:**"]
idx = []
for h in heads:
    hits = [i for i, l in enumerate(L) if l.startswith(h)]
    assert len(hits) == 1, (h, hits)
    idx.append(hits[0])
moved = [L[i] for i in idx]
title = "Follow-up candidates — s49-r4 / s49-r9 / s49-r10-r11 (verbatim, s51 §5d condense #2)"
io.open(A, "a", encoding="utf-8", newline="\n").write(f"\n## {title}\n\n" + "\n".join(moved) + "\n")
ptr = (f"- The s49-r4 (the writer's black side-tab list: CEDT207 / MXEX201, 2 modules), s49-r9 (the placement census on the r507 corpus — "
       f"its CANDIDATE rows the dispositioned lanes) and s49-r10 / r11 (BLL265's body Knowledge / Practices, the one-word `[radioquiz]`, "
       f"the MXEX201 / 202 menu-less lessons, the mcq TABLE bundles) follow-up entries → LOOP_STATE_ARCHIVE.md '{title}'. None is struck.")
L[idx[0]] = ptr
for i in sorted(idx[1:], reverse=True): del L[i]
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print("LOOP_STATE", os.path.getsize(S))
