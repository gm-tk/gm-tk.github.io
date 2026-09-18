#!/usr/bin/env python3
"""Session 26 Round 7 (r393) — LOOP_STATE.md: archive the Round 7 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r7 (engine r393)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 7 PICK (engine r393)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r393, build 260619.64, 19 Sept ≈03:35 NZST):** data `body_region.drop_glyph_only_lines {enabled, env GLYPHLINE_OFF, keep: [•]}` + "
           "`ListsAndRuns.renderBlackText`'s line filter (free-body text only; a line that with its `*` markers removed is one non-letter / non-digit / non-`_` "
           "character is dropped) (`_s26_r393_splice.py`). Probe OFF 2109 / 2109; ON 68 pages / 60 modules (every change = one `<p>glyph</p>` removed); scored "
           "before the regen: 41 up / 6 down / 19 same, pp-sum +12.7. SCOPED regeneration of the 60 (6 batches rc 0; `fresh --affected` 0 truly stale; manifest "
           "diff = 68 pages / 60 modules; probe ON == disk 339 / 339). Skeleton 53.554 → 53.560 (+0.0065pp), ≥50 1160 → 1159 (CEDK501_5_1 52.0 → 42.9 — its "
           "`<p>[</p>` sat in a '2× repeated p' slot the gold also has, so the stray bracket was standing in for a gold paragraph Claude lacks; the gate's "
           "repeat-collapse alignment, not a structural loss; ENGI301_4_0 −4.1 the same), ≥75 191 / ≥90 15 EXACT, RAW 37.785 → 37.787, 1956 pairs / 0 skipped / "
           "47 movers 35 up / 6 down / 0 outside; compare_structure 11723 / 172 / 626, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all "
           "EXACT; every verifier RESULT identical to r392; 15 selftests + the index selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped "
           "#5 since the r388 full; the miner re-mined 178 CANDIDATE rows (nothing gone; one NEW #3699 `body EXTRA div.col-12.col-md-8 › div.row`, 20 pages / 18 "
           "modules at the floor — a Claude row opened INSIDE the text column where the gold has none, Online Safety 7 pages, 'Watch this video…' leads = the "
           "Round 8 candidate); checksums refreshed; finalise = changelog entry `_s26_r393_entry.md`, AppVersion 260619.64, CLAUDE.md §9 / §11 / §14, "
           "gate_baseline.json, loop/README.md. Plateau window 1 of 3 (+0.0065pp with ≥50 −1 — a bucket moving down does not rescue the round). DECLINED on "
           "measurement the same round: adjacent `<ol>` merge (MERGED 0.11) and the gold's unclosed rows (815 `row › row` nestings predicted by nothing).\n")
a = rd(AR)
if "## Session 26 — Round 7 PICK (engine r393) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 7 PICK (engine r393) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈03:35 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r392)"):]; old = old[:old.index("\n") + 1]
new = old.replace("r387–r392", "r387–r393", 1)
s = s.replace(old, new, 1)
line = ("- s26-r7 (engine r393) · A GLYPH-ONLY LINE RENDERS NOTHING (a free-body line that is one punctuation glyph never ships as `<p>`; Claude 170 on 69 "
        "pages / 64 modules, the gold 0 = dropped 1.00); data `body_region.drop_glyph_only_lines`, env `GLYPHLINE_OFF` · SHIPPED 19 Sept · ON 68 pp / 60 mods "
        "(41 up / 6 down, +12.7); SCOPED (#5 since r388) · skeleton 53.554→53.560 (+0.0065), ≥50 −1 (CEDK501_5_1, an alignment artefact); all else EXACT · "
        "plateau 1 of 3 · adjacent `<ol>` + the gold's unclosed rows measured, declined · build 260619.64\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r6 (engine r392)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r392**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r393** (build 260619.64, 19 Sept ≈03:35, session 26 Round 7 — a glyph-only line renders nothing; r392 adjacent sibling lists are one "
       "list; r391 the own-row supervisor panel's text column in Leaving to Learn; r390 the supervisor note's explicit closer; r389 the built flipCard group "
       "closes its column; r388 the plain / solid alert (the FULL backstop); r387 the whakataukī; r386 the skeleton label's class-token order; r385 the panel's "
       "first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 the reader's shared `body_source`; r381 the reverse trio; "
       "r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` heading opener) — SCOPED regeneration of 60 modules (the "
       "ledger at scoped #5 since the r388 FULL, 3 of headroom). **Corpus = r393** (2109 pages / 416 modules). Gates at r393 (`gate_baseline.json`): skeleton "
       "**53.560 %** / ≥50 **1159** / ≥75 **191** / ≥90 **15** @ 1956 pairs; RAW 37.787 %; compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap "
       "23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.3 % of "
       "achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈03:30 on the r393 corpus (`_diff_miner_s26_r393.log`: 1956 pairs / 8138 classes / **CANDIDATE 178** — "
       "nothing gone, ONE new: #3699 `body EXTRA div.col-12.col-md-8 › div.row` (20 pages / 18 modules, AT the floor; a Claude `div.row` opened INSIDE the "
       "text column where the gold has none — Online Safety 7 pages, Leaving to Learn 3, 'Watch this video…' / a video block's lead) — DISPOSITION: the Round 8 "
       "candidate — name the block that opens the inner row (a media / video wrapper?) and measure the gold's form across the 18 before any code; "
       "`_s26_r393_queue_delta.log`; the pre-r393 queue kept at `_diff_queue_pre_r393.md`); every other disposition stands (#660 = the gold's unclosed rows, "
       "declined on measurement in r393).\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **1 of 3** (r393 +0.0065pp with ≥50 −1 — a bucket moving DOWN does not rescue the round, so it counts; r392 +0.028pp with ≥50 +2 / "
       "cs exact +23; r391 +0.008pp but ≥50 +1 moved; r390 +0.047pp / cs exact +57; r389 +0.016pp with ≥50 +2 / ≥75 −1).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.63;", "- Standing facts: AppVersion 260619.64;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈02:50 on the r392 corpus, 177 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈03:30 on the r393 corpus, 178 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
