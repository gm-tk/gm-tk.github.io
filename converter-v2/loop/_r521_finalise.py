#!/usr/bin/env python3
"""ROUND 521 finalise (session 50 Round 15 — the new activity id ends the walk, ACTIDSPLIT_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 521, build 260620.82) — THE NEW ACTIVITY ID ENDS THE WALK: a widget bundle no longer absorbs a follower whose own bracket opens a DIFFERENT activity ('[Activity 3B – self marking type the answer]' inside Activity 3A's walk) — 15 modules, the MX family most; each activity gets its own box (the gold's form) and 11 more typing quizzes build; skeleton +0.0400pp

### 1. WHAT CHANGED

**The class** (`_s50_r15_actid.cjs`, from the s50 r519 / r520 follow-up "the MX merged pairs"): of the 1,570 bundles that absorbed a follower widget (`member_rule.same_activity_multi_widget` — a different-type follower stays in the bundle when the bundle belongs to a real `[Activity N]`), **58 bundles / 17 modules** absorbed one whose OWN bracket names a different activity id — the MX family types the id and the widget in one bracket (`[Activity 3A – self-marking drag and drop] … [Activity 3B – self marking type the answer]`), so the tag resolves to the widget and the scanner's absolute `[activity]` break never sees it (MX 44, BLL 4 — BLL120's `[Activity 5H] [Flip cards]` inside 5G, ARFUN 3, JPFUN / XMES 2 each). The gold keeps the two activities apart.

**The fix** (`InteractiveScanner` — the follower absorb; data `Interactive_Boundary_ChildTag_Bank.json` `_meta.member_rule.new_activity_id_terminates {{enabled, pattern}}`, env **`ACTIDSPLIT_OFF`**): when the bundle HAS an activity id and the follower's own text names a different one, the walk ends there; the follower opens its own bundle, and its activity id is read from the same bracket (as the first one's was). A bundle with no activity id (ARFUN04's clickDrop decks, WJFUN210) is unchanged.

### 2. PROOF

- In-memory probe over all 545 modules: `ACTIDSPLIT_OFF=1` → 0 pages changed; ON → **15 modules** (BLL120, BLL143, CHWHA, ENGR102, ENGR302, GENO901, JPFUN02, MXDB302, MXEO301, MXFL301, MXFL302, MXFU301, MXFU302, OSSC401, XMES102 — many pages per module only through the hand-off boxes' renumbered codes). `scoped_ship.sh … --round 521` PASS with one NAMED movement (below); containment 15 ⊆ 15; the 12-module spot-check byte-identical.
- body_compare on the 15: every changed page's biggest box shrinks and its mixed-type count falls (MXEO301_1_0 over-capture 0.26 → 0.05, MXFL301_2_0 0.15 → 0.01, MXFU301_9_0 0.15 → 0.03, XMES102_3_0 0.56 → 0.34, JPFUN02_0_0 multi-type 3 → 1 …).
- The freed followers build: `_verify_typing.cjs` over the 15 — 26 quizzes / 266 inputs, 240 answers the gold's own, DEFECTS 0; on the typing gate set the count GREW 14 → 25 quizzes, 145 → 232 inputs (MXEO301 5 → 10, MXFL301 2 → 6, MXFL302 3 → 5), recorded with `VERIFY_COUNT_RECORD=1`. Dashboard: typing built 19 → 34.

### 3. PROTECTED GATES

Skeleton **55.7489 → {MEAN} % @ 2486 (+0.0400pp; 28 pages up / 11 down — split per §1e)**, ≥50 1612 → 1616, ≥75 285 → 286, ≥90 26. The largest rise: MXFL301_2_0 +9.8pp, CHWHA_0_0 +9.7, MXFL302_2_0 +9.1, MXEO301_4_0 +8.1; the largest dip, **MXDB302_7_0 48.2 → 32.6 %, is difflib's alignment: its matched lines fall 72 → 50 while the position-free overlap RISES 93 → 96** — the split gives the page the gold's missing Activity 7F (6 → 7 of the gold's 8 activities, 7F between 7E and 7G as in the gold) and the longest-block alignment re-anchors (LOOP §3 step 6's companion test); the other ten dips are 0.3–2.2pp each, the new activity wrappers lengthening the page (e.g. MXFU301_6_0 matched 49 → 49, overlap 59 → 64; ENGR302_5_0 70 → 70, 77 → 81; MXFU302_10_0 −0.3pp — its 10A / 10B now apart, as in the gold's 10A–10D); RAW 39.594 → {RAW} %; cs exact 16769 → 16772, EXTRA 204 / missing 886 held; **body ANY 235 → 236 NAMED**: MXDB302_5_0 — Activity 5D ('[Activity 5D – self marking drag and drop]', typed entirely in red by the writer: the instruction, the question lines and the answers) now has its own box, whose member-character count reads 20 (< 40 = body_compare's 'empty'); before the split the same 20 characters sat inside 5C's box (386 + 20) — a correctly separated activity, not lost content (`--accept-named "body_compare ANY"`); clean 98.40 %, leak 52 / 42 EXACT; tags 9557; every verifier ✓, every COUNT held or recorded (`_r521_gates_rec.log`); aggregates written by `scoped_ship.sh … --commit --round 521`; `--gate-baseline-check` PASS. Plateau: **reset** (+0.0400pp).

**Ledger:** scoped #1 since the s50-r14 FULL (r520) · data `_meta.member_rule.new_activity_id_terminates` · env `ACTIDSPLIT_OFF` · code `InteractiveScanner` (the follower absorb) · `gate_baseline.json.typing` 25 / 232 · session 50 Round 15.
"""
F.finalise(
    N=521, old_build="260620.81", new_build="260620.82", entry=entry,
    config_comment="THE NEW ACTIVITY ID ENDS THE WALK (session 50 Round 15): a follower whose own bracket names a different "
                   "activity id opens its own bundle. Env ACTIDSPLIT_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 521 BASELINE (the new activity id ends the walk, "
        f"`ACTIDSPLIT_OFF`; SCOPED, scoped #1 since the s50-r14 FULL): SCAFFOLD mean {MEAN}% / >=50% 1616 / >=75% 286 / >=90% 26 / "
        f"RAW {RAW}% @ 2486 pairs (+0.0400pp, 28 up / 11 down); cs exact 16772; body ANY 236 NAMED (MXDB302_5_0).**",
    og11="| `ACTIDSPLIT_OFF` | 521 | **THE NEW ACTIVITY ID ENDS THE WALK** (session 50 Round 15). Reverts "
         "`member_rule.new_activity_id_terminates`: a follower whose own bracket names a different activity id is absorbed into the "
         "bundle again (the MX merged pairs — 15 modules — back to one mixed box; the r520 output exactly). |",
    og14=f"- **Build:** `260620.82` (round 521 — **the new activity id ends the walk**; `ACTIDSPLIT_OFF`; scoped #1 since the s50-r14 "
         f"FULL; 15 modules; skeleton {MEAN} % (+0.0400pp), RAW {RAW} %; body ANY 236 NAMED; typing 25 / 232).",
    gb_note=f"Round 521 (session 50 Round 15, 2026-09-26) — THE NEW ACTIVITY ID ENDS THE WALK (ACTIDSPLIT_OFF): 15 modules; skeleton "
            f"55.7489 -> {MEAN} (+0.0400pp), >=50 1616, >=75 286; cs exact 16772; body ANY 236 NAMED (MXDB302_5_0 the all-red 5D box "
            f"reads 20 chars); typing 25 / 232 recorded; scoped #1.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 15 — r521 (the new activity id ends the walk) SHIPPED and "
             "committed; the in-flight marker is cleared). LAST SHIPPED **r521** (260620.82); **LAST FULL = r520 (the session-50 Round 14 "
             "backstop)**; ledger **scoped #1** (7 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / "
             "9 modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` "
             "(the lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / `_r489_accbullet_declined.patch` (the accordion "
             "bulleted bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN "
             "tile's \"Year N\" lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides "
             "only after the TRR table-dialect ownership fix). Checked at r521: none rides (no patch has all its pages inside the 15).",
    last_shipped=f"- LAST SHIPPED: **r521** (build 260620.82, 26 Sept {T}, session 50 Round 15 — THE NEW ACTIVITY ID ENDS THE WALK, "
                 "`ACTIDSPLIT_OFF`; SCOPED, **scoped #1 since the s50-r14 FULL**; 15 modules; skeleton 55.7489 → "
                 f"{MEAN} % (+0.0400pp), ≥50 1616, ≥75 286, RAW {RAW} %, cs exact 16772; body ANY 236 NAMED; typing 25 / 232 recorded).",
    before_them_add="the drag-and-drop FIB form",
    plateau="- Plateau window (§4): **0 of 3** — r521 +0.0400pp (a real gain: reset); s50-r14 the FULL backstop, change-free (neither); ",
    standing="- Standing facts: AppVersion **260620.82** (r521 the new activity id ends the walk — session 50 Round 15, 26 Sept); before it "
             "260620.81 (",
    roundlog=f"- s50-r15 (engine r521, build 260620.82, 26 Sept ≈06:05 → {T}) · a PICK pass on the recorded MX merged-pairs follow-up "
             "(`_s50_r15_actid.cjs`: 58 bundles / 17 modules absorb a follower naming another activity id) then THE NEW ACTIVITY ID ENDS "
             "THE WALK · SHIPPED scoped #1 · 15 modules · skeleton +0.0400pp, ≥50 +4, ≥75 +1, cs exact +3, body ANY +1 NAMED (MXDB302_5_0) "
             "· typing 14 → 25 quizzes recorded · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r521, 260620.82):** `InteractiveScanner` follower absorb + `member_rule.new_activity_id_terminates` "
                  "(ACTIDSPLIT_OFF). Probe OFF 0; ON 15 modules; +0.0400pp; body ANY +1 NAMED; typing 25 / 232 recorded.",
)
