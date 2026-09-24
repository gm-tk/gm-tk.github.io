#!/usr/bin/env python3
"""Session 44 Round 2 — write the PICK (engine r479) + raise the in-flight marker in LOOP_STATE.md (§3 step 1). WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); shutil.copyfile(S, S + ".pre-r479-inflight.bak")
L = io.open(S, encoding="utf-8").read().split("\n")
k = [i for i, l in enumerate(L) if l.startswith("- **No round in flight** (25 Sept 2026 ≈00:05, session 44 Round 1")]; assert len(k) == 1
L.insert(k[0], "- **ROUND 479 IN FLIGHT — NOT PROVEN** (session 44 Round 2, 25 Sept ≈00:35): THE BILINGUAL PROVERB TABLE IS THE KB 07B "
         "WHAKATAUKĪ BOX. Files: `app/js/BilingualBuilder.js` (`bilingualRows` → a new `#proverbBox`), `data/Emit_Templates.json` "
         "`elements.dual_language.proverb_box` {enabled, env `PROVERBBOX_OFF`}. Affected: the Bilingual modules whose Writers Template "
         "carries a `[H1] Proverb ║ [H1] Whakataukī` row (21 of 23; TRR104 / TRR105 have no Claude build).")
p = [i for i, l in enumerate(L) if l.startswith("## Session 43 — Round 10 PICK (engine r478)")]; assert len(p) == 1
L[p[0]:p[0]] = [
 "## Session 44 — Round 2 PICK (engine r479) — THE BILINGUAL PROVERB TABLE IS THE KB 07B WHAKATAUKĪ BOX (IN FLIGHT)",
 "- **Lanes this pass (00:05 → 00:35):** the miner re-run on r478 (197 CANDIDATE, unchanged); the §1g placement census re-run "
 "(`_s44_placement.log`: 533 modules / 163,771 gold blocks — SAME 64,992 / MOVED 37,314 / OTHER-PAGE 8,175 / ABSENT-inWT 16,750); the "
 "LOSS LEDGER BY FAMILY re-cut on r478 (`_s44_r2_famloss.py`): BLL2 148 p 60.8 % (2.33pp), BLL1 150 p 63.5 %, **TRR1 68 p 41.6 % (1.59pp — "
 "the lowest-scoring large family; its 55 LESSON pages 18–51 %)**, HIS1 77 p 49.8 %, PES1, XDLS9 … — the TRR lesson pages (the r453 "
 "follow-up) had never been taken. `_s44_famdiff.py '^TRR1' --pages lesson` (the miner's line classes over one family) and three "
 "side-by-side dumps (`_s44_skdump.py` TRR116_4_0 / TRR102_1_0) triangulated them.",
 "- **Placement-census rows dispositioned this pass:** (a) `body:free → header:other` 121 headings / 48 modules (AGH1005_2_0 …): the "
 "gold's header title is the developer's own SHORT title (not in the WT — `header:other → ABSENT-notWT` 222) with the WT's `[H2]` kept "
 "as a body `<h3>`; Claude's header = the `[H2]` and the duplicate dropped = **KB c47 / D10-1, KB-correct — no class.** (b) `body:activity → "
 "body:free` TRR share: the MTK `Activity NX: ║ Ngohe NX:` + `[H2]` intro table (KB 07B 'Activity Structure') that the gold boxes TOGETHER "
 "with the following `[Activity: Embedded]` table — `_s44_r2_actlabel.py`: 52 such tables in TWO modules only (TRR116 43, TRR106 9), gold "
 "boxes the title 47 / 50, Claude 0 (free) — **below the floor (≈ 12 pages / 2 modules); recorded in Follow-up (a §1d family dialect "
 "candidate).**",
 "- **The class (TRIANGULATED TRR102 / TRR116 / PNR101):** 21 of the 23 Bilingual Writers Templates write the module's proverb as a "
 "bilingual table row `[H1] Proverb ║ [H1] Whakataukī | Whakatauākī:` followed by `[Body] <english proverb> ║ [Body] <māori proverb>` "
 "(`_s44_r2_proverb.cjs` → `_s44_r2_proverb.log`; TRR104 / TRR105 have no Claude build). **The gold renders a `div.whakatauki` on 23 / 23 "
 "Bilingual modules** (`_s44_r2_whakform.py` → `.log`): the heading row DROPPED, the box holds `p reo` + `p eng` (+ an author line "
 "`p > span reo + span eng` on TRR102 / 103 / 106, a plain `p` on PMT101; TRR107's `[H3]` + `[Body]` variant keeps h3 + p per language "
 "inside); commentary after the proverb flows OUTSIDE the box (TRR114). **Claude renders 0 boxes:** `h3 reo 'Whakataukī | Whakatauākī:'` + "
 "`h3 eng 'Proverb'` + loose `p`s in every one (the proverb table reaches `bilingualTable` / `bilingualRows` — `bilingualContainer` only "
 "fires on a leading `[Whakatauki]` TAG, which these tables never carry).",
 "- **Authority:** KB 07B §7 'Whakatauki / Proverb' ('Uses a dedicated component: `<div class=\"whakatauki\"><p reo>…</p><p eng>…</p>`', "
 "author line optional; the TRR107 h3 variation named) — §1b rank 1, and the gold agrees 23 / 23 (no override). Wrapper: the box sits "
 "in the table's own `row > col-md-8` (the KB snippet has no extra wrapper; the gold adds `col-md-12` on 13 / 23 — a split below 0.60, "
 "not derivable). Body class, 21 pages / 21 modules (at the 20-page floor); predicts a small skeleton move (h3 ×2 → the box line); "
 "plateau: a KB-rule round (neither counts nor resets).",
 "- **Fix (planned):** `BilingualBuilder.bilingualRows` — a row whose English cell reads `Proverb` and Māori cell `Whakataukī` / "
 "`Whakatauākī` (tags, bold, red markers stripped; data patterns) is dropped and the NEXT row renders as ONE `div.whakatauki`: the "
 "proverb paragraph(s) (joined while a quote is open — TRR203 / TRR304's two-line proverb), bold / italic stripped; a trailing short line "
 "(≤ 6 words, no terminal punctuation) in both cells = the author `p > span reo + span eng`; a heading-led cell (TRR107) keeps its "
 "h3 + p per language inside (reo block, then eng); any other paragraph = commentary AFTER the box (reo / eng interleaved); media after. "
 "Data `elements.dual_language.proverb_box`; env `PROVERBBOX_OFF` = the r478 bytes.",
 "",
]
io.open(S, "w", encoding="utf-8", newline="\n").write("\n".join(L)); print("ok", os.path.getsize(S))
