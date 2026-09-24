#!/usr/bin/env python3
"""ROUND 492 finalise (session 46 Round 2 — the accordion panel after a table, ACCPANELBREAK_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 492," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.54";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 491 BASELINE"; a11 = "| `ACCMARKTABLE_OFF` | 491 |"; a14 = "- **Build:** `260620.54` (round 491"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 492 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈11:00, session 46 Round 1", "- LAST SHIPPED: **r491**",
          "- Before it: **r490**", "- Before them: **r488 → r467**", "- Plateau window (§4): **0 of 3** — r491", "- Standing facts: AppVersion **260620.54**",
          "## Round log", "**Next session starts with:**", "## Session 46 — Round 2 PICK (engine r492)", "- **(s46-r1) the accordion after r491"):
    find(p)

entry = """## 2026-09-25 (round 492, build 260620.55) — THE ACCORDION PANEL AFTER A TABLE: the scanner's "a [Body] after the table starts a new section" break is scoped to the current panel for the accordion — the [Body] / heading right after the writer's next `[accordion N] Title` is that panel's content (10 modules; 13 hand-off boxes fewer, 9 accordions built)

### 1. WHAT CHANGED

**The find** (session 46 Round 2 — the D10-3 accordion lane after r491). The 270 still-a-box accordions, by the builder's own guard (`_s46_whynull.cjs`, every `return null` in `InteractiveBuilder.js` rewritten IN MEMORY to record why it fired): 67 fail inside the member walk (buttons 17 across 11 modules, each a different kind), 41 in the D2 table reading (several small shapes), and **57 in D1 with a panel left EMPTY — mostly the LAST panel** (MXFL301 ×3, MXFU301, MXDB302, OSOH301, ENGR302, PWY1002, ENGJ102, CEDT501, CEDR501 …). Where the scanner ends each bundle (`_s46_scanend.cjs`): on the `[Body]` / `[H3]` right after the last panel's `[accordion N] Title` — `member_rule.body_terminates_after_table` / `heading_terminates_after_table` (the OSBY201 memoryGame rule, r352: after a TABLE-DATA widget has captured its table, a `[Body]` or heading starts a new section). The accordion carries `uses_data_table` (a D2 accordion IS its table), so a table inside panel 1 turned the next panel's opening `[Body]` into a section break: panel 2 came out empty, the whole accordion shipped as the hand-off box, and panel 2's content ran free below it (ENGJ102-2.0's accordion was even split into two bundles). Corpus-wide (`_s46_r2_scanend_all.cjs`, every bundle that rule closes): **accordion 18 bundles / 14 pages / 11 modules whose last captured member is the writer's own numbered panel delimiter** — every one a hand-off box; other types 0–5 each.

**The fix** (`InteractiveScanner` — the TABLE-DATA SECTION-BREAK check): for a type listed in `member_rule.panel_scoped_table_break.types` (the accordion, with its numbered-delimiter pattern), the break does not fire on the item IMMEDIATELY after the writer's new numbered panel delimiter — the panel's opening `[Body]` / heading is its content. Once the panel has opened the ordinary rule applies again (a first cut that suspended the break for the whole panel let OSOH201-1.0's last panel run on past the READYSAFE section; the refinement stops it). Data `member_rule.panel_scoped_table_break` (Interactive_Boundary_ChildTag_Bank.json), env `ACCPANELBREAK_OFF`.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed** (and the OFF render of the 10 modules is byte-identical to the saved r491 render `_r492_off`); ON **10 modules** — the accordion pages + later pages whose hand-off-box numbers drop by one where a split bundle re-merged (gate-excluded chrome). Regeneration + 12-module spot-check clean; `scoped_ship.sh` (first cut) FAIL on compare_structure exact −2 → **accepted NAMED** (`_fastloop_diff.py --accept-named`, `_r492_named.log`); the refinement's own scoped ship (`_r492b_scoped_ship.log`) **PASS**.
- **Accordion Still-a-box 270 → 257** (the dashboard; 9 accordions newly built — MXFL301 4.0 / 6.0 / 7.0, MXFU301 3.0, ENGJ102 2.0, ENGR302 5.0, CEDT501 2.0, CEDR501 6.0 (ten panels, one bundle to the writer's `[End accordions]`), PWY1002 2.1 — and split bundles re-merged). 27 of 28 new panel titles are gold accordion headings (`_s46_r1_headcheck.py _r492_on`); the free blocks that moved into the widget sit in the gold's own `accContent` (`_s46_freemoved.py`). `_verify_accordion.cjs` on the 10 modules: **86 panels, defect 0 ✓**.

### 3. PROTECTED GATES

- Skeleton **55.3709 % → 55.3852 % @ 2491 (+0.0144pp)**, RAW 39.321 → 39.340 %; **≥50 1585 → 1586 (+1)**, ≥75 277, ≥90 26; 13 movers, **10 up / 3 down NAMED** (`_r492_companion.py`): up CEDR501_6_0 +12.4, CEDT501_5_0 +4.4, PWY1002_2_1_0 +3.9, ENGR302_5_0 +3.8, MXDB302_7_0 +3.2, MXFL301_6_0 +2.7, MXFU301_3_0 +2.6, ENGJ102_2_0 +2.0, MXFL301_4_0 +2.0, OSOH301_1_0 +1.6; **down** CEDR501_3_0 −0.3 (position-free overlap 83 = 83 while Claude's unmatched lines fall 244 → 241 — precision rises; alignment), MXFL301_7_0 −0.5 (the moved paragraph "Some time problems require us to add or take away time…" is in the gold's own `accContent` — a correct move the aligned scorer reads as a dip), **OSOH201_1_0 −2.0** (A1, a developer substitution: the writer's `[Accordion 3] Taha whānau – social wellbeing` opens panel 3 with `[Body] To get the most out of your online learning it is important to connect…` + READYSAFE + its click-drop, exactly parallel to panels 1 and 2; the gold replaced the whole accordion with a shapeHover and freed that text; the writer's accordion is still a hand-off box here because panel 1's click-drop table cannot render inside a panel).
- **compare_structure exact 16702 → 16700 NAMED** (matched 19460 → 19458: CEDT501 −1 — the paragraph now sits inside the built accordion where the gold keeps it, `accContent`; OSOH301 −1 — the same shapeHover substitution as OSOH201); EXTRA 198 / missing 878 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): +0.0144pp (< 0.02) but ≥50 +1 — a protected bucket moved: neither counts nor resets; **0 of 3**.

**Recorded, not built:** the other terminators that empty an accordion's last panel — a `[video]` / `[audio]` after the delimiter (EXIP901 5.0, XDLS502 4.0, BLL266 2.0, XDLS501 1.0), CEDR401 / TEFUN08's `[Accordion] Title` + `[Dropdown text] body` vocabulary (the writer's `[Dropdown text]` read as a new dropDown widget; 11 bundles, 10 of them CEDR401 0.0); the accordions r492's capture now reaches but still decline — a panel table the kept-table emitter refuses (OSOH201 / OSOH301 / PWY1002 1.2), a leak-guard trip (CEDR501 3.0, CEDT501 5.0).

**Ledger:** scoped #2 since the r490 FULL · data `member_rule.panel_scoped_table_break` · env `ACCPANELBREAK_OFF` · code `InteractiveScanner` TABLE-DATA SECTION-BREAK · tools `_s46_whynull.cjs`, `_s46_r2_{whyrun,whyrun2,whyrun3}.sh`, `_s46_r2_{whyreport,parts}.py`, `_s46_scanend.cjs`, `_s46_r2_scanend_all.cjs`, `_s46_csdelta.py`, `_s46_freemoved.py`, `_r492_companion.py`, `_r492_finalise.py` · session 46 Round 2.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 492 (260620.55): THE ACCORDION PANEL AFTER A TABLE (session 46 Round 2) — the scanner's section break after a "
                "table-data widget's table does not fire on the [Body] / heading right after the writer's next numbered panel delimiter. "
                "Env ACCPANELBREAK_OFF.\n" + '\tstatic AppVersion = "260620.55";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 492 BASELINE (the accordion panel after a table, "
                "`ACCPANELBREAK_OFF`; SCOPED, scoped #2 since the r490 FULL; scoped_ship PASS after the NAMED cs −2; accordion Still-a-box 270 -> 257): "
                "SCAFFOLD mean 55.3852% / >=50% 1586 / >=75% 277 / >=90% 26 / RAW 39.340% @ 2491 pairs — +0.0144pp (10 up / 3 down NAMED), >=50 +1; "
                "cs exact 16700 (−2 NAMED); body / clean / leak EXACT.** Previous: **ROUND 491 BASELINE")
so = so.replace(a11, "| `ACCPANELBREAK_OFF` | 492 | **THE ACCORDION PANEL AFTER A TABLE** (session 46 Round 2). Reverts "
                "`member_rule.panel_scoped_table_break` (Interactive_Boundary_ChildTag_Bank.json): a [Body] / heading after an accordion's captured "
                "table ends the widget again even right after the writer's next `[accordion N] Title` — the last panel empties and the accordion "
                "ships as the hand-off box (10 modules); byte-identical to r491. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.55` (round 492 — **the accordion panel after a table**; `ACCPANELBREAK_OFF`; scoped #2 since the r490 "
                "FULL; 10 modules; Still-a-box 270 -> 257; skeleton 55.3852 % @ 2491, +0.0144pp, ≥50 +1; cs exact −2 NAMED).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r492.bak")
G = rd(P).split("\n")
def setv(key, old, new):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.54"', '"260620.55"'); setv("round", "491", "492")
insert_before("_note_r491", '    "_note_r492": "Round 492 (session 46 Round 2, 2026-09-25) — THE ACCORDION PANEL AFTER A TABLE (ACCPANELBREAK_OFF): 10 modules; '
              'Still-a-box 270 -> 257; SCAFFOLD 55.3709 -> 55.3852 @ 2491 (+0.0144pp, 10 up / 3 down NAMED); RAW 39.321 -> 39.340; >=50 1585 -> 1586; '
              'cs exact 16702 -> 16700 NAMED (CEDT501 / OSOH301 — moved inside the writer\'s accordion); body / clean / leak EXACT; scoped #2 since the '
              'r490 FULL.",')
setv("mean_scaffold_pct", "55.37", "55.39"); setv("pages_ge_50", "1585", "1586"); setv("raw_mean_pct", "39.32", "39.34")
insert_before("_note_r491_state", '    "_note_r492_state": "r492 (the accordion panel after a table): SCAFFOLD 55.3852 @ 2491, RAW 39.340; 13 movers (10 up / 3 down NAMED).",')
# compare_structure exact_chain / matched: set whichever keys carry 16702 / 19460
for i, l in enumerate(G):
    s = l.strip()
    if s.startswith('"exact_chain": 16702') or s.startswith('"exact": 16702'): G[i] = l.replace("16702", "16700")
    if s.startswith('"matched": 19460'): G[i] = l.replace("19460", "19458")
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")

shutil.copyfile(S, S + ".pre-r492-finalise.bak")
i = find("- **ROUND 492 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈11:45, session 46 Round 2 — r492 (the accordion panel after a table) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r492** (260620.55); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger **scoped #2** "
        "(6 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈11:00, session 46 Round 1"); prior = L[k]; del L[k]
k = find("- Before it: **r490**"); r490 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r491**"); L[k] = L[k].replace("- LAST SHIPPED: **r491**", "- Before it: **r491**", 1)
L.insert(k, "- LAST SHIPPED: **r492** (build 260620.55, 25 Sept ≈11:45, session 46 Round 2 — THE ACCORDION PANEL AFTER A TABLE, "
         "`ACCPANELBREAK_OFF`; SCOPED, **scoped #2 since the r490 FULL backstop**; a widget-BUILD round — **accordion Still-a-box 270 → 257**; "
         "**skeleton 55.3709 → 55.3852 % @ 2491 (+0.0144pp, 10 up / 3 down NAMED)**, **≥50 1586 (+1)**, ≥75 277, ≥90 26, RAW 39.340 %; "
         "**cs exact 16700 (−2 NAMED)**; body / clean / leak EXACT; `gate_baseline.json` at r492; the miner 194 CANDIDATE).")
k = find("- Before them: **r488 → r467**")
L[k] = L[k].replace("- Before them: **r488 → r467** (260620.52 → 260620.34 — the story-reference carousel shell,",
                    "- Before them: **r490 → r467** (260620.53 → 260620.34 — the LO WALT alert, the story-reference carousel shell,", 1)
assert "r490 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r491")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r491", "- Plateau window (§4): **0 of 3** — r492 +0.0144pp but ≥50 +1 (a protected "
                    "bucket moved: neither); r491", 1)
k = find("- Standing facts: AppVersion **260620.54**")
L[k] = L[k].replace("AppVersion **260620.54** (r491 the accordion marker-cell table — session 46 Round 1, 25 Sept); before it 260620.53",
                    "AppVersion **260620.55** (r492 the accordion panel after a table — session 46 Round 2, 25 Sept); before it 260620.54 (r491 the "
                    "accordion marker-cell table — session 46 Round 1); before it 260620.53", 1)
assert "260620.55" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r2 (engine r492, build 260620.55, 25 Sept ≈11:00 → 11:45) · THE ACCORDION PANEL AFTER A TABLE (the accordion lane: 57 of the "
         "270 still-a-box fail with a panel EMPTY — the scanner's body/heading-after-table section break fired on the `[Body]` right after the "
         "writer's next `[accordion N] Title`; scoped to the current panel) · SHIPPED scoped #2 · 10 modules, **Still-a-box 270 → 257** (9 built "
         "+ re-merged splits); verifier 86 panels defect 0 · skeleton +0.0144pp (10 up / 3 down NAMED), ≥50 +1, cs exact −2 NAMED · plateau 0 of 3 "
         "(neither).")
k = find("- **(s46-r1) the accordion after r491")
L.insert(k + 1, "- **(s46-r2) the accordion after r492 (257 still a box; `_s46_whynull.cjs` + `_s46_r2_whyreport.py` name each decline's guard):** "
         "the other last-panel terminators — a `[video]` / `[audio]` after the delimiter (EXIP901 5.0, XDLS502 4.0, BLL266 2.0, XDLS501 1.0) and "
         "CEDR401 / TEFUN08's `[Accordion] Title` + `[Dropdown text] body` vocabulary (11 bundles, 10 on CEDR401 0.0 — the writer's `[Dropdown "
         "text]` read as a new dropDown widget); accordions r492's capture now reaches that still decline — a panel table the kept-table emitter "
         "refuses (OSOH201 / OSOH301 / PWY1002 1.2), a leak-guard trip (CEDR501 3.0, CEDT501 5.0); the member-walk refusals (buttons 17 / 11 "
         "modules, each a different kind — dropbox upload, link buttons, instruction buttons).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r492** (260620.55, the "
        "accordion panel after a table); LAST FULL = **r490** (the s45 backstop); ledger scoped #2; plateau **0 of 3**; 2,491 pairs; census 552 / "
        "545 / 2,679. Ride-along patches `_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
k = find("## Session 46 — Round 2 PICK (engine r492)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 2 PICK (engine r492) — THE ACCORDION PANEL AFTER A TABLE — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 46 — Round 2 PICK (engine r492) + what shipped'; the one-line summary is the s46-r2 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r490 + the r491 no-round line (verbatim, s46 r492)\n\n" + r490 + "\n" + prior + "\n"
    "\n## Session 46 — Round 2 PICK (engine r492) + what shipped\n\n" + marker + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r492, 260620.55):** `member_rule.panel_scoped_table_break` (env `ACCPANELBREAK_OFF`) — the scanner's table-data "
    "section break does not fire on the item right after the writer's next numbered accordion delimiter. First cut (the break suspended for the "
    "whole panel) let OSOH201-1.0's last panel run past the READYSAFE section (−3.7, overlap 144 → 106) → refined to the opening item only (−2.0, "
    "the writer's panel-3 content, the gold's shapeHover substitution — NAMED). Probe OFF 0; ON 10 modules; Still-a-box 270 → 257; +0.0144pp, ≥50 "
    "+1; cs exact −2 NAMED (`_fastloop_diff.py --accept-named`); verifier 86 panels defect 0.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
