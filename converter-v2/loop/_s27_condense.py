#!/usr/bin/env python3
"""Session 27 §5d condense of LOOP_STATE.md (99.6 KB → target well under 100 KB).
Moves (A) the s19–s25 STOPPED entries, (B) the verbatim D10 decisions block and (C) the
sessions 5–9 decisions blocks to LOOP_STATE_ARCHIVE.md (append-only) and leaves a condensed
summary of each in the hot file. Idempotent guard: refuses to run twice."""
import io, os, sys, datetime

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOT = os.path.join(ROOT, 'LOOP_STATE.md')
ARC = os.path.join(ROOT, 'LOOP_STATE_ARCHIVE.md')
STAMP = '2026-09-19 session 27 §5d condense'

with io.open(HOT, encoding='utf-8') as f:
    lines = f.read().split('\n')

if any('archived at the ' + STAMP in l for l in lines):
    print('already condensed'); sys.exit(0)

def find(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix):
            return i
    raise SystemExit('not found: ' + prefix)

# --- locate the blocks by their headings (never by hard-coded line numbers) ---
s26_stop = find('## >>> STOPPED 2026-09-19')
s25_stop = find('## >>> STOPPED 2026-09-18 ≈20:40')
s19_stop = find('## >>> STOPPED 2026-09-17 ≈22:15')
dec_s25 = find('## Decisions from Chris (session 25')
dec_s10 = find('## Decisions from Chris (session 10')
dec_s9 = find('## Decisions from Chris (session 9')
dec_s2 = find('## Decisions from Chris (session 2 —')
env = find('## Environment (decided 2026-09-14')

assert s26_stop < s25_stop < s19_stop < dec_s25 < dec_s10 < dec_s9 < dec_s2 < env

# block A: s25 .. s19 STOPPED entries (lines s25_stop .. dec_s25-1)
blockA = lines[s25_stop:dec_s25]
# block B: the D10 verbatim block (dec_s10 .. dec_s9-1)
blockB = lines[dec_s10:dec_s9]
# block C: sessions 9,8,6,5 (dec_s9 .. dec_s2-1)
blockC = lines[dec_s9:dec_s2]

summaryA = [
    '## STOPPED entries, sessions 19 / 21 / 22 / 23 / 24 / 25 → LOOP_STATE_ARCHIVE.md \'STOPPED entries sessions 19–25 (archived at the ' + STAMP + ')\' — grep the session number there. One line each: s25 (18 Sept 20:40) §4 EXHAUSTION with the miner quoted (179 rows dispositioned) + the loss ledger (47.94pp by family; honest ceiling ≈ 87 %); s24 (19:30) §4 EXHAUSTION, 10 rounds / 7 shipped r377–r385 (+0.364pp incl. two instrument re-baselines r382 / r386); s23 (12:35) `/loop-stop`, 7 shipped r370–r376 (+0.289pp, the heading census); s22 (08:35) §4 EXHAUSTION, r369 declined inert (the activity-number provenance question raised); s21 (03:05) §4 EXHAUSTION, r364–r368 (3 shipped +0.351pp; the journal button + the dual-build pairing questions raised); s19 (17 Sept 22:15) `/loop-stop` after Round 0c (the DIFF MINER built) + r357–r362 (+0.284pp).',
    '',
]

summaryB = [
    '## Decisions from Chris (session 10 — 2026-09-16 ≈15:20 NZST; the `/loop-decisions` session; ALL NINE pending decisions answered) — the VERBATIM record (his words, every authorisation, scope and KB delta) is in LOOP_STATE_ARCHIVE.md \'Decisions from Chris D10-1…D10-9 (verbatim, archived at the ' + STAMP + ')\' — grep `D10-N` there before acting on any of them. The report he answered: `DECISIONS__Pending_2026-09-16.md`. The decisions, one line each (every one actioned or recorded in later rounds — see the Round log / archive):',
    '- **D10-1 — the duplicate opening body heading (KB c47): Option A** — on every lesson page drop the opening body heading whose text equals the header title once case / punctuation / a `Lesson N` prefix are ignored; the lesson number stays in the `#module-code` h1, the lesson title stays the `<h1><span>`; headings inside an activity box or introducing a sub-topic are KEPT; overview strip-only. Named override on the ≈ 6 pages where the human kept the repeat. Sibling: the title\'s stray `*` / `**` markers (c79 hygiene). SHIPPED r344.',
    '- **D10-2 — the bilingual lesson-title pair order in Standard modules: Option B — English first** (the r316 `header.lesson_bilingual_pair` mechanism, `reo_detect "macron"`); the MTK rule (Māori first, 07D rule 7) untouched for Bilingual; ANZH105_1_0 / HIS1006_10_0 named overrides. KB delta: 00G c79 / 01A to state it. Not covered: the overview `[TITLE BAR]` pair, Languages three-part titles (c85).',
    '- **D10-3 — building the un-built interactives: Option A** — widget-BUILD rounds inside the loop, ONE type per kickoff, largest un-built population first (dragAndDrop → clickDrop → accordion → carousel → flipCard → selfCheck → modal → tabs → slider → infoTrigger → shapeHover → hint → hintSlider → glossary; re-run the dashboard census at each kickoff); each round = the type\'s largest un-built authoring SHAPE family ≥ 20 sites, behind a data flag + env toggle, judged A1 on the widget\'s own verifier (never on the human\'s substitution), NEVER half-built (an unbuildable shape stays the hand-off box); family regeneration; the plateau "moved" test for a build round = the type\'s *Still a box* count (≥ 20 sites converted = progress). The `interactive` modifier + widened wrapper follow each build. Sequence: after D10-6 → D10-1 → D10-2 → D10-7 → D10-5 → D10-9.',
    '- **D10-4 — the `stickyNav` include: Option C — keep the ban everywhere. CLOSED**, no round; `Emit_Templates.skeleton.never_emit` stays. KB edits authorised for a KB session: 14A lines 54 / ~121, 14B line 93, 14D line 11 → "never emitted by the Convertor or PageForge".',
    '- **D10-5 — the table form: Option A — 05D\'s `table table-bordered` everywhere**, `table tableFixed` (no border) for a true two-column COMPARISON table (data-driven contrast-lexicon header test); `noHover` / `center-text` not emitted; a named override in Standard (the 0.51 tie), gains in the other three templates; 06 §6 SUPERSEDED (KB delta). FULL regeneration. Verifier: every table\'s class set ∈ {`table table-bordered`, `table tableFixed`}. SHIPPED r346.',
    '- **D10-6 — the eight CED revision-brief modules (CEDR201 / CEDR301 / CEDR302 / CEDT201 / CEDT202 / CEDT203 / CEDT204 / CEDW303): Option C — excluded from the comparison set** (`reference/tests/compare_exclusions.txt`, honoured by `_corpus.py mods()`), their Claude dirs stay and regenerate as today; every baseline re-established on the new population BEFORE any later class (a POPULATION change, never a gain). Option A (scaffold from the brief) NOT authorised. SHIPPED r343.',
    '- **D10-7 — Word equations: Option A — MathML** (the gold\'s form, renders in MTK): `DocxExtractor.js` reads `m:oMath` / `m:oMathPara` beside the runs (unknown OMML preserved as text, counter `mathEquations`); output `<math xmlns="http://www.w3.org/1998/Math/MathML">` (inline in a run, block on its own paragraph — follow the gold\'s majority per position), ported from V1.5 `pageforge-site/js/omml-to-mathml.js`; `body class="container-fluid mathJax"` on every page with a `<math>`. Scope 12 WTs / 329 equations / ~80 pages. KB delta: 05A → MathML is the shipped form. Verifier: docx OMML count == page `<math>` count. SHIPPED r347.',
    '- **D10-8 — the `alertPadding` activity class: Option B — leave the plain form. CLOSED**, no round (the gold\'s 0.81 + 05B "own class set"); 01F line 27 / 05B line 39 are an example, not the default.',
    '- **D10-9 — the lesson-menu label form (KB c23 / 01B): Option A — every lesson-menu label `<h5>`** with the KB\'s normalised wording (`We are learning:`; `I can:` years 7–10 / `You will show your understanding by:` years 1–6 — the level from `module_meta` / the code digit; the writer\'s label kept where unknown), a ROLE classifier replacing the r117 phrase list, NO section title above the labels on a lesson page, the r81 eng-family `<p>` skip retired, the c70 OSSC lead-in SENTENCE stays a `<p>` above the first `<h5>`, the overview tab\'s labels `<h5>` too (its `<h4><span>` titles STAY). Scope 176 lesson pages / 42 modules + ~296 overview pages; a named KB-over-gold override (≈ −0.1pp). FULL regeneration. Verifier `_verify_menulabels` (defect 0). SHIPPED r348 / r349.',
    '',
]

summaryC = [
    '## Decisions from Chris (sessions 5 / 6 / 8 / 9 — 2026-09-15 → 2026-09-16) → LOOP_STATE_ARCHIVE.md \'Decisions from Chris sessions 5–9 (verbatim, archived at the ' + STAMP + ')\'. Each held only the standing §7 kickoff (12 rounds or 10 hours; `REGENERATE CORPUS` scoped by §0a / §0b; RUN UNINTERRUPTED; never push) and, in s5 / s6 / s9, the standing STOP message (finish-and-commit if provable in ≤ 5–10 minutes, else toggle OFF and describe; record decisions; "Next session starts with:"; the §5 report; no push). No numbered decision was given in them; the classes they left open (stickyNav, equations, c47, the title-pair order, the interactive builds, the table form, the CED briefs, `alertPadding`, the c23 menu labels) were ALL decided in session 10 (D10-1…D10-9 above). Applied stops: s5 r335 shipped OFF then finished in s6; s6 stopped after the r337 plateau; s8 r340 shipped, exhaustion at 10:10; s9 r342 toggled OFF at the stop (later finished).',
    '',
]

new = (lines[:s25_stop] + summaryA + lines[dec_s25:dec_s10] + summaryB + lines[dec_s9:dec_s9] + summaryC + lines[dec_s2:])

arc_add = [
    '',
    '## STOPPED entries sessions 19–25 (archived at the ' + STAMP + ')',
    '',
] + blockA + [
    '',
    '## Decisions from Chris D10-1…D10-9 (verbatim, archived at the ' + STAMP + ')',
    '',
] + blockB + [
    '',
    '## Decisions from Chris sessions 5–9 (verbatim, archived at the ' + STAMP + ')',
    '',
] + blockC

with io.open(ARC, 'a', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(arc_add) + '\n')
with io.open(HOT, 'w', encoding='utf-8', newline='\n') as f:
    f.write('\n'.join(new))

print('hot lines', len(lines), '->', len(new), '; archived', len(blockA) + len(blockB) + len(blockC), 'lines')
print('hot bytes', os.path.getsize(HOT), '; archive bytes', os.path.getsize(ARC))
