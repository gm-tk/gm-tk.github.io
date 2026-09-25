#!/usr/bin/env python3
"""ROUND 495 finalise (session 46 Round 5 — KB c5 the literal-tag leak: hint-slider face markers + black [Body text]). WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 495," not in sc[:4000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.57";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 494 BASELINE"; a11 = "| `CARBODYEND_OFF` | 494 |"; a14 = "- **Build:** `260620.57` (round 494"
for a in (a9, a11, a14): assert so.count(a) == 1, a
PK = os.path.join(ROOT, "KB_AMALGAMATION_STATUS.md"); sk = rd(PK)
k5 = "| 5 | Never render `[tags]` as visible text | pre-ledger | every module | **PARTIAL** — the literal-tag leak gate: 288 occurrences / 46 pages remain (round 313)"
assert sk.count(k5) == 1
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 495 IN FLIGHT — NOT PROVEN**", "- **No round in flight** (25 Sept 2026 ≈12:45, session 46 Round 4", "- LAST SHIPPED: **r494**",
          "- Before it: **r493**", "- Before them: **r492 → r467**", "- Plateau window (§4): **0 of 3** — r494", "- Standing facts: AppVersion **260620.57**",
          "## Round log", "**Next session starts with:**", "## Session 46 — Round 5 PICK (engine r495)", "- **(s46-r4) the gathering lane after r494"):
    find(p)

entry = """## 2026-09-25 (round 495, build 260620.58) — KB CONSTRAINT 5, THE LITERAL-TAG LEAK: a built hint slider no longer prints the writer's own face marker (`[Hintslider front]`, `[hint slider text 1]`) on its faces, and a black-typed `[Body text]` is stripped like `[body]` — the leak gate 75 → 52 occurrences

### 1. WHAT CHANGED

**The PICK pass first** (session 46 Round 5): the gathering lane's remaining sub-shapes after r494 — the widget's first member swallowed (59 bundles: half a data table, half the lead sentence typed on the opener line across six types) and the unclassified box (56: r378's look-ahead keeps AGH's prose between two informational tables) — are each diffuse; recorded. The KB lane: row 5 (constraint 5 — never render a `[tag]` as visible text; every module; level-1 authority) is PARTIAL with the protected literal-tag leak gate at **75 occurrences / 46 pages**.

**Measured** (`_s46_r5_leaks.py` — every leak the gate counts, through the gate's own `visible_text` + `LITERAL_TAG`): the writer's markers typed in BLACK or kept as text — **hint-slider face markers inside a BUILT slider** (GENO901_7_3 `[Hintslider front]` / `[Hintslider back]` on 16 faces; PWY1009_1_1_0 `[hint slider 1]` / `[hint slider text 1]` on 4): the table-form builder reads each cell through `#cellText`, which strips the red style but keeps the marker words, while the gold's faces are the bare text (GENO901_0_7, PWY1009_1_0); black `[Image …]` requests ≈ 20 (DTC1005 ×8 …); black `[H1]`–`[H5]` ≈ 20 (the gold h3 twice, p once where checked — mixed, recorded); **black `[Body text]` 3** (HIS1002-7.0, MXDI201-8.0, MXS1004-8.0 — the r73 black-leading-tag strip knows only `[body]`); others.

**The fix:** (a) `InteractiveBuilder.#hintSliderTable` removes a leading bracket matching `interactive_builders.hintSlider.face_marker_strip.pattern` (`[hint slider …]` with up to three of the words front / back / text / label / hint / answer / reveal or a number) from each face (env `HINTFACEMARK_OFF`); (b) `ListsAndRuns.renderBlackText` reads `body_region.black_leading_tag_strip_more.tags` (`body text`) beside the r73 list (env `BLACKBODYTEXT_OFF`; the r73 `BLACKTAGSTRIP_OFF` still reverts the whole strip).

### 2. PROOF

- In-memory A/B over all 545 modules: **OFF (both toggles) 0 pages changed**; ON **5 pages / 5 modules** (GENO901, PWY1009, ENFUN09, HIS1002, MXS1004). Regeneration + 12-module spot-check clean; **`scoped_ship.sh` PASS**.
- `_verify_hintslider.cjs` GENO901 / PWY1009 / ENFUN09 (`_r495_verify_hintslider.log`): GENO901 28 / 28 rows, **unmatched 8 → 0** (exact 19 → 26); PWY1009 2 / 2, **unmatched 2 → 0**; ENFUN09's one unmatched row pre-existing (its `[hintslider]` line sits in free text — not this mechanism).

### 3. PROTECTED GATES

- **literal-[tag] leak 75 → 52 occurrences, 46 → 42 pages**; **structurally clean 2587 → 2591 / 2633 (98.25 → 98.40 %)**; compare_structure exact 16744 → 16745; EXTRA 198 / missing 888 / row-wrap 24; body ANY 236; skeleton **55.4051 % @ 2491 EXACT** (0 movers — a face's words and a line's leading tag are skeleton-blind); tags 9557 / 9557; every verifier RESULT ✓; selftests 50 green / 0 fail; the miner 194 CANDIDATE.
- Plateau (§4): skeleton-blind by design (a KB-rule leak round): neither counts nor resets; **0 of 3**.

**Recorded, not built:** the other leak mechanisms — black `[Image …]` requests with a URL or a description (≈ 20; DTC1005 ×8, HIS1005 ×2, ENGI102 ×2, SSFUN05, HIS1001, TRR102 / 106, ENGS404, MUS1004 ×2, ENFUN09), black `[H1]`–`[H5]` at a line's head (≈ 20; the gold's form mixed — h3 twice, p once where checked; a heading promotion needs its own census), `[Activity …]`, `[Answer: A]`, `[Rollover definition]`, `[Clickdrop 1 Image]`, `[carousel]`, `[drag and drop …]` singles.

**Ledger:** scoped #5 since the r490 FULL · data `interactive_builders.hintSlider.face_marker_strip`, `body_region.black_leading_tag_strip_more` · env `HINTFACEMARK_OFF`, `BLACKBODYTEXT_OFF` · code `InteractiveBuilder.#hintSliderTable`, `ListsAndRuns.renderBlackText` · tools `_s46_r5_leaks.py`, `_r495_finalise.py` · session 46 Round 5.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 495 (260620.58): KB C5 THE LITERAL-TAG LEAK (session 46 Round 5) — a built hint slider strips the writer's own face "
                "marker from each face; a black [Body text] is stripped like [body]. Env HINTFACEMARK_OFF / BLACKBODYTEXT_OFF.\n" + '\tstatic AppVersion = "260620.58";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 495 BASELINE (KB c5 the literal-tag leak — hint-slider face "
                "markers + black [Body text], `HINTFACEMARK_OFF` / `BLACKBODYTEXT_OFF`; SCOPED, scoped #5 since the r490 FULL; scoped_ship PASS): "
                "SCAFFOLD mean 55.4051% / >=50% 1587 / >=75% 277 / >=90% 26 / RAW 39.375% @ 2491 pairs — EXACT (skeleton-blind); leak 75 -> 52 occ / "
                "46 -> 42 pages; clean 2587 -> 2591; cs exact 16745 (+1).** Previous: **ROUND 494 BASELINE")
so = so.replace(a11, "| `HINTFACEMARK_OFF` | 495 | **KB C5 — THE HINT-SLIDER FACE MARKER** (session 46 Round 5). Reverts "
                "`interactive_builders.hintSlider.face_marker_strip`: a built table-form hint slider prints the writer's own `[Hintslider front]` / "
                "`[hint slider text N]` marker on its faces again (GENO901, PWY1009 — 20 literal-tag leaks). |\n"
                "| `BLACKBODYTEXT_OFF` | 495 | **KB C5 — THE BLACK [Body text]** (session 46 Round 5). Reverts `body_region.black_leading_tag_strip_more`: "
                "a black-typed `[Body text]` at a line's head leaks again (HIS1002, MXS1004 — 3). Together with HINTFACEMARK_OFF byte-identical to r494. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.58` (round 495 — **KB c5 the literal-tag leak: hint-slider face markers + black [Body text]**; "
                "`HINTFACEMARK_OFF` / `BLACKBODYTEXT_OFF`; scoped #5 since the r490 FULL; 5 modules / 5 pages; leak 75 -> 52 occ; clean +4; skeleton "
                "EXACT).\n" + a14)
wr(PO, so); print("OG ok")
sk = sk.replace(k5, k5.replace("**PARTIAL** — the literal-tag leak gate: 288 occurrences / 46 pages remain (round 313)",
                "**PARTIAL** — the literal-tag leak gate: **52 occurrences / 42 pages** after round 495 (2026-09-25, session 46 Round 5: a built hint "
                "slider's own face markers stripped, a black `[Body text]` stripped — 75 → 52; `_s46_r5_leaks.py` lists every remaining one: black "
                "`[Image …]` requests ≈ 20, black `[H1]`–`[H5]` ≈ 20, singles); was 288 / 46 at round 313"))
wr(PK, sk); print("KB status ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r495.bak")
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
setv("build", '"260620.57"', '"260620.58"'); setv("round", "494", "495")
insert_before("_note_r494", '    "_note_r495": "Round 495 (session 46 Round 5, 2026-09-25) — KB C5 THE LITERAL-TAG LEAK (HINTFACEMARK_OFF / BLACKBODYTEXT_OFF): 5 '
              'modules / 5 pages; leak 75 -> 52 occ, 46 -> 42 pages; clean 2587 -> 2591; cs exact 16744 -> 16745; skeleton EXACT; scoped #5; '
              'scoped_ship PASS.",')
setv("exact_chain", "16744", "16745")
out = "\n".join(G); json.loads(out)
# the defect / leak fields: report what they hold now (updated only when present with the old value)
for key, old, new in (("literal_tag_leak_occ", "75", "52"), ("leak_occ", "75", "52"), ("leak_pages", "46", "42"), ("clean_pages", "2587", "2591"), ("clean_pct", "98.25", "98.4")):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": {old}'): G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); print("set", key)
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")

shutil.copyfile(S, S + ".pre-r495-finalise.bak")
i = find("- **ROUND 495 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (25 Sept 2026 ≈13:05, session 46 Round 5 — r495 (KB c5 the literal-tag leak) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r495** (260620.58); **LAST FULL = r490 (the s45 Round 10 backstop)**; ledger **scoped #5** "
        "(3 of headroom). Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **No round in flight** (25 Sept 2026 ≈12:45, session 46 Round 4"); prior = L[k]; del L[k]
k = find("- Before it: **r493**"); r493 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r494**"); L[k] = L[k].replace("- LAST SHIPPED: **r494**", "- Before it: **r494**", 1)
L.insert(k, "- LAST SHIPPED: **r495** (build 260620.58, 25 Sept ≈13:05, session 46 Round 5 — KB C5 THE LITERAL-TAG LEAK: hint-slider face markers "
         "+ black [Body text], `HINTFACEMARK_OFF` / `BLACKBODYTEXT_OFF`; SCOPED, **scoped #5 since the r490 FULL backstop**, scoped_ship PASS; "
         "**leak 75 → 52 occ / 46 → 42 pages**, **clean 2587 → 2591**; skeleton 55.4051 % @ 2491 EXACT; cs exact 16745 (+1); `gate_baseline.json` "
         "at r495; the miner 194 CANDIDATE).")
k = find("- Before them: **r492 → r467**")
L[k] = L[k].replace("- Before them: **r492 → r467** (260620.55 → 260620.34 — the accordion panel after a table,",
                    "- Before them: **r493 → r467** (260620.56 → 260620.34 — the BLL closing section, the accordion panel after a table,", 1)
assert "r493 → r467" in L[k]
k = find("- Plateau window (§4): **0 of 3** — r494")
L[k] = L[k].replace("- Plateau window (§4): **0 of 3** — r494", "- Plateau window (§4): **0 of 3** — r495 a KB-rule leak round, skeleton-blind "
                    "(neither); r494", 1)
k = find("- Standing facts: AppVersion **260620.57**")
L[k] = L[k].replace("AppVersion **260620.57** (r494 the carousel slide-table tail — session 46 Round 4, 25 Sept); before it 260620.56",
                    "AppVersion **260620.58** (r495 KB c5 the literal-tag leak — session 46 Round 5, 25 Sept); before it 260620.57 (r494 the carousel "
                    "slide-table tail — session 46 Round 4); before it 260620.56", 1)
assert "260620.58" in L[k]
k = find("## Round log")
L.insert(k + 1, "- s46-r5 (engine r495, build 260620.58, 25 Sept ≈12:40 → 13:05) · a PICK pass (the gathering residue — diffuse, recorded) then "
         "KB C5 THE LITERAL-TAG LEAK (`_s46_r5_leaks.py`: a built hint slider's own face markers, 20; a black `[Body text]`, 3) · SHIPPED scoped #5, "
         "scoped_ship PASS · 5 modules / pages · **leak 75 → 52 occ / 46 → 42 pages, clean +4**; hint-slider verifier GENO901 / PWY1009 unmatched "
         "10 → 0 · skeleton EXACT · plateau 0 of 3 (neither).")
k = find("- **(s46-r4) the gathering lane after r494")
L.insert(k + 1, "- **(s46-r5) the literal-tag leak after r495 (52 occ / 42 pages, `_s46_r5_leaks.py` lists each):** black `[Image …]` requests "
         "≈ 20 (DTC1005 ×8 `[Image or something similar – https://unsplash…]`, HIS1005 ×2 `[Image Link] URL`, ENGI102 ×2, SSFUN05, HIS1001, "
         "TRR102 / 106 `[Item N] [Image] …`, ENGS404, MUS1004 ×2, ENFUN09) — a black image request could take the red `[image]` path (asset "
         "request / URL image); black `[H1]`–`[H5]` at a line's head ≈ 20 (DAN1003 / DTC1005 `[H1]`, CBI1008 / ART1003 / MXFU302 `[H5]`, "
         "XGF9004 / AGH1006 / ANZH401 / CEDT104 `[H3]`, TRR116 / HIS1006 / MUS1004 `[H2]` — the gold h3 / h3 / p where checked; a promotion "
         "needs its census); singles.")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r495** (260620.58, KB c5 "
        "the literal-tag leak); LAST FULL = **r490** (the s45 backstop); ledger scoped #5; plateau **0 of 3**; 2,491 pairs; census 552 / 545 / "
        "2,679. Ride-along patches `_r469_declined.patch` / `_r469b_declined.patch` / `_r468_declined.patch`. Needs Chris #17–#19, #22, #23.")
k = find("## Session 46 — Round 5 PICK (engine r495)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 46 — Round 5 PICK (engine r495) — KB C5: THE LITERAL-TAG LEAK — SHIPPED; the PICK + what-shipped record is in "
         "LOOP_STATE_ARCHIVE.md 'Session 46 — Round 5 PICK (engine r495) + what shipped'; the one-line summary is the s46-r5 Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r493 + the r494 no-round line (verbatim, s46 r495)\n\n" + r493 + "\n" + prior + "\n"
    "\n## Session 46 — Round 5 PICK (engine r495) + what shipped\n\n" + marker + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r495, 260620.58):** `interactive_builders.hintSlider.face_marker_strip` (env `HINTFACEMARK_OFF`) + "
    "`body_region.black_leading_tag_strip_more` [`body text`] (env `BLACKBODYTEXT_OFF`). Probe OFF 0; ON 5 modules / pages; scoped_ship PASS; "
    "leak 75 → 52 occ, 46 → 42 pages; clean +4; skeleton EXACT.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
