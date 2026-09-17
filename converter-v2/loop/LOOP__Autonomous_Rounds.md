# LOOP__Autonomous_Rounds.md — the standing instructions for an unattended PageForge improvement loop

**Who reads this:** a Claude Code session started in `FINAL_MODULE_DATA` (this folder) by Chris.
**What it does:** runs the disciplined round from `CONVERTER_V2/CLAUDE.md` §5 over and over —
pick the largest measured class of mismatch, fix it, rebuild what the fix touches, prove every
protected gate held or improved, write the changelog, commit — and only stops on the rules in §4.
**Written:** 14 September 2026 (after round 313, build 260618.84). This is a STANDING file, not a
kickoff: do not delete it. Update it when the loop's rules change.

---

## 0. Read first, in this order (no exceptions)

1. `CONVERTER_V2/CLAUDE.md` — the operating guide. §0 (regeneration is opt-in — see §2 below for
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

Then run `bash _MIGRATION/verify_after_transfer.sh` once. It must say PASS before anything else
(it checks the five symlinks and the engine checksums). If it fails, stop and report — do not
regenerate anything on a broken tree.

## 1. The measure of success — and the honest ceiling

The scorecard is the existing protected-gate set (CLAUDE.md §9): the skeleton SCAFFOLD mean and
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

## 1b. The order of authority — what the converter is trying to match (Chris, 14 September 2026)

The human gold is NOT one uniform target. It spans years, several template systems, many
subjects and levels, and it contains mistakes. The target for any element is decided in this
order; the first source that has a rule for the element wins:

1. **The knowledge base (§0 item 4).** A front-facing CL decision, a `00_MASTER_INSTRUCTIONS`
   constraint, or a `14_SUBJECT_GLOBAL_PARAMETERS` family rule that covers the element, within
   its stated scope (subject / template / level / series). This outranks the module's own gold
   — the gold predates the rule. This generalises the recorded doc-14 exception in CLAUDE.md §6
   (`Subject_Global_Parameters.json` `overrides_gold`) to the whole KB.
2. **The previously-developed sibling.** The specific earlier module of the same series and
   template (`Module_Structure_Index.json` `module_meta`: subject / template_type / phase /
   series / dev_order; `Precedence_Cascade.json` levels 2–5). A module inherits its sibling's
   structure unless the KB or its own gold says otherwise.
3. **This module's own gold** (CLAUDE.md §6 Level 0) — for everything 1 and 2 are silent on.
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

## 2. What this loop is authorised to do (Chris, 14 September 2026)

- **Regeneration.** The message that started this session carries the code `REGENERATE CORPUS`
  for every round of the loop, scoped by the CLAUDE.md §0a / §0b rules: rebuild every module the
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
- **Git.** Commit `pageforge-site` at the end of every shipped round (CLAUDE.md §16). NEVER push
  and NEVER `git checkout` / `git restore` a file without proving it is committed. The final
  report gives Chris the copy-and-paste push block.
- **Not authorised:** editing anything under `01-Finalized_Modules_` (the human gold is
  read-only, forever); reading the gold as a converter INPUT (Level 0 guardrail); any per-module
  `if (code === …)` special case (DATA OVER CODE); disabling a new rule to silence a verifier
  (§0a: debug until both populations build).

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
   update `CLAUDE.md` §14 if a baseline or toggle changed, refresh `gate_baseline.json` and the
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

## 6. Anti-timeout discipline (why this runs in Claude Code, not Cowork)

- Claude Code runs on Chris's computer with no 45-second command wall and no folder-mount bug.
- Never run a single command longer than ~10 minutes; batch the corpus.
- Write `LOOP_STATE.md` before and after every round; a new session resumes from it.
- Commit after every round, so a crash loses at most one round.
- Keep console output small: write big results to files under `CONVERTER_V2/outputs/` and print
  the summary line only.
- **Context diet (added 14 Sept 2026 after the first run filled 1M of context in an hour).**
  `CLAUDE.md` is ~970 KB and `BUILD_CHANGELOG.md` ~2 MB — never read either whole. Read
  CLAUDE.md §0–§6, §9, §10, §12, §16 by line range (grep the `## ` headings first) and only the
  top 3–4 changelog entries. Read gold/Claude pages with `grep`/`sed -n` ranges, never whole
  files. Prefer `head`/`wc`/counts over dumping lists. **After every automatic context
  compaction, the FIRST action is to re-read this file and `LOOP_STATE.md`** — the compaction
  summary keeps the gist but not the rules, and the rules are what keep the loop honest.

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
> in pageforge-site, `bash _MIGRATION/verify_after_transfer.sh` (must PASS), and delete any stale
> `.git/index.lock`. Then read LOOP__Autonomous_Rounds.md and LOOP_STATE.md — if LOOP_STATE.md
> does not exist, do Round 0 and Round 0b first. Reconcile git with the state file: any
> uncommitted engine or data files belong to the round LOOP_STATE.md names as in progress — never
> git checkout or git restore them; check them against that round's PICK, finish or toggle OFF,
> and continue from the step the state file shows. Honour every entry under "Decisions from
> Chris" and never re-ask them. This message carries the code REGENERATE CORPUS for every round
> of the loop, scoped by the §0a/§0b family rules in CLAUDE.md. Budget for this session: 12
> rounds or 10 hours, whichever comes first. RUN UNINTERRUPTED (§5c): never end your turn to
> wait for gates, regenerations, verifiers or background commands — run them in the foreground
> with a long timeout or poll them until done; never ask me whether to continue; a blocked item
> ends the round, not the session — record it and move to the next class. Follow the §6
> context-diet rules: never read CLAUDE.md or BUILD_CHANGELOG.md whole, and after every automatic
> compaction re-read the loop file and LOOP_STATE.md before anything else. Update LOOP_STATE.md
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
