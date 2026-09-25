#!/usr/bin/env python3
"""ROUND 494 finalise (session 46 Round 4 — the [body] after a carousel's slide table, CARBODYEND_OFF). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 494," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.56";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 493 BASELINE"; a11 = "| `DROPBOXEND_OFF` | 493 |"; a14 = "- **Build:** `260620.56` (round 493"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 494 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈12:10, session 46 Round 3", "- LAST SHIPPED: **r493**",
          "- Before it: **r492**", "- Before them: **r491 → r467**", "- Plateau window (§4): **0 of 3** — r493", "- Standing facts: AppVersion **260620.56**",
          "## Round log", "**Next session starts with:**", "## Session 46 — Round 4 PICK (engine r494)", "- **(s46-r3) the PICK pass residue:**"):
    find(p)

entry = """## 2026-09-25 (round 494, build 260620.56 → 260620.57) — THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE: a carousel whose slides are a table no longer swallows the writer's next section — the [body] after the slide table ends the capture, and a carousel that owns its activity box keeps that box open for it (38 modules; 26 carousels newly built)

### 1. WHAT CHANGED

**The find** (session 46 Round 4 — the gathering lane continued: text the gold keeps FREE that Claude ships inside a hand-off box). `_s46_r3_swallow.py` → `_s46_r3_swallow.json` (1,126 such blocks) → `_s46_r4_boxend.cjs` (the scanned member that carries each, and what the capture ran past): 448 bundles, the swallow starting at a `[body]` 154 / a black line 142 / a table 74 … diffuse by type, except ONE shape — **a carousel whose slides are a TABLE, then a `[body]`**. `_s46_r4_cartail.cjs` (every carousel bundle holding a table then a `[body]`) + `_s46_r4_cartail.py` (the gold's placement of that `[body]`): **72 bundles / 42 modules — outside the carousel 53 of 54** (free 39; inside an activity box 14), a slide caption once (XTAS102 4.0), absent 9, too short to place 9. And the split that decides the box: **when the carousel OWNS its activity box the gold keeps the text inside that box 10 / 10; when it owns none, the text is free 39 / 43.** The cause: `member_rule.body_terminates_after_table_exempt_types` lists the carousel — r352 kept an image-series carousel's trailing `[body]` as a slide caption (and split the HEADING half off as CARHEADEND) — but the break is only considered once the bundle HOLDS a table, and a carousel whose slides ARE a table carries its captions in the cells.

**The fix** (`InteractiveScanner` — the TABLE-DATA SECTION-BREAK exemption): for a type listed in `member_rule.body_after_slide_table_ends.types` (the carousel) the exemption is lifted, so the `[body]` after its table ends the capture like any other table-data widget's; with `owned_box_stays_open`, a carousel that owns its activity box sets the r378 `_postTableResume` hold, so the converter's owner close site keeps the box open and the prose renders INSIDE it after the widget (BLL127 2.0: the built carousel, then "Choose one of these foods to make…", then the box's Upload-to-dropbox button — the gold's order). A first cut without the hold put the owned-box prose free (BLL127 / BLL157 / AGH1009 dipped); the hold is what the gold does. Env `CARBODYEND_OFF`.

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF 0 pages changed** (the OFF render of the 38 modules is byte-identical to the saved r493 render); ON **38 modules** (+ later pages whose hand-off-box numbers drop where a carousel now builds). No text lost (`_s46_textloss.py`: the lost lines are hand-off-box chrome and the writer's asset descriptions a built carousel does not print). Regeneration + 12-module spot-check clean; `scoped_ship.sh` FAIL on compare_structure missing +9 only → **accepted NAMED** (`_r494_named.log`, `_s46_csdelta.py`: matched +51, exact +36 — every module only GAINS matches; the nine are new matches carrying one gold wrapper — ENGI301 4 (the gold's `alert.solid`), XTAS102 2, XTAS103 2, MXEO401 1).
- **Carousel Still-a-box 277 → 252** (748 built of 1,000; the widget coverage 45.6 → 46.0 %). `_verify_carousel.cjs` / `_verify_image_carousel.cjs` on the 38 modules: 140 → 166 carousels built, the 11 video-id mismatches and CHFUN05's 4 image-carousel defects identical OFF and ON (pre-existing — the s45-r5 follow-up).

### 3. PROTECTED GATES

- Skeleton **55.3885 % → 55.4051 % @ 2491 (+0.0167pp)**, RAW 39.342 → 39.375 %; **≥50 1586 → 1587 (+1)**, ≥75 277, ≥90 26; 39 movers, **22 up / 17 down NAMED** (`_r494_companion2.log`): up XMES201_0_0 +10.8, XDLS912_2_0 +9.2, FRNO901_1_0 +7.5 …; every dip but two has its position-free overlap or its RAW score RISE (ENGJ201_5_0 RAW 46.9 → 54.3; XMES202_2_0 RAW +3.0; XFUN02_3_0 overlap +9; XMES103_3_0 overlap +14 …) — alignment; the two without (ENFUN04_0_0 −0.4, ENGR201_4_0 −0.5) are class C — the freed sentence is in the gold's wordHighlighter row (ENFUN04) / not in the gold at all (ENGR201's "When you ask your reader a question like this…").
- **compare_structure exact 16708 → 16744 (+36)**, matched 19467 → 19518, **missing 879 → 888 NAMED** (new matches); EXTRA 198 / row-wrap 24 EXACT; **body_compare ANY 238 → 236 (−2)**; clean 2587 / 2633 / leak 75 / 46 EXACT; tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): +0.0167pp (< 0.02) but ≥50 +1 and cs exact +36 — protected gates moved: neither counts nor resets; **0 of 3**.

**Ledger:** scoped #4 since the r490 FULL · data `member_rule.body_after_slide_table_ends` · env `CARBODYEND_OFF` · code `InteractiveScanner` TABLE-DATA SECTION-BREAK exemption + the owned-box hold · tools `_s46_r3_swallow.{py,json}`, `_s46_r4_boxend.cjs`, `_s46_r4_cartail.{cjs,py}`, `_s46_textloss.py`, `_r494_companion.py`, `_r494_finalise.py` · session 46 Round 4.

"""
entry = entry.replace("build 260620.56 → 260620.57", "build 260620.57")
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 494 (260620.57): THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE (session 46 Round 4) — the carousel's exemption from the "
                "body-after-table section break is lifted; an activity-owned carousel keeps its box open for the prose. Env CARBODYEND_OFF.\n"
                + '\tstatic AppVersion = "260620.57";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 494 BASELINE (the [body] after a carousel's slide table, "
                "`CARBODYEND_OFF`; SCOPED, scoped #4 since the r490 FULL; cs missing +9 NAMED — new matches; carousel Still-a-box 277 -> 252): "
                "SCAFFOLD mean 55.4051% / >=50% 1587 / >=75% 277 / >=90% 26 / RAW 39.375% @ 2491 pairs — +0.0167pp (22 up / 17 down NAMED), >=50 +1; "
                "cs exact 16744 (+36), missing 888; body ANY 236 (−2); clean / leak EXACT.** Previous: **ROUND 493 BASELINE")
so = so.replace(a11, "| `CARBODYEND_OFF` | 494 | **THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE** (session 46 Round 4). Reverts "
                "`member_rule.body_after_slide_table_ends` (Interactive_Boundary_ChildTag_Bank.json): the carousel is exempt from the body-after-table "
                "section break again, so a table-slide carousel swallows the writer's next `[body]` (and the owned activity box closes with the "
                "widget) — 38 modules; 26 carousels return to the hand-off box; byte-identical to r493. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.57` (round 494 — **the [body] after a carousel's slide table**; `CARBODYEND_OFF`; scoped #4 since the "
                "r490 FULL; 38 modules; carousel Still-a-box 277 -> 252; skeleton 55.4051 % @ 2491, +0.0167pp, ≥50 +1; cs exact +36).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r494.bak")
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
setv("build", '"260620.56"', '"260620.57"'); setv("round", "493", "494")
insert_before("_note_r493", '    "_note_r494": "Round 494 (session 46 Round 4, 2026-09-25) — THE [BODY] AFTER A CAROUSEL\'S SLIDE TABLE (CARBODYEND_OFF): 38 modules; '
              'carousel Still-a-box 277 -> 252; SCAFFOLD 55.3885 -> 55.4051 @ 2491 (+0.0167pp, 22 up / 17 down NAMED); RAW 39.342 -> 39.375; >=50 '
              '1586 -> 1587; cs exact 16708 -> 16744, missing 879 -> 888 NAMED (new matches); body ANY 238 -> 236; clean / leak EXACT; scoped #4.",')
setv("mean_scaffold_pct", "55.39", "55.41"); setv("pages_ge_50", "1586", "1587"); setv("raw_mean_pct", "39.34", "39.38")
setv("exact_chain", "16708", "16744"); setv("claude_missing_container", "879", "888")
insert_before("_note_r493_state", '    "_note_r494_state": "r494 (the carousel slide-table tail): SCAFFOLD 55.4051 @ 2491, RAW 39.375; 39 movers (22 up / 17 down NAMED).",')
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")

shutil.copyfile(S, S + ".pre-r494-finalise.bak")
i = find("- **ROUND 494 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈12:45, session 46 Round 4 — r494 (the [body] after a carousel's slide table) SHIPPED and "
        "committed; the in-flight marker is cleared). LAST SHIPPED **r494** (260620.57); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger "
        "**scoped #4** (4 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, "
        "10 pages) / `_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈12:10, session 46 Round 3"); prior = L[k]; del L[k]
k = find("- Before it: **r492**"); r492 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r493**"); L[k] = L[k].replace("- LAST SHIPPED: **r493**", "- Before it: **r493**", 1)
L.insert(k, "- LAST SHIPPED: **r494** (build 260620.57, 25 Sept ≈12:45, session 46 Round 4 — THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE, "
         "`CARBODYEND_OFF`; SCOPED, **scoped #4 since the r490 FULL backstop**; **carousel Still-a-box 277 → 252**; **skeleton 55.3885 → "
         "55.4051 % @ 2491 (+0.0167pp, 22 up / 17 down NAMED)**, **≥50 1587 (+1)**, ≥75 277, ≥90 26, RAW 39.375 %; **cs exact 16744 (+36)**, "
         "missing 888 (+9 NAMED, new matches); **body ANY 236 (−2)**; clean / leak EXACT; `gate_baseline.json` at r494; the miner 194 CANDIDATE).")
k = find("- Before them: **r491 → r467**")
L[k] = L[k].replace("- Before them: **r491 → r467** (260620.54 → 260620.34 — the accordion marker-cell table,",
                    "- Before them: **r492 → r467** (260620.55 → 260620.34 — the accordion panel after a table, the accordion marker-cell table,", 1)
assert "r492 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r493")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r493", "- Plateau window (§4): **0 of 3** — r494 +0.0167pp but ≥50 +1 / cs exact "
                    "+36 (protected gates moved: neither); r493", 1)
k = find("- Standing facts: AppVersion **260620.56**")
L[k] = L[k].replace("AppVersion **260620.56** (r493 the BLL closing section — session 46 Round 3, 25 Sept); before it 260620.55",
                    "AppVersion **260620.57** (r494 the carousel slide-table tail — session 46 Round 4, 25 Sept); before it 260620.56 (r493 the BLL "
                    "closing section — session 46 Round 3); before it 260620.55", 1)
assert "260620.57" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r4 (engine r494, build 260620.57, 25 Sept ≈12:10 → 12:45) · THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE (the gathering "
         "lane: 72 table-slide carousels / 42 modules swallowed the next `[body]`; gold outside the carousel 53 / 54, inside the owned activity "
         "box 10 / 10) · SHIPPED scoped #4 · 38 modules, **carousel Still-a-box 277 → 252** · skeleton +0.0167pp (22 up / 17 down NAMED), ≥50 "
         "+1, cs exact +36, body ANY −2 · plateau 0 of 3 (neither).")
k = find("- **(s46-r3) the PICK pass residue:**")
L.insert(k + 1, "- **(s46-r4) the gathering lane after r494 (`_s46_r4_boxend.json`, 448 bundles that hold gold-free text):** no other single "
         "shape — the swallow starts at a `[body]` 154 / a black line 142 / a table 74 across every widget type (unclassified 56, accordion 44, "
         "clickDrop 39, flipCard 38 …); 59 are the widget's own first member (its lead-in, which the gold keeps free above the widget — a "
         "per-type 'lead above the box' rule would be the next measure); the other table-data types' own post-table `[body]` (`_s46_r4_cartail.cjs` "
         "with `CT_TYPE=<type>`) is the next sizing.")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r494** (260620.57, the "
        "carousel slide-table tail); LAST FULL = **r490** (the s45 backstop); ledger scoped #4; plateau **0 of 3**; 2,491 pairs; census 552 / 545 "
        "/ 2,679. Ride-along patches `_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
k = find("## Session 46 — Round 4 PICK (engine r494)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 4 PICK (engine r494) — THE [BODY] AFTER A CAROUSEL'S SLIDE TABLE — SHIPPED; the PICK + what-shipped record "
         "is in LOOP_STATE_ARCHIVE.md 'Session 46 — Round 4 PICK (engine r494) + what shipped'; the one-line summary is the s46-r4 Round-log line "
         "below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r492 + the r493 no-round line (verbatim, s46 r494)\n\n" + r492 + "\n" + prior + "\n"
    "\n## Session 46 — Round 4 PICK (engine r494) + what shipped\n\n" + marker + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r494, 260620.57):** `member_rule.body_after_slide_table_ends` {types [carousel], owned_box_stays_open} (env "
    "`CARBODYEND_OFF`). First cut (the exemption lifted only) put an owned box's prose free (BLL127 / BLL157 / AGH1009 dipped; the gold keeps "
    "it inside the box 10 / 10) → the r378 `_postTableResume` hold added. Probe OFF 0; ON 38 modules; carousel Still-a-box 277 → 252; "
    "+0.0167pp, ≥50 +1, cs exact +36, missing +9 NAMED (new matches), body ANY −2.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
