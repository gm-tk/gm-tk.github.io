#!/usr/bin/env python3
"""Session 26 Round 11 (r397) — LOOP_STATE.md: archive the Round 11 PICK (+ what shipped), the Round-log line, the Position block.
LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s26-r11 (engine r397)" in s:
    print("already applied"); sys.exit(0)
h = "## Session 26 — Round 11 PICK (engine r397)"
i = s.index(h); j = s.index("\n## Round log", i)
pick = s[i:j].rstrip("\n") + "\n"
shipped = ("\n**What shipped (r397, build 260619.68, 19 Sept ≈05:55 NZST):** data `elements.table.header_cell_plain {enabled, env THPLAIN_OFF}` + the wrapper drop at "
           "`TablesAndGrids`' cell emit for free-body header cells whose rendered content is exactly one <b>/<strong> span (`_s26_r397_splice.py`). Probe OFF 2109 / "
           "2109; ON 92 pages / 58 modules; scored before the regen: 73 up / 7 down / 7 same, pp-sum +23.0 (the dips = English pages whose own gold keeps the "
           "bold). SCOPED regeneration of the 58 (7 batches rc 0; `fresh --affected` 0 truly stale; manifest diff = 92 pages / 58 modules; probe ON == disk "
           "430 / 430). Skeleton 53.684 → 53.695 (+0.012pp), ≥50 1163 / ≥75 195 / ≥90 18 / median 54.3 EXACT, RAW 37.780 → 37.782, 1956 pairs / 0 skipped / 80 "
           "movers 70 up / 7 down / 0 outside (SCFUN01_0_0 +7.3, XTAS103_3_1 +4.1; ENGJ403_6_0 −0.9, ENGI405_6_0 −0.8); compare_structure 11723 / 172 / 626, "
           "body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — all EXACT; every verifier RESULT identical to r396; 15 selftests + the index "
           "selftest GREEN; fast-loop / manifest / feature index refreshed; ledger scoped #1 since the r396 full; the miner re-mined 173 CANDIDATE rows "
           "(unchanged); checksums refreshed; finalise = changelog entry `_s26_r397_entry.md`, AppVersion 260619.68, CLAUDE.md §9 / §11 / §14, "
           "gate_baseline.json, loop/README.md. Plateau window 2 of 3 (+0.012pp, no bucket moved; r396 was 1). DECLINED on measurement the same round: the "
           "speech bubble's character image (`_s26_r397_bubbles*.py`): Claude's 454 text-only `bubble-top` bubbles on 129 pages / 62 modules vs the gold's "
           "developer-added character image (OS 0.95, TEDC 0.91, Inquiry-LtL 0.65; iStock / module mascots) in five layouts none ≥ 0.6 — a needs-Chris "
           "question (a placeholder character image per subject?), not a rule; LtL 0.68 text-only, English / Maths ties.\n")
a = rd(AR)
if "## Session 26 — Round 11 PICK (engine r397) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n## Session 26 — Round 11 PICK (engine r397) + what shipped (archived from LOOP_STATE.md 2026-09-19 ≈05:55 NZST, session 26)\n" + pick + shipped
    wr(AR, a)
s = s[:i] + s[j + 1:]
old = s[s.index("## Sessions 23 / 24 / 26 — every shipped round (engine r370–r376, r377–r386, r387–r396)"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, old.replace("r387–r396", "r387–r397", 1), 1)
line = ("- s26-r11 (engine r397) · A TABLE HEADER CELL IS PLAIN (a `<th>` wholly wrapped in one <b>/<strong> drops the wrapper; the gold's th plain 0.96, Claude's "
        "bold 0.18 on 86 pages / 56 modules; KB 05D's form); data `elements.table.header_cell_plain`, env `THPLAIN_OFF` · SHIPPED 19 Sept · ON 92 pp / 58 mods "
        "(73 up / 7 down, +23.0); SCOPED (#1 since r396) · skeleton 53.684→53.695 (+0.012), buckets EXACT; all else EXACT · plateau 2 of 3 · the speech bubble's "
        "character image measured, declined (needs Chris) · build 260619.68\n")
assert len(line) <= 560, len(line)
anchor = "- s26-r10 (engine r396)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
old = s[s.index("- LAST SHIPPED: **r396**"):]; old = old[:old.index("\n") + 1]
new = ("- LAST SHIPPED: **r397** (build 260619.68, 19 Sept ≈05:55, session 26 Round 11 — a table header cell is plain; r396 the captioned carousel video slide is "
       "`item video` (the FULL backstop); r395 the flip-card column width follows the card count; r394 the clickDrop buttons sit directly in the column; r393 a "
       "glyph-only line renders nothing; r392 adjacent sibling lists are one list; r391 the own-row supervisor panel's text column in Leaving to Learn; r390 the "
       "supervisor note's explicit closer; r389 the built flipCard group closes its column; r388 the plain / solid alert (the previous FULL); r387 the whakataukī; "
       "r386 the skeleton label's class-token order; r385 the panel's first own heading is h2; r384 declined inert; r383 the long first row is a data row; r382 "
       "the reader's shared `body_source`; r381 the reverse trio; r380 / r379 the mode-opener boxes; r378 the post-table body; r377 the `[Hn] Activity <id>` "
       "heading opener) — SCOPED regeneration of 58 modules (the ledger at scoped #1 since the r396 FULL, 7 of headroom). **Corpus = r397** (2109 pages / 416 "
       "modules). Gates at r397 (`gate_baseline.json`): skeleton **53.695 %** / ≥50 **1163** / ≥75 **195** / ≥90 **18** @ 1956 pairs; RAW 37.782 %; "
       "compare_structure exact **11723** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget "
       "verifier at its recorded baseline. Ceiling 91.9 % → 58.4 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈05:50 on the r397 corpus "
       "(`_diff_miner_s26_r397.log`: 1956 pairs / 8058 classes / **CANDIDATE 173** — unchanged; `_s26_r397_queue_delta.log`; the pre-r397 queue kept at "
       "`_diff_queue_pre_r397.md`); every other disposition stands (#3633 the clickDrop panels' alignment residue — measure the panel COUNT per group first; "
       "#3606 the Inquiry `inquiryPanel` under consensus).\n")
s = s.replace(old, new, 1)
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
new = ("- Plateau window (§4): **2 of 3** (r397 +0.012pp, no bucket moved — counts; r396 +0.000pp, no gate moved — counts; r395 +0.010pp but ≥75 +1 moved; r394 "
       "+0.114pp reset the window). One more sub-0.02pp round with no protected gate moving = the §4 plateau stop.\n")
s = s.replace(old, new, 1)
s = s.replace("- Standing facts: AppVersion 260619.67;", "- Standing facts: AppVersion 260619.68;", 1)
s = s.replace("`DIFF_QUEUE.md` 19 Sept ≈05:20 on the r396 corpus, 173 candidates, all dispositioned)", "`DIFF_QUEUE.md` 19 Sept ≈05:50 on the r397 corpus, 173 candidates, all dispositioned)", 1)
wr(LS, s)
print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes; archive:", len(a.encode("utf-8")), "bytes")
