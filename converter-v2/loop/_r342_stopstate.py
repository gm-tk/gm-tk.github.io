# _r342_stopstate.py — session-9 STOP (Chris's instruction ≈11:05 NZST): write the loop position into LOOP_STATE.md
# (banner, header result, Decisions from Chris, Position, the Round-2 in-progress section, round log, "Next session starts with:").
import io, os, re
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "LOOP_STATE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(P)
NL = "\n" if "\r\n" not in s[:2000] else "\r\n"

# 1. the stop banner, inserted above the session-8 banner
anchor = "## >>> STOPPED 2026-09-16 ≈10:10 NZST (session 8) on the EXHAUSTION rule"
assert s.count(anchor) == 1
banner = (
    "## >>> STOPPED 2026-09-16 ≈11:10 NZST (session 9) on CHRIS'S INSTRUCTION — \"stop the loop at the next logical point\" — after ONE shipped round "
    "(r341, the near-red tag rule, the FULL-regeneration backstop, commit bb56efc); Round 2 (engine r342 — the HYPERLINKED media tag) is built and "
    "part-proven, could NOT be finished and proven inside 10 minutes, so BOTH of its data flags are switched OFF (the engine reproduces the disk corpus "
    "byte-for-byte, 89/89 pages on 12 modules), its four files stay UNCOMMITTED-but-described below <<<" + NL +
    "- Session 9 shipped r341 (76 pages / 10 added / 2 removed across 23 modules; skeleton +0.021pp, ≥50 +7, cs exact +103, clean 97.81 → 98.91%, leak" + NL +
    "  288/46 → 26/23; corpus now 2110 pages). Round 2 (r342) reached PROVE: the OFF leg = disk 2110/2110; the ON leg changed 76 pages / 52 modules and" + NL +
    "  surfaced TWO pre-existing gaps in the hand-off box (one fixed in the same working tree, one measured and left for the next session — see" + NL +
    "  \"Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop\"). Tree: verify PASS (its page-count expectation corrected 2102 → 2110 for the r341" + NL +
    "  corpus; the engine checksum manifest refreshed to the working tree, backup `CHECKSUMS__engine.pre-r342stop.bak`), git = bb56efc + 4 modified files." + NL + NL
)
s = s.replace(anchor, banner + anchor)

# 2. header: the session-9 result sentence
hdr = re.search(r"\*\*Session 9 started:\*\* 2026-09-16 09:21 NZST[^\n]*", s)
assert hdr
line = hdr.group(0)
if "Session 9 result" not in line:
    s = s.replace(line, line + " **Session 9 result: r341 (near-red tag runs, FULL regeneration, +0.021pp; commit bb56efc) · r342 (hyperlinked media tags) built + part-proven, STOPPED by Chris at ≈11:05 NZST with both flags OFF, uncommitted-but-described.**")

# 3. Decisions from Chris (session 9)
dec_anchor = "## Decisions from Chris (session 8 — 2026-09-16; every instruction he gave, in order; the durable record)"
assert s.count(dec_anchor) == 1
dec = (
    "- **2026-09-16 ≈11:05 — \"STOP THE LOOP at the next logical point, without interrupting anything already running.\"** Question: keep going? Answer:" + NL +
    "  let any regeneration / gate / verifier in progress finish, start no new round, class or rebuild; if the current round's remaining steps can be" + NL +
    "  finished and proven in under 10 minutes, finish and commit it — otherwise **switch its toggle OFF so the corpus is back to its last proven state and" + NL +
    "  leave its work uncommitted-but-described**; then record every decision of the session here, update LOOP_STATE with exactly where the loop is" + NL +
    "  (round / class / step / shipped-declined-blocked / anything uncommitted) ending with \"Next session starts with:\", commit everything FINISHED in" + NL +
    "  pageforge-site, give the §5 report with the push block, and confirm it is safe to close. Applied: r342 needed well over 10 minutes (the media" + NL +
    "  embedded-lead gap, the 416-module re-probe, the scoped regeneration, gates, finalise) → both r342 flags OFF, disk identity re-proven, four files" + NL +
    "  left modified and described; r341 was already committed (bb56efc). No answer to any recorded decision — all stay BLOCKED, not re-asked." + NL + NL
)
s = s.replace(dec_anchor, dec + dec_anchor)

# 4. Position line after the r341 line
pos_anchor = re.search(r"- Session 9 Round 1 \(engine r341[^\n]*\n", s)
assert pos_anchor
pos = (
    "- Session 9 Round 2 (engine r342 — a writer's MEDIA tag typed as a HYPERLINK is still a tag: `[audio 1]` linked to its sound file; the r341 seam" + NL +
    "  extended to runs inside a `w:hyperlink` whose bracket head word is a data-listed media word): **IN PROGRESS — STOPPED 2026-09-16 ≈11:05 (Chris)" + NL +
    "  at PROVE, BOTH FLAGS OFF, UNCOMMITTED.** Built: `Input_Doc_Rules.red_runs.hyperlinked_tag_runs` (env HYPERTAG_OFF) + `DocxExtractor.#hyperlinkedTagHead`;" + NL +
    "  `Emit_Templates.interactive_placeholder.embedded_member_text` (env MEMBERTEXT_OFF) + the `embeddedText` helper in `ContentConverter.#interactivePlaceholder`" + NL +
    "  (the fix for the first gap the ON leg exposed). Proven: OFF = disk 2110/2110 (all 416); flags-OFF engine = disk 89/89 on 12 modules. NOT done: the" + NL +
    "  media embedded-lead gap (measured, undecided), the ON re-probe + page-by-page explanation, scoped regeneration, gates, finalise." + NL
)
s = s.replace(pos_anchor.group(0), pos_anchor.group(0) + pos)

# 5. the in-progress section above the Round 2 PICK
pick_anchor = "## Session 9 · Round 2 PICK (engine r342) — written before any code, 2026-09-16 11:05 NZST"
assert s.count(pick_anchor) == 1
sec = (
    "## Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop (Chris ≈11:05 NZST): what was built, what the proof found, what is left" + NL +
    "- **State of the tree:** four files modified and UNCOMMITTED in `pageforge-site/converter-v2` — `data/Input_Doc_Rules.json` (the `hyperlinked_tag_runs`" + NL +
    "  block, **`enabled: false`** at the stop), `app/js/DocxExtractor.js` (`hyperRed` in `#parseParagraph` + `static #hyperlinkedTagHead`), `data/Emit_Templates.json`" + NL +
    "  (the `interactive_placeholder.embedded_member_text` block, **`enabled: false`** at the stop), `app/js/ContentConverter.js` (the `embeddedText` helper wired" + NL +
    "  into `hasText` / `hasRenderedNonInstr` / the member dump of `#interactivePlaceholder`). With both flags OFF the engine reproduces the r341 disk corpus" + NL +
    "  byte-for-byte (`_r342_flagsoff_identity.log`: 89/89 pages on BLL240 BLL150 BLL166 ENGC101 XMES101 XDLS904 XDLS905 HIS1002 BLL220 OSAH501 CEDW501 TRR203)." + NL +
    "  **To resume: flip both `enabled` to `true` (never git checkout these files).** Patch scripts: `_r342_patch_membertext.py` (the ContentConverter + Emit_Templates" + NL +
    "  edit, already applied); the DocxExtractor / Input_Doc_Rules edit was applied in-session (described in the PICK). The r341 checksum manifest was refreshed to" + NL +
    "  this working tree so `verify_after_transfer.sh` PASSES (backup `_MIGRATION/CHECKSUMS__engine.pre-r342stop.bak`); its page-count expectation was corrected" + NL +
    "  2102 → 2110 (the r341 corpus) in the script and `CORPUS_CENSUS.txt`." + NL +
    "- **Step reached:** PICK ✔ · TRIANGULATE ✔ · MEASURE ✔ · IMPLEMENT ✔ · REBUILD (in-memory probe) ✔ · **PROVE — in progress** · FINALISE ✘." + NL +
    "- **The in-memory probe (`_r342_probe_run.sh`, 4 shards, all 416 modules):** OFF (HYPERTAG_OFF) = disk **2110/2110**; ON changed **76 pages / 52 modules**" + NL +
    "  (`_r342_probe_on_0*.log`; output saved under `outputs/_r342_on/` — NOTE that dir predates the member-text fix, so its BLL240 / BLL150 / BLL166 / ENGC101 /" + NL +
    "  XMES101 / XDLS904 pages are the pre-fix form; `outputs/_r342_on2/` holds the post-fix output for those 7 modules)." + NL +
    "- **Gap 1 — FOUND, FIXED (the member-text rule).** BLL240 1.1's `[word drag]` bundle has ONE member: the (now red) `[audio] while, whale, whirl, whole, whine`" + NL +
    "  element with the words on its own bracket line and an empty tail. `#interactivePlaceholder`'s two guards (`hasText` / `hasRenderedNonInstr`) and the member" + NL +
    "  dump read `blackAfter` alone, so the bundle read as notes-only: the box vanished and the writer's word list with it (`_r342_scanstate.cjs` traced it — the" + NL +
    "  bundle IS captured, `consumedBy 3`, members [28, 29, 30]; my first diagnosis, a `bare_invocation_dissolve_empty` dissolve, was wrong — that rule is" + NL +
    "  `types: [\"interactive\"]` only). MEASURED over the whole r341 corpus (`_measure_r342_embedded_members.cjs`, OFF state, `_r342_emb_off_*.json`): **1,555 un-built" + NL +
    "  bundles / 351 modules carry a tag member with bracket-line text the box never dumps; 92 boxes / 55 modules are suppressed outright** — of those the" + NL +
    "  content-ELEMENT/INLINE sub-class is **255 bundles / 124 modules (button 112, image 94, embed 56, audio button 12, external link 12, body 10, audio 9, video 9)" + NL +
    "  with 7 boxes lost from the page today** (BLL150 0.0 + BLL166 1.0 `[audio]` word lists, ENGC101 4.0's five `[image] angry person …` faces, MXEO201 4.0 `[h3]`," + NL +
    "  XWHA02 3.0, EXPFUN04 0.0, HIS1001 10.0) — a PRE-EXISTING class the hyperlink rule made visible (the r293b rule: fixed, not worked around). The fix is scoped" + NL +
    "  to members whose primary directive is ELEMENT / INLINE and whose span is a TAG (an instruction-class member already surfaces as the note before the box;" + NL +
    "  an INTERACTIVE invocation's bracket text is its own spec and lives in the .txt) and renders the raw bracket line (`[audio] while, whale, whirl, whole, whine`)." + NL +
    "  Post-fix (`_r342_on2/`): BLL240 1.1 box back with the words in the dump and the note holding only the writer's real instruction; ENGC101 4.0 gains its 4B" + NL +
    "  dragAndDrop box with the five `[Source image: …]` lines; BLL150 / BLL166 keep their audio word lists; XMES101 2.0 dumps `[Audio animation] Names for each body" + NL +
    "  part …` as one line (was `[Audio animation]` + a note)." + NL +
    "- **Gap 2 — FOUND, MEASURED, NOT DECIDED (the media embedded lead).** `MediaBuilder.media` renders an element's OWN text from `blackAfter` (+ gathered following" + NL +
    "  black) only — the words INSIDE the red span after the tag (the embedded lead, `RenderText(it.text)`) are never rendered, for audio, video and embed alike." + NL +
    "  MEASURED (`_measure_r342_media_embedded.cjs`, `_r342_medemb_summary.log`): free-body media elements with a bracket-line lead the page drops = **359 / 159" + NL +
    "  modules in the r341 corpus (video 136, embed 129, audio 90, audio button 4)** — pre-existing — and **399 / 166 with the hyperlink rule ON; the 40 new ones" + NL +
    "  (23 modules) are audio 31 / audio button 8 / video 1**: the BLL phonics word lists (`[audio] snail, paint, trail, stain, faint, train` → the gold's" + NL +
    "  `audioButton` / player per word list; today the ON output ships a bare `<audio src=\"audio/.mp3\">` and the words are gone), the `[audio button] / j /` sound" + NL +
    "  buttons, and **XDLS903/904/905 0.0's `[Audio Animation N: <sharepoint script doc> Note this will be repeated across five units XDLS 902-6]`** — a CS-produced" + NL +
    "  animation (the r233 / CL-0037 class; the gold ships a Vimeo `videoSection`) that the head word `audio` now routes to the audio ELEMENT: a `.mp3` default" + NL +
    "  player and the writer's note LOST (the OFF page carried the literal `[Audio Animation 1:` + a Writers Note + the link line). Options for the next session," + NL +
    "  in order of preference: (a) fold the embedded lead into the element's `own` text in `MediaBuilder.media` behind a data flag (env e.g. MEDIALEAD_OFF) — the" + NL +
    "  r80 title-drop semantics then apply unchanged (a BUILT video drops it as its title; audio / un-built keep it as the caption `<p>`), which restores every" + NL +
    "  word on the 399 sites; (b) for the `[Audio Animation N:` / `[Audiovisual …]` CS-animation forms, either drop `audio` heads whose bracket carries `animation`" + NL +
    "  from `head_words` (they stay the OFF literal + note) or route them to the r300 kind-todo note (`Designer/Developer To Do: Audio Animation 1 — <link> — note`)," + NL +
    "  the KB-consistent form (05A / CL-0037 declined the vimeo scaffold; the note matches both gold eras). Decide by measuring (a)'s blast over the 359 pre-existing" + NL +
    "  sites (a scoped §0b family regeneration of the audio / video / embed tag families — ~160+ modules — follows either way)." + NL +
    "- **Still to explain from the ON diff (not yet looked at after the fix):** HIS1002 3/5/7/10/11/13/15 (\"anchors removed with nothing added\" — the hyperlinked" + NL +
    "  `[Link: https://www.youtube.com/watch?v=…]` lines now red → the r340 url-only video-link class? verify each), XDLS904 5.0 / XDLS905 4.0 (a `[Image: Learn by" + NL +
    "  Heart icon from LS global edits]` line now inside a box dump), BLL220 0.0, XMES101 2.0 — then the word-loss check (`_r341_quality.py` pattern) over all 76." + NL +
    "- **Remaining steps to ship r342:** flip both flags ON → settle gap 2 → re-run `_r342_probe_run.sh` (OFF must stay 2110/2110; explain every changed page) →" + NL +
    "  word-loss / quality check → scoped regeneration = the ON-changed modules ∪ the §0b family (the audio / video / image / embed / link tag carriers; the ledger" + NL +
    "  is at 0 after the r341 full ship) → `_stalecheck` / `_content_manifest fresh` → gates (`run_all_gates.sh`; skeleton `--json`; `_fastloop_diff.py`; the cs" + NL +
    "  decomposition) → finalise (changelog r342, AppVersion 260619.13, CLAUDE.md §9 / §11 `HYPERTAG_OFF` + `MEMBERTEXT_OFF` (+ the gap-2 toggle) / §14, gate_baseline," + NL +
    "  KB status D-row, guide A4, LOOP_STATE what-shipped + position + round log) → loop mirror → checksum manifest → commit. Three repair attempts on gap 2 is the" + NL +
    "  §3 limit — after that toggle OFF, prove identity, record BLOCKED, move on." + NL + NL
)
s = s.replace(pick_anchor, sec + pick_anchor)

# 6. round log line after s9-r1
rl = re.search(r"- s9-r1 \(engine r341\)[^\n]*\n", s)
assert rl
s = s.replace(rl.group(0), rl.group(0) +
    "- s9-r2 (engine r342 — IN PROGRESS, stopped by Chris ≈11:05) · a writer's media tag typed as a HYPERLINK (`[audio 1]` linked to its Drive / SharePoint sound file) is still a tag — the r341 seam extended to `w:hyperlink` runs whose bracket head word is a data-listed media word (`audio`, `audio button`, `audiovisual`, `av`, `video`, `image`, `embed`, `link` — fenced so the ~230 hyperlinked phonics WORDS `[scissors]` … stay content). Built + OFF-proven (disk 2110/2110); the ON leg (76 pages / 52 modules) exposed two pre-existing hand-off-box gaps: the bracket-line member text the box never dumped (FIXED, `embedded_member_text`, 255 bundles / 124 modules, 7 boxes lost today) and the media element's embedded lead `MediaBuilder.media` never renders (MEASURED 359 pre-existing + 40 new sites, UNDECIDED). Both flags OFF at the stop, four files uncommitted-but-described; skeleton / gates NOT run." + NL)

# 7. Next session starts with
nx = s.rfind("**Next session starts with:**")
assert nx > 0
new_next = (
    "**Next session starts with:** (1) Health check (`verify_after_transfer.sh` — its page count is now 2110), `git status` in pageforge-site: expect HEAD bb56efc" + NL +
    "+ EXACTLY four modified files (`app/js/ContentConverter.js`, `app/js/DocxExtractor.js`, `data/Emit_Templates.json`, `data/Input_Doc_Rules.json`) = Round 2" + NL +
    "(engine r342) in progress — NEVER git checkout / restore them; both data flags are `enabled: false` (the corpus on disk is the proven r341 state)." + NL +
    "(2) Read \"Session 9 · Round 2 (engine r342) — IN PROGRESS at the stop\" + the Round 2 PICK, flip `hyperlinked_tag_runs.enabled` and" + NL +
    "`embedded_member_text.enabled` to `true`, and resume at PROVE: settle gap 2 (the media embedded lead — option (a) `MediaBuilder.media` folds the bracket-line" + NL +
    "words into the element's own text behind a data flag; option (b) for the `[Audio Animation N:` CS-animation sites), re-run `_r342_probe_run.sh` (OFF must" + NL +
    "= disk 2110/2110), explain every ON-changed page, word-loss check, scoped §0b regeneration, gates, finalise, commit — or, after three failed repairs of" + NL +
    "gap 2, toggle OFF, prove identity, record BLOCKED and move on. (3) Then continue the loop under the standing §7 kickoff; the candidates left after r342 are" + NL +
    "recorded in the r342 PICK (plain-black tag brackets 195 / 98 modules — thin; the AGH1006 widget-release leak; the bilingual-cell `[Item N] [Image]` r167" + NL +
    "class) and every KB row ≥ 20 pages stays BLOCKED on Chris's recorded decisions (stickyNav, equations, c23 label form, alertPadding, table form, CED" + NL +
    "briefs, decisions 1 / 4 / 5) — never re-asked. The plateau window after r341 (+0.021pp) is open at one round." + NL
)
s = s[:nx] + new_next
wr(P, s)
print("LOOP_STATE.md updated")
