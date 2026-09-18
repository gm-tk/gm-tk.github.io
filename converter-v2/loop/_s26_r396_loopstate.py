#!/usr/bin/env python3
"""Session 26 Round 10 (r396) — LOOP_STATE.md: archive the Round 10 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r10 (engine r396)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 10 PICK (engine r396)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r396, build 260619.67, 19 Sept ≈05:25 NZST):** data `interactive.carousel.item_video_with_caption {enabled, env ITEMVIDEO_OFF, from, to}` "
           "+ the swap in `InteractiveBuilder.#carRenderSlides` when the slide holds a videoSection AND its caption block opened (`_s26_r396_splice.py`). Probe OFF "
           "2109 / 2109; ON 52 pages / 44 modules; scored before the regen: 0 up / 0 down / 49 same — the class is a widget-internal token the scaffold does not "
           "line. THE FULL REGENERATION (the ledger's backstop at scoped #7 since r388): the r388 batch list, 36 batches / 4 parallel, all rc 0 in 5 minutes; "
           "`_stalecheck.sh` 0 stale; `fresh --affected` over all 416: 413 fresh + the 3 source-less TRR modules (TRR104 / 105 / 115, no Writers Template, no "
           "pages — the ceiling's standing exception); the manifest diff = 52 pages / 44 modules = the probe's ON set EXACTLY (no residue from the seven scoped "
           "ships r389–r395); probe ON == disk 254 / 254; `record-full --round 396` (scoped-since reset to 0). Skeleton 53.684 / ≥50 1163 / ≥75 195 / ≥90 18 / "
           "median 54.3 EXACT (0 movers), RAW 37.784 → 37.780; compare_structure 11723 / 172 / 626, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak "
           "26 / 23 — all EXACT; every verifier RESULT identical to r395; 15 selftests + the index selftest GREEN; fast-loop / manifest / feature index "
           "refreshed; the miner re-mined 173 CANDIDATE rows (nothing gone, nothing new); checksums refreshed; finalise = changelog entry `_s26_r396_entry.md`, "
           "AppVersion 260619.67, CLAUDE.md §9 / §11 / §14, gate_baseline.json, loop/README.md. Plateau window 1 of 3 (+0.000pp, no gate moved — gold-matching "
           "but gate-invisible). Recorded: the video-ONLY slide's class (gold 0.55 corpus-wide; Maths 0.75 / Inquiry-BLL 0.67 / LtL 0.65 / ConnectED 0.60 vs "
           "Standard-BLL 0.32 / EXPlore 0.00) a per-group, gate-invisible candidate.\n")
a = rd(AR)
if "## Session 26 — Round 10 PICK (engine r396) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 10 PICK (engine r396) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈05:25 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r395)"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, old.replace("r387–r395", "r387–r396", 1), 1)
line = ("- s26-r10 (engine r396) · A CAROUSEL VIDEO SLIDE WITH A CAPTION IS `item video` (the gold 273 / 298 = 0.92; the video-only slide a tie, untouched); data "
        "`interactive.carousel.item_video_with_caption`, env `ITEMVIDEO_OFF` · SHIPPED 19 Sept · ON 52 pp / 44 mods, gate-invisible (0 movers) · THE FULL "
        "BACKSTOP: all 416 regenerated, 0 stale, manifest diff = the probe's 52 pages (no residue from r389–r395), ledger reset · skeleton 53.684 / 1163 / 195 / 18 "
        "EXACT, RAW 37.780; all else EXACT · plateau 1 of 3 · build 260619.67\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r9 (engine r395)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r395**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r396** (build 260619.67, 19 Sept ≈05:25, session 26 Round 10 — the captioned carousel video slide is `item video`, THE FULL-REGENERATION "
       "BACKSTOP; r395 the flip-card column width follows the card count; r394 the clickDrop buttons sit directly in the column; r393 a glyph-only line renders "
       "nothing; r392 adjacent sibling lists are one list; r391 the own-row supervisor panel's text column in Leaving to Learn; r390 the supervisor note's "
       "explicit closer; r389 the built flipCard group closes its column; r388 the plain / solid alert (the previous FULL); r387 the whakataukī; r386 the skeleton "
       "label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 the reader's shared "
       "`body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` heading opener) — FULL "
       "regeneration of all 416 (the ledger at scoped #0 since the r396 FULL, 8 of headroom). **Corpus = r396** (2109 pages / 416 modules). Gates at r396 "
       "(`gate_baseline.json`): skeleton **53.684 %** / ≥50 **1163** / ≥75 **195** / ≥90 **18** @ 1956 pairs; RAW 37.780 %; compare_structure exact **11723** "
       "(EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded "
       "baseline. Ceiling 91.9 % → 58.4 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈05:20 on the r396 corpus (`_diff_miner_s26_r396.log`: 1956 pairs / "
       "8071 classes / **CANDIDATE 173** — nothing gone, nothing new; `_s26_r396_queue_delta.log`; the pre-r396 queue kept at `_diff_queue_pre_r396.md`); every "
       "other disposition stands (#3633 the clickDrop panels' alignment residue — measure the panel COUNT per group first; #3606 the Inquiry `inquiryPanel` under "
       "consensus).\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **1 of 3** (r396 +0.000pp, no gate moved — gold-matching but gate-invisible, counts; r395 +0.010pp but ≥75 +1 moved; r394 +0.114pp "
       "reset the window; r393 +0.0065pp with ≥50 −1 had counted 1).\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.66;", "- Standing facts: AppVersion 260619.67;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈04:50 on the r395 corpus, 173 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈05:20 on the r396 corpus, 173 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
