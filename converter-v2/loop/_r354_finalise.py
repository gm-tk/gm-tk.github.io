#!/usr/bin/env python3
"""ROUND 354 (loop session 15 Round 4 — the words on a widget tag's own line become the Writers Note) — finalise: changelog,
AppVersion (260619.24 → 260619.25), CLAUDE.md §11 / §14, gate_baseline _meta, loop/README.md rows, LOOP_STATE.md. Idempotent."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 354, build 260619.25) — THE WORDS A WRITER TYPES ON A WIDGET TAG'S OWN LINE BECOME THE WRITERS NOTE AFTER THE BUILT WIDGET (they were lost on 193 built widgets of every type; the autonomous loop's session-15 Round 4; FULL regeneration of all 416 — 220 pages / 159 modules gain a red note, nothing else changes; every gate EXACT, gate-neutral by design)

### 1. WHAT CHANGED, IN ONE LINE

**"[flip card] Click on the card to see examples of noun or pronoun", "[drag and drop] answers are placed in the correct columns, please place outside the box", "[carousel] Click on the slide to see examples of noun 和 hé noun", "[please arrange each individual's paragraph on an accordion tab labelled with their name…]", "[speech bubble] example of how to display this" — the words a writer types on the widget invocation tag's OWN line, outside the bracket or as the whole bracket — were LOST on every built widget of every type: the builders read the tag as the invocation and never the words beside it.** Measured over all 416 with the r353 census narrowed to the tag line (`_measure_r354_tagwords.cjs`): **193 built widgets — flipCard 51 (42 pages / 37 modules), carousel 37, dragAndDrop 33 (the words sit in the tag's own text, not its blackAfter, so the r351 paragraph never saw them), speechBubble 33, modal 15, clickDrop 7, tabs 6, accordion 5, hintSlider 5.** They are MOSTLY developer instructions ("please…", "can we…", "if possible…" — the gold keeps only 14 of the 51 flipCard lines as learner text), so they are neither guessed into learner prose nor a reason to decline the build: **they become the red Writers Note after the widget** (the r214 instruction-member class, `bundle.instructions`, emitted by `#interactivePlaceholder`), unless the build's own visible text already carries them or a note already says them. The tag's own name is never a note (an alias the normaliser matched is trimmed at the edges of the bracket text; a broken bracket — "Carousel of images]", "[interactive: carousel + captions" — is read the same way; "interactive:" / "insert" prefixes go; a residue under 5 words is the tag's own vocabulary and is dropped).

### 2. THE MECHANISM

- `InteractiveBuilder.Build` → `#tagWordsNote({ bundle, html, templates })` after every successful build (dragAndDrop included, after r351's own rule): the invocation tag's text outside the bracket + the bracket's inner text (alias-trimmed) + its blackAfter, red runs stripped (already notes), ≥ 5 words, a 4-word-shingle presence test against the built html's visible text + alt / title, de-duplicated against `bundle.instructions`, then pushed to `bundle.instructions`. No widget markup changes; a build never reverts. Data `Emit_Templates.interactive_builders._tag_words_note` {enabled, env `TAGWORDSNOTE_OFF`, min_words 5}.
- Refinements the probes forced (three of them): a broken-bracket line carries the tag's own name outside any regex → alias trimming at the bracket edges (never inside a sentence: the first version mangled "a flip card so that" into "a  so that"); the bracket's INNER text is the instruction when the whole bracket is one ("[please arrange each individual's paragraph on an accordion tab…]" — the normaliser's own remainder deletes the alias words from inside the sentence); a 3–4-word residue ("of with captions", "insert icon for") is the tag's vocabulary, not a note → min_words 5.

### 3. PROOF + PROTECTED GATES (FULL regeneration of all 416 — 36 batches, 4 workers, ALL rc 0; `_stalecheck.sh` 0 stale)

- **The in-memory OFF/ON probe (`_r354_probe.cjs`, all 416):** OFF (`TAGWORDSNOTE_OFF=1`) = the r353 corpus 2110 / 2110; ON = the regenerated corpus 2110 / 2110 byte-identical (`_r354_probe_final_0*.log`); `_content_manifest.py diff` vs the r352/r353 snapshot: **220 pages / 159 modules changed, 0 added / removed** — every change a red `<p class="cv2-note">Writers Note: …</p>` after a built widget, nothing else (`_r354_probe_classify.log`: "pages with a non-note change 0"; the corpus now carries 5980 Writers Notes on 1593 pages).
- **Skeleton (PRIMARY): SCAFFOLD 50.9646 → 50.9646, RAW 35.1173 → 35.1173 — IDENTICAL page-for-page (0 movers; a red note is chrome the scorer excludes)**; ≥50 1073 / ≥75 160 / ≥90 14 @ 1955. compare_structure 11607 / 175 / 617, clean 2080/2103, leak 26/23, body 182, tags 9557/9557, every widget verifier — the gate log identical to r352's line for line except two OVER-CAPTURE percentages (65 → 64 %, 51 → 50 % — the note's words in the body count). Every RESULT line ✓; 15 selftests GREEN. Gate-neutral by design: outside the plateau window.
- **The tag-words census after the round (`_r354_tagwords.log` re-run):** 193 → 72 lines still off the page by the census's ≥ 3-word test, 40 of them ≥ 5 words (a red-marked `[CS …]` bracket the census reads as words but the rule reads as an existing note; a nested bracket inside the tag; a hintSlider whose entry route drops the tag) — recorded for a follow-up, not chased.

**Ledger:** FULL ship (round 354; counter reset) · data `Emit_Templates.interactive_builders._tag_words_note` · env `TAGWORDSNOTE_OFF` · engine `InteractiveBuilder.js` (`#tagWordsNote`, the dispatch seam) · tools `outputs/_measure_r354_tagwords.cjs` (+ `_r354_tw_run.sh`, `_r354_tagwords.json`, `_r354_tagwords.log`), `_r354_probe.cjs` (+ `_r354_probe_run.sh`, `_r354_probe_{off,on,final}_0*.log`), `_r354_probe_classify.log`, `_r354_on_changed_{pages,modules}.txt`, `_r354_changed_modules.txt`, `_r354_debug.cjs`, `_r354_fullship_par.sh` / `_r354_fullship_run.sh`, `_r354_manifest_diff.log`, `_r354_sk_full.log`, `_r354_sk_final.json`, `_r354_gates.log`, `_r354_notes_summary.log`, `_r354_postship.sh`, `_r354_finalise.py` · AppVersion 260619.25.

"""
if "round 354, build 260619.25" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r354 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.25"' not in s:
    old = '\tstatic AppVersion = "260619.24";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 354 (260619.25): the words on a widget tag\'s own line become the Writers Note after the built widget (#tagWordsNote) — 193 built widgets had been losing them.\n' + '\tstatic AppVersion = "260619.25";', 1)
    wr(P, s); print("Config.js: 260619.25")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "| `TAGWORDSNOTE_OFF` | 354 |" not in s:
    OLD11 = "| `WIDGETMEMBERS_OFF` | 353 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `TAGWORDSNOTE_OFF` | 354 | **THE WORDS ON A WIDGET TAG'S OWN LINE BECOME THE WRITERS NOTE.** \"[flip card] Click on the card to see examples…\", \"[drag and drop] answers are placed in the correct columns, please place outside the box\", \"[please arrange each individual's paragraph on an accordion tab…]\" — lost on 193 built widgets of every type (the builders read the tag, never the words beside it; `_measure_r354_tagwords.cjs`). Mostly developer instructions (the gold keeps 14 of 51 flipCard lines as learner text) → the red Writers Note after the widget (`InteractiveBuilder.#tagWordsNote` → `bundle.instructions`, the r214 class), unless the build's text already carries them or a note already says them; the tag's own name is trimmed at the bracket edges, broken brackets read the same way, residues under 5 words dropped. FULL regeneration: 220 pages / 159 modules gain a note, NOTHING else changes; every gate EXACT (gate-neutral by design). Data `Emit_Templates.interactive_builders._tag_words_note`. |\n"
             "| `WIDGETMEMBERS_OFF` | 353 |")
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.24` (round 353"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.25` (round 354 — **the words on a widget tag's own line become the Writers Note after the built widget** (`#tagWordsNote`, data `_tag_words_note`, env `TAGWORDSNOTE_OFF`; 193 built widgets of every type had been losing them; the loop's session-15 Round 4; **FULL regeneration of all 416, ledger counter 0**). **Every baseline = the r352 state (SCAFFOLD 50.965% / 1073 / 160 / 14 @ 1955; RAW 35.117%; cs 11607 / 175 / 617; clean 2080/2103; leak 26/23; body 182; math 323/323) — IDENTICAL page-for-page on every gate**; 220 pages / 159 modules carry a new red note and nothing else (probe ON = disk 2110/2110). Gate-neutral by design.\n"
             "- **Build:** `260619.24` (round 353")
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if d["_meta"].get("build") != "260619.25":
    d["_meta"]["build"] = "260619.25"; d["_meta"]["round"] = 354
    d["_meta"]["_note_r354"] = "Round 354: the tag-line words → Writers Note — every gate IDENTICAL to r352 (a red note is chrome); FULL regeneration, 220 pages gain a note."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: _meta")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r354_finalise.py" not in s:
    A = "| `_r353_probe.cjs` / `_r353_probe_run.sh`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_measure_r354_tagwords.cjs` / `_r354_tw_run.sh` / `_r354_tagwords.json` / `_r354_tagwords.log` / `_r354_probe.cjs` / `_r354_probe_run.sh` / `_r354_probe_{off,on,final}_0*.log` / `_r354_probe_classify.log` / `_r354_on_changed_{pages,modules}.txt` / `_r354_changed_modules.txt` / `_r354_debug.cjs` / `_r354_fullship_par.sh` / `_r354_fullship_run.sh` / `_r354_fullship_regen.log` / `_r354_manifest_diff.log` / `_r354_sk_full.log` / `_r354_sk_final.json` / `_r354_gates.log` / `_r354_notes_summary.log` / `_r354_postship.sh` / `_r354_selftests.log` / `_r354_finalise.py` | `CONVERTER_V2/outputs/` | Session 15 Round 4 (engine r354) — the tag-line words census over every built widget (193 lost), the four probes that shaped the cleaning, the FULL regeneration (220 pages gain a red note, nothing else), the identical gates, the finalise. |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r354 rows")

P = os.path.join(ROOT, "LOOP_STATE.md"); s = rd(P)
if "## Session 15 · Round 4 (engine r354" not in s:
    A = "## Session 15 · Round 4 PICK (engine r354"
    assert s.count(A) == 1, "LOOP_STATE PICK anchor"
    SHIPPED = """## Session 15 · Round 4 (engine r354 — the words on a widget tag's own line become the Writers Note) — what shipped
- **Shipped 2026-09-17 ≈12:25 NZST (session 15).** AppVersion 260619.25, changelog entry r354, CLAUDE.md §11 / §14, `gate_baseline.json` `_meta`, loop/README rows; FULL regeneration of all 416 (36 batches, ALL rc 0; 0 stale), ledger record-full (counter 0).
- **Built:** `InteractiveBuilder.#tagWordsNote` after every successful build (data `_tag_words_note`, env `TAGWORDSNOTE_OFF`, min_words 5): the words outside the bracket, the alias-trimmed bracket text, the blackAfter → `bundle.instructions` → the red Writers Note after the widget, unless the build's text carries them or a note already says them. Four probes shaped the cleaning (alias trimming at the bracket edges only — the first version mangled sentences; the whole-bracket instruction; min_words 5 against the 3–4-word tag-vocabulary residues). OFF = the r353 corpus 2110/2110; ON = disk 2110/2110 after the regeneration; **220 pages / 159 modules gain a red note and NOTHING else changes** (`_r354_probe_classify.log`: non-note changes 0).
- **Gates:** IDENTICAL page-for-page — skeleton 50.9646 / 1073 / 160 / 14, RAW 35.1173, 0 movers; cs 11607 / 175 / 617; clean 2080/2103; leak 26/23; body 182; math 323/323; every verifier EXACT (the gate log differs from r352's only in two OVER-CAPTURE percentages, 65 → 64 and 51 → 50); 15 selftests GREEN. Gate-neutral by design — outside the plateau window. Ship ledger: FULL at r354 (counter 0).
- **Residue (recorded):** the tag-words census still reads 72 lines off the page by its own ≥ 3-word test (40 of ≥ 5 words): a `[CS …]` red bracket the census counts as words but the rule reads as an existing note, a nested bracket inside the tag, the hintSlider entry route — a follow-up; and the note text of an alias-trimmed bracket can read clipped ("of the kupu on the front to play as card is flipped" — the leading "Audio" was the audio alias) — honest, readable, recorded.

"""
    s = s.replace(A, SHIPPED + A, 1)
    B = "- Remaining KB queue (§D): stickyNav (BLOCKED"
    assert s.count(B) == 1, "position anchor"
    s = s.replace(B, "- Session 15 Round 4 (engine r354 — the words on a widget tag's own line become the Writers Note after the built widget; FULL regeneration of all 416): **SHIPPED 2026-09-17 ≈12:25 (session 15)**. AppVersion 260619.25, CLAUDE.md §11/§14; 193 built widgets had been losing the writer's tag-line instructions; 220 pages / 159 modules gain a red note, nothing else; every gate IDENTICAL (gate-neutral by design).\n" + B, 1)
    C = "- s15-r3 (engine r353, the generic members rule at the Build seam)"
    assert s.count(C) == 1, "round log anchor"
    s = s.replace(C, "- s15-r4 (engine r354, the tag-line words → Writers Note) · the words a writer types on a widget tag's own line — lost on 193 built widgets of every type — become the red Writers Note after the widget (never learner prose, never a reason to decline) · SHIPPED · every gate IDENTICAL (gate-neutral by design) · 220 pages / 159 modules gain a note · FULL regeneration, ledger 0 · commit — see git log\n" + C, 1)
    wr(P, s); print("LOOP_STATE.md: round 4 recorded")
print("finalise done")
