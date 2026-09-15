#!/usr/bin/env python3
"""ROUND 329 — finalise: changelog, AppVersion (260618.99 → 260619.00 rollover), CLAUDE.md §9/§11/§14, gate_baseline.json,
LOOP_STATE.md (what shipped + position + round log + THE PLATEAU STOP banner + 'Next session starts with'). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.492", "50.496", "34.831", "34.832"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 329, build 260619.00) — `[trigger engagement]` IS A MARKER, NOT A BUTTON (KB constraint 43 / 05B / 01F — the dropbox-trigger signal; the autonomous loop, session 4, Round 4; **SCOPED regeneration of the 42 affected modules; skeleton +0.004pp, every other gate EXACT; scoped ship #3 since the round-326 full — and THE LOOP STOPS HERE on the plateau rule: r327 0.000pp, r328 0.000pp, r329 +0.004pp**)

### 1. WHAT CHANGED, IN ONE LINE

**The writer's `[trigger engagement]` / `[engagement trigger]` no longer ships a phantom `<div class="button engagementTrigger">Go to your journal</div>`: the KB reads the tag as the dropbox-trigger condition on the activity (constraint 43: "any activity that ends in a dropbox submission button … / `[trigger engagement]` carries the `dropbox` modifier"), the finished modules carry no engagement element at all (0 of 2,385 gold pages), and the engine already treated the same marker as content-less in two other seams (r292, r322). A label-less marker now emits nothing; a bracket carrying other words surfaces them as one red flag. 60 pages / 42 modules changed; the phantom buttons 99 → 28 (the residue = compound brackets the narrow rule does not claim).**

### 2. THE EVIDENCE (docx → human → Claude)

- **BLL240 lesson 1 (seven sub-pages)** — docx: `[Button] Upload to dropbox [trigger engagement]` → gold: `<a href="" target="_blank"><div class="button">Upload to dropbox</div></a>` and the activity closes → Claude before: the upload anchor + `<div class="button engagementTrigger">Go to your journal</div>`; after: the upload anchor only.
- **ENGI401 lessons 6 / 8** — docx: `[Button] Upload to dropbox. [Trigger Engagement]` → gold: the dropbox anchor only → Claude after: the same.
- **The KB:** constraint 43 and `05B_COMP14_LAYOUT_STRUCTURE` ("whose writer source carries `[trigger engagement]`") read the tag as the activity's dropbox-trigger condition; `01D` / `01F` list `engagement quiz button` → `engagement_quiz_button` = "External quiz link button" — the real `[engagement quiz button]` (23 modules), whose aliases never included the trigger forms. **The gold:** no `engag…` class or attribute anywhere in 2,385 pages.

### 3. THE MEASUREMENT (all 454 Writers Templates; every Claude page)

- WT bracket forms: `[trigger engagement]` 183, `[dropbox to trigger engagement]` 25, `[engagement trigger]` 21, `[dev – quiz to trigger engagement …]` 18, `[to trigger engagement]` 8, `[insert mtk quiz – trigger engagement]` 8, MTK-quiz compounds 9, `[insert text box for student response – engagement trigger]` 3 — 275 occurrences / 71 modules. Claude shipped **99 phantom `button engagementTrigger` elements on 88 pages / 70 modules** (Standard 74 / Inquiry 10 / Fundamentals 4 pages): 84 with the `journal_label_default` label (the label-less tag), 15 with a swept-in filename or the bracket's own words.
- After: 28 phantoms remain — the compound brackets where the alias is not the bracket's tail (`[Activity: Emotions – MKT Quiz] Engagement trigger`, `[… – Engagement trigger Activity]`) or the tag carries black text; named, not chased. 7 red flags surface a bracket's extra words.

### 4. THE FIX — one data block `Emit_Templates.buttons["engagement quiz button"].trigger_marker` `{{ enabled, env: "ENGMARKER_OFF", aliases: ["trigger engagement", "engagement trigger"], words_flag }}`

- At the generic `[button]` seam, before the label / URL derivation: an `engagement quiz button` item with NO black text whose folded bracket equals — or ends in — one of `aliases` returns nothing; if the bracket carried other words (`[insert text box for student response – engagement trigger]`) ONE `NotesAndComments.redFlag(…, "diagnostic")` cv2-note quotes it (the round-292 rule: a content-less marker is skipped, its words surfaced). `[engagement quiz button]` itself, and any marker followed by writer text, are untouched.
- **Env toggle `ENGMARKER_OFF`** reverts byte-for-byte.

### 5. THE PROOF AND THE GATES

- The in-memory ON probe over ALL 416 modules (`_r329_probe_on_0*.log`) names **60 pages / 42 modules**; scoped regeneration (`_r329_batches_run.sh`); `_content_manifest.py fresh --affected` → **0 truly stale**; OFF in memory vs disk on the 42 = exactly the 60 changed pages; ON in memory = disk on 266/266.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.004pp) IMPROVED / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 60 pages moved — **57 up / 3 down**, pp-sum +8.24 (BLL242_1_1 +0.75, MXFU302_11_0 +0.75, MXFL401_7_0 +0.72, ENGI401_8_0 +0.71 …); the dips NAMED: CEDO105_5_0 −7.63 — the removal of ONE skeleton line (`div.button.engagementTrigger`) re-aligns difflib's block matching against the gold (the r325 / r326 scorer artefact; the page's element sequence is strictly closer to the gold's), MXEO301_7_0 −1.15 (the repeat-collapse: `a>div.button / phantom / a>div.button` becomes one `2× repeated` line), ENGI401_6_0 −0.42.
- Every other gate EXACT (`_fastloop_diff.py` PASS; full suite `_r329_gates.log`): cs exact 11360 / EXTRA 186 / missing 591 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN**.
- **Ceiling:** SCAFFOLD {SK_A}% = **55.1% of achievable** (55.13).

### 6. NAMED, NOT CHASED — AND THE STOP

- The 28 residual phantoms (compound / text-bearing engagement brackets) and the `[engagement quiz button]`'s own form (the gold anchors an external quiz link; Claude ships `button engagementTrigger` with a swept-in filename label) — their own PICK.
- **THE LOOP STOPS on the plateau rule (§4):** three consecutive shipped rounds — r327 0.000pp, r328 0.000pp, r329 +0.004pp — each under 0.02pp with no other protected gate moved (r326 restarted the window at +0.057pp). The derivable, KB-backed queue above the 20-page floor is spent; what remains needs Chris's decisions (see `LOOP_STATE.md`).

**Ledger:** scoped ship #3 since the r326 full · data `buttons["engagement quiz button"].trigger_marker` · env `ENGMARKER_OFF` · tools `outputs/_r329_finalise.py` (the measurement is the inline probe recorded in `LOOP_STATE.md`) · state `outputs/_r329_sk_final.json` (FRESH) · logs `_r329_gates.log`, `_r329_sk_full.log`, `_r329_fastloop.log`, `_r329_selftests.log`, `_r329_probe_on_0*.log`, `_r329_probe_off.log`, `_r329_probe_on.log`, `_r329_regen.log`, `_r329_affected.txt`, `_r329_off_pages/` (the dip check).

"""
if "round 329, build 260619.00" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260618.99";\n'
NEW = ('\t// ROUND 329 (2026-09-15, build 260619.00): "[trigger engagement]" is a marker, not a button — the KB\'s\n'
       '\t// dropbox-trigger condition (constraint 43); the phantom <div class="button engagementTrigger">Go to\n'
       '\t// your journal</div> no longer ships (99 -> 28 on 60 pages / 42 modules, scoped). Env ENGMARKER_OFF;\n'
       '\t// data buttons["engagement quiz button"].trigger_marker. THE LOOP STOPPED after this round on the\n'
       '\t// plateau rule (r327 0.000 / r328 0.000 / r329 +0.004pp).\n'
       '\tstatic AppVersion = "260619.00";\n')
if '"260619.00"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 328 BASELINE (a submission button keeps its full 'Go to' label — KB constraint 55's label half; scoped, gate-neutral)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 329 BASELINE (`[trigger engagement]` is a marker, not a button; scoped): SCAFFOLD mean {SK_A}% / >=50% 1030 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r329_sk_final.json`, FRESH). r329 +0.004 (60 moved, 57 up; dips NAMED CEDO105_5_0 −7.63 / MXEO301_7_0 −1.15 / ENGI401_6_0 −0.42 = the scorer's alignment / repeat-collapse artefacts on a strictly closer element sequence). **The loop STOPPED here on the plateau rule** (r327 0.000 / r328 0.000 / r329 +0.004). Older r328 text: **ROUND 328 BASELINE (a submission button keeps its full 'Go to' label — KB constraint 55's label half; scoped, gate-neutral)")
if "ROUND 329 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `ENGMARKER_OFF` | 329 | **`[trigger engagement]` IS A MARKER, NOT A BUTTON** (KB constraint 43 / 05B / 01F — the dropbox-trigger condition on the activity; the gold carries no engagement element on any of 2,385 pages; the autonomous loop's session-4 Round 4; **SCOPED regeneration of the 42 affected modules; scoped ship #3 since the r326 full**). Reverts byte-for-byte. ON (default), `buttons[\"engagement quiz button\"].trigger_marker`: at the generic `[button]` seam an `engagement quiz button` item with no black text whose folded bracket equals or ends in `trigger engagement` / `engagement trigger` emits NOTHING (the r292 / r322 reading of the same marker); a bracket carrying other words surfaces them as one diagnostic red flag (cv2-note). `[engagement quiz button]` itself is untouched. MEASURED: 275 marker occurrences / 71 modules in the WTs; Claude shipped 99 phantom `button engagementTrigger` (84 with the journal default label) on 88 pages / 70 modules → 28 residue (compound brackets). 60 pages / 42 modules changed. Skeleton +0.004pp (57 up / 3 down, dips named as scorer artefacts); every other gate EXACT; 13 selftests GREEN. **The loop stopped after this round (plateau).** |\n")
if "| `ENGMARKER_OFF` | 329 |" not in m:
    A = "| `BTNLABEL_OFF` | 328 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.00` (round 329 — **`[trigger engagement]` is a marker, not a button** (KB constraint 43; the autonomous loop's session-4 Round 4; **SCOPED regeneration of 42 modules; scoped ship #3 since the r326 full; THE LOOP STOPPED after this round on the plateau rule — r327 0.000 / r328 0.000 / r329 +0.004pp**). **ROUND 329 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r329_sk_final.json`, FRESH) = **55.1% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **60 pages / 42 modules changed, 0 added/removed**; toggle `ENGMARKER_OFF`; data `buttons[\"engagement quiz button\"].trigger_marker`. The next levers need Chris — see `LOOP_STATE.md`.)\n")
if "- **Build:** `260619.00` (round 329" not in m:
    A = "- **Build:** `260618.99` (round 328 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.00"; d["_meta"]["round"] = 329; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A)})
d["_meta"]["_round329_note"] = f"Round 329 ([trigger engagement] is a marker, not a button — KB constraint 43; scoped 42-module regeneration, scoped ship #3 since the r326 full). Skeleton {SK_B}->{SK_A} (+0.004pp; 60 moved, 57 up; dips named as scorer artefacts); every other gate EXACT. The loop stopped after this round on the plateau rule (r327 0.000 / r328 0.000 / r329 +0.004)."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 4 · Round 4 (engine r329) — what shipped (`[trigger engagement]` is a marker, not a button)
- **Fix:** `buttons["engagement quiz button"].trigger_marker` {{enabled, env ENGMARKER_OFF, aliases [trigger engagement, engagement trigger],
  words_flag}} at the generic `[button]` seam before the label / URL derivation: a label-less marker (bracket equals or ends in an alias, no
  black text) emits nothing; a bracket with other words → one diagnostic red flag. `[engagement quiz button]` untouched.
- **Regeneration:** scoped — the in-memory ON probe over all 416 named 60 pages / 42 modules; regenerated; 0 truly stale; OFF vs disk = exactly
  the 60 pages; ON = disk 266/266. Phantom `button engagementTrigger` 99 → 28 (the residue = compound / text-bearing brackets, named).
- **Gates:** skeleton {SK_B} → {SK_A} (+0.004pp; 60 moved, 57 up / 3 down — dips NAMED CEDO105_5_0 −7.63 (one removed skeleton line re-aligns
  difflib's blocks; the element sequence is strictly closer to the gold), MXEO301_7_0 −1.15 (repeat-collapse), ENGI401_6_0 −0.42); every other
  gate EXACT; 13 selftests GREEN. **55.1% of achievable.**
- **Plateau:** r327 0.000 · r328 0.000 · r329 +0.004 → the third consecutive sub-threshold round → STOP (§4).

""")
ANCHOR = "## Session 4 · Round 4 PICK (engine r329)"
if "## Session 4 · Round 4 (engine r329) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Session 4 Round 3 (engine r328 — a submission button keeps its full 'Go to' label, KB constraint 55's label half): SHIPPED 2026-09-15 ≈15:25 (session 4). AppVersion 260618.99, CLAUDE.md §9/§11/§14, KB status row 55 → the label half CAPTURED, scoped ship #2 since the r326 full. Gate-neutral."
NEW_P = OLD_P + nl + "- Session 4 Round 4 (engine r329 — `[trigger engagement]` is a marker, not a button, KB constraint 43): SHIPPED 2026-09-15 ≈15:45 (session 4). AppVersion 260619.00, CLAUDE.md §9/§11/§14, scoped ship #3 since the r326 full. **THE LOOP STOPPED after it (plateau rule: r327 0.000 / r328 0.000 / r329 +0.004).**"
if "- Session 4 Round 4 (engine r329" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s4-r3 (engine r328) · a submission button keeps its full 'Go to' label"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s4-r4 (engine r329) · `[trigger engagement]` is a marker, not a button (KB constraint 43: the dropbox-trigger condition; the phantom `button engagementTrigger` journal button no longer ships) · SHIPPED 2026-09-15 · scoped regeneration, 60 pages / 42 modules · scaffold {SK_B}→{SK_A} (+0.004; 57 up / 3 down, dips named), every other gate EXACT · phantoms 99→28 · 55.1% of achievable · commit (see git log) · **LOOP STOPPED — plateau (r327 0.000, r328 0.000, r329 +0.004)**" + nl
if "- s4-r4 (engine r329)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
