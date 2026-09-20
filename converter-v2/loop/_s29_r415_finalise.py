#!/usr/bin/env python3
"""r415 finalise (CLAUDE.md §12): changelog entry, Config.js bump, CLAUDE.md §9 / §11 / §14, gate_baseline.json. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-20 (round 415, build 260619.86) — THE OWNED HEADING-LED BUNDLE WITH NO TABLE: the empty writer-owned box takes its section (the autonomous loop's session 29 Round 6; SCOPED regeneration of the 22 affected modules — scoped ship #7 since the 19 Sept FULL, the FULL backstop is due at the next ship; every protected gate HELD-or-IMPROVED, the compare_structure exact −6 named as the relocation class)

### 1. WHAT CHANGED

**The class.** The r412 / r413 shape without the table: a writer-owned typed-widget invocation — a real `[Activity N]` opener, or the r92 embedded form whose invocation carries the id (`[Activity 1A] [Dropdown Quiz – Auto Check]`) — whose member walk ended at once on the writer's `[H3]`, with the quiz written as PARAGRAPHS after it (`[H3] Synonym strength` + `[body]` + the questions and options as lines, `[Correct answer]` marks, `[Hint]` spans — WJFUN307 / 210 / 211, ENGJ403, ENFUN03, ENGS404, TEFUN05, SCES201, HIS1002 2.0, MXFU302 3.0). r413 took the heading + prose only when a TABLE followed; without one the box shipped EMPTY (the `no content captured` flag) and the whole section free after it. Found through the empty-box census (`outputs/_s29_r6_emptybox.py` → `_s29_r6_emptybox.out`: Claude 96 EMPTY writer-owned boxes on 73 pages / 47 modules; the gold's same-numbered box holds text 39 / media 21 = **60 / 96 = 0.63**, no box with that number 36) and the r4 owned-walk census's no-table rows (`_s29_r6_notable_rows.tsv`: 47 owned bundles / 40 pages / 28 modules).

**Measured** (`_s29_r6_goldcheck.py` — the r3 gold check without its table filter — over all 125 heading-led no-table bundles → `_s29_r6_notablecheck.out`): the heading inside the gold's box 46 / 99 found = 0.46 overall, a TIE split by family (MiW 7 / 9, Technology 4 / 4, Science 3 / 4, dragAndDrop 5 / 7 IN; English 0 / 7, NCEA1 1 / 7, dropDown 6 / 13 out) — so the UNOWNED half (0.41) stays free and the OWNED half, whose box already exists, was decided by the gate's own scorer on the probe's ON pages (`_s29_r415_pagescore.py`): **34 paired pages, 24 up / 2 down / 8 same, +57.7 pp-sum** — MiW 8 / 0, NCEA1 4 / 0, Science 3 / 0, Mathematics 1 / 0, Technology 6 / 0 (7 same — the TEDC boxes whose section is a collapsed widget either way), ENFUN 1 / 2 (−1.5). NEW-FAMILY CHECK: without WJFUN 26 pages, 16 up / 2 down, +36.6 — the class holds outside the intake family.

**The fix (DATA OVER CODE).** `opener_rule.heading_table_owner.owned_bundles.no_table {enabled, env NOTABLEOWNED_OFF}`: in `InteractiveScanner.#headingTableOwner` the table look-ahead no longer returns on a non-table item — when it finds no table, an OWNED bundle (a real owner, or `activityId` set by the embedded form) takes the heading as its FIRST lead item and the member walk RESUMES right after it (`#swallowMembers` from the heading's successor — the standard capture with its own terminators: the next heading, an activity opener, a section marker; the r366 lead_free rule then frees the first paragraph). An unowned bundle without a table returns as before. OFF = the r414 output byte-for-byte.

### 2. PROOF

- `_s29_r415_probe_run.sh` (the r410 harness over all 494 Claude-dir modules): **OFF (`NOTABLEOWNED_OFF`) = disk 2555 / 2555**; **ON = 35 pages / 22 modules** (`_affected_r415.txt`).
- `_s29_r415_pagescore.py`: **24 up / 2 down / 8 same, SCAFFOLD pp-sum +57.7, RAW −3.8** (the captured section's nodes move inside the collapsed widget — the r176 net-positive class); the dips ENFUN03_0_0 −1.8, ENFUN01_0_0 −0.2 (the ENFUN family's boxes whose gold keeps the quiz free, named).
- `REGENERATE CORPUS` scoped by §0a: the 22 + the 12-module spot-check sample (`_s29_r415_regen.sh`, 4 batches rc 0); `scoped_ship.sh --affected _affected_r415.txt --toggle NOTABLEOWNED_OFF --no-regen --commit --round 415`: content-hash 0 truly stale, containment 22 ⊆ 22, spot-check 12 / 12 byte-identical; the exact decomposition gate proof FAILED on `compare_structure exact chain` −6 alone (14174 → 14168) = **the matched pool −13 (ENFUN01 −2, ENFUN03 −6, ENFUN04 −1, SCES201 −1, TEFUN02 −1, WJFUN210 −1, WJFUN306 −1 — every one inside the affected set, `_s29_r415_cs_decomp.log`): the captured section's text-matched elements moving into the widget subtree the comparator excludes — the r57 / r147 / r412 relocation class; EXTRA 186 EXACT, MISSING 690 → 683 IMPROVED** → committed with `_fastloop_diff.py $UNION --commit --accept-named "compare_structure exact chain"` (`_s29_r415_fastloop_commit.log`); the content manifest refreshed.
- `_s29_skdelta.py _s29_r414_sk_final.json _s29_r415_sk_final.json --affected _affected_r415.txt`: **26 movers, 24 up / 2 down, 0 outside the affected set**, 0 pages added / gone; MXFU302_3_0 +6.5, SCES201_1_0 +6.2, HIS1002_2_0 +5.2, WJFUN211_0_0 +5.0.
- Verifiers in the gate run: dragAndDrop 21 widgets / defect 0, flipCard divergence 0, speechBubble / modal / mtkquiz / math / menulabels ✓ — every RESULT identical to r414.

### 3. PROTECTED GATES (all HELD-or-IMPROVED — `_s29_r415_gates.log`, `_s29_r415_scoped_ship.log`, `_s29_r415_fastloop_commit.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **53.886 → 53.911 % (+0.0246pp)**; ≥50 **1412 → 1415**, ≥75 **238**, ≥90 **20** EXACT; RAW **37.997 → 37.996 %** (−0.002, the relocation class); 2349 pairs, skipped 0 (state `outputs/_s29_r415_sk_final.json`).
- **compare_structure** exact **14168** (−6 = the pool −13, named) / EXTRA **186** EXACT / MISSING **683** (−7 IMPROVED) / row-wrap **23**; **body_compare** 54 / **5** (runaway −1 IMPROVED) / 190 / **247** (ANY −1); **defect** clean 2504 / 2548 = 98.27 %, leak 73 / 44 EXACT.
- tags **9557 / 9557**; entry-parity PASS; index-sync 33 / 28; **16 selftests GREEN** (46 PASS / GREEN lines, 0 FAIL).
- Ship ledger: **scoped ship #7 since the 19 Sept FULL — the FULL backstop is due at the next ship (#8)**; fast-loop baseline + content manifest refreshed; feature index `--rehtml` / `--merge` / `--selftest` GREEN.
- DIFF MINER re-mined on the r415 corpus (`_diff_miner_s29_r415.log`): **181 → 181 CANDIDATE rows**.
- Plateau: **+0.0246pp with ≥50 +3 — above the 0.02 threshold; the window stays at 0 of 3** (r414 reset it).

### 4. RECORDED, NOT TAKEN (the Round 6 PICK's measurements — `LOOP_STATE.md`)

- The unowned heading-led no-table shape (78 bundles / 62 pages / 50 modules): the gold boxes it 0.41 — stays free.
- DIFF_QUEUE #3677 (gold `col-12` section column vs Claude `col-md-8 col-12`, 315 pages): the gold's single-column body row is `col-12 col-md-8` ≥ 0.78 for every content kind (`_s29_r6_colwidth.py`; tables 0.46 / 0.42 col-md-12 a tie, overview headings 0.61 / 0.37) — an alignment artefact.
- #587 / #606 (the box's `interactive` class, 247 + 114 pages): number-paired (`_s29_r6_intflag.py`) the flag tracks the widget Claude's box holds (dragAndDrop 0.88 / mcq 0.65 int; clickDrop / carousel / TKmodal plain); the 446 gold-interactive / Claude-plain boxes hold NO widget at all — a capture class, not a flag rule.
- The after-widget row break (`_s26_rowpair.py` re-run → `_s29_r6_rowpair.out`: WIDGET 0.63 on 129 pages; the raw-HTML instrument `_s29_r6_widgetflow.py`: 0.57 on 61 pages, speechBubble 0.60, the hand-off box 0.58) — a tie between the two instruments.
- The footer rows #441–#443 (MISSING next-lesson / home-nav on 97–100 pages) — page-COUNT artefacts (Claude's last page pairs with a gold page that is not the gold's last: AGH1004 7 pages vs the gold's 10); the 133 'gold menu / Claude no menu' lesson pages — the gold's menu is COMMENTED OUT (ART1002); CHI1003 / 1004 / 1005's ≤ 20 % pages are `Merge item N` lessons (the r300 zero class, the ceiling's population).

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-20 (round 414")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.85";'; assert s.count(old) == 1
note = ("\t// ROUND 415 (260619.86): THE OWNED HEADING-LED BUNDLE WITH NO TABLE — a writer-owned (or embedded-id) typed-widget box whose walk ended on the "
        "heading, with the quiz written as paragraphs after it, takes the heading as its lead and resumes the member walk right after it (the r412 / r413 rule "
        "completed for the no-table dialect; the gold's same-numbered box holds the section on 60 / 96 of Claude's empty writer-owned boxes). "
        "`heading_table_owner.owned_bundles.no_table`, env NOTABLEOWNED_OFF. The loop's session 29 Round 6: OFF = disk 2555 / 2555, ON 35 pages / 22 modules "
        "(24 up / 2 down, +57.7pp-sum); SCOPED regeneration of the 22 (scoped ship #7 since the 19 Sept FULL — the full backstop is due next); "
        "skeleton 53.886 → 53.911 % (+0.0246pp), ≥50 1412 → 1415; cs exact −6 = the pool −13 (the relocation class, named); miner 181 → 181.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.86";'))

p = PF + "CLAUDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 414 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 415 BASELINE (the owned heading-led bundle with no table takes its section — "
        "`heading_table_owner.owned_bundles.no_table`, env `NOTABLEOWNED_OFF`; 22 modules / 35 pages; SCOPED regeneration of the 22, the probe proving the other 472 "
        "byte-identical; scoped ship #7 since the 19 Sept full — the FULL backstop is due next): SCAFFOLD mean 53.911% / >=50% 1415 / >=75% 238 / >=90% 20 / RAW 37.996% "
        "@ 2349 pairs, pairs skipped 0 — hold-or-improve; 26 movers (24 up, 2 down — ENFUN03_0_0 −1.8, ENFUN01_0_0 −0.2; 0 outside the affected set); the 2323 "
        "unaffected pairs EXACT. compare_structure exact 14168 (−6 = the matched pool −13, the r57 / r147 relocation class, named) / EXTRA 186 EXACT / MISSING 683 "
        "(−7 IMPROVED) / row-wrap 23; body_compare 54 / 5 / 190 / 247 (runaway −1); defect clean 2504 / 2548 = 98.27%, leak 73 / 44 EXACT.** Previous — ROUND 414 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `NESTBOX_OFF` | 414 | **THE NESTED ACTIVITY BOX"; assert s.count(old11) == 1
row11 = ("| `NOTABLEOWNED_OFF` | 415 | **THE OWNED HEADING-LED BUNDLE WITH NO TABLE — the empty writer-owned box takes its section** (the autonomous loop's session 29 "
         "Round 6 — the r412 / r413 rule completed for the no-table dialect). A writer-owned typed-widget invocation (a real `[Activity N]` opener, or the r92 embedded "
         "form `[Activity 1A] [Dropdown Quiz – Auto Check]`) whose walk ended at once on the writer's `[H3]`, the quiz written as PARAGRAPHS after it — the box shipped "
         "EMPTY and the section free after it (WJFUN307 / 210 / 211, ENGJ403, ENFUN03, ENGS404, TEFUN05, SCES201). Measured: Claude 96 EMPTY writer-owned boxes on "
         "73 pages / 47 modules, the gold's same-numbered box holding text or media on 60 = 0.63 (`_s29_r6_emptybox.py`); the heading-led no-table shape's gold box "
         "0.46 overall — the unowned half 0.41 stays free, the owned half decided by the gate's own scorer (24 up / 2 down / 8 same, +57.7pp-sum; every group net up "
         "but ENFUN 1 / 2). Data `heading_table_owner.owned_bundles.no_table {enabled, env}`: when the table look-ahead finds none, an owned bundle takes the heading "
         "as its first lead item and the member walk resumes right after it (the standard capture; r366 frees the first paragraph). OFF = the r414 output byte-for-byte "
         "(2555 / 2555). ON = 35 pages / 22 modules. Recorded: the unowned no-table shape (0.41), the ENFUN family's free-quiz minority. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.85` (round 414 — **the nested activity box"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.86` (round 415 — **the owned heading-led bundle with no table takes its section: a writer-owned (or embedded-id) typed-widget box whose "
       "walk ended on the heading, the quiz written as paragraphs after it, takes the heading as its lead and resumes the member walk right after it** (the r412 / r413 "
       "rule completed for the no-table dialect; Claude 96 empty writer-owned boxes, the gold's same-numbered box holding the section on 60 = 0.63; "
       "`heading_table_owner.owned_bundles.no_table`, env `NOTABLEOWNED_OFF`); the autonomous loop's session 29 Round 6; the probe OFF = disk 2555 / 2555, ON 35 pages / "
       "22 modules (24 up / 2 down, +57.7pp-sum, 0 outside the set); **SCOPED regeneration of the 22 (scoped ship #7 since the 19 Sept FULL — the FULL backstop is due "
       "at the next ship)**; **ROUND 415 BASELINE: SCAFFOLD mean 53.911% / >=50% 1415 / >=75% 238 / >=90% 20 / RAW 37.996% @ 2349 pairs** (+0.0246pp; ≥50 +3); "
       "compare_structure 14168 (−6 = the pool −13, named) / 186 / 683 (−7) / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44; every verifier EXACT; "
       "16 selftests GREEN; the miner 181 → 181; plateau window 0 of 3). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.85"', '"260619.86"'); setv("round", 414, 415)
setv("mean_scaffold_pct", 53.89, 53.91); setv("median_scaffold_pct", 54.8, 54.9)
setv("pages_ge_50", 1412, 1415); setv("exact_chain", 14174, 14168); setv("claude_missing_container", 690, 683)
setv("any_breakdown", 248, 247); setv("runaway", 6, 5)
a = '    "_note_r414": "Round 414 (session 29 Round 5)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r415": "Round 415 (session 29 Round 6): the owned heading-led bundle with no table takes its section (heading_table_owner.owned_bundles.no_table, env NOTABLEOWNED_OFF; 22 modules / 35 pages; SCOPED regeneration of the 22; skeleton 53.8864 -> 53.9110, >=50 1412 -> 1415, RAW 37.997 -> 37.996; compare_structure exact 14174 -> 14168 = the matched pool -13 (the relocation class, named), missing 690 -> 683; body_compare runaway 6 -> 5).",\n' + a)
a2 = '    "_note_r413b": "Round 414: SCAFFOLD 53.8168'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r414b": "Round 415: SCAFFOLD 53.8864 -> 53.9110 (+0.0246pp; 26 movers 24 up / 2 down — MXFU302_3_0 +6.5, SCES201_1_0 +6.2, HIS1002_2_0 +5.2; dips ENFUN03_0_0 -1.8, ENFUN01_0_0 -0.2; 0 outside the 22-module affected set), 1415 / 238 / 20, RAW 37.996; 2349 pairs.",\n' + a2)
b2 = '    "_note_r410": "Round 410: exact 14091 -> 14175'; assert s.count(b2) == 1
s = s.replace(b2, '    "_note_r415": "Round 415: exact 14174 -> 14168 (-6) = the text-matched pool 16469 -> 16456 (-13: ENFUN01 -2, ENFUN03 -6, ENFUN04 -1, SCES201 -1, TEFUN02 -1, WJFUN210 -1, WJFUN306 -1 — the captured section moving inside the widget subtree the comparator excludes, the r57 / r147 relocation class); EXTRA 186 EXACT; missing 690 -> 683 IMPROVED. Accepted by name (_fastloop_diff.py --accept-named).",\n' + b2)
b3 = '    "_note_r410": "Round 410: over-capture 54 / runaway 6 / EMPTY 190 / ANY 248'; assert s.count(b3) == 1
s = s.replace(b3, '    "_note_r415": "Round 415: over-capture 54 / runaway 6 -> 5 / EMPTY 190 / ANY 248 -> 247 (IMPROVED — the owned no-table box now holds its section).",\n' + b3)
wr(p, s); json.load(open(p, encoding="utf-8"))
print("r415 finalise: changelog + Config.js 260619.86 + CLAUDE.md §9/§11/§14 + gate_baseline.json done")
