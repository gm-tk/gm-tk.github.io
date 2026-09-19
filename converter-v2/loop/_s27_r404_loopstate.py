#!/usr/bin/env python3
"""Session 27 Round 9 DECLINED-INERT (engine r404, no regeneration) — LOOP_STATE.md: the Position block's build line, the plateau window 1 of 3,
Standing facts AppVersion 260619.75, the Round-9 PICK section moved to the archive as the decline record, the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r9 (engine r404" in s:
    print("already applied"); sys.exit(0)
# 1. Position: the build line (the corpus stays r403)
old = "- LAST SHIPPED: **r403** (build 260619.74, 19 Sept ≈15:05, session 27 Round 8"
assert s.count(old) == 1
s = s.replace(old, "- LAST SHIPPED: **r403** (build 260619.74 — the engine is at 260619.75 = r404 DECLINED-INERT, corpus byte-identical; 19 Sept ≈15:05, session 27 Round 8", 1)
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **1 of 3** — r404 a DECLINED-INERT round (no movement); r403's ≥50 +1 had RESET the window.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.74 (session 27 in progress);", "- Standing facts: AppVersion 260619.75 (session 27 in progress);", 1)
# 4. the Round-9 PICK section -> archive as the decline record
h = "## Session 27 — Round 9 PICK (engine r404, in progress; 19 Sept ≈15:25 NZST): the alert-top side column's class follows the subject — `col-md-4 offset-md-0 col-12 paddingL` in NCEA1 / Mathematics / TMoA"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
declined = sec.replace(h, "## Session 27 — Round 9 PICK (engine r404) DECLINED on measurement, shipped inert — the alert-top side column's class by subject (19 Sept ≈15:10 → 15:25 NZST)", 1)
declined += ("- **What happened:** built as a `#sideAlertCol` data map (`positional_side_alert.after_content.side_column_by_subject`, env `SIDECOLSUBJ_OFF`) and probed over all 416: "
             "OFF = disk 2109 / 2109; ON with {NCEA1, Mathematics, TMoA} 17 pages / 10 modules, scored **2 up / 0 down / 13 same, +1.4 pp-sum** — the subject share is a per-module "
             "mix of four spellings (MXFU301's gold `col-md-4 col-12 paddingL`, HIS1004's the offset form) and Claude's 56 alert-top pairs sit mostly in the English / LtL ties. "
             "DECLINED: the map ships EMPTY (the hook a no-op; ON with the empty map = disk 2109 / 2109), the `_doc` carries the measurement; AppVersion 260619.75; no regeneration, "
             "no ledger increment (scoped #7 since r396 — the next SHIP is the FULL backstop); every r403 baseline stands. The `alertActivity` sidebar (n = 414) is already Claude's "
             "form (0.48 = the plurality); the image sidebar (806) is the r331 declined class.\n")
a = rd(AR)
if "Round 9 PICK (engine r404) DECLINED" not in a:
    a = a.rstrip("\n") + "\n\n" + declined
    wr(AR, a); print("archive: r404 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r9 (engine r404, DECLINED-INERT, no regen) · THE ALERT-TOP SIDE COLUMN'S CLASS BY SUBJECT (the label census's `col-12 col-md-4 offset-md-0 paddingL` gold 392 / Claude 0; "
        "the two-column side-pair census `_s27_r9_sidepair.py`: the gold 0.51 corpus-wide, 0.70 / 0.75 / 0.86 in NCEA1 / Mathematics / TMoA — built as a `#sideAlertCol` map, probed 17 pages "
        "/ 10 modules for +1.4 pp-sum: a per-module mix of four spellings, Claude's pairs mostly in the English / LtL ties) · the map ships EMPTY (`SIDECOLSUBJ_OFF`), corpus byte-identical "
        "to r403 · 15:25 · plateau 1 of 3\n")
anchor = "- s27-r8 (engine r403)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
