#!/usr/bin/env python3
"""ROUND 345 (loop session 12 Round 2 — Chris's D10-2) — finalise: changelog, AppVersion (260619.15 → 260619.16), CLAUDE.md
§9/§11/§14, gate_baseline.json meta, KB status row, LOOP_STATE.md. Idempotent; LF kept; never json.dumps a data file."""
import io, os, json
HERE = os.path.dirname(os.path.abspath(__file__))
PF = os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)

SK, RAW, GE50, GE75, GE90, PAIRS = "51.281", "35.407", 1073, 198, 15, 1955
CS, EX, MI = 11461, 175, 607
SEVEN = "ANZH101_2_0 / ANZH105_1_0 / HIS1006_9_0 / MXDB202_3_0 / TEDC402_1_0 / XDLS501_1_0 / XGF9002_9_0"

CL = os.path.join(PF, "BUILD_CHANGELOG.md"); s = rd(CL)
head = "# BUILD CHANGELOG — Stage 2 (engine + UI)" + chr(10) + chr(10)
ENTRY = f"""## 2026-09-16 (round 345, build 260619.16) — THE BILINGUAL LESSON-TITLE PAIR IS ENGLISH FIRST OUTSIDE THE MTK MODULES (Chris's decision D10-2, Option B: "English first in Standard modules"; the r316 `header.lesson_bilingual_pair` seam; the autonomous loop's session-12 Round 2; SCOPED regeneration of 7 modules / 7 pages — scoped ship #2 since the r342 full; GATE-NEUTRAL by construction, ships on the visible human match)

### 1. WHAT CHANGED, IN ONE LINE

**A lesson whose own title is a `|`-separated bilingual pair ships the ENGLISH half as the first `<h1><span>` and the Te Reo half second in every module that is not an MTK reoTranslate module** — `Stories` over `Pūrākau` (ANZH101_2_0), `Easter Island` over `Rapa Nui` (MXDB202_3_0), `Learning to relate well with others` over `Whakawhanaungatanga` (XDLS501_1_0) — the gold's order on each. The MTK rule (`reo_first_when_body_class "reoTranslate"`, 07D rule 7 — Māori first) is untouched: every TRR / PNR page is byte-identical.

### 2. THE MEASUREMENT (`outputs/_measure_r345_engfirst.py` — every paired non-reoTranslate lesson page with a two-span title)

- 23 pages (Standard 22 / Inquiry 1; 36 more are Bilingual, information only). Which half reads as Te Reo: a MACRON decides 6 pages (ENG-FIRST-ALREADY 4 = XMES103's `Taku Whānau` second; REO-FIRST 2 = ANZH101 `Pūrākau | Stories`, ANZH105 `Nō Hea Koe? | Where Are You From?`); the other 17 carry no macron on either half (`Rapa Nui | Easter Island`, `Whakawhanaungatanga | Learning to relate…`, `Mautohe | Protest`, MXFL101's `One | Tahi` ×6, XMES102's `… | Taku Wahi` ×5 …). **D10-2 as recorded said the writer's order stands where no macron decides — which would have left MXDB202_3_0, the very page the decision named as a gain, as written.** The engine's own r321 `#looksMaori` test (a macron OR letters only from the Māori alphabet) decides 5 of those 17: `Rapa Nui`, `Whakawhanaungatanga`, `He kupu whakakapi`, `Whakatau`, `Mautohe` read as Te Reo, their partners do not; `One | Tahi` both read as Te Reo (as written), `Taku Wahi` is already second. So the detector is **macron first, the alphabet test as the fallback** (`reo_detect "macron+alphabet"`) — Chris's rule, the engine's existing test, no new vocabulary.
- Gold order agreement 12 → 13 of 23: gains ANZH101_2_0 / MXDB202_3_0 / XDLS501_1_0; NAMED overrides ANZH105_1_0 and HIS1006_9_0 (the human kept the writer's Te-Reo-first order — the two pages D10-2 itself names); XGF9002_9_0 / TEDC402_1_0 swap toward English first but their golds carry a different title altogether; MXFL101 ×6 / XMES102 ×5 / CEDT207 unchanged.

### 3. THE SEAM (data `header.lesson_bilingual_pair.english_first` {{enabled, env, reo_detect}}; env `ENGFIRST_OFF`)

- `SkeletonBuilder.#lessonPair`, the `!reoMode` branch that returned `[a, b]` as written: when exactly one half reads as Te Reo it ships second; both / neither → the writer's order. The reoTranslate branch (macron → Te Reo first, `reo_fallback second`) is byte-unchanged.

### 4. THE PROOF

- In-memory probe over ALL 416 (`_r345_probe.cjs`, 4 shards): **OFF = disk 2110/2110; ON = 7 pages / 7 modules** ({SEVEN}; `_affected_r345.txt`), every other page byte-identical — the whole two-span-title family (59 pages incl. all 36 Bilingual) proven in memory. SCOPED regeneration of the 7 (3 batches rc 0); `_content_manifest.py fresh` 0 truly stale; `diff` = exactly the 7, 0 added / removed.
- **Gates: the full suite is line-for-line identical to r344's** (`_r345_gates.log`): skeleton {SK}% / ≥50 {GE50} / ≥75 {GE75} / ≥90 {GE90} @ {PAIRS} — **0 pages moved** (`_r345_sk_final.json`; two identical `h1 > span` nodes swapping order is invisible to the text-stripped skeleton, the r327 class); RAW {RAW}%; cs {CS} / {EX} / {MI}; clean 2080/2103; leak 26/23; body 180; every verifier identical. Fast-loop PASS, baseline committed; ledger scoped #2 since the r342 full (6 of headroom); feature index rebuilt (GREEN).
- The round's verifier re-run: REO-FIRST (macron) 2 → 0; gold agreement 12 → 13.

### 5. RECORDED

- KB DELTA for a KB session: 00G c79 / 01A to gain "a bilingual lesson-title pair is English first in Standard modules, Māori first in MTK (07D rule 7)".
- NOT in this round (D10-2's own scope): the overview `[TITLE BAR]` module-title pair; the Languages three-part titles (c85).
- The two named overrides (ANZH105_1_0, HIS1006_9_0); the `One | Tahi` number pages (both halves read as Te Reo — as written; their golds carry `Numbers 1–10`).

**Ledger:** SCOPED ship #2 since the r342 full (6 of headroom) · data `header.lesson_bilingual_pair.english_first` · env `ENGFIRST_OFF` · tools `outputs/_measure_r345_engfirst.py` (+ `_r345_engfirst.json`, `_r345_engfirst_pre.json`, `_r345_engfirst.log`, `_r345_engfirst_post.log`), `_r345_lessonpair_now.log`, `_r345_splice.py`, `_r345_probe.cjs` + `_r345_probe_{{off,on}}_0*.log`, `_r345_changed_pages.txt`, `_affected_r345.txt`, `_r345_regen.log`, `_r345_gates.log`, `_r345_sk_final.json` / `_r345_sk_full.log`, `_r345_sk_movers.log`, `_r345_fastloop_commit.log`, `_r345_feature_index.log`, `_r345_finalise.py` · AppVersion 260619.16.

"""
if "round 345, build 260619.16" not in s:
    assert s.startswith(head); s = head + ENTRY + s[len(head):]; wr(CL, s); print("changelog prepended")

CF = os.path.join(PF, "app", "js", "Config.js"); c = rd(CF)
OLD = '\tstatic AppVersion = "260619.15";' + chr(10)
NEW = ('\t// ROUND 345 (2026-09-16, build 260619.16): a bilingual lesson-title pair is ENGLISH FIRST outside the MTK reoTranslate' + chr(10) +
       '\t// modules (Chris\'s D10-2) — a macron, else the r321 Māori-alphabet test, decides which half is Te Reo; scoped' + chr(10) +
       '\t// regeneration of 7 modules / 7 pages; gate-neutral (a header h1 swap is invisible to the skeleton).' + chr(10) +
       '\tstatic AppVersion = "260619.16";' + chr(10))
if '"260619.16"' not in c:
    assert c.count(OLD) == 1; c = c.replace(OLD, NEW, 1); wr(CF, c); print("AppVersion bumped")

CM = os.path.join(PF, "CLAUDE.md"); m = rd(CM)
OLD9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 344 BASELINE (the opening duplicate body heading dropped in full"
NEW9 = (f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 345 BASELINE = r344, page-for-page (the bilingual lesson-title pair English first outside the MTK modules — Chris's D10-2; SCOPED regeneration of 7 modules / 7 pages, scoped ship #2 since the r342 full; a header `h1 > span` swap is invisible to the text-stripped skeleton): SCAFFOLD mean {SK}% / >=50% {GE50} / >=75% {GE75} / >=90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW}%** (state `outputs/_r345_sk_final.json`, FRESH, 0 pages moved); every other gate line-for-line identical to r344. Older r344 text: **ROUND 344 BASELINE (the opening duplicate body heading dropped in full")
if "ROUND 345 BASELINE" not in m:
    assert m.count(OLD9) == 1, "§9"; m = m.replace(OLD9, NEW9, 1); print("§9")
A11 = "| `DEDUPC47_OFF` | 344 | **THE OPENING DUPLICATE BODY HEADING IS DROPPED IN FULL"
R11 = ("| `ENGFIRST_OFF` | 345 | **THE BILINGUAL LESSON-TITLE PAIR IS ENGLISH FIRST OUTSIDE THE MTK MODULES** (Chris's D10-2, Option B — \"English first in Standard modules\"; the autonomous loop's session-12 Round 2; **SCOPED regeneration of 7 modules / 7 pages; scoped ship #2 since the r342 full; gate-neutral**). Reverts byte-for-byte (OFF in memory = disk 2110/2110). ON (default), `header.lesson_bilingual_pair.english_first` `{ enabled, env, reo_detect \"macron+alphabet\" }`: in `SkeletonBuilder.#lessonPair`'s non-reoTranslate branch, when exactly one half of the r316 pair reads as Te Reo — a macron decides first; when neither or both halves carry one, the r321 `#looksMaori` alphabet test decides (`Rapa Nui` / `Whakawhanaungatanga` / `He kupu whakakapi` read as Te Reo; `One | Tahi` both do → as written) — that half ships SECOND; both / neither → the writer's order. The reoTranslate branch (07D rule 7, Māori first) is untouched — every TRR / PNR page byte-identical. MEASURED (`outputs/_measure_r345_engfirst.py`, 23 paired non-MTK two-span lesson pages): 7 swap ({SEVEN}); gold order agreement 12 → 13 (gains ANZH101 / MXDB202 / XDLS501; NAMED overrides ANZH105_1_0 + HIS1006_9_0 — the human kept the writer's Te-Reo-first order, the two pages D10-2 itself names). Skeleton 0 pages moved; every gate line-for-line identical. KB delta recorded (00G c79 / 01A). |\n")
if "| `ENGFIRST_OFF` | 345 |" not in m:
    assert m.count(A11) == 1, "§11"; m = m.replace(A11, R11 + A11, 1); print("§11")
B14 = (f"- **Build:** `260619.16` (round 345 — **the bilingual lesson-title pair is ENGLISH FIRST outside the MTK modules** (Chris's D10-2, Option B; the r316 `header.lesson_bilingual_pair` seam gains `english_first` — a macron, else the r321 Māori-alphabet test, decides which half is Te Reo and it ships second; MTK's 07D rule 7 untouched; the autonomous loop's session-12 Round 2; **SCOPED regeneration of 7 modules / 7 pages; scoped ship #2 since the r342 full**). **ROUND 345 BASELINE = r344 page-for-page: SCAFFOLD mean {SK}% / ≥50% {GE50} / ≥75% {GE75} / ≥90% {GE90} / skipped 0 @ {PAIRS}; RAW {RAW}%** (state `outputs/_r345_sk_final.json`, FRESH, 0 pages moved — a header h1 swap is invisible to the skeleton) = **55.8% of achievable** (ceiling 91.9%). Every other gate line-for-line identical to r344 (cs **{CS}** / **{EX}** / **{MI}**; clean **2080/2103**; leak **26/23**; body **180**; 13 selftests GREEN). Corpus 2110 pages / 416 modules, 0 truly stale, **7 pages / 7 modules changed, 0 added/removed**; toggle `ENGFIRST_OFF`; data `header.lesson_bilingual_pair.english_first`. Gold order agreement 12 → 13 of 23 (2 named overrides). **Plateau window (§4's TWO conditions — under 0.02pp AND no other protected gate moved): r342 −0.003 but body 191 → 180 / ≥75 −2 moved; r344 +0.016 but cs exact −8 moved; r345 0.000 with nothing moved — the strict window stands at 1 of 3.**\n")
if "- **Build:** `260619.16` (round 345" not in m:
    A = "- **Build:** `260619.15` (round 344 —"; assert m.count(A) == 1, "§14"; m = m.replace(A, B14 + A, 1); print("§14")
wr(CM, m)

GB = os.path.join(HERE, "..", "reference", "tests", "gate_baseline.json"); raw = rd(GB); d = json.loads(raw)
d["_meta"]["build"] = "260619.16"; d["_meta"]["round"] = 345; d["_meta"]["date"] = "2026-09-16"
d["_meta"]["_round345_note"] = "Round 345 (D10-2: English-first lesson-title pairs outside MTK; scoped 7 modules / 7 pages). Gate-neutral: every metric identical to r344, skeleton 0 pages moved."
wr(GB, json.dumps(d, ensure_ascii=False) + (chr(10) if raw.endswith(chr(10)) else "")); print("gate_baseline.json meta")

KB = os.path.join(HERE, "..", "..", "KB_AMALGAMATION_STATUS.md"); k = rd(KB)
OK = "| — | (not a KB row — a house rule the KB lacks) a `\\|`-separated bilingual LESSON title in a Standard-template module ships English first (MTK stays Māori first, 07D rule 7) | **AUTHORISED — Chris D10-2 (2026-09-16), queued item 3**;"
NK = "| — | (not a KB row — a house rule the KB lacks) a `\\|`-separated bilingual LESSON title in a Standard-template module ships English first (MTK stays Māori first, 07D rule 7) | **SHIPPED round 345 (2026-09-16)** — `header.lesson_bilingual_pair.english_first`, a macron else the r321 Māori-alphabet test decides; 7 pages / 7 modules swapped, gold order agreement 12 → 13 of 23 (ANZH105_1_0 + HIS1006_9_0 the named overrides); gate-neutral. Was: **AUTHORISED — Chris D10-2 (2026-09-16), queued item 3**;"
if "SHIPPED round 345" not in k:
    assert k.count(OK) == 1, "kb d10-2 row"; k = k.replace(OK, NK, 1); wr(KB, k); print("KB status row")

LS = os.path.join(HERE, "..", "..", "LOOP_STATE.md"); s = rd(LS); nl = chr(13) + chr(10) if chr(13) + chr(10) in s[:3000] else chr(10)
def L(t): return t.replace(chr(10), nl)
SEC = L(f"""## Session 12 · Round 2 (engine r345 — D10-2) — what shipped (the bilingual lesson-title pair is English first outside the MTK modules)
- **Fix:** `header.lesson_bilingual_pair.english_first` {{enabled, env ENGFIRST_OFF, reo_detect "macron+alphabet"}} in `SkeletonBuilder.#lessonPair`'s
  non-reoTranslate branch: when exactly one half reads as Te Reo (a macron decides; when neither or both halves carry one the r321 `#looksMaori`
  alphabet test decides) it ships SECOND; both / neither → the writer's order. The reoTranslate branch (07D rule 7) untouched — every TRR / PNR page
  byte-identical. Splice `outputs/_r345_splice.py`.
- **Measured first** (`_measure_r345_engfirst.py`): 23 paired non-MTK two-span lesson pages; the macron alone decides 2 (ANZH101 gain / ANZH105 override —
  net zero, and it would have left MXDB202_3_0, the page D10-2 names as a gain, as written); the alphabet fallback decides 5 more → 7 swap
  ({SEVEN}); gold order agreement 12 → 13 (gains ANZH101_2_0 / MXDB202_3_0 / XDLS501_1_0; NAMED overrides ANZH105_1_0 + HIS1006_9_0 — the two D10-2 itself
  names; XGF9002 / TEDC402 golds carry a different title; MXFL101's `One | Tahi` both halves read as Te Reo → as written).
- **Regeneration:** SCOPED — probe over ALL 416: OFF = disk 2110/2110, ON = 7 pages / 7 modules (`_affected_r345.txt`), the other 409 byte-identical (the whole
  two-span family incl. all 36 Bilingual pages proven in memory); 3 batches rc 0; `fresh` 0 truly stale; `diff` = exactly the 7.
- **Gates: line-for-line identical to r344** (`_r345_gates.log`); skeleton 0 pages moved (a header `h1 > span` swap is invisible to the text-stripped
  skeleton — the r327 class): {SK} / {GE50} / {GE75} / {GE90} @ {PAIRS}, RAW {RAW}; cs {CS} / {EX} / {MI}; clean 2080/2103; leak 26/23; body 180; fast-loop PASS + committed;
  ledger scoped #2 since the r342 full (6 of headroom); feature index rebuilt (GREEN). 55.8% of achievable.
- **Recorded:** the KB delta (00G c79 / 01A — "English first in Standard modules, Māori first in MTK"); the overview `[TITLE BAR]` pair + the c85
  three-part titles are outside D10-2; the two named overrides.
- **Plateau window (§4's TWO conditions — under 0.02pp AND no other protected gate moved):** r342 −0.003 moved body 191 → 180 and ≥75 −2; r344 +0.016
  moved cs exact −8 (named); r345 0.000 moved nothing — the strict window is 1 of 3 (the loose "under-0.02" tally would read 3, but the rule's second
  condition is not met by r342 or r344); Chris's queue still carries the gate-moving D10-7 / D10-5 / D10-9 / D10-3 rounds.

""")
ANCHOR = "## Session 12 · Round 2 PICK (engine r345 — D10-2"
if "## Session 12 · Round 2 (engine r345 — D10-2) — what shipped" not in s:
    assert s.count(ANCHOR) == 1, "state anchor"; s = s.replace(ANCHOR, SEC + ANCHOR, 1); print("LOOP_STATE section")
OLD_P = "- Remaining KB queue (§D):"
NEW_P = (f"- Session 12 Round 2 (engine r345 — Chris's D10-2: a bilingual lesson-title pair is ENGLISH FIRST outside the MTK modules; a macron, else the r321 Māori-alphabet test, decides which half is Te Reo): **SHIPPED 2026-09-16 ≈19:10 (session 12)**. AppVersion 260619.16, CLAUDE.md §9/§11/§14, KB status D10-2 row SHIPPED, **SCOPED regeneration of 7 modules / 7 pages (scoped ship #2 since the r342 full)**. Gate-neutral (skeleton 0 pages moved; every gate line-for-line identical); gold order agreement 12 → 13 of 23 (2 named overrides). Plateau window (both §4 conditions) 1 of 3 — r342 / r344 each moved another gate.\n")
if "- Session 12 Round 2 (engine r345" not in s:
    assert s.count(OLD_P) == 1, "position"; s = s.replace(OLD_P, L(NEW_P) + OLD_P, 1); print("position")
OLD_R = "- s12-r1 (engine r344, D10-1)"
i = s.find(OLD_R); assert i > 0, "round log anchor"; j = s.find(nl, i) + len(nl)
NEW_R = (f"- s12-r2 (engine r345, D10-2) · a bilingual lesson-title pair is ENGLISH FIRST outside the MTK modules (the r316 seam gains `english_first`; a macron, else the r321 Māori-alphabet test, decides which half is Te Reo and it ships second; 07D rule 7 untouched) · SHIPPED 2026-09-16 ≈19:10 · SCOPED regeneration 7 modules / 7 pages ({SEVEN}), 0 added/removed (scoped #2 since the r342 full) · GATE-NEUTRAL: skeleton {SK} / {GE50} / {GE75} / {GE90} @ {PAIRS} 0 pages moved, every gate line-for-line identical to r344 · gold order agreement 12→13 of 23 (gains ANZH101 / MXDB202 / XDLS501; named overrides ANZH105_1_0 + HIS1006_9_0) · 55.8% of achievable · commit (see git log) · **plateau window (both §4 conditions): r345 = 1 of 3 (r342 moved body / ≥75, r344 moved cs exact)**\n")
if "- s12-r2 (engine r345, D10-2)" not in s:
    s = s[:j] + L(NEW_R) + s[j:]; print("round log")
wr(LS, s); print("LOOP_STATE.md written")
