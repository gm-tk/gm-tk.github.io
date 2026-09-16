#!/usr/bin/env python3
"""ROUND 353 (loop session 15 Round 3 — the GENERIC members rule, SHIPPED OFF) — finalise: changelog, AppVersion (260619.23 →
260619.24), CLAUDE.md §11 / §14, loop/README.md rows, LOOP_STATE.md (what shipped + position + round log). Idempotent."""
import io, os, json
ROOT = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA"
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = """## 2026-09-17 (round 353, build 260619.24) — THE GENERIC MEMBERS RULE AT THE BUILD SEAM — BUILT, MEASURED ON ALL 416, SHIPPED OFF (`interactive_builders._members_rule.enabled: false`; the corpus is byte-identical to r352 — proven by the flag-off probe 2110 / 2110 and a full regeneration whose manifest diff is IDENTICAL; the autonomous loop's session-15 Round 3)

### 1. WHAT WAS BUILT

**`InteractiveBuilder.#withMembers`, applied after the type dispatch for every built widget except dragAndDrop (its own r351 rule):** `consumed` = the built html's visible text + alt / title attributes + the instruction notes; a member is consumed when its words are there (a short member whole, a longer one by ≥ 0.5 of its 4-word shingles; a table by its sentence rows; a media line / tag by its URL, YouTube id, iStock id or URL slug; a media tag's own words are its reference title; a go-to-journal `[button]` is the caller's `#goJournalTail` business); an un-consumed prose member (a black paragraph, a `[body]` / bracket-less line, the invocation tag's own words, an ignored sentence row of a consumed table) renders through the free-body block emitter before / after the widget by position; prose between consumed members longer than 6 words, a developer cue, a heading, a media member whose URL is not in the build, any other tag, a table the build ignored → the build DECLINES (strict mode, `decline_on_unrenderable: true`) or is left as it was (prose-only mode). Data `Emit_Templates.interactive_builders._members_rule` {enabled, env `WIDGETMEMBERS_OFF`, exclude_types, min_words 3, short_words 6, shingle 4, consumed_ratio 0.5, sentence_row_words 5, heading_tags, media_tags, between_short_skip, between_short_words, decline_on_unrenderable, note_cue_pattern}.

### 2. WHAT THE MEASUREMENT SAID (the 416-module OFF/ON probe, `_r353_probe.cjs`; OFF = disk 2110 / 2110 every time)

- **Strict mode:** 291 pages / 188 modules change; **475 built widgets on 150 pages revert to the hand-off box** (flipCard 149, clickDrop 96, accordion 67, modal 65, dropDown 45, carousel 41, tabs 12) — most for reasons the seam cannot verify one by one: a media URL the builder legitimately transformed, a title a builder drops by its own rule, a same-type sub-tag's short words ("[Modal 2 text] 2. Watch the video."), a channel link riding a video title (BLL210 0.0 #21 — a REAL loss: the carousel dropped the writer's second video). Too many reverts for a corpus a developer is using, and the true losses among them are not separable at this seam (`_r353_wm_debug.log`, `_r353_wm_debug2.log`).
- **Prose-only mode:** 160 pages / 121 modules, 228 `<p>` added, 0 reverts — but **text DUPLICATED on 18 pages** where the consumed test misses a builder's rewrite (HPRE203 5.0: the flipCard's `image filename / back text` rows rendered again as paragraphs, 64 duplicated shingles; CEDO301 6.0; ENFUN01 0.0; XMES103 1.0) and writer notes surfaced as prose ("x 4 slides") — `_r353_probe_classify.log`.
- **Conclusion:** a text-presence test at the seam cannot know what a builder consumed. The rule needs each builder to REPORT the members it used (`bundle._consumedMembers`, a per-builder seam — 2–3 engine rounds), or the losses are closed builder by builder where the shape is exact (the flipCard first-row instruction sentence 41 sites, the modal caption under `[modal]` + `[image]`, the XDLS accordion `[H2] [body] [video]` body). The code stays behind the flag for that day.

### 3. PROOF

- `WIDGETMEMBERS_OFF=1` and `enabled: false` = disk **2110 / 2110** (`_r353_probe_flagoff_0*.log`); a FULL regeneration with the flag OFF → `_content_manifest.py diff` **IDENTICAL (0 pages)**, `_stalecheck.sh` 0 stale. No gate number moves (the corpus is r352's); the gate suite is not re-run for an identical corpus — the r352 numbers stand as the baseline.

**Ledger:** no ship (the corpus is r352's; the ledger counter stays 0) · data `Emit_Templates.interactive_builders._members_rule` (OFF) · env `WIDGETMEMBERS_OFF` · engine `InteractiveBuilder.js` (`#withMembers`, the dispatch seam) · tools `outputs/_r353_probe.cjs` (+ `_r353_probe_run.sh`, `_r353_probe_{off,on,flagoff}_0*.log`), `_r353_probe_classify.log`, `_r353_dupcheck.log`, `_r353_losses_by_type.log`, `_r353_wm_debug{,2}.log`, `_r353_on_changed_{pages,modules}.txt`, `_r353_fullship_par.sh` / `_r353_fullship_run.sh`, `_r353_finalise.py` · AppVersion 260619.24.

"""
if "round 353, build 260619.24" not in s:
    assert s.startswith(head), "changelog head"
    s = head + ENTRY + s[len(head):]
    wr(CL, s); print("changelog: r353 entry prepended")

P = os.path.join(PF, "app", "js", "Config.js"); s = rd(P)
if '"260619.24"' not in s:
    old = '\tstatic AppVersion = "260619.23";'
    assert s.count(old) == 1, "Config anchor"
    s = s.replace(old, '\t// ROUND 353 (260619.24): the generic members rule at the Build seam (#withMembers) — built, measured, SHIPPED OFF (data _members_rule.enabled false); the corpus is byte-identical to r352.\n' + '\tstatic AppVersion = "260619.24";', 1)
    wr(P, s); print("Config.js: 260619.24")

P = os.path.join(PF, "CLAUDE.md"); s = rd(P)
if "| `WIDGETMEMBERS_OFF` | 353 |" not in s:
    OLD11 = "| `CARHEADEND_OFF` / `CARMEMBERS_OFF` | 352 |"
    assert s.count(OLD11) == 1, "§11 anchor"
    NEW11 = ("| `WIDGETMEMBERS_OFF` | 353 | **THE GENERIC MEMBERS RULE (every built widget) — SHIPPED OFF.** `InteractiveBuilder.#withMembers` after the type dispatch (dragAndDrop excluded): consumed = the built html's text + alt/title + notes; an un-consumed prose member renders before / after the widget by position; an un-renderable one declines the build (strict) or is left (prose-only). MEASURED on all 416 and NOT shipped: strict mode reverts 475 widgets on 150 pages (too many unverifiable), prose-only mode duplicates text on 18 pages (a builder's rewrite the seam cannot see). Data `Emit_Templates.interactive_builders._members_rule` — `enabled: false`; the corpus is byte-identical to r352. Next: per-builder consumption reporting (`bundle._consumedMembers`) or builder-by-builder rounds (the flipCard first-row instruction sentence, the modal caption, the XDLS accordion body). |\n"
             "| `CARHEADEND_OFF` / `CARMEMBERS_OFF` | 352 |")
    s = s.replace(OLD11, NEW11, 1)
    OLD14 = "- **Build:** `260619.23` (round 352"
    assert s.count(OLD14) == 1, "§14 anchor"
    NEW14 = ("- **Build:** `260619.24` (round 353 — **the generic members rule at the Build seam, built + measured on all 416, SHIPPED OFF** (`_members_rule.enabled: false`, env `WIDGETMEMBERS_OFF`): strict mode 475 reverts / 150 pages, prose-only mode 18 pages with duplicated text — a text-presence test cannot know what a builder consumed; per-builder consumption reporting is the next design. **The corpus is byte-identical to r352 (flag-off probe 2110/2110; full regeneration IDENTICAL, 0 stale) — every r352 baseline stands.**\n"
             "- **Build:** `260619.23` (round 352")
    s = s.replace(OLD14, NEW14, 1)
    wr(P, s); print("CLAUDE.md: §11 / §14")

P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); s = rd(P)
d = json.loads(s)
if d["_meta"].get("build") != "260619.24":
    d["_meta"]["build"] = "260619.24"; d["_meta"]["round"] = 353
    d["_meta"]["_note_r353"] = "Round 353: the generic members rule SHIPPED OFF — the corpus is byte-identical to r352; every r352 number stands."
    wr(P, json.dumps(d, indent=2, ensure_ascii=False) + "\n"); print("gate_baseline.json: _meta")

P = os.path.join(PF, "loop", "README.md"); s = rd(P)
if "_r353_finalise.py" not in s:
    A = "| `_measure_r352_widgetloss.cjs` / `_r352_wl_run.sh`"
    assert s.count(A) == 1, "README anchor"
    ROWS = ("| `_r353_probe.cjs` / `_r353_probe_run.sh` / `_r353_probe_{off,on,flagoff}_0*.log` / `_r353_probe_classify.log` / `_r353_dupcheck.log` / `_r353_losses_by_type.log` / `_r353_wm_debug{,2}.log` / `_r353_on_changed_{pages,modules}.txt` / `_r353_fullship_par.sh` / `_r353_fullship_run.sh` / `_r353_fullship_regen.log` / `_r353_finalise.py` | `CONVERTER_V2/outputs/` | Session 15 Round 3 (engine r353, SHIPPED OFF) — the generic members rule measured on all 416 in both modes (strict: 475 reverts / 150 pages; prose-only: 228 <p> restored but 18 pages with duplicated text), the flag-off identity probe, the identical full regeneration. |\n")
    s = s.replace(A, ROWS + A, 1)
    wr(P, s); print("README: r353 rows")

P = os.path.join(ROOT, "LOOP_STATE.md"); s = rd(P)
if "## Session 15 · Round 3 (engine r353" not in s:
    A = "## Session 15 · Round 3 PICK (engine r353"
    assert s.count(A) == 1, "LOOP_STATE PICK anchor"
    SHIPPED = """## Session 15 · Round 3 (engine r353 — the generic members rule) — BUILT, MEASURED, SHIPPED OFF (the corpus is byte-identical to r352)
- **Closed 2026-09-17 ≈11:55 NZST (session 15).** AppVersion 260619.24, changelog entry r353, CLAUDE.md §11 / §14, `gate_baseline.json` `_meta` only; `Emit_Templates.interactive_builders._members_rule.enabled: false`; the flag-off probe = disk 2110/2110; a FULL regeneration with the flag off → manifest IDENTICAL, 0 stale. No gate re-run (an identical corpus); every r352 baseline stands. Ship ledger unchanged (counter 0).
- **What the probe measured (`_r353_probe_classify.log`, `_r353_dupcheck.log`, `_r353_wm_debug{,2}.log`):** STRICT mode (an un-renderable un-consumed member declines the build) — 291 pages / 188 modules, **475 built widgets revert to the box on 150 pages** (flipCard 149, clickDrop 96, accordion 67, modal 65, dropDown 45, carousel 41, tabs 12), most for reasons the seam cannot verify (a builder's own transformation of a media URL, a title it drops by rule, a same-type sub-tag's short words) with real losses mixed in (BLL210 0.0 #21's second video, dropped because a channel link rides its title); PROSE-ONLY mode — 160 pages / 121 modules, 228 `<p>` restored, 0 reverts, **but duplicated text on 18 pages** (HPRE203 5.0's flipCard rows rendered again, CEDO301 6.0, ENFUN01 0.0, XMES103 1.0) and writer notes surfaced as prose ("x 4 slides"). Five refinements (media-tag words = reference titles, go-journal buttons, iStock ids / URL slugs, short-between skip, the prose-only mode) did not make it safe: **a text-presence test at the seam cannot know what a builder consumed.**
- **Not BLOCKED on Chris — a design finding.** The next design: each builder REPORTS the members it used (`bundle._consumedMembers` — one seam, ten builders, 2–3 engine rounds), after which the rule is exact; until then the losses are closed builder by builder where the authoring shape is exact: (1) flipCard — the card table's first row is the writer's instruction sentence dropped as a "label row" (41 builds / ≈ 35 pages; CHFUN05 "Click on the card to see examples…"); (2) modal — the caption under `[modal] label` + `[image]` / `[video]` (MXFL101 ×10, BLL1xx); (3) accordion — the XDLS `[accordion] [H2] [body] [video]` body (12); (4) the carousel in-table title row (OSGM301 1.0 = the gold's `<h3>`; 44) and the video carousels' reference titles (80 — mostly the r240 reference-title class, fine to drop; the real losses are videos dropped by the title-link confusion, BLL210). The code stays behind the flag.
- **Lessons for the tools:** (1) a probe classify must check DUPLICATED text as well as lost text — the prose-only mode looked clean by every other number; (2) `const html` in a builder → a reassignment throws "Assignment to constant variable" inside Build's catch and looks like a decline — read the build NOTES (`run.notes`) in every probe, not just the output; (3) the Windows Python heredoc path is unusable for engine patches (tabs / backslashes / `\\u{…}` are mangled) — every engine or data edit goes through a scratchpad script written with the editor and run as a file.

"""
    s = s.replace(A, SHIPPED + A, 1)
    B = "- Remaining KB queue (§D): stickyNav (BLOCKED"
    assert s.count(B) == 1, "position anchor"
    s = s.replace(B, "- Session 15 Round 3 (engine r353 — the generic members rule at the Build seam): **BUILT + MEASURED on all 416, SHIPPED OFF 2026-09-17 ≈11:55 (session 15)** — strict mode reverts 475 widgets / 150 pages, prose-only mode duplicates text on 18 pages; a text-presence test cannot know what a builder consumed → per-builder consumption reporting is the next design; the losses proceed builder by builder. AppVersion 260619.24; the corpus is byte-identical to r352 (probe 2110/2110, full regeneration IDENTICAL); every r352 baseline stands.\n" + B, 1)
    C = "- s15-r2 (engine r352, a built carousel never discards the writer's words)"
    assert s.count(C) == 1, "round log anchor"
    s = s.replace(C, "- s15-r3 (engine r353, the generic members rule at the Build seam) · built + measured on all 416 in two modes (strict: 475 widgets revert on 150 pages; prose-only: 228 <p> restored but duplicated text on 18 pages) · SHIPPED OFF — a text-presence test cannot know what a builder consumed; per-builder consumption reporting is the next design · corpus byte-identical to r352 · no gate moved · commit — see git log\n" + C, 1)
    wr(P, s); print("LOOP_STATE.md: round 3 recorded")
print("finalise done")
