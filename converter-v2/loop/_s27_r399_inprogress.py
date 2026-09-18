#!/usr/bin/env python3
"""Mark Round 2 (r399) IN PROGRESS in LOOP_STATE.md's Position block (idempotent; LF preserved)."""
import io, os
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
p = os.path.join(ROOT, "LOOP_STATE.md")
s = io.open(p, encoding="utf-8", newline="").read()
anchor = "- LAST SHIPPED: **r398**"
i = s.index(anchor); j = s.index("\n", i) + 1
line = ("- IN PROGRESS (session 27 Round 2, ≈10:40 NZST): **r399 — the wānanga / talanoa box is the KB cultural alert** (PICK above; data "
        "`callouts.by_tag.wananga.kb_form` + `.table_cell_content` + a `tag_promote` carousel→wananga rule, one env `WANANGA_OFF`). "
        "Steps: data + engine → probe OFF (== disk) / ON → score with the gate's match() → scoped regen of the affected set + the §0b family → "
        "gates → finalise → commit. If this line is still here at the next session start, the engine / data edits are uncommitted r399 work: "
        "check them against the PICK, finish or toggle OFF.\n")
if "IN PROGRESS (session 27 Round 2" not in s:
    s = s[:j] + line + s[j:]
    io.open(p, "w", encoding="utf-8", newline="").write(s); print("added", len(s.encode("utf-8")))
else:
    print("present")
