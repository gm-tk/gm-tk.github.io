#!/usr/bin/env python3
"""r427 finalise (OPERATING_GUIDE §12) — written by SESSION 34 Round 1 (22 Sept 2026), which FINISHED the round the
session-33 Round 5 crash left at §3 step 7: changelog entry, Config.js 260619.99 -> 260620.00, OPERATING_GUIDE §9 / §11 / §14,
gate_baseline.json (round 427, values unchanged — the round is gate-neutral by design), LOOP_STATE.md (Round-log line, the
Position bullets — the IN-FLIGHT marker CLEARED — plateau, standing facts, the next-session line, the archive pointer),
LOOP_STATE_ARCHIVE.md (the PICK + what-shipped section), LOOP__Autonomous_Rounds.md §0 (the census-table build).
Exact-text edits only; every anchor asserted unique. Run under WSL: python3 _s33_r427_finalise.py
"""
import re, json
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
PF = R + "pageforge-site/converter-v2/"
def rd(p): return open(p, encoding="utf-8").read()
def wr(p, s): open(p, "w", encoding="utf-8", newline="\n").write(s)

entry = """## 2026-09-22 (round 427, build 260620.00) — THE CODE-PREFIX CHIP DELTAS: a family's lesson-chip FORM can turn on the TENS digit of the module code, so `Style_Anchor_Registry` gains a sixth, optional cascade tier `prefix_deltas` (longest matching code prefix wins, merged per key) — BLL14x / 15x / 16x take the DECIMAL chip (`1.0`) under the padded BLL1 level, BLL26x / 27x the PADDED chip (`01`) under the decimal BLL2 base; the autonomous loop's session 33 Round 5, CRASHED after its post-ship suite and FINISHED by session 34 Round 1; SCOPED regeneration of the 33, scoped ship #2 since the intake FULL

### 1. WHAT CHANGED

**The class (the diff miner's chrome facts F3 / F8 on the r426 queue; the intake handover's §7 item 2 — the lesson chip).** `EXTRA header:chip=decimal-number` 237 pages / 62 modules (CANDIDATE on the BLL subject group, c = 0.61, n = 16) with its mirror `MISSING header:chip=lesson-number` 202 / 43, and `EXTRA header:chip=lesson-number` 83 / 35 (era = Refresh c = 0.80) with its mirror `MISSING header:chip=decimal-number` 119 / 52. A Style-Anchor LEVEL is keyed by the hundreds digit of the module code (BLL1 = BLL110–177, BLL2 = BLL210–276), but the human developer's chip convention turns on the TENS digit inside those levels. Measured over every BLL gold lesson page (re-run by session 34 from the gold pages themselves — the crashed session's census was quoted only in the `_doc` strings): BLL11x / 12x / 13x padded 14 / 14 / 14 pages (the BLL1 level delta, `padded-number`); **BLL14x decimal 14 / 14 (7 / 7 modules), BLL15x decimal 10 vs padded 4 (5 / 6 — BLL153 is the padded one), BLL16x decimal 14 / 14 (7 / 7)**; BLL17x padded 10 vs decimal 6 (5 / 2 modules — stays padded); BLL21x–25x decimal 14 / 14 / 12 / 17 / 12 vs padded 0 / 0 / 0 / 6 / 4 (the BLL2 base, `decimal`; BLL240 / 253 / 255 the padded minority); **BLL26x padded 12 / 12 (6 / 6), BLL27x padded 12 / 12 (6 / 6)**. Authority: LOOP §1b level 2 — the family's own gold convention, each sub-series ≥ 0.83 uniform; no KB rule names the chip's number form (the KB-first check found none). Class C-free: a structure-free chrome TEXT difference, always derivable.

**The fix — DATA OVER CODE, one generic tier.** `ModuleResolver.Resolve` (+40 lines, after the level and template deltas): `prefix_deltas` is a SIXTH, optional cascade tier at a base or a level — `{"<code prefix>": {field: value}}` — the LONGEST prefix matching the upper-cased module code wins (base tier first, then level tier), `_`-keys skipped; unlike the other tiers an OBJECT-valued field is merged PER KEY, so a row may name only `module_code.lesson` and leave the overview form and the Inquiry parents' template-delta `overview: absent` standing (BLL140 / 150 / 160 keep their no-chip overview). Data flag `StyleRegistry._meta.code_prefix_deltas.enabled` (true), env toggle **`PREFIXDELTA_OFF`** (the level's value stands for every module). Rows: BLL1 level `prefix_deltas` BLL14 / BLL15 / BLL16 → `{module_code: {lesson: "decimal"}}`; BLL2 level `prefix_deltas` BLL26 / BLL27 → `{module_code: {lesson: "padded-number"}}`. The chip is TEXT inside the same `div#module-code > h1` — the skeleton ignores it, so the round is **gate-neutral by design** and its verifier is the miner's chrome facts.

**The crash.** Session 33 Round 5 (12:26 → 12:52) first measured the `[Tab N]` labelled-repeated-opener dialect it was titled for (`_s33_r5_labelled_openers.py`: 3 modules / 3 pages — BLL250, CEDR101, CEDR401 — under every floor; the wider "Inquiry gold is one page WITH crumbs, Claude's one page WITHOUT" set is 7 modules across BLL2 / CEDR / CEDT / CEDW, under the 10-module chrome floor and not one family) and set it aside, picked the chip class, implemented it, ran the probe, the scoped regeneration, `scoped_ship.sh`, `run_all_gates.sh`, the selftests, the feature index and the miner — then the Cowork session died on a server error before §3 step 7. The recovery note (b892ff1) read the tree as "steps 5–7 never run, the corpus still r426"; session 34 found the `_s33_r427_*` logs (12:31 → 12:52) and the regenerated pages (12:37 → 12:40, `BLL141_1_0.html` `<h1>1.0</h1>` = its gold) and finished the round from step 7 — nothing regenerated twice, nothing re-proven that the logs already proved.

### 2. PROOF

- `_s33_r427_probe_run.sh` (the r410 in-memory harness over all 545 Claude-dir modules, 4 shards): **OFF (`PREFIXDELTA_OFF=1`) = 2699 / 2699 identical, 0 changed** — the toggle-OFF corpus IS the r426 corpus byte-for-byte; **ON = exactly 67 pages in 33 modules changed** (BLL141–147, BLL151–157, BLL161–167, BLL261–266, BLL271–276 — every lesson page of the five sub-series, nothing outside them; 2632 identical).
- SCOPED regeneration (`_s33_r427_regen.sh`: the 33 + a fresh 12-module spot-check sample, seed 427, in 4 batches — 45 / 45 fresh): `scoped_ship.sh --affected _affected_r427.txt --toggle PREFIXDELTA_OFF --round 427` (`_s33_r427_scoped_ship.log`) — toggle-exists ✓, content-hash **0 truly stale** (33 affected regenerated; the 509 untouched byte-identical to the manifest, mtime ignored), containment **33 ⊆ 33** ✓, spot-check **12 / 12 byte-identical** ✓, the exact decomposition: skeleton 54.14 / 1531 / 254, cs 15372 / 195 / 790, body 262, clean 98.33, leak 75 / 45 — **every protected gate HELD exact**; `_fastloop_diff.py --commit` (the baseline PATCHED, the content manifest refreshed 12:44).
- `_s33_r427_postship.sh` (`_s33_r427_gates.log`): `run_all_gates.sh` rc 0 — skeleton state `_s33_r427_sk_final.json` **54.1406 % @ 2491 pairs → 54.1406 % (+0.0000pp; 0 movers up / 0 down, 0 outside the set; new-only 0 / gone 0)**, ≥50 1531, ≥75 254, ≥90 23, RAW 38.069 %; compare_structure 15372 / 195 / 790 / 23; body_compare 56 / 5 / 203 / 262; clean 2646 / 2691 = 98.33 %; leak 75 occ / 45 pages; tags 9557 / 9557; every verifier ✓ (entry parity, flipCard divergence 0, speechBubble 4 at baseline, pop-outs, MTK quiz shells, MathML, dragAndDrop, bingo); 49 selftest PASS / 0 FAIL; feature index GREEN (552 modules); the ledger: scoped #2 since the intake FULL (6 of headroom); `_gatecheck.py` refused on its mtime assertion (a scoped round — the content-hash proof above is the honest one).
- **The verifier — the miner's chrome facts, r426 queue → r427 queue (`DIFF_QUEUE.md` 12:21 → 12:52, both 196 CANDIDATE):** `EXTRA header:chip=decimal-number` **237 / 62 → 215 / 51** (CANDIDATE → BELOW CONSENSUS — the BLL subject group no longer reaches 0.60), `MISSING header:chip=decimal-number` **119 / 52 → 81 / 33**, `MISSING header:chip=lesson-number` **202 / 43 → 180 / 32**, `EXTRA header:chip=lesson-number` **83 / 35 → 45 / 16** — 60 gold-mismatched chip pages / 30 module-rows removed across the four facts, exactly the 19 + 12 sub-series golds (BLL153, the one padded BLL15x gold, now reads decimal — the recorded 1-of-20 cost of the sub-series rule; BLL155's gold has no lesson page, so its two changed pages are unpaired). The remaining chip rows (F7 MISSING decimal 81 / 33, NCEA1 c = 0.81 n = 10; F15 EXTRA lesson-number 45 / 16, Refresh c = 0.80) are other families and stay in the queue.

### 3. PROTECTED GATES (all HELD EXACT — `_s33_r427_gates.log`, `_s33_r427_scoped_ship.log`, `_s33_r427_skdelta.log`)

- **Skeleton (PRIMARY)**: SCAFFOLD **54.1406 % @ 2491 pairs** (+0.0000pp, 0 movers — gate-neutral by design); ≥50 **1531**, ≥75 **254**, ≥90 **23**, RAW **38.069 %**; skipped 0.
- **compare_structure** 15372 / 195 / 790 / 23 EXACT; **body_compare** 56 / 5 / 203 / 262 EXACT; **defect** clean 2646 / 2691 = 98.33 %, leak 75 / 45 EXACT; tags 9557 / 9557; every verifier EXACT.
- Plateau (§4): the PICK declared the round gate-neutral by design (chrome TEXT the skeleton ignores) — it neither counts toward the window nor resets it; the window stays 0 of 3.

"""
p = PF + "BUILD_CHANGELOG.md"; s = rd(p)
head, rest = s.split("\n", 1)
assert head.startswith("# BUILD CHANGELOG") and rest.lstrip("\n").startswith("## 2026-09-22 (round 426, build 260619.99)")
wr(p, head + "\n\n" + entry + rest.lstrip("\n"))

p = PF + "app/js/Config.js"; s = rd(p)
old = '\tstatic AppVersion = "260619.99";'; assert s.count(old) == 1
note = ("\t// ROUND 427 (260620.00): THE CODE-PREFIX CHIP DELTAS — Style_Anchor_Registry gains a sixth, optional cascade tier `prefix_deltas` "
        "({\"<code prefix>\": {field: value}}, longest matching prefix wins, object fields merged per key) resolved in ModuleResolver.Resolve after the "
        "level and template deltas; rows BLL14 / 15 / 16 -> the DECIMAL lesson chip (1.0) under the padded BLL1 level, BLL26 / 27 -> the PADDED chip (01) "
        "under the decimal BLL2 base (measured over every BLL gold lesson page: each sub-series >= 0.83 uniform). Data flag "
        "StyleRegistry._meta.code_prefix_deltas.enabled, env PREFIXDELTA_OFF. The loop's session 33 Round 5 (crashed after its post-ship suite) finished by "
        "session 34 Round 1: OFF probe 2699 / 2699 identical, ON = exactly 67 pages / 33 modules; scoped regeneration of the 33; gate-neutral by design "
        "(skeleton 54.1406 % @ 2491, 0 movers; every gate EXACT); the miner's four chip facts -60 pages / -30 module-rows.\n")
wr(p, s.replace(old, note + '\tstatic AppVersion = "260620.00";'))

p = PF + "OPERATING_GUIDE.md"; s = rd(p)
old9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 426 BASELINE ("; assert s.count(old9) == 1
new9 = ("| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 427 BASELINE (the code-prefix chip deltas — `prefix_deltas`, the sixth "
        "Style-Anchor cascade tier, BLL14 / 15 / 16 decimal + BLL26 / 27 padded; SCOPED regeneration of the 33, scoped ship #2 since the intake FULL; "
        "gate-neutral by design): SCAFFOLD mean 54.1406% / >=50% 1531 / >=75% 254 / >=90% 23 / RAW 38.069% @ 2491 pairs, pairs skipped 0 — 0 movers "
        "(the chip is text the skeleton ignores); cs 15372 / 195 / 790 / 23, body 56 / 5 / 203 / 262, clean 2646 / 2691 = 98.33 %, leak 75 / 45 — every "
        "gate EXACT to r426; the verifier is the miner's chrome facts (the four chip rows −60 pages / −30 module-rows).** Previous — ROUND 426 BASELINE (")
s = s.replace(old9, new9)
old11 = "| *(no toggle — the reversal is the committed pre-round registry, `outputs/_s33_r426_pre/`)* | 426 |"; assert s.count(old11) == 1
row11 = ("| `PREFIXDELTA_OFF` | 427 | **THE CODE-PREFIX CHIP DELTAS — a family's lesson-chip FORM turns on the TENS digit, so `Style_Anchor_Registry` "
         "gains a sixth, optional cascade tier `prefix_deltas`** (the autonomous loop's session 33 Round 5, crashed after its post-ship suite; finished by "
         "session 34 Round 1). `ModuleResolver.Resolve`: at a base or a level, `prefix_deltas: {\"<code prefix>\": {field: value}}` — the LONGEST prefix "
         "matching the module code wins (base tier, then level tier), overlaid AFTER the level and template deltas; an object-valued field is merged PER KEY, "
         "so a row names only `module_code.lesson` and the overview form / the Inquiry parents' `absent` delta stand. Rows: BLL1 level BLL14 / BLL15 / BLL16 "
         "→ `lesson: decimal` (the gold's `1.0` — 7 / 7, 5 / 6, 7 / 7 modules under a level whose delta says `padded-number`); BLL2 level BLL26 / BLL27 → "
         "`lesson: padded-number` (the gold's `01` — 6 / 6, 6 / 6 under a base that says `decimal`); BLL17x (5 / 2) and BLL24x / 25x (the padded minority) "
         "keep their level's form. Data flag `StyleRegistry._meta.code_prefix_deltas.enabled`. OFF probe 2699 / 2699 identical; ON = exactly 67 pages / 33 "
         "modules; gate-neutral by design (0 movers, every gate EXACT); the miner's chip facts F3 / F4 / F5 / F8 −60 pages / −30 module-rows. |\n")
s = s.replace(old11, row11 + old11)
old14 = "- **Build:** `260619.99` (round 426 — **THE SINGLE-PAGE INQUIRY PAGE MODEL"; assert s.count(old14) == 1
b14 = ("- **Build:** `260620.00` (round 427 — **THE CODE-PREFIX CHIP DELTAS** — `Style_Anchor_Registry` gains the sixth cascade tier `prefix_deltas` "
       "(`ModuleResolver.Resolve`, longest matching code prefix, per-key merge); rows BLL14 / 15 / 16 → the decimal lesson chip, BLL26 / 27 → the padded "
       "chip; data flag `_meta.code_prefix_deltas.enabled`, env `PREFIXDELTA_OFF`; the autonomous loop's session 33 Round 5, crashed after its post-ship "
       "suite and finished by session 34 Round 1; OFF probe 2699 / 2699 identical, ON = exactly 67 pages / 33 modules; **SCOPED regeneration of the 33 "
       "(scoped ship #2 since the intake FULL)**; **ROUND 427 BASELINE = the r426 numbers EXACT, gate-neutral by design: SCAFFOLD mean 54.1406% / >=50% "
       "1531 / >=75% 254 / >=90% 23 / RAW 38.069% @ 2491 pairs**, 0 movers; cs 15372 / 195 / 790 / 23, body 56 / 5 / 203 / 262, clean 2646 / 2691, leak "
       "75 / 45; every verifier EXACT; 49 selftest PASS; the miner 196 with its four chip facts −60 pages / −30 module-rows). Previous: ")
s = s.replace(old14, b14 + old14)
wr(p, s)

p = R + "CONVERTER_V2/reference/tests/gate_baseline.json"; s = rd(p)
def setv(key, old, new):
    global s
    pat = r'("%s":\s*)%s(?=[,\s}])' % (re.escape(key), re.escape(str(old)))
    s, n = re.subn(pat, lambda m: m.group(1) + str(new), s, count=1); assert n == 1, key
setv("build", '"260619.99"', '"260620.00"'); setv("round", 426, 427)
a = '    "_note_r426": "Round 426 (session 33 Round 4, 2026-09-22)'; assert s.count(a) == 1
s = s.replace(a, '    "_note_r427": "Round 427 (session 33 Round 5, 2026-09-22 — crashed after its post-ship suite; finished by session 34 Round 1): the code-prefix chip deltas — Style_Anchor_Registry gains the sixth cascade tier prefix_deltas (ModuleResolver.Resolve; longest matching code prefix, per-key merge), rows BLL14 / 15 / 16 -> the decimal lesson chip, BLL26 / 27 -> the padded chip; data flag _meta.code_prefix_deltas.enabled, env PREFIXDELTA_OFF. OFF probe 2699 / 2699 identical, ON = exactly 67 pages / 33 modules; SCOPED regeneration of the 33 (scoped #2 since the intake FULL). GATE-NEUTRAL BY DESIGN: every value in this file EXACT to r426 (0 skeleton movers; cs / body / defect / leak / verifiers identical); the verifier is the miner\'s chrome facts — the four chip rows 237 / 62, 119 / 52, 202 / 43, 83 / 35 -> 215 / 51, 81 / 33, 180 / 32, 45 / 16.",\n' + a)
a2 = '    "_note_r426": "Round 426: SCAFFOLD 54.1172 -> 54.1406'; assert s.count(a2) == 1
s = s.replace(a2, '    "_note_r427": "Round 427: SCAFFOLD 54.1406 -> 54.1406 @ 2491 pairs (+0.0000pp, 0 movers — the chip is text inside div#module-code > h1, which the skeleton ignores); >=50 1531 / >=75 254 / >=90 23 EXACT; RAW 38.069 EXACT. State outputs/_s33_r427_sk_final.json.",\n' + a2)
a3 = '    "_note_r426": "Round 426: exact 15131 -> 15372'; assert s.count(a3) == 1
s = s.replace(a3, '    "_note_r427": "Round 427: exact 15372 / EXTRA 195 / missing 790 / row-wrap 23 EXACT (the matched pool 17901 EXACT).",\n' + a3)
a4 = '    "_note_r426": "Round 426: over-capture 57 -> 56'; assert s.count(a4) == 1
s = s.replace(a4, '    "_note_r427": "Round 427: over-capture 56 / runaway 5 / EMPTY 203 / ANY 262 EXACT on 2691 pages.",\n' + a4)
a5 = '    "_note_r426": "Round 426: clean 2690 / 2736 -> 2646 / 2691'; assert s.count(a5) == 1
s = s.replace(a5, '    "_note_r427": "Round 427: clean 2646 / 2691 = 98.33, leak 75 occ / 45 pages EXACT.",\n' + a5)
json.loads(s); wr(p, s)

# LOOP__Autonomous_Rounds.md §0 — the census table's build (counts unchanged)
p = R + "LOOP__Autonomous_Rounds.md"; s = rd(p)
o = "Current (22 September 2026, build 260619.99 — after the 22 Sept Round 0d and r426: the 12 XOTP modules and the 38 pre-intake never-converted modules are IN; r426 folded 45 over-split pages into 8 single pages):"
assert s.count(o) == 1
s = s.replace(o, "Current (22 September 2026, build 260620.00 — after the 22 Sept Round 0d, r426 and r427: the 12 XOTP modules and the 38 pre-intake never-converted modules are IN; r426 folded 45 over-split pages into 8 single pages; r427 changed chip text only):")
wr(p, s)

# LOOP_STATE.md
st = rd(R + "LOOP_STATE.md")
o = "- s33-r4 (data r426, build 260619.99"; assert st.count(o) == 1
line = ("- s33-r5 / s34-r1 (engine r427, build 260620.00, 22 Sept ≈12:25 → 12:52 CRASHED after its post-ship suite; FINISHED by session 34 Round 1, 13:49 → ≈14:35) · "
        "THE CODE-PREFIX CHIP DELTAS — a family's lesson-chip FORM turns on the TENS digit: `Style_Anchor_Registry` gains the sixth cascade tier `prefix_deltas` "
        "(`ModuleResolver.Resolve`, longest matching prefix, per-key merge; `_meta.code_prefix_deltas.enabled`, `PREFIXDELTA_OFF`), rows BLL14 / 15 / 16 → decimal "
        "(7 / 7, 5 / 6, 7 / 7 golds), BLL26 / 27 → padded (6 / 6, 6 / 6) · OFF probe 2699 / 2699 identical · ON = exactly 67 pages / 33 modules · SCOPED regeneration "
        "of the 33 (scoped #2 since the intake FULL) · GATE-NEUTRAL BY DESIGN: skeleton 54.1406 % @ 2491, 0 movers, every gate EXACT · the verifier = the miner's "
        "four chip facts −60 pages / −30 module-rows (F3 CANDIDATE → below consensus) · the `[Tab N]` labelled-repeated-opener dialect measured first: 3 modules / "
        "3 pages, DECLINED under every floor · plateau window 0 of 3 (neither counts nor resets)\n")
st = st.replace(o, line + o)
o = "- Every shipped round r314–r425 is ONE line"; assert st.count(o) == 1
st = st.replace(o, "- Every shipped round r314–r427 is ONE line")
o = "`DIFF_QUEUE.md` 22 Sept 12:21 on the r426 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows"; assert st.count(o) == 1
st = st.replace(o, "`DIFF_QUEUE.md` 22 Sept 12:52 on the r427 corpus (2,491 pairs / 533 modules), 196 CANDIDATE rows")
# the IN-FLIGHT marker → cleared
lines = st.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("- **ROUND 427 IN FLIGHT — NOT MEASURED IN THIS FILE")]
assert len(idx) == 1
lines[idx[0]] = ("- **No round in flight** (22 Sept 2026 ≈14:35, session 34 Round 1: r427 FINISHED and committed — the two loose files over c254225 were its whole "
                 "implementation, every §3 step 5–6 proof was already on disk in `outputs/_s33_r427_*`, only step 7 was missing; the corpus on disk IS the r427 "
                 "state; the r427 record is in LOOP_STATE_ARCHIVE.md 'Session 33 — Round 5 (engine r427 …)'). The §3 step-1 rule stands: the next PICK raises "
                 "`ROUND <N> IN FLIGHT — NOT PROVEN` here BEFORE any code is edited.")
st = "\n".join(lines)
o = "- LAST SHIPPED: **r426** (build 260619.99, 22 Sept ≈12:45, session 33 Round 4 — "; assert st.count(o) == 1
st = st.replace(o, ("- LAST SHIPPED: **r427** (build 260620.00, 22 Sept 12:52 / finalised ≈14:35, session 33 Round 5 finished by session 34 Round 1 — the code-prefix chip "
                    "deltas, `prefix_deltas` + `PREFIXDELTA_OFF`; SCOPED regeneration of the 33, scoped #2 since the intake FULL; GATE-NEUTRAL BY DESIGN — **skeleton "
                    "54.1406 % @ 2491, ≥50 1531, ≥75 254, ≥90 23, RAW 38.069 %** EXACT to r426; cs 15372 / 195 / 790 / 23; body 56 / 5 / 203 / 262; clean 2646 / 2691 = "
                    "98.33 %; leak 75 / 45; `gate_baseline.json` at r427 (`_note_r427`, values unchanged); `outputs/_s33_r427_sk_final.json` the skeleton state; 54.141 / "
                    "91.2 = **59.4 % of achievable**; the miner re-run 22 Sept 12:52, 196 CANDIDATE (the four chip facts −60 pages); corpus 2699 pages / 545 dirs / 2491 "
                    "pairs). Before it **r426** (build 260619.99, 22 Sept ≈12:45, session 33 Round 4 — "))
o = "- Plateau window (§4): **0 of 3** — r426 predicted a skeleton move"; assert st.count(o) == 1
st = st.replace(o, "- Plateau window (§4): **0 of 3** — r427 is gate-neutral by design (chrome TEXT the skeleton ignores: neither counts nor resets); r426 predicted a skeleton move")
o = "- Standing facts: AppVersion 260619.99 (r426 the single-page Inquiry page-model rows, session 33 Round 4, 22 Sept); before it 260619.98"; assert st.count(o) == 1
st = st.replace(o, "- Standing facts: AppVersion 260620.00 (r427 the code-prefix chip deltas, session 33 Round 5 finished by session 34 Round 1, 22 Sept); before it 260619.99 (r426 the single-page Inquiry page-model rows, session 33 Round 4, 22 Sept); before it 260619.98")
o = "## Session 31 — Round 3 (engine r425, BUILT + SHIPPED INERT) and Session 33 — Round 1 (r425 FINISHED)"; assert st.count(o) == 1
st = st.replace(o, ("## Session 33 — Round 5 (engine r427, crashed after its post-ship suite) and Session 34 — Round 1 (r427 FINISHED at §3 step 7) — THE CODE-PREFIX CHIP DELTAS → "
                    "LOOP_STATE_ARCHIVE.md 'Session 33 — Round 5 (engine r427 …) + Session 34 — Round 1'; the one-line summary is the s33-r5 / s34-r1 Round-log line below.\n\n" + o))
# the next-session line
i = st.rfind("**Next session starts with:**"); assert i > 0
st = st[:i] + ("**Next session starts with:** the standing `/loop-start` (health check — the census is 552 gold / 545 Claude dirs / 2,699 Claude pages; the \"Amended:\" line; "
               "the §7 diff check; `git status` CLEAN at the session-34 commits). No round in flight (r427 finished by session 34 Round 1 — see the Position section). "
               "Then: the miner's 196-row queue on the r427 corpus under §3 / §4 (chrome first — the remaining chip facts F7 MISSING decimal 81 / 33 NCEA1 c = 0.81 and "
               "F15 EXTRA lesson-number 45 / 16 Refresh c = 0.80 are the next chip rows; then title / module-menu / crumbs / footer), the intake handover's §7 item 3 "
               "(#4177), the ghost-dir / recognition lane, and the §4 exhaustion test only with every lane tried. NEEDS CHRIS: the open lines of the \"Needs Chris\" section.\n")
wr(R + "LOOP_STATE.md", st)

# the archive: the PICK + what-shipped section
sec = """
## Session 33 — Round 5 (engine r427, build 260620.00, 22 Sept ≈12:25 → 12:52, CRASHED after its post-ship suite) + Session 34 — Round 1 (r427 FINISHED at §3 step 7, 22 Sept 13:49 → ≈14:35) — THE CODE-PREFIX CHIP DELTAS: `prefix_deltas`, the sixth Style-Anchor cascade tier

**PICK (the diff miner's chrome facts F3 / F8 on the r426 queue — `EXTRA header:chip=decimal-number` 237 pages / 62 modules, CANDIDATE on the BLL subject group c = 0.61 n = 16, and `EXTRA header:chip=lesson-number` 83 / 35, era = Refresh c = 0.80 — with their MISSING mirrors 119 / 52 and 202 / 43; the intake handover's §7 item 2; authority §1b level 2, the family's own gold convention).** A Style-Anchor LEVEL is keyed by the hundreds digit (BLL1 = BLL110–177 says `padded-number`; the BLL2 base says `decimal`) but the human's chip convention turns on the TENS digit. Measured over every BLL gold lesson page (`_doc` strings of the two files; re-run by session 34 from the gold pages): BLL11x / 12x / 13x padded 14 / 14 / 14; **BLL14x decimal 14 / 14 (7 / 7 modules), BLL15x decimal 10 vs padded 4 (5 / 6 — BLL153 padded), BLL16x decimal 14 / 14 (7 / 7)**; BLL17x padded 10 vs decimal 6 (5 / 2 — stays); BLL21x–25x decimal 14 / 14 / 12 / 17 / 12 vs padded 0 / 0 / 0 / 6 / 4 (BLL240 / 253 / 255 the padded minority — stays); **BLL26x padded 12 / 12 (6 / 6), BLL27x padded 12 / 12 (6 / 6)**. No KB rule names the chip's number form (the KB-first check). The class is chrome TEXT inside `div#module-code > h1` — the skeleton ignores it, so the PICK declared the round gate-neutral by design with the miner's chrome facts as its verifier. The crashed session was TITLED for the `[Tab N]` labelled-repeated-opener dialect (the r426 FOUND item) and measured it FIRST (`_s33_r5_labelled_openers.py`, 12:26): list ≥ 3, empty openers < 2, repeated-label openers ≥ 2 → **3 modules / 3 pages (BLL250, CEDR101, CEDR401)** — under every floor; the wider "Inquiry gold is one page WITH crumbs, Claude's one page WITHOUT" set is 7 modules (+ BLL260, CEDT208, CEDW201, CEDR203) across BLL2 / CEDR / CEDT / CEDW — under the 10-module chrome floor and not one family (no §1d exception 1) → DECLINED on measurement; the r100 empty-opener form covers 13 modules and already fires on all of them.

**WHAT SHIPPED.** `ModuleResolver.Resolve` (+40, after the level and template deltas): `prefix_deltas` at a base or a level — `{"<code prefix>": {field: value}}`, the LONGEST prefix matching the upper-cased code wins (base tier, then level tier; `_`-keys skipped), overlaid after the level AND template deltas; an object-valued field is merged PER KEY, so a row names only `module_code.lesson` and the overview form / the Inquiry parents' template-delta `absent` stand (BLL140 / 150 / 160 keep their no-chip overview). Data flag `StyleRegistry._meta.code_prefix_deltas.enabled` (true), env `PREFIXDELTA_OFF`. Rows (`_s33_r427_patch_sar.py`, the pre-round file in `_s33_r427_pre/`): BLL1 level `prefix_deltas` BLL14 / BLL15 / BLL16 → `{module_code: {lesson: "decimal"}}`; BLL2 level BLL26 / BLL27 → `{module_code: {lesson: "padded-number"}}`. `_s33_r427_probe_run.sh` (4 shards over all 545): **OFF 2699 / 2699 identical, 0 changed; ON exactly 67 pages / 33 modules** (BLL141–147 / 151–157 / 161–167 / 261–266 / 271–276). `_s33_r427_regen.sh` (the 33 + 12 spot-checks seed 427, 4 batches, 45 / 45 fresh, 12:37 → 12:40); `scoped_ship.sh --affected _affected_r427.txt --toggle PREFIXDELTA_OFF --round 427` PASS (content-hash 0 truly stale, containment 33 ⊆ 33, spot-check 12 / 12, decomposition every gate HELD exact; the ledger scoped #2 since the intake FULL); `_fastloop_diff.py --commit` 12:44. `_s33_r427_postship.sh`: `run_all_gates.sh` rc 0 — **skeleton 54.1406 % @ 2491 → 54.1406 % (0 movers, 0 outside the set)**, ≥50 1531 / ≥75 254 / ≥90 23, RAW 38.069; cs 15372 / 195 / 790 / 23; body 56 / 5 / 203 / 262; clean 2646 / 2691 = 98.33 %; leak 75 / 45; every verifier ✓; 49 selftest PASS / 0 FAIL; feature index GREEN; the miner 12:52 → 196 CANDIDATE with **the four chip facts 237 / 62 → 215 / 51 (F3 CANDIDATE → below consensus), 119 / 52 → 81 / 33, 202 / 43 → 180 / 32, 83 / 35 → 45 / 16 (−60 pages / −30 module-rows)**; BLL153 (the one padded BLL15x gold) now reads decimal — the recorded 1-of-20 cost; BLL155's gold has no lesson page (its 2 changed pages unpaired). **The crash:** the Cowork session died on a server error after the miner and before §3 step 7; the 13:26 recovery commit (b892ff1) wrote the IN-FLIGHT note but read the tree as "steps 5–7 never run, the corpus still r426" — session 34 found the `_s33_r427_*` logs (12:31 → 12:52) and the regenerated pages (12:37 → 12:40, `BLL141_1_0.html` `<h1>1.0</h1>` = its gold), re-censused the golds, and finished from step 7 without regenerating or re-proving anything: `_s33_r427_finalise.py` (the changelog entry, Config.js 260620.00, OPERATING_GUIDE §9 / §11 / §14, `gate_baseline.json` round 427 `_note_r427` with every value unchanged, LOOP §0's census-table build, this record), `_s33_r427_checksums.sh`, `_s33_r427_mirror.sh`, the commit. Plateau window 0 of 3 (gate-neutral: neither counts nor resets).
"""
ar = rd(R + "LOOP_STATE_ARCHIVE.md")
assert "## Session 33 — Round 5 (engine r427" not in ar
wr(R + "LOOP_STATE_ARCHIVE.md", ar.rstrip("\n") + "\n" + sec)
print("finalise OK")
