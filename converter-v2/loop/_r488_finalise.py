#!/usr/bin/env python3
"""ROUND 488 finalise (session 45 Round 5 — the story-reference carousel shell, CARSTORY_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 488," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.51";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 487 BASELINE"; a11 = "| `HOVERNAMED_OFF` | 487 |"; a14 = "- **Build:** `260620.51` (round 487"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 488 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈06:35, session 45 Round 2", "- LAST SHIPPED: **r487**",
          "- Before it: **r486**", "- Before them: **r485 → r467**", "- Plateau window (§4): **0 of 3** — r487", "- Standing facts: AppVersion **260620.51**",
          "## Round log", "**Next session starts with:**", "## Session 45 — Round 5 PICK (engine r488)", "- **(s45-r2) the hover markers after r487"):
    find(p)
entry = """## 2026-09-25 (round 488, build 260620.52) — THE STORY-REFERENCE CAROUSEL SHELL: a carousel whose members are the writer's `[embed book N]` / `[embed story]` reference builds the r126 story shell + a Designer/Developer To Do (43 hand-off boxes → built carousels)

### 1. WHAT CHANGED

**The find** (session 45 Round 5 — the hand-off-box lane: the coverage dashboard's un-built carousels and `WHY_UNBUILT__carousel.md` reason 1): the writer asks for a decodable / School Journal story to be paged through as a carousel — `[carousel]` + `[embed book 1] Are we able to embed just the story into the module … Also is it possible to put the story into a carousel so it’s like turning the pages …` + `The story ‘Zac hid from Dad’ can be found - (in Set 5)` + the story's PDF link (BLL152, the BLL1 / BLL2 phonics families). The human builds `div.row.carousel > viewer > item.image > img` × the story's pages, cut from the PDF by hand (BLL152-2.0) — the page count is nowhere in the WT, so the SLIDES are not derivable; the SHELL is, and since r126 the ordinary-text path emits exactly that shell for an `[embed story]` line — but a member captured inside a carousel bundle never reached it: **59 of 60 story-carrying carousel bundles shipped as the hand-off box** (`_s45_r5_cardump.log` / `_s45_r5_carshape.py`, the 82 modules whose WT carries the tag).

**The fix:** `InteractiveBuilder.#carouselStoryShell`, dispatched in `#carousel` AFTER every strict dialect and the rich fallback (so every existing carousel build is byte-identical) and before the table-slide last resort. With no table and no merged type, the members from the opener on form the REFERENCE RUN: a tag whose first bracket matches `reference_pattern` (`embed … book|story`, not `audio`) is a story reference; after one, a line naming the story / set / source (`run_line_pattern`, ≤ 16 words — also when it parses as an instruction, BLL152's title line) and a black line of ≤ 4 words (the link, `(in Set 5)`, `……`) belong to it. It emits the r126 shell (the carousel's own open / close + `elements.embed_story_carousel`'s item and placeholder image) and a **Designer/Developer To Do** — "Build this carousel from the pages of the story ‘Zac hid from Dad’ (Set 5) — one slide per page (the human's form: images/<story title>/<story title>-01.jpg …); source: <the link>" (title from `title_pattern` — a quoted phrase right after story / book / text; set from `set_pattern`; NO link → the box is kept). The reference tags' own words (the writer's request) join the Writers Note after the widget. After the run a black line or a `[body]` renders after the shell (the r352 carousel members form — the dispatch's video test reads every member, so the generic members rule cannot place it), an instruction is skipped (already the Writers Note), anything else → null (the box keeps every member). Data `Emit_Templates.interactive_builders.carousel.story_shell`; env **`CARSTORY_OFF`**, byte-identical OFF.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed**; ON **76 pages / 33 modules** (BLL113 … BLL225 — the extra pages over the 43 built carousels are the hand-off boxes' running index shifting once earlier boxes build). **Built: 44 of the 60 story carousels (43 new)**, 38 with the story title and 39 with the set in the To Do. The 16 still boxed are MIXED bundles — the writer's `[Have the questions appear in an accordion drop down…]` merged a second widget type, which `#carousel` refuses at its top (WHY_UNBUILT reason 2, out of scope). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.
- **Coverage dashboard (refreshed, `_r488_dashboard_before.md` → `COVERAGE_DASHBOARD.md`): carousel built 679 → 722, Still a box 320 → 277 (−43), coverage 68.0 → 72.3 %; the `carousel · embed` cross-cutting blocker (59 declines / 1 build) is gone** — ≥ 20 sites converted = progress (§4 widget-build bullet).
- Adjunct `_verify_carousel.cjs` over the 33 modules: 8 mismatched video slide ids — **identical with CARSTORY_OFF** (BLL116 / BLL144 / BLL155's existing video carousels; the shells carry no video); selftest GREEN. Not a protected gate; recorded as a follow-up.

### 3. PROTECTED GATES

- Skeleton **55.3576 % → 55.3605 % @ 2491 (+0.0029pp)**, RAW 39.243 → **39.280 % (+0.037pp** — the built carousels match the gold's widget internals); ≥50 1584 / ≥75 277 / ≥90 26 EXACT; 9 movers, **6 up / 3 down NAMED** with the position-free companion (`_r488_companion.py`): BLL175_1_1 64.9 → 63.2 (overlap +1), BLL223_2_0 54.2 → 53.8 (+1), BLL145_1_1 59.9 → 59.7 (+5) — alignment; up BLL176 +3.3, BLL143 +2.7 …
- compare_structure exact 16702 / EXTRA 198 / missing 878 / row-wrap 24 EXACT; body 238 / clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every protected verifier RESULT line ✓; selftests 50 green / 0 fail; the miner 195 → 194 CANDIDATE.
- Plateau (§4): a widget-BUILD round (D10-3; judged on the widget's own verifier + the dashboard's Still-a-box count) — neither counts nor resets; **0 of 3**.

**Ledger:** scoped #6 since the r482 FULL · data `interactive_builders.carousel.story_shell` · env `CARSTORY_OFF` · code `InteractiveBuilder.#carouselStoryShell` · tools `_s45_r5_{pick,carshape}.py`, `_s45_r5_cardump{,_on}.log`, `_r488_companion.py`, `_r488_verify_carousel{,_off}.log`, `_r488_dashboard_before.md`, `_s45_{regen,postship}.sh`, `_r488_finalise.py` · session 45 Round 5.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 488 (260620.52): THE STORY-REFERENCE CAROUSEL SHELL (session 45 Round 5) — a carousel whose members are the writer's "
                "[embed book N] / [embed story] reference builds the r126 shell + a To Do (InteractiveBuilder.#carouselStoryShell). Env CARSTORY_OFF.\n"
                + '\tstatic AppVersion = "260620.52";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 488 BASELINE (the story-reference carousel shell, `CARSTORY_OFF`; "
                "SCOPED, scoped #6 since the r482 FULL; scoped_ship PASS; a widget-build round): SCAFFOLD mean 55.3605% / >=50% 1584 / >=75% 277 / "
                ">=90% 26 / RAW 39.280% @ 2491 pairs — +0.0029pp (6 up / 3 down NAMED); cs / body / clean / leak EXACT; carousel Still-a-box 320 -> "
                "277.** Previous: **ROUND 487 BASELINE")
so = so.replace(a11, "| `CARSTORY_OFF` | 488 | **THE STORY-REFERENCE CAROUSEL SHELL** (session 45 Round 5). Reverts "
                "`interactive_builders.carousel.story_shell`: a carousel bundle whose members are the writer's `[embed book N]` / `[embed story]` "
                "reference goes back to the hand-off box — 33 modules / 76 pages, 43 carousels; byte-identical to r487. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.52` (round 488 — **the story-reference carousel shell**; `CARSTORY_OFF`; scoped #6 since the r482 FULL; "
                "33 modules, 43 carousels built — Still-a-box 320 → 277; skeleton 55.3605 % @ 2491, +0.0029pp, RAW +0.037pp).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r488.bak")
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
setv("build", '"260620.51"', '"260620.52"'); setv("round", "487", "488")
insert_before("_note_r487", '    "_note_r488": "Round 488 (session 45 Round 5, 2026-09-25) — THE STORY-REFERENCE CAROUSEL SHELL (CARSTORY_OFF): 33 modules / 76 pages, '
              '43 carousels built (Still-a-box 320 -> 277); SCAFFOLD 55.3576 -> 55.3605 @ 2491 (+0.0029pp, 6 up / 3 down NAMED); RAW 39.243 -> 39.280; '
              'buckets / cs / body / clean / leak EXACT; scoped #6 since the r482 FULL; scoped_ship PASS. Adjunct _verify_carousel: 8 video-id '
              'mismatches identical OFF.",')
setv("raw_mean_pct", "39.24", "39.28")
insert_before("_note_r487_state", '    "_note_r488_state": "r488 (the story-reference carousel shell): SCAFFOLD 55.3605 @ 2491, RAW 39.280; 9 movers (6 up / 3 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r488-finalise.bak")
i = find("- **ROUND 488 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈07:25, session 45 Round 5 — r488 (the story-reference carousel shell) SHIPPED and committed; "
        "the in-flight marker is cleared). LAST SHIPPED **r488** (260620.52); **LAST FULL = r482 (the s44 backstop)**; ledger **scoped #6** (2 of "
        "headroom — a FULL backstop is due after two more scoped ships). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / "
        "`_r469b_declined.patch` (buttons, 10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈06:35, session 45 Round 2"); prior = L[k]; del L[k]
k = find("- Before it: **r486**"); r486 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r487**"); L[k] = L[k].replace("- LAST SHIPPED: **r487**", "- Before it: **r487**", 1)
L.insert(k, "- LAST SHIPPED: **r488** (build 260620.52, 25 Sept ≈07:25, session 45 Round 5 — THE STORY-REFERENCE CAROUSEL SHELL, `CARSTORY_OFF`; "
         "SCOPED, **scoped #6 since the r482 FULL backstop**, scoped_ship PASS; a widget-BUILD round — **carousel Still-a-box 320 → 277 (43 "
         "built)**; **skeleton 55.3576 → 55.3605 % @ 2491 (+0.0029pp, 6 up / 3 down NAMED)**, ≥50 1584, ≥75 277, ≥90 26, RAW 39.280 % (+0.037); "
         "cs / body / clean / leak EXACT; `gate_baseline.json` at r488; the miner 194 CANDIDATE).")
k = find("- Before them: **r485 → r467**")
L[k] = L[k].replace("- Before them: **r485 → r467** (260620.49 → 260620.34 — the title-bar language split,",
                    "- Before them: **r486 → r467** (260620.50 → 260620.34 — KB 01F the quote form, the title-bar language split,", 1)
k = find("- Plateau window (§4): **0 of 3** — r487")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r487", "- Plateau window (§4): **0 of 3** — r488 a widget-build round (neither); r487", 1)
k = find("- Standing facts: AppVersion **260620.51**")
L[k] = L[k].replace("AppVersion **260620.51** (r487 the unquoted named hover anchor — session 45 Round 2, 25 Sept); before it 260620.50",
                    "AppVersion **260620.52** (r488 the story-reference carousel shell — session 45 Round 5, 25 Sept); before it 260620.51 (r487 the "
                    "unquoted named hover anchor — session 45 Round 2); before it 260620.50", 1)
assert "260620.52" in L[k]
k = find("- **(s45-r2) the hover markers after r487")
L.insert(k, "- **(s45-r5) the carousel after r488:** (a) 16 story carousels still boxed are MIXED bundles — the writer's `[Have the questions appear "
         "in an accordion drop down …]` line merges an accordion / dropdown type into the carousel bundle, which `#carousel` refuses (WHY_UNBUILT "
         "reason 2 — the scanner's two-activities-in-one-basket class, 50 activities / 29 modules, its own round); (b) adjunct "
         "`_verify_carousel.cjs`: 8 built video slides whose YouTube id is not in the human's carousels (BLL116 ×3, BLL144 ×1, BLL155 ×4) — "
         "pre-existing, measure whether the gold swapped the videos (class C) or Claude took the wrong URLs; (c) the dashboard's next "
         "cross-cutting blockers: dragAndDrop / typing / multiChoiceQuiz / dropDown `(a captured TABLE)`, dragAndDrop / dropDown / mcq "
         "`button+txt`, clickDrop `video:yt` 37.")
k = find("## Round log")
L.insert(k + 1, "- s45-r5 (engine r488, build 260620.52, 25 Sept ≈06:25 → 07:25 real clock) · THE STORY-REFERENCE CAROUSEL SHELL (the hand-off-box "
         "lane; WHY_UNBUILT__carousel reason 1: `[carousel]` + `[embed book N]` + the story's title / set / PDF link → the r126 shell + a To Do "
         "naming the story, set and source; the discussion questions render after it) · SHIPPED scoped #6, scoped_ship PASS · 33 modules / 76 "
         "pages, **43 carousels built — Still-a-box 320 → 277** · skeleton +0.0029pp (6 up / 3 down NAMED), RAW +0.037pp · plateau 0 of 3 "
         "(neither — a widget-build round).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r488** (260620.52, "
        "the story-reference carousel shell); LAST FULL = **r482** (the s44 backstop); ledger scoped #6 (a FULL backstop due within two scoped "
        "ships); plateau **0 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along patches `_r469_declined.patch` (alerts) / "
        "`_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
k = find("## Session 45 — Round 5 PICK (engine r488)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 45 — Round 5 PICK (engine r488) — THE STORY-REFERENCE CAROUSEL SHELL — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 45 — Round 5 PICK (engine r488) + what shipped'; the one-line summary is the s45-r5 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r486 (verbatim, s45 r488)\n\n" + r486 + "\n"
    "\n## Session 45 — Round 5 PICK (engine r488) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r488, 260620.52):** `interactive_builders.carousel.story_shell` (env `CARSTORY_OFF`) — `InteractiveBuilder.#carouselStoryShell` "
    "after `#carouselRich`. Probe OFF 0 changed; ON 76 pages / 33 modules; 44 of 60 story carousels built (43 new; 16 mixed bundles still boxed); "
    "scoped_ship PASS; +0.0029pp, 6 up / 3 down NAMED; dashboard carousel Still-a-box 320 → 277.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
