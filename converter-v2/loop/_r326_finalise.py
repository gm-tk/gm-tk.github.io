#!/usr/bin/env python3
"""ROUND 326 — finalise: changelog, AppVersion, CLAUDE.md §9/§11/§14, KB status (both copies), gate_baseline.json,
LOOP_STATE.md (the round's what-shipped section + position + round log). Idempotent."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
SK_B, SK_A, RAW_B, RAW_A = "50.435", "50.492", "34.794", "34.831"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
ENTRY = f"""## 2026-09-15 (round 326, build 260618.97) — A CALL-TO-ACTION BUTTON IS AN ANCHOR (the KB's universal button form, 05D_COMP14_BUTTONS_TABLES_COLUMNS; the autonomous loop, session 4, Round 1; **FULL regeneration — the `[button]` tag family is the corpus; skeleton +0.057pp with a NAMED KB-over-gold dip on the ≥50 bucket (1031 → 1030), every other gate HELD-or-IMPROVED; the loop's plateau window restarts here at +0.057pp**)

### 1. WHAT CHANGED, IN ONE LINE

**A writer's plain `[button]` never ships as a bare `<div class="button">` any more: it sits inside the KB's anchor — `<a href="…" target="_blank"><div class="button">label</div></a>` — carrying the writer's own hyperlink where the Writers Template gives one (285 buttons whose `[LINK: …]` was being silently LOST), and a blank `href` plus ONE Designer/Developer To Do note where it does not (1,177 buttons: dropbox / portfolio / journal / quiz / download targets that live in no Writers Template). A reveal-type label (`Check answers`, `Reset`, `Reveal answer`) is left exactly as it was — the gold ships those as its JS `button clickDrop`, not a link. 713 pages / 286 modules changed.**

### 2. THE EVIDENCE (docx → human → Claude)

- **SSOG101 lesson 6** — docx: `[Button] Upload to dropbox.` → gold: `<a href="/d2l/common/dialogs/quickLink/quickLink.d2l?ou={{orgUnitId}}&type=dropbox&rcode=TCS-181940" target="_blank"><div class="button">Upload to dropbox</div></a>` → Claude before: `<div class="button">Upload to dropbox</div>`; after: `<a href="" target="_blank"><div class="button">Upload to dropbox</div></a>` + the To Do note. On the same page the docx's `[Button] How Can I Help Activity [LINK: https://docs.google.com/presentation/d/…/copy]` shipped a bare button with the link DROPPED; after: `<a href="https://docs.google.com/presentation/d/…/copy" target="_blank"><div class="button">How Can I Help Activity</div></a>` — the gold's form (it re-points the URL to a fresh copy, class C).
- **TEFUN01** — docx: `[Button] Go to quiz` ×3 → gold: `<a href="https://…/quickLink.d2l?ou={{orgUnitId}}&type=quiz&rcode=TCS_Dev-73113" target="_blank"><div class="button">Go to quiz</div></a>` → Claude before: bare `<div class="button">Go to quiz</div>`; after: `<a href="#" target="_blank">…</a>` (constraint 65's blank quiz href) + the To Do note.
- **AGH1003** — docx: a bare `[Button]` (the journal_label_default) → gold: `<a href="https://drive.google.com/drive/u/0/my-drive" target="_blank"><div class="button">Go to journal</div></a>` → Claude before: bare `<div class="button">Go to your journal</div>`; after: anchored, blank href, To Do note.
- **The KB:** `05D_COMP14_BUTTONS_TABLES_COLUMNS.md` gives ONE button form — `<a href="URL" target="_blank"><div class="button">Button text</div></a>` (lines 11, 58–59) — and constraint 65's quiz button is `<a href="#" target="_blank">…</a>` with the developer wiring the quicklink. **The gold agrees** (`outputs/_measure_r326_buttonanchor.py` → `_r326_buttonanchor_before.json`): an `<a>` around the non-JS `div.button` / `div.buttonD` on **0.997 of Standard (n=2553) / 0.977 Inquiry (558) / 1.000 Bilingual (65) / 1.000 Fundamentals (159)** buttons; by category upload 0.998 (1245) / journal 1.000 (1179) / quiz 0.995 (193) / download 1.000 (110) / other 0.970 (608); **62 of 62 subject prefixes ≥ 0.60**. The gold anchors even where the developer has not wired the target: `href=""`/`#` on 244 buttons.

### 3. THE MEASUREMENT (Claude, every paired page; JS buttons clickDrop / TKmodalButton / rSBtn / externalButton excluded)

- Before: **1,800 bare buttons on 762 pages / 306 modules** (upload 480, journal 460, quiz 25, download 17, other 818); anchored 475 (183 with a real URL, 292 blank — the round-308 upload box). After: bare **338 on 178 pages / 109 modules** — every one either a reveal-type label the exclusion keeps as the gold's JS button (219) or the `button engagementTrigger` / audio / builder forms this round does not touch (119); anchored **1,937** (468 with the writer's URL — **+285 hyperlinks recovered** — and 1,469 blank + To Do note).
- A first regeneration wrapped the reveal-type labels too (`Check answers` 78, `Reset` 80, `Check answer` 17 … 219 buttons / 38 modules): the gold ships those as `<div class="button clickDrop">` (157 of its 936 JS-driven buttons; 0 of its 3,311 anchored labels match the exclusion pattern), so `exclude_label_match` was added and the corpus regenerated again in full — the reveal build itself is its own round, recorded.

### 4. THE FIX — one data block `Emit_Templates.buttons.anchor_wrap` `{{ enabled, env: "BTNANCHOR_OFF", form, todo_note, exclude_label_match, targets[], default }}`

- **`ContentConverter.#buttonAnchorWrap`** at the generic `[button]` emit (the round-323 seam — `key === "button"` only; the engagement / supervisor / audio forms and every widget builder's own button never enter): a form that does not itself open with an anchor is wrapped in `form` (`<a href="{{href}}" target="_blank">{{button}}</a>`). With a URL (the writer's Word hyperlink on the label — parsed `[LINK: …]` — or a URL typed in the tag) the anchor carries it and no note is added; without one the first `targets` row whose `label_match` hits the label supplies `href` (default `""`; the quiz row `#`) and the To Do wording (dropbox quicklink / portfolio link / quiz quicklink / journal document / download file / link target), emitted as ONE `NotesAndComments.redFlag(…, "todo")` cv2-note after the button (the round-308 upload-box pattern; gate-neutral).
- **Env toggle `BTNANCHOR_OFF`** reverts byte-for-byte (OFF in memory = disk on 2,102 / 2,102 pages before the regeneration, `_r326_probe_off_0*.log`).

### 5. THE PROOF AND THE GATES

- FULL regeneration (416 modules / 70 batches, `_r326_batches_run.sh`, twice — before and after the exclusion); `_stalecheck.sh` **0 stale**; `_content_manifest.py diff` vs r325 → **713 pages / 286 modules changed, 0 added / 0 removed**.
- **Skeleton (PRIMARY): SCAFFOLD mean {SK_B}% → {SK_A}% (+0.057pp) IMPROVED / ≥50% 1031 → 1030 / ≥75% 193 → 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_B}% → {RAW_A}%.** 675 pages moved — 210 up / 465 down, pp-sum +111.26; every mover is one of the 713 changed pages and **net of them the corpus is IDENTICAL (53.624% = 53.624% over the other 1,276 pages)**; on the 678 changed paired pages 44.432% → 44.596%. Rises: CEDW101_0_0 +15.09, TEFUN05_0_0 +9.48, HES1005_7_0 +8.12, ANZH404_5_0 +6.95, PHE1005_3_0 +6.20.
- **The dips, NAMED (the §1b KB-over-gold override accounting):** the PRIMARY gate scores difflib over skeleton LINES after `_structural_skeleton` collapses consecutive repeats; wrapping a button turns `p / div.button / p / a>div.button` into one `┌ 2× repeated block of 3:` line the gold's skeleton does not use, and the ratio drops although the element sequence now matches the gold's. `outputs/_r326_scorer_diag.py` re-scores the 248 moved pages of the 69 biggest-mover modules ON vs OFF, collapsed (the gate) and uncollapsed: **gate pp-sum −4.26 vs uncollapsed +104.40**; XMES201_5_0 −18.81 (uncollapsed **+0.84** — its two anchored buttons now match the gold's `a > div.button` exactly), ANZH105_6_0 −10.89 (+2.40), ARFUN02_0_0 −8.66 (+0.54), MXEO202_8_0 −3.80 (+2.53); BLL146_2_0 −16.35 / BLL141_2_0 −11.60 / AGH1004_2_0 −6.07 are −0.35 / −0.85 / −0.42 uncollapsed. The structural residue: ENGI401_8_0 −7.37 (−8.10 uncollapsed) and MXEX302_7_0 −4.59 (−5.22) — Claude's page carries buttons its PAIRED gold page (ENGI401 5.3) does not, and an anchored extra button costs two unmatched lines instead of one. **≥50 crossers:** down 10 — CEDT501_6_0 / AGH1004_2_0 / ANZH304_4_0 / BLL222_1_0 / ENGI202_4_0 / CEDO502_6_0 (all six sat at exactly 50.00), MXFU401_1_0 50.27 → 49.73, CEDO301_3_0 50.47 → 49.54, BLL146_2_0, XMES201_5_0; up 9 — AGH1004_5_0, XLP01_4_0, MXFL203_4_0, BLL215_2_0, ANZH404_6_0, BLL126_2_0, MXEX302_1_0, BLL236_2_0, MXFL203_11_0. ≥75 up 3: MXFL301_9_0, BLL166_1_0, BLL217_1_0. `_gatecheck.py` reports the −1 as REGRESSED; it is judged as round 317 was — a named structural KB emission that diverges from the scorer's alignment, identical net of the named pages, the mean and the ≥75 bucket up.
- Every other gate: compare_structure exact **11360** / EXTRA **186** / missing **591** (text-matched 13398) · structurally clean **2056/2102** / leak **288/46** · **body 192 → 191 IMPROVED** (over-capture 43 → 42, runaway 4, empty 147) · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · speechBubble / modal lines identical · mtkQuiz shell 17 shells defect 0 · entry-parity PASS · index-sync 33/28 · pairs skipped 0 · **all THIRTEEN selftests GREEN** (`_r326_selftests.log`).
- Full-ship refresh: fast-loop baseline (`_fastloop_snapshot.py`), content manifest, ship ledger (FULL ship — scoped-ship counter reset), feature index `--rehtml` + `--merge` (selftest GREEN).
- **Ceiling:** SCAFFOLD {SK_A}% = **55.1% of achievable** (55.12; ceiling 91.6%).

### 6. NAMED, NOT CHASED

- The reveal-type `[button]` (`Check answers` / `Reset` / `Reveal answer` — 219 buttons / 38 modules) stays bare: the gold's `button clickDrop` reveal (button + the answers panel) is a widget build, its own round.
- The `button engagementTrigger` (99) / `audioButton` (19) forms: the gold carries neither class — the writer's `[Insert text box for student response – Engagement trigger]` is an MTK quiz there (ARFUN01) — unmeasured, its own PICK.
- KB constraint 55's label half: Claude ships bare labels `Quiz` 33 / `Portfolio` 25 / `Dropbox` 12 / `Quiz button` 11 / `Journal` 7 on 50 pages where the KB says `Go to quiz` / `Go to portfolio` / `Go to dropbox` (gate-neutral text) — a queue candidate.
- The "dropbox terminates its activity" follow-up is CLOSED on measurement (`_measure_r326_dbxterminate.py`: Claude 0 boxes with content after the button; gold 710 / 718 last-child).
- The gold's own 21 bare buttons and the 244 blank hrefs are the developer's unfinished wiring (class C); the per-module D2L rcode / journal document is in no Writers Template — the note says so.

**Ledger:** FULL ship (scoped-ship counter reset) · data `buttons.anchor_wrap` · env `BTNANCHOR_OFF` · tools `outputs/_measure_r326_buttonanchor.py` (+ `_r326_buttonanchor_{{before,after}}.json`), `_measure_r326_dbxterminate.py`, `_r326_scorer_diag.py` (+ `_r326_scorer_diag.json`), `_r326_fixpat.py`, `_r326_finalise.py` · state `outputs/_r326_sk_final.json` (FRESH) · logs `_r326_gates.log`, `_r326_gatecheck.log`, `_r326_sk_full.log`, `_r326_sk_moved.json`, `_r326_fastloop_snapshot.log`, `_r326_selftests.log`, `_r326_probe_off_0*.log`, `_r326_regen.log` / `_r326_regen2.log` / `_r326_regen3.log`, `_r326_manifest_diff.{{log,json}}`, `_r326_reveal_modules.txt`.

"""
if "round 326, build 260618.97" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260618.96";\n'
NEW = ('\t// ROUND 326 (2026-09-15, build 260618.97): a call-to-action button is an ANCHOR (the KB\'s\n'
       '\t// universal button form): a plain [button] with no URL ships inside <a href="" target="_blank">\n'
       '\t// + one To Do note, a [button] whose label carries the writer\'s hyperlink keeps it (285 links\n'
       '\t// were being lost), reveal-type labels (Check answers / Reset) stay the gold\'s JS button.\n'
       '\t// 713 pages / 286 modules, FULL regeneration. Env BTNANCHOR_OFF; data buttons.anchor_wrap.\n'
       '\tstatic AppVersion = "260618.97";\n')
if '"260618.97"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 325 BASELINE (phase-scoped activity numbering on the Fundamentals pages; scoped)"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 326 BASELINE (a call-to-action button is an anchor — the KB's universal button form; FULL regeneration): SCAFFOLD mean {SK_A}% / >=50% 1030 / >=75% 196 / >=90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r326_sk_final.json`, FRESH). r326 +0.057 (675 moved, 210 up / 465 down; every mover one of the 713 changed pages, IDENTICAL net of them; the dips NAMED — the scorer's repeat-collapsing, `_r326_scorer_diag.py`: gate pp-sum −4.26 vs uncollapsed +104.40 on the 248 biggest movers; ≥50 1031 → 1030 with six of the ten down-crossers from exactly 50.00 — the §1b override accounting, as r317). Older r325 text: **ROUND 325 BASELINE (phase-scoped activity numbering on the Fundamentals pages; scoped)")
if "ROUND 326 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
ROW = ("| `BTNANCHOR_OFF` | 326 | **A CALL-TO-ACTION BUTTON IS AN ANCHOR** (the KB's universal button form `05D_COMP14_BUTTONS_TABLES_COLUMNS` + constraint 65's blank quiz href; the autonomous loop's session-4 Round 1; **FULL regeneration — the `[button]` tag family is the corpus**). Reverts byte-for-byte (proven: OFF in memory = disk on 2,102/2,102 pages before the regeneration). ON (default), `buttons.anchor_wrap`: at the generic `[button]` emit (`#buttonAnchorWrap`, key === 'button' only — never the engagement / supervisor / audio forms or a widget builder's own button) a bare form is wrapped in `<a href=\"{href}\" target=\"_blank\">…</a>`; with a URL (the writer's `[LINK: …]` hyperlink or a typed URL) the anchor carries it and no note ships — 285 hyperlinks were being LOST; without one the matching `targets` row supplies the href (blank; `#` for quiz) and ONE Designer/Developer To Do note (cv2-note, gate-neutral). `exclude_label_match` keeps reveal-type labels (`Check answers` / `Reset` / `Reveal answer`) as the gold's JS `button clickDrop` — bare, untouched. MEASURED: the gold anchors 0.997 / 0.977 / 1.000 / 1.000 of non-JS buttons by template, 62/62 prefixes ≥ 0.60; Claude bare 1,800 → 338 (the 338 = reveal 219 + engagementTrigger / audio / builder 119). 713 pages / 286 modules changed. Skeleton +0.057pp (≥75 +3; ≥50 −1 NAMED — the scorer's repeat-collapsing, identical net of the changed pages), body 192 → 191, every other gate EXACT, 13 selftests GREEN. |\n")
if "| `BTNANCHOR_OFF` | 326 |" not in m:
    A = "| `PHASENUM_OFF` | 325 |"; assert m.count(A) == 1, "§11"; m = m.replace(A, ROW + A, 1); print("§11")
B14 = (f"- **Build:** `260618.97` (round 326 — **a call-to-action button is an anchor** (the KB's universal button form; the autonomous loop's session-4 Round 1; **FULL regeneration; scoped-ship counter reset**). **ROUND 326 BASELINE: SCAFFOLD mean {SK_A}% / ≥50% 1030 / ≥75% 196 / ≥90% 15 / skipped 0 @ 1954; RAW {RAW_A}%** (state `outputs/_r326_sk_final.json`, FRESH) = **55.1% of achievable** (ceiling 91.6%). cs exact **11360** / EXTRA **186** / missing **591** · clean **2056/2102** / leak **288/46** · **body 191** (was 192) · tags **9557/9557** · flipCard TOTAL 61 divergence 0 · index-sync 33/28 · entry-parity PASS · mtkQuiz shell defect 0 · all THIRTEEN selftests GREEN. Corpus 2102 pages / 413 modules, 0-stale, **713 pages / 286 modules changed, 0 added/removed**; toggle `BTNANCHOR_OFF`; data `buttons.anchor_wrap`. The ≥50 bucket's −1 is a NAMED scorer-alignment dip (see §9), identical net of the changed pages.)\n")
if "- **Build:** `260618.97` (round 326" not in m:
    A = "- **Build:** `260618.96` (round 325 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

# ---------------------------------------------------------------- KB status: a D-table row (both copies)
for P in (os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"), os.path.join(PF, "loop", "KB_AMALGAMATION_STATUS.md")):
    k = rd(P); nl = "\r\n" if "\r\n" in k[:3000] else "\n"
    A = "| — | c92 language fonts (7 pages)"
    ROWD = ("| ~~—~~ | 05D universal button form — every call-to-action `[button]` is `<a href target=_blank><div class=button>` (+ constraint 65's blank quiz href) | **SHIPPED round 326** (713 pages / 286 modules, full regeneration; Claude bare buttons 1,800 → 338, 285 lost hyperlinks recovered) | skeleton-visible (`<a>` node; +0.057pp, ≥50 −1 named) | — | not a numbered constraint — the component doc's one button form; the reveal-type labels (`Check answers` / `Reset`) stay the gold's JS `button clickDrop` (its own round); constraint 55's label half (`Quiz` / `Portfolio` / `Dropbox` bare labels, 50 pages) is a queue candidate |" + nl)
    if "05D universal button form" not in k:
        assert k.count(A) == 1, P; k = k.replace(A, ROWD + A, 1); wr(P, k); print("KB status D-row:", os.path.basename(os.path.dirname(P)))

# ---------------------------------------------------------------- gate_baseline.json
GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260618.97"; d["_meta"]["round"] = 326; d["_meta"]["date"] = "2026-09-15"
d["skeleton"].update({"mean_scaffold_pct": float(SK_A), "raw_mean_pct": float(RAW_A), "pages_ge_50": 1030, "pages_ge_75": 196, "pages_ge_90": 15})
d["body_compare"].update({"any_breakdown": 191, "over_capture": 42, "runaway": 4, "empty_container": 147})
d["_meta"]["_round326_note"] = (f"Round 326 (a call-to-action button is an anchor — the KB's universal button form; FULL regeneration, the loop's session-4 Round 1). Skeleton {SK_B}->{SK_A} (+0.057pp; 675 moved, 210 up; every mover a changed page, identical net of them; the dips NAMED = the scorer's repeat-collapsing, outputs/_r326_scorer_diag.py), >=50 1031->1030 (named, six down-crossers from exactly 50.00), >=75 193->196, RAW {RAW_B}->{RAW_A}; body 192->191; every other gate EXACT.")
wr(GB, json.dumps(d, ensure_ascii=False) + ("\n" if raw.endswith("\n") else "")); print("gate_baseline.json refreshed")

# ---------------------------------------------------------------- LOOP_STATE.md
LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = "\r\n" if "\r\n" in s[:3000] else "\n"
def L(t): return t.replace("\n", nl)
SEC = L(f"""## Session 4 · Round 1 (engine r326) — what shipped (the KB's universal button form)
- **Fix:** `buttons.anchor_wrap` {{enabled, env BTNANCHOR_OFF, form `<a href="{{href}}" target="_blank">{{button}}</a>`, todo_note, exclude_label_match,
  targets [dropbox / portfolio / quiz(href #) / journal|workbook / download], default}} — `ContentConverter.#buttonAnchorWrap` at the generic
  `[button]` emit (key === 'button' only). A URL-carrying button keeps its link (285 `[LINK: …]` hyperlinks were being lost); a URL-less one ships
  the blank anchor + ONE To Do note (the r308 pattern). Reveal-type labels excluded (gold = JS `button clickDrop`; 0 false hits on 3,311 gold
  anchored labels). Repair inside the round: the first full regeneration wrapped 219 reveal buttons / 38 modules → exclusion added → second full
  regeneration.
- **Regeneration:** FULL (416 modules / 70 batches, twice); 0 stale (mtime); 713 pages / 286 modules changed, 0 added / removed; OFF in memory =
  disk 2,102 / 2,102 before. Claude bare buttons 1,800 → 338 (upload 480 → 0, quiz 25 → 0, download 17 → 0, journal 460 → 91 = engagementTrigger,
  other 818 → 247 = reveal 219 + builder 28); anchored 475 → 1,937.
- **Gates:** skeleton {SK_B} → {SK_A} (+0.057pp; 675 moved, 210 up / 465 down; IDENTICAL net of the 713 changed pages — 53.624 = 53.624 over
  1,276), ≥50 1031 → 1030 (NAMED: the scorer's repeat-collapsing — `_r326_scorer_diag.py`: gate pp-sum −4.26 vs uncollapsed +104.40 on the 248
  biggest movers; six of the ten down-crossers sat at exactly 50.00; `_gatecheck.py` says REGRESSED on that line, judged under the §1b override
  accounting as r317), ≥75 193 → 196, ≥90 15; body 192 → 191 IMPROVED; every other gate EXACT; 13 selftests GREEN. **55.1% of achievable.**
- **Plateau window:** restarts at this round: r326 +0.057pp (≥ 0.02).

""")
ANCHOR = "## Session 4 · Round 1 PICK (engine r326)"
if "## Session 4 · Round 1 (engine r326) — what shipped" not in s:
    assert s.count(ANCHOR) == 1; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Round 12 (engine r325 — phase-scoped activity numbering on the Fundamentals pages, the r217/r266 follow-up): SHIPPED 2026-09-15 ≈13:10 (session 3). AppVersion 260618.96, CLAUDE.md §9/§11/§14, scoped ship #2 since the r323 full. **THE LOOP STOPPED after it (plateau rule).**"
NEW_P = OLD_P + nl + "- Session 4 Round 1 (engine r326 — a call-to-action button is an anchor, the KB's universal button form): SHIPPED 2026-09-15 ≈15:05 (session 4). AppVersion 260618.97, CLAUDE.md §9/§11/§14, KB status D-row added, FULL regeneration (scoped-ship counter reset)."
if "- Session 4 Round 1 (engine r326" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, NEW_P, 1); print("position")
OLD_R = "- r12 (engine r325) · phase-scoped activity numbering on the Fundamentals pages"
i = s.find(OLD_R); assert i > 0; j = s.find(nl, i) + len(nl)
NEW_R = f"- s4-r1 (engine r326) · a call-to-action button is an anchor (the KB's universal button form: a plain `[button]` ships inside `<a href target=_blank>` — the writer's hyperlink kept, else a blank href + one To Do note; reveal-type labels stay the gold's JS button) · SHIPPED 2026-09-15 · FULL regeneration, 713 pages / 286 modules · scaffold {SK_B}→{SK_A} (+0.057; 675 moved, 210 up; dips NAMED = scorer repeat-collapsing, identical net of the changed pages), ≥50 −1 named, ≥75 +3, body 192→191 · every other gate EXACT · bare buttons 1,800→338, 285 lost links recovered · 55.1% of achievable · commit (see git log)" + nl
if "- s4-r1 (engine r326)" not in s:
    s = s[:j] + NEW_R + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
