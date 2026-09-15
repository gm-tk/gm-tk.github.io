#!/usr/bin/env python3
"""ROUND 339 (loop session 7, Round 2) — finalise: changelog, AppVersion (260619.09 → 260619.10), CLAUDE.md §9/§11/§14,
gate_baseline.json, KB status D-row, LOOP_STATE.md (what shipped + position + round log + the declined activity `interactive`
modifier). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.102", "51.112", "35.279", "35.287"
GE50_B, GE50_A, GE75, GE90 = 1065, 1066, 201, 15
CS_B, CS_A = 11375, 11378
DELTA = "+0.010"; PCT = "55.8"
MOVED = ("21 moved — 16 up / 5 down, every mover in the affected set, pp-sum +20.26 (HIS1005_9_0 +5.73, HIS1005_5_0 +4.43, HIS1002_1_0 +3.12, "
         "HIS1007_4_1 +1.27 …; HIS1007_1_0 49.48 → 50.17 re-crosses ≥50 — the r338 named crosser HEALED, its `[video link]` buttons are now the gold's "
         "embeds); the 5 dips ≤ 0.85pp are NAMED: MXEX401_5_0 −0.85 and TWHA905_0_0 −0.26 = the gold's editorial video substitutions (the writer's "
         "youtube id is absent from the gold page — MXEX401 one of two, TWHA905 five of eight on its 16-embed single-file page), HIS1005_7_0 −0.33 / "
         "MXFU401_1_0 −0.27 / TWHK903_0_0 −0.02 = the scorer's alignment artefact on a strictly closer element sequence (every embedded id is the "
         "gold's own embed on the paired page)")
ACC = "14 panels / 5 modules, every panel matches the human, defect 0"
VER = ("the PICK's 54 Claude BUTTON sites (of the 109 button-family video blocks) → 0 on the `[button]` emitter; 36 new `videoSection` embeds on the "
       "30 changed pages; the word-loss check (`_r339_wordloss.py`) over the 30: 0 non-video links lost, the only lost words the dropped play-button "
       "labels (\"go to video\" ×23, \"play\" ×7, \"recording\" ×2 …). Corpus-wide, 46 anchored buttons with a video href remain (31 pages / 18 modules, "
       "`_r339_verify_videobtn.py`) — ALL on the `[external link]` / `[external link button]` emitters this class excludes by design (a standalone "
       "`[Link] URL` after a \"watch the video\" sentence — HIS1005_2_0, ENFUN01_0_0, ANZH303 `[Link please clip from 1:42-4:16]`; an embed "
       "instruction with no own URL followed by a `[link] URL` — HIS1006_10_0)")

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-16 (round 339, build 260619.10) — A `[button]` WHOSE DESTINATION IS A VIDEO IS THE EMBEDDED VIDEO, NOT A LINK BUTTON (the gold's consensus 0.90 — the nearest KB rule is 01E `[video]` → `videoSection`; 05D's buttons are internal / external LINKS; the autonomous loop's session-7 Round 2; **SCOPED regeneration of the 14 affected modules — 30 pages; skeleton {DELTA}pp, ≥50 +1, compare_structure exact +3, every other gate EXACT, nothing needed naming; scoped ship #5 since the round-334 full-ship backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**A `[button]`-family item that names a video — its own URL is a YouTube / Vimeo VIDEO url (a watch / shorts / embed / youtu.be id, never a channel), or the next item is a `[video]`-family tag or a bare video-url line carrying one — now ships the standard `videoSection` embed the `[video]` tag has always produced (host, `icon`, title-drop conventions included) instead of an anchored button; a writer's real label that is not play-like ("Go to", "Learning journal") keeps the button, and a label longer than four words renders as body text above the embed — never silently stripped.**

### 2. THE EVIDENCE (docx → human → Claude)

- **HIS1007 lesson 1** — WT `[Button] Play Video` + `[video link] https://www.youtube.com/watch?v=lmRkPXfmCx0` → gold `<div class="videoSection icon ratio ratio-16x9"><iframe … embed/lmRkPXfmCx0 …>` → Claude before `<a href="https://www.youtube.com/watch?v=lmRkPXfmCx0" target="_blank"><div class="externalButton">Play Video</div></a>`; after the gold's embed. The same lesson's `[Please embed this video with a play button and an image of the first scene]` + `[Video link] TED Ed video … https://www.youtube.com/watch?v=3NXC4Q_4JVg` → gold embed → Claude before `externalButton` "Go to video"; after the embed. The page re-crosses the ≥50 line the r338 note had named (49.48 → 50.17).
- **HIS1005 lesson 8** — `[embed this video with an image and play button]` + `[link] https://www.youtube.com/watch?v=…` → gold embed → Claude before a phantom journal button + a To Do note + a link button; after the embed (the "next-tag-url" shape).
- **TWHA905** — `[Button] Love Food Hate Waste` + a youtube url → gold embed → Claude before a labelled button; after the embed with the label rendered as body text (the gold drops it — the r80 title-drop class).
- **The KB:** silent on a button that names a video; 01E `[video]` → `videoSection` is the nearest rule, 05D's buttons are internal / external links. LOOP §1b level 3/4 — the gold's consensus decides (0.90 of the found sites).

### 3. THE MEASUREMENT (`outputs/_measure_r339_videobutton.cjs` → `_r339_videobutton.json` / `.log`, the LIVE extractor over all 454 WTs — every button-family para block carrying a video-host URL, its own or the next block's, paired to the gold by the video id; the shipped rule's own OFF/ON probe `_r339_probe.cjs` over all 416 modules in four shards; the declined candidate `_measure_r339_actinteractive.py` → `_r339_actinteractive.json` / `.log`)

- **109 blocks / 34 modules**; gold EMBED **0.90 of the found sites** (Standard 0.90 n=101 / Inquiry 0.75 n=4 / Fundamentals 1.00 n=4). By shape: A own-URL 21 (0.60), **B next-`[video]`-block 52 (0.98)**, **C next-bare-URL 32 (0.96)**, D next-prose 4 (0.67 — not chased). By bracket: the instruction-like brackets (`[embed this video with … play button]`) 63 (0.96), a real `[button]` tag 46 (0.81). By label: no label 72 (0.95), "Play" / "Play video" 7 (1.00). Gold BUTTON only 8 (TWHK903's iOS / Android tutorial links). Claude before: BUTTON 51 / OTHER 13 / EMBED 33 (the `[video]` path already embedded some).
- **The round's first candidate DECLINED on measurement — the activity `interactive` modifier** (KB 01F / 03A): 4,213 paired activity boxes (same `number=` on the paired page) — gap 758 boxes / 455 pages / 238 modules, but the gold marks a box `interactive` because it BUILT a widget Claude cannot (D&D 212 / mcq 76 / typing 76 / dropQuiz 41 …); on Claude's side those boxes hold plain text (gold-interactive 0.26) or an `unclassified` hand-off (0.49) — no Claude-visible signature reaches the r182 floor; decision 5's population. Recorded in LOOP_STATE "Declined classes".
- On the shipped rule's own trigger (the OFF/ON probe, three refinements in): **30 pages / 14 modules** change, every diff a button (or button + note + link button) → `videoSection` embed — 36 new embeds; `_r339_wordloss.py`: 0 non-video links lost.

### 4. THE FIX — one data block `buttons.video_destination` `{{ enabled, env: "VIDBTN_OFF", host_match, next_tag_families, play_label_match, label_max_words, exclude_released }}` + `ContentConverter.#videoDestination(url, it, bodyItems, i, key, tpl)` + a guard in the r88 following-URL absorb

- At the plain-`[button]` seam (`key === "button"` only; a r307-released item excluded), right after the own-URL resolution: `#videoDestination` classifies the item — **own** (its URL is a VIDEO url — `host_match`: `youtube.com/watch?|shorts/|embed/`, `youtu.be/`, `vimeo.com/<digits>` — a CHANNEL url is not a video; and the url or its hyperlink text sits in the button's OWN text, so a shared-block link elsewhere in the paragraph never claims it — the SSOG301 quiz-control catch); **next-tag** (the next unconsumed item is a `[video]` / `[audio]`-family TAG carrying a video url); **next-tag-url** (the next item is any other non-structural TAG whose text is nothing but a video url — `[link] URL`); **next-url** (a bare video-url black line). The play-likeness of the writer's label (`play_label_match`: play / watch / play the video / go to video / video, or no label) decides: for **next-tag** a play-like button renders NOTHING and the `[video]` item embeds itself (a real label such as "Go to" / "Learning journal" falls through to the normal button path — the MXDI201 / MXFL203 catch); for the other three the button item (or the url-only tag item, consumed) goes through `MediaBuilder.media(…, "video", run)` — the standard `[video]` embed — with the gather FENCED to the button + its url line (`bodyItems.slice(0, i + 2)`) so a following article link is never swallowed as media residue (the rnz-link catch); a label over `label_max_words` renders through `renderBlackText` above the embed.
- The r88 `absorb_following_url` block no longer absorbs a VIDEO url into a `button_linked` form when the rule is on (`noVideoAbsorb`), so a real-label button beside a video line stays a plain button rather than a video-linked one — the rule and the absorb cannot fight.

### 5. THE PROOF AND THE GATES

- OFF/ON in memory over ALL 416 modules (`_r339_probe_off_0*.log` / `_r339_probe_on_0*.log`): **OFF (`VIDBTN_OFF=1`) = disk 2102/2102; ON = exactly 30 pages / 14 modules** (`_r339_affected.txt`; the ON pages saved to `_r339_on/` for the word-loss check). Scoped regeneration in the planner's 3 batches (`_r339_batches_run.sh`, all rc 0; `_r339_regen.log`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = **exactly the 30 pages / 14 modules, 0 added/removed**.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50_B} → {GE50_A} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r339_sk_final.json`, FRESH). {MOVED}. `--accept-named` neither used nor needed.
- Every other gate EXACT or IMPROVED (`_fastloop_diff.py` on the 14: PASS, every protected gate held-or-improved; full suite `_r339_gates.log` RESULT / TOTAL lines identical to r338's): cs exact **{CS_A}** (+3) / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · modal defect 0 · mtkQuiz 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN** (`_r339_selftests.log`). **Widget verifiers over the 14 affected modules:** accordion {ACC}; tabs 6 built / 6 exact / divergence 0; flipCard TOTAL 64 identical ON and OFF (`_r339_verify_flipcard.log` = `_r339_verify_flipcard_OFF.log` — TWHK903's divergence 8 is the r282-named A1 module whose gold carries no flipCard anywhere). **Ceiling:** SCAFFOLD {SK_A}% = **{PCT}% of achievable** (ceiling 91.6%).
- **Verifier:** {VER}.

### 6. NAMED, NOT CHASED

- The gold's editorial video substitutions (MXEX401_5_0, TWHA905 — the writer's id is on no gold page; the writer's video ships). The 8 gold BUTTON sites (TWHK903's iOS / Android tutorial links — writer labels, kept as buttons by the play-likeness rule where the label is real). Shape D (next-prose-with-video-url, 4 sites, 0.67). The 46 video-href anchored buttons on the `[external link]` / `[external link button]` emitters — a separate class ("a standalone `[link]` to a video after a watch instruction is the embed"), measured next. The `[embed …]` instruction with no own url followed by a `[link] URL` (HIS1006) — the same class from the media side.
- Also this round: the activity `interactive` modifier DECLINED on measurement (see §3 and LOOP_STATE "Declined classes"); the super-content class order, the BLL footer `inquiry-nav`, `videoSection.icon` and the Inquiry `body.inquiry` token checked and not chased (the gold's own majority / the KB's class-less form / blocked downstream of the CED briefs).

**Ledger:** scoped ship #5 since the r334 full-ship backstop · data `buttons.video_destination` · env `VIDBTN_OFF` · tools `outputs/_measure_r339_actinteractive.py` (+ `_r339_actinteractive.{{json,log}}`), `_measure_r339_videobutton.cjs` (+ `_r339_videobutton.{{json,log}}`), `_r339_probe.cjs` + `_r339_probe_run.sh` + `_r339_shard_0*`, `_r339_affected.txt`, `_r339_batches_plan.txt` / `_r339_batches_run.sh`, `_r339_wordloss.py`, `_r339_proof.sh`, `_r339_sk_movers.py`, `_r339_dips.py`, `_r339_verify_videobtn.py`, `_r339_finalise.py` · state `outputs/_r339_sk_final.json` (FRESH) · logs `_r339_probe_off_0*.log`, `_r339_probe_on_0*.log`, `_r339_regen.log`, `_r339_fastloop.log`, `_r339_gates.log`, `_r339_sk_full.log`, `_r339_selftests.log`, `_r339_verify_accordion.log`, `_r339_verify_flipcard.log` / `_r339_verify_flipcard_OFF.log`, `_r339_verify_tabs.log`, `_r339_fastloop_commit.log`.

"""
if "round 339, build 260619.10" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.09";\n'
NEW = ('\t// ROUND 339 (2026-09-16, build 260619.10): a [button] whose destination is a VIDEO is the embedded video (the gold\'s\n'
       '\t// consensus 0.90; the nearest KB rule 01E [video] -> videoSection) — ContentConverter.#videoDestination at the plain-[button]\n'
       '\t// seam (own url / next [video] tag / next url-only tag / next bare url line) + the r88 absorb guard; scoped 14 modules;\n'
       '\t// env VIDBTN_OFF.\n'
       '\tstatic AppVersion = "260619.10";\n')
if '"260619.10"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 338 BASELINE (an external destination is the KB's externalButton — 05D + constraint 75; scoped 71 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 339 BASELINE (a [button] whose destination is a video is the embedded video — the gold's consensus 0.90, nearest KB rule 01E; scoped 14 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r339_sk_final.json`, FRESH). r339 {DELTA} ({MOVED}); compare_structure exact {CS_B} → {CS_A}; every other gate EXACT. Older r338 text: **ROUND 338 BASELINE (an external destination is the KB's externalButton — 05D + constraint 75; scoped 71 modules)")
if "ROUND 339 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `VIDBTN_OFF` | 339 | **A `[button]` WHOSE DESTINATION IS A VIDEO IS THE EMBEDDED VIDEO** (the gold's consensus 0.90 of 109 found sites; the nearest KB rule is 01E `[video]` → `videoSection`, 05D's buttons are LINKS; the autonomous loop's session-7 Round 2; **SCOPED regeneration of the 14 affected modules / 30 pages; scoped ship #5 since the r334 full backstop**). Reverts byte-for-byte (OFF in memory = disk 2102/2102). ON (default), `buttons.video_destination`: at the plain-[button] seam (`key === \"button\"`, r307-released items excluded) `ContentConverter.#videoDestination` classifies the item — OWN (its url is a VIDEO url per `host_match` — youtube watch / shorts / embed, youtu.be, vimeo video id; a channel url is not — and the url or its link text sits in the button's own text), NEXT-TAG (the next item is a `[video]` / `[audio]`-family tag with a video url), NEXT-TAG-URL (the next item is a non-structural tag whose text is only a video url — `[link] URL`), NEXT-URL (a bare video-url line). A play-like or absent label (`play_label_match`) on NEXT-TAG renders nothing and lets the `[video]` item embed itself; a real label falls through to the normal button. The other shapes go through `MediaBuilder.media(…, \"video\")` — the standard `[video]` embed — with the gather fenced to the button + its url line; a label over `label_max_words` (4) renders as body text above the embed. The r88 following-url absorb skips a video url while the rule is on. MEASURED (live extractor, all 454 WTs): 109 button-family blocks with a video-host url / 34 modules; gold EMBED 0.90 (shape B next-[video] 0.98 n=52, C next-bare-url 0.96 n=32, A own 0.60 n=21). " + f"Skeleton {DELTA}pp ({MOVED}); cs exact +3; every other gate EXACT; accordion verifier over the 14 {ACC}; tabs 6/6 exact; 13 selftests GREEN. Residue: 46 video-href anchored buttons on the `[external link]` / `[external link button]` emitters (31 pages / 18 modules — a separate class). |\n")
if "| `VIDBTN_OFF` | 339 |" not in m:
    A = "| `EXTDEST_OFF` | 338 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.10` (round 339 — **a `[button]` whose destination is a video is the embedded video** (the gold's consensus 0.90; nearest KB rule 01E `[video]` → `videoSection`; the autonomous loop's session-7 Round 2; **SCOPED regeneration of 14 modules / 30 pages; scoped ship #5 since the r334 full backstop**). **ROUND 339 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r339_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). ≥50 +1 (HIS1007_1_0 49.48 → 50.17 — the r338 named crosser healed); nothing needed naming. cs exact **{CS_A}** (+3) / EXTRA **171** / missing **593**; every other gate EXACT: clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **30 pages / 14 modules changed, 0 added/removed**; toggle `VIDBTN_OFF`; data `buttons.video_destination`. Button-family video sites 54 → 0 (36 new embeds). **Plateau window: r338 {'+0.023'} · r339 {DELTA}.**)\n")
if "- **Build:** `260619.10` (round 339" not in m:
    A = "- **Build:** `260619.09` (round 338 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.10"; d["_meta"]["round"] = 339; d["_meta"]["date"] = "2026-09-16"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75, "pages_ge_90": GE90})
if "compare_structure" in d and isinstance(d["compare_structure"], dict) and "exact_chain" in d["compare_structure"]:
    d["compare_structure"]["exact_chain"] = CS_A
d["_meta"]["_round339_note"] = f"Round 339 (a [button] whose destination is a video is the embedded video — the gold's consensus 0.90, nearest KB rule 01E; scoped 14-module regeneration, scoped ship #5 since the r334 full backstop). Skeleton {SK_B}->{SK_A} ({DELTA}pp; >=50 {GE50_B}->{GE50_A}, >=75 {GE75}, >=90 {GE90}); cs exact {CS_B}->{CS_A}; every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
anchor = "| ~~—~~ | 05D \"Buttons\" Internal/External"
drow = (f"| ~~—~~ | 01E `[video]` → `videoSection` extended to a `[button]` that NAMES a video (own video url / next `[video]` tag / next `[link] URL` / next bare url line — the gold's consensus 0.90 of 109 sites; the KB is silent on the button form) | **SHIPPED round 339** (button-family video sites 54 → 0; 36 new embeds; 30 pages / 14 modules) | 30 pages | {DELTA}pp / ≥50 +1 / cs exact +3, nothing named | `VIDBTN_OFF` | CAPTURED-LIVE (gold consensus, §1b level 3/4) |\n")
if "extended to a `[button]` that NAMES a video" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 7 · Round 2 (engine r339) — what shipped (a [button] whose destination is a video is the embedded video)
- **Fix:** `buttons.video_destination` {{enabled, env VIDBTN_OFF, host_match, next_tag_families, play_label_match, label_max_words,
  exclude_released}} → `ContentConverter.#videoDestination(url, it, bodyItems, i, key, tpl)` at the plain-[button] seam, right after the
  own-URL resolution: OWN (a VIDEO url — youtube watch / shorts / embed, youtu.be, vimeo id; never a channel — in the button's OWN text),
  NEXT-TAG (a `[video]`/`[audio]`-family tag with a video url follows), NEXT-TAG-URL (a non-structural tag whose text is only a video url
  follows — `[link] URL`), NEXT-URL (a bare video-url line follows). A play-like / absent label on NEXT-TAG renders nothing (the `[video]`
  item embeds itself); a real label ("Go to", "Learning journal") keeps the normal button. The other shapes → `MediaBuilder.media(…,
  "video")`, the gather fenced to the button + its url line; a label over 4 words renders as body text above the embed. The r88
  following-url absorb skips a video url while the rule is on.
- **Three refinements the probe forced (all fences, none a revert):** the OWN test (a shared-block link elsewhere in the paragraph turned
  SSOG301's quiz-control / journal buttons into duplicate embeds); a youtube CHANNEL url is not a video (XLP05 `[button] Link` became a
  generic iframe — `host_match` tightened to video-id urls); the media gather fenced (a following rnz article link was swallowed as
  "media residue" — content loss).
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 30 pages / 14 modules
  (`_r339_affected.txt`: ANZH404 HIS1001 HIS1002 HIS1005 HIS1006 HIS1007 HIS1008 HPFUN303 MXEO401 MXEX401 MXFU401 TWHA905 TWHK903
  XGF9006); planner batches (3) all rc 0; 0 truly stale; manifest diff = exactly the 30 / 14. Word-loss over the 30 (`_r339_wordloss.py`):
  0 non-video links lost, only the dropped play-button labels.
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {MOVED}); ≥50 {GE50_B} → {GE50_A}; ≥75 {GE75}; ≥90 {GE90}; RAW {RAW_B} → {RAW_A}; cs exact
  {CS_B} → {CS_A} (+3) / EXTRA 171 / missing 593; every other gate line-for-line EXACT with r338 (fastloop PASS, nothing named; full suite
  `_r339_gates.log`); accordion verifier over the 14: {ACC}; tabs 6/6 exact; flipCard over the 14 identical ON vs OFF (TWHK903's
  divergence 8 = the r282-named A1 module); 13 selftests GREEN. **{PCT}% of achievable.**
- **Verifier:** {VER}.
- **Named:** the gold's editorial video substitutions (MXEX401_5_0, TWHA905); the 8 gold BUTTON sites (TWHK903's tutorial links — real
  labels, kept); shape D (4 sites); the 46 video-href buttons on the `[external link]` / `[external link button]` emitters = THE NEXT
  CANDIDATE CLASS ("a standalone `[link]` to a video after a watch instruction is the embed"; HIS1006's `[embed …]` + `[link] URL` from
  the media side). Ship ledger: scoped #5 since the r334 full backstop (3 of headroom). **Plateau window: r338 +0.023 · r339 {DELTA}.**

""")
ANCHOR = "## Session 7 · Round 2 PICK (engine r339)"
if "## Session 7 · Round 2 (engine r339) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = f"- Session 7 Round 2 (engine r339 — a [button] whose destination is a video is the embedded video; the gold's consensus 0.90, nearest KB rule 01E): SHIPPED 2026-09-16 ≈00:55 (session 7). AppVersion 260619.10, CLAUDE.md §9/§11/§14, KB status D-row (01E extended to the button form), scoped ship #5 since the r334 full backstop. Skeleton {DELTA}pp, ≥50 +1, cs exact +3, every other gate EXACT, nothing named. The activity `interactive` modifier DECLINED on measurement (decision 5's population)." + nl + OLD_P
if "- Session 7 Round 2 (engine r339" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s7-r1 (engine r338)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = f"- s7-r2 (engine r339) · a `[button]` whose destination is a video is the embedded video (the writer's \"[Button] Play video\" + \"[video link] URL\", \"[Button: youtube-url]\", the \"[embed this video with a play button]\" + `[link] URL` instruction brackets → the standard `videoSection` embed instead of an anchored button; a real label keeps the button; the gold embeds 0.90 of 109 sites, nearest KB rule 01E) · SHIPPED 2026-09-16 · scoped regeneration, 30 pages / 14 modules · scaffold {SK_B}→{SK_A} ({DELTA}; {MOVED}), ≥50 +1, cs exact +3, every other gate EXACT, nothing named · button-family video sites 54→0, 36 new embeds · {PCT}% of achievable · scoped ship #5 since the r334 full · the activity `interactive` modifier DECLINED (no Claude-visible signature ≥ 0.60) · commit (see git log)" + nl
if "- s7-r2 (engine r339)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
DECL_ANCHOR = "## Declined classes" + nl
DECL = L("""- **The activity `interactive` modifier (KB 01F `activity` + ID (interactive) → `<div class="activity interactive" number="ID">`; 03A)
  — DECLINED 2026-09-16 (session 7, Round 2 PICK; `outputs/_measure_r339_actinteractive.py` → `_r339_actinteractive.json` / `.log`,
  every gold activity box paired with Claude's box of the SAME number on the paired page).** 4,213 paired boxes: agree-yes 1,208 · agree-no
  1,964 · GAP gold-yes/Claude-no 758 (455 pages / 238 modules) · OVER gold-no/Claude-yes 283 (Claude's own hand-off boxes). The gold marks a box `interactive` because it
  BUILT a task widget Claude cannot (dragAndDrop 212 / mcq 76 / typing 76 / dropQuiz 41 / clickDrop 38 …): on Claude's side the gap boxes
  hold plain text (n=967, gold-interactive share 0.26) or an `unclassified` hand-off with its table (n=474, 0.49); a built videoSection 0.15, carousel 0.11, image 0.22, accordion 0.22 — no Claude-visible signature reaches the r182 floor,
  and the r58/r64 post-pass already marks every box whose widget Claude names. This is decision 5's population (the un-built task widgets);
  the token follows the build. Never re-attempt from the box side.
""")
if "The activity `interactive` modifier (KB 01F" not in s:
    assert s.count(DECL_ANCHOR) == 1, "declined anchor"; s = s.replace(DECL_ANCHOR, DECL_ANCHOR + DECL, 1); print("declined class")
wr(LS, s); print("LOOP_STATE.md written")
