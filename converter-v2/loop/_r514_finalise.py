#!/usr/bin/env python3
"""ROUND 514 finalise (session 50 Round 6 — THE WRITERS' MISSING SPELLINGS OF FIVE WIDGET TAGS, SPELLALIAS_OFF). WSL. argv: MEAN RAW."""
import sys
import _s50_fin as F
MEAN, RAW = sys.argv[1], sys.argv[2]
T = F.now()
entry = f"""## 2026-09-26 (round 514, build 260620.76) — THE WRITERS' MISSING SPELLINGS: `[type and check]`, `[click drops]` / `[clickdrops]`, `[radioquiz]`, `[carrousel]` now name their widget (a toggled-alias group that only FILLS a span with no widget or closer); 45 modules; skeleton +0.0455pp

### 1. WHAT CHANGED

**Found by** the widened recognition census (`outputs/_s50_r4_unresolved.cjs`: 3,313 red brackets resolve to NO tag / 420 modules). Five spellings of existing widget tags the alias lists lacked, each checked against the gold's own widgets in the modules that use it: **`[type and check]`** (46 spans / 7 modules — MXEO201, MXEX302, MXFL203, MXFUN01–03, SSCI205; the gold builds typing quizzes there) → `typing quiz`; **`[click drops]` / `[clickdrops]`** (16 / 7) → `click drop`; **`[radioquiz]`** (8 / 6) → `radio quiz`; **`[carrousel]`** (3 / 3) → `carousel`. `[checkboxes]` (15 / 11) is NOT added — the gold builds multiChoiceQuiz or selectionBox for it, no single target. KB c14 (the writer's tag decides the component); the lexicon's own extension rule (a new writer phrasing = one alias).

**The mechanism** (`TagNormaliser` constructor + `Parse`; data `Tag_Lexicon.json _meta.toggled_aliases` [{{tag, aliases, env}}], NEW; env `SPELLALIAS_OFF`): a toggled alias group is merged into the alias map unless its env toggle is set, so the OFF corpus stays the last shipped state; its tags carry a `toggled` mark, and **a toggled spelling only FILLS a span that resolved to no widget and no closer — it never competes with one**. The first probe (without that rule) turned `[click drops end here]` / `[modals and click drops end here]` into openers (MXDB302_1_0 absorbed five widget types) and gave `[Clickdrops or Tabs]` a second widget; with it, those spans parse exactly as before while `[end click drops]` becomes the more specific `end click drop` closer.

### 2. PROOF

- In-memory probe: `SPELLALIAS_OFF=1` → the 45 modules' 288 comparable files equal the shipped manifest's md5s (0 differ); corpus-wide the OFF probe changes nothing outside them. ON → **45 modules** (`outputs/_affected_r514.txt`; `_s50_r514_spans.cjs`: 160 spans change parse). `scoped_ship.sh … --round 514` PASS (0 stale, containment 45 ⊆ 45, the 12-module spot-check byte-identical).
- Widgets over the 45 (OFF → ON): clickDrop built 58 → 65, items 84 → 107, defect 0; carousels 70 → 73 (the 5 mismatched slide ids are pre-existing, equal OFF and ON); typing 0 → 0 (its builder reads red answers only — the new `typing` hand-offs name the writer's widget).

### 3. PROTECTED GATES

- **Skeleton 55.6929 → {MEAN} % @ 2486 (+0.0455pp)** — 49 movers, 36 up / 13 down, +113.1pp-sum; **≥50 1607 → 1612** (7 up-crossings, HPFUN203_0_0 50.0 → 49.0 down); **≥75 281 → 283** (SCPH301_4_0 57.5 → 79.6, SCBI301_7_0 71.2 → 75.1); ≥90 26; **RAW 39.539 → {RAW} %**. The largest down movers — MXFU202_8_0 46.6 → 39.8, PWY1001_1_3_0 46.8 → 41.3, XFUN02_4_0, TEDC401_4_0 — each a writer's widget now captured into its named hand-off box (A1).
- **compare_structure exact 16768 → 16769, missing 887 → 886**, EXTRA 204.
- **body_compare ANY 233 → 236 (+3), NAMED** (`_s50_bcsplit.py` / `_s50_bcpages.py`): TEDC401_6_0 — the SAME 3,674-char box, its label now listing a fourth type (`+ clickDrop`), which trips the 4-type line; ANZH302_10_0 — the writer's `[Carrousel]` box holds exactly its own "Please create a carrousel of these three sources" and the three sources (279 chars), and the page's older 1,373-char box (57 % before, 58 % after) now counts three blocks lost; CEDR501_2_1 — its two clickDrop boxes (1,569 + 1,347) become one of 3,018 at the writer's second `[Clickdrops]`.
- Clean / leak EXACT; tags 9557; every verifier ✓, every COUNT held (`_r514_gates.log`); aggregates written by `scoped_ship.sh … --commit --round 514 --accept-named`; `--gate-baseline-check` PASS. Plateau: **reset** (a real gain).

**Ledger:** scoped #1 since the r513 FULL · data `Tag_Lexicon.json _meta.toggled_aliases` · env `SPELLALIAS_OFF` · code `TagNormaliser` (constructor, `#matchOne`, `#resolveFragment`, `Parse`) · tools `_s50_r4_unresolved.cjs`, `_s50_r514_spans.cjs`, `_r514_finalise.py` · session 50 Round 6.
"""
F.finalise(
    N=514, old_build="260620.75", new_build="260620.76", entry=entry,
    config_comment="THE WRITERS' MISSING SPELLINGS (session 50 Round 6): `[type and check]`, `[click drops]`, `[radioquiz]`, `[carrousel]` "
                   "name their widget — a toggled alias only fills a span with no widget or closer. Env SPELLALIAS_OFF.",
    og9=f"| **Skeleton (PRIMARY)** | `python3 _skeleton_compare.py` | **ROUND 514 BASELINE (the writers' missing spellings, `SPELLALIAS_OFF`; "
        f"SCOPED, scoped #1 since the r513 FULL): SCAFFOLD mean {MEAN}% / >=50% 1612 / >=75% 283 / >=90% 26 / RAW {RAW}% @ 2486 pairs "
        f"(+0.0455pp, 36 up / 13 down); cs exact 16769 (+1), missing 886 (−1); body ANY 236 (+3 NAMED).**",
    og11="| `SPELLALIAS_OFF` | 514 | **THE WRITERS' MISSING SPELLINGS OF FIVE WIDGET TAGS** (session 50 Round 6). Drops the "
         "`Tag_Lexicon _meta.toggled_aliases` groups from the alias map: `[type and check]` / `[click drops]` / `[clickdrops]` / "
         "`[radioquiz]` / `[carrousel]` resolve to no tag again; byte-identical to r513. |",
    og14=f"- **Build:** `260620.76` (round 514 — **the writers' missing spellings**; `SPELLALIAS_OFF`; scoped #1 since the r513 FULL; 45 "
         f"modules; skeleton {MEAN} % (+0.0455pp), ≥50 1612, ≥75 283; body ANY 236 NAMED).",
    gb_note=f"Round 514 (session 50 Round 6, 2026-09-26) — THE WRITERS' MISSING SPELLINGS (SPELLALIAS_OFF): 45 modules; SCAFFOLD 55.6929 -> "
            f"{MEAN} @ 2486 (+0.0455pp, 36 up / 13 down), >=50 1607 -> 1612, >=75 281 -> 283, RAW 39.539 -> {RAW}; cs exact 16768 -> 16769, "
            f"missing 887 -> 886; body ANY 233 -> 236 NAMED (TEDC401_6_0 label count, ANZH302_10_0 / CEDR501_2_1 capture artefacts); scoped #1.",
    no_round=f"- **No round in flight** (26 Sept 2026 {T}, session 50 Round 6 — r514 (the writers' missing spellings) SHIPPED and committed; "
             "the in-flight marker is cleared). LAST SHIPPED **r514** (260620.76); **LAST FULL = r513 (the session-50 Round 5 backstop)**; "
             "ledger **scoped #1** (7 of headroom). Ride-along patches (LOOP §3 step 1 reads this list at every PICK): "
             "`outputs/_r469_declined.patch` (alerts, 7 pages — ANZH301 / 302, ENGC403) / `_r469b_declined.patch` (buttons, 10 pages / 9 "
             "modules — CEDK401, HIS1002, HPRE203, MXDI201, MXDI202 ×2, MXEX302, SSOG105, TWHA906, XGF9004) / `_r468_declined.patch` (the "
             "lesson menu's `[H2]` lead, 3 pages — CBI1008 L1 / L2, PES1004_8_0) / `_r489_accbullet_declined.patch` (the accordion bulleted "
             "bold lead, 8 accordions / 4 modules — MXEX302, ENGS101, XGF9003, XLP05) / `_r463_declined.patch` (the WJFUN tile's \"Year N\" "
             "lead, 1 page) / `_r512_declined.patch` (the `[Activity: Embedded] <widget>` bracket, 10 modules — rides only after the TRR "
             "table-dialect ownership fix). Checked at r514 (45 modules): r469 (ENGC403 outside) and r469b (CEDK401, HIS1002 … outside) "
             "are not wholly inside; none rides.",
    last_shipped=f"- LAST SHIPPED: **r514** (build 260620.76, 26 Sept {T}, session 50 Round 6 — THE WRITERS' MISSING SPELLINGS OF FIVE WIDGET "
                 "TAGS, `SPELLALIAS_OFF`; SCOPED, **scoped #1 since the r513 FULL**; 45 modules; clickDrop built 58 → 65 on them; "
                 f"**skeleton 55.6929 → {MEAN} % (+0.0455pp)**, 36 up / 13 down, **≥50 1612 (+5)**, **≥75 283 (+2)**; cs exact +1, "
                 "missing −1; body ANY +3 NAMED).",
    before_them_add="D15-19 the yellow-✅ dropDown quiz",
    plateau="- Plateau window (§4): **0 of 3** — r514 +0.0455pp (a real gain: reset); ",
    standing="- Standing facts: AppVersion **260620.76** (r514 the writers' missing spellings — session 50 Round 6, 26 Sept); before it "
             "260620.75 (",
    roundlog=f"- s50-r6 (engine r514, build 260620.76, 26 Sept 02:34 → {T}) · THE WRITERS' MISSING SPELLINGS (`[type and check]`, `[click "
             "drops]`, `[radioquiz]`, `[carrousel]` — a toggled alias that only fills a span with no widget or closer; the first probe's "
             "closer-turned-opener fixed) · SHIPPED scoped #1 · 45 modules · skeleton **+0.0455pp**, ≥50 +5, ≥75 +2, cs exact +1, body ANY "
             "+3 NAMED · plateau reset (0 of 3).",
    archive_extra="- **What shipped (r514, 260620.76):** `Tag_Lexicon _meta.toggled_aliases` (SPELLALIAS_OFF); `TagNormaliser` constructor / "
                  "`#matchOne` / `#resolveFragment` / `Parse`. Probe OFF = manifest; ON 45 modules; +0.0455pp.",
)
