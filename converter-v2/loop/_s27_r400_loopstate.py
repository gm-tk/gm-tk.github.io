#!/usr/bin/env python3
"""Session 27 Round 5 SHIPPED (engine r400) — LOOP_STATE.md: the Position block (LAST SHIPPED r400, gates, ledger scoped #4, miner re-mined 169),
the plateau window RESET, Standing facts AppVersion 260619.71, the Round-5 PICK section moved to the archive as the what-shipped record,
the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r5 (engine r400)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r399**"); j = s.index("\n", i) + 1
old = s[i:j]
new = ("- LAST SHIPPED: **r400** (build 260619.71, 19 Sept ≈12:58, session 27 Round 5 — the un-numbered activity opener takes the next positional letter; "
       "r399 the wānanga / talanoa box is the KB's cultural alert; r398 the videoSection `icon` registry re-mined + the widget-embedded video; r397 a table header cell is plain; "
       "r396 the captioned carousel video slide is `item video` (the FULL backstop); r395 the flip-card column width; r394 the clickDrop buttons in the column; r393 the glyph-only "
       "line; r392 adjacent lists; r391 the LtL panel column; r390 the supervisor closer; r389 the flipCard group closes its column; r388 the plain / solid alert (the previous FULL); "
       "r387 the whakataukī; r386 / r382 instrument corrections; r385–r377 session 24) — SCOPED regeneration of 94 modules (the ledger at scoped #4 since the r396 FULL, 4 of "
       "headroom). **Corpus = r400** (2109 pages / 416 modules). Gates at r400 (`gate_baseline.json`): skeleton **53.979 %** / ≥50 **1174** / ≥75 **200** / ≥90 **18** @ 1956 pairs; "
       "RAW 37.995 %; compare_structure exact **11798** (EXTRA 172 / MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier "
       "at its recorded baseline. Ceiling 91.9 % → 58.7 % of achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈12:58 on the r400 corpus (`_diff_miner_s27_r400.log`: 1956 pairs / "
       "**CANDIDATE 169**; `_s27_r400_queue_delta.log`; the pre-r400 queue kept at `_diff_queue_pre_r400.md`): four rows GONE (the numberless `div.activity` rows — "
       "`activity EXTRA div.activity › div.row` 607 lines / 45 pages and its three shadows), nothing new; every other disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **0 of 3** — r400 +0.118pp RESET it (s27-r3 / s27-r4 had counted 1 and 2).\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.70 (session 27 in progress);", "- Standing facts: AppVersion 260619.71 (session 27 in progress);", 1)
# 4. the Round-5 PICK section -> archive as the what-shipped record; a one-line pointer stays
h = "## Session 27 — Round 5 PICK (engine r400, in progress; 19 Sept ≈12:45 NZST): the un-numbered activity opener takes the next positional letter"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 5 PICK (engine r400) + what shipped — the un-numbered activity opener takes the next positional letter (19 Sept ≈12:45 → 12:58 NZST)", 1)
shipped += ("- **What shipped (r400, build 260619.71):** the probe OFF 2109 / 2109; ON 281 pages / 94 modules; scored on the ON pages 67 up / 13 down / 186 same (+229.9); the 94 regenerated "
            "(10 batches, all rc 0; `fresh --affected` 0 truly stale; probe ON == disk 795 / 795); skeleton 53.862 → 53.979 % (+0.118pp; 80 movers 67 up / 13 down, 0 outside the "
            "affected set — the 13 dips named in the changelog, the r369 letter-shift class: ENGI201_2_0 −11.3 the largest), ≥50 1170 → 1174, ≥75 197 → 200, ≥90 18, RAW 37.918 → "
            "37.995 %; compare_structure 11798 / 172 / 626, body_compare 42 / 4 / 173 / 218, clean 2079 / 2102, leak 26 / 23 — EXACT; every verifier RESULT identical to r399; 15 "
            "selftests + the feature-index selftest GREEN; ledger scoped #4 since the r396 FULL; miner 173 → 169 CANDIDATE (four numberless-box rows gone, nothing new); "
            "checksums engine 4 changed / gates 0.\n")
a = rd(AR)
if "Round 5 PICK (engine r400) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r400 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r5 (engine r400) · THE UN-NUMBERED ACTIVITY OPENER TAKES THE NEXT POSITIONAL LETTER (a writer's bare `[Activity]` / `[Activity: Embedded]` / `[interactive] …` opener on a "
        "numbered-lesson page ships `number=\"{lesson}{letter}\"` — the gold numbers every box, 6 numberless in 2385 pages vs Claude's 629; `activity_wrapper.lesson_letter_number.unnumbered_positional`, "
        "env `ACTUNNUM_OFF`; found by the label census's EXTRA `div.activity` 529 lines, `_s27_r5_numberless.py` / `_s27_r5_posnum.py` 0.68 on the count-equal pages) · SCOPED regen 94 modules "
        "(the probe proving the other 322 byte-identical; scoped ship #4 since the r396 FULL) · skeleton 53.862 → 53.979 (+0.118pp; 80 movers 67 up / 13 down, named), ≥50 1170 → 1174, "
        "≥75 197 → 200, ≥90 18; every other gate EXACT · 12:58 · plateau RESET\n")
anchor = "- s27-r4 (no engine change)"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
