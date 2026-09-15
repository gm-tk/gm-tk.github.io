#!/usr/bin/env python3
"""ROUND 340 (loop session 8, finishing session 7's Round 3) — finalise: changelog, AppVersion (260619.10 → 260619.11), CLAUDE.md
§9/§11/§14, gate_baseline.json, KB status D-row, LOOP_STATE.md (what shipped + position + round log). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.112", "51.112", "35.287", "35.285"
SK_B4, SK_A4 = "51.1124", "51.1120"
GE50, GE75, GE90 = 1066, 201, 15
CS_B, CS_A = 11378, 11379
DELTA = "−0.000"; PCT = "55.8"
MOVED = ("5 moved — 2 up / 3 down, every mover in the affected set, pp-sum −0.64 (at 4 dp 51.1124 → 51.1120 = −0.0003pp, which is 0.000 at the "
         "3-dp precision every round reports; NET OF THE TWO A1-NAMED PAGES BELOW +0.0006pp): HIS1008_7_0 +1.08 and HIS1008_1_0 +0.67 (the gold's "
         "own embeds, in the gold's positions); the 3 dips are NAMED — ANZH303_6_0 −1.41 and HIS1008_5_0 −0.40 = the gold's OWN embed of the SAME "
         "video wrapped in a widget the writer never tagged (ANZH303 a `div.tabs` around `Ez6uNsAONL0`; HIS1008-4.0 a `div.row.carousel` around "
         "`XBMfBVsymUo` + `TLberHUJgHY` under \"[embed the following two videos with images and play buttons]\" — the KB's 04A video-carousel doc "
         "says HOW to build one, not WHEN two videos become one; the gold's other multi-video sites (HIS1008-6.0, four embeds) are plain "
         "videoSections, so the carousel is the human's one-off) — the Decision-Framework A1 exception: the embed is judged right, its container is "
         "the human's widget substitution (decision 5's population); ENFUN01_0_0 −0.58 = the scorer's repeat-collapse artefact (a uniform "
         "`┌ 2× repeated` run of h5 / p / a > div.externalButton / table became a mixed run — +12 skeleton lines — while the new embed is the "
         "gold's own `us6ZcvCcYoo` at gold line 2563)")
ACC = "12 panels / 4 modules, every panel matches the human, defect 0"
VER = ("corpus-wide anchored buttons with a video href (`_r339_verify_videobtn.py`, the r339 standing verifier) **46 → 19**: the 27 url-only sites "
       "now embed (27 new `videoSection`s on the 19 changed pages, 17 phantom \"[video] with no URL found\" red flags gone); the 19 left are 15 "
       "LABELLED video buttons (real writer labels — kept by design: TWHK903's tutorials, MXDI202's titled links, OSBY201 …) + 4 url-only "
       "\"Go to video\" buttons on PROSE paragraphs (TEFUN07, HPRE203, XDLS908 — the fence's own exclusions, gold ANCHOR — and MXFU401's r339-named "
       "site); the word-loss check (`_r340_wordloss.py`, OFF pages vs the regenerated disk) over the 19: 0 non-video links lost, the only lost "
       "words the 27 dropped \"go to video\" labels")

# ---------------------------------------------------------------- 1. BUILD_CHANGELOG.md
CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-16 (round 340, build 260619.11) — A STANDALONE `[link]`-FAMILY PARAGRAPH WHOSE TEXT IS NOTHING BUT A VIDEO URL IS THE EMBEDDED VIDEO (the gold's consensus 0.90 of the url-only sites; the KB is silent on the link form — 01E `[video]` → `videoSection` is the nearest rule, r339's sibling on the `[external link]` emitter; the autonomous loop's session-7 Round 3, finished in session 8; **SCOPED regeneration of the 9 affected modules / 19 pages; scoped ship #6 since the r334 full backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**A `[link]` / `[Link 1]` / `[link video]`-family paragraph whose whole visible text is a single YouTube / Vimeo VIDEO url — a watch / shorts / embed / youtu.be / vimeo-id url, never a channel — now ships the standard `videoSection` embed the `[video]` tag has always produced, instead of the r76 `externalButton` "Go to video"; and a url-less `[video]` / `[embed …]` element followed by such a line takes the line's url and consumes it, so the phantom "[video] with no URL found" red flag + link button pair no longer ships. A link with ANY other visible word in its paragraph (a title, a prose sentence before or after the tag) is untouched.** Data `elements.external_link_video_embed` · env `LINKVID_OFF`.

### 2. THE EVIDENCE (docx → human → Claude)

- **HIS1008 lesson 1** — WT `[embed video with image and play button]` then `[link] https://www.youtube.com/watch?v=l9yY9H3Y49M` → gold `<div class="videoSection icon ratio ratio-16x9"><iframe … embed/l9yY9H3Y49M …>` → Claude before a red "[video] with no URL found" note + `<a href target=_blank><div class="externalButton">Go to video</div></a>`; after the embed (seam B).
- **HIS1005 lesson 2** — "Click on the play button to watch the short video below." + `[Link:] https://www.youtube.com/watch?v=NJ9LJfM4PjM` → gold embed → Claude before `externalButton` "Go to video"; after the embed (seam A).
- **ENFUN01** — "Ricky Baker 'Happy Birthday song' …" + `[Link] https://www.youtube.com/watch?v=us6ZcvCcYoo` → gold embed (line 2563 of the single-file page) → Claude before `externalButton`; after the embed.
- **The KB:** silent on a link that IS a video; 01E `[video]` → `videoSection` is the nearest rule; constraint 75 / 05D govern a link to a website. LOOP §1b level 4 — the gold's consensus decides (0.90 of the url-only found sites).

### 3. THE MEASUREMENT (`outputs/_measure_r340_linkvideo.cjs` → `_r340_linkvideo.json` / `.log`, the LIVE extractor over all 454 WTs — every external-link-family para block carrying a video-id url, paired to the gold by the id; the shipped rule's own OFF/ON probe `_r340_probe.cjs` over all 416 modules)

- **71 blocks / 22 modules**, gold EMBED 0.74 of found — the SHAPE decides: **url-only (0 visible words) 37 blocks / 13 modules → gold EMBED 26 of 29 found = 0.90** (Standard 0.89 n=36 / Fundamentals 1.00 n=1; NCEA1 0.86 / Mathematics 1.00 / English, ANZH, EXPlore, Leaving-to-Learn 1.00 n=1 each; after a media tag with no own url 0.94 n=24, after a watch / play sentence 0.75 n=9, neither 1.00 n=4); **a link with ≥ 4 visible words 0.47** (the gold anchors the phrase inline — `[Link for video] Title` ×13 in one English module) → the titled / prose form is NOT in the class. Gold BUTTON 2 (HIS1005 / HIS1007 "If you want to learn more…" — an optional extra), gold ANCHOR 1.
- On the shipped rule's own trigger: **19 pages / 9 modules** change (ANZH303 ENFUN01 HIS1005 HIS1006 HIS1007 HIS1008 MXDI202 MXFL203 MXFU202), every diff a "Go to video" button (27) and / or a phantom "no URL" note (17) → a `videoSection` embed (27). The PICK's other three modules are NOT reachable by these two seams and are recorded, not chased: EXBP901 and HIS1003 (the url-only `[Link]` is bundled into an `[Interactive] Please embed / clip …` hand-off — a third emitter, 2 sites), XWHA02 ("Link to video" is an unrecognised bare red span, 1 site).
- **The fence the probe forced (a narrowing, not a revert):** the first 416-module probe changed 22 pages / 12 modules — HPRE203_5_0, TEFUN07_0_0 and XDLS908_5_0 were the PROSE form (18–31 visible words BEFORE a trailing `[link] URL`; the gold anchors the phrase inline), reached because `blackAfter` alone (the r76 `!labelText` test) sees only the text AFTER the tag. `MediaBuilder.LinkVideoUrlOnly(it)` now applies the measurement's definition — the item's WHOLE paragraph block minus red spans, urls and `*` is empty — on both seams; the second probe = exactly the 19 / 9.

### 4. THE FIX — one data block `elements.external_link_video_embed` `{{ enabled, env: "LINKVID_OFF", host_match, media_follow }}` + three `MediaBuilder` statics + two seams

- **Seam A — `ContentConverter.#inline`**, before the r76 standalone-button rule: an `[external link]`-family item that is url-only (`!labelText` AND `MediaBuilder.LinkVideoUrlOnly(it)`) whose url matches `host_match` (`youtube.com/(watch?|shorts/|embed/)`, `youtu.be/`, `vimeo.com/<digits>` — falls back to r339's `buttons.video_destination.host_match` so the two rules can never disagree) → `MediaBuilder.media(it, [it], 0, "video", run)` — the standard `[video]` embed, host / icon / title-drop conventions included.
- **Seam B — `MediaBuilder.media`'s following-link source** (the r247 black-line rule extended to the TAGGED line): a `[video]` / `[embed]` element with no url of its own whose next unconsumed item is such a url-only external-link TAG item (`FollowingVideoLinkTag`, walks over consumed items and blank black lines, stops at the first other item) takes that url and marks the item consumed — so the media element embeds and no "no URL" note + button ships. The `[embed]` route in `ContentConverter` peeks the same helper so a url-less embed instruction reaches `media()` instead of printing the note.
- `LinkVideoEmbedOn(tpl)` (flag + env), `LinkVideoHost(tpl)` (the shared regex), `LinkVideoUrlOnly(it)` (the whole-paragraph url-only test). `media_follow: false` in the data switches seam B off on its own.

### 5. THE PROOF AND THE GATES

- OFF/ON in memory over ALL 416 modules (`_r340_probe_off_0*.log` / `_r340_probe_on_0*.log`): **OFF (`LINKVID_OFF=1`) = disk 2102/2102; ON = exactly 19 pages / 9 modules** (`_r340_affected.txt`, `_r340_changed_pages.txt`; the OFF pages saved to `_r340_off/` for the word-loss check). Scoped regeneration in the planner's 3 batches (`_r340_batches_run.sh`, all rc 0, `_r340_regen.log`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = exactly the 19 / 9; the regenerated disk pages == the probe's ON pages on all 88 pages of the 9.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r340_sk_final.json`, FRESH). {MOVED}. The fast-loop's `--accept-named "skeleton SCAFFOLD"` used for the −0.0003pp (the r289 named-movement override; every mover decomposed above and in `_r340_dips.py`).
- Every other gate EXACT or IMPROVED (`_fastloop_diff.py` on the 9; full suite `_r340_gates.log` line-for-line identical to r339's except the two improved lines): cs exact **{CS_A}** (+1) / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard over the 9 identical ON vs OFF (`_r340_verify_flipcard_OFF.log`; ENFUN01's defect 1 = the tracked baseline) · accordion over the 9: {ACC} · tabs 7: exact 3, divergence 4 (developer) · 13 selftests GREEN (`_r340_selftests.log`).
- **Verifier:** {VER}.

### 6. NAMED, NOT CHASED

- The gold's widget substitutions around its own embed (ANZH303's tabs, HIS1008-4.0's carousel — decision 5's population); the scorer's repeat-collapse artefact (ENFUN01). The 3 unreached PICK sites (EXBP901 / HIS1003's `[Interactive]`-bundled link, XWHA02's unrecognised "Link to video") — 3 sites, three shapes, none near the floor. The 15 labelled video buttons (kept by design) and the 4 prose-paragraph "Go to video" buttons (the fence's exclusions).
- **Session 8's health check:** `verify_after_transfer.sh` reported FAIL on 4 engine checksums — every one explained by git (Config.js = the committed r338/r339 AppVersion bumps; the three round-340 files uncommitted since session 7 ended after the IMPLEMENT step at 00:52), no corruption; the manifests are refreshed at this commit (the r316 precedent).

**Ledger:** scoped ship #6 since the r334 full-ship backstop (2 of headroom) · data `elements.external_link_video_embed` · env `LINKVID_OFF` · tools `outputs/_measure_r340_linkvideo.cjs` (+ `_r340_linkvideo.{{json,log}}`), `_r340_probe.cjs` + `_r340_probe_run.sh` + `_r340_shard_0*` + `_r340_probe_{{off,on}}_0*.log`, `_r340_itemdump.cjs`, `_r340_fence_patch.py`, `_r340_batches_{{plan.txt,run.sh}}`, `_r340_regen.log`, `_r340_wordloss.py`, `_r340_proof.sh`, `_r340_fastloop.log`, `_r340_gates.log`, `_r340_sk_final.json` / `_r340_sk_full.log`, `_r340_sk_movers.py`, `_r340_dips.py`, `_r340_selftests.log`, `_r340_verify_{{accordion,flipcard,flipcard_OFF,tabs}}.log`, `_r340_finalise.py` · AppVersion 260619.11.

"""
if "round 340, build 260619.11" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

# ---------------------------------------------------------------- 2. Config.js
CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.10";\n'
NEW = ('\t// ROUND 340 (2026-09-16, build 260619.11): a standalone [link]-family paragraph whose text is nothing but a VIDEO url is\n'
       '\t// the embedded video (the gold\'s consensus 0.90 of the url-only sites; nearest KB rule 01E; r339\'s sibling on the\n'
       '\t// [external link] emitter) — seam A in ContentConverter.#inline + seam B in MediaBuilder.media\'s following-link source\n'
       '\t// (a url-less [video]/[embed] takes the following url-only [link] line); whole-paragraph url-only fence; scoped 9 modules;\n'
       '\t// env LINKVID_OFF.\n'
       '\tstatic AppVersion = "260619.11";\n')
if '"260619.11"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

# ---------------------------------------------------------------- 3. CLAUDE.md §9 / §11 / §14
CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 339 BASELINE (a [button] whose destination is a video is the embedded video — the gold's consensus 0.90, nearest KB rule 01E; scoped 14 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 340 BASELINE (a standalone [link]-family paragraph whose text is nothing but a video url is the embedded video — the gold's consensus 0.90 of the url-only sites, nearest KB rule 01E; scoped 9 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r340_sk_final.json`, FRESH). r340 {DELTA} ({MOVED}); compare_structure exact {CS_B} → {CS_A}; every other gate EXACT. Older r339 text: **ROUND 339 BASELINE (a [button] whose destination is a video is the embedded video — the gold's consensus 0.90, nearest KB rule 01E; scoped 14 modules)")
if "ROUND 340 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `LINKVID_OFF` | 340 | **A STANDALONE `[link]`-FAMILY PARAGRAPH WHOSE TEXT IS NOTHING BUT A VIDEO URL IS THE EMBEDDED VIDEO** (the gold's consensus 0.90 of 29 url-only found sites; the KB is silent on the link form — 01E `[video]` → `videoSection` is the nearest rule; r339's sibling on the `[external link]` emitter; the autonomous loop's session-7 Round 3, finished in session 8; **SCOPED regeneration of the 9 affected modules / 19 pages; scoped ship #6 since the r334 full backstop**). Reverts byte-for-byte (OFF in memory = disk 2102/2102). ON (default), `elements.external_link_video_embed` `{ enabled, env, host_match, media_follow }`: **seam A** — in `ContentConverter.#inline`, before the r76 standalone-button rule, an `[external link]`-family item that is url-only (`!labelText` AND `MediaBuilder.LinkVideoUrlOnly(it)` — the item's WHOLE paragraph block minus red spans / urls / `*` is empty, so a trailing `[link] URL` after a prose sentence stays the r76 button — HPRE203 / TEFUN07 / XDLS908) whose url is a VIDEO url (`host_match`, falls back to r339's `buttons.video_destination.host_match`) → `MediaBuilder.media(it, [it], 0, \"video\", run)`; **seam B** — in `MediaBuilder.media`'s following-link source, a `[video]` / `[embed]` element with no own url whose next unconsumed item is such a url-only external-link TAG item (`FollowingVideoLinkTag`) takes that url and consumes the item — the r247 black-line rule extended to the tagged line — so the phantom \"[video] with no URL found\" note + button pair no longer ships (`media_follow: false` switches seam B off alone). OFF: the r76 `externalButton` \"Go to video\" and the red-flag note return. Measured `outputs/_measure_r340_linkvideo.cjs`; probe `_r340_probe.cjs`. |\n")
if "| `LINKVID_OFF` | 340 |" not in m:
    A = "| `VIDBTN_OFF` | 339 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.11` (round 340 — **a standalone `[link]`-family paragraph whose text is nothing but a video url is the embedded video** (the gold's consensus 0.90 of the url-only sites; nearest KB rule 01E `[video]` → `videoSection`; r339's sibling on the `[external link]` emitter; the autonomous loop's session-7 Round 3, finished in session 8; **SCOPED regeneration of 9 modules / 19 pages; scoped ship #6 since the r334 full backstop**). **ROUND 340 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r340_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). {DELTA}pp at 3 dp ({SK_B4} → {SK_A4}; {MOVED}). cs exact **{CS_A}** (+1) / EXTRA **171** / missing **593**; every other gate EXACT: clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard over the 9 identical ON vs OFF · accordion over the 9 defect 0 · all THIRTEEN selftests GREEN. Video-href buttons corpus-wide 46 → 19 (15 labelled kept by design + 4 prose-fenced). Env `LINKVID_OFF`.\n")
if "- **Build:** `260619.11` (round 340" not in m:
    A = "- **Build:** `260619.10` (round 339 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- 4. gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.11"; d["_meta"]["round"] = 340; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict) and "exact_chain" in d["compare_structure"]:
    d["compare_structure"]["exact_chain"] = CS_A
d["_meta"]["_round340_note"] = (f"Round 340 (a standalone [link]-family paragraph whose text is nothing but a video url is the embedded video — the gold's consensus 0.90 "
    f"of the url-only sites, nearest KB rule 01E; scoped 9-module regeneration, scoped ship #6 since the r334 full backstop). Skeleton {SK_B4}->{SK_A4} "
    f"(−0.0003pp = {DELTA} at 3 dp; net of the two A1-named widget-substitution pages +0.0006pp; >=50 {GE50}, >=75 {GE75}, >=90 {GE90}); cs exact {CS_B}->{CS_A}; every other gate EXACT.")
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- 5. KB_AMALGAMATION_STATUS.md D-row
KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 01E `[video]` → `videoSection` extended to a `[button]` that NAMES a video"
drow = (f"| ~~—~~ | 01E `[video]` → `videoSection` extended to a STANDALONE `[link]`-family paragraph whose text is nothing but a video url (seam A), and a url-less `[video]` / `[embed]` element followed by such a line takes its url (seam B) — the gold's consensus 0.90 of 29 url-only sites; the titled / prose form (≥ 4 words, 0.47) stays the inline anchor / button; the KB is silent on the link form | **SHIPPED round 340** (video-href buttons corpus-wide 46 → 19 — the 19 left are labelled or prose sites kept by design; 27 new embeds; 19 pages / 9 modules) | 19 pages | {DELTA}pp at 3 dp (−0.0003; +0.0006 net of two A1-named widget substitutions) / cs exact +1 / every other gate EXACT | `LINKVID_OFF` | CAPTURED-LIVE (gold consensus, §1b level 4) |\n")
if "extended to a STANDALONE `[link]`-family paragraph" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

# ---------------------------------------------------------------- 6. LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 7 · Round 3 (engine r340) — what shipped (a standalone [link] paragraph that is nothing but a video url is the embedded video) — FINISHED IN SESSION 8
- **Fix:** `elements.external_link_video_embed` {{enabled, env LINKVID_OFF, host_match, media_follow}} + `MediaBuilder.LinkVideoEmbedOn / LinkVideoHost /
  LinkVideoUrlOnly / FollowingVideoLinkTag`. **Seam A** (`ContentConverter.#inline`, before the r76 standalone-button rule): an `[external link]`-
  family item that is url-only — `!labelText` AND the item's WHOLE paragraph block minus red spans / urls / `*` is empty — whose url is a video
  url → `MediaBuilder.media(it, [it], 0, "video", run)`. **Seam B** (`MediaBuilder.media`'s following-link source): a `[video]` / `[embed]`
  element with no own url whose next unconsumed item is such a url-only external-link TAG item takes that url and consumes the item (the r247
  black-line rule extended to the tagged line); the `[embed]` route peeks the same helper so the phantom "[video] with no URL found" note never
  prints. `host_match` falls back to r339's `buttons.video_destination.host_match`.
- **The fence the probe forced (a narrowing, not a revert):** the first 416-module probe changed 22 pages / 12 modules — HPRE203_5_0, TEFUN07_0_0,
  XDLS908_5_0 were the PROSE form (18–31 visible words BEFORE a trailing `[link] URL`; gold ANCHOR), reached because `blackAfter` sees only the
  text after the tag. `LinkVideoUrlOnly` applies the measurement's whole-paragraph `words 0` definition on both seams → the second probe = 19 / 9.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 19 pages / 9 modules
  (`_r340_affected.txt`: ANZH303 ENFUN01 HIS1005 HIS1006 HIS1007 HIS1008 MXDI202 MXFL203 MXFU202); planner batches (3) all rc 0; 0 truly stale;
  manifest diff = exactly the 19 / 9; disk == probe ON on all 88 pages of the 9. Word-loss over the 19 (`_r340_wordloss.py`, OFF vs disk): 0
  non-video links lost, only the 27 dropped "go to video" labels. The PICK's other 3 modules are unreachable by these seams and recorded: EXBP901 /
  HIS1003 (the `[Link]` is bundled into an `[Interactive] Please embed / clip …` hand-off — a third emitter, 2 sites), XWHA02 ("Link to video" is an
  unrecognised bare red span, 1 site).
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp at 3 dp; {MOVED}); ≥50 {GE50}; ≥75 {GE75}; ≥90 {GE90}; RAW {RAW_B} → {RAW_A}; cs exact {CS_B} → {CS_A}
  (+1) / EXTRA 171 / missing 593; every other gate line-for-line EXACT with r339 (full suite `_r340_gates.log`); the fast-loop's
  `--accept-named "skeleton SCAFFOLD"` used for the −0.0003pp (the r289 named-movement override, every mover decomposed — `_r340_dips.py`);
  accordion over the 9: {ACC}; tabs 7 (exact 3, divergence 4 developer); flipCard over the 9 identical ON vs OFF (ENFUN01's defect 1 = the
  tracked baseline); 13 selftests GREEN. **{PCT}% of achievable.**
- **Verifier:** {VER}.
- **Named:** the gold's widget substitutions around its OWN embed (ANZH303's tabs, HIS1008-4.0's carousel — decision 5's population; the KB's
  04A video-carousel doc is a HOW, not a WHEN, and the gold's other multi-video site HIS1008-6.0 is plain videoSections); the scorer's
  repeat-collapse artefact (ENFUN01_0_0); the 3 unreached PICK sites; the 15 labelled video buttons + 4 prose-fenced "Go to video" buttons
  (kept by design). Ship ledger: scoped #6 since the r334 full backstop (2 of headroom). **Plateau window: r338 +0.023 · r339 +0.010 · r340 −0.000
  — two consecutive under-0.02 rounds; a third ends the loop on the plateau rule.**

""")
ANCHOR = "## Session 7 · Round 3 PICK (engine r340)"
if "## Session 7 · Round 3 (engine r340) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 7 Round 3 (engine r340 — a standalone [link] paragraph that is nothing but a video url is the embedded video; the gold's consensus 0.90 of the url-only sites, nearest KB rule 01E; r339's sibling): PICK + code in session 7 (ended after the IMPLEMENT step), "
         f"probe / fence / regeneration / proof / finalise in session 8 — **SHIPPED 2026-09-16 ≈08:45 (session 8)**. AppVersion 260619.11, CLAUDE.md §9/§11/§14, KB status D-row (01E extended to the link form), scoped ship #6 since the r334 full backstop. Skeleton {DELTA}pp at 3 dp (−0.0003; three dips NAMED, +0.0006 net of the two A1 pages), cs exact +1, every other gate EXACT." + nl)
if "- Session 7 Round 3 (engine r340" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P + OLD_P, 1); print("position")
OLD_R = "- s7-r2 (engine r339)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s7-r3 (engine r340, finished in session 8) · a standalone `[link]`-family paragraph whose text is nothing but a video url is the embedded video (the writer's \"[link] https://www.youtube.com/watch?v=…\" on its own line, under an \"[embed video with image and play button]\" instruction or after a \"watch the video\" sentence → the standard `videoSection` embed instead of the r76 \"Go to video\" button, and the url-less `[video]`/`[embed]` element takes the line's url instead of printing a \"no URL\" red flag; a titled or prose link keeps its anchor / button; the gold embeds 0.90 of the url-only sites, nearest KB rule 01E) · SHIPPED 2026-09-16 · scoped regeneration, 19 pages / 9 modules · scaffold {SK_B}→{SK_A} ({DELTA} at 3 dp; {SK_B4}→{SK_A4}; 5 moved — 2 up / 3 down, every mover in the affected set, the 3 dips NAMED: ANZH303_6_0 −1.41 and HIS1008_5_0 −0.40 = the gold's own embed inside a tabs / carousel widget the writer never tagged (A1), ENFUN01_0_0 −0.58 = the repeat-collapse artefact; +0.0006 net of the two A1 pages), ≥50 {GE50} / ≥75 {GE75} / ≥90 {GE90} EXACT, cs exact +1, every other gate EXACT · video-href buttons 46→19 (27 new embeds, 17 phantom notes gone) · {PCT}% of achievable · scoped ship #6 since the r334 full · commit (see git log) · **plateau window: r338 +0.023 · r339 +0.010 · r340 −0.000 (two under 0.02)**" + nl)
if "- s7-r3 (engine r340" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
