#!/usr/bin/env python3
"""Session 26 Round 9 (r395) — LOOP_STATE.md: archive the Round 9 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r9 (engine r395)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 9 PICK (engine r395)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r395, build 260619.66, 19 Sept ≈04:55 NZST):** data `interactive.flipCard.card_col_by_count {enabled, env FLIPCOL_OFF, default, "
           "by_count {2, 4 → col-md-6 col-12 paddingLR}, exclude_subjects_by_count {2: [NCEA1, the subject-less], 4: [1-10 English, ConnectED, NCEA1]}}` + "
           "`InteractiveBuilder.#flipCardsByCount(tpl, cards, run)` at the four `tpl.card` join sites (`_s26_r395_splice.py` + `_splice2.py`). The first cut "
           "(no exclusions) scored 20 up / 4 down with every dip an English 4-card page (the gold's English 4-card form is a TIE, col-md-6 10 / col-md-3 9) → "
           "the per-subject census in full → the exclusions; the second cut: probe OFF 2109 / 2109; ON 39 pages / 37 modules; scored before the regen 15 up / 1 "
           "down / 22 same, pp-sum +19.4. SCOPED regeneration of the 37 (4 batches rc 0; `fresh --affected` 0 truly stale; manifest diff = 39 pages / 37 modules; "
           "probe ON == disk 202 / 202). Skeleton 53.674 → 53.684 (+0.010pp), ≥75 194 → 195 (OSOH201_2_0 up), ≥50 1163 / ≥90 18 EXACT, median 54.2 → 54.3, RAW "
           "37.779 → 37.784, 1956 pairs / 0 skipped / 16 movers 15 up / 1 down (TEFUN08_0_0 −0.2) / 0 outside; compare_structure 11723 / 172 / 626, body_compare "
           "42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; every verifier RESULT identical to r394 (the flipCard verifier included); 15 "
           "selftests + the index selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #7 since the r388 full — THE NEXT SHIP MUST BE A "
           "FULL REGENERATION; the miner re-mined 173 CANDIDATE rows (#3649 `body EXTRA div.flipCardsContainer.row › div.col-12.col-md-4.paddingLR` GONE; nothing "
           "new); checksums refreshed; finalise = changelog entry `_s26_r395_entry.md`, AppVersion 260619.66, CLAUDE.md §9 / §11 / §14, gate_baseline.json, "
           "loop/README.md. Recorded: 1-card groups → col-md-12 (gold 0.63 on 16 pages; Claude 8 pages) under the floor. Plateau window 0 of 3 (≥75 moved).\n")
a = rd(AR)
if "## Session 26 — Round 9 PICK (engine r395) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 9 PICK (engine r395) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈04:55 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r394)"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, old.replace("r387–r394", "r387–r395", 1), 1)
line = ("- s26-r9 (engine r395) · THE FLIP-CARD COLUMN WIDTH FOLLOWS THE CARD COUNT (a 2-card / 4-card group's cards are `col-md-6`, the gold 0.86 / 0.76; "
        "English's 4-card tie, ConnectED / NCEA1's col-md-3 lead, NCEA1 / TEDC's 2-card forms excluded; Claude was all col-md-4); data "
        "`interactive.flipCard.card_col_by_count`, env `FLIPCOL_OFF` · SHIPPED 19 Sept · ON 39 pp / 37 mods (15 up / 1 down, +19.4); SCOPED (#7 since r388 — "
        "the next ship is the FULL backstop) · skeleton 53.674→53.684 (+0.010), ≥75 +1; all else EXACT · build 260619.66\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r8 (engine r394)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r394**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r395** (build 260619.66, 19 Sept ≈04:55, session 26 Round 9 — the flip-card column width follows the card count; r394 the clickDrop "
       "buttons sit directly in the column; r393 a glyph-only line renders nothing; r392 adjacent sibling lists are one list; r391 the own-row supervisor "
       "panel's text column in Leaving to Learn; r390 the supervisor note's explicit closer; r389 the built flipCard group closes its column; r388 the plain / "
       "solid alert (the FULL backstop); r387 the whakataukī; r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 "
       "declined inert; r383 the long first row is a data row; r382 the reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; "
       "r378 the post-table body; r377 the `[Hn] Activity <id>` heading opener) — SCOPED regeneration of 37 modules (the ledger at scoped #7 since the r388 "
       "FULL — **THE NEXT SHIP MUST BE A FULL REGENERATION**). **Corpus = r395** (2109 pages / 416 modules). Gates at r395 (`gate_baseline.json`): skeleton "
       "**53.684 %** / ≥50 **1163** / ≥75 **195** / ≥90 **18** @ 1956 pairs; RAW 37.784 %; compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap "
       "23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.4 % of "
       "achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈04:50 on the r395 corpus (`_diff_miner_s26_r395.log`: 1956 pairs / 8071 classes / **CANDIDATE 173** — #3649 "
       "GONE, nothing new; `_s26_r395_queue_delta.log`; the pre-r395 queue kept at `_diff_queue_pre_r395.md`); every other disposition stands (#3633 the clickDrop "
       "panels' alignment residue — measure the panel COUNT per group first; #3606 the Inquiry `inquiryPanel` under consensus).\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r395 +0.010pp but ≥75 +1 moved — not a plateau round; r394 +0.114pp reset the window; r393 +0.0065pp with ≥50 −1 had "
       "counted 1; r392 +0.028pp; r391 +0.008pp but ≥50 +1).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.65;", "- Standing facts: AppVersion 260619.66;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈04:25 on the r394 corpus, 174 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈04:50 on the r395 corpus, 173 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
