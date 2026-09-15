#!/usr/bin/env python3
"""Session 8 — the Round 2 PICK record (no class reached the floor), the new BLOCKED item (KB c23 lesson-menu label form), the
EXHAUSTION stop banner, the round-log line and the 'Next session starts with:' line. Idempotent; CRLF kept."""
import io, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md")
s = io.open(LS, encoding="utf-8", newline="").read(); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)

PICK = L("""## Session 8 · Round 2 PICK (would have been engine r341) — written 2026-09-16 09:10–10:05 NZST — NO CLASS REACHED THE FLOOR → the loop stops on §4 EXHAUSTION
- **The queue after r340:** the r336 substitution instrument (`_r340_subst.log`, unchanged by r340 except the 27 embeds), the KB queue §D
  (every remaining ≥ 20-page row is BLOCKED — stickyNav, c23 (new, below) — or DECLINED — c47/c95, c67 — or an un-built widget builder —
  rows 26 D&D / 46 labelled diagrams / 48 typing = decision 5), the skeleton gap tallies re-run (`_measure_r334_skelgaps.py` → `_r341_skelgaps.log`:
  the top missing / extra lines are the generic p / div.row / WIDGET / img noise of the content-start and un-built-widget gaps, not classes), and
  FIVE fresh measurements of the rows not yet explicitly settled:
- **(1) `ul ⇐ ol` (gold bullets where Claude numbers; 34 sites / 25 pages / 14 modules — `_r341_ulol_sites.py`, `_r341_ulol_source.cjs`,
  `_measure_r341_numlists.cjs` → `_r341_numlists.log`):** 31 of 33 located sites are the writer's WORD-NUMBERED list (`w:numFmt` decimal) and 2
  are typed digits (r337) — KB constraint 42 (Universal: numbered steps / sub-questions → semantic `<ol>`) makes Claude KB-CORRECT. Corpus-wide the
  gold agrees: 2,530 Word-numbered lists in 330 WTs → gold `ol` **0.84** of found (Standard 0.87, Fundamentals 0.79, Inquiry 0.84). The only
  context that flips is the learning-intention list (gold `ul` 24 of 37 found, 0.35 ol) and ALL 24 `ul`s are ONE series — AGH1001 / AGH1004 /
  AGH1005 (NCEA1; every other subject numbers its LI lists 1.00) — the §1b human outlier at 13 pages, under the floor. NOT a class; recorded.
- **(2) `h5 ⇐ p` (gold h5 where Claude p; 32 sites / 31 pages / 14 modules — `_r341_h5p_sites.py`):** every site is the LESSON-MENU LABEL
  ("We are learning about/to…", "We are learning:", "You will show your understanding by…") that the r117 exact-fold phrase list misses. KB
  constraint 23 / 01B: lesson-page module-menu labels are `<h5>`, the writer's wording normalised to the canonical label. Measured INSIDE
  `#module-menu-content` on every paired lesson page (`_measure_r341_menulabels.py` → `_r341_menulabels.{json,log}`, void-aware parser): 1,491
  Claude labels / 690 pages; Claude `<h5>` 1,257 → gold h5 0.71; **Claude `<p>` 206 labels / 176 pages / 42 modules → gold h5 59 / p 80 / h3 24 /
  absent 39 = h5 0.35 of found** — split BY SERIES: NCEA1 0.95 (18/19), English 0.36 (h5 27 / h3 24 / p 22 — a three-way per-module split:
  ENGI h3-span, ENGJ301 / ENGS401 p, ENGJ402 / 403 h5), Mathematics 0.06, ConnectED 0.20, Online Safety 0.00 (the "Ākonga will…" lead-in
  SENTENCE = KB constraint 70's own `<p>` exception — Claude right), Leaving to Learn 0.00. The one variant that solidifies — the writer's
  "We are learning about/to…" (fold `we are learning about to`, 29 pages / 10 modules, gold h5 0.69) — is **17 pages once the r81 eng-family
  menus (skipped by `skip_named_promotion`; their gold is h3 / p) are removed** (AGH1002 6, AGH1003 8, PES1007, MXDI301, MXEO201) — under the
  floor. Applying c23 to the whole residue would be a KB-over-gold override on 80 gold-`p` pages for 59 gold-h5 pages (a wash the loop does
  not take unattended) and, read with 01B line 196–197 (the OVERVIEW tab's "We are learning:" / "I can:" labels are `<h5>` too), would also
  overturn the r81 two_col eng-family form on ~296 overview pages where the gold keeps `<p>` at 0.80 → **BLOCKED — needs Chris** (below).
- **(3) The Inquiry `body.inquiry` token (`body.inquiry.container-fluid ⇐ body.container-fluid`, 22 pages / 22 modules):** the gold ships the
  token on every module's crumbs / inquiryPanel landing page and on no plain page (r107's measured invariant re-confirmed: 66 token pages, 62
  with panels; 0 all-no modules); Claude ships it iff it BUILT the panels (25 modules) and 24 Inquiry modules build none — the crumb-less
  dialects (`[tab N]` 11 / `[LESSON N]`-as-panels 5 / `[page N]` 2 / EXPFUN `[section N]` 4 / TWH* 5, each a PanelsBuilder round of 1–14 pages —
  and the CED revision briefs, BLOCKED). Emitting the token without the layout would break the r107 invariant to buy the root skeleton line;
  downstream of the dialect rounds, not a class of its own.
- **(4) The Bilingual audio form (`audio.audioPlayer.icon` EXTRA 148 occ / 32 pages / 14 modules vs the gold's `div.audioImage` 290 occ / 33
  pages / 11 TRR modules + `span.audioTrigger` 216 / 13 / 5 — `_r341_audioforms.py`):** the gold's `audioImage` is a click-the-picture-to-hear
  WIDGET (`audioImageOption` per image — "Click on the vowel and hear its sound"), not a player form; the gold uses the plain `audioPlayer.icon`
  on 20 pages / 12 modules where the writer wants a player. An un-built interactive type = decision 5's population; recorded, not chased.
- **(5) `┌ 2× repeated ⇐ ┌ 3× repeated` (50 occ / 49 pages / 40 Standard modules — `_r341_repeat32.py`):** 27 of 50 are three `<p>` where the
  gold has two (the human merged or dropped a paragraph), 9 `li`, 6 `b`, 3 `td` — the ceiling's editorial rewording (class C), no derivable
  discriminator.
- Also re-checked and unchanged: `div#body.container-fluid` (the gold's BLL17x minority), `div.row.supervisor` 16 pages, `div.alert.solid` 19,
  `li ⇐ b` 17, `img.img-fluid ⇐ p` 15, `div.col-md-8 ⇐ div.col-md-8.col-12` 25 pages / 4 modules (a module quirk), the Fundamentals
  `phaseContainer.justify-content-center` 6 modules and `h2 ⇐ h3` 9 — all under the 20-page floor or already declined; the r314 follow-ups
  (dropbox terminates / release order) were closed in r320 / r326. The doc-14 families stay CAPTURED-INERT (`master_enabled:false`, the
  2026-07-12 policy's "one family at a time via a measured round"; every derivable family convention has been worked as its own constraint).
- **Verdict:** no class with a derivable population ≥ 20 pages remains and no KB row ≥ 20 pages is left that a session can act on without a
  decision from Chris — the §4 EXHAUSTION stop (the GOOD ending). Everything remaining is class C, DECLINED, or BLOCKED on a decision.

""")
ANCHOR = "## Session 7 · Round 3 (engine r340) — what shipped"
if "## Session 8 · Round 2 PICK (would have been engine r341)" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, PICK + ANCHOR, 1); print("PICK section")

BLOCK = L("""- **KB constraint 23 / 01B — the lesson-menu LABEL form (`<h5>` for every "We are learning… / I can: / You will show your understanding by:"
  label, the writer's wording normalised) vs the gold's per-series forms — needs Chris, 2026-09-16 (session 8, Round 2 PICK;
  `outputs/_measure_r341_menulabels.py` → `_r341_menulabels.{json,log}`, measured INSIDE `#module-menu-content` on every paired lesson page).**
  Claude already ships `<h5>` on 1,257 labels (gold h5 0.71); the RESIDUE is 206 `<p>` labels / 176 pages / 42 modules where the r117
  exact-fold phrase list misses the writer's variant or the r81 eng-family skip applies — and there the gold is split BY SERIES: NCEA1 h5 0.95,
  English h5 27 / h3 24 / p 22 (per module), Mathematics p, ConnectED p 20 / h5 5, Leaving to Learn p, Online Safety = the c70 "Ākonga will…"
  lead-in SENTENCE (a `<p>` by the KB's own rule — Claude right). 01B lines 196–197 also make the OVERVIEW tab's "We are learning:" / "I can:"
  labels `<h5>`, which the r81 two_col eng-family rule deliberately keeps `<p>` (gold 0.80 on ~296 overview pages). Decision needed: (a) apply
  c23 everywhere — every lesson-menu label `<h5>` (a named KB-over-gold override on ~80 lesson pages + ~296 overview pages; skeleton ≈ −0.1pp,
  KB-correct), (b) apply c23 to lesson menus only, keeping the r81 overview form (override on ~80 lesson pages for ~60 gains — a wash), (c) leave
  the r117 list + the r81 skip (the gold's per-series forms), adding only the NCEA1-solidified "We are learning about/to…" variant (17 pages —
  under the floor, so recorded here rather than shipped). Recommendation: (c) now; (a) only if Chris confirms the KB's label form is meant to
  overturn the eng-family overview convention the gold carries at 0.80 — that is a design-team call, not a converter inference.
""")
DECL_ANCHOR = "## Blocked classes" + nl
if "KB constraint 23 / 01B — the lesson-menu LABEL form" not in s:
    assert s.count(DECL_ANCHOR) == 1; s = s.replace(DECL_ANCHOR, DECL_ANCHOR + BLOCK, 1); print("blocked entry")

BANNER = L("""## >>> STOPPED 2026-09-16 ≈10:10 NZST (session 8) on the EXHAUSTION rule (§4 — the GOOD ending): after r340 shipped, no class with a derivable population ≥ 20 pages remains and every KB row ≥ 20 pages left is BLOCKED on a decision from Chris (stickyNav, equations, c23 label form, alertPadding, table form, CED briefs, decision 5 interactives) or DECLINED on measurement <<<
- Session 8 shipped ONE round: r340 (finished from session 7's PICK + code) — 19 pages / 9 modules, skeleton −0.000pp at 3 dp (three dips
  NAMED, +0.0006 net of the two A1 pages), cs exact +1, every other gate EXACT; commit 56bb70c. Then the Round 2 PICK measured five candidates
  (below) and none reached the floor. Tree: verify PASS, git clean after the stop commit, manifests refreshed.

""")
S7 = "## >>> STOPPED 2026-09-15 ≈22:40 NZST (session 6)"
if "STOPPED 2026-09-16 ≈10:10 NZST (session 8)" not in s:
    assert s.count(S7) == 1; s = s.replace(S7, BANNER + S7, 1); print("stop banner")

ROUNDLOG = L("""- s8-pick2 (no engine round) · the Round 2 PICK measured five candidates — `ul ⇐ ol` (Claude KB-correct, c42; gold ol 0.84; the AGH LI-list `ul` is one series at 13 pages), the lesson-menu label variants (c23 — gold split by series, h5 0.35 of the residue; BLOCKED for Chris; the one solidified variant is 17 pages), the Inquiry `body.inquiry` token (downstream of the crumb-less dialect rounds), the Bilingual `audioImage` widget (decision 5), the 3-vs-2 `<p>` repeat (editorial) · NOTHING ≥ 20 derivable pages left · **LOOP STOPPED — EXHAUSTION (§4)** · 2026-09-16 ≈10:10
""")
OLD_R = "- s7-r3 (engine r340"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
if "- s8-pick2 (no engine round)" not in s:
    s = s[:j] + ROUNDLOG + s[j:]; print("round log")

# the Next-session line: replace the whole trailing paragraph
k = s.rfind("**Next session starts with:**")
assert k > 0
NEXT = L("""**Next session starts with:** (1) The loop is EXHAUSTED for unattended work — do NOT start a round until Chris answers at least one of the recorded decisions (each is under "Blocked classes" with its measurement, options and a recommendation; none is re-asked in the session, the answer is recorded under "Decisions from Chris" first): (a) the EQUATION FORM (329 Word equations dropped; MathML per the gold + the V1.5 finding vs LaTeX per KB 05A — recommendation MathML), (b) stickyNav (KB families only vs every ≥ 0.60 series vs keep the ban — recommendation KB families only), (c) decision 5 — the interactive builds (the corpus's largest class by far: D&D 292 modules, typing 283 gold pages, the TRR `audioImage` click-to-hear widget, labelled diagrams…), (d) NEW — KB constraint 23's lesson-menu label form (`<h5>` everywhere vs the gold's per-series forms; recommendation (c) leave, see the entry), (e) the `alertPadding` activity class (recommendation: leave plain), (f) the KB table form 05D vs 06 §6, (g) the CED revision-brief modules, (h) decision 4 (Standard title-pair order), (i) decision 1 (c47). (2) With a "yes" to any of them the round recipe is unchanged: PICK written first, live-extractor measure, data flag + env toggle, the 416-module OFF/ON probe (`_r340_probe.cjs` is the template), scoped regeneration, `_r340_proof.sh`, finalise, commit. (3) Housekeeping due regardless: the FULL-SHIP BACKSTOP is due after 2 more scoped ships (ledger: 6 since the r334 full; hard stop at 16) — run it with the first authorised round or on its own if Chris asks. (4) The state of the tree at this stop: HEAD = the session-8 stop commit in `pageforge-site`, working tree clean, `verify_after_transfer.sh` PASS, `_MIGRATION/CHECKSUMS__engine.txt` refreshed at the r340 commit (backup `CHECKSUMS__engine.pre-r340.bak`), corpus == `_content_manifest.txt` (0 pages differ), fast-loop baseline patched at r340 with the named skeleton mover recorded.
""")
s = s[:k] + NEXT
io.open(LS, "w", encoding="utf-8", newline="").write(s); print("LOOP_STATE.md written")
