#!/usr/bin/env python3
"""ROUND 337 (loop session 6, Round 3) — finalise: changelog, AppVersion (260619.07 → 260619.08), CLAUDE.md §9/§11/§14,
gate_baseline.json, KB status row 42 → CAPTURED-LIVE (+ a D-row), LOOP_STATE.md (what shipped + position + round log). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.078", "51.079", "35.256", "35.263"
GE50_B, GE50_A, GE75_B, GE75_A, GE90 = 1066, 1066, 200, 200, 15
DELTA = "+0.001"; MOVED = "3 moved — 2 up / 1 down, every mover in the affected set, pp-sum +1.89 (XLP05_5_0 +2.01, MXFU402_3_0 +0.09; PES1001_5_0 −0.21 NAMED = its new <li>s keep the writer's bold lead the gold strips inside the list, the r164/r165 bold class — the <ol> itself now matches); the other 21 changed pages sit inside collapsed accordion widget markers and cannot move the scaffold"; PCT = "55.8"; ACC = "166 panels / 22 modules, every panel matches the human, defect 0"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 337, build 260619.08) — NUMBERED STEPS ARE A SEMANTIC `<ol>`, NEVER `<p>1. …</p>` (KB constraint 42, Universal — the writer's typed sequence AND the extractor's Word-numbered-list marker that shipped every item as "1." inside built widget panels; the autonomous loop's session-6 Round 3; **SCOPED regeneration of the 24 affected modules — a SMALL ship under the loop's 20-page floor on the r320 precedent; skeleton {DELTA}pp, every other gate EXACT; scoped ship #3 since the round-334 full-ship backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**Numbered instructions / steps / sub-questions that reached the page as a run of `<p>1. …</p>` paragraphs now ship as one semantic `<ol><li>` with the typed number stripped (`start="N"` when the run does not begin at 1) — including the visible defect where a Word numbered list inside a built accordion panel shipped EVERY item as "1." (BLL213 / 214 / 235 / 236 / 237 / 263: every comprehension question numbered 1), because `DocxExtractor` marks a numbered-list paragraph with a fixed "1. " and never counts, and the widget panels render lines as `<p>` without ever reaching `renderBlackText`'s list builder.**

### 2. THE EVIDENCE (docx → human → Claude)

- **BLL213 lesson 2** — the docx carries a real Word numbered list (`w:numPr`) "Why did Spotty pick up Sant…" / "How was Sant feeling…" / "Can ants swim…" → gold, inside the accordion panel: `<ol><li>Why did Spotty…</li><li>How was Sant…</li>…</ol>` → Claude before: `<p>1. Why did Spotty…</p><p>1. How was Sant…</p><p>1. Can ants swim…</p>`; after: the gold's `<ol>`.
- **BLL212 lesson 2** — the writer TYPED `1. What happened…` / `2. Can you find…` → gold `<ol>` → Claude before `<p>1. …</p><p>2. …</p>`; after: the `<ol>`. **MXFU402 lesson 3** — `<b>1.</b> Play <b>10 rounds</b>…` (the number bolded on its own) → gold `<ol><li>Play <b>10 rounds</b>…` → after: byte-identical to the gold's list. **SCCH301 / SCPH301 lesson steps, PES1001's five greenhouse steps (`<b>1. Sunlight In:</b>`), XTAS101's "Set the scene" steps** — the same.
- **The KB:** constraint 42 (00D, Universal) — numbered instructions / steps / sub-questions inside an activity or interactive use semantic `<ol><li>` (with `start="N"` for continuation), NEVER `<p>1. …</p>` manual numbering.

### 3. THE MEASUREMENT (`outputs/_measure_r337_typednum.py` → `_r337_typednum.json`; `_measure_r337_numruns.py` → `_r337_numruns.json`; the shipped rule's own OFF/ON probe `_r337_probe.cjs` over all 416 modules in four shards)

- Two forms reach the page as numbered `<p>`s: the writer's typed count (`1. 2. 3.`) and the extractor's marker (`1.` on every item of a Word numbered list — `DocxExtractor` line ~1121 prefixes each numbered-list paragraph with "1. " and never counts). The free-body path (`ListsAndRuns.renderBlackText`) already turns both into `<ol>`; the built-widget panels (`#accordionRich` and its siblings) render `part.text` lines as `<p>${{inline(l)}}</p>` and never see the list builder — which is why the class lives almost entirely inside accordion panels.
- On the shipped rule's own adjacency (a run of ≥ 2 consecutive bare `<p>`s): **24 pages / 24 modules** change (the OFF/ON probe: OFF = disk 2102/2102; ON = exactly the 24). The wider typed-number census (218 numbered paragraphs / 34 pages) also counts single numbered `<p>`s in separate containers — flipCard faces (the gold keeps `1.` as the card title: TWHK901 `<h5>1. Partnership…</h5>`), D&D questions (a plain `<p>`), carousel captions — which are not lists and stay untouched by construction (the run needs two adjacent bare `<p>`s; a widget face holds one). Where the gold holds the run's text it is `<ol>` 111 / `<ul>` 30 / `<p>` 30 (a list at 0.81, `<ol>` at 0.63 — the KB form solidifies).
- **Under the loop's 20-page floor (14 pages by the strict census, 24 by the shipped rule)** — shipped small on the r320 precedent: built, proven, the KB's rule, and the marker form is a visible defect.

### 4. THE FIX — one data block `body_region.typed_number_list` `{{ enabled, env: "TYPEDOL_OFF", lead_pattern, min_run 2, sequential, marker_form_all_equal, start_attr, verbatim_widget_classes }}` + `ListsAndRuns.TypedNumberList(html)`

- A FULL-PAGE post-pass at the r234 `EmojiStrip` seam (`PageAssembler`, after the emoji list clause, before `LinkTextDisplay`, body only — the acks block is never touched): within each LIVE zone, a run of ≥ 2 consecutive bare `<p>` elements (nothing but whitespace between one `</p>` and the next `<p>`) whose text opens with SEQUENTIAL numbers (n, n+1, …) or with the same number on every item (the marker form) becomes one `<ol>` (`start="n"` when n > 1) of `<li>`s; the lead is removed from the paragraph's first text node — a number inside a leading `<b>`/`<i>` is removed there and the wrapper kept (`<b>1. Sunlight In:</b>` → `<b>Sunlight In:</b>`), a number bolded on its own drops its emptied wrapper (`<b>1.</b> Play` → `Play`). A restart or a gap ends the group; a single numbered `<p>` and an attributed `<p>` never join.
- VERBATIM zones (copied through untouched) = EmojiStrip's — cv2-interactive hand-off boxes, cv2-note / cv2-comment, script / style — PLUS every built-widget subtree whose class opens with one of `verbatim_widget_classes` (flipCard, dragAndDrop, clickDrop, dropQuiz, mcq, speechBubble, carousel, tabs, hintSlider, TKmodal, selfCheck, memoryGame, rotateBanner, bubble): those widgets own their inner shape and their verifiers read it. Accordion panels, activity boxes and free body are LIVE. Unit probe `outputs/_r337_unit.cjs`: 20/20 (plain / bold-lead / bold-wrapped / start=2 / restart / gap / non-adjacent / attributed / marker form / every verbatim zone / toggle OFF).

### 5. THE PROOF AND THE GATES

- OFF/ON in memory over ALL 416 modules (`_r337_probe_off_0*.log` / `_r337_probe_on_0*.log`): **OFF (`TYPEDOL_OFF=1`) = disk 2102/2102; ON = exactly 24 pages / 24 modules**, every diff a `<p>` run → `<ol>`. Scoped regeneration in the planner's batches (`_r337_batches_run.sh`, all rc 0; `_r337_regen.log`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = **exactly the 24, 0 added/removed**.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50_B} → {GE50_A} / ≥75% {GE75_B} → {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r337_sk_final.json`, FRESH). {MOVED}.
- Every other gate EXACT (`_fastloop_diff.py` on the 24 PASS; full suite `_r337_gates.log` line-for-line identical to r336 outside the skeleton block): cs exact 11375 / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN** (`_r337_selftests.log`). **Widget verifiers over the 24 affected modules:** accordion {ACC}; flipCard / tabs identical in shape (no run lives inside them by construction). **Ceiling:** SCAFFOLD {SK_A}% = **{PCT}% of achievable** (ceiling 91.6%).
- **Verifier:** runs of numbered `<p>`s on the 24 pages 26 → 0.

### 6. NAMED, NOT CHASED

- **CEDW501 lesson 1:** the writer's Word list is a quiz (question + options, every item "1."); the gold builds an MCQ from it — the r305 quiz builder does not reach a list inside an accordion panel (a nested-quiz follow-up); the page now ships the KB's `<ol>` of those items instead of eleven "1." paragraphs. The single numbered `<p>`s inside flipCard faces / D&D questions / captions (the gold's own forms). The 30 gold `<ul>` renderings of typed sequences (the KB says `<ol>`).
- Also this round: **c41 captions** re-measured — of 512 gold `captionText` lines in the paired modules, 50 ship (every `[caption]`-tagged one), 0 tagged ones are missing, 154 are in no WT and 308 are UNTAGGED writer lines the human captioned; the "line after an `[image]`" discriminator is a caption in the gold at ~0.00 → the remaining gap is editorial (recorded). **c75 external-link buttons** — 15 tagged-and-missing (13 pages, under the floor) and 452 UNTAGGED hyperlink phrases the human buttoned (255 pages): the standalone-hyperlink discriminator needs the live extractor's `block.links` channel (the parsed-text dumps cannot see it) — the next session's first measured PICK.

**Ledger:** scoped ship #3 since the r334 full-ship backstop · data `body_region.typed_number_list` · env `TYPEDOL_OFF` · tools `outputs/_measure_r337_typednum.py` (+ `_r337_typednum.json`), `_measure_r337_numruns.py` (+ `_r337_numruns.json`), `_r337_unit.cjs`, `_r337_probe.cjs` + `_r337_probe_run.sh` + `_r337_shard_0*`, `_r337_affected.txt`, `_r337_batches_plan.txt` / `_r337_batches_run.sh`, `_r337_proof.sh`, `_r337_finalise.py` · state `outputs/_r337_sk_final.json` (FRESH) · logs `_r337_probe_off_0*.log`, `_r337_probe_on_0*.log`, `_r337_regen.log`, `_r337_fastloop.log`, `_r337_gates.log`, `_r337_sk_full.log`, `_r337_selftests.log`, `_r337_verify_accordion.log`, `_r337_verify_flipcard.log`, `_r337_verify_tabs.log`, `_r337_fastloop_commit.log`.

"""
if "round 337, build 260619.08" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.07";\n'
NEW = ('\t// ROUND 337 (2026-09-15, build 260619.08): numbered steps are a semantic <ol>, never <p>1. …</p> (KB constraint 42) —\n'
       '\t// ListsAndRuns.TypedNumberList, a full-page post-pass at the EmojiStrip seam, turns a run of consecutive numbered\n'
       '\t// paragraphs (the writer\'s typed count or the extractor\'s all-"1." Word-list marker) into one <ol>; scoped 24 modules;\n'
       '\t// env TYPEDOL_OFF.\n'
       '\tstatic AppVersion = "260619.08";\n')
if '"260619.08"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 336 BASELINE (the Fundamentals overview chip is a family convention — a registry correction; scoped 31 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 337 BASELINE (numbered steps are a semantic <ol> — KB constraint 42; scoped 24 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75_A} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r337_sk_final.json`, FRESH). r337 {DELTA} ({MOVED}); every other gate EXACT. Older r336 text: **ROUND 336 BASELINE (the Fundamentals overview chip is a family convention — a registry correction; scoped 31 modules)")
if "ROUND 337 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `TYPEDOL_OFF` | 337 | **NUMBERED STEPS ARE A SEMANTIC `<ol>`, NEVER `<p>1. …</p>`** (KB constraint 42, Universal; the autonomous loop's session-6 Round 3; **SCOPED regeneration of the 24 affected modules; scoped ship #3 since the r334 full backstop; a small ship under the 20-page floor on the r320 precedent**). Reverts byte-for-byte (OFF in memory = disk 2102/2102). ON (default), `body_region.typed_number_list`: `ListsAndRuns.TypedNumberList`, a full-page post-pass at the r234 EmojiStrip seam (PageAssembler, after the emoji list clause, before LinkTextDisplay, body only): a run of ≥ 2 consecutive bare `<p>`s whose text opens with sequential numbers (`1. 2. 3.`) or the extractor's Word-numbered-list marker (`1.` on every item — `DocxExtractor` never counts, so a Word list inside a built accordion panel shipped every question as \"1.\") becomes one `<ol>` (`start=\"n\"` when n > 1), the number removed from the first text node (a bolded-alone number drops its emptied `<b>`). Verbatim zones = EmojiStrip's + the data-listed built widgets that own their inner shape (flipCard, dragAndDrop, clickDrop, dropQuiz, mcq, speechBubble, carousel, tabs, hintSlider, TKmodal, selfCheck, memoryGame, rotateBanner, bubble). MEASURED: 24 pages / 24 modules on the rule's own adjacency (the gold holds the run text as `<ol>` 0.63 / a list 0.81). " + f"Skeleton {DELTA}pp ({MOVED}); every other gate EXACT; accordion verifier over the 24 {ACC}; 13 selftests GREEN. |\n")
if "| `TYPEDOL_OFF` | 337 |" not in m:
    A = "| *(no toggle)* | 336 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.08` (round 337 — **numbered steps are a semantic `<ol>`, never `<p>1. …</p>`** (KB constraint 42; the autonomous loop's session-6 Round 3; **SCOPED regeneration of 24 modules; scoped ship #3 since the r334 full backstop; a small ship under the 20-page floor**). **ROUND 337 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r337_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). Every other gate EXACT: cs exact **11375** / EXTRA **171** / missing **593** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **24 pages / 24 modules changed, 0 added/removed**; toggle `TYPEDOL_OFF`; data `body_region.typed_number_list`. Numbered-paragraph runs 26 → 0. **Plateau window: r335 +0.018 · r336 +0.000 · r337 {DELTA} — THE LOOP STOPPED after this round on the plateau rule.**)\n")
if "- **Build:** `260619.08` (round 337" not in m:
    A = "- **Build:** `260619.07` (round 336 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.08"; d["_meta"]["round"] = 337; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75_A})
d["_meta"]["_round337_note"] = f"Round 337 (numbered steps are a semantic <ol> — KB constraint 42; scoped 24-module regeneration, scoped ship #3 since the r334 full backstop). Skeleton {SK_B}->{SK_A} ({DELTA}pp; {MOVED}; >=50 {GE50_B}->{GE50_A}, >=75 {GE75_B}->{GE75_A}, >=90 {GE90}); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
old42 = "| 42 | Numbered steps = semantic `<ol>` (+`start=N`), never typed numbers | CL-0030 area | activity modules | **PARTIAL** — `<ol start=` 3 Claude pages vs gold 156; typed `<p>1.` numbering remains on 28 Claude pages | ListsAn"
i = k.find(old42);
if i > 0 and "SHIPPED round 337" not in k[i:i + 600]:
    j = k.find("\n", i)
    row42 = "| 42 | Numbered steps = semantic `<ol>` (+`start=N`), never typed numbers | CL-0030 area | activity modules | **CAPTURED-LIVE (round 337, 2026-09-15, the loop's session 6)** — `ListsAndRuns.TypedNumberList`: a run of consecutive numbered `<p>`s (the writer's typed count OR the extractor's all-\"1.\" Word-list marker inside a built widget panel) → one `<ol>` (`start=N` when n > 1); 24 pages / 24 modules regenerated; the free-body path already built the `<ol>`. Remaining: the gold's `<ol start=` on 156 pages is mostly its own continuation numbering across split content (no WT signal) | `body_region.typed_number_list`; env `TYPEDOL_OFF` |"
    k = k[:i] + row42 + k[j:]; print("KB row 42")
anchor = "| ~~—~~ | 01F \"Activities\" — `engagement_quiz_button`"
drow = (f"| ~~—~~ | c42 numbered steps = semantic `<ol>`, never `<p>1. …</p>` (the Word-list marker form inside widget panels + typed sequences) | **SHIPPED round 337** (26 numbered-paragraph runs → `<ol>`; 24 pages / 24 modules) | 24 pages | {DELTA}pp | `TYPEDOL_OFF` | CAPTURED-LIVE |\n")
if "c42 numbered steps = semantic" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 6 · Round 3 (engine r337) — what shipped (numbered steps are a semantic <ol>, never <p>1. …</p>)
- **Fix:** `body_region.typed_number_list` {{enabled, env TYPEDOL_OFF, lead_pattern, min_run 2, sequential, marker_form_all_equal,
  start_attr, verbatim_widget_classes}} → `ListsAndRuns.TypedNumberList(html)`, a full-page post-pass at the r234 EmojiStrip seam
  (PageAssembler, body only): a run of ≥ 2 consecutive bare `<p>`s opening with sequential numbers or the extractor's all-"1."
  Word-list marker → one `<ol>` (`start="n"` when n > 1), the number stripped from the first text node (an emptied `<b>` dropped);
  verbatim zones = EmojiStrip's + the built widgets that own their inner shape. Unit probe 20/20.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 24 pages / 24 modules
  (`_r337_affected.txt`); planner batches all rc 0; 0 truly stale; manifest diff = exactly the 24.
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {MOVED}); ≥50 {GE50_B} → {GE50_A}; ≥75 {GE75_B} → {GE75_A}; ≥90 {GE90}; every other gate
  line-for-line EXACT with r336 (fastloop PASS; full suite `_r337_gates.log`); accordion verifier over the 24: {ACC}; 13 selftests GREEN.
  **{PCT}% of achievable.** A small ship under the 20-page floor (14 pages by the strict census, 24 by the shipped rule) — the r320 precedent.
- **Named:** CEDW501's quiz-as-list (the gold builds an MCQ — a nested-quiz follow-up); c41's untagged captions (editorial, "line after
  an image" is a caption at ~0.00); c75's 452 untagged hyperlink buttons (255 pages — needs the live extractor's link channel to measure;
  the next session's first PICK). Ship ledger: scoped #3 since the r334 full backstop.
  **Plateau window: r335 +0.018 · r336 +0.000 · r337 {DELTA} — three consecutive shipped rounds under 0.02pp with no other protected
  gate moved → THE LOOP STOPPED after this round (§4 plateau).**

""")
ANCHOR = "## Session 6 · Round 3 PICK (engine r337)"
if "## Session 6 · Round 3 (engine r337) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = f"- Session 6 Round 3 (engine r337 — numbered steps are a semantic <ol>, KB constraint 42): SHIPPED 2026-09-15 (session 6). AppVersion 260619.08, CLAUDE.md §9/§11/§14, KB status row 42 → CAPTURED-LIVE + D-row, scoped ship #3 since the r334 full backstop. Skeleton {DELTA}pp; every other gate EXACT. **THE LOOP STOPPED after it (plateau rule: r335 +0.018 / r336 +0.000 / r337 {DELTA}).**" + nl + OLD_P
if "- Session 6 Round 3 (engine r337" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s6-r2 (engine r336)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = f"- s6-r3 (engine r337) · numbered steps are a semantic `<ol>`, never `<p>1. …</p>` (KB constraint 42: a run of consecutive numbered paragraphs — the writer's typed count or the extractor's all-\"1.\" Word-list marker inside a built accordion panel — becomes one `<ol>`, `start=N` when needed; a full-page post-pass at the EmojiStrip seam, the built widgets that own their shape verbatim) · SHIPPED 2026-09-15 · scoped regeneration, 24 pages / 24 modules (a small ship under the 20-page floor, the r320 precedent) · scaffold {SK_B}→{SK_A} ({DELTA}; {MOVED}), every other gate EXACT · numbered-paragraph runs 26→0 · {PCT}% of achievable · scoped ship #3 since the r334 full · c41 captions declined (editorial), c75 untagged buttons → next PICK · commit (see git log) · **LOOP STOPPED — plateau (r335 +0.018, r336 +0.000, r337 {DELTA})**" + nl
if "- s6-r3 (engine r337)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
