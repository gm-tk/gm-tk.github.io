#!/usr/bin/env python3
"""ROUND 472 finalise (session 43 Round 1 — the built flip card never drops the writer's words, FLIPTEXTGUARD_OFF) —
BUILD_CHANGELOG.md (prepend), Config.js AppVersion 260620.35 -> 260620.36, OPERATING_GUIDE §9 / §11 / §14, gate_baseline.json
(skeleton mean / RAW / flipcard), LOOP_STATE.md (marker cleared, Position, plateau, round log, next-session line; the PICK →
archive). Line edits only; .bak kept; nothing written until every anchor is found. Run under WSL."""
import io, os, json, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "(round 472," not in sc[:3000]
PJ = os.path.join(CV, "app", "js", "Config.js"); sj = rd(PJ); oldj = '\tstatic AppVersion = "260620.35";'; assert sj.count(oldj) == 1
PO = os.path.join(CV, "OPERATING_GUIDE.md"); so = rd(PO)
a9 = "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 470 BASELINE"; a11 = "| `TABLETBWT_OFF` | 470 |"; a14 = "- **Build:** `260620.35` (round 470"
for a in (a9, a11, a14): assert so.count(a) == 1, a
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
for p in ("- **ROUND 472 IN FLIGHT — NOT PROVEN**", "- **Before r472:**", "- LAST SHIPPED: **r470**", "- Before it: **r467**",
          "- Plateau window (§4): **2 of 3** — r470", "- Standing facts: AppVersion 260620.35", "## Round log", "**Next session starts with:**",
          "## Session 43 — Round 1 PICK (engine r472)"):
    find(p)

entry = """## 2026-09-24 (round 472, build 260620.36) — THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS: a text guard on every flipCard build, and the three root causes it exposed (a picture label read as a column header, a stacked front / back label column read once, an escaped line break) — 24 lossy builds now carry every word, 0 builds lost

### 1. WHAT CHANGED

**The find** (session 43 Round 1 — the §1g placement census re-run on r470: `body:widget:flipCard → ABSENT-inWT` 593 blocks / 113 pages / 83 modules — Writers-Template text the gold carries in a flip card that NO Claude page carries). Triangulated on **CEDO502-5.0**: the writer's `[Flipcards]` table is 2 × 2, every cell a whole card (`**What is a closed question?** / [Image: iStock …] url / [Reverse] / A closed question can be answered …`); the gold builds four cards (front `img` + `h5`, back `p` × 2); **Claude shipped ONE card of two pictures and lost all eight sentences.** Measured with the r352 widget text-loss census re-run over all 533 scored modules (`outputs/_s43_widgetloss.cjs`, `_s43_wl_run.sh`, 45 s): 3,267 built widgets, **331 lose ≥ 1 writer run of ≥ 3 words — flipCard 46 builds / 44 pages / 37 modules** (carousel 130, modal 46, accordion 37, clickDrop 26, dropDown 18 — follow-ups).

**The fix** (`InteractiveBuilder.#flipCard` + new `#flipTextLost` / `#flipLearnerParts` / `#flipNoteRows` / `#flipWithNotes` / `#flipVisible`; data `Emit_Templates.json` `flipCard.text_guard` {enabled, env, min_words 3, header_max_words 8, header_black_label, face_column_pairs, br_after_inline, note_rows_after} and `_tag_words_note.covering_note_min_words` 3; ONE env **`FLIPTEXTGUARD_OFF`** reverts all of it, byte-identical):
1. **The guard.** Every LEARNER PART of the captured table (a cell split at the writer's ` / ` and line breaks; red spans, `[tags]`, `[LINK:]` and URLs removed; ≥ 3 words) must be in the build's visible text. A part carrying a picture reference is the picture's own label (the gold's `alt` — XMES202 `[image] fruits on white background`) and a first row of short keyword labels is the column header ("Text for the outer side") — both exempt. A lossy DIALECT build falls through to the round-282 composer; a lossy COMPOSER build keeps the hand-off box (never half-build).
2. **`header_black_label`** — `#looksLikeFlipHeader` threw away any first row whose cells merely CONTAINED a keyword — the red picture label "Image: iStock" counted (CEDO502, PWY1002-3.1's "Retail" card, SSOG103-2.0's "Kia ora" card, SSOG103-4.0's kiwi card). A row that carries learner text is now a header only when its labels are the cells' own short black words; a row of picture labels alone keeps the old reading (XMES201-1.0 stays a box).
3. **`face_column_pairs`** — the composer's T1b face-label column read only the FIRST front / back row pair; OSAI101-2.0 stacks two, so three cards vanished. Every consecutive pair is read.
4. **`br_after_inline`** — `#flipCell` joined the writer's ` / ` lines with `<br>` and THEN ran the escaping inline renderer: the break shipped as a visible `&lt;br&gt;` — **145 on 10 pages → 0** (ENGJ302-3.0 ×91, MXDB302, OSGM201 / 401, BLLR202 / 203, ENGR302, XLP03, ENFUN01).
5. **`note_rows_after`** — a one-cell row spanning the card table is the writer's closing sentence, not a card (AGH1006-2.0 "The graft support material can be removed once the graft is healed …"); when the build leaves it out it follows the cards as a `<p>` instead of vanishing.
6. **`_tag_words_note.covering_note_min_words`** — the round-354 tag-line note skipped the writer's instruction when any existing note was a substring of it; the composer's bare `[Image]` note ("image") suppressed SSOG103-2.0's whole request ("Can these please be created to look like postcards … an audio button to hear the greeting"). A covering note now needs ≥ 3 words — 8 more modules get their writer instruction back in the red Writers Note (ARFUN04, ENGS102, HPRE203, TEFUN03, XDLS902, XMES101, XMES202, XTAS103; the red-note family is outside the skeleton).

### 2. PROOF

- In-memory A/B over all 545 modules (`outputs/_s42_probe_run.sh r472`): **OFF 3222 / 3222 identical; ON 37 pages / 31 modules changed**, all inside the flipCard family.
- The loss census, OFF → ON (`_r472_wl_compare_final2.log`): flipCard **built 290 → 290 (no build lost), lossy 46 → 22**; 24 lossy → lossless (CEDO502, ENGJ302 ×2, OSGM201, OSGM401, OSAI101, OSSM401, ENGC201, ENGI302, ENGI202, MXEX201, PWY1002, SSOG103 ×2, SSOG105, SSCI205 ×3, CEDO301, ENFUN01, AGH1006 …), 6 lose less; the 22 left are the writer's column labels, picture titles and the census's own whole-cell artefact (a picture file name joined to its caption). Every other widget type byte-identical.
- **OPERATING_GUIDE §0a whole-type rule:** the flipCard family = every module carrying a flipCard bundle (551 bundles / **246 modules**, `outputs/_r472_family.txt`) was regenerated (`_r472_regen.sh`, 24 batches, 4 workers, 6 min) + the 12-module spot-check: 0 truly stale, spot-check 12 / 12 byte-identical; `scoped_ship.sh` **PASS** (31 changed ⊆ 246 affected).
- The flipCard verifier over the WHOLE family (`_r472_verify_family.sh`): card-texts 2125 → 2256, **exact 1213 → 1291**, copy-edit 184 → 175, gold-subst 206 → 241, defect 359 → 360 (SSCI205 +2 — its restored cards carry wording the gold edited; ENFUN01 −1), divergence 163 → 189 (CEDO301 / MXEX201 / SSOG103 — modules whose human built NO flipCard, now carrying the writer's full text; "not a defect" by the verifier's own rule). The protected 4-module set: **exact 32 → 39, copy-edit 11 → 4** (MXDB302's escaped breaks), defect 18, divergence 0 ✓.

### 3. PROTECTED GATES

- Skeleton **55.2245 % → 55.2277 % @ 2491 (+0.0032pp)**, RAW 39.194 → 39.200 %; ≥50 1576, ≥75 276, ≥90 25; 9 movers, **8 up / 1 down**: OSGM401_2_0 +2.2, ENGI302_5_0 +1.3, ENGC201_3_0 +1.2, SSOG105_4_0 +1.0, CEDO502_5_0 +0.9, SSOG103_2_0 +0.6, OSAI101_2_0 +0.6, SSCI205_3_0 +0.5; **AGH1006_2_0 −0.3 NAMED** (the writer's closing sentence, restored as a `<p>` the gold dropped — constraint 1); movers outside the affected set 0.
- compare_structure 16757 / 208 / 903 / 24, body 61 / 5 / 175 / 238, clean 2587 / 2633, leak 75 / 46 — all EXACT; every verifier RESULT line identical to r470; 17 selftests + the skeleton selftest green (50 PASS / 0 FAIL); the feature index green; the miner 197 CANDIDATE @ 2491.
- Plateau (§4): a widget-correctness round, skeleton-blind by design (a widget is one WIDGET line) — neither counts nor resets: **2 of 3** stands.

**Ledger:** scoped #5 since the r460 FULL · data `Emit_Templates.flipCard.text_guard`, `Emit_Templates._tag_words_note.covering_note_min_words` · env `FLIPTEXTGUARD_OFF` · code `InteractiveBuilder.#flipCard / #flipTextLost / #flipLearnerParts / #flipNoteRows / #flipWithNotes / #flipVisible / #looksLikeFlipHeader / #flipTableCards (T1b) / #flipCell / #tagWordsNote` · tools `outputs/_s43_widgetloss.cjs`, `_s43_wl_{run.sh,report.py,compare.py}`, `_s43_family.cjs`, `_s43_fam_{run.sh,report.py}`, `_s43_flipdump.cjs`, `_r472_{measure,regen,verify_family,postship}.sh`. **Follow-ups (recorded):** the same census's other types (carousel 130 lossy builds / 79 modules, modal 46, accordion 37, clickDrop 26, dropDown 18 — each its own measure: many are picture titles); SSOG103-4.0's red `(front)` / `(back)` face labels printed as card text.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
sj = sj.replace(oldj, "\t// ROUND 472 (260620.36): THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS (session 43 Round 1; the placement-census lane). "
                "flipCard.text_guard — a lossy dialect build falls through to the composer, a lossy composer build keeps the box; the header row, "
                "the stacked face column, the escaped <br>, the spanning note row and the tag-line note's covering test fixed. Env FLIPTEXTGUARD_OFF.\n"
                '\tstatic AppVersion = "260620.36";')
wr(PJ, sj); print("config ok")
so = so.replace(a9, "| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 472 BASELINE (the built flip card never drops the "
                "writer's words, `FLIPTEXTGUARD_OFF`; SCOPED, scoped #5 since the r460 FULL — the 246-module flipCard family regenerated): SCAFFOLD "
                "mean 55.2277% / >=50% 1576 / >=75% 276 / >=90% 25 / RAW 39.200% @ 2491 pairs — +0.0032pp, 8 up / 1 down (AGH1006_2_0 −0.3 NAMED: "
                "the restored closing sentence); cs / body / clean / leak EXACT; flipCard verifier exact 32 → 39, copy-edit 11 → 4.** Previous: "
                "**ROUND 470 BASELINE")
so = so.replace(a11, "| `FLIPTEXTGUARD_OFF` | 472 | **THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS** (session 43 Round 1; the placement-census "
                "lane). Reverts `flipCard.text_guard` (the text guard; `header_black_label`, `face_column_pairs`, `br_after_inline`, "
                "`note_rows_after`) and `_tag_words_note.covering_note_min_words`: 24 flipCard builds lose writer text again (CEDO502-5.0's one "
                "two-picture card), the escaped `&lt;br&gt;` returns (145 on 10 pages) and 9 Writers Notes lose the writer's instruction; "
                "byte-identical to r470. |\n" + a11)
so = so.replace(a14, "- **Build:** `260620.36` (round 472 — **THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS** (a text guard + the header "
                "row / stacked face column / escaped `<br>` / spanning note row / tag-note covering fixes); `FLIPTEXTGUARD_OFF`; scoped #5 since "
                "the r460 FULL; the 246-module flipCard family regenerated, 37 pages / 31 modules changed; skeleton 55.2277 % @ 2491).\n" + a14)
wr(PO, so); print("OG ok")
P = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests", "gate_baseline.json"); shutil.copyfile(P, P + ".pre-r472.bak")
G = rd(P).split("\n")
def setv(key, old, new, after=0):
    for i, l in enumerate(G):
        if i < after: continue
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            G[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}'); return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(G):
        if l.strip().startswith(f'"{key}": '): G.insert(i, line); return
    raise SystemExit(f"anchor {key}")
setv("build", '"260620.35"', '"260620.36"'); setv("round", "470", "472")
insert_before("_note_r470", '    "_note_r472": "Round 472 (session 43 Round 1, 2026-09-24; the placement-census lane) — THE BUILT FLIP CARD NEVER DROPS THE '
              'WRITER\'S WORDS (FLIPTEXTGUARD_OFF): the 246-module flipCard family regenerated, 37 pages / 31 modules changed; SCAFFOLD 55.2245 -> '
              '55.2277 @ 2491 (+0.0032pp, 8 up / 1 down: AGH1006_2_0 -0.3 NAMED, the restored closing sentence), RAW 39.194 -> 39.200; cs / body / '
              'clean / leak EXACT; flipcard exact 32 -> 39, copy_edit 11 -> 4 (defect 18, divergence 0); scoped #5 since the r460 FULL.",')
setv("mean_scaffold_pct", "55.22", "55.23"); setv("raw_mean_pct", "39.19", "39.2")
insert_before("_note_r470_state", '    "_note_r472_state": "r472 (the flip-card text guard): SCAFFOLD 55.2277 @ 2491, RAW 39.200; 9 movers (8 up / 1 down).",')
k = [i for i, l in enumerate(G) if l.strip().startswith('"flipcard": {')]; assert len(k) == 1
setv("exact", "32", "39", after=k[0]); setv("copy_edit", "11", "4", after=k[0])
out = "\n".join(G); json.loads(out); wr(P, out); print("gate_baseline ok")
shutil.copyfile(S, S + ".pre-r472-finalise.bak")
i = find("- **ROUND 472 IN FLIGHT — NOT PROVEN**"); marker = L[i]
L[i] = ("- **No round in flight** (24 Sept 2026 ≈19:25, session 43 Round 1 — r472 (the flip-card text guard) SHIPPED and committed; the "
        "in-flight marker is cleared). LAST SHIPPED **r472** (260620.36); **LAST FULL = r460**; ledger **scoped #5** since it (3 of headroom). "
        "Ride-along patches `outputs/_r469_declined.patch` (alerts, 7 pages) / `_r469b_declined.patch` (buttons, 10 pages) / "
        "`_r468_declined.patch` (the lesson menu's `[H2]` lead, 3 pages).")
k = find("- **Before r472:**"); prior = L[k]; del L[k]
k = find("- Before it: **r467**"); r467 = L[k]; del L[k]
k = find("- LAST SHIPPED: **r470**"); L[k] = L[k].replace("- LAST SHIPPED: **r470**", "- Before it: **r470**", 1)
L.insert(k, "- LAST SHIPPED: **r472** (build 260620.36, 24 Sept ≈19:25, session 43 Round 1 — THE BUILT FLIP CARD NEVER DROPS THE WRITER'S "
         "WORDS, `FLIPTEXTGUARD_OFF`: the flipCard text guard + the header row / stacked face column / escaped `<br>` / spanning note row / "
         "tag-note covering fixes; SCOPED, **scoped #5 since the r460 FULL** (the 246-module flipCard family regenerated), scoped_ship PASS; "
         "**skeleton 55.2245 → 55.2277 % @ 2491 (+0.0032pp, 8 up / 1 down — AGH1006_2_0 −0.3 NAMED)**, ≥50 1576, ≥75 276, ≥90 25, RAW "
         "39.200 %; cs / body / clean / leak EXACT; flipCard lossy builds 46 → 22 with 290 → 290 built; verifier exact 32 → 39; escaped "
         "`&lt;br&gt;` 145 → 0; `gate_baseline.json` at r472; the miner 197 CANDIDATE).")
k = find("- Before them: **r461 / r460 / r459")
L[k] = L[k].replace("- Before them: **r461 / r460 / r459", "- Before them: **r467** (260620.34, KB c67 the canonical Standards tab, skeleton "
                    "exact, menu-only 24 up / 16 down — verbatim → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED r467 (verbatim, s43 r472)'), "
                    "**r461 / r460 / r459", 1)
k = find("- Plateau window (§4): **2 of 3** — r470")
L[k] = L[k].replace("- Plateau window (§4): **2 of 3** — r470", "- Plateau window (§4): **2 of 3** — r472 a widget-correctness round "
                    "(skeleton-blind by design, +0.0032pp; neither counts nor resets); r470", 1)
k = find("- Standing facts: AppVersion 260620.35")
L[k] = L[k].replace("- Standing facts: AppVersion 260620.35 (r470", "- Standing facts: AppVersion 260620.36 (r472 the flip-card text guard — "
                    "session 43 Round 1, 24 Sept); before it 260620.35 (r470", 1)
k = find("## Round log")
L.insert(k + 1, "- s43-r1 (engine r472, build 260620.36, 24 Sept 18:12 → ≈19:25) · THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS (the "
         "placement census's `flipCard → ABSENT-inWT` row; CEDO502's four cards shipped as one two-picture card) · SHIPPED scoped #5 (the "
         "246-module family regenerated; 37 pages / 31 modules changed) · flipCard lossy builds 46 → 22, built 290 → 290 · skeleton +0.0032pp "
         "(8 up / 1 down) · plateau 2 of 3 (neither).")
k = find("**Next session starts with:**")
L[k] = ("**Next session starts with:** (provisional — rewritten at the stop) the standing `/loop-start`. LAST SHIPPED **r472** (260620.36, "
        "the flip-card text guard); LAST FULL = **r460**; ledger scoped #5; plateau **2 of 3**; 2,491 pairs; census 552 / 545 / 2,679. Ride-along "
        "patches `_r469_declined.patch` (alerts) / `_r469b_declined.patch` (buttons) / `_r468_declined.patch`. Needs Chris #17–#19, #22.")
# the PICK section → archive
k = find("## Session 43 — Round 1 PICK (engine r472)")
j = k + 1
while j < len(L) and not L[j].startswith("## "): j += 1
pick = L[k:j]; del L[k:j]
L.insert(k, "## Session 43 — Round 1 PICK (engine r472) — THE BUILT FLIP CARD NEVER DROPS THE WRITER'S WORDS — SHIPPED; the PICK + what-shipped "
         "record is in LOOP_STATE_ARCHIVE.md 'Session 43 — Round 1 PICK (engine r472) + what shipped'; the one-line summary is the s43-r1 "
         "Round-log line below.\n")
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Position — LAST SHIPPED r467 (verbatim, s43 r472)\n\n" + r467 + "\n"
    "\n## Session 43 — Round 1 PICK (engine r472) + what shipped\n\n" + marker + "\n" + prior + "\n" + "\n".join(pick[1:]).rstrip() + "\n"
    "- **What shipped (r472, 260620.36):** `flipCard.text_guard` (a lossy dialect build falls through to the composer; a lossy composer "
    "build keeps the box) + `header_black_label` / `face_column_pairs` / `br_after_inline` / `note_rows_after` + "
    "`_tag_words_note.covering_note_min_words`, one env `FLIPTEXTGUARD_OFF`. Probe OFF 3222 identical / ON 37 pages / 31 modules; the "
    "246-module family regenerated; scoped_ship PASS; lossy flipCards 46 → 22 (24 lossless, 6 fewer, 0 boxed), built 290 → 290; the "
    "escaped `&lt;br&gt;` 145 → 0; skeleton +0.0032pp (8 up / 1 down, AGH1006_2_0 −0.3 NAMED); verifier exact 32 → 39.\n")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
