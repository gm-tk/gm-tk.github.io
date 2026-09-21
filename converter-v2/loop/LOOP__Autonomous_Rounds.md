# LOOP__Autonomous_Rounds.md — the standing instructions for an unattended PageForge improvement loop

**Who reads this:** a Claude Code session started in `FINAL_MODULE_DATA` (this folder) by Chris.
**What it does:** runs the disciplined round from `CONVERTER_V2/OPERATING_GUIDE.md` §5 over and over —
pick the largest measured class of mismatch, fix it, rebuild what the fix touches, prove every
protected gate held or improved, write the changelog, commit — and only stops on the rules in §4.
**Written:** 14 September 2026 (after round 313, build 260618.84). This is a STANDING file, not a
kickoff: do not delete it. Update it when the loop's rules change.

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
6. **`LOOP_INTAKE__2026-09-19_98_Modules.md`** (folder root) — the September 2026 intake of 98
   modules: what the corpus now is, what the new families are, the 20 modules that cannot
   convert and why, and the six operational traps it exposed. Read this once per session until
   the loop has shipped three rounds on the new corpus; it is the reason several numbers in
   older changelog entries no longer compare.
7. **`SESSION_28__Pre_Loop_Summary_2026-09-20.md`** (folder root) — the interactive session that
   rebuilt the registries (r408) and fixed the XOTP parsed-text message (r409), and that left
   **round 410 (the WJFUN tile dialect) BUILT AND PROVEN BUT NOT SHIPPED**, five files
   uncommitted with the corpus rolled back to the shipped state.
   **CHECK FOR AN IN-FLIGHT ROUND BEFORE PICKING ANYTHING.** `LOOP_STATE.md` carries the
   handover block. Either finish round 410 from that state or revert its five files
   deliberately — never `git checkout` them away without deciding (OPERATING_GUIDE.md §16, the round-284
   lesson).

Then run `bash _MIGRATION/verify_after_transfer.sh` once. It must say PASS before anything else
(it checks the five symlinks and the engine checksums). If it fails, stop and report — do not
regenerate anything on a broken tree.

**The census it prints changed on 19–20 September 2026** and any older figure you find in this
file, in `LOOP_STATE.md` or in a changelog entry is pre-intake. Current, after the 98-module
intake and the round-408 registry rebuild:

| | before | now |
|---|---:|---:|
| Claude module dirs | 416 | **494** |
| Claude pages | 2,109 | **2,555** |
| gold dirs | 454 | **552** |
| Writers Template / Media List docx | 619 | **762** |

**552 gold dirs against 494 Claude dirs is CORRECT, not a fault.** 20 modules have no Claude
build at all (§2), so a gold-only dir is the expected state for them.

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

**The ceiling is currently UNMEASURED on this corpus (20 Sept 2026).** Every recorded ceiling —
`_ceiling_r0`, `_ceiling_r315`, `_ceiling_r343`, and the "X % of the 91.9 % ceiling" phrasing in
`LOOP_STATE.md` — was measured on the 1,956-pair corpus. The population is now 2,349 pairs with
new families whose derivable share is unknown. **Do not quote a "% of achievable" figure until
`_measure_ceiling.py` has been re-run**, and re-run it early: it is the denominator every
"how much is left" judgement uses. `COVERAGE_DASHBOARD.md` is stale for the same reason (last
built on the r349 corpus).

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

**Cadence.** Re-run the miner at the start of every session and after every full
regeneration (it reads 2 × ~2,100 pages; keep it under the timeout by sharding if needed).
`DIFF_QUEUE.md` is committed each time. The PICK step (§3) reads it FIRST.
(It now reads 2 × ~2,555 pages, not 2 × ~2,100 — budget accordingly; a full mine took ~134 s on
19 Sept.)

## 1e. PROVING HOLD-OR-IMPROVE ACROSS THE SEPTEMBER INTAKE (20 September 2026) — read before judging any gate

On 19 September 2026 the corpus grew by 98 gold modules and 78 Claude builds: skeleton pairs
**1,956 → 2,349**, compare_structure matched **13,794 → 15,668**, body/defect pages
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
confirmed all 413 pre-existing modules **byte-identical**, and identical bytes cannot produce
different metrics. Reach for the manifest first — it is one command and it settles the question
outright.

**Two consequences for the round log.** Round-over-round deltas from before 19 September are not
comparable with deltas after it: the population is larger and harder, so the same amount of real
work now buys a smaller headline movement. And the §4 plateau test (three consecutive rounds
under 0.02pp) must be read in that light — say so in the entry rather than letting a session
stop on a plateau that is really a denominator change.

## 2. What this loop is authorised to do (Chris, 14 September 2026)

- **Regeneration.** The message that started this session carries the code `REGENERATE CORPUS`
  for every round of the loop, scoped by the OPERATING_GUIDE.md §0a / §0b rules: rebuild every module the
  fix touches PLUS the whole family of the tag or widget type it touches (the working half as
  well as the broken half). A full-corpus regeneration is allowed when a change is corpus-wide
  (skeleton / footer / menu scaffold / acks / tag normalisation) and at the §10a cadence (every
  8 scoped ships, hard stop 16). State the resolved module list and its size in the log before
  each rebuild.
- **Declines.** A class may be DECLINED without asking Chris when the r182 solidify procedure
  says so: the measured share of the corpus that follows the candidate rule is below 0.60, or it
  is a tie, or there is no derivable discriminator. Record the measurement in the changelog
  entry and in `LOOP_STATE.md` under "Declined classes"; never re-attempt a declined class in
  this loop unless new evidence is named.
- **Git.** Commit `pageforge-site` at the end of every shipped round (OPERATING_GUIDE.md §16). NEVER push
  and NEVER `git checkout` / `git restore` a file without proving it is committed. The final
  report gives Chris the copy-and-paste push block.
- **Not authorised:** editing anything under `01-Finalized_Modules_` (the human gold is
  read-only, forever); reading the gold as a converter INPUT (Level 0 guardrail); any per-module
  `if (code === …)` special case (DATA OVER CODE); disabling a new rule to silence a verifier
  (§0a: debug until both populations build).
- **The 20 modules with no Claude build are NOT converter faults — do not "fix" them by
  inventing a source.** 12 XOTP modules (`XOTPB08–13`, `XOTPG01`, `XOTPG03–06`, `XOTPO01`) are
  refused because their Writers Templates are an activity-table dialect with no red tags — that
  is a recognition round with a written spec
  (`00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`), not a defect. Seven
  (`GER1003–1007`, `SAM1005`, `SAM1006`) **have no Writers Template at all**; nothing the
  converter can do will ever build them, and chasing them is wasted work. One (`PMT101`) is a
  real recognition gap: its content is entirely inside table cells, so the paragraph-level
  opener test refuses it. Their empty Claude dirs were deliberately removed so no ghost
  directory skews pairing (the r285 trap) — **do not recreate them.**
- **The subject labels are PROPOSED, not final.** `data/Subject_Prefix_Map.json` (round 408)
  assigns a subject to 30 module-code prefixes that had no learning-area folder. Chris has not
  yet approved the Languages split (CHI/GER/JPN/SAM/SPA under NCEA1 vs a single Languages
  label). Treat the labels as a grouping convenience; **do not build a rule that depends on one
  being correct**, and do not re-litigate them — they are one data edit plus a registry
  re-merge when he decides.
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
   corpus), then the NOT CAPTURED rows of `KB_AMALGAMATION_STATUS.md`, then
   `python3 reference/tests/_coverage_dashboard.py` / the `STOCKTAKE__Track.md` backlog.
   Choose the top candidate: chrome regions before body, KB rows first within an area (§1c),
   then the largest derivable population, skipping anything listed under "Declined classes"
   in `LOOP_STATE.md`. **KB-FIRST CHECK before committing to a
   gold-matching class:** search the KB for a rule covering the element; if one exists, the
   KB rule is the target, not the gold. Write the choice, its measured size per template and
   subject group, and its authority source (§1b, 1–4) to `LOOP_STATE.md` FIRST.
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
3. **MEASURE corpus-wide before coding** (§5 step 2) with a probe in `outputs/` that scans ALL
   Writers Templates — remember the §16 trap: a filter on `/media list/` hides the 286 combined
   `Writers Template + Media List.docx` files. Report the share PER template family and subject
   family, not just the total (§1b). Classify: A1 / A2 / B-i / B-ii / C. Only B and C
   (instructions) are actionable. If the share is < 0.60 or tied in every group → DECLINE (§2),
   log it, go to 1. If it holds in some groups only, scope the fix to those groups (a data
   flag keyed by template/subject — `Template_Modes.json` / `Subject_Global_Parameters.json`
   are the precedents), never a corpus-wide rule.
4. **IMPLEMENT** behind a data flag in `data/*.json` AND an env toggle `<NAME>_OFF`. Edit data
   files with the Edit tool only (they are tab-indented; never `json.dumps` them).
5. **REBUILD** the affected set + the tag/type family (§0a/§0b), via `_batch_plan.py` and
   `_regen_safe.sh`, one batch per command. There is no 45-second wall in Claude Code, but keep
   each command under ~10 minutes and write progress to a file so nothing is lost.
   Prove freshness: `python3 _content_manifest.py fresh --affected <list>` → 0 truly stale.
6. **PROVE** with `_ab.py <TOGGLE>_OFF=1 <codes>` (the toggle-OFF corpus must be byte-identical
   on every untouched module), then the gates: `bash run_all_gates.sh`, plus the verifier of any
   widget touched, over its WHOLE family. Every gate holds-or-improves, `pairs skipped (parse
   error)` is 0, all selftests green.
   - If a gate regresses: **debug, never revert** (§0a). Up to **three** repair attempts inside
     the round. After the third failure, toggle the round OFF, prove byte-identity with the
     pre-round corpus, record the class as "BLOCKED — needs Chris" in `LOOP_STATE.md` with the
     evidence, and move to the next class. Blocked is not the same as declined.
7. **FINALISE** (§12): prepend the `BUILD_CHANGELOG.md` entry, bump `Config.js AppVersion`,
   update `OPERATING_GUIDE.md` §14 if a baseline or toggle changed, refresh `gate_baseline.json` and the
   feature index (`build_feature_index.cjs`) after any regeneration, `git add` + `git commit` in
   `pageforge-site`. Then append the round's one-line result to `LOOP_STATE.md`
   ("r314 · class X · shipped/declined/blocked · scaffold 49.94→50.02 · pages moved N").

Never chain a skeleton score from a state file that a scoped regeneration has left stale (§16):
refresh the state after every scoped regen, and run a fresh full score when one fits.

## 4. When to stop (any one of these ends the loop)

- **Exhaustion.** ALL of: `DIFF_QUEUE.md` exists, was produced by the §1d miner on the CURRENT
  corpus, and has no candidate row left (chrome floor 10 modules, body floor 20 pages, each
  judged per template/subject group); `KB_AMALGAMATION_STATUS.md` has no NOT CAPTURED row
  left with ≥ 20 in-scope pages; and the dashboard backlog has no derivable class ≥ 20 pages.
  **Any exhaustion verdict reached before 19 September 2026 is VOID**, for the same reason the
  sessions 15–18 verdicts are: the corpus gained 98 modules and 24 family bases the queue had
  never seen, and re-mining on 19 Sept moved it 168 → 188 candidate rows (183 after round 408).
  Exhaustion may only be declared on a miner run over the POST-intake corpus.
  Everything remaining is class C (editorial) or is in "Declined classes". This is the GOOD
  ending — but it may only be declared with the miner's output quoted in the report. The
  session 15–18 verdicts, reached without the miner, do not count.
- **Plateau.** Three consecutive shipped rounds each move the skeleton SCAFFOLD mean by less
  than 0.02 percentage points AND move no other protected gate. Stop and report — the next lever
  needs a human decision, not another round.
- **Budget.** The round cap Chris set in the starting message (default: 10 rounds per session)
  is reached, or the session has run for the time cap he set (default: 6 hours).
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
  every candidate) and the top-25 candidate details here (≈120 KB); everything else goes to
  `CONVERTER_V2/outputs/_diff_queue_details.md` (≈600 KB), which is NEVER read whole — grep a rank.
- A STOPPED entry ≤ 1,500 characters. A Round-log line ≤ 500. A "Next session starts with" line
  ≤ 800. A Decisions-from-Chris block records the decision, not the conversation.
- **No file over 100 KB is ever read whole**, by anyone, for any reason: `wc -c` first; if large,
  `grep -n` the headings and `sed -n` the range you need. `cat` of a `.json` in `outputs/` is banned
  (the miner's JSON is 41 MB); use `python3 -c` to pull the one key you need.
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
- Never run a single command longer than ~10 minutes; batch the corpus.
- Write `LOOP_STATE.md` before and after every round; a new session resumes from it.
- Commit after every round, so a crash loses at most one round.
- Keep console output small: write big results to files under `CONVERTER_V2/outputs/` and print
  the summary line only.
- **Context diet (added 14 Sept 2026 after the first run filled 1M of context in an hour).**
  `OPERATING_GUIDE.md` (the converter guide — it WAS `CLAUDE.md` until 21 Sept 2026, when its 1.3 MB was found to be auto-loaded into context after every compaction, thrashing the loop; the real `CLAUDE.md` is now a 4 KB pointer) is ~1.3 MB and `BUILD_CHANGELOG.md` ~2 MB — never read either whole. Read
  OPERATING_GUIDE.md §0–§6, §9, §10, §12, §16 by line range (grep the `## ` headings first) and only the
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
  audits KB drift, progress, rule quality, gate health and session mechanics, writes
  `LOOP_REVIEW__<date>.md`, proposes changes to this file (and the SKILL.md copies) and applies
  only what Chris approves, then appends a "## Loop review <date>" entry to `LOOP_STATE.md`.
- **`/loop-decisions`** — explains every open decision in plain English with real module
  examples (WT → gold → Claude, quoted), writes `DECISIONS__Pending_<date>.md`, and records
  Chris's answers under "## Decisions from Chris" in `LOOP_STATE.md` so the next `/loop-start`
  actions them.

Chris keeps one message and pastes it unchanged into every new Claude Code session on this
folder, whether the previous session ended cleanly, ran out of context, or died in a power
cut. It contains no state — the state is in `LOOP_STATE.md` and git — so it never needs
editing. When a session receives it, the order of work is: health check → read the two files →
reconcile git with the state file → honour recorded decisions → continue. The message text is
kept in this file so it can never be lost:

> Continue the PageForge autonomous loop in this folder. Start with a health check: `git status`
> in pageforge-site, `bash _MIGRATION/verify_after_transfer.sh` (must PASS), delete every stale
> git lock in pageforge-site (`.git/index.lock`, `.git/HEAD.lock`, `.git/next-index-*.lock`,
> `.git/objects/maintenance.lock`, and any `.git/objects/*/tmp_obj_*` — a session that dies or a
> shell without delete rights leaves them, and every commit fails until they are gone), and
> `wc -c LOOP_STATE.md DIFF_QUEUE.md` — LOOP_STATE.md over 100 KB →
> condense/archive per §5d BEFORE anything else (over 160 KB = health check FAILED until fixed);
> never read any file over 100 KB whole (LOOP_STATE_ARCHIVE.md and outputs/_diff_queue_details.md
> are grep-only). Then read LOOP__Autonomous_Rounds.md and LOOP_STATE.md — if LOOP_STATE.md
> does not exist, do Round 0 and Round 0b first. Reconcile git with the state file: any
> uncommitted engine or data files belong to the round LOOP_STATE.md names as in progress — never
> git checkout or git restore them; check them against that round's PICK, finish or toggle OFF,
> and continue from the step the state file shows. Honour every entry under "Decisions from
> Chris" and never re-ask them. THE DIFF MINER (§1d) IS MANDATORY: if
> reference/tests/_diff_miner.py or DIFF_QUEUE.md does not exist, or DIFF_QUEUE.md is older than
> the corpus, do Round 0c FIRST — build/re-run the miner, commit DIFF_QUEUE.md — and take the PICK
> from it (chrome regions first: module-code chip, title, module menu, crumbs/side-nav, footer).
> The "exhaustion" verdicts of sessions 15–18 and any "do not re-measure" note in LOOP_STATE.md
> are VOID — they predate the miner; exhaustion may only be declared with the miner's empty
> queue quoted. This message carries the code REGENERATE CORPUS for every round
> of the loop, scoped by the §0a/§0b family rules in OPERATING_GUIDE.md. Budget for this session: 12
> rounds or 10 hours, whichever comes first. RUN UNINTERRUPTED (§5c): never end your turn to
> wait for gates, regenerations, verifiers or background commands — run them in the foreground
> with a long timeout or poll them until done; never ask me whether to continue; a blocked item
> ends the round, not the session — record it and move to the next class. Follow the §6
> context-diet rules: never read OPERATING_GUIDE.md or BUILD_CHANGELOG.md whole, and after every automatic
> compaction do ONLY the bounded §5d re-read (sections by line range, never a whole file; the
> thrash breaker applies). Update LOOP_STATE.md
> before and after every round and commit after every round, never push. Stop only when §4 says
> so; then give me the §5 plain-English report with the copy-and-paste push block, and end
> LOOP_STATE.md with a "Next session starts with:" line.

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
