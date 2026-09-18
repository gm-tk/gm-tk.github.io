#!/usr/bin/env python3
"""Session 26 Round 3 (r389) — LOOP_STATE.md: archive the Round 3 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r3 (engine r389)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 3 PICK (engine r389)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r389, build 260619.60, 19 Sept ≈01:35 NZST):** data `body_region.row_breaks.after_built_widgets` (rule: class_match "
           "`\\bflipCardsContainer\\b`, templates [Standard], exclude_subjects [Leaving to Learn, NCEA1, 1-10 English]; env `FLIPBREAK_OFF`) + "
           "`ContentConverter.#breaksAfterBuilt(html, run)` at the INLINE widget site (`_s26_r389_splice.py`). Probe OFF 2109 / 2109; ON first cut 54 pages / "
           "40 modules scored 26 up / 26 down (+22.5) → by subject: LtL 0 / 13 (−5.3), NCEA1 0 / 3, English 3 / 4 (a tie) EXCLUDED on the scorer; OS 12 / 4 "
           "(+15.1), ConnectED 6 / 0 (+10.7), Maths 2 / 0, Science 1 / 0, TEDC 2 / 2 kept → ON 29 pages / 21 modules, 23 up / 6 down, pp-sum +30.7. SCOPED "
           "regeneration of the 21 (4 batches rc 0; `fresh --affected` 0 truly stale; manifest diff = 29 pages / 21 modules; probe ON == disk 155 / 155). "
           "Skeleton 53.455 → 53.470 (+0.016pp = the prediction), ≥50 1155 → 1157 (CEDO501_2_0, MXFL301_1_0 up), ≥75 192 → 191 (OSAH301_1_0 76.2 → 73.4 — "
           "the gold-flow minority, accepted BY NAME, the r338 / r342 precedent), ≥90 15, RAW 37.719 → 37.725, 1956 pairs / 0 skipped / 0 movers outside the "
           "affected set; compare_structure 11643 / 172 / 625, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; every verifier "
           "RESULT identical to r388; 15 selftests + the skeleton selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #1 since the "
           "r388 full; the miner re-mined 177 CANDIDATE rows (178 → 177, 0 new — the `body MISSING col-md-8 › WIDGET` row (OS lessons c = 0.65) fell below "
           "consensus); checksums refreshed (engine 3 changed); finalise = changelog entry `_s26_r389_entry.md`, AppVersion 260619.60, CLAUDE.md §9 / §11 / "
           "§14, gate_baseline.json, loop/README.md.\n")
a = rd(AR)
if "## Session 26 — Round 3 PICK (engine r389) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 3 PICK (engine r389) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈01:35 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
stub = ("## Session 26 — Round 3 (engine r389) SHIPPED — its PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md ('Session 26 — Round 3 PICK (engine r389) + "
        "what shipped'); the one-line summary is in the Round log below.\n")
s = s[:i] + stub + s[j:]
line = ("- s26-r3 (engine r389) · THE BUILT FLIPCARD GROUP CLOSES ITS COLUMN — prose after `div.row.flipCardsContainer` opens a new row (paired 0.82, gold "
        "LAST-or-only 0.75; the one built widget whose after-rule the gold breaks; LtL / NCEA1 / English excluded on the scorer); data "
        "`row_breaks.after_built_widgets`, env `FLIPBREAK_OFF` · SHIPPED 19 Sept · ON 29 pp / 21 mods (23 up / 6 down, +30.7); SCOPED (#1 since r388) "
        "· skeleton 53.455→53.470 (+0.016), ≥50 +2, ≥75 −1 named; all else EXACT · build 260619.60\n")
assert len(line) <= 512, len(line)
anchor = "- s26-r2 (engine r388)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r388**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r389** (build 260619.60, 19 Sept ≈01:35, session 26 Round 3 — the built flipCard group closes its column; r388 the plain / solid alert "
       "(the FULL backstop); r387 the whakataukī; r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; "
       "r383 the long first row is a data row; r382 the reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the "
       "post-table body; r377 the `[Hn] Activity <id>` heading opener) — SCOPED regeneration of the 21 flipCard modules (the ledger at scoped #1 since the r388 "
       "FULL, 7 of headroom). **Corpus = r389** (2109 pages / 416 modules). Gates at r389 (`gate_baseline.json`): skeleton **53.470 %** / ≥50 **1157** / ≥75 "
       "**191** / ≥90 **15** @ 1956 pairs; RAW 37.725 %; compare_structure exact 11643 (EXTRA 172 / MISSING 625 / row-wrap 23); body_compare 218 / 42 / 4 / 173; "
       "clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.2 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept "
       "≈01:27 on the r389 corpus (`_diff_miner_s26_r389.log`: 1956 pairs / 8154 classes / **CANDIDATE 177** — 178 → 177, 0 new; `_s26_r389_queue_delta.log`; "
       "the pre-r389 queue kept at `_diff_queue_pre_r389.md`); every disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r389 +0.016pp is under 0.02pp but ≥50 +2 / ≥75 −1 moved — §4 needs BOTH conditions, so not a plateau round; "
       "r388 +0.060pp / ≥50 +3 / ≥75 +3 and r387 +0.043pp / ≥75 +4 — not plateau rounds).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.59;", "- Standing facts: AppVersion 260619.60;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈00:57 on the r388 corpus, 178 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈01:27 on the r389 corpus, 177 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s), "bytes; archive:", len(a), "bytes")
