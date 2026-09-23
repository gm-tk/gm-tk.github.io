# LOOP__Autonomous_Rounds.md — the standing instructions for an unattended PageForge improvement loop

**Who reads this:** a Claude Code session started in `FINAL_MODULE_DATA` (this folder) by Chris.
**What it does:** runs the disciplined round from `CONVERTER_V2/OPERATING_GUIDE.md` §5 over and over —
pick the largest measured class of mismatch, fix it, rebuild what the fix touches, prove every
protected gate held or improved, write the changelog, commit — and only stops on the rules in §4.
**Written:** 14 September 2026 (after round 313, build 260618.84). This is a STANDING file, not a
kickoff: do not delete it. Update it when the loop's rules change.
**Amended:** 16 September 2026 by the first `/loop-review` (`LOOP_REVIEW__2026-09-16.md`, twelve
approved changes — LOST on 17 September when session 19 rewrote this file from an older copy, and
RESTORED on 22 September) and 22 September 2026 by the second `/loop-review`
(`LOOP_REVIEW__2026-09-22.md`: §0, §1, §1d, §1f NEW, §2, §3, §4, §5b, §5d, §6, §7)), and again on 22 September 2026 by the SESSION-33 CRASH RECOVERY (the §0 item 7
crashed-round rule, the §3 step-1 in-flight marker and its §3 step-7 clear, and the matching clause in
the §7 message and `.claude/skills/loop-start/SKILL.md`). **This file is
edited IN PLACE only — never rewritten from an older copy, never regenerated from memory after a
compaction.** At every commit the mirror copy in `pageforge-site/converter-v2/loop/` is proven
byte-identical (`cmp`), and every session's health check confirms this "Amended" line is present.

---

## 0. Read first, in this order (no exceptions)

1. `CONVERTER_V2/OPERATING_GUIDE.md` — the operating guide. §0 (regeneration is opt-in — see §2 below for
   what this loop is authorised to do), §5 the loop, §9 the gates, §10 the regeneration recipe,
   §12 the finalise ritual, §16 the gotchas.
2. `CONVERTER_V2/BUILD_CHANGELOG.md` — the top 3–4 entries: the current baselines are there.
3. `CONVERTER_V2/reference/Decision_Framework_Human_vs_Claude.md` — the A / B-i / B-ii / C test.
   It is the reason this loop will never reach 100% and must not try to: the human developer's
   pages carry changes from verbal writer feedback that is in no Writers Template. Those are
   class C, they are DECLINED and recorded, and a recorded decline is a successful outcome.
4. **The HTML Convertor knowledge base** — `00-Other-TK-Resources/htmlconvertor-kb/`: `INDEX.md`,
   `00_MASTER_INSTRUCTIONS/` (the constraints), `06_TEMPLATE_RECOGNITION.md` (Legacy vs Refresh;
   Standard / Bilingual / Fundamentals / Inquiry / Combo sub-types), `10_CORPUS_VALIDATED_SCAFFOLDING.md`,
   `14_SUBJECT_GLOBAL_PARAMETERS/` (the subject-family rules), and the whole of
   `12_CHANGE_LEDGER/` (CL-0001 → the latest; `12G_PAGEFORGE_AMALGAMATION_LOG.md` is the
   front-facing subset written for PageForge). **This KB is the most recent statement of what a
   finished module must look like. Where it has a rule, the rule outranks the human gold** (see
   §1b). It has been maintained for ~9 months AFTER most of the human gold was built.
5. `LOOP_STATE.md` at the folder root, IF it exists — a previous session's position in the loop.
   Resume from it. If it does not exist, this is the first session: start at Round 0.
6. **The latest `LOOP_INTAKE__<date>_*.md`** (folder root; today `LOOP_INTAKE__2026-09-19_98_Modules.md`,
   the September 2026 intake of 98 modules) — what the corpus is after an intake, the new
   families, the modules that cannot convert and why, the traps the intake exposed, and its
   **§7 recommended round order, every item of which must be dispositioned before exhaustion may
   be declared (§4)**. A new intake (§1f) writes a new one.
7. **`SESSION_28__Pre_Loop_Summary_2026-09-20.md`** (folder root) — the pre-loop session that
   rebuilt the registries (r408) and fixed the XOTP parsed-text message (r409); round 410 was
   finished by session 29. **CHECK FOR AN IN-FLIGHT ROUND BEFORE PICKING ANYTHING:** the
   Position section and the "Next session starts with" line of `LOOP_STATE.md` say whether a
   round is in flight or built-but-inert (today: no round in flight — see LOOP_STATE.md; r425 was
   finished by session 33 on 22 September 2026).
   Never `git checkout` an in-flight round's files away without deciding (OPERATING_GUIDE.md
   §16, the round-284 lesson).
   **A DIRTY TREE OUTRANKS A CLEAN-LOOKING POSITION LINE (added 22 September 2026, after the
   session-33 Round 5 crash).** If `git status` shows uncommitted engine or data files but this
   file's Position section names no round in flight, the previous session died mid-round and the
   Position line is stale. Recover the round from the tree — `git diff`, the round number and class
   in the files' own comments and `_doc` strings, `Config.js` AppVersion against the top
   `BUILD_CHANGELOG.md` entry (equal = never finalised, nothing regenerated, the corpus is still the
   last shipped state), and whether the round's data flag is `enabled: true` (a live unproven round
   is finished or toggled OFF before ANY regeneration, an intake's included). Write the missing
   §3 step-1 in-flight entry, then continue from §3 step 5. Never `git stash` them either.

Then run `bash _MIGRATION/verify_after_transfer.sh` once. It must say PASS before anything else
(six checks: the five symlinks, the engine and gate-tool checksums, the corpus census, the two
git repos, the toolchain). If it fails, stop and report — do not regenerate anything on a broken
tree. **Three census exceptions:**
- a census FAIL whose only cause is that the gold-module, gold-page or docx counts have GROWN
  is not a broken tree — it is the INTAKE TRIGGER (§1f, Round 0d). Round 0d runs before any
  PICK and BEFORE the miner check (do not re-mine a pre-intake corpus; Round 0d re-mines) — but
  an in-flight or built-but-inert round named in `LOOP_STATE.md` is finished (or toggled OFF and
  proven byte-identical) FIRST, so the intake's full regeneration runs on a proven engine state;
- a Claude-dir / Claude-page mismatch that equals the change the last shipped round records
  (e.g. r425 shipping on 22 Sept 2026 = +12 dirs / +24 pages) is a stale `expect` value in
  `_MIGRATION/verify_after_transfer.sh` lines 76–80 — update it (dated comment, `.pre-rNNN.bak`)
  and continue; it is neither an intake trigger nor a broken tree;
- a count that FELL is never an intake trigger: stop and report — unless the last STOPPED entry
  or handover names the parked / removed file, in which case update the `expect` value the same
  way and continue.

**Then run the other three intake checks (§1f triggers (b)–(d)), one command each:** the gold
dirs with no Claude dir (`comm -23` of the two dir listings) against the §2 no-build list; any
Writers Template / Media List docx newer than its module's `_run.json`
(`find 01-Finalized_Modules_ -name "*.docx" -newer <that module's _run.json>`); the two staging
areas (`ls`) against the latest `00-NEW_NEW_NEW/_INTAKE_AUDIT_<date>.md`. Any hit not already
recorded → Round 0d.

Then note the KB repo's HEAD (`git -C 00-Other-TK-Resources/htmlconvertor-kb log -1 --oneline`)
against the commit `KB_AMALGAMATION_STATUS.md` names as last checked: if it has moved, read the
new commits' ledger rows before the first PICK and record the new HEAD in the status file's
header.

**The census it prints changed on 19–20 September 2026** (the 98-module intake) and again on
21 September (PMT101 converts, r423); any older figure in `LOOP_STATE.md` or a changelog entry
is pre-intake. Current (23 September 2026, build 260620.13 — after the 22 Sept Round 0d and r426–r442: the 12 XOTP modules and the 38 pre-intake never-converted modules are IN; r426 folded 45 over-split pages into 8 single pages; r427 changed chip text only; r440 (D13-6) built MXFUN01 / BLL240 / CEDT207 as one page each and re-paired the five dual-build golds — 2,699 → 2,666 pages, 2,491 → 2,470 pairs; r442 paired six more lesson pages → 2,476):

| | before the intake | now |
|---|---:|---:|
| Claude module dirs | 416 | **545** |
| Claude pages | 2,109 | **2,700** (r457, 24 Sept: −17 — the section-label marker no longer splits HIS1002 / PES1008; r456: +41 — the mid-page lesson heading opens its page, 22 modules; r453: +10 — the TRR table-cell title bar) |
| gold dirs | 454 | **552** |
| Writers Template / Media List docx | 619 | **762** |
| skeleton paired pages | 1,956 | **2,519** (r457: −1 — PES1008's lesson 3 is one page, the human's 3.0 / 3.1 split; r456, 24 Sept: +33 net — 37 new lesson pages, 4 lost to content pairing; r453: +10 — the restored TRR pages; r447: +1 — PWY1002_2_2_0 pairs by content once its journal heading is the gold's own) |

**552 gold dirs against 545 Claude dirs is CORRECT, not a fault — the gap is exactly the 7 with no source.**
The 7 (`GER1003–1007`, `SAM1005`, `SAM1006`) have no Writers Template at all (§2). The 12 XOTP modules joined the
corpus when r425 finished (22 Sept 2026, session 33 Round 1) and **the 38 pre-intake never-converted modules
joined at the 22 Sept Round 0d (session 33 Round 3: 38 / 38 converted, 0 refused — `LOOP_INTAKE__2026-09-22_38_Modules.md`)**.
Three Claude dirs (`TRR104`, `TRR105`, `TRR115`) hold only a `_run.json` (no Writers Template / a pre-existing refusal)
and are not pairs. A gold-only dir is the expected state for a recorded no-build. The table above and
`_MIGRATION/verify_after_transfer.sh` lines 77–78 are updated at every finalise that changes them (`.pre-<tag>.bak` kept).

## 1. The measure of success — and the honest ceiling

The scorecard is the existing protected-gate set (OPERATING_GUIDE.md §9): the skeleton SCAFFOLD mean and
its ≥50 / ≥75 / ≥90 buckets (PRIMARY), % structurally clean, literal-tag leak, compare_structure
exact/EXTRA/missing, body_compare, tags 9557/9557, and every widget verifier at divergence /
defect 0. Every round must hold-or-improve all of them (the A1 exception in the Decision
Framework applies: a writer-tagged widget is judged on its verifier, not on the human's
substitution).

**Round 0 (first session only) builds the ceiling instrument.** Write
`CONVERTER_V2/outputs/_measure_ceiling.py`: for every gold page in the compare set, take each
text-bearing block of the human's page and check (fuzzy, the round-110 matcher's tolerance)
whether that text exists anywhere in the module's parsed Writers Template. Report, per page and
corpus-wide, the share of the human's structure that has NO source in the WT. That share is the
part of the gap no converter rule can ever close. From then on every progress report states the
score as "X% of achievable" alongside the raw number. Commit the tool and its first output
(`outputs/_ceiling_r0.json`) before Round 1. This round changes NO converter output.

**The ceiling was re-measured on 20 September 2026 (session 29, `outputs/_ceiling_r410.{json,md,log}`):
scaffold 90.9 % (loose 93.5 %) on 2,290 paired pages, full-scope 86.7 %.** (2,290 is the
ceiling's own population — paired pages whose module has a parsed Writers Template; the skeleton
gate's 2,353 includes 9 modules the ceiling skips.) Every report quotes "% of achievable" against
**90.9 %** (the earlier 91.6 % / 91.9 % figures were the 1,956-pair corpus).
`CONVERTER_V2/outputs/COVERAGE_DASHBOARD.md` was regenerated the same day. **Both are re-run as part of every
intake (§1f Round 0d)** — an intake changes the denominator, and a "% of achievable" quoted
against a pre-intake ceiling is wrong.

## 1b. The order of authority — what the converter is trying to match (Chris, 14 September 2026)

The human gold is NOT one uniform target. It spans years, several template systems, many
subjects and levels, and it contains mistakes. The target for any element is decided in this
order; the first source that has a rule for the element wins:

1. **The knowledge base (§0 item 4).** A front-facing CL decision, a `00_MASTER_INSTRUCTIONS`
   constraint, or a `14_SUBJECT_GLOBAL_PARAMETERS` family rule that covers the element, within
   its stated scope (subject / template / level / series). This outranks the module's own gold
   — the gold predates the rule. This generalises the recorded doc-14 exception in OPERATING_GUIDE.md §6
   (`Subject_Global_Parameters.json` `overrides_gold`) to the whole KB.
2. **The previously-developed sibling.** The specific earlier module of the same series and
   template (`Module_Structure_Index.json` `module_meta`: subject / template_type / phase /
   series / dev_order; `Precedence_Cascade.json` levels 2–5). A module inherits its sibling's
   structure unless the KB or its own gold says otherwise.
3. **This module's own gold** (OPERATING_GUIDE.md §6 Level 0) — for everything 1 and 2 are silent on.
4. **Template / subject consensus** (`Granular_Scaffold_Registry.json`, solidify share ≥ 0.60),
   then the corpus — only when the module has no gold of its own.

**Human mistakes.** A gold pattern is a TARGET only when it is the convention of its group
(same template, subject and series) at share ≥ 0.60. A single module — or a single page — that
departs from its own group is a HUMAN OUTLIER (the round-178 discipline): do not chase it,
record it, and expect that page's score to stay low. That is a known, accepted cost, not a bug.
The Round-0 ceiling report lists these outlier pages so they are visible, not mysterious.

**Template awareness.** Every measurement, probe and gate run in this loop is grouped by
template family (`01-Finalized_Modules_/{Standard,Bilingual,Fundamentals,Inquiry}` plus the
Legacy-vs-Refresh split from `06_TEMPLATE_RECOGNITION.md`) and by subject family. A class is
never sized corpus-wide alone; it is sized per group, because a rule that is right for
Fundamentals and wrong for Bilingual is not a rule.

**Gates and KB overrides.** The protected gates measure against gold. When the converter
follows a KB rule that the gold does not, those elements will score lower against gold. That is
an INTENTIONAL OVERRIDE, not a regression, and must be handled the way `Subject_Global_Parameters.json`
`_meta.gold_override_policy` already prescribes: record the expected dip, name the pages, and
exclude override-matched elements from the hold-or-improve test via the gate's override policy.
A KB-driven round is judged on (a) its own verifier — does the output match the KB's stated
shape on every module in scope — and (b) every OTHER gate holding.

## 1c. Round 0b — the KB amalgamation audit (first session, after Round 0)

Measured on 14 September 2026: PageForge's changelog references KB decisions up to about
**CL-0070** (with gaps: CL-0016–0021, 0034, 0045, 0049, 0057, 0059–0060, 0063–0064, 0066,
0069), **nothing from CL-0071 to CL-0095**, `Subject_Global_Parameters.json` holds the doc-14
text of 9 July 2026 with `master_enabled:false` (captured but INERT — the engine does not apply
it), and `12G` only starts at CL-0086. So the KB and the converter have drifted apart.

Round 0b builds `KB_AMALGAMATION_STATUS.md` at the folder root: one row per front-facing KB
decision (every CL, every `00_MASTER_INSTRUCTIONS` constraint that passes the 12G front-facing
test, every `14` family rule), with: scope (subject / template / level), status in PageForge
(CAPTURED-LIVE / CAPTURED-INERT / NOT CAPTURED / SUPERSEDED), the data file or toggle that
would carry it, and the number of corpus modules in scope. Also diff the live
`14_SUBJECT_GLOBAL_PARAMETERS/` text against the 9-July capture and list what changed.
**No converter output changes in Round 0b.** Commit the file. From Round 1 on, every NOT
CAPTURED row with ≥ 20 in-scope pages is a class in the queue with **priority over
gold-matching classes in the same area** — a gold-matching round in an area the KB has since
changed is wasted work.

## 1d. Round 0c — THE DIFF MINER (Chris, 17 September 2026 — after four false "exhaustion" verdicts)

**Why this exists.** Sessions 15–18 each declared "exhaustion" on the r356 corpus. Chris then
opened ONE module (BLL110, Inquiry) and found six derivable structural differences on its
overview page alone: a phantom `#module-code` chip, a phantom "Overview" menu heading (gold
1/65), menu labels shipped as `<h5>` where 63/65 Inquiry golds use `<h4><span>`, lead-ins
("Ākonga will:") shipped as headings where the gold uses `<p>`, an extra full-width menu row
with `paddingR` on both columns, and the intro panel's `h3 Introduction` + welcome text placed
after the supervisor note instead of before. The loop's queue had never contained any of them,
because the queue was only ever fed by the KB audit and by classes a session thought to write a
probe for. **Nothing systematically read the per-page structural diffs the scorecard is
computed from.** Those verdicts are VOID. "Exhaustion" may not be declared again until the miner
below exists and its queue is empty.

**The instrument — `reference/tests/_diff_miner.py`** (build it in Round 0c; no converter
output changes in that round; commit the tool and its first output):
1. For every paired page (use the skeleton gate's OWN pairing — never a private one), build the
   gold and Claude skeletons with `_structural_skeleton.py`, keeping each line's TEXT alongside
   its `tag#id.class` signature, and diff them line by line.
2. Tag every differing line with: template family (Standard / Bilingual / Fundamentals /
   Inquiry; Legacy vs Refresh), subject family, series; REGION — `module-code`, `title`,
   `module-menu`, `crumbs` (the Inquiry side-nav), `phases-nav`, `body`, `activity`, `footer`,
   `acks`; ELEMENT ROLE — the gold signature vs the Claude signature at that position (e.g.
   `menu-label: h5 → h4>span`); DIRECTION — MISSING (gold has, Claude lacks), EXTRA (Claude
   has, gold lacks), SUBSTITUTED (same position, different tag/class/wrapper), MOVED (same
   text, different region or order); and DERIVABLE-CONTENT — whether the gold line's text
   exists in that module's Writers Template (fuzzy, the round-110 matcher). A structure-only
   difference (tag, class, wrapper, order, attribute) needs no content and is always derivable.
3. Aggregate into CLASSES keyed by (region, gold signature, Claude signature, direction).
   For each class report: pages, modules, the per-template and per-subject GOLD CONSENSUS
   (of gold pages where the region exists, the share using the gold signature), the
   derivable-content share, the KB rule if one exists (grep the KB for the element and region),
   the authority it would fall under (§1b), and three example modules with the WT / gold /
   Claude lines quoted.
4. Add the COMPLETENESS CENSUS for the repeating chrome: for the module menu, the crumbs /
   side-nav, the phases nav and the footer, count the gold's subsections whose text is in the WT
   against the number Claude rendered. "The WT had it, the human rendered it, Claude did not"
   is a derivable miss and is its own class (`menu-subsections: gold 6 / Claude 2`).
5. Write `outputs/_diff_miner.json` and **`DIFF_QUEUE.md`** at the folder root: the ranked
   table, chrome regions FIRST (module-code → title → module-menu → crumbs/phases-nav →
   footer → acks → activity → body), then by modules affected.

**Candidate rule.** A class is a candidate when: modules ≥ 10 (chrome elements occur once per
module, so the floor is 10 MODULES, not 20 pages — the 20-page floor still applies to body
classes); gold consensus ≥ 0.60 in at least one template or subject group; and either the
class is structure-only or its derivable-content share is ≥ 0.60. A class below the floor in
every group is recorded in the queue as "below floor" with its numbers — never silently
dropped. The BLL110 supervisor-note `div.alert` wrapper (gold 1/24) is the worked example of a
correct decline; the menu-label `h4>span` class (63/65) is the worked example of a candidate.

**Two exceptions to the floor (22 Sept 2026 review).** The floor exists to stop a rule learnt on
a few pages being applied where it does not belong; neither of these can over-reach:
1. A **family dialect** — a rule keyed to ONE family by a registry row or a family flag — may
   ship under the floor when it matches that family's own gold on every page of the family, its
   OFF corpus is byte-identical, and every other gate holds. (The r422 FRFUN06 side-tab dialect
   is the worked example: 10 pages, 8 up / 2 down, +34.7pp-sum, built and parked for want of
   this rule — it ships under it.)
2. A **per-group rule** (a data table keyed by prefix, subject or template, one row per group)
   meets the floor on the SUM of the groups that each pass consensus ≥ 0.60, not on each group
   alone. (The s27 `<br>` soft-break form: ENGJ 0.97 / HIS 0.65 / EXPFUN 0.99, ≈ 25 pages
   together — a candidate under this rule.)

**Cadence.** Re-run the miner at the start of every session and after every full
regeneration (it reads 2 × ~2,560 pages — a full mine took ~134 s on 19 Sept and 90 s on 21
Sept; shard if it nears the timeout). `DIFF_QUEUE.md` is committed each time. The PICK step
(§3) reads it FIRST — by section, since it is ≈ 130 KB (§5d).

## 1e. PROVING HOLD-OR-IMPROVE ACROSS THE SEPTEMBER INTAKE (20 September 2026) — read before judging any gate

On 19 September 2026 the corpus grew by 98 gold modules and 78 Claude builds: skeleton pairs
**1,956 → 2,349** (2,353 today, after r423), compare_structure matched **13,794 → 15,668**, body/defect pages
**2,102 → 2,606**. **Every gate absolute therefore moved and every rate fell, with no regression
behind any of it.** `gate_baseline.json` has been re-based to the whole population and
`_gatecheck.py` reports PASS, but anyone comparing a live number to a figure quoted in a
changelog entry written before 19 September will see a "drop" that is pure arithmetic.

**The rule: when a gate looks worse, SPLIT IT BY POPULATION before concluding anything.** Score
the pre-existing modules separately from the new ones. On 19 September the pre-existing subset
reproduced round 407 exactly:

| gate | r407 baseline | pre-existing subset, after a full regen |
|---|---|---|
| skeleton mean / ≥50 / ≥75 / ≥90 | 54.084 % / 1181 / 202 / 18 | **identical** |
| compare_structure exact / EXTRA / missing / row-wrap | 11779 / 172 / 626 / 23 | **identical** |
| body_compare runaway / empty_container | 5 / 170 | **identical** |
| literal-[tag] leak occ / pages | 26 / 23 | **identical** |
| structurally clean | 2079 / 2102 = 98.91 % | **identical** |

The structural argument underneath it is stronger than the table: `_content_manifest.py fresh`
confirmed the pre-existing modules (413 in the manifest) **byte-identical**, and identical bytes cannot produce
different metrics. Reach for the manifest first — it is one command and it settles the question
outright.

**Two consequences for the round log.** Round-over-round deltas from before 19 September are not
comparable with deltas after it: the population is larger and harder, so the same amount of real
work now buys a smaller headline movement. And the §4 plateau test (three consecutive rounds
under 0.02pp) must be read in that light — say so in the entry rather than letting a session
stop on a plateau that is really a denominator change.

## 1f. Round 0d — THE INTAKE ROUND (Chris, 22 September 2026: new human-developer modules are a standing loop job)

**Why this exists.** From time to time new modules arrive in the human-developer module folders.
Twice so far (3 August: 24 modules; 19 September: 98 modules) an interactive session did the
intake by hand over one to two days, and each time the loop then ran for days on stale
instruments and a stale queue (the September intake voided the ceiling, the dashboard, the
exhaustion verdicts and the `verify_after_transfer.sh` census, and its recommended round order
sat undispositioned until session 31). Chris's instruction (D12-3): when new modules appear,
the loop itself builds their Claude-generated equivalents, amalgamates every discrepancy they
bring into the pipeline, and re-assesses and re-prioritises the pending queue. Round 0d is that
procedure, reconstructed from the two intakes' records (`00-NEW_NEW_NEW/_INTAKE_AUDIT_2026-09-19.md`,
`NEW_MODULES__Intake_2026-08-03.md`, `LOOP_INTAKE__2026-09-19_98_Modules.md`, the r408 scripts
`outputs/_s28_t1_*`, the changelog entries r253 / r264 / r265 / r408 / "FULL CORPUS REGENERATION +
INTAKE RE-BASELINE"). Every tool it names exists on disk (verified 22 Sept 2026) except the
copies it tells you to create (`outputs/_intake_split.cjs`, the `_intake_<date>_*` scripts).

**The trigger (checked at every session start, §0 — (a) by the verify script, (b)–(d) by the
three one-line checks §0 lists).** Any of: (a) `verify_after_transfer.sh`'s census FAILS and the
only figures off are gold dirs / gold pages / docx GROWN; (b) a gold module dir under
`01-Finalized_Modules_/*/` has no Claude dir and is not on the recorded no-build list (the §2
bullet — the 38 pre-intake never-converted modules plus the 19 intake no-builds — or the latest
`LOOP_INTAKE` §5); (c) a Writers Template / Media List docx in an existing gold dir that HAS a
Claude build is NEWER than that module's `_run.json` (a newer human page alone is not a trigger —
note it under "Needs Chris" at the next STOP); (d) a module folder in a staging area
(`00-NEW_NEW_NEW/NEW_MODULES/+_FINALIZED_+/`, `new-html-files-and-wt/`) that is not in the gold
folders AND is not already dispositioned in the latest `00-NEW_NEW_NEW/_INTAKE_AUDIT_<date>.md`
(placed / no source / needs Chris / rejected). **Today every leftover in both areas is
dispositioned** — the seven `+_UNSURE_+` folders (DVCFUN02–5, ENGI205, MPT1004, SCBI202, SCES302,
TEAFUN01–05, XOPTB11) and `new-html-files-and-wt/`'s remnants (SCBI202, SCFUN09, `new-new/`
SCES201 / SCES302: no human HTML on the server) are NOT a trigger; only a folder newer than that
audit is, and a Round 0d that places or refuses a staging folder records it in its own audit so
the trigger cannot re-fire on it. Write the delta list — every gold dir under
`01-Finalized_Modules_/*/` whose code is NOT a key of `data/Module_Structure_Index.json`
`module_meta` (the registry built at the last intake; it carries every gold code including the
no-build ones — `ls -d 01-Finalized_Modules_/*/*/ | xargs -n1 basename` against the
`module_meta` keys, under WSL), plus any docx newer than its module's `_run.json`, plus any
undispositioned staging folder — with where each was found and what it holds, to
`outputs/_intake_<date>_delta.txt` before anything else (Phase 4 rebuilds the index, so this
reference list self-updates). Round 0d then runs BEFORE any
PICK (after any in-flight round is finished or toggled OFF — §0). It is ONE ledger record (a FULL
ship, counter → 0) but TWO changelog entries and two round numbers — `intake-<date>` for the
regeneration + re-base, `r<NNN>` for the registry rebuild — and it has eight phases, each logged
as a line in `LOOP_STATE.md` as it completes, so a session that dies mid-intake resumes at the
phase, not the start. It may take a whole session; that is budgeted.

**What Round 0d may touch under `01-Finalized_Modules_` (the one exception to §2's read-only
rule):** it may ADD — place a new module's folder, write `_parsed.txt` beside its docx, rename a
NEW module's files to the corpus form with a reversible log. It never modifies, renames or
deletes an existing gold page or docx (a replaced human page for an existing module is recorded
in the handover for Chris, who parks the old one as `.superseded.bak` as the HPFUN301 / HES1002
precedents did).

**Phase 1 — provenance, classification, placement** (skip what is already done when Chris has
placed the folders himself).
- Record where each new module came from (`00-NEW_NEW_NEW/_INTAKE_AUDIT_<date>.md`: the 19 Sept
  audit is the template — Part 1 what is missing, Part 2 what each docx is and was renamed to,
  Part 4 placement).
- Classify every Word file BY CONTENT, never by its name: `DocxExtractor.LooksLikeWritersTemplate`
  picks the Writers Template, `MediaListParser.FindMediaTable` the Media List (the engine does the
  same at run time, `ModuleResolver.PrepareRun`) — via `outputs/_intake_classify.cjs <dir>`
  (write it once: load the engine under `--require ./_deflate_raw_polyfill.cjs`, call the two
  functions per docx, print `path<TAB>WT|ML|WT+ML|neither`; the 19 Sept `_docx_classify.json`
  is the expected output shape; keep it for the next intake). Rename to the corpus form — `{CODE} Writers
  Template.docx` / `{CODE} Media List.docx` / `{CODE} Writers Template + Media List.docx`, human
  pages to `{CODE}_{lesson}_{part}.html` (`00-NEW_NEW_NEW/_KB_RULE__Page_Filename_Tails.md`) —
  logging every rename to `00-NEW_NEW_NEW/_RENAME_LOG_<date>.tsv` (`# folder	old	new	rule`, the
  19 Sept file's format). A module with no
  Writers Template is NOT placed: it is recorded (no source — needs Chris). A broken docx
  (truncated, unopenable) is recorded, not renamed.
- Placement: the template folder is read from the module's OWN human HTML body container class —
  `container-fluid` → Standard, `fundamentals container-fluid` → Fundamentals,
  `inquiry container-fluid` → Inquiry, `container-fluid reoTranslate` → Bilingual — cross-checked
  against where its siblings sit. **Only those four folders exist**: `TEMPLATE_DIRS` is hard-coded
  in `reference/tests/_corpus.py`, `reference/tests/corpus.cjs`, `outputs/_corpus.py` and
  `outputs/corpus.cjs`, and a fifth folder would be read as one module named after the folder
  (the reason XOTP sits in Standard). A module with no human HTML defaults to Standard and is
  flagged for Chris (the r128 precedent). Move the folder into
  `01-Finalized_Modules_/{Template}/{CODE}/`, verify the file count, log to
  `00-NEW_NEW_NEW/_MOVE_LOG_<date>.tsv` (`# code	template	files` — the path
  `outputs/_s28_t1_mine_sar.cjs` reads). Chris's "FUN → Fundamentals" rule applies to NEW modules
  only; an existing FUN module stays where its gold was built.
- Parsed text: `node CONVERTER_V2/outputs/parse_docx.cjs "<dir>/<CODE> Writers Template.docx"
  "<dir>/<CODE> Writers Template_parsed.txt"` (and the Media List), under WSL (its deps live in
  the WSL home: `$PF_NODE_MODULES`, default `$HOME/pfdeps/node_modules`). Prove it byte-identical
  on three existing corpus modules FIRST (the 3 Aug 17 / 17 and 19 Sept 5 / 5 proofs), then run it
  for every new docx; 0 failures or stop.

**Phase 2 — the Claude equivalents.**
- Pre-create `01-Claude_Modules_/{Template}/{CODE}/` for every new module (from the move log):
  `corpus.mdir` falls back to a FLAT `01-Claude_Modules_/{CODE}` when the nested dir is absent
  (trap 5). Never pre-create one for a module with no Writers Template.
- Convert the new modules by explicit CODE list (the no-argument default converts only
  `compare_set.txt`, which contains none of them), in batches of ≤ 11 with a long wall, under
  WSL: `cd CONVERTER_V2/reference/tests && REGEN_TIMEOUT=600 ./_regen_safe.sh <≤ 11 CODES>` (wraps
  `STUB_OEMBED=1 timeout $REGEN_TIMEOUT node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs … --force`).
  `batch_convert.cjs` deletes and rewrites each output dir, so an `EPERM … rmdir` on the first
  module means delete permission is missing on the folder — a precondition, not a converter error.
- Record every refusal BY CAUSE under one of three headings and never as a defect: (i) a
  recognition gap with a written spec (a Writers Template dialect the resolver refuses — write the
  spec to `00-NEW_NEW_NEW/_SPEC__<name>.md`, the XOTP spec is the template; it becomes a queued
  recognition round); (ii) no source (no Writers Template — needs Chris); (iii) needs Chris
  (content that exists only as a pasted picture, a missing Media List the page needs). Remove the
  ghost Claude dirs the refusals leave (a dir holding only a `_run.json` with an error) so no
  ghost skews pairing (the r285 trap), and never recreate one (§2).
- A changed docx for an EXISTING module (trigger (c)) regenerates that module in this phase; a
  changed human page is recorded for Chris (see the exception above).

**Phase 3 — the FULL regeneration and its proofs, on the UNCHANGED registries** (authorised by
the §7 message; this is the periodic backstop, so the scoped-ship counter resets to 0). The
order matters: the 19 Sept precedent regenerated and re-based FIRST, with no engine, data or
registry change, so the pre-existing proof is pure — then rebuilt the registries as their own
round (r408). Reversing it makes the "pre-existing EXACT" proof impossible, because a registry
rebuild moves pages (r408 moved 103 modules).
- `_batch_plan.py` (WSL) emits LIGHT lines of up to 22 codes, which are NOT reliable (§6): either
  run its lines with the r416 pattern (`outputs/_s29_r416_fullship_par.sh` — each line rewritten
  to `timeout 900 … batch_convert.cjs … --force`, 4 workers, safe under WSL; the "never in
  parallel" line in `_regen_safe.sh`'s header is the stale 45-second-wall note) or re-split any
  line over 11 codes before `REGEN_TIMEOUT=600 ./_regen_safe.sh …`. Then `./_stalecheck.sh` → 0
  stale (it names every stale dir; regen exactly them and re-check).
- `_content_manifest.py fresh --affected outputs/_intake_<date>_affected.txt` (the new modules)
  → every module OUTSIDE that list byte-identical to the shipped manifest (identical bytes cannot
  move a metric — the strongest proof, one command); `_content_manifest.py changed` must list
  exactly the new codes.
- `./run_all_gates.sh > ../../outputs/_intake_<date>_gates.log 2>&1`, then `_gatecheck.py
  skeleton defect` AND `_gatecheck.py cs bc` (never trust a cached row). Every verifier RESULT ✓.
- **SPLIT BY POPULATION (§1e).** Score the pre-existing subset and the new batch separately
  (generalise `outputs/_s28_t1_split.cjs` to take the new-module list; keep it as
  `outputs/_intake_split.cjs` so the next intake has it). The pre-existing subset must reproduce
  the last shipped round EXACTLY on every decomposable gate; the new batch's own figures are
  named. A rate that fell is arithmetic, not regression.
- Re-base `gate_baseline.json` to the whole population (every field, `skeleton.pairs` included)
  with a `_meta._note_intake_<date>` that states the split; `_fastloop_snapshot.py`;
  `_content_manifest.py snapshot`; `_ship_ledger.py record-full --round intake-<date> --build <AppVersion>`.
  Mirror `gate_baseline.json` (§3 step 7).
- Note in the handover which new modules carry a widget type that has a verifier: the verifiers'
  module sets are fixed lists and do not grow by themselves — extending one is a queued tooling
  round, listed in the round order.

**Phase 4 — the registries, ALL in the same round, as its own ledgered round `r<NNN>` (the r263
stale-registry trap: an index rebuilt without its sibling registries shipped a missing-menu
bug).** The r408 recipe, scripts in `outputs/_s28_t1_*` (generalise their module lists; keep the
new copies as `_intake_<date>_*`):
1. Snapshot the nine registries — `data/Module_Structure_Index.json`,
   `Granular_Scaffold_Registry.json`, `Style_Anchor_Registry.json`,
   `Style_Anchor_Registry_Majority_And_Deviations.json`, `Menu_Scaffold_Registry.json`,
   `Html_Convention_Registry.json`, `Overview_Menu_Heading_Lexicon.json`,
   `Module_Feature_Index.json`, `Scaffold_Consensus.json` — to `outputs/_intake_<date>_pre/`
   (the OFF state for the probe; the r408 list in `outputs/_s28_t1_pre/`).
2. `build_granular_registry.py --shard K 8` × 8 under WSL → `--merge` → `--selftest`
   (`Module_Structure_Index.json` `module_meta` gains every new code with subject /
   template_type / phase / series / dev_order; `Granular_Scaffold_Registry.json`). A prefix the
   `All_Template_Reports` folders never filed needs a `data/Subject_Prefix_Map.json` row: propose
   the label, mark it PROPOSED, and add one line to the "Needs Chris" list — never invent a label
   silently and never build a rule that depends on it (§2).
3. Style-Anchor bases for every new family: `STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs
   ../../outputs/_s28_t1_mine_sar.cjs <PREFIX …>` then `node ../../outputs/_s28_t1_update_sar.cjs`
   (`ReferenceMiner.Distil` over the family's gold; one level per first digit; `page_model
   single-file` where the gold is one page — the CHFUN r265 / WJFUN r408 precedents). A faithful
   row for a family whose renderer does not exist yet can score the family DOWN (FRFUN r408, 26 of
   28 pages): measure each new row in memory, hold back a row that scores its family down, and
   record the family as a DIALECT candidate (§1d exception 1) in the handover's round order.
4. The rest of the chain: `node derive_menu_type.cjs`; `build_convention_registry.py`;
   `build_menu_heading_lexicon.py`; `GRANULAR_SIG_OFF=1 anchor_compare.py --build-consensus` × 8
   then `--merge-consensus`; the feature index `build_feature_index.cjs --shard K 16` × 16 →
   `--merge` → `--selftest`; re-pin the cascade / parity selftests if a pin moved; every selftest
   green. Say explicitly which registry could NOT be rebuilt and why (the r408 entry names
   `Style_Anchor_Registry_Majority_And_Deviations` as a Stage-1 artefact left alone).
5. Prove, then ship SCOPED: the in-memory A/B probe over every module (OFF = the `_pre`
   registries swapped in = disk byte-identical; ON = the changed pages and their module list →
   `outputs/_intake_<date>_r<NNN>_affected.txt`), the gate's own `match()` pre-score on the ON
   pages; then `scoped_ship.sh --affected <that list> --toggle <the registry toggle> --round <NNN>`
   with its named delta (the r408 form: 103 modules, movers 197 up / 76 down, the unaffected pairs
   EXACT). The registry round's movement is ITS entry's named delta, never folded into the intake's
   population re-base.

**Phase 5 — the instruments the intake voids.** In this order, all under WSL: the ceiling
(`outputs/_measure_ceiling.py --baseline outputs/<the current sk_final>.json --json
outputs/_ceiling_r<NNN>.json --md outputs/_ceiling_r<NNN>.md > outputs/_ceiling_r<NNN>.log 2>&1`
— its defaults write `_ceiling_r0.*` against `_r313_sk_final.json`; quote the new "% of
achievable" denominator in §1 and in every later report); the coverage dashboard (`outputs/_s29_dashboard_run.sh`
pattern: the r271 variation census + the r286 decline recorder in 16 shards, then
`_coverage_dashboard.py --refresh`); the DIFF MINER twice — full (`_diff_miner.py` →
`DIFF_QUEUE.md`) and scoped over the new modules alone (`_diff_miner.py <CODES>` →
`outputs/_diff_miner_scoped.{md,json}`); `build_feature_index.cjs --rehtml` / `--merge` /
`--selftest` (the checksum manifests are refreshed AFTER it, never before).

**Phase 6 — the records.** (1) `BUILD_CHANGELOG.md`: one entry "(FULL CORPUS REGENERATION +
INTAKE RE-BASELINE, build <AppVersion> — no engine change)" with the population-split table,
the new committed baseline and the refusals by cause; a second entry for the registry rebuild
(the r408 form) with its probe / scoped-regen proof. Bump `Config.js AppVersion` for the registry
round. (2) `OPERATING_GUIDE.md` §9 / §14 baselines. (3) This file's §0 census table and the §2
no-build bullet. (4) `_MIGRATION/verify_after_transfer.sh` lines 76–82 (`expect` values, a dated
comment, `.pre-<date>.bak` kept) — the intake session of 19 Sept did not, and the next health
check read as a broken tree. (5) `_MIGRATION/CHECKSUMS__engine.txt` / `CHECKSUMS__gates.txt` after
the feature index. (6) `LOOP_STATE.md`: the session-start note's census figures and the Position
section's corpus bullet (LAST FULL = intake-<date>; the no-build count and where the list is), the Round-log line
"0d · intake <date> · N modules · converted / refused by cause · gates re-based", the "Needs
Chris" lines the intake raised. (7) `NEW_MODULES__Intake_<date>.md` (the 3 Aug format: results,
gate numbers, findings) and **`LOOP_INTAKE__<date>_<N>_Modules.md`** at the folder root, the
handover the next session reads (§0 item 6), with the September file's nine sections: §1 summary
· §2 the numbers that changed · §3 what the loop must do at its next start · §4 the influx of
discrepancies, measured (the scoped miner) · §5 the modules that do not convert, by cause · §6
traps hit · **§7 recommended round order** · §8 where everything is · §9 needs Chris. Both mirrored
into `converter-v2/loop/`. Commits: "Corpus: <N>-module intake <date> + full regeneration,
re-baselined at build <X>", "r<NNN> (…): the mined registries rebuilt over the <M>-module gold
corpus", "Loop: intake handover for the <N>-module <date> batch". Never push.

**Phase 7 — re-assess and re-prioritise the queue (Chris's D12-3).** The intake changes what the
best next round is; the queue is re-ranked, not appended to:
1. **Pre-intake exhaustion verdicts are VOID** (§4) — write that into the handover and the Round
   log.
2. The handover's **§7 round order** ranks: (a) each new FAMILY with no renderer or registry row
   (a page-model dialect, the WJFUN / CHFUN precedent — usually the largest single loss: WJFUN
   was 23 modules at 10.4 %), by pages × gap; (b) each recognition gap with a spec; (c) the scoped
   miner's candidate rows for the new modules that hold OUTSIDE the new family too (§3 NEW-FAMILY
   CHECK — a class that collapses without the new family is a dialect, (a) not (c)); (d) then the
   standing queue.
3. **Re-measure the standing queue's "below floor" rows** for every family that grew: a class
   listed below the floor on the old corpus may be above it now (the miner's ranked table keeps
   them with their numbers for exactly this).
4. **Re-read the "Needs Chris" list and the "Follow-up candidates" against the new modules:** an
   item's page count changes; a new module may carry the very shape a pending decision is about
   (say so on its line); a decision that only mattered for a family the intake made moot is
   struck with the reason.
5. **The KB queue (§1c)** is unchanged by an intake, but every NOT CAPTURED row's in-scope
   population is re-counted (a row under the 20-page floor on the old corpus may now be over it —
   c92 was, at r419).
6. Write the re-ranked order into the handover §7 and into `LOOP_STATE.md`'s "Next session
   starts with" line; the first ordinary PICK after Round 0d takes item (a) unless the miner's
   chrome-first rule outranks it with a bigger derivable class.

**Phase 8 — the record.** Round 0d ends with a §5-shaped summary written into its Round-log line
and the handover's §1: the census before → after, the split table, the refusals by cause, the
re-ranked order, the needs-Chris lines it added. The session does NOT stop for it — the §5 report
and the push block are given only when §4 says stop (§5c). If the session's budget is spent, the
next session's Round 1 is the top of the re-ranked order; if not, the loop continues into it at
once.

## 2. What this loop is authorised to do (Chris, 14 September 2026)

- **Regeneration.** The message that started this session carries the code `REGENERATE CORPUS`
  for every round of the loop, scoped by the OPERATING_GUIDE.md §0a / §0b rules: rebuild every module the
  fix touches PLUS the whole family of the tag or widget type it touches (the working half as
  well as the broken half). A full-corpus regeneration is allowed when a change is corpus-wide
  (skeleton / footer / menu scaffold / acks / tag normalisation) and at the OPERATING_GUIDE.md
  §10a cadence (every 8 scoped ships, hard stop 16) — and in Round 0d (§1f Phase 3), which the
  §7 message authorises by name and which resets the cadence counter. State the resolved module
  list and its size in the log before each rebuild.
- **Declines.** A class may be DECLINED without asking Chris when the r182 solidify procedure
  says so: the measured share of the corpus that follows the candidate rule is below 0.60, or it
  is a tie, or there is no derivable discriminator. Record the measurement in the changelog
  entry and in `LOOP_STATE.md` under "Declined classes"; never re-attempt a declined class in
  this loop unless new evidence is named. **The 0.60 floor and the tie test apply only when the
  target comes from authority levels 3–4** (this module's gold, or template / subject consensus).
  When a numbered `00_MASTER_INSTRUCTIONS` constraint or a front-facing CL row covers the element
  (level 1), the gold share is NOT consulted: the KB form is the target, the gold's disagreement is
  a NAMED override (§1b "Gates and KB overrides"), and the round ships — whether or not the
  constraint has a CL row of its own. BLOCK for Chris only when (a) two KB documents disagree with
  each other, (b) the KB disagrees with one of Chris's own project instructions, or (c) the KB
  offers a component-doc example rather than a numbered rule and the gold contradicts it at
  ≥ 0.60. The 20-page floor is a PICK floor: a class under it is recorded, not built, unless it
  rides along with a round already in scope and is proven the same way — or it meets one of the
  two §1d exceptions (a family dialect; a per-group rule summed over its passing groups). (Review
  of 16 Sept 2026: c47 and c23 were declined / blocked on the gold share and Chris confirmed the
  KB on both.)
- **Git.** Commit `pageforge-site` at the end of every shipped round (OPERATING_GUIDE.md §16). NEVER push
  and NEVER `git checkout` / `git restore` a file without proving it is committed. The final
  report gives Chris the copy-and-paste push block.
- **Intake (Chris, 22 September 2026, D12-3).** When new human-developer modules arrive, the
  loop runs Round 0d (§1f) unattended: it may ADD to `01-Finalized_Modules_` (place a new
  module's folder, write its `_parsed.txt`, rename a NEW module's files to the corpus form with a
  reversible log), build the Claude equivalents, rebuild every registry, run the FULL regeneration
  and re-base every instrument and gate, write the handover, and re-rank the queue. It never
  modifies or deletes an existing gold page or docx.
- **Not authorised:** editing anything under `01-Finalized_Modules_` other than the §1f
  additions (the human gold is read-only, forever); reading the gold as a converter INPUT (Level
  0 guardrail); any per-module
  `if (code === …)` special case (DATA OVER CODE); disabling a new rule to silence a verifier
  (OPERATING_GUIDE.md §0a: debug until both populations build).
- **The modules with no Claude build are NOT converter faults — do not "fix" them by inventing
  a source.** The 12 XOTP modules (`XOTPB08–13`, `XOTPG01`, `XOTPG03–06`, `XOTPO01`) convert
  since r425 finished on 22 Sept (the activity-table adapter enabled,
  `Input_Doc_Rules.input_shapes.activity_table.adapter.enabled: true`; the spec is
  `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`; their reader book and the XOTPB
  Overview text are open needs-Chris items). Seven (`GER1003–1007`, `SAM1005`, `SAM1006`) **have
  no Writers Template at all**; nothing the converter can do will ever build them, and chasing
  them is wasted work. `PMT101` converts since r423 (the table-row page markers). **The 38
  PRE-INTAKE modules that held a Writers Template but were never converted** (the BLL243–BLL276
  block, CEDK401, CEDO201, CEDO402, CEDR101, CEDR203, CEDR401, CEDT102, CEDW303, HPRE301, OSSM501,
  SSCI104, SSEA203, SSOG105, TRR110, TWHK902, TWHK907, TWHR905, TWHR907, TWHT903, XMES202) were
  converted at the 22 Sept 2026 Round 0d (session 33 Round 3): 38 / 38 built, 0 refused — they are
  ordinary corpus members now (`LOOP_INTAKE__2026-09-22_38_Modules.md`). A refused
  module's empty Claude dir is deliberately absent so no ghost directory skews pairing (the r285
  trap) — **do not recreate one.** An intake (§1f) records every new no-build module in its
  handover under one of these three headings (recognition gap with a spec / no source / needs
  Chris) and never as a defect.
- **The subject labels: the LANGUAGE split is CONFIRMED, the rest is PROPOSED.** `data/Subject_Prefix_Map.json`
  (round 408) assigns a subject to 30 module-code prefixes that had no learning-area folder. Chris
  confirmed the Languages split on 23 Sept 2026 (D13-12, recorded at r441): CHI / GER / JPN / SAM / SPA
  → "NCEA1", CHFUN / FRFUN / JPFUN / FRNO / GENO / CHWHA / GEWHA → "1-10 Languages" (the file's
  `_meta.confirmed` list) — a subject-keyed rule MAY depend on those. Every other row (WJFUN
  "1-10 Writing (MiW)", PWY / PWYWHA "NCEA1", …) is still PROPOSED: treat it as a grouping
  convenience, **do not build a rule that depends on one being correct**, and do not re-litigate it.
- **The division of labour with interactive sessions (Chris, 20 September 2026).** An
  interactive session does only what the loop cannot do for itself — a registry rebuild after
  an intake, the parsed-text process, the example-module UI. **Converter rounds belong to the
  loop**, because the loop has the compaction and handover machinery for them. If a round is
  stopped mid-flight: roll the corpus back with that round's `*_OFF` toggle, prove
  `_content_manifest.py diff` is 0 pages, leave the code uncommitted, and write the state into
  `LOOP_STATE.md`.

## 3. One round, exactly (repeat until §4 says stop)

Each round is bounded so an interruption loses at most one round of work.

1. **PICK.** Read **`DIFF_QUEUE.md` first** (§1d — re-run the miner if it is older than the
   corpus) — BY SECTION, it is ≈ 130 KB: `grep -n "^## "`, then the Summary and the CANDIDATE
   rows of the ranked table by `sed -n` range — then the NOT CAPTURED rows of
   `KB_AMALGAMATION_STATUS.md`, then `outputs/_coverage_dashboard.py --refresh` (under WSL; it
   writes `CONVERTER_V2/outputs/COVERAGE_DASHBOARD.md`) / the `STOCKTAKE__Track.md` backlog,
   then the latest intake's §7 round order and `LOOP_STATE.md`'s "Follow-up candidates".
   Choose the top candidate: chrome regions before body, KB rows first within an area (§1c),
   then the largest derivable population, skipping anything listed under "Declined classes"
   in `LOOP_STATE.md`. **KB-FIRST CHECK before committing to a
   gold-matching class:** search the KB for a rule covering the element; if one exists, the
   KB rule is the target, not the gold. Write the choice, its measured size per template and
   subject group, and its authority source (§1b, 1–4) to `LOOP_STATE.md` FIRST.
   **AND RAISE THE IN-FLIGHT MARKER IN THAT SAME WRITE (added 22 September 2026, after the
   session-33 Round 5 crash left r427 loose under a Position line that still read “no round in
   flight”).** The Position section's in-flight bullet becomes `ROUND <N> IN FLIGHT — NOT PROVEN`,
   naming the class, the files the round will touch, the data flag and the env toggle. That bullet
   is the ONLY breadcrumb a crashed session leaves, so it is written BEFORE any code is edited,
   not after. A round that has been picked but not marked is a round the next session has to
   reconstruct by forensics — which is exactly the cost this rule exists to remove.
   **NEW-FAMILY CHECK (20 Sept 2026).** The intake added 24 family bases the registries had
   never seen. A class can now reach the candidate floor purely because one new family repeats
   the same shape 20 times. Before committing, check whether the class holds OUTSIDE that
   family: if its consensus collapses once the new family is excluded, it is a family dialect,
   and the right fix is a registry row for that family — not a general rule applied corpus-wide.
   The round-408 FRFUN row is the worked example of getting this wrong in the safe direction: a
   faithful registry row for a family whose renderer does not exist yet scored 26 of 28 pages
   DOWN, and was held back rather than shipped.
2. **TRIANGULATE** three named modules for the class — raw WT → human gold → Claude output, side
   by side, the literal text (Decision Framework, "SHOW THE WRITERS-TEMPLATE EVIDENCE").
3. **MEASURE corpus-wide before coding** (OPERATING_GUIDE.md §5 step 2) with a probe in
   `outputs/` that scans ALL Writers Templates — remember the OPERATING_GUIDE.md §16 trap: a filter on `/media list/` hides the 286 combined
   `Writers Template + Media List.docx` files. Report the share PER template family and subject
   family, not just the total (§1b). Classify: A1 / A2 / B-i / B-ii / C. Only B and C
   (instructions) are actionable. If the target is gold-derived and the share is < 0.60 or tied
   in every group → DECLINE (§2), log it, go to 1. If a numbered constraint covers the element,
   skip the share test — measure only the override list. If it holds in some groups only, scope the fix to those groups (a data
   flag keyed by template/subject — `Template_Modes.json` / `Subject_Global_Parameters.json`
   are the precedents), never a corpus-wide rule.
4. **IMPLEMENT** behind a data flag in `data/*.json` AND an env toggle `<NAME>_OFF`. Edit data
   files with the Edit tool only (they are tab-indented; never `json.dumps` them).
5. **REBUILD** the affected set + the tag/type family (OPERATING_GUIDE.md §0a/§0b) with
   `batch_convert.cjs` run directly under WSL — the form every round since r410 has used:
   `cd CONVERTER_V2/reference/tests && STUB_OEMBED=1 node --require ./_deflate_raw_polyfill.cjs batch_convert.cjs <codes> --force`
   — `scoped_ship.sh --affected <list> --toggle <NAME>_OFF --round N` for a scoped ship, and the
   OPERATING_GUIDE.md §10 recipe for a FULL regeneration (batches of ~11 modules; a batch that
   fails on the oembed-cache write race is re-run singly). Which form: direct `batch_convert.cjs`
   for ≤ 11 codes; `REGEN_TIMEOUT=600 ./_regen_safe.sh` when you want the rc-124 split and the
   freshness post-check; `outputs/_s29_r416_fullship_par.sh` for a FULL regen (4 parallel workers,
   safe under WSL — the "never in parallel" line in `_regen_safe.sh`'s header is the stale
   45-second-wall note). Keep each command under the 30-minute shell timeout and write progress
   to a file so nothing is lost. Prove freshness (under WSL):
   `_content_manifest.py fresh --affected <list>` → 0 truly stale.
6. **PROVE** with `_ab.py <TOGGLE>_OFF=1 <codes>` (the toggle-OFF corpus must be byte-identical
   on every untouched module), then the gates: `bash run_all_gates.sh`, plus the verifier of any
   widget touched, over its WHOLE family. Every gate holds-or-improves, `pairs skipped (parse
   error)` is 0, all selftests green.
   - If a gate regresses: **debug, never revert** (OPERATING_GUIDE.md §0a). Up to **three** repair attempts inside
     the round. After the third failure, toggle the round OFF, prove byte-identity with the
     pre-round corpus, record the class as "BLOCKED — needs Chris" in `LOOP_STATE.md` with the
     evidence, and move to the next class. Blocked is not the same as declined.
   - A page dip may be attributed to the scorer's alignment or repeat-collapse artefact ONLY when
     a companion number on that page rises — the position-free overlap or the uncollapsed
     matched-line count — and both numbers are written beside the page name; the
     `--accept-named` flag (r420) may be used only with those numbers in the log. When the same
     artefact has been named in three shipped rounds, the next PICK is a measurement-tool round
     (the r315 / r382 / r386 precedents) that makes the scorer report the companion metric itself.
   - A verifier's RESULT line must read ✓ at its recorded baseline and ✗ only above it (the r348
     form). A round may not ship while any RESULT line is red; "red at the standing baseline" is
     not a state the loop is allowed to learn to ignore.
7. **FINALISE** (OPERATING_GUIDE.md §12): prepend the `BUILD_CHANGELOG.md` entry, bump `Config.js AppVersion`,
   update `OPERATING_GUIDE.md` §14 if a baseline or toggle changed, refresh `gate_baseline.json`
   (every field — `skeleton.pairs` included) and the feature index (`build_feature_index.cjs`)
   after any regeneration, **mirror every changed loop artefact — `gate_baseline.json`,
   `run_all_gates.sh`, `_corpus.py`, any new verifier, `LOOP_STATE.md`, `KB_AMALGAMATION_STATUS.md`,
   `DIFF_QUEUE.md`, `outputs/COVERAGE_DASHBOARD.md`, this file, and the command copies
   (`.claude/skills/*/SKILL.md` → `loop/_skills/<name>.SKILL.md`, `.claude/settings.json` →
   `loop/_settings/`, `.claude/hooks/*` → `loop/_hooks/`) — into `pageforge-site/converter-v2/loop/`
   and prove the mirror byte-identical (`cmp`)**:
   `CONVERTER_V2/reference/tests/` is NOT in git, so the mirror is the gate tooling's only
   committed copy (22 Sept 2026: the committed baseline was found twelve rounds behind the live
   one). If the round changed the Claude dir or page count, update the `expect` values at
   `_MIGRATION/verify_after_transfer.sh` lines 76–80 the same way (dated comment,
   `.pre-r<NNN>.bak`) — the next health check reads a stale value as a broken tree. When the
   round just finalised is the one §0 item 7 or the §0 census table names (today r425), update
   those two places in the same commit (item 7 → "no round in flight — see LOOP_STATE.md"), **and CLEAR
   the step-1 in-flight marker in the same write** — the Position bullet goes back to "no round in
   flight", or to `LAST BUILT, SHIPPED INERT: r<N>` if the round shipped inert. A finalise that leaves
   the marker standing is as wrong as a PICK that never raised it. Then `git add`
   + `git commit` in `pageforge-site`. Then move the round's PICK + what-shipped sections to
   `LOOP_STATE_ARCHIVE.md` (§5d) and append the round's one-line result to `LOOP_STATE.md`
   ("r314 · class X · shipped/declined/blocked · scaffold 49.94→50.02 · pages moved N").

Never chain a skeleton score from a state file that a scoped regeneration has left stale
(OPERATING_GUIDE.md §16):
refresh the state after every scoped regen, and run a fresh full score when one fits.

## 4. When to stop (any one of these ends the loop)

- **Exhaustion.** ALL of: `DIFF_QUEUE.md` exists, was produced by the §1d miner on the CURRENT
  corpus, and has no candidate row left (chrome floor 10 modules, body floor 20 pages, each
  judged per template/subject group); `KB_AMALGAMATION_STATUS.md` has no NOT CAPTURED row
  left with ≥ 20 in-scope pages; and the dashboard backlog has no derivable class ≥ 20 pages.
  **Any exhaustion verdict reached before the latest Round 0d (§1f) is VOID** — today that means
  before 19 September 2026 — for the same reason the sessions 15–18 verdicts are: the corpus
  gained 98 modules and 24 family bases the queue had never seen, and re-mining on 19 Sept moved
  it 168 → 188 candidate rows (183 after round 408). Exhaustion may only be declared on a miner
  run over the POST-intake corpus. A "do not re-measure" note in `LOOP_STATE.md` is likewise VOID
  after an intake.
  Everything remaining is class C (editorial) or is in "Declined classes". This is the GOOD
  ending — but it may only be declared with the miner's output quoted in the report. The
  session 15–18 verdicts, reached without the miner, do not count.
  **AND (22 Sept 2026 review):** every item in the latest intake handover's recommended round
  order (`LOOP_INTAKE__*.md` §7), in `LOOP_STATE.md`'s "Follow-up candidates" section and in its
  "Needs Chris" list has been dispositioned in writing; **an exhaustion verdict is PROVISIONAL
  until the session has spent one PICK pass on at least one lane OTHER THAN the miner's rows that
  it has not used this session** — the lanes are: the miner's rows; the KB queue; a content-level
  re-read of the hand-off boxes on disk; the recognition / no-build list; per-family registry rows
  (§1d exception 1); the loss ledger's largest family — if every lane has been tried this
  session, the verdict stands, and the STOPPED entry names all six with what each found. (Nine exhaustion
  stops in eighteen sessions to 21 Sept 2026; each of the five miner-quoted ones — s21, s22, s24,
  s25, s30 — was followed within two sessions by 7–11 shipped rounds and +0.29 to +0.34pp found
  on a lane the stopping session had not tried; s30 stopped with two items still recorded in the
  intake's §7 list.)
- **Waiting.** Every remaining class ≥ 20 pages is BLOCKED — needs Chris. This is NOT
  exhaustion: report it as "the loop needs N decisions", list each with §5 item 4, and point
  Chris at `/loop-decisions`. Resume only after `LOOP_STATE.md` carries the answers.
- **Plateau.** Three consecutive shipped rounds **whose PICK predicted a skeleton move** each
  move the skeleton SCAFFOLD mean by less than 0.02 percentage points AND move no other protected
  gate. A round the PICK declares gate-neutral by design — text-only, `<head>`-only, a class or
  attribute the skeleton ignores, a registry correction, a recognition round, a gate-configuration
  round — neither counts toward the window nor resets it. The window does not fire while the §3
  queue still holds a derivable class ≥ 20 pages, or a NOT CAPTURED / AUTHORISED KB row, whose
  PICK predicts ≥ 0.02pp: a plateau is a statement about the QUEUE, not about the last three
  picks. Read every delta on the post-intake population (§1e). Stop and report — the next lever
  needs a human decision, not another round. (16 Sept 2026 review: all three plateau stops to
  then were followed by a score-moving round in the very next session; none has fired since.)
- **Budget.** The round cap or time cap in the kickoff message is reached (`/loop-start` with no
  argument = **12 rounds or 10 hours**, the §7 default). When the time left is less than the next
  round needs to ship AND prove (≈ 60–75 minutes for an engine round, more with a full
  regeneration), do not start it: finish that round's PICK and measurement, record them in
  `LOOP_STATE.md`, and stop — the sessions 11–12 pattern.
- **Widget-BUILD rounds (Chris's D10-3).** A build round is invisible to the skeleton score by
  design (A1: a writer-tagged widget is judged on its own verifier; one widget type per kickoff,
  largest un-built population first — D10-3), so: (a) the plateau "moved" test is the type's
  *Still a box* count on `outputs/COVERAGE_DASHBOARD.md`, regenerated with
  `outputs/_coverage_dashboard.py --refresh` at the start of every build round and again after
  its regeneration (a stale dashboard cannot be the test) — ≥ 20 sites converted from hand-off
  box to built widget is progress; (b) the §3 step-3 solidify test does not apply — the writer's tag is
  the target — while the 20-page floor applies per authoring SHAPE family within the type; (c)
  exhaustion counts the dashboard's un-built widget rows as queue classes.
- **Blocked.** Two classes in a row end BLOCKED (§3 step 6). Something systemic is wrong; stop.
- **Tree health.** `verify_after_transfer.sh` fails, `_check_index_sync.cjs` fails, or a
  regeneration leaves stale modules that a second attempt cannot clear.

On every stop, write the final `LOOP_STATE.md` and then give Chris the report in §5.

## 5. The report Chris receives (plain English, every time the loop stops)

1. Why it stopped (one of the §4 reasons, in one sentence).
2. The scorecard before → after, as "X% of achievable" using the Round-0 ceiling AND the raw
   numbers, each gate on one line.
3. Each round in one line: the class, what the fix does in everyday words, how many pages it
   changed, shipped / declined / blocked.
4. Anything BLOCKED, with the decision Chris needs to make, explained as: what the choice is,
   what happens either way, and a recommendation.
5. The copy-and-paste git block — EXACTLY two lines, nothing else:
   `cd C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site` then `git push`. NEVER include a
   `git log` line: on Chris's machine it opens the `less` viewer, which waits for a keypress,
   blocks the push and (16 Sept 2026) left a stray file in the repo. If Chris should see the
   commits, print them in the chat yourself with `git --no-pager log --oneline -n <N>`. Say
   plainly if anything could not be committed and why.

No jargon without a plain-English definition on first use. "Skeleton SCAFFOLD" = how closely the
page's row/column/activity/section structure matches the human developer's, with the insides of
interactive widgets ignored. "Gate" = one of the automatic scores that must never get worse.

## 5b. Decisions from Chris live in LOOP_STATE.md, not in the conversation

When a round ends BLOCKED and Chris answers the question in the session, the FIRST action is to
record the answer in `LOOP_STATE.md` under a `## Decisions from Chris` heading — date, the
question in one line, the answer in his words, and what it authorises — before acting on it.
A new session never re-asks a question that section already answers, and never treats a
BLOCKED item as open once it has a recorded answer. Chris's in-session authorisations (a
class to build, a budget, a scope) are recorded the same way. This is what makes a fresh
session seamless: the conversation is disposable, the state file is not.

**The open ones live in ONE list (22 Sept 2026).** Every needs-Chris item is one line in
`LOOP_STATE.md`'s `## Needs Chris — open decisions` section — date raised, the question, what it
holds up in pages — oldest first. A STOPPED entry or a round record points at that list and
never restates it; a session that raises a new item appends one line; a decision strikes its
line. `/loop-decisions` reads that list first; `/loop-review` re-checks it (the skill's step 3g).

## 5c. NEVER end the turn to wait (added 15 Sept 2026 — the "continue once the gates finish" stall)

The loop stalled several times because a long command (the gate suite, a regeneration batch, a
verifier) ran past the shell timeout, Claude Code moved it to the background, and the session
ENDED ITS TURN with "I'll continue once the gates finish" — which left the loop waiting for
Chris to type "continue". That is a defect in the loop, not a feature. The rules:

- **The only reasons to end a turn are the §4 stop conditions or a BLOCKED item that needs
  Chris.** Waiting for a command, a regeneration, a gate, a verifier, a compaction, or "the
  next round" is NEVER a reason to end the turn. If work remains inside the budget, keep going.
- The project's `.claude/settings.json` raises the shell timeout to 30 minutes per command
  (ceiling 60). Run gates and batches in the FOREGROUND with an explicit long timeout, and size
  each command to finish inside it. If a command is still backgrounded, stay in the turn: poll
  its output file every 30–60 s (`sleep 45; tail -n 3 <log>`) until it is done, then continue.
- Never ask "shall I continue?", "ready for the next round?", or offer options mid-loop. Every
  decision inside the loop is pre-settled by §1b, §2 and the solidify rule; anything they do
  not settle is BLOCKED — record it in LOOP_STATE.md and MOVE ON to the next class, do not wait.
- A blocked-needs-Chris item ends the ROUND, not the SESSION: keep working other classes.
  Only stop the session when §4 says so, then write the report.

## 5d. STATE-FILE HYGIENE — the size caps (Chris, 17 September 2026, after session 20 died of context thrash)

**What happened.** Session 20 (Opus) ended after 90 minutes with "Autocompact is thrashing". The cause
was not the model: `LOOP_STATE.md` had grown to 636 KB (2,694 lines, 143 sections — every STOPPED entry a
page-long paragraph, every PICK kept forever) and the miner had written a 728 KB `DIFF_QUEUE.md`. The §6
rule "after every compaction re-read the loop file and LOOP_STATE.md" then meant: compact → read 1.4 MB →
full again → compact → … three times, and Claude Code gave up. Session 19 (Fable) lasted 5.5 hours only
because the files were smaller then. **The fix is in the files, not the model.**

**The caps (checked with `wc -c` at every session start, after every write, and in the health check):**
- `LOOP_STATE.md` — the HOT file: hard cap **160 KB**, target **≤ 100 KB**. Over target → condense
  (the Position section, then the oldest Decisions blocks — summarise, never delete a decision) or
  archive, BEFORE any other work. Over the hard cap → the health check FAILS until it is fixed.
- `LOOP_STATE_ARCHIVE.md` — append-only; every round's PICK + what-shipped sections MOVE there at the
  finalise step; only the one-line Round-log entry stays hot. NEVER read it whole: `grep -n '^## '`,
  then `sed -n 'a,bp'`.
- `DIFF_QUEUE.md` — the miner writes the summary, census, chrome facts, the ranked table (top 100 +
  every candidate) and the top-25 candidate details here (≈130 KB — over the whole-read cap below,
  so it is read BY SECTION, §3 step 1); everything else goes to
  `CONVERTER_V2/outputs/_diff_queue_details.md` (≈600 KB), which is NEVER read whole — grep a rank.
- A STOPPED entry ≤ 1,500 characters. A Round-log line ≤ 500. A "Next session starts with" line
  ≤ 800. A Decisions-from-Chris block records the decision, not the conversation.
- **No file over 100 KB is ever read whole**, by anyone, for any reason: `wc -c` first; if large,
  `grep -n` the headings and `sed -n` the range you need. `cat` of a `.json` in `outputs/` is banned
  (the miner's JSON is 41 MB); use a `python3 -c` UNDER WSL (never native — §6) to pull the one
  key you need.
- Every tool output is capped: pipe anything that could be long through `| head -c 6000` (or
  `| tail -n 40`). A regeneration or gate log goes to a file; print its last 3 lines.

**Post-compaction re-read (replaces the §6 sentence).** After an automatic compaction the FIRST
actions are, in order and nothing else: (1) `wc -c LOOP_STATE.md DIFF_QUEUE.md LOOP__Autonomous_Rounds.md`;
(2) read `LOOP__Autonomous_Rounds.md` §3, §4, §5c, §5d, §6 by line range (grep the `## ` headings
first); (3) read `LOOP_STATE.md` ONLY the Session line at the top, the "Next session starts with"
line, the "Position" section and the current round's PICK section — by `grep -n` + `sed -n`, never
the whole file; (4) continue. **Never read the same file twice after one compaction.**

**Thrash breaker.** If a compaction happens twice within five turns: STOP reading files; append one
line to `LOOP_STATE.md` — `COMPACTION THRASH <time>: reads suspended; working from the compaction
summary` — then continue the current step from memory, writing results to files as you go; do the
§5d condense at the next round boundary. If a third compaction follows within five turns, run the
STOP procedure (§7) immediately so the session ends with the state saved rather than dying.

## 6. Anti-timeout discipline (why this runs in Claude Code, not Cowork)

- Claude Code runs on Chris's computer with no 45-second command wall and no folder-mount bug.
- **NEVER call `python3` from the Bash tool on this machine (Chris, 20 September 2026).** It
  resolves to the Windows Store stub and hangs for the full 30-minute timeout — hit three times
  in session 28, once on a line that looked like a harmless guard. **Every Python and every gate
  runs under WSL.** Write scripts with the Write tool; make engine and data edits with the Edit
  tool against the real `pageforge-site/converter-v2/…` path.
- **`_regen_safe.sh` honours `REGEN_TIMEOUT`** (default 40 s, behaviour unchanged when unset).
  Batches of ~11 modules are reliable; the 22-module batches `_batch_plan.py` emits are not.
- **`_gatecheck.py` prints CACHED rows for gates it did not run.** Running it as
  `_gatecheck.py skeleton defect` still prints compare_structure and body_compare lines, from
  the previous run. On 19 September that showed exact-chain down 419 when it was actually up
  1,631 — a false regression verdict that took an hour to unpick. **Always run `cs bc` before
  believing those two rows.**
- Size every command to finish well inside the 30-minute shell timeout — aim for ≤ 10 minutes;
  batch the corpus (a 900 s per-batch wall is the ceiling, not the target).
- Write `LOOP_STATE.md` before and after every round; a new session resumes from it.
- Commit after every round, so a crash loses at most one round.
- Keep console output small: write big results to files under `CONVERTER_V2/outputs/` and print
  the summary line only.
- **Never rewrite an engine or data file in place from a script.** Write to a temporary file,
  check it is non-empty and parses (`node --check` for `.js`, a JSON load for `.json`), then
  move it over the original. (r347: a writer that opened `DocxExtractor.js` before encoding its
  content truncated the engine file to 0 bytes; it was rebuilt from the committed blob with
  `git show`, never a checkout.)
- **Record every automatic compaction** as one line in `LOOP_STATE.md` — "compaction at HH:MM
  during rN, step X" — so the next `/loop-review` can count them; and record why a session
  ended whenever the reason is not a §4 stop (session 7 of 16 Sept left no record; session 31
  had three compactions and a manual `/compact` before the 1.3 MB `CLAUDE.md` cause was found).
- **The native-python hook.** `.claude/settings.json` installs `.claude/hooks/no_native_python.sh`
  (22 Sept 2026) as a pre-command hook: any Bash / PowerShell command that invokes `python` or
  `python3` without `wsl` in it is refused in one second with the WSL form to use — five
  recorded slips had each cost up to 30 minutes. If the hook ever blocks a legitimate command,
  put the python inside the `wsl` call; never remove the hook to get past it.
- **Context diet (added 14 Sept 2026 after the first run filled 1M of context in an hour).**
  `OPERATING_GUIDE.md` (the converter guide — it WAS `CLAUDE.md` until 21 Sept 2026, when its 1.3 MB was found to be auto-loaded into context after every compaction, thrashing the loop; the real `CLAUDE.md` is now a 4 KB pointer) is ~1.3 MB and `BUILD_CHANGELOG.md` ~2 MB — never read either whole. Read
  OPERATING_GUIDE.md §0, §5, §9, §10, §12, §16 (the §0 item 1 list; §2 DATA OVER CODE and §6
  conventions once) by line range (grep the `## ` headings first) and only the
  top 3–4 changelog entries. Read gold/Claude pages with `grep`/`sed -n` ranges, never whole
  files. Prefer `head`/`wc`/counts over dumping lists. **After every automatic context
  compaction, follow the §5d post-compaction re-read exactly** — bounded, by section, never a whole
  file — the compaction summary keeps the gist but not the rules, and an unbounded re-read is what
  killed session 20.

## 7. The standard session-start message (Chris pastes this into EVERY new session)

**Shortcut (added 15 Sept 2026):** both messages below are installed as project slash
commands in `.claude/skills/loop-start/SKILL.md` and `.claude/skills/loop-stop/SKILL.md`.
In any Claude Code session started in this folder, typing **`/loop-start`** sends the start
message (optionally `/loop-start 6 rounds or 4 hours` to set the budget) and **`/loop-stop`**
sends the stop message. If the message text below changes, change the SKILL.md files too —
they are the copies that actually run.

Two companion commands (also in `.claude/skills/`) are NOT loop runs and carry no
`REGENERATE CORPUS` code:
- **`/loop-review`** — a periodic health review of the loop itself, meant to be run on Fable:
  audits KB drift, progress, rule quality, gate health, session mechanics, the intake state
  (§1f) and the open decisions, writes `LOOP_REVIEW__<date>.md`, and **APPLIES every change it
  recommends without an approval gate (Chris, 22 September 2026)** — to this file, to the
  SKILL.md copies, to the next starting message and to `LOOP_STATE.md`'s "Next session starts
  with" line — so the next `/loop-start` already carries the amended framework. It asks Chris
  only when a recommendation would change converter code or data, regenerate modules, or delete
  a recorded decision. It then appends a "## Loop review <date>" entry to `LOOP_STATE.md` and
  commits (never pushes).
- **`/loop-decisions`** — explains every open decision (the `LOOP_STATE.md` "Needs Chris" list,
  §5b) in plain English with real module examples (WT → gold → Claude, quoted), writes
  `DECISIONS__Pending_<date>.md`, and records Chris's answers under "## Decisions from Chris" in
  `LOOP_STATE.md` — striking the decided lines — so the next `/loop-start` actions them.

Chris keeps one message and pastes it unchanged into every new Claude Code session on this
folder, whether the previous session ended cleanly, ran out of context, or died in a power
cut. **It contains no state — the state is in `LOOP_STATE.md` and git** — so it never needs
editing after an intake or a round (22 Sept 2026: the skill copy had acquired a census and a
"round 410 unshipped" sentence that were wrong within a day — never again; anything that can
change belongs in `LOOP_STATE.md` or §0). When a session receives it, the order of work is:
health check → intake check → read the two files → reconcile git with the state file → honour
recorded decisions → continue. The message text is kept here as ONE line so it can never be
lost and so the health check can compare it with the skill body mechanically (`$ARGUMENTS` is
the placeholder `/loop-start` fills with the budget Chris typed; it is kept literally in both
copies so they are byte-identical):

> Continue the PageForge autonomous loop in this folder. Start with a health check: `git status` in pageforge-site, `bash _MIGRATION/verify_after_transfer.sh` (must PASS — except that a census FAIL whose only cause is that the gold-module, gold-page or docx counts have GROWN is the INTAKE TRIGGER: new human-developer modules have arrived, so do Round 0d per LOOP__Autonomous_Rounds.md §1f — build their Claude equivalents, re-base every instrument, write the intake handover and re-prioritise the queue — before any PICK and before the miner check, but AFTER finishing or toggling OFF any in-flight or built-but-inert round; a Claude-dir or Claude-page count off by exactly what the last shipped round records is a stale expect value in that script — fix it and continue; then run the §0 intake checks (b)–(d)), delete every stale git lock in pageforge-site (`.git/index.lock`, `.git/HEAD.lock`, `.git/next-index-*.lock`, `.git/objects/maintenance.lock`, and any `.git/objects/*/tmp_obj_*`), `wc -c LOOP_STATE.md DIFF_QUEUE.md` — LOOP_STATE.md over 100 KB → condense/archive per §5d BEFORE anything else (over 160 KB = health check FAILED until fixed); never read any file over 100 KB whole (LOOP_STATE_ARCHIVE.md and outputs/_diff_queue_details.md are grep-only); confirm `grep -c '^\*\*Amended:\*\*' LOOP__Autonomous_Rounds.md` prints 1 (if not, an older copy has overwritten it — find the newest mirror version that has the header with `git -C pageforge-site log -S'**Amended:**' --oneline -- converter-v2/loop/LOOP__Autonomous_Rounds.md`, `git show <hash>:converter-v2/loop/LOOP__Autonomous_Rounds.md`, diff it against the live file and merge the lost sections IN — never replace the whole file — before doing anything else); and note the KB repo's HEAD against KB_AMALGAMATION_STATUS.md. Then read LOOP__Autonomous_Rounds.md and LOOP_STATE.md — if LOOP_STATE.md does not exist, do Round 0 and Round 0b first. Reconcile git with the state file: any uncommitted engine or data files belong to the round LOOP_STATE.md names as in progress — never git checkout or git restore them; check them against that round's PICK, finish or toggle OFF, and continue from the step the state file shows; **CRASHED-ROUND CHECK — run this BEFORE you believe the Position section:** if `git status` is dirty but LOOP_STATE.md says no round is in flight, the previous session DIED mid-round (a server error, a context blow-out, a power cut) and that line is STALE, not true — the tree is authoritative, not the state file. Do this, in order: `git diff` the uncommitted files; read the round number and the class out of their own code comments and `_doc` strings (a round implemented under §3 step 4 documents itself there); compare `Config.js` AppVersion against the top `BUILD_CHANGELOG.md` entry — EQUAL means the round never finalised, so nothing was regenerated and the corpus on disk is still the last shipped state; check whether the round's data flag is `enabled: true`, because a LIVE unproven round must be finished or toggled OFF BEFORE any regeneration, an intake's full regeneration included; then WRITE the §3 step-1 in-flight entry the dead session never got to write, and continue from §3 step 5. Never `git checkout`, `git restore` or `git stash` those files, and never take a new PICK while they are loose; if the Position section names a round as LAST BUILT, SHIPPED INERT (a DECLINED-INERT round is not it), finishing it is Round 1 — the "Next session starts with" line names the round and the order. Honour every entry under "Decisions from Chris" and never re-ask them; the open ones are in the "Needs Chris" list. THE DIFF MINER (§1d) IS MANDATORY: if reference/tests/_diff_miner.py or DIFF_QUEUE.md does not exist, or DIFF_QUEUE.md is older than the corpus (and no intake round is due — an intake outranks this check and re-mines in its Phase 5), do Round 0c FIRST — build/re-run the miner, commit DIFF_QUEUE.md — and take the PICK from it (chrome regions first: module-code chip, title, module menu, crumbs/side-nav, footer). Any exhaustion verdict reached before the latest intake round (today: before 19 September 2026) and any "do not re-measure" note in LOOP_STATE.md are VOID; exhaustion may only be declared under §4's full test — the miner's queue quoted, the intake's §7 list and the follow-up list dispositioned, and one PICK pass spent on a lane other than the miner's rows that this session has not used (if every lane has been tried, the verdict stands and the STOPPED entry names them all). BEFORE JUDGING ANY GATE READ §1e: when a gate looks worse, split it by population or run _content_manifest.py fresh; never stop on a plateau or a regression you have not split. Never call python or python3 from the Bash tool on this machine (the Windows Store stub hangs 30 minutes; the settings hook now refuses it) — every Python and gate runs under WSL; _gatecheck.py prints CACHED rows for gates it did not run, so run `cs bc` before believing the compare_structure or body_compare lines. This message carries the code REGENERATE CORPUS for every round of the loop, scoped by the §0a/§0b family rules in OPERATING_GUIDE.md (the converter guide; CLAUDE.md is only a pointer to it), and for the intake round's full regeneration. Budget for this session: $ARGUMENTS — if that is blank, 12 rounds or 10 hours, whichever comes first. RUN UNINTERRUPTED (§5c): never end your turn to wait for gates, regenerations, verifiers or background commands — run them in the foreground with a long timeout or poll them until done; never ask me whether to continue; a blocked item ends the round, not the session — record it and move to the next class. Follow the §6 context-diet rules: never read OPERATING_GUIDE.md or BUILD_CHANGELOG.md whole, and after every automatic compaction do ONLY the bounded §5d re-read and log the compaction as one line in LOOP_STATE.md. Update LOOP_STATE.md before and after every round, mirror the loop artefacts and commit after every round, never push. Stop only when §4 says so; then give me the §5 plain-English report with the copy-and-paste push block, and end LOOP_STATE.md with a "Next session starts with:" line.

**The mechanical check** (the health check of every session and of every `/loop-review`):
`diff <(sed -n 's/^> Continue the PageForge/Continue the PageForge/p' LOOP__Autonomous_Rounds.md) <(sed -n '6p' .claude/skills/loop-start/SKILL.md)`
must print nothing, and `grep -c '^\*\*Amended:\*\*' LOOP__Autonomous_Rounds.md` must print 1
(an unanchored grep for "Amended:" also matches the quoted message above and proves nothing).

**The standard STOP message** (Chris pastes this into a running session to end it cleanly; it
lets whatever is running finish rather than cutting it off):

> STOP THE LOOP at the next logical point, without interrupting anything already running: let
> any regeneration, gate or verifier that is in progress finish, then do not start any new
> round, class or rebuild. If the current round's remaining steps can be finished and proven
> in under 10 minutes, finish and commit the round; otherwise switch its toggle OFF so the
> corpus is back to its last proven state, and leave its work uncommitted-but-described. Then:
> (1) record every decision I gave you this session under "## Decisions from Chris" in
> LOOP_STATE.md; (2) update LOOP_STATE.md with exactly where the loop is — round, class, step,
> shipped / declined / blocked, anything uncommitted — and end it with a "Next session starts
> with:" line; (3) commit everything finished in pageforge-site; (4) give me the §5
> plain-English report with the push block; (5) confirm in one sentence that it is safe to
> close this session.
