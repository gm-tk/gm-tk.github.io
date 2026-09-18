#!/usr/bin/env python3
"""Session 26 Round 5 (r391) — LOOP_STATE.md: archive the Round 5 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r5 (engine r391)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 5 PICK (engine r391)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r391, build 260619.62, 19 Sept ≈02:25 NZST):** data `callouts.by_tag.\"supervisor note\".inner_row.text_col_by_subject "
           "{enabled, env PANELCOL_OFF, by_subject: {Leaving to Learn: col-12 col-md-12}}` + `#calloutOpen`'s inner_row def swap rewriting the LAST "
           "`<div class=\"col-12\">` of the open string (`_s26_r391_splice.py`). Probe OFF 2109 / 2109; ON 28 pages / 6 modules (XDLS502 / 901 / 904 / 905 / "
           "906 / 911 — the other LtL panels are activity-owned, untouched by design); scored before the regen: 21 up / 2 down / 5 same, pp-sum +15.2. SCOPED "
           "regeneration of the 6 (1 batch rc 0; `fresh --affected` 0 truly stale; manifest diff = 28 pages / 6 modules; probe ON == disk 36 / 36). Skeleton "
           "53.518 → 53.525 (+0.008pp = the prediction), ≥50 1157 → 1158 (XDLS906_2_0 up), ≥75 191 / ≥90 15 EXACT, RAW 37.756 → 37.762, 1956 pairs / 0 "
           "skipped / 0 movers outside; compare_structure 11700 / 172 / 625, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; "
           "every verifier RESULT identical to r390; 15 selftests + the skeleton selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped "
           "#3 since the r388 full; the miner re-mined 178 CANDIDATE rows (#3735 GONE; one NEW #4286 `body EXTRA div.col-12.col-md-12 › ul`, 21 pages / 3 "
           "modules = XDLS904 / 905 / 906's panel lists — the writer's consecutive bullets split by their trailing inline `[link to X]` markers into separate "
           "`<ul>`s where the gold ships ONE list — the Round 6 candidate); checksums refreshed (engine 3 changed); finalise = changelog entry "
           "`_s26_r391_entry.md`, AppVersion 260619.62, CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md.\n")
a = rd(AR)
if "## Session 26 — Round 5 PICK (engine r391) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 5 PICK (engine r391) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈02:25 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
stub = ("## Session 26 — Round 5 (engine r391) SHIPPED — its PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md ('Session 26 — Round 5 PICK (engine r391) + "
        "what shipped'); the one-line summary is in the Round log below.\n")
s = s[:i] + stub + s[j:]
line = ("- s26-r5 (engine r391) · THE OWN-ROW SUPERVISOR PANEL'S TEXT COLUMN IS `col-12 col-md-12` IN LEAVING TO LEARN (gold 28 / 37 = 0.76 on 35 pages / "
        "15 modules; the r390 miner row #3735 decomposed = a parent-label mismatch; activity-owned panels a tie, untouched); data `inner_row.text_col_by_subject`, "
        "env `PANELCOL_OFF` · SHIPPED 19 Sept · ON 28 pp / 6 mods (21 up / 2 down, +15.2); SCOPED (#3 since r388) · skeleton 53.518→53.525 (+0.008), ≥50 +1; "
        "all else EXACT · build 260619.62\n")
assert len(line) <= 520, len(line)
anchor = "- s26-r4 (engine r390)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r390**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r391** (build 260619.62, 19 Sept ≈02:25, session 26 Round 5 — the own-row supervisor panel's text column in Leaving to Learn; r390 the "
       "supervisor note's explicit closer; r389 the built flipCard group closes its column; r388 the plain / solid alert (the FULL backstop); r387 the "
       "whakataukī; r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a "
       "data row; r382 the reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] "
       "Activity <id>` heading opener) — SCOPED regeneration of 6 LtL modules (the ledger at scoped #3 since the r388 FULL, 5 of headroom). **Corpus = r391** "
       "(2109 pages / 416 modules). Gates at r391 (`gate_baseline.json`): skeleton **53.525 %** / ≥50 **1158** / ≥75 **191** / ≥90 **15** @ 1956 pairs; RAW "
       "37.762 %; compare_structure exact **11700** (EXTRA 172 / MISSING 625 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; "
       "every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.3 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈02:20 on the r391 corpus "
       "(`_diff_miner_s26_r391.log`: 1956 pairs / 8143 classes / **CANDIDATE 178** — #3735 gone, ONE new: #4286 `body EXTRA div.col-12.col-md-12 › ul` (21 "
       "pages / 3 modules = XDLS904 / 905 / 906's panel lists: consecutive bullets split by their trailing inline `[link to X]` markers into separate `<ul>`s "
       "where the gold ships ONE list) — DISPOSITION: the Round 6 PICK (measure the list-merge across every inline-marker-split bullet run first); "
       "`_s26_r391_queue_delta.log`; the pre-r391 queue kept at `_diff_queue_pre_r391.md`); every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r391 +0.008pp but ≥50 +1 moved — §4 needs BOTH conditions, not a plateau round; r390 +0.047pp / cs exact +57; r389 "
       "+0.016pp with ≥50 +2 / ≥75 −1; r388 +0.060pp; r387 +0.043pp).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.61;", "- Standing facts: AppVersion 260619.62;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈02:00 on the r390 corpus, 178 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈02:20 on the r391 corpus, 178 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s), "bytes; archive:", len(a), "bytes")
