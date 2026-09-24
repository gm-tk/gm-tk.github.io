#!/usr/bin/env python3
"""ROUND 475 finalise (session 43 Round 7 — KB c75: the module menu keeps the writer's inline links, MENULINKS_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.38 -> 260620.39, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json (build / round /
note), KB_AMALGAMATION_STATUS.md row 75, LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line; the PICK →
archive). Line edits only; .bak kept; nothing written until every anchor is found. WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 475," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.38";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 474 BASELINE"; a11 = "| `WIDGETALT_OFF` | 474 |"; a14 = "- **Build:** `260620.38` (round 474"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k75 = "residue 41 external-host `div.button`s on other emitters (18 pages) |"
assert sk.count(k75) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 475 IN FLIGHT — NOT PROVEN**", "- **Before r475: no round in flight**", "- LAST SHIPPED: **r474**", "- Before it: **r473**",
          "- Plateau window (§4): **2 of 3** — r474", "- Standing facts: AppVersion 260620.38", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 7 PICK (engine r475)", "- Before them: **r472**"):
    find(p)

entry = """## 2026-09-24 (round 475, build 260620.39) — KB CONSTRAINT 75 IN THE MODULE MENU: the writer's inline links keep their href — the menu's text buffers now carry their items' hyperlinks into the free-body weave; the NCEA standard pages in the Standards / Information tabs, the modules' glossary and resource links

### 1. WHAT CHANGED

**The find** (session 43 Round 7 — two NEW instruments: the ATTRIBUTE census `outputs/_s43_r7_attrs.py` and the LINK census `_s43_r7_links.py` / `_s43_r7_inlinelinks.py`, which asks for every writer inline link `__words__ [LINK: url]` whether Claude kept the words, the href, or neither, by container × the gold's treatment). Triangulated on AGH1009-0.0's Standards tab ("__Agricultural and Horticultural Science 1.4__ [LINK: ncea.education.govt.nz/…]" → Claude `<p>` without the link; the gold's `<a href … target="_blank">`) and ANZH104-6.0 ("__Google Lens__ / __Seek by iNaturalist__" → plain text inside an activity box). **Mechanism:** `ListsAndRuns.inlineMarkup` weaves each paragraph's `block.links` onto its exact phrase, but several emitters pass NO links — `MenuBuilder`'s menu text buffers (`renderBlackText(textBuf.join("\\n"), run)`), table cells (`TablesAndGrids`), built-widget internals (deliberately). **The menu class:** 52 writer inline links lost from the module menus in ≈ 30 modules — the gold keeps 12 (the NCEA standard pages — AGH1009, COM1002, HIS1004, MXS1004 ×2, PES1001–1004, PES1008 — XDLS909, XTAS102) and drops 40 (D2L cross-module links, glossary / vocabulary documents, Drive folders). **KB constraint 75** ("inline → anchor", universal) makes the writer's link the target; the gold's omissions are NAMED overrides.

**The fix** (`MenuBuilder` — the section / tab builder and `#writerTabPane` each keep a link buffer beside their text buffer, filled from the buffered items' `block.links`, passed to `renderBlackText`; data `Emit_Templates.menu.inline_links` {enabled, env}; env **`MENULINKS_OFF`**, byte-identical OFF): the free-body weave (exact phrase, first occurrence per line, never inside an existing `<a>`) now runs on menu text too.

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r475`): **OFF 3222 / 3222 identical; ON 35 pages / 33 modules changed** — every change an added `<a>` on the writer's own phrase (AGH1009's journal "here" and its NCEA standard; GER1002's vocabulary documents and D2L resources; ENGC403 / ENGI405 / ENGS404's ENFUN module links …).
- Regeneration of the 33 + the 12-module spot-check (`_r475_regen.sh`): 0 truly stale, spot-check 12 / 12 byte-identical; `scoped_ship.sh` containment OK (33 ⊆ 33) and its decomposition flagged the skeleton's −0.0006pp (below); committed NAMED with `_fastloop_diff.py --accept-named` (the r470 precedent — `_r475_fastloop_named.log`). (The post-ship feature-index rebuild rewrote `Module_Feature_Index.json` with identical bytes and a newer mtime; the 33 were regenerated once more before the named commit.)
- The link census after (`_r475_inlinelinks_after.log`): menu links the gold keeps, lost **12 → 2**; menu links the gold drops, lost 44 → 19 (the rest: the phrase occurs earlier on its line — "here", "activity").

### 3. PROTECTED GATES

- Skeleton **55.2315 % → 55.2309 % @ 2491 (−0.0006pp)**, ≥50 1577, ≥75 276, ≥90 25, RAW 39.194 → 39.192 %; 5 movers, **1 up / 4 down — NAMED (KB c75 over the gold):** GEO1005_1_0 −0.3 (the writer's "GLOSSARY GEO 2.docx" link), XLP03_0_0 −0.3 ("see PDF"), ENGI405_0_0 −0.4 (the ENFUN module list + the Te Kura library link), XLP04_0_0 −0.5 ("Sensory Materials for Home Learning") — flat (untabbed) menus, where the skeleton sees the `<a>` the gold dropped; movers outside the affected set 0.
- compare_structure 16758 / 208 / 903, body 238, clean 2587 / 2633, leak 75 / 46 — HELD; every verifier RESULT line identical to r474; 17 selftests + the skeleton selftest green; the feature index green; the miner 197 CANDIDATE @ 2491.
- Plateau (§4): a KB-rule round that predicted no skeleton move (the menu is one WIDGET line except on flat menus) and delivered −0.0006pp NAMED — neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #1 since the r474 FULL · data `menu.inline_links` · env `MENULINKS_OFF` · code `MenuBuilder` (the two text buffers + `#menuLinksOn`) · tools `outputs/_s43_r7_{attrs,links,inlinelinks,bodylinks}.py`, `_r475_{regen,postship,commit_named,checksums}.sh`, `_r475_finalise.py`. **Follow-ups (recorded):** the same census's other link-dropping paths — activity boxes (33 gold-kept links / 6 modules: ANZH104's Google Lens, CEDT301's Te Ara), free body (30 / 8: AGH1009's Yara N-Sensor, ANZH205's Waitangi Treaty Grounds), alerts (18 / 7: OSBY401's Netsafe form), table cells (54 / 13, but 388 more the gold drops — mostly picture-source pointers, a precision question), widget internals (accordion 6, speechBubble 4); Claude's Bilingual audio players ship no `src` / `title` (551, TRR / PMT — KB 04C's form carries both; the gold names them after the reo phrase).

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 475 (260620.39): KB c75 — THE MODULE MENU KEEPS THE WRITER'S INLINE LINKS (session 43 Round 7). MenuBuilder's text "
                "buffers carry their items' block.links into ListsAndRuns.renderBlackText (the free-body weave). Env MENULINKS_OFF.\n"
                '\tstatic AppVersion = "260620.39";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 475 BASELINE (KB c75 — the module menu keeps the writer's "
                "inline links, `MENULINKS_OFF`; SCOPED, scoped #1 since the r474 FULL): SCAFFOLD mean 55.2309% / >=50% 1577 / >=75% 276 / "
                ">=90% 25 / RAW 39.192% @ 2491 pairs — −0.0006pp NAMED (4 flat-menu pages carry the writer's resource links the gold drops: "
                "GEO1005_1_0, XLP03_0_0, ENGI405_0_0, XLP04_0_0); cs / body / clean / leak EXACT; menu links the gold keeps, lost 12 → 2.** "
                "Previous: **ROUND 474 BASELINE")
so = so.replace(a11, "| `MENULINKS_OFF` | 475 | **KB c75 — THE MODULE MENU KEEPS THE WRITER'S INLINE LINKS** (session 43 Round 7). Reverts "
                "`menu.inline_links`: the menu's text buffers render without their items' hyperlinks again — 35 pages / 33 modules lose the "
                "writer's links (the NCEA standard pages in the Standards tabs, glossary / resource documents); byte-identical to r474. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.39` (round 475 — **KB c75: THE MODULE MENU KEEPS THE WRITER'S INLINE LINKS**; `MENULINKS_OFF`; "
                "scoped #1 since the r474 FULL; 35 pages / 33 modules; skeleton 55.2309 % @ 2491, −0.0006pp NAMED).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k75, "residue 41 external-host `div.button`s on other emitters (18 pages). **r475 (24 Sept 2026, session 43 Round 7): the "
                "INLINE half in the module MENU — the menu's text buffers now weave the writer's inline links (`menu.inline_links`, "
                "`MENULINKS_OFF`; 35 pages / 33 modules; gold-kept menu links lost 12 → 2). Still PARTIAL for inline links in activity boxes "
                "(33 gold-kept / 6 modules), free body (30 / 8), alerts (18 / 7), table cells (54 / 13) — `outputs/_s43_r7_inlinelinks.py`.** |")
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r475.bak")
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
setv("build", '"260620.38"', '"260620.39"'); setv("round", "474", "475")
insert_before("_note_r474", '    "_note_r475": "Round 475 (session 43 Round 7, 2026-09-24) — KB c75: THE MODULE MENU KEEPS THE WRITER\'S INLINE LINKS (MENULINKS_OFF): '
              '35 pages / 33 modules; SCAFFOLD 55.2315 -> 55.2309 @ 2491 (-0.0006pp NAMED: GEO1005_1_0 -0.3, XLP03_0_0 -0.3, ENGI405_0_0 -0.4, '
              'XLP04_0_0 -0.5 — flat menus carrying the writer\'s resource links the gold drops), RAW 39.194 -> 39.192; cs / body / clean / leak '
              'EXACT; scoped #1 since the r474 FULL; committed NAMED (_fastloop_diff --accept-named).",')
insert_before("_note_r473_state", '    "_note_r475_state": "r475 (the menu inline links): SCAFFOLD 55.2309 @ 2491, RAW 39.192; 5 movers (1 up / 4 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r475-finalise.bak")
i = find("- **ROUND 475 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈21:40 real clock, session 43 Round 7 — r475 (KB c75, the menu's inline links) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r475** (260620.39); **LAST FULL = r474**; ledger **scoped #1** (7 of "
        "headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r475: no round in flight**"); prior = L[k]; del L[k]
k = find("- Before it: **r473**"); r473 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r474**"); L[k] = L[k].replace("- LAST SHIPPED: **r474**", "- Before it: **r474**", 1)
L.insert(k, "- LAST SHIPPED: **r475** (build 260620.39, 24 Sept ≈21:40 real clock, session 43 Round 7 — KB c75: THE MODULE MENU KEEPS THE "
         "WRITER'S INLINE LINKS, `MENULINKS_OFF`; SCOPED, **scoped #1 since the r474 FULL**, committed NAMED (the r470 precedent); **skeleton "
         "55.2315 → 55.2309 % @ 2491 (−0.0006pp NAMED: 4 flat-menu pages)**, ≥50 1577, ≥75 276, ≥90 25, RAW 39.192 %; cs / body / clean / "
         "leak EXACT; gold-kept menu links lost 12 → 2; `gate_baseline.json` at r475; the miner 197 CANDIDATE).")
k = find("- Before them: **r472**")
L[k] = L[k].replace("- Before them: **r472**", "- Before them: **r473** (260620.37, the modal text fence — verbatim → LOOP_STATE_ARCHIVE.md "
                    "'Position — LAST SHIPPED r473 (verbatim, s43 r475)'), **r472**", 1)
k = find("- Plateau window (§4): **2 of 3** — r474")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r474", "- Plateau window (§4): **2 of 3** — r475 a KB-rule round, −0.0006pp NAMED "
                    "(neither counts nor resets); r474", 1)
k = find("- Standing facts: AppVersion 260620.38")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.38 (r474", "- Standing facts: AppVersion 260620.39 (r475 KB c75 the menu's inline "
                    "links — session 43 Round 7, 24 Sept); before it 260620.38 (r474", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r7 (engine r475, build 260620.39, 24 Sept ≈21:05 → 21:40 real clock) · KB c75: THE MODULE MENU KEEPS THE WRITER'S INLINE "
         "LINKS (two new instruments: the attribute census + the link census) · SHIPPED scoped #1, committed NAMED · 35 pages / 33 modules; "
         "gold-kept menu links lost 12 → 2 · skeleton −0.0006pp (4 flat-menu pages NAMED) · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r475** (260620.39, "
        "KB c75 the menu's inline links); LAST FULL = **r474**; ledger scoped #1; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. "
        "Ride-along patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 43 — Round 7 PICK (engine r475)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 7 PICK (engine r475) — KB c75: THE MODULE MENU KEEPS THE WRITER'S INLINE LINKS — SHIPPED; the PICK + "
         "what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 43 — Round 7 PICK (engine r475) + what shipped'; the one-line summary "
         "is the s43-r7 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r473 (verbatim, s43 r475)\n\n" + r473 + "\n"
    "\n## Session 43 — Round 7 PICK (engine r475) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r475, 260620.39):** `menu.inline_links` (env `MENULINKS_OFF`) — MenuBuilder's two text buffers carry their items' "
    "`block.links` into `renderBlackText`. Probe OFF 3222 identical / ON 35 pages / 33 modules (every change an `<a>` on the writer's "
    "phrase); regenerated + spot-check; scoped_ship containment OK, decomposition −0.0006pp → committed NAMED (4 flat-menu pages); "
    "gold-kept menu links lost 12 → 2.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
