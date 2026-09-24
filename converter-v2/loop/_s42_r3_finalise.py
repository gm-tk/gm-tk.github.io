#!/usr/bin/env python3
"""Session 42 Round 3 finalise — THE PLACEMENT CENSUS built (a measurement-tool round, no engine change; build 260620.33 unchanged):
BUILD_CHANGELOG.md entry, LOOP_STATE.md (marker cleared, the census finds as Follow-up candidates, Needs Chris #22, round log).
Line edits only; .bak kept. Run under WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "session 42 Round 3" not in sc[:4000]
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 3 (session 42) IN FLIGHT", "- **Before Round 3: no round in flight**", "## Round log",
          "- **(D14-S1 placement residue, s41) already measured", "21. ~~**24 Sept (session 41 Round 12)**"):
    find(p)
entry = """## 2026-09-24 (session 42 Round 3 — no engine change; build 260620.33 unchanged) — THE PLACEMENT CENSUS (LOOP §1g, Chris's D14-S1): one standing probe that says where the human puts each piece of content and where Claude puts it — the module menu's panes, activity boxes, widgets, alerts, side columns — the regions the skeleton collapses

**The tool** (`outputs/_placement_census.py`, run from `reference/tests` under WSL; 77 s over the corpus): every text block (h1–h6 / p / li / td / th / figcaption / dt / dd, ≥ 20 characters or ≥ 4 words) on the gold page and on Claude's paired page is tagged with its CONTAINER PATH — `header:chip|other`, `menu:<pane>` (the nav label canonicalised: Overview / Knowledge / Practices / Information / Standards / LI / Lesson / paneN, or `flat`), `body[:panelN]:<widget:type|activity|alert|acks|free>[:side]`, `footer`, `acks` — then matched by text (exact → 40-character prefix → token Jaccard ≥ 0.7 on the paired page; exact / prefix on the module's other Claude pages = OTHER-PAGE; else ABSENT, split by the module's Writers Template: ABSENT-inWT a derivable loss, ABSENT-notWT the developer's own words). Output `outputs/_placement_census.{md,json}`: the transition table (gold region → Claude region / fate, blocks / pages / modules / the best family's share / templates / a flag against the §1d floors — `not derivable`, `acks gate`, `un-built widget (A1)` are never candidates), the headings-only table (the SECTIONS), region agreement, and examples. Population `_corpus.gate_mods()`; pairing `_discrepancy_audit.pairs()`. It folds `_r460_rawmenu.py`, `_s41_r8_kppane.py`, `_s41_r8_lost.py` and `_s41_r10_boxtitle2.py`. Companion: `outputs/_s42_r4_navtabs.py` (the overview's nav tab SET, gold vs Claude, per module).

**The first census (r466 corpus, 533 modules / 2,488 pairs / 163,390 gold blocks):** SAME 39.6 % · MOVED 22.7 % · OTHER-PAGE 5.0 % · ABSENT-inWT 5.5 % · ABSENT-notWT 27.1 %. The chrome finds: (1) **the Standards / Assessment tab** — 27 modules' gold opens a Standards pane with the writer's "Assessment for Learning" heading (ART / CBI / COM / DAN / DTC / GEO / GER / HIS / MUS / PWY / SPA / XTAS / EXBP) and Claude folds it into Information, while 49 modules already match (KB constraint 67 / CL-0040's Standards/Assessment tab) → the next round; (2) **BLL's Knowledge / Practices** stay in Claude's Overview pane in 19 BLL2xx modules where the gold always moves them out — own tabs 10–11, Information 7 (≈ 0.59–0.61; the writer's "Tab 2 – Information" note does not separate the two; CL-0040 leaves the BLL tab split open) → Needs Chris #22; (3) `menu:LI → menu:Overview` 12 modules (a Learning-Intentions tab, mixed families); (4) `menu:flat → body:free` 303 blocks / 85 pages / 44 modules (a lesson menu's WALT block the gold keeps in the menu). The body finds (each needs its own split before a round): `body:alert → body:free` 1,262 blocks / 375 pages / 167 modules; `widget → free` (accordion 1,185 / 142 / 83, tabs 643 / 72 / 59, wordHighlighter 436 / 55 / 42 — WJFUN 277); `body:free:side → body:free` 145 / 50 / 40 (HIS 0.77); the quiz text inside Claude's activity box (multiChoiceQuiz 355 / 57 / 43, radioQuiz 167 / 29 / 22).

No converter output changed; no gate moved; plateau: a measurement-tool round neither counts nor resets. Tools `outputs/_placement_census.{py,md,json,log}`, `_pc_test.md`, `_s42_r4_navtabs.{py,log}`, `_s42_r3_finalise.py`.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
shutil.copyfile(S, S + ".pre-s42-r3-finalise.bak")
i = find("- **ROUND 3 (session 42) IN FLIGHT"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈15:15, session 42 Round 3 — THE PLACEMENT CENSUS built and run, a measurement-tool round; "
        "committed). LAST SHIPPED **r466** (260620.33); **LAST FULL = r460**; ledger **scoped #2**. Next: Round 4 = the Standards / "
        "Assessment tab (KB c67; 27 modules — `outputs/_s42_r4_navtabs.log`).")
k = find("- **Before Round 3: no round in flight**"); prior = L[k]; del L[k]
k = find("- **(D14-S1 placement residue, s41) already measured")
L.insert(k, "- **(s42-r3) THE PLACEMENT CENSUS — the standing §1g probe `outputs/_placement_census.py` (re-run it in every PICK pass; "
         "`_placement_census.md` is the ranked table).** First run on the r466 corpus: SAME 39.6 % / MOVED 22.7 % / OTHER-PAGE 5.0 % / "
         "ABSENT-inWT 5.5 % / ABSENT-notWT 27.1 % of 163,390 gold blocks. **Its finds, each a candidate for its own PICK:** "
         "(P1) the Standards / Assessment tab — 27 modules, KB c67 → **Round 4**; (P2) BLL Knowledge / Practices out of Overview — 19 "
         "BLL2xx modules, gold own tabs 10–11 / Information 7, never Overview → Needs Chris #22; (P3) `menu:LI → menu:Overview` 153 "
         "blocks / 12 modules (XMES 0.98 in 3; TRR, BLL, MXEX, MXS, PMT, PWY, WJFUN — a Learning-Intentions tab the gold builds); "
         "(P4) `menu:flat → body:free` 303 blocks / 85 pages / 44 modules (TEDC 67, CBI 37, MXEX 34, EXPFUN 0.86 — the lesson menu's "
         "WALT / LI block the gold keeps in the menu, Claude in the body); (P5) `body:alert → body:free` 1,262 blocks / 375 pages / 167 "
         "modules (HIS 96, PES 95, HPRE 81, XGF 77, CEDO 74, TRR 70 — split by the WT's alert tag first); (P6) gold widget → Claude "
         "free text: accordion 1,185 / 142 pages / 83 modules (XGF 139, MXFL 96, ENGFUN 89, TEFUN 0.74), tabs 643 / 72 / 59 (TEFUN "
         "0.70), wordHighlighter 436 / 55 / 42 (WJFUN 277, 0.72) — tagged-but-unrecognised vs the developer's choice (class C) is "
         "the first split; (P7) `body:free:side → body:free` 145 / 50 / 40 (HIS 0.77 — the gold's side column); (P8) quiz text "
         "inside Claude's activity box: multiChoiceQuiz 355 / 57 / 43 (PES 0.73), radioQuiz 167 / 29 / 22 (the D13-4 lane). "
         "Largest non-derivable rows for the record: acks (the acks gate), `body:activity → ABSENT-notWT` 5,305, `body:free → "
         "ABSENT-notWT` 4,943. Evidence `outputs/_placement_census.{md,json}`, `_s42_r4_navtabs.log`.")
k = find("21. ~~**24 Sept (session 41 Round 12)**")
L.insert(k + 1, "22. **24 Sept (session 42 Round 3, the placement census)** — **BLL2xx overview: Knowledge / Practices in their own tabs or "
         "in Information?** Claude keeps them in the Overview pane in 19 BLL2xx modules; the gold NEVER does — own tabs in 10–11 "
         "(BLL247 / 253 / 261 / 262 / 265 / 271–274 / 276, BLL250's one combined tab), Information in 7 (BLL251 / 255 / 257 / 263 / "
         "264 / 266 / 275) — ≈ 0.59–0.61, under or at the 0.60 line; the writer's \"Tab 2 – Information\" note appears on both sides; "
         "KB CL-0040 leaves the BLL overview tab split open (the BLL263 D2 question). Options: A own tabs (the KB c67 canonical form, "
         "r460's rule with BLL no longer excluded — the 7 Information golds become named overrides), B Information, C leave. "
         "Recommended: A. Holds up 19 modules' overview menus.")
k = find("## Round log")
L.insert(k + 1, "- s42-r3 (no engine change, 24 Sept 14:58 → ≈15:15) · THE PLACEMENT CENSUS (§1g, D14-S1): `outputs/_placement_census.py` "
         "built (folds the four s41 probes) and run — 163,390 gold blocks, MOVED 22.7 %; finds P1–P8 recorded in Follow-up candidates "
         "(the Standards tab 27 modules → Round 4; BLL K / P → Needs Chris #22) · a measurement-tool round · plateau 2 of 3 (neither).")
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 42 — Round 3 (the placement census, no engine change)\n\n" + marker + "\n" + prior + "\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
