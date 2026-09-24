#!/usr/bin/env python3
"""Session 44 §5d condense #1 (session start, 98.6 KB): MOVE verbatim to LOOP_STATE_ARCHIVE.md (1) the session-43 start note,
(2) the six session-43 shipped-round pointer headers (r472 / r473 / r474 / r475 / r476 / r477), (3) the struck Follow-up entries.
Pointer lines left in place; then write the session-44 start note and raise the r478 in-flight marker. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s44-condense1.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8")); arch = []

# (1) the s43 start note
k = [i for i, l in enumerate(L) if l.startswith("**Session 43 started:**")]; assert len(k) == 1
arch.append(("Session start note 43 (verbatim, s44 §5d condense #1)", [L[k[0]]]))
L[k[0]] = ("**Session 43 started:** 24 Sept 18:06 (Opus 5.5) — clean start at 871d40d, 12 rounds (≈ 5 h), two §5d condenses, one compaction "
           "(22:40 during r477); r472–r477 shipped, three PICK passes, r478 toggled OFF at the `/loop-stop`. Verbatim → LOOP_STATE_ARCHIVE.md "
           "'Session start note 43 (verbatim, s44 §5d condense #1)'.")
k43 = k[0]

# (2) the six s43 shipped-round pointer headers (+ the blank line after each)
idx = [i for i, l in enumerate(L) if l.startswith("## Session 43 — Round ") and "— SHIPPED" in l and "LOOP_STATE_ARCHIVE.md" in l]
assert len(idx) == 6, idx
arch.append(("Session 43 shipped-round pointer headers (verbatim, s44 §5d condense #1)", [L[i] for i in idx]))
first = idx[0]
L[first] = ("## Session 43 — every shipped round (engine r472 / r473 / r474 / r475 / r476 / r477) — each PICK + what-shipped record is in "
            "LOOP_STATE_ARCHIVE.md under 'Session 43 — Round N PICK (engine rXXX) + what shipped' (grep the engine number); the six pointer "
            "headers → 'Session 43 shipped-round pointer headers (verbatim, s44 §5d condense #1)'; the one-line summaries are the s43 Round-log lines below.")
drop = set()
for i in idx[1:]:
    drop.add(i)
    if i + 1 < len(L) and L[i + 1].strip() == "": drop.add(i + 1)

# (3) the struck Follow-up entries
struck_prefix = ("- ~~**(s40-r10)", "- ~~**(r449) The coverage dashboard", "- ~~**(r447) The following-URL", "- ~~**(r447) The r61",
                 "- ~~**(r447) Journal buttons", "- ~~**(r370) The bold-header")
sidx = [i for i, l in enumerate(L) if l.startswith(struck_prefix)]
assert len(sidx) == 6, sidx
arch.append(("Follow-up candidates — struck entries s40-r10 / r449 / r447 ×3 / r370 (verbatim, s44 §5d condense #1)", [L[i] for i in sidx]))
L[sidx[0]] = ("- Struck Follow-up entries (s40-r10 the `[Image]` description DECLINED; r449 the dashboard quiz rows SHIPPED s40-r10; r447 the "
              "following-URL absorb and the r61 alert-title regex MEASURED below floor s42-r7 (ride-along patches); r447 journal buttons "
              "inside a bundle DISPOSITIONED s40-r9 → r452; r370 the bold-header media table ALREADY SHIPPED r372) → LOOP_STATE_ARCHIVE.md "
              "'Follow-up candidates — struck entries s40-r10 / r449 / r447 ×3 / r370 (verbatim, s44 §5d condense #1)'.")
for i in sidx[1:]: drop.add(i)

L = [l for i, l in enumerate(L) if i not in drop]

# the session-44 start note, after the s43 one
k = [i for i, l in enumerate(L) if l.startswith("**Session 43 started:**")][0]
L.insert(k + 1, (
    "**Session 44 started:** 2026-09-24 23:33 NZST (Claude Code, Opus 5.5). Budget: **12 rounds or 10 hours** (the `/loop-start` default → ends ≈ 09:33 "
    "on 25 Sept). **Health check:** `git status` DIRTY = r478's two files (ContentConverter.js / Emit_Templates.json, `activity_lead_links` "
    "enabled: false) — the Position line names them (LAST BUILT, TOGGLED OFF), so NOT a crash; `verify_after_transfer.sh` FAIL on those two "
    "engine checksums ONLY (census 552 / 545 / 2679 / 2993 / 762 EXACT — no intake trigger (a)); §0 (b) the 7 gold-only dirs = the no-source "
    "list, (c) 0 docx newer than its `_run.json`, (d) nothing in either staging area newer than the 19 Sept audit — no Round 0d; no stale "
    "locks; `**Amended:**` = 1; KB HEAD `910a9cb` = the recorded HEAD; no `outputs/` write since the s43 stop (23:04). `DIFF_QUEUE.md` 22:43 "
    "= the r477 corpus (the r478 ON / OFF regen restored identical bytes). **§5d condense #1 at 23:40** (98.6 KB → see `wc`): the s43 start "
    "note, the six s43 shipped-round pointer headers and the six struck Follow-up entries moved verbatim (`outputs/_s44_condense1.py`). "
    "Order: Round 1 = FINISH r478, then the miner + the placement census re-run, then the PICK."))

s2 = "\n".join(L)
io.open(S, "w", encoding="utf-8", newline="\n").write(s2)
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch:
        f.write("\n## " + title + "\n\n" + "\n".join(lines) + "\n")
print("LOOP_STATE.md", n0, "->", len(s2.encode("utf-8")), "bytes; archived", len(arch), "sections")
