#!/usr/bin/env python3
"""ROUND 493 finalise (session 46 Round 3 — the BLL closing section after the dropbox button, DROPBOXEND_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 493," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.55";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 492 BASELINE"; a11 = "| `ACCPANELBREAK_OFF` | 492 |"; a14 = "- **Build:** `260620.55` (round 492"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 493 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈11:45, session 46 Round 2", "- LAST SHIPPED: **r492**",
          "- Before it: **r491**", "- Before them: **r490 → r467**", "- Plateau window (§4): **0 of 3** — r492", "- Standing facts: AppVersion **260620.55**",
          "## Round log", "**Next session starts with:**", "## Session 46 — Round 3 PICK (engine r493)", "- **(s46-r2) the accordion after r492"):
    find(p)

entry = """## 2026-09-25 (round 493, build 260620.56) — THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON: in the Blended Literacy modules, a widget capture that already holds the writer's `[Button] Upload to dropbox` ends at the module's closing `[image]` / `[body]` — the celebration picture + "Congratulations on completing this module…" render free, as in the gold (a family dialect, 13 modules)

### 1. WHAT CHANGED

**The PICK pass** (session 46 Round 3 — the §1g placement census, the loss ledger, the miner's chrome rows): the census re-run (`_placement_census_s46`) — its CANDIDATE rows are the s42 class-C declines, and two rows (dropDown / flipCard text "ABSENT" from every Claude page, 617 / 546 blocks) are an instrument artefact: the text sits inside an un-built widget's hand-off table cell with the writer's options joined (`Start of a book. / Middle of a book. / End of a book.`); the loss ledger's never-worked MXFL2 (38 pages, 42.5 %) is the r436-declined repeated overview menu + row composition; miner row #5 (a second header span, 21 modules) is four different mechanisms each under the chrome floor; the accordion's D2 table refusals after r491 are five small shapes (≈ 12 bundles). All recorded in LOOP_STATE.md.

**The find** (the gathering lane): `_s46_r3_swallow.py` — text the gold keeps FREE that Claude ships inside an un-built widget's hand-off box — then `_s46_r3_pastdropbox.cjs` (every bundle that captured more members after the writer's `[Button] Upload to dropbox`): 59 bundles, 51 of them only the button line's own `[trigger engagement]` tag; **18 with real content after it, 13 of them the Blended Literacy module's CLOSING section** — after the last activity's `[Button] Upload to dropbox [trigger engagement]` the writer ends the module with a celebration `[image]` (a 3D party popper / trophy) and `[body] Congratulations on completing this module…` (BLL272 / 273 `Ka rawe tō mahi!`), and the last widget's member walk (modal ×5, clickDrop ×5, unclassified ×2, typing ×1 — BLL210's is a 12-modal + carousel bundle for Activity 8G) swallowed both into its hand-off box. The activity box itself already closes at that button (r376). **The gold keeps them FREE on every checked page (10 / 10)** — `div#body > (div.inquiryPanel >) div.row > div.col-md-8 / col-md-6 > p`.

**The fix** (`InteractiveScanner.#swallowMembers`, beside the table-data section break): in a module `member_rule.dropbox_button_ends_capture.module_pattern` names (`^BLL\\d`), a `[body]` / `[image]` (stop_tags) after a captured upload-to-dropbox button member (button_label_pattern on its own text + black line) ends the walk; the closing picture and text then render as free body after the activity. A §1d exception-1 FAMILY DIALECT: keyed to one family by data, 13 pages (under the 20-page floor), matching the family's own gold on every checked page, OFF byte-identical, every other gate held. The other five past-the-button captures (XDLS903 / 906's next `[click drop]` item, CEDT404's checklist black lines, BLL254 1.0's noise tag) are untouched. Env `DROPBOXEND_OFF`.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **13 modules / 13 pages** (+ their `_interactives.txt`) — exactly the 13 BLL modules; e.g. BLL230_0_0 now ends `div.row > div.col-md-8 > img (iStock-1461683255 "3D Two Party Popper") + p "Congratulations on completing this module…"` after the activity box. Regeneration + 12-module spot-check clean; `scoped_ship.sh` FAIL on compare_structure missing +1 only → **accepted NAMED** (`_r493_named.log`: matched +9 across the 13 modules, exact +8 — every one a NEW match of the closing paragraph; BLL170's new match carries one wrapper the gold adds).

### 3. PROTECTED GATES

- Skeleton **55.3852 % → 55.3885 % @ 2491 (+0.0032pp)**, RAW 39.340 → 39.342 %; ≥50 1586, ≥75 277, ≥90 26 HELD; 13 movers, **11 up / 2 down NAMED** (`_r493_companion.py`): up BLL254_2_0 +2.1, BLL273_2_0 +1.9, BLL272_2_0 +1.5, BLL256_2_0 +1.4 …; down BLL243_1_1 −0.7 (position-free overlap 93 → 94) and BLL160_0_0 −0.1 (502 → 503) — alignment.
- **compare_structure exact 16700 → 16708 (+8)**, matched 19458 → 19467, **missing 878 → 879 NAMED** (a new match); EXTRA 198 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): +0.0032pp — a PICK that predicted a skeleton move and delivered < 0.02pp, but cs exact +8 (a protected gate moved): neither counts nor resets; **0 of 3**.

**Ledger:** scoped #3 since the r490 FULL · data `member_rule.dropbox_button_ends_capture` · env `DROPBOXEND_OFF` · code `InteractiveScanner.#swallowMembers` · tools `_placement_census_s46.{md,json}`, `_s46_r3_swallow.py`, `_s46_r3_pastdropbox.cjs`, `_r493_companion.py`, `_r493_finalise.py` · session 46 Round 3.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 493 (260620.56): THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON (session 46 Round 3) — in the BLL family a widget "
                "capture holding an upload-to-dropbox button ends at the following [body] / [image]. Env DROPBOXEND_OFF.\n" + '\tstatic AppVersion = "260620.56";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 493 BASELINE (the BLL closing section after the dropbox "
                "button, `DROPBOXEND_OFF`; SCOPED, scoped #3 since the r490 FULL; cs missing +1 NAMED): SCAFFOLD mean 55.3885% / >=50% 1586 / "
                ">=75% 277 / >=90% 26 / RAW 39.342% @ 2491 pairs — +0.0032pp (11 up / 2 down NAMED); cs exact 16708 (+8), missing 879 (+1 NAMED, a "
                "new match); body / clean / leak EXACT.** Previous: **ROUND 492 BASELINE")
so = so.replace(a11, "| `DROPBOXEND_OFF` | 493 | **THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON** (session 46 Round 3). Reverts "
                "`member_rule.dropbox_button_ends_capture` (Interactive_Boundary_ChildTag_Bank.json): the last BLL widget's capture runs past the "
                "writer's `[Button] Upload to dropbox` again and swallows the module's closing picture + Congratulations text into its hand-off box "
                "(13 BLL modules); byte-identical to r492. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.56` (round 493 — **the BLL closing section after the dropbox button**; `DROPBOXEND_OFF`; scoped #3 since "
                "the r490 FULL; 13 modules / 13 pages; skeleton 55.3885 % @ 2491, +0.0032pp; cs exact +8).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r493.bak")
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
setv("build", '"260620.55"', '"260620.56"'); setv("round", "492", "493")
insert_before("_note_r492", '    "_note_r493": "Round 493 (session 46 Round 3, 2026-09-25) — THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON (DROPBOXEND_OFF): '
              '13 BLL modules / 13 pages; SCAFFOLD 55.3852 -> 55.3885 @ 2491 (+0.0032pp, 11 up / 2 down NAMED); RAW 39.340 -> 39.342; cs exact '
              '16700 -> 16708, missing 878 -> 879 NAMED (a new match, BLL170); body / clean / leak EXACT; scoped #3 since the r490 FULL.",')
setv("exact_chain", "16700", "16708"); setv("claude_missing_container", "878", "879")
insert_before("_note_r492_state", '    "_note_r493_state": "r493 (the BLL closing section): SCAFFOLD 55.3885 @ 2491, RAW 39.342; 13 movers (11 up / 2 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")

shutil.copyfile(S, S + ".pre-r493-finalise.bak")
i = find("- **ROUND 493 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈12:10, session 46 Round 3 — r493 (the BLL closing section after the dropbox button) SHIPPED "
        "and committed; the in-flight marker is cleared). LAST SHIPPED **r493** (260620.56); **LAST FULL = r490 (the s45 Round 10 backstop)**; "
        "ledger **scoped #3** (5 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` "
        "(buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈11:45, session 46 Round 2"); prior = L[k]; del L[k]
k = find("- Before it: **r491**"); r491 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r492**"); L[k] = L[k].replace("- LAST SHIPPED: **r492**", "- Before it: **r492**", 1)
L.insert(k, "- LAST SHIPPED: **r493** (build 260620.56, 25 Sept ≈12:10, session 46 Round 3 — THE BLL CLOSING SECTION AFTER THE DROPBOX "
         "BUTTON, `DROPBOXEND_OFF`; SCOPED, **scoped #3 since the r490 FULL backstop**; a family dialect (§1d exception 1); **skeleton 55.3852 → "
         "55.3885 % @ 2491 (+0.0032pp, 11 up / 2 down NAMED)**, ≥50 1586, ≥75 277, ≥90 26, RAW 39.342 %; **cs exact 16708 (+8)**, missing 879 "
         "(+1 NAMED, a new match); body / clean / leak EXACT; `gate_baseline.json` at r493; the miner 194 CANDIDATE).")
k = find("- Before them: **r490 → r467**")
L[k] = L[k].replace("- Before them: **r490 → r467** (260620.53 → 260620.34 — the LO WALT alert,",
                    "- Before them: **r491 → r467** (260620.54 → 260620.34 — the accordion marker-cell table, the LO WALT alert,", 1)
assert "r491 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r492")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r492", "- Plateau window (§4): **0 of 3** — r493 +0.0032pp but cs exact +8 (a "
                    "protected gate moved: neither); r492", 1)
k = find("- Standing facts: AppVersion **260620.55**")
L[k] = L[k].replace("AppVersion **260620.55** (r492 the accordion panel after a table — session 46 Round 2, 25 Sept); before it 260620.54",
                    "AppVersion **260620.56** (r493 the BLL closing section — session 46 Round 3, 25 Sept); before it 260620.55 (r492 the accordion "
                    "panel after a table — session 46 Round 2); before it 260620.54", 1)
assert "260620.56" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r3 (engine r493, build 260620.56, 25 Sept ≈11:40 → 12:10) · a PICK pass (census re-run, loss ledger, miner row #5, the "
         "accordion D2 residue — all recorded) then THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON (the gathering lane: the last widget's "
         "capture swallowed the module's closing picture + Congratulations text past `[Button] Upload to dropbox`; gold free 10 / 10; a family "
         "dialect) · SHIPPED scoped #3 · 13 BLL modules / pages · skeleton +0.0032pp (11 up / 2 down NAMED), cs exact +8, missing +1 NAMED · "
         "plateau 0 of 3 (neither).")
k = find("- **(s46-r2) the accordion after r492")
L.insert(k + 1, "- **(s46-r3) the PICK pass residue:** the gathering lane's other boxes (`_s46_r3_swallow.log`: gold-free text inside Claude "
         "hand-off boxes — unclassified 121 blocks / 37 pages / 32 modules, flipCard 88 / 16 / 15, carousel 45 / 14 / 13 … — the next gathering "
         "measure is the unclassified box's end: which terminator it misses); the accordion's D2 table refusals (≈ 12 bundles, five shapes — "
         "the flip-card-word label row `front || drop`, label + picture-only rows, `[accordion tab N]` / `[Accordion Item N title]` / `[insert "
         "accordion N]` marker words, bulleted bold leads in cells, a trailing `[go to journal]` row); miner row #5 by mechanism (BLL27x `Module "
         "N – Te Reo Māori` bar: the `Module N` chip where the gold has the module code + a fetched `Blended Literacy Learning` half, 6 modules; "
         "WJFUN105's `(Te Reo)` placeholder span; AGH1005 / XDLS904 subtitle splits); the census's dropDown / flipCard ABSENT rows are an "
         "instrument artefact (joined options inside a hand-off table cell).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r493** (260620.56, the "
        "BLL closing section); LAST FULL = **r490** (the s45 backstop); ledger scoped #3; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / "
        "2,679. Ride-along patches `_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
k = find("## Session 46 — Round 3 PICK (engine r493)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 3 PICK (engine r493) — THE BLL CLOSING SECTION AFTER THE DROPBOX BUTTON — SHIPPED; the PICK + what-shipped "
         "record is in LOOP_STATE_ARCHIVE.md 'Session 46 — Round 3 PICK (engine r493) + what shipped'; the one-line summary is the s46-r3 "
         "Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r491 + the r492 no-round line (verbatim, s46 r493)\n\n" + r491 + "\n" + prior + "\n"
    "\n## Session 46 — Round 3 PICK (engine r493) + what shipped\n\n" + marker + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r493, 260620.56):** `member_rule.dropbox_button_ends_capture` (env `DROPBOXEND_OFF`; module_pattern `^BLL\\d`). Probe "
    "OFF 0; ON 13 modules / 13 pages; scoped_ship FAIL on cs missing +1 → accepted NAMED (a new match); +0.0032pp, 11 up / 2 down NAMED; cs "
    "exact +8.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
