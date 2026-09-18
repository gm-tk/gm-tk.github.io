#!/usr/bin/env python3
"""Session 26 Round 8 (r394) — LOOP_STATE.md: archive the Round 8 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r8 (engine r394)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 8 PICK (engine r394)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r394, build 260619.65, 19 Sept ≈04:30 NZST):** data `interactive.clickDrop.no_row_wrapper {enabled, env CDROW_OFF}` + "
           "`InteractiveBuilder.#cdWrap(tpl)` feeding both clickDrop emit sites an empty wrapper (`_s26_r394_splice.py`). Probe OFF 2109 / 2109; ON 122 pages / "
           "77 modules; scored before the regen: 88 up / 29 down / 1 same, pp-sum +221.9. SCOPED regeneration of the 77 (7 batches rc 0; `fresh --affected` 0 truly "
           "stale; manifest diff = 122 pages / 77 modules; probe ON == disk 445 / 445). Skeleton 53.560 → 53.674 (+0.114pp), ≥50 1159 → 1163 (7 up / 3 down), "
           "≥75 191 → 194, ≥90 15 → 18, ≥95 5 → 7, median 54.0 → 54.2, RAW 37.787 → 37.779 (the removed row line had been a coincidental raw match on some pages), "
           "1956 pairs / 0 skipped / 117 movers 84 up / 29 down / 0 outside (OSBY201_1_0 −6.2, MXFU301_7_0 −6.1, BLL217_2_0 −5.1 = the gate's alignment "
           "re-pairing after the row line goes; SCPH301_0_0 +32.3, SCCH301_0_0 +25.8, ENGR302_2_0 +14.8); compare_structure 11723 / 172 / 626, body_compare "
           "42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; every verifier RESULT identical to r393 (the clickDrop verifier included); 15 "
           "selftests + the index selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #6 since the r388 full (2 of headroom); the miner "
           "re-mined 174 CANDIDATE rows (GONE #3699 = the lead, #683 / #684 / #3687 = the panels-under-the-row shadows, #3684 / #3725 under the floor; NEW #3633 "
           "`body EXTRA div.col-12.col-md-8 › div.clickDropContent` 25 pages / 21 modules = the panels' own alignment residue now that they sit in the column "
           "(ARFUN04's page-pairing mismatch, CEDO502's slash-led item; verifier-owned content) and #3606 `body MISSING div#body › div.inquiryPanel` 29 pages / 26 "
           "modules — consensus 0.02 corpus-wide, Inquiry 0.34, Te ara Whakapuawa 0.75 on 5 pages: under consensus everywhere at the floor); checksums refreshed; "
           "finalise = changelog entry `_s26_r394_entry.md`, AppVersion 260619.65, CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md. Plateau window "
           "reset to 0 of 3.\n")
a = rd(AR)
if "## Session 26 — Round 8 PICK (engine r394) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 8 PICK (engine r394) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈04:30 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r393)"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, old.replace("r387–r393", "r387–r394", 1), 1)
line = ("- s26-r8 (engine r394) · THE CLICKDROP BUTTONS SIT DIRECTLY IN THE COLUMN (the built widget's inner `div.row` dropped; the gold's 385 groups: parent = a "
        "column 0.78, an inner row 0.05, every subject ≥ 0.73; Claude wrapped 127 / 128); data `interactive.clickDrop.no_row_wrapper`, env `CDROW_OFF` · SHIPPED 19 "
        "Sept · ON 122 pp / 77 mods (88 up / 29 down, +221.9); SCOPED (#6 since r388) · skeleton 53.560→53.674 (+0.114), ≥50 +4, ≥75 +3, ≥90 +3; all else EXACT, "
        "every verifier RESULT identical · build 260619.65\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r7 (engine r393)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r393**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r394** (build 260619.65, 19 Sept ≈04:30, session 26 Round 8 — the clickDrop buttons sit directly in the column; r393 a glyph-only line "
       "renders nothing; r392 adjacent sibling lists are one list; r391 the own-row supervisor panel's text column in Leaving to Learn; r390 the supervisor "
       "note's explicit closer; r389 the built flipCard group closes its column; r388 the plain / solid alert (the FULL backstop); r387 the whakataukī; r386 the "
       "skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 the "
       "reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` heading "
       "opener) — SCOPED regeneration of 77 modules (the ledger at scoped #6 since the r388 FULL, 2 of headroom — the ship after next must be a FULL "
       "regeneration). **Corpus = r394** (2109 pages / 416 modules). Gates at r394 (`gate_baseline.json`): skeleton **53.674 %** / ≥50 **1163** / ≥75 **194** / "
       "≥90 **18** @ 1956 pairs; RAW 37.779 %; compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean "
       "2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.4 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈04:25 "
       "on the r394 corpus (`_diff_miner_s26_r394.log`: 1956 pairs / 8076 classes / **CANDIDATE 174** — #3699 + the three panels-under-the-row shadows GONE, "
       "#3684 / #3725 under the floor; TWO new: #3633 `body EXTRA div.col-12.col-md-8 › div.clickDropContent` (25 pages / 21 modules — the clickDrop panels' own "
       "alignment residue now that they sit in the column; ARFUN04's page-pairing mismatch, CEDO502's slash-led item; the widget's content is verifier-owned) — "
       "DISPOSITION: measure the panel COUNT Claude vs gold per group before any code; #3606 `body MISSING div#body › div.inquiryPanel` (29 pages / 26 modules; "
       "consensus 0.02 corpus-wide, Inquiry 0.34, Te ara Whakapuawa 0.75 on 5 pages) — DISPOSITION: under consensus in every group at the floor, not a PICK; "
       "`_s26_r394_queue_delta.log`; the pre-r394 queue kept at `_diff_queue_pre_r394.md`); every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r394 +0.114pp with ≥50 +4 / ≥75 +3 / ≥90 +3 — reset; r393 +0.0065pp with ≥50 −1 had counted 1; r392 +0.028pp; r391 "
       "+0.008pp but ≥50 +1; r390 +0.047pp).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.64;", "- Standing facts: AppVersion 260619.65;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈03:30 on the r393 corpus, 178 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈04:25 on the r394 corpus, 174 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
