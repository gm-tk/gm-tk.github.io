#!/usr/bin/env python3
"""ROUND 338 (loop session 7, Round 1) — finalise: changelog, AppVersion (260619.08 → 260619.09), CLAUDE.md §9/§11/§14,
gate_baseline.json, KB status row 75 (+ a D-row), LOOP_STATE.md (what shipped + position + round log). Idempotent; LF kept."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK_B, SK_A, RAW_B, RAW_A = "51.079", "51.102", "35.263", "35.279"
GE50_B, GE50_A, GE75_B, GE75_A, GE90 = 1066, 1065, 200, 201, 15
DELTA = "+0.023"; PCT = "55.8"
MOVED = ("60 moved — 37 up / 23 down, every mover in the affected set, pp-sum +44.21 (XMES201_5_0 +18.96, XGF9003_1_4 +10.81 — crosses ≥75, "
         "AGH1004_2_0 +5.61, HES1007_9_0 +4.85 …); the 23 dips ≤ 5.17pp are NAMED and of two kinds: (a) the 11 gold `button`s on an external host — "
         "the KB-over-gold sites (ANZH404_4_0 −2.92 'Source A/B/C', MXFL401_5_0 −1.18, MXEO201_4_0/_8_0 −0.94/−2.00, ENGC202_5_0 −2.68), (b) the scorer's "
         "repeat-collapse / coincidental-match artefact (HIS1007_3_0 −5.17 and HIS1005_9_0 −1.56 each gain +4 gold-matched lines on the uncollapsed "
         "multiset — a uniform `┌ N× repeated` run of `a > div.button` became a mixed run; HIS1007_1_0 −1.37 crosses <50: its `[video link]`s ship as "
         "buttons the gold embeds, and their `div.button` lines had been matching the gold's journal `div.button`s by coincidence)")
ACC = "162 panels / 27 modules, every panel matches the human, defect 0"
VER = "external-host `div.button` 304 → 41 (the residue = the r73 modal document button + the widget builders' own forms, 18 pages / 13 modules — EXPFUN02/03's istock image modals), external-host `div.externalButton` 230 → 493, gold agreement on the found sites 0.950; the internal-host buttons untouched (docs.google 90 / sharepoint 73 / drive 31 / desire2learn 15 — 0 changed)"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 338, build 260619.09) — AN EXTERNAL DESTINATION IS THE KB'S `externalButton` (KB 05D "Buttons": Internal → `div.button`, External → `div.externalButton`; + constraint 75's default label "Go to website" for a URL-only button; the autonomous loop's session-7 Round 1; **SCOPED regeneration of the 71 affected modules — 134 pages; skeleton {DELTA}pp, ≥75 +1, ≥50 −1 NAMED, every other gate EXACT; scoped ship #4 since the round-334 full-ship backstop**)

### 1. WHAT CHANGED, IN ONE LINE

**A `[button]`-family button whose URL points at an outside website now ships the KB's external form `<a href="URL" target="_blank"><div class="externalButton">…</div></a>` instead of the internal `div.button`, and a URL-only button (`[Button: https://…]`, `[Button – External Link] https://…`) that had no writer label reads "Go to website" ("Go to video" for a video host) instead of falling to the JOURNAL default "Go to your journal" — the destination decides the class (05D), the writer's words decide the label (constraint 75), and Te Kura's own systems (Google Drive / Docs / Forms, the LMS, SharePoint, the vimeo player) stay `button`.**

### 2. THE EVIDENCE (docx → human → Claude)

- **TWHA905 overview** — WT `[Button: https://www.kiwiharvest.org.nz/ ]` → gold `<a href="https://www.kiwiharvest.org.nz/" target="_blank"><div class="button externalButton">Go to Kiwiharvest</div></a>` → Claude before `<a href="https://www.kiwiharvest.org.nz/" target="_blank"><div class="button">Go to your journal</div></a>`; after `<div class="externalButton">Go to website</div>` (the gold's label is editorial — the KB says the resource's name is never the button text).
- **AGH1007 lesson 4** — `[Button – External Link] https://www.lumendigital.co.nz/staging/TheAmazingCow/` → gold `<div class="externalButton">The Amazing Cow: An introduction to ruminant digestive systems</div>` → Claude before `div.button` "Go to your journal"; after `div.externalButton` "Go to website". **HIS1007 lesson 3** — the writer's labelled buttons "US 1776" / "Walkfree" with their hyperlinks → gold `externalButton` → Claude before `div.button`, after `div.externalButton` with the writer's labels kept. **HIS1007 lesson 1** — `[add button] Go to journal` + `[add button] Download journal` (Google Drive / Docs links in the gold) stay `div.button` — the internal list.
- **The KB:** 05D "Buttons" — `<!-- Internal --> <a href="URL" target="_blank"><div class="button">Button text</div></a>` / `<!-- External --> <a href="URL" target="_blank"><div class="externalButton">Button text</div></a>`; constraint 75's label table — a writer's call to action is kept verbatim, a bare URL with no accompanying words reads "Go to website".

### 3. THE MEASUREMENT (`outputs/_measure_r338_extbutton_class.py` → `_r338_extbutton_class.json` / `.log` (before) and `_r338_extbutton_class_AFTER.{{json,log}}`; the two sizing probes `_measure_r338_standalone_links.cjs` → `_r338_standalone_links.{{json,log}}` and `_measure_r338_gold_buttons.cjs` → `_r338_gold_buttons.{{json,log}}`; the shipped rule's own OFF/ON probe `_r338_probe.cjs` over all 416 modules in four shards)

- **The PICK's first candidate did not survive measurement.** The r337 note's "452 untagged hyperlink phrases the human buttoned" was a parsed-text artefact: with the LIVE extractor (`DocxExtractor.Extract` → `run.wtBlocks` → `block.links`), the untagged STANDALONE hyperlink class is 486 phrase + 1,226 bare-URL paragraphs and the gold buttons them at **0.067 / 0.072 of the found sites** — the rest are the writer's asset references (sharepoint / drive / istock / docs) the gold ships as media, or inline `<a>`s; untagged INLINE 0.067 / 0.202. DECLINED (LOOP_STATE). The reverse trace of every gold `externalButton` (873 on 440 pages / 198 modules): HREF-sourced 526, text-only 140, no WT source 207 (class C); the largest HREF-sourced signature is the writer's `[button]`-family tag WITH a URL — which Claude already anchors (r326) as `div.button`.
- **The class that solidifies: the gold decides `button` vs `externalButton` by HOST.** Every gold anchored button by href host: relative paths 592:3, `#` 156:1, drive.google.com 586:1, docs.google.com 92:6, desire2learn 17:8, player.vimeo 6:0 are `button`; youtube 1:24, youtu.be 2:14, earth.google 0:16, sparklers 1:15, teara 3:11, nzhistory 0:11, natlib 0:8, nzonscreen 1:7, stuff 0:7 … every outside website is `externalButton`. Claude's external-host `div.button`s: **304 buttons / 147 pages / 80 modules**; paired to the gold by href (then label): `externalButton` **120** / `button` 11 / on no gold page 173 (the writer's istock / Education Perfect / twinkl asset links the gold never buttons) → **0.916 of the found sites**. Per template: Standard 0.913 (126 pages) / Inquiry 0.909 (13) / Fundamentals 1.000 (8). Per subject family (≥ 6 found): NCEA1 1.000, Leaving to Learn 0.964, 1-10 English 1.000, ConnectED 1.000, 1-10 Social Science 1.000, Te ara Whakapuawa 0.833, 1-10 Mathematics 0.667; ANZH 0.400 on 5 found (its three `button`s are the human's "Source A/B/C" evidence buttons — under any floor). The converse holds: internal hosts docs.google 0 ext / 15 button, sharepoint 1:1, desire2learn 1:4, drive 1:0 (n = 1). The label half: 60 external-host buttons carried the journal default "Go to your journal".
- On the shipped rule's own trigger (the OFF/ON probe): **134 pages / 71 modules** change — 213 lines class-only, 28 class + "Go to website", 24 class + "Go to video"; every changed line is exactly that swap (`_r338_proof.log`-side line check: 0 other differences).

### 4. THE FIX — one data block `buttons.external_destination` `{{ enabled, env: "EXTDEST_OFF", form, internal_hosts, plain_form_match, default_label, video_label, video_host_match }}` + `ContentConverter.#externalDestination(url, key, form, tpl)`

- At the plain-`[button]` seam only (`key === "button"` — the engagement / supervisor / audio forms, the widget builders' own buttons and the `[external link button]` tag never enter), after the URL / form / label resolution and before the r326 anchor wrap: a button carrying an http(s) URL whose host is not in `internal_hosts` (exact, or a sub-domain of an entry: drive.google.com, docs.google.com, forms.gle, desire2learn.com, mytekuraschool.sharepoint.com, mytekuraschool-my.sharepoint.com, player.vimeo.com, vimeo.com — www.tekura.school.nz deliberately NOT listed, the gold ships the school's public site 3:0 external) and whose resolved form is the plain `<div class="button">` (`plain_form_match` — never `buttonD` / `downloadButton` / the reveal JS buttons) takes `form`; the r326 wrap then sees an anchor form and adds nothing. A label that fell to `journal_label_default` (tracked as `labelDefaulted` at the seam) becomes `default_label` "Go to website", or `video_label` "Go to video" when the URL matches `video_host_match` — the round-56 external-link-button defaults. A writer-supplied label is never touched; the r323 trailing-stop trim and the r328 canonical labels run after as before.
- The KB's "Go to website" replaces the gold's editorial resource-name labels (TWHA905 "Go to Kiwiharvest", ENFUN02 "Thoughtful Learning", CEDO102 "Young ocean explorers") — never matched either way, text-only, recorded not chased.

### 5. THE PROOF AND THE GATES

- OFF/ON in memory over ALL 416 modules (`_r338_probe_off_0*.log` / `_r338_probe_on_0*.log`): **OFF (`EXTDEST_OFF=1`) = disk 2102/2102; ON = exactly 134 pages / 71 modules**. Scoped regeneration in the planner's 8 batches (`_r338_batches_run.sh`, all rc 0; `_r338_regen.log`); `_content_manifest.py fresh --affected` → **0 truly stale**; `diff` = **exactly the 134 pages / 71 modules, 0 added/removed**.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% ({DELTA}pp) / ≥50% {GE50_B} → {GE50_A} (NAMED) / ≥75% {GE75_B} → {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%** (state `outputs/_r338_sk_final.json`, FRESH). {MOVED}. The ≥50 −1 is accepted through the r289 named-movement override (`_fastloop_diff.py --accept-named`, recorded in the fast-loop manifest) — the r326 precedent.
- Every other gate EXACT (`_fastloop_diff.py` on the 71: every non-skeleton metric HELD; full suite `_r338_gates.log` line-for-line identical to r337 outside the skeleton block): cs exact 11375 / EXTRA 171 / missing 593 · clean 2056/2102 / leak 288/46 · body 191 · tags 9557/9557 · flipCard TOTAL 61 divergence 0 · entry-parity PASS · index-sync 33/28 · **13 selftests GREEN** (`_r338_selftests.log`, identical to r337's). **Widget verifiers over the 71 affected modules:** accordion {ACC}; tabs 35 built, every built tab matches a human tab; flipCard over the 71 = TOTAL 677 identical ON and OFF (`_r338_verify_flipcard.log` = `_r338_verify_flipcard_OFF.log` — that set's pre-existing baseline; the round touches no widget). The feature index needs no rebuild: its `button` feature already matches both classes. **Ceiling:** SCAFFOLD {SK_A}% = **{PCT}% of achievable** (ceiling 91.6%).
- **Verifier:** {VER}.

### 6. NAMED, NOT CHASED

- The 11 gold `button`s on external hosts (ANZH404's "Source A/B/C" evidence buttons, MXFL401's "Go to GST calculator" / "Kiwisaver Benefits" / "Go to PDF", XGF9006's "Feedback padlet", BLL234's "Go to resources", TWHK901 "Genless", MXFU402, XMES103 "Google Earth") — the KB-over-gold sites. The 173 external-host buttons on no gold page (the writer's istock / Education Perfect / twinkl asset links; the gold ships images or nothing) — equally unmatched before and after. The 41-button residue on other emitters (the r73 modal document button "Go to resource" — EXPFUN02/03's istock image modals — and the widget builders' own `div.button` forms; 18 pages / 13 modules, under the floor). The `[video link]` tag routed through the button branch (HIS1007 lesson 1: the gold EMBEDS the video) — a pre-existing route, recorded for a video-tag round. Education Perfect (app.educationperfect.com — 17 buttons, gold has none) is treated as an outside website by the host rule; the KB is silent and the gold gives no evidence either way.
- Also this round: the untagged standalone-hyperlink class DECLINED on the live-extractor measurement (see §3 and LOOP_STATE "Declined classes").

**Ledger:** scoped ship #4 since the r334 full-ship backstop · data `buttons.external_destination` · env `EXTDEST_OFF` · tools `outputs/_measure_r338_standalone_links.cjs` (+ `_r338_standalone_links.{{json,log}}`), `_measure_r338_gold_buttons.cjs` (+ `_r338_gold_buttons.{{json,log}}`), `_measure_r338_extbutton_class.py` (+ `_r338_extbutton_class{{,_BEFORE,_AFTER}}.{{json,log}}`), `_r338_probe.cjs` + `_r338_probe_run.sh` + `_r338_shard_0*`, `_r338_affected.txt`, `_r338_batches_plan.txt` / `_r338_batches_run.sh`, `_r338_proof.sh`, `_r338_finalise.py` · state `outputs/_r338_sk_final.json` (FRESH) · logs `_r338_probe_off_0*.log`, `_r338_probe_on_0*.log`, `_r338_regen.log`, `_r338_fastloop.log`, `_r338_gates.log`, `_r338_sk_full.log`, `_r338_selftests.log`, `_r338_verify_accordion.log`, `_r338_verify_flipcard.log` / `_r338_verify_flipcard_OFF.log`, `_r338_verify_tabs.log`, `_r338_fastloop_commit.log`.

"""
if "round 338, build 260619.09" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.08";\n'
NEW = ('\t// ROUND 338 (2026-09-15, build 260619.09): an external destination is the KB\'s externalButton (05D — Internal\n'
       '\t// div.button, External div.externalButton; the gold follows it by host) and a URL-only button reads "Go to website" /\n'
       '\t// "Go to video" (constraint 75) — ContentConverter.#externalDestination at the plain-[button] seam; scoped 71 modules;\n'
       '\t// env EXTDEST_OFF.\n'
       '\tstatic AppVersion = "260619.09";\n')
if '"260619.09"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 337 BASELINE (numbered steps are a semantic <ol> — KB constraint 42; scoped 24 modules)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 338 BASELINE (an external destination is the KB's externalButton — 05D + constraint 75; scoped 71 modules): SCAFFOLD mean {SK_A}% / >=50% {GE50_A} / >=75% {GE75_A} / >=90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r338_sk_final.json`, FRESH). r338 {DELTA} ({MOVED}); >=50 −1 accepted as NAMED (the r289 override, the r326 precedent); every other gate EXACT. Older r337 text: **ROUND 337 BASELINE (numbered steps are a semantic <ol> — KB constraint 42; scoped 24 modules)")
if "ROUND 338 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `EXTDEST_OFF` | 338 | **AN EXTERNAL DESTINATION IS THE KB'S `externalButton`** (KB 05D \"Buttons\" Internal/External + constraint 75's \"Go to website\" default label; the autonomous loop's session-7 Round 1; **SCOPED regeneration of the 71 affected modules / 134 pages; scoped ship #4 since the r334 full backstop**). Reverts byte-for-byte (OFF in memory = disk 2102/2102). ON (default), `buttons.external_destination`: at the plain-[button] seam (`key === \"button\"`), a button carrying an http(s) URL whose host is not in `internal_hosts` (drive.google.com, docs.google.com, forms.gle, desire2learn.com, the two mytekuraschool sharepoint hosts, player.vimeo.com / vimeo.com — exact or sub-domain) and whose resolved form is the plain `<div class=\"button\">` ships `<a href=\"{url}\" target=\"_blank\"><div class=\"externalButton\">{label}</div></a>`; a label that fell to `journal_label_default` becomes \"Go to website\" (\"Go to video\" for a `video_host_match` URL). Never touches buttonD / downloadButton / reveal buttons / a writer's label / the widget builders' own buttons. MEASURED: the gold decides the class by host (drive 586:1 / docs 92:6 / desire2learn 17:8 button; youtube 1:24 / earth.google 0:16 / teara 3:11 / nzhistory 0:11 externalButton); Claude's 304 external-host `div.button`s (147 pages / 80 modules) → gold externalButton 120 / button 11 = 0.916 of found (Standard 0.913 / Inquiry 0.909 / Fundamentals 1.000). " + f"Skeleton {DELTA}pp ({MOVED}); every other gate EXACT; accordion verifier over the 71 {ACC}; 13 selftests GREEN. Residue: 41 external-host `div.button`s on other emitters (the r73 modal document button, the widget builders' forms; 18 pages). |\n")
if "| `EXTDEST_OFF` | 338 |" not in m:
    A = "| `TYPEDOL_OFF` | 337 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260619.09` (round 338 — **an external destination is the KB's `externalButton`** (KB 05D Internal/External + constraint 75's \"Go to website\" default; the autonomous loop's session-7 Round 1; **SCOPED regeneration of 71 modules / 134 pages; scoped ship #4 since the r334 full backstop**). **ROUND 338 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% {GE50_A} / ≥75% {GE75_A} / ≥90% {GE90} / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r338_sk_final.json`, FRESH) = **{PCT}% of achievable** (ceiling 91.6%). ≥50 −1 NAMED (HIS1007_1_0 50.86 → 49.48, a coincidental-match loss on `[video link]` buttons the gold embeds; accepted through the r289 override). Every other gate EXACT: cs exact **11375** / EXTRA **171** / missing **593** · clean **2056/2102** / leak **288/46** · body **191** · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **134 pages / 71 modules changed, 0 added/removed**; toggle `EXTDEST_OFF`; data `buttons.external_destination`. External-host `div.button` 304 → 41. **Plateau window restarts at this round (Chris's session-7 \"continue\" after the r337 plateau stop): r338 {DELTA}.**)\n")
if "- **Build:** `260619.09` (round 338" not in m:
    A = "- **Build:** `260619.08` (round 337 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.09"; d["_meta"]["round"] = 338; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": GE50_A, "pages_ge_75": GE75_A})
d["_meta"]["_round338_note"] = f"Round 338 (an external destination is the KB's externalButton — 05D + constraint 75; scoped 71-module regeneration, scoped ship #4 since the r334 full backstop). Skeleton {SK_B}->{SK_A} ({DELTA}pp; >=50 {GE50_B}->{GE50_A} NAMED (HIS1007_1_0), >=75 {GE75_B}->{GE75_A}, >=90 {GE90}); every other gate EXACT; 13 selftests GREEN."
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
old75 = "| 75 | Standalone `[external link]` → `externalButton`; inline → anchor; \"Go to website\" default label | CL-0050; CL-0078 | 16 WT modules tag external links; gold 417 pages carry externalButtons | **PARTIAL** — Claude 117 pages / 200 buttons; \"Go to website\" LIVE (108 pages) | buttons emitter |"
new75 = "| 75 | Standalone `[external link]` → `externalButton`; inline → anchor; \"Go to website\" default label | CL-0050; CL-0078 | 16 WT modules tag external links; gold 417 pages carry externalButtons | **PARTIAL → the destination half CAPTURED-LIVE (round 338, 2026-09-15, the loop's session 7)** — 05D's Internal/External class by host (`buttons.external_destination`: an outside-website URL on a `[button]` → `externalButton`, 134 pages / 71 modules) + the \"Go to website\" / \"Go to video\" default for a URL-only button (60 sites); the `[external link]` tag forms were already LIVE (r56/r76/r88). Re-measured with the live extractor: the UNTAGGED standalone-hyperlink form is NOT a button in the gold (0.067 / 0.072) — declined; residue 41 external-host `div.button`s on other emitters (18 pages) | `buttons.external_destination`; env `EXTDEST_OFF` |"
if old75 in k:
    k = k.replace(old75, new75, 1); print("KB row 75")
anchor = "| ~~—~~ | c42 numbered steps = semantic `<ol>`"
drow = (f"| ~~—~~ | 05D \"Buttons\" Internal/External — an outside-website destination on a `[button]` is `externalButton`, Te Kura's own systems stay `button`; + c75's \"Go to website\" default for a URL-only button | **SHIPPED round 338** (external-host `div.button` 304 → 41; 134 pages / 71 modules) | 134 pages | {DELTA}pp / ≥75 +1 / ≥50 −1 named | `EXTDEST_OFF` | CAPTURED-LIVE |\n")
if "05D \"Buttons\" Internal/External" not in k:
    assert k.count(anchor) == 1; k = k.replace(anchor, drow + anchor, 1); print("KB status D-row")
wr(KB, k)

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 7 · Round 1 (engine r338) — what shipped (an external destination is the KB's externalButton)
- **Fix:** `buttons.external_destination` {{enabled, env EXTDEST_OFF, form, internal_hosts, plain_form_match, default_label, video_label,
  video_host_match}} → `ContentConverter.#externalDestination(url, key, form, tpl)` at the plain-[button] seam, after the URL / form /
  label resolution and before the r326 anchor wrap: an http(s) URL whose host is not Te Kura's own (drive / docs / forms.gle /
  desire2learn / sharepoint / vimeo player) on the plain `div.button` form → the KB external form `<a href target=_blank><div
  class="externalButton">`; a label that fell to `journal_label_default` → "Go to website" / "Go to video". Writer labels untouched.
- **Regeneration:** scoped — the in-memory OFF/ON probe over ALL 416 modules: OFF = disk 2102/2102; ON = exactly 134 pages / 71 modules
  (`_r338_affected.txt`; every changed line the class swap or class + default label, 0 other differences); planner batches (8) all rc 0;
  0 truly stale; manifest diff = exactly the 134 / 71.
- **Gates:** skeleton {SK_B} → {SK_A} ({DELTA}pp; {MOVED}); ≥50 {GE50_B} → {GE50_A} (NAMED, accepted through the r289 override — the r326
  precedent); ≥75 {GE75_B} → {GE75_A}; ≥90 {GE90}; RAW {RAW_B} → {RAW_A}; every other gate line-for-line EXACT with r337 (fastloop: every
  non-skeleton metric HELD; full suite `_r338_gates.log`); accordion verifier over the 71: {ACC}; tabs 35 every built tab matches; flipCard
  over the 71 identical ON vs OFF (pre-existing baseline); 13 selftests GREEN (identical to r337's). **{PCT}% of achievable.**
- **Verifier:** {VER}.
- **Named:** the 11 gold `button`s on external hosts (ANZH404 "Source A/B/C", MXFL401, XGF9006, BLL234, TWHK901, MXFU402, XMES103); the
  173 external-host buttons on no gold page (istock / EP / twinkl asset links); the 41-button residue on other emitters; the `[video link]`
  tag routed through the button branch (HIS1007 lesson 1 — the gold embeds the video; a video-tag round). Ship ledger: scoped #4 since
  the r334 full backstop (4 of headroom). **Plateau window restarts at r338 ({DELTA}pp).**

""")
ANCHOR = "## Session 7 · Round 1 PICK (engine r338)"
if "## Session 7 · Round 1 (engine r338) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = f"- Session 7 Round 1 (engine r338 — an external destination is the KB's externalButton, 05D + constraint 75): SHIPPED 2026-09-16 ≈00:05 (session 7). AppVersion 260619.09, CLAUDE.md §9/§11/§14, KB status row 75 → the destination half CAPTURED-LIVE + D-row, scoped ship #4 since the r334 full backstop. Skeleton {DELTA}pp, ≥75 +1, ≥50 −1 named; every other gate EXACT. The untagged standalone-hyperlink candidate DECLINED on the live-extractor measurement." + nl + OLD_P
if "- Session 7 Round 1 (engine r338" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- s6-r3 (engine r337)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = f"- s7-r1 (engine r338) · an external destination is the KB's `externalButton` (KB 05D Internal/External: a `[button]` whose URL points at an outside website ships `<a href target=_blank><div class=\"externalButton\">`, Te Kura's own systems — drive / docs / forms / LMS / sharepoint / vimeo player — stay `button`; + constraint 75's \"Go to website\" / \"Go to video\" for a URL-only button that had fallen to the journal default) · SHIPPED 2026-09-16 · scoped regeneration, 134 pages / 71 modules · scaffold {SK_B}→{SK_A} ({DELTA}; {MOVED}), ≥75 +1, ≥50 −1 NAMED, every other gate EXACT · external-host div.button 304→41 · {PCT}% of achievable · scoped ship #4 since the r334 full · the untagged standalone-hyperlink candidate DECLINED (gold buttons it at 0.07) · commit (see git log) · **plateau window restarts (r338 {DELTA})**" + nl
if "- s7-r1 (engine r338)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
DECL_ANCHOR = "## Declined classes" + nl
DECL = L(f"""- **The UNTAGGED standalone hyperlink → externalButton (KB constraint 75's "position decides" read onto an untagged link) — DECLINED
  2026-09-15 (session 7, Round 1 PICK; `outputs/_measure_r338_standalone_links.cjs` → `_r338_standalone_links.json` / `.log`, the LIVE
  extractor over all 454 modules; the reverse trace `_measure_r338_gold_buttons.cjs` → `_r338_gold_buttons.json` / `.log`).** The r337
  note's "452 untagged hyperlink phrases the human buttoned (255 pages)" was a parsed-text artefact. Untagged STANDALONE hyperlink paragraphs:
  486 phrase + 1,226 bare-URL; the gold ships them as a button at **0.067 / 0.072 of the found sites** (the majority are the writer's asset
  references — sharepoint 114, drive 112, istock 87, docs.google 41 — that the gold ships as media or drops; youtube 62 → inline `<a>` 28 /
  plain 18 / button 1); untagged INLINE 0.067 (phrase) / 0.202 (URL); in a list item 0.028. Below the r182 floor in every template and
  subject group. The 873 gold externalButtons trace to: HREF-sourced 526 (the `[button]`-family tags with a URL dominate → round 338),
  text-only 140, no WT source 207 (class C). Never re-attempt without a new discriminator.
""")
if "The UNTAGGED standalone hyperlink → externalButton" not in s:
    assert s.count(DECL_ANCHOR) == 1, "declined anchor"; s = s.replace(DECL_ANCHOR, DECL_ANCHOR + DECL, 1); print("declined class")
wr(LS, s); print("LOOP_STATE.md written")
