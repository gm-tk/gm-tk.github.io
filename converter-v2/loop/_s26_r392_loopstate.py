#!/usr/bin/env python3
"""Session 26 Round 6 (r392) — LOOP_STATE.md: archive the Round 6 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r6 (engine r392)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 6 PICK (engine r392)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r392, build 260619.63, 19 Sept ≈02:55 NZST):** data `body_region.merge_adjacent_lists {enabled, env ULMERGE_OFF, tags: [ul]}` + "
           "`ListsAndRuns.MergeAdjacentLists(html)` (a full-page post-pass at the r337 seam — PageAssembler after TypedNumberList, before the link-text pass; "
           "the same verbatim zones) (`_s26_r392_splice.py`). Probe OFF 2109 / 2109; ON 51 pages / 32 modules; scored before the regen: 40 up / 5 down / 6 same, "
           "pp-sum +48.2 (three of the 5 dips = CED `_0_0` pages outside the gate's pair set). SCOPED regeneration of the 32 (4 batches rc 0; `fresh --affected` "
           "0 truly stale; manifest diff = 51 pages / 32 modules; probe ON == disk 202 / 202). Skeleton 53.525 → 53.554 (+0.028pp), ≥50 1158 → 1160 (AGH1006_5_0, "
           "XDLS905_2_0 up), ≥75 191 / ≥90 15 EXACT, RAW 37.762 → 37.785, 1956 pairs / 0 skipped / 38 movers 35 up / 2 down (SSOG103_0_0 −0.9, ENGI103_1_0 −0.5 — "
           "alignment shifts, the gold keeps its lists apart with paragraphs Claude does not emit) / 0 outside; compare_structure 11723 / 172 / 626 (exact +23, "
           "MISSING +1), body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — EXACT; every verifier RESULT identical to r391; 15 selftests + the "
           "index selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #4 since the r388 full; the miner re-mined 177 CANDIDATE rows "
           "(#4286 GONE = the lead cleared; #3682 under the 20-page floor; one NEW #660 `activity SUBSTITUTED div.row › gold div.col-12 / Claude div.row`, 20 pages / "
           "19 modules at the floor — the miner's examples pair a gold column heading with a Claude row carrying DIFFERENT text = an alignment artefact across 19 "
           "modules, measure before taking); checksums refreshed (engine 4 changed); finalise = changelog entry `_s26_r392_entry.md`, AppVersion 260619.63, "
           "CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md. Recorded: adjacent `<ol>` NOT merged (202 Claude pairs / gold 0 — a restart is a new "
           "numbered list; measure the gold's restart form first).\n")
a = rd(AR)
if "## Session 26 — Round 6 PICK (engine r392) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 6 PICK (engine r392) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈02:55 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
stub = ("## Session 26 — Round 6 (engine r392) SHIPPED — its PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md ('Session 26 — Round 6 PICK (engine r392) + "
        "what shipped'); the one-line summary is in the Round log below.\n")
s = s[:i] + stub + s[j:]
line = ("- s26-r6 (engine r392) · ADJACENT SIBLING LISTS ARE ONE LIST (`</ul>` + whitespace + `<ul>` in the live body joins; Claude 106 pairs on 54 pages / 34 "
        "modules vs the gold's 3 = 0.97; the r391 miner row #4286 decomposed; `ol` NOT taken — a restart is a new list); data `body_region.merge_adjacent_lists`, "
        "env `ULMERGE_OFF` · SHIPPED 19 Sept · ON 51 pp / 32 mods (40 up / 5 down, +48.2); SCOPED (#4 since r388) · skeleton 53.525→53.554 (+0.028), ≥50 +2, "
        "cs exact +23; all else EXACT · build 260619.63\n")
assert len(line) <= 520, len(line)
anchor = "- s26-r5 (engine r391)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r391**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r392** (build 260619.63, 19 Sept ≈02:55, session 26 Round 6 — adjacent sibling lists are one list; r391 the own-row supervisor panel's "
       "text column in Leaving to Learn; r390 the supervisor note's explicit closer; r389 the built flipCard group closes its column; r388 the plain / solid alert "
       "(the FULL backstop); r387 the whakataukī; r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 "
       "the long first row is a data row; r382 the reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table "
       "body; r377 the `[Hn] Activity <id>` heading opener) — SCOPED regeneration of 32 modules (the ledger at scoped #4 since the r388 FULL, 4 of headroom). "
       "**Corpus = r392** (2109 pages / 416 modules). Gates at r392 (`gate_baseline.json`): skeleton **53.554 %** / ≥50 **1160** / ≥75 **191** / ≥90 **15** @ 1956 "
       "pairs; RAW 37.785 %; compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak "
       "26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.3 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈02:50 on the r392 corpus "
       "(`_diff_miner_s26_r392.log`: 1956 pairs / 8142 classes / **CANDIDATE 177** — #4286 GONE (the r392 lead cleared), #3682 `body SUBSTITUTED div.row › "
       "div.col-12.col-md-8 / p` fell under the 20-page floor, ONE new: #660 `activity SUBSTITUTED div.row › gold div.col-12 / Claude div.row` (20 pages / 19 "
       "modules, AT the floor; the miner's example lines pair a gold column heading with a Claude row carrying different text — an alignment artefact spread over "
       "19 modules, not one mechanism) — DISPOSITION: measure the Claude row-in-row vs the gold column across the 19 before any code; `_s26_r392_queue_delta.log`; "
       "the pre-r392 queue kept at `_diff_queue_pre_r392.md`); every other disposition stands.\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **0 of 3** (r392 +0.028pp with ≥50 +2 / cs exact +23; r391 +0.008pp but ≥50 +1 moved — §4 needs BOTH conditions, not a plateau "
       "round; r390 +0.047pp / cs exact +57; r389 +0.016pp with ≥50 +2 / ≥75 −1; r388 +0.060pp).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.62;", "- Standing facts: AppVersion 260619.63;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈02:20 on the r391 corpus, 178 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈02:50 on the r392 corpus, 177 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
