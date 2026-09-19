# Loop intake — the 98-module September batch

**Written 19–20 Sept 2026, at the end of the Cowork session that collected, named, placed,
converted and regenerated the batch.** This is the handover into the autonomous loop
(`LOOP__Autonomous_Rounds.md`, state in `LOOP_STATE.md`, artefacts mirrored in
`pageforge-site/converter-v2/loop/`).

Read this once before the next `/loop-start`. The short version: **the corpus grew by about a
quarter, every protected gate was re-proved, the diff queue has been re-mined and is current,
and the loop's own census figures in `LOOP_STATE.md` are now wrong and must be corrected
before anything else.**

---

## 1. The one-minute summary

98 modules that developers had built over the preceding months were collected into the corpus
as human gold, converted by PageForge, and the whole corpus regenerated at build `260619.78`.

- `01-Finalized_Modules_`: **454 → 552** module dirs
- `01-Claude_Modules_`: **416 → 494** module dirs
- paired pages the gates score: **1,956 → 2,349**
- Claude pages: **2,109 → 2,613**
- Writers Template / Media List docx: **619 → 762**, each now with its `_parsed.txt`
- diff-queue CANDIDATE rows: **168 → 188**

**No engine change was made.** No `data/*.json`, no `app/js`, no `Config.js` AppVersion bump.
The full regeneration reproduced all 413 pre-existing modules **byte-identical**, so every
protected gate holds exactly on the population it was measured on.

---

## 2. Correct these numbers in LOOP_STATE.md before the next round

The session-27 start note records a `verify_after_transfer.sh` census of
*"2109 pages / 416 modules / 454 gold dirs / 619 docx"*. All four are now stale, and the
health check at §0 will look like a failure if they are not updated:

| figure | session-27 note | now |
|---|---:|---:|
| Claude pages | 2,109 | **2,613** |
| Claude module dirs | 416 | **494** |
| gold dirs | 454 | **552** |
| docx | 619 | **762** |

Also stale and worth correcting in the same pass:

- **The ship ledger is at FULL #0**, not "scoped #2 since the r405 FULL". A full ship was run
  and recorded on 19 Sept; the scoped counter reset. Fresh headroom of 8 before the next
  backstop is due.
- **The plateau window is 0 of 3** and untouched — no engine round ran, so nothing advanced or
  reset it beyond where r406/r407 left it.
- **The ceiling figure is unmeasured on this corpus.** `LOOP_STATE.md` carries "58.8 % of the
  91.9 % ceiling" from the 1,956-pair corpus. `_measure_ceiling.py` has NOT been re-run over
  the 2,349-pair corpus. Treat the old ceiling as void until it is, and re-run it early — it is
  the denominator every "how much is left" judgement uses.
- **`COVERAGE_DASHBOARD.md` / `_coverage_dashboard.json`** were last built on the r349 corpus.
  They do not know about the 98 modules.

---

## 3. What the loop must do at its next start

### 3.1 The §1d miner check — already satisfied, do not skip re-verifying

§1d requires the miner to be re-run **at the start of every session and after every full
regeneration**. Both applied here, so **the miner has been run and `DIFF_QUEUE.md` is
current**:

```
pairs 2349 / modules 483 / parse errors 0 / diff lines 269,709
classes 8,934  (CANDIDATE 188, below floor 8,463)     19 Sept 20:42
```

Freshness verified the way §1d asks — nothing in `01-Claude_Modules_`,
`01-Finalized_Modules_`, `app/js` or `data/` is newer than the queue (0 / 0 / 0 / 0). The
queue IS this corpus's. **But re-run the check anyway at session start**, because any
regeneration between now and then invalidates it.

### 3.2 Do not read a baseline drop as a regression

This is the single biggest trap the intake introduces, and it will bite every session until
the numbers settle.

`gate_baseline.json` has been re-based to the whole 2,349-pair population, and
`_gatecheck.py` now reports **PASS / HELD on all ten metrics**. But anyone comparing to a
number quoted in an older changelog entry will see rates fall and counts rise, and conclude a
regression that did not happen.

The proof method that settles it, and the one to reuse: **split the gate by population.** The
pre-existing modules reproduce round 407 exactly.

| gate | r407 baseline | live, pre-existing subset | new batch contributes |
|---|---|---|---|
| skeleton mean / ≥50 / ≥75 / ≥90 | 54.084 % / 1181 / 202 / 18 | **identical** | 393 pairs @ 48.409 % (197 / 26 / 1) |
| compare_structure exact / EXTRA / missing / row-wrap | 11779 / 172 / 626 / 23 | **identical** | 1631 / 12 / 59 / 0 |
| body_compare runaway / empty_container | 5 / 170 | **identical** | 1 / 22 |
| literal-[tag] leak occ / pages | 26 / 23 | **identical** | 47 / 21 |
| structurally clean | 2079 / 2102 = 98.91 % | **identical** | 483 / 504 = 95.83 % |

Underneath it: `_content_manifest.py fresh` confirmed all 413 pre-existing modules
byte-identical to the manifest. Identical bytes cannot produce different metrics — the table
just confirms it line by line.

**The new committed baseline** (whole population): skeleton **53.13 %** / ≥50 **1378** /
≥75 **228** / ≥90 **19** / RAW **37.49 %**; cs exact **13410** / EXTRA **184** /
missing **685** / row-wrap **23**; body ANY **250**; defect clean **2562 / 2606 = 98.31 %**,
leak **73 occ / 44 pages**. The population change and this proof are written into
`gate_baseline.json._meta._note_intake_2026_09_19` so a future session cannot misread it.

### 3.3 The corpus mean fell, and that is arithmetic, not decay

Skeleton went 54.084 % → **53.13 %**. The whole −0.95pp is the 393 new pairs entering at
48.409 %. Pre-existing pages did not move by a single hundredth. Any round that now claims
"+0.05pp" is moving a larger, harder population, so **round-over-round deltas from before
19 Sept are not comparable to deltas after it.** Say so in the first changelog entry that
follows.

---

## 4. The influx of discrepancies, measured

Run over the 78 newly-converted modules alone, the miner reports:

```
pairs 393 / modules 78 / parse errors 0 / diff lines 45,365
classes 2,285  (CANDIDATE 43, below floor 2,195)
directions: MISSING 24,914 · EXTRA 15,465 · SUBSTITUTED 3,542 · MOVED 1,444
regions: body 28,131 · activity 13,452 · module-menu 2,743 · footer 336 ·
         root 247 · acks 164 · phases-nav 160 · title 109 · crumbs 23
```

Corpus-wide that lifted the queue from **168 to 188 CANDIDATE rows**.

### 4.1 One family dominates, and two instruments found it independently

**The WJFUN family is the story of this intake.** It surfaced first as a page-count anomaly,
then again — with no prompting — as the best group on seven of the new chrome candidates:

| row | direction | fact | pages | modules | best group |
|---|---|---|---:|---:|---|
| F1 | EXTRA | `header:chip=decimal-number` | 82 | 34 | series=WJFUN c=1.00 n=20 |
| F2 | MISSING | `header:title-h1-count=2` | 86 | 31 | series=WJFUN c=0.62 n=13 |
| F4 | MISSING | `header:chip=module-code` | 31 | 30 | series=WJFUN c=1.00 n=20 |
| F19 | MISSING | `nav:phases` | 36 | 27 | series=WJFUN c=1.00 n=21 |
| F22 | MISSING | `footer:links=home-nav` | 39 | 30 | series=WJFUN c=1.00 n=21 |
| F23 | EXTRA | `footer:links=prev-lesson,home-nav` | 27 | 27 | series=WJFUN c=1.00 n=11 |

The cause is one thing, not six. **21 WJFUN modules plus JPFUN01/02 ship ONE human page each,
and the converter builds 2–5.** Mean SCAFFOLD across them is **10.4 %**, and they now hold 17
of the worst 25 module scores in the entire corpus. Once the converter splits one gold page
into four, every page it invents carries a wrong header chip, no phases nav and the wrong
footer link set — so six chrome classes are six symptoms of one pagination fault.

This is the documented **`page_model: "single-file"`** class (r106 / r186 `MTKPAGE_OFF`) — the
same finding the 3 Aug 2026 intake recorded for CHFUN, which was then fixed. The WJFUN family
simply has no registry entry declaring it. **It is a data-only change**, it clears the largest
single block of new discrepancies, and it is by a wide margin the highest-value next round.

Expect the six chrome rows above to collapse together when it ships. Do not chase them
individually.

### 4.2 The other new candidate classes worth the queue's attention

Body and activity rows, with the population they reach (all structure-only unless noted):

| # | region | dir | context → element | pages | modules | best group |
|---|---|---|---|---:|---:|---|
| 785 | body | EXTRA | `div.col-12.col-md-8` → `p` | 206 | 65 | Standard c=0.90 |
| 786 | body | EXTRA | `div#body` → `div.row` | 225 | 52 | overview c=0.91 |
| 788 | body | MISSING | `div#body` → `div.row` | 224 | 47 | series=PWY10 c=0.77, derivable 0.87 |
| 789 | body | MISSING | `div.col-12.col-md-8` → `p` | 94 | 46 | Fundamentals c=0.76, derivable 0.85 |
| 791 | body | EXTRA | `div.col-12.col-md-8` → `img.img-fluid` | 92 | 41 | Refresh c=0.89 |
| 185 | activity | MISSING | `div.col-12` → `h3` | 90 | 38 | Fundamentals/lesson c=0.63, derivable 0.88 |
| 189 | activity | EXTRA | `div.col-12` → `p` | 59 | 32 | Standard c=0.86 |
| 1 | title | MISSING | `div#header` → `h1>span` | 68 | 33 | overview c=0.83, derivable 0.80 |

The **completeness census** (§1d item 4) also flags two chrome regions:

- **module-menu** — 251 pages carry the region; gold has 1,816 items (1,549 present in the
  Writers Template), Claude renders 1,187; **933 derivable misses across 144 pages / 33
  modules.** Worst: ANZH302, where the gold's 31-item menu renders as 0 on every page.
- **phases-nav** — gold 123 items, Claude 2; **120 derivable misses, 36 pages / 27 modules**,
  all Fundamentals, all WJFUN/FRFUN. This is the same single-file-page-model fault as §4.1.

### 4.3 What the new modules do *not* change

- **`compare_set.txt` is untouched** — 200 entries, unchanged since 13 July, and none of the
  98 appear in it. Anything reading that list behaves exactly as before.
- **No new module is in any verifier's fixed gate set.** tags, flipCard, speechBubble, math,
  menulabels, dragAndDrop, modal and mtkQuiz all run over named module lists, and those lists
  were not extended. Their numbers are therefore directly comparable across the intake — and
  all nine matched baseline exactly. If the loop wants the new modules covered by a verifier,
  that is a deliberate edit to `run_all_gates.sh` and `gate_baseline.json`, not something that
  happened by itself.

---

## 5. The 20 modules that do not convert

78 of the 98 converted. The other 20 produce no Claude output, and **their empty Claude
directories were removed** so no ghost directory can skew the gates' pairing (the r285 trap).
They are gold-only dirs: they raise the gold count to 552 while the Claude count is 494.

| count | modules | cause | loop action |
|---:|---|---|---|
| 12 | XOTPB08–13, XOTPG01, XOTPG03–06, XOTPO01 | a different Writers Template dialect — no red tags at all | needs an input adapter; spec written, see §7 |
| 7 | GER1003–1007, SAM1005, SAM1006 | **no Writers Template exists** | source-collection gap — nothing the converter can do |
| 1 | PMT101 | its content is entirely inside table cells | a real converter gap, diagnosed in §7 |

**Do not treat these as a converter regression** and do not let a session try to "fix" the
seven that have no source document.

---

## 6. Traps this session hit, recorded so the next one does not

1. **`_gatecheck.py` prints stale rows for gates it did not run.** Running
   `_gatecheck.py skeleton defect` still prints compare_structure and body_compare lines —
   from cache. Ours showed exact-chain *down 419* when it was actually *up 1,631*. **Always
   run `cs bc` before believing those two rows.** This nearly produced a false regression
   verdict.
2. **`batch_convert` cannot write until file deletion is granted.** It removes each module's
   output folder before rewriting it, so every conversion fails with
   `EPERM: operation not permitted, rmdir …` until the connected folder has delete
   permission. The failure is per-module and easy to mistake for a converter error.
3. **`_regen_safe.sh` hard-coded `timeout 40`.** It now honours **`REGEN_TIMEOUT`**, default 40
   — behaviour unchanged unless set. A shell with a longer wall can use `REGEN_TIMEOUT=150`
   and far bigger batches. The 22-module batches `_batch_plan.py` emits still exceed 150 s;
   11 is a reliable size.
4. **`outputs/parse_docx.cjs` was unrunnable.** It carried absolute paths from a retired
   session. It now resolves its dependencies from `PF_NODE_MODULES` (default
   `$HOME/pfdeps/node_modules`, needing `jszip` and `@xmldom/xmldom`) and its JS directory from
   its own location. Proven byte-identical 5/5 against existing corpus `_parsed.txt` before
   use.
5. **A new module with no Claude dir regenerates FLAT.** §10 says it; it is real. The nested
   `01-Claude_Modules_/{Template}/{CODE}` must be pre-created or `corpus.mdir` will not resolve
   it.
6. **`TEMPLATE_DIRS` is hard-coded in two places** — `outputs/_corpus.py` and
   `outputs/corpus.cjs` — as exactly `Standard, Inquiry, Fundamentals, Bilingual`. A fifth
   template folder would be read as a *module named after the folder*, and every module inside
   it would vanish from every gate. This is why the XOTP family went into Standard rather than
   getting its own folder.

---

## 7. Recommended round order

1. **The WJFUN / JPFUN single-file page model.** Data-only registry entry, 23 modules at
   ~10.4 % mean, collapses six chrome candidate rows and the phases-nav completeness miss at
   once. The precedent is the CHFUN fix from the 3 Aug intake. **Start here.**
2. **Re-run `_measure_ceiling.py`** over the 2,349-pair corpus, and regenerate
   `COVERAGE_DASHBOARD.md`. Both are instruments the PICK step depends on and both are stale.
   Cheap, and everything after them is better judged.
3. **PMT101 — the table-only Te Aka Taumatua opener.** `LooksLikeWritersTemplate` requires a
   *paragraph-level* red opener. PMT101 has 450 red bracket runs inside table cells and only 3
   at paragraph level (`[tags]`, `[Content for DROP DOWN MENU]`), so it is refused as "no
   Writers Template". PNR107 (11 paragraph-level, including `[MODULE CONTENT: PAGE 1]`) and
   TRR116 (22, including `[Lesson 2]`) convert fine. Round 212 recorded this family's shape and
   rescued the *trim* step; recognition was never extended. Smallest real fix in the list.
   *Ruled out during diagnosis, so do not re-investigate:* a UTF-8 BOM (30 of the corpus's 762
   docx carry one and convert), and red-hex case (`DocxExtractor` line 1477 already
   lower-cases).
4. **The XOTP activity-table family** — 12 modules. Full spec in
   `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md`. Needs an input adapter, not a new
   engine: every page is plain Standard (`container-fluid`) and every widget it uses already
   exists. Two output-inert rounds (recognition, then the adapter), since nothing else in the
   corpus carries a `Section heading | Text/Activity` table.
5. Then return to the queue's own ranking in `DIFF_QUEUE.md`.

---

## 8. Where everything is

| file | what it holds |
|---|---|
| `NEW_MODULES__Intake_2026-09-19.md` | the intake report in the 3 Aug format — results, gate numbers, findings |
| `00-NEW_NEW_NEW/_INTAKE_AUDIT_2026-09-19.md` | the full audit: what was missing, every rename, the family placement reasoning, the XOTP evidence |
| `00-NEW_NEW_NEW/_SPEC__XOTP_Activity_Table_Template.md` | the XOTP dialect grammar and the conversion spec |
| `00-NEW_NEW_NEW/_KB_RULE__Page_Filename_Tails.md` | the page-filename tail rule, measured, ready for the KB |
| `00-NEW_NEW_NEW/_RENAME_LOG_2026-09-19.tsv` | every file rename, before → after (reversible) |
| `00-NEW_NEW_NEW/_MOVE_LOG_2026-09-19.tsv` | the 98 modules and the template family each went to |
| `DIFF_QUEUE.md` | the re-mined queue — 188 candidates on the current corpus |
| `CONVERTER_V2/outputs/_diff_miner_scoped.{md,json}` | the miner over the 78 new modules alone |
| `CONVERTER_V2/reference/tests/gate_baseline.json` | re-based, with the population-change note |
| `PUSH_INSTRUCTIONS__Corpus_Regen_2026-09-19.md` | the one commit awaiting Chris's push |

---

## 9. Open items that need Chris

1. **One commit is unpushed** — `bb32cfd`, the changelog entry. Clean fast-forward; the machine
   has no saved GitHub credentials, which is the only blocker. Steps in
   `PUSH_INSTRUCTIONS__Corpus_Regen_2026-09-19.md`.
2. **Seven modules have no Writers Template** (GER1003–1007, SAM1005, SAM1006). They need
   collecting before they can ever convert.
3. **XOTPB08 needs its author.** The writer pasted a *picture* of the drag-and-drop activity
   instead of typing it, so 8 of its 12 payload items exist nowhere in the document text. No
   converter can read that.
4. **The five items in the session-26 STOPPED entry still stand** — untouched by this work.
5. **The XOTP family has no Media List at all** (all 12). The reader book supplies the carousel
   images, the picture/sentence matching sentences and the acknowledgement credits, so the
   family cannot convert end-to-end until that is settled.
