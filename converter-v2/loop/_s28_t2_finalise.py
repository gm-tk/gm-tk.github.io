#!/usr/bin/env python3
"""SESSION 28 / TASK 2 (round 409, build 260619.80 — the XOTP activity-table notice in the V1 parser) — finalise: changelog + CLAUDE.md §14 line.
Idempotent; LF preserved. WSL."""
import io, os
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; PF = os.path.join(ROOT, "pageforge-site", "converter-v2"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = rd(os.path.join(HERE, "_s28_t2_entry.md")).replace("\r\n", "\n")
if not ENTRY.endswith("\n\n"): ENTRY = ENTRY.rstrip("\n") + "\n\n"
if "round 409, build 260619.80" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog: r409 entry prepended")
assert '"260619.80"' in rd(os.path.join(PF, "app", "js", "Config.js"))
P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "`260619.80` (round 409" not in s:
    OLD = "- **Build:** `260619.79` (round 408"
    assert s.count(OLD) == 1
    NEW = ("- **Build:** `260619.80` (round 409 — **the XOTP activity-table template is recognised by the Module Development tab's V1 parser and said so plainly** "
           "(session 28 pre-loop Task 2: `pageforge-site/js/formatter.js` `OutputFormatter._isActivityTableDoc` — a table whose first rows hold the two-cell header "
           "`Section heading | Text/Activity`, present in exactly the 12 XOTP documents and nowhere else in the 762 — swaps the `⚠ [TITLE BAR] marker not found` warning "
           "for `ℹ Activity-table template detected … no [TITLE BAR] expected`; data-shaped switch `ACTIVITY_TABLE_NOTICE`, A/B `window.PF_ACTIVITY_TABLE_NOTICE_OFF`; the "
           "parser itself untouched — all 12 dumps differ from the corpus parsed txt in that one line only, PMT101 / PNR107 / TRR102 keep the warning, SCCH301 / WJFUN105 "
           "byte-identical); V1-site message only — no engine / data / output change, no regeneration, the r408 baselines stand). Previous: " + OLD)
    s = s.replace(OLD, NEW, 1); wr(P, s); print("CLAUDE.md §14")
print("done")
