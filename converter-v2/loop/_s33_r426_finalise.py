#!/usr/bin/env python3
"""r426 finalise (OPERATING_GUIDE §12): changelog entry, Config.js 260619.98 -> .99, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json,
LOOP_STATE.md (round log, Position, next-session line), the archive record. Run under WSL."""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 426, build 260619.99) — THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight golds the 22 Sept intake found over-split: `Style_Anchor_Registry` rows only (BLL2's x0 parents BLL250 / 260 / 270 as `page_model_exceptions`; `page_model: single-file` on CEDO4, CEDK4 (+ CEDK401), TWHT9 (+ TWHT903); NEW levels CEDR1 / CEDR4) — the autonomous loop's session 33 Round 4; SCOPED regeneration of the 8, scoped ship #1 since the intake FULL

### 1. WHAT CHANGED

**The class (the intake handover's §7 item 1).** Eight Inquiry golds are ONE page (an in-page crumb nav + inquiry panels) that Claude split into lesson pages at the 22 Sept intake — BLL250 8 pages / BLL260 13 / BLL270 5 / CEDK401 12 / CEDO402 6 / TWHT903 5 / CEDR101 2 / CEDR401 2 — because their codes were in no Style-Anchor level's members or `page_model_exceptions`: never converted, so the r408 miner never listed them. Authority: the family's own rule (LOOP §1b level 2 — the previously-developed sibling): every x0 parent of BLL1 / BLL2 is single-file (BLL110–170, BLL210 / 220 / 230: 10 / 10 gold), CEDK1 / CEDO2 / CEDR2 / CEDR3 / CEDT1 / CEDT2 / CEDT4 / TWHK9 are single-file, and each of the eight golds is itself one page (level 3). DATA ONLY, no engine change, no env toggle — the reversal is the committed pre-round registry (`outputs/_s33_r426_pre/Style_Anchor_Registry.json`, the r336 precedent); `_s33_r426_patch_sar.py` is the verbatim edit: BLL2 `page_model_exceptions` += BLL250 / BLL260 / BLL270; CEDO4 `page_model: single-file`; CEDK4 members += CEDK401, `page_model: single-file`; TWHT9 members += TWHT903, `page_model: single-file`; two NEW levels CEDR1 {CEDR101, 1-3, single-file} and CEDR4 {CEDR401, 9-10, single-file} — without them the resolver's "nearest level" rule fell to the HIGHEST level (CEDR5, multi-file), which is why CEDR101 / 401 split. CEDR203 (1 Claude page vs 11 gold) is the reverse case and NOT this round: its gold's ten named sub-pages are case-study tile pages (`[Insert image for front of tile]` / `[Body for modal or back of tile]` in the WT) — a CED tile-page dialect, recorded (10 pages / 1 module, under the floor).

**What the single page does and does not fix.** All eight now build exactly the gold's one page (the pairing is honest: the split pages' content was unpaired before). BLL270 takes the full inquiry shell (`div.crumbs` + 5 `inquiryPanel`s, `body.inquiry`) and jumps 5.2 → **49.9 %** — its WT has EMPTY `[Tab N]` panel openers, the r100 form. The other seven build one plain page WITHOUT the shell: their writers REPEAT the label on every panel opener (`[Tab 2] Silent b` … after the `[Tab 1] Introduction … [Tab 6] ough` crumb list — BLL250 lines 75–91; with the writer's own numbering slips, `[Tab 3] eigh` for the list's Tab 4), so `_emptyOpeners` is 0 and `_bllInquiry` never fires. That is a fourth `[Tab N]` authoring dialect ("labelled repeated openers"), the next round — measured corpus-wide first (it may also explain the low-scoring gated singles CEDT104 7 %, TWHK901 9 %, TWHA901 19 %).

### 2. PROOF

- `_s33_r426_probe_run.sh ON` (the r410 harness over all 545 Claude-dir modules; the disk IS the pre-round-registry state, byte-identical to the intake manifest): **2691 identical / 8 changed — exactly the eight** (one page each), every other module untouched; `_r426_note` keys inside the level deltas are skipped by `#overlayRules` like every other `_`-key (no page elsewhere moved).
- SCOPED regeneration (`_s33_r426_regen.sh`: the 8 + a fresh 12-module spot-check sample, seed 426): `_content_manifest.py fresh` **0 truly stale**; `_scoped_spotcheck.py verify` **12 / 12**; `scoped_ship.sh` toggle-exists ✓ (`TMPLDELTA_OFF` named for the check — the registry round's real reversal is the pre-round file), containment **8 ⊆ 8** ✓, spot-check ✓; the exact decomposition (`_s33_r426_fastloop_named.log`): skeleton 54.12 → 54.14 IMPROVED, ≥50 / ≥75 HELD, cs exact **+241**, body ANY **−3**, clean +0.01, leak pages −1; **cs EXTRA +1 / missing +17 ACCEPTED AS NAMED** — the text-matched pool grew 17624 → 17901 (+277: the single pages match the gold's whole content where the split pages' content was unpaired) and 241 of the 277 newly matched elements are exact; the +1 / +17 are the composition of NEW matches, not a worsening of any previously matched element (`_intake_split.py`-style reasoning: the 534 untouched modules' rows are byte-identical).
- `run_all_gates.sh` (`_s33_r426_gates.log`): skeleton state `_s33_r426_sk_final.json` **54.1172 → 54.1406 % @ 2491 pairs (+0.0234pp)**, ≥50 1531, ≥75 254, ≥90 23, RAW 38.069; per module (the gate's own pairs, one each): BLL250 4.9 → 6.7, BLL260 3.2 → 7.3, **BLL270 5.2 → 49.9**, CEDK401 5.7 → 10.1, CEDR101 9.8 → 11.0, CEDR401 8.3 → 9.7, TWHT903 5.4 → 12.6, **CEDO402 18.2 → 11.8 (−6.5) NAMED**: its old page 0 was a short overview whose menu region matched the gold's menu; the single page now holds all six former pages' content without the inquiry shell (the labelled-opener dialect above), so the gold's panel structure is unmatched over a longer skeleton — 7 up / 1 down, +58.3pp-sum; `_s29_skdelta.py` reads the seven renamed pairs as 7 new-only / 7 gone and CEDO402 as the one mover (0 movers outside the eight); compare_structure 15372 / 195 / 790 / 23; body_compare 56 / 5 / 203 / 262 (pages 2736 → 2691 — the 45 unpaired split pages are gone); clean 2646 / 2691 = 98.33 %; leak 75 / 45; tags 9557 / 9557; every verifier ✓; 17 selftests GREEN (49 / 0); feature index GREEN; the miner 190 → **196 CANDIDATE** (the single pages now expose their whole content to the miner — the inquiry-shell rows #438 / #4098 and the BLL module-menu rows strengthen; they are the next round's class).

### 3. PROTECTED GATES (all HELD or IMPROVED, the two cs rows NAMED — `_s33_r426_gates.log`, `_s33_r426_fastloop_named.log`, `_s33_r426_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.1406 % @ 2491 pairs** (+0.0234pp; 7 up / 1 down, the dip named); ≥50 **1531**, ≥75 **254**, ≥90 **23**, RAW **38.069 %**; skipped 0.
- **compare_structure** 15372 / 195 / 790 / 23 (exact +241; EXTRA +1 / missing +17 named — the +277 matched pool); **body_compare** 56 / 5 / 203 / 262 (−1 / 0 / −3 / −3, all on the eight); **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK predicted a skeleton move; +0.0234pp ≥ 0.02 — the window resets to 0 of 3.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (FULL CORPUS REGENERATION + INTAKE RE-BASELINE")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.98";'; assert s.count(old) == 1
note = ("\t// ROUND 426 (260619.99): THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight golds the 22 Sept intake found over-split — Style_Anchor_Registry rows only "
        "(BLL2 page_model_exceptions += BLL250 / 260 / 270; page_model single-file on CEDO4, CEDK4 (+CEDK401), TWHT9 (+TWHT903); NEW levels CEDR1 / CEDR4 — without "
        "them the resolver fell to CEDR5, multi-file). No engine change, no env toggle: the reversal is the committed pre-round registry (outputs/_s33_r426_pre). "
        "The loop's session 33 Round 4: ON probe = exactly the 8; scoped regeneration of the 8; skeleton 54.1172 -> 54.1406 % @ 2491 (7 up / 1 down, +58.3pp-sum; "
        "BLL270 5.2 -> 49.9 takes the inquiry shell; CEDO402 -6.5 named); cs exact +241 (the matched pool +277, EXTRA +1 / missing +17 named); body ANY -3. "
        "The other seven build one page without the inquiry shell — their writers repeat the label on every [Tab N] opener (no empty openers): the next round.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260619.99";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **INTAKE 2026-09-22 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 426 BASELINE (the single-page Inquiry page model for the eight over-split golds — "
        "Style_Anchor_Registry rows only; SCOPED regeneration of the 8, scoped ship #1 since the intake FULL): SCAFFOLD mean 54.1406% / >=50% 1531 / >=75% 254 / "
        ">=90% 23 / RAW 38.069% @ 2491 pairs, pairs skipped 0 — 7 up / 1 down on the eight alone, +58.3pp-sum (BLL270 5.2 → 49.9; CEDO402 −6.5 named), 0 movers "
        "elsewhere; cs 15372 / 195 / 790 / 23 (exact +241; EXTRA +1 / missing +17 named — the matched pool +277), body 56 / 5 / 203 / 262, clean 2646 / 2691 = "
        "98.33 %, leak 75 / 45.** Previous — INTAKE 2026-09-22 BASELINE (")
s = s.replace(old9, new9)
old11 = "| `SIDETABNAV_OFF` | 422 (enabled 2026-09-22) |"; assert s.count(old11) == 1
row11 = ("| *(no toggle — the reversal is the committed pre-round registry, `outputs/_s33_r426_pre/`)* | 426 | **THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight "
         "golds the 22 Sept intake found over-split** (the autonomous loop's session 33 Round 4; `Style_Anchor_Registry.json` rows only — the r336 precedent). "
         "BLL2 `page_model_exceptions` += BLL250 / BLL260 / BLL270 (the x0 parents, 10 / 10 of the family's x0 golds are one page); `page_model: single-file` on "
         "CEDO4 (CEDO402), CEDK4 (+ CEDK401 as a member), TWHT9 (+ TWHT903); NEW levels CEDR1 {CEDR101} and CEDR4 {CEDR401} (the resolver's nearest-level rule "
         "had fallen to CEDR5, multi-file). ON probe = exactly the 8 (2691 / 2691 elsewhere); scoped regeneration of the 8; skeleton +0.0234pp (7 up / 1 down; "
         "BLL270 takes the inquiry shell at 49.9 %, the other seven build one plain page — their writers REPEAT the label on every `[Tab N]` opener, so the r100 "
         "inquiry mode's empty-opener test never fires: the next round's class). CEDR203 (1 vs 11 gold pages) recorded: a CED case-study tile-page dialect. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.98` (**FULL CORPUS REGENERATION + INTAKE RE-BASELINE, 22 Sept 2026"; assert s.count(old14) == 1
b14 = ("- **Build:** `260619.99` (round 426 — **THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight over-split golds** — `Style_Anchor_Registry` rows only "
       "(BLL2 exceptions + BLL250 / 260 / 270; single-file on CEDO4 / CEDK4 / TWHT9; NEW CEDR1 / CEDR4), no engine change; the autonomous loop's session 33 "
       "Round 4; ON probe = exactly the 8; **SCOPED regeneration of the 8 (scoped ship #1 since the intake FULL)**; **ROUND 426 BASELINE: SCAFFOLD mean 54.1406% / "
       ">=50% 1531 / >=75% 254 / >=90% 23 / RAW 38.069% @ 2491 pairs** — 7 up / 1 down, +58.3pp-sum (BLL270 5.2 → 49.9; CEDO402 −6.5 named), 0 movers elsewhere; "
       "cs 15372 / 195 / 790 / 23 (exact +241, the matched pool +277), body 56 / 5 / 203 / 262, clean 2646 / 2691, leak 75 / 45; every verifier EXACT; 17 selftests "
       "GREEN; the miner 196). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.98"', '"260619.99"'); setv("round", '"intake-2026-09-22"', 426)
setv("claude_pages", 2795, 2750)
setv("mean_scaffold_pct", 54.12, 54.14); setv("raw_mean_pct", 38.05, 38.07)
setv("exact_chain", 15131, 15372); setv("claude_extra_container", 194, 195); setv("claude_missing_container", 773, 790)
setv("any_breakdown", 265, 262); setv("over_capture", 57, 56); setv("empty_container", 206, 203)
setv("clean_pages", 2690, 2646); setv("total_pages", 2736, 2691); setv("clean_pct", 98.32, 98.33)
a = '    "_note_intake_2026_09_22": "INTAKE 2026-09-22 (session 33 Round 3'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r426": "Round 426 (session 33 Round 4, 2026-09-22): the single-page Inquiry page model for the eight over-split golds — Style_Anchor_Registry rows only (BLL2 page_model_exceptions += BLL250 / 260 / 270; page_model single-file on CEDO4, CEDK4 (+CEDK401), TWHT9 (+TWHT903); NEW levels CEDR1 / CEDR4), no engine change; SCOPED regeneration of the 8, ON probe = exactly the 8. Skeleton 54.1172 -> 54.1406 @ 2491 (7 up / 1 down, +58.3pp-sum; CEDO402 -6.5 named — one plain page without the inquiry shell); cs exact 15131 -> 15372 (+241) with EXTRA +1 / missing +17 named (the matched pool 17624 -> 17901: the single pages match the gold\'s whole content); body ANY 265 -> 262; Claude pages 2795 -> 2750 (the 45 unpaired split pages gone), clean 2646 / 2691.",\n' + a)
a2 = '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: SCAFFOLD 54.2466'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r426": "Round 426: SCAFFOLD 54.1172 -> 54.1406 @ 2491 pairs (+0.0234pp; BLL270 5.2 -> 49.9, TWHT903 5.4 -> 12.6, CEDK401 5.7 -> 10.1, BLL260 3.2 -> 7.3, BLL250 4.9 -> 6.7, CEDR101 9.8 -> 11.0, CEDR401 8.3 -> 9.7, CEDO402 18.2 -> 11.8 named); >=50 1531 / >=75 254 / >=90 23 EXACT; RAW 38.049 -> 38.069. State outputs/_s33_r426_sk_final.json.",\n' + a2)
a3 = '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: exact 14318 -> 15131'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r426": "Round 426: exact 15131 -> 15372 (+241), EXTRA 194 -> 195 (+1), missing 773 -> 790 (+17) = the text-matched pool 17624 -> 17901 (+277) on the eight single pages alone (their split pages\' content was unpaired before); 241 of the 277 new matches exact — NAMED, not a worsening of any previously matched element; row-wrap 23 EXACT.",\n' + a3)
a4 = '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: over-capture 55 -> 57'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r426": "Round 426: over-capture 57 -> 56, EMPTY 206 -> 203, ANY 265 -> 262 — the eight modules\' split pages (45 unpaired pages, 2736 -> 2691) folded into one page each; runaway 5 EXACT.",\n' + a4)
a5 = '    "_note_intake_2026_09_22": "INTAKE 2026-09-22: clean 2532 / 2576'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r426": "Round 426: clean 2690 / 2736 -> 2646 / 2691 = 98.33 (the 45 split pages gone), leak 75 occ / 46 -> 45 pages (BLL260\'s two leak pages fold into its one page).",\n' + a5)
json.loads(s); wr(p, s)

st = rd(R + "LOOP_STATE.md"); ar = rd(R + "LOOP_STATE_ARCHIVE.md")
o = "- s33-r3 (ROUND 0d · intake 2026-09-22"
assert st.count(o) == 1
line = ("- s33-r4 (data r426, build 260619.99, 22 Sept ≈12:25 → ≈12:45) · THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight over-split golds — `Style_Anchor_Registry` "
        "rows only (BLL2 exceptions += BLL250 / 260 / 270; single-file on CEDO4 / CEDK4 / TWHT9; NEW levels CEDR1 / CEDR4 — the resolver had fallen to CEDR5), "
        "no engine change, reversal = the pre-round registry (`_s33_r426_pre/`) · ON probe = exactly the 8 · SCOPED regeneration of the 8 (scoped #1 since the "
        "intake FULL) · skeleton 54.1172 → 54.1406 % @ 2491 (+0.0234pp; 7 up / 1 down, +58.3pp-sum; BLL270 5.2 → 49.9 takes the inquiry shell; CEDO402 −6.5 named) "
        "· cs exact +241 (matched pool +277; EXTRA +1 / missing +17 named) · body ANY −3 · clean 2646 / 2691 · every verifier ✓ · miner 196 · FOUND: the other seven "
        "build one page WITHOUT the inquiry shell — their writers repeat the label on every `[Tab N]` opener (no empty openers, `_bllInquiry` never fires) = the next "
        "round's class; CEDR203 (1 vs 11 gold pages) = a CED case-study tile-page dialect, recorded · plateau window 0 of 3\n")
st = st.replace(o, line + o)
o = "- LAST FULL: **ROUND 0d — the 22 Sept 2026 intake of the 38 pre-intake never-converted modules**"
assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r426** (build 260619.99, 22 Sept ≈12:45, session 33 Round 4 — the single-page Inquiry page model, registry rows only; SCOPED regeneration of "
                    "the 8, scoped #1 since the intake FULL; **skeleton 54.1406 % @ 2491, ≥50 1531, ≥75 254, ≥90 23, RAW 38.069 %**; cs 15372 / 195 / 790 / 23; body 56 / 5 / 203 / 262; "
                    "clean 2646 / 2691 = 98.33 %; leak 75 / 45; `gate_baseline.json` at r426; `outputs/_s33_r426_sk_final.json` the skeleton state; 54.141 / 91.2 = **59.4 % of "
                    "achievable**; the miner re-run 22 Sept 12:21, 196 CANDIDATE; corpus 2750 pages / 545 dirs / 2491 pairs). "
                    "LAST FULL: **ROUND 0d — the 22 Sept 2026 intake of the 38 pre-intake never-converted modules**"))
o = "- Plateau window (§4): **1 of 3** — the 22 Sept Round 0d is a population round (does not count); r422e predicted"
assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r426 predicted a skeleton move and delivered +0.0234pp (the window resets); the 22 Sept Round 0d is a population round (does not count); r422e predicted")
o = "- Standing facts: AppVersion 260619.98 (r422 ENABLED"
assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260619.99 (r426 the single-page Inquiry page-model rows, session 33 Round 4, 22 Sept); before it 260619.98 (r422 ENABLED")
o = "`DIFF_QUEUE.md` 22 Sept 11:51 on the intake-2026-09-22 corpus (2,491 pairs / 533 modules), 190 CANDIDATE rows"
assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 12:21 on the r426 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows")
m = re.search(r"^\*\*Next session starts with:\*\* .*$", st, re.M); assert m
nxt = ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,750 Claude pages; the \"Amended:\" line; "
       "the §7 diff check; `git status` CLEAN at the session-33 commits). No round in flight (r425 finished, r422 enabled, the 38 intaken, r426 the page-model rows — "
       "all 22 Sept). Next: **the labelled-repeated-opener `[Tab N]` dialect** — the seven single-page Inquiry modules that build one page WITHOUT the inquiry shell "
       "(BLL250 / 260, CEDK401, CEDO402, CEDR101 / 401, TWHT903: the writer repeats the crumb label on every panel opener, so `_emptyOpeners` = 0 and `_bllInquiry` "
       "never fires — ContentConverter ≈ line 1138); measure it corpus-wide first (every WT with a labelled `[Tab N]` list and no empty openers, incl. the low gated "
       "singles CEDT104 / TWHK901 / TWHA901), then the intake handover's §7 items 2–3 (the lesson chip; #4177) and the miner's 196-row queue under §3 / §4. NEEDS CHRIS: "
       "the open lines of the \"Needs Chris\" section.")
st = st[:m.start()] + nxt + st[m.end():]
record = """## Session 33 — Round 4 (data r426, build 260619.99, 22 Sept ≈12:25 → ≈12:45) — THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight over-split golds (registry rows only)

**PICK (the 22 Sept intake handover's §7 item 1; authority §1b level 2 — the family's own x0 rule 10 / 10, and level 3 — each gold is one page).** BLL250 / BLL260 / BLL270, CEDK401, CEDO402, TWHT903, CEDR101, CEDR401 split into 8 / 13 / 5 / 12 / 6 / 5 / 2 / 2 lesson pages against ONE gold page each: their codes were in no Style-Anchor level's members / `page_model_exceptions` (never converted, never mined), and CEDR101 / 401 fell through the resolver's nearest-level rule to CEDR5 (multi-file) because no CEDR1 / CEDR4 level existed.

**WHAT SHIPPED.** `_s33_r426_patch_sar.py` (exact text edits, the pre-round file snapshotted to `_s33_r426_pre/`): BLL2 `page_model_exceptions` += BLL250 / 260 / 270; CEDO4 `page_model: single-file`; CEDK4 += CEDK401, single-file; TWHT9 += TWHT903, single-file; NEW levels CEDR1 {CEDR101, 1-3} / CEDR4 {CEDR401, 9-10}, single-file. `_s33_r426_probe_run.sh ON` over all 545: exactly the 8 changed (one page each), 2691 / 2691 elsewhere. `_s33_r426_regen.sh` (the 8 + 12 spot-checks, seed 426): 0 stale, 12 / 12; `scoped_ship.sh` containment 8 ⊆ 8; `_fastloop_diff.py … --accept-named "compare_structure EXTRA container,compare_structure missing container" --commit` — the matched pool 17624 → 17901 (+277, the single pages match the gold's whole content), 241 exact, the +1 / +17 the composition of new matches. `run_all_gates.sh`: skeleton **54.1172 → 54.1406 % @ 2491 (+0.0234pp)**, ≥50 1531 / ≥75 254 / ≥90 23 EXACT; per module BLL250 4.9 → 6.7, BLL260 3.2 → 7.3, **BLL270 5.2 → 49.9** (its WT has empty `[Tab N]` openers — the r100 form fires, crumbs + 5 panels = the gold), CEDK401 5.7 → 10.1, CEDR101 9.8 → 11.0, CEDR401 8.3 → 9.7, TWHT903 5.4 → 12.6, **CEDO402 18.2 → 11.8 NAMED** (its old page 0 was a short overview whose menu matched; the single page holds everything without the inquiry shell); cs 15372 / 195 / 790 / 23; body 56 / 5 / 203 / 262 (pages 2736 → 2691, the 45 unpaired split pages gone); clean 2646 / 2691; leak 75 / 45; every verifier ✓; 17 selftests GREEN; feature index GREEN; miner 196 CANDIDATE. `_gatecheck.py` refused on its mtime assertion (scoped round). Finalise: the changelog entry, Config.js 260619.99, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` (`_note_r426`), the mirror.

**FOUND (the next round).** Seven of the eight build the single page WITHOUT the inquiry shell: their writers REPEAT the crumb label on every `[Tab N]` panel opener (BLL250 lines 75–91: `[Tab 1] Introduction … [Tab 6] ough` then `[Tab 2] Silent b` again, with numbering slips `[Tab 3] eigh` for the list's Tab 4), so `_emptyOpeners` = 0 and `_bllInquiry` (ContentConverter ≈ 1138–1168) never fires — a fourth `[Tab N]` authoring dialect ("labelled repeated openers"), to be measured corpus-wide (it may also be the shape behind the low gated singles CEDT104 7 %, TWHK901 9 %, TWHA901 19 %). CEDR203 (1 Claude page vs 11 gold) is a CED case-study tile-page dialect (`[Insert image for front of tile]` / `[Body for modal or back of tile]`), 10 pages / 1 module, recorded under the floor. Tooling: `_s33_r426_postship.sh` passed `_affected_r422.txt` to `_s29_skdelta.py` by a sed slip — its "1 mover outside the set" line is that, the numbers are right.
"""
ar = ar.rstrip("\n") + "\n\n" + record + "\n"
wr(R + "LOOP_STATE.md", st); wr(R + "LOOP_STATE_ARCHIVE.md", ar)
print("FINALISE_R426_DONE", len(st))
