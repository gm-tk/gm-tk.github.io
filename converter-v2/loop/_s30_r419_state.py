#!/usr/bin/env python3
"""r419 finalise — LOOP_STATE.md: the Round 1 PICK section moves to the archive (+ the what-shipped record), the Position updates,
the Round-log line is appended. Run under WSL."""
import os, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
STATE, ARCH = R + "LOOP_STATE.md", R + "LOOP_STATE_ARCHIVE.md"
lines = io.open(STATE, encoding="utf-8").read().split("\n")
def idx(prefix, start=0):
    for i in range(start, len(lines)):
        if lines[i].startswith(prefix): return i
    raise SystemExit("not found: " + prefix)
a = idx("## Session 30 — Round 1 PICK (engine r419)"); b = idx("## Round log")
pick = lines[a:b]
shipped = ("- **What shipped (r419, build 260619.90, 21 Sept ≈16:50):** `Emit_Templates.body_region.language_fonts {enabled, env LANGFONT_OFF, wrapper, classes, "
           "module_language, kana_is_japanese, han_needs_module_language, cjk_chars, han_chars, kana_chars, internal_joiners, lead_open_chars, skip_zones}` + "
           "`ListsAndRuns.LanguageFontWrap(html, run)` at the PageAssembler whole-page seam (after `LinkTextDisplay`, before `MathReplace`, the pre-acks slice): every "
           "CJK run → `<span class=\"ch-text\">` / `<span class=\"jp-text\">` (a run = CJK blocks joined by internal whitespace / brackets / slashes / stops, starting on a "
           "character or an opening bracket — the leading `：` stays outside — ending on a CJK character, ≥ 1 Han / kana; kana → jp anywhere, Han → the module's language "
           "by code prefix, bare where the module has none; verbatim script / style / title / cv2-note / cv2-comment; idempotent). Unit 22 / 22. Probe OFF (`LANGFONT_OFF`) "
           "= disk 2555 / 2555; ON 25 pages / 13 modules (CHWHA's `MODULE_0_0.html` = the code-detection gap, recorded); scored 13 up / 7 down / 4 same, +49.7pp-sum "
           "(CHFUN08 +30.1; the JPN1004 dips inspected — the form is the gold's, the pages are structurally far from it). SCOPED regeneration of the 13 + 12 spot-checks "
           "(0 truly stale, 12 / 12 byte-identical; disk == probe 52 / 52); `scoped_ship.sh --commit` containment 13 ⊆ 13, PASS, the ledger scoped #3 since the r416 FULL "
           "(5 of headroom). `run_all_gates.sh`: skeleton 54.1860 → 54.2072 % (+0.0212pp; 20 movers 13 up / 7 down, 0 outside the set), ≥50 1439 → 1441, ≥75 238 / ≥90 20 "
           "EXACT, RAW 38.204 → 38.227; cs exact 14168 → 14170 (the pool +2) / 186 / 683 / 23, body 54 / 5 / 190 / 247, clean 2504 / 2548, leak 73 / 44, tags 9557 — all "
           "EXACT; every verifier ✓ (dragAndDrop's CHFUN05 21 widgets / 148 drags / defect 0); 16 selftests GREEN (46 / 0); feature index GREEN; miner 183 → 182; KB status "
           "row 92 → CAPTURED-LIVE (ch / jp; pinyin pending); checksums refreshed. Plateau: +0.0212pp, ≥50 +2 — 0 of 3. Recorded follow-ups: pinyin (Round 2), the "
           "cross-tag run (4 %), CHWHA's code detection.")
lines[a:b] = ["## Session 30 — Round 1 (engine r419) — THE LANGUAGE-FONT WRAP: every CJK run takes `span.ch-text` / `span.jp-text` (KB constraint 92 / CL-0093, the CJK half) — SHIPPED; the PICK + what-shipped record is in LOOP_STATE_ARCHIVE.md 'Session 30 — Round 1 PICK (engine r419) + what shipped'; the one-line summary is the s30-r1 Round-log line below.", ""]
p = idx("- LAST SHIPPED: **r418**")
old = lines[p]
assert old.startswith("- LAST SHIPPED: **r418** (build 260619.89, 20 Sept ≈22:05, session 29 Round 9 — ")
rest = old[len("- LAST SHIPPED: **r418** (build 260619.89, 20 Sept ≈22:05, session 29 Round 9 — "):]
# the r418 text becomes the "before it" clause, trimmed to its headline
r418_short = ("**r418** (build 260619.89, 20 Sept ≈22:05, session 29 Round 9 — the first tile panel takes the `row.clickDropContent.noBorder` form + the r417 title-pin "
              "repair, `CDFIRSTROW_OFF`, 30 up / 0 down, +0.0630pp, ≥50 +1)")
tail_ix = rest.find("; before it **r417**")
assert tail_ix > 0
tail = rest[tail_ix + len("; before it "):]
lines[p] = ("- LAST SHIPPED: **r419** (build 260619.90, 21 Sept ≈16:50, session 30 Round 1 — THE LANGUAGE-FONT WRAP: every run of Chinese / Japanese text takes "
            "`span.ch-text` / `span.jp-text` (KB constraint 92 / CL-0093 — the gold wraps 5,437 of 5,512 runs, Claude shipped 3,812 bare on 26 pages / 14 modules; "
            "`body_region.language_fonts`, env `LANGFONT_OFF`; `ListsAndRuns.LanguageFontWrap` at the PageAssembler whole-page seam, pre-acks); probe OFF = disk "
            "2555 / 2555, ON 25 pages / 13 modules (13 up / 7 down, +49.7pp-sum); SCOPED regeneration of the 13 (scoped ship #3 since the r416 FULL); **skeleton "
            "54.186 → 54.207 % (+0.0212pp), ≥50 1439 → 1441, ≥75 238, ≥90 20, RAW 38.227 % @ 2349 pairs**; cs 14170 (+2) / 186 / 683 / 23, body 54 / 5 / 190 / 247, "
            "clean 2504 / 2548, leak 73 / 44 — all EXACT; every verifier EXACT; 16 selftests GREEN; the miner 183 → 182; pinyin is Round 2); before it " + r418_short + ", " + tail)
lines[p] = lines[p].replace("**Corpus = r418** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r418; `outputs/_s29_r418_sk_final.json` the skeleton state; ceiling 90.9 % → 54.186 = **59.6 % of achievable**)",
                            "**Corpus = r419** (2555 pages / 494 dirs / 2349 pairs; `gate_baseline.json` at r419; `outputs/_s30_r419_sk_final.json` the skeleton state; ceiling 90.9 % → 54.207 = **59.6 % of achievable**)")
assert "Corpus = r419" in lines[p]
q = idx("- Plateau window (§4): **0 of 3**")
lines[q] = "- Plateau window (§4): **0 of 3** — r419 +0.0212pp (≥50 +2), r418 +0.0630pp (≥50 +1), r417 +0.1947pp (≥50 +23). Read every delta on the post-intake 2,349-pair population (§1e)."
r = idx("- Standing facts: AppVersion 260619.89")
lines[r] = lines[r].replace("AppVersion 260619.89 (r418, session 29 Round 9, 20 Sept); before it 260619.88 (r417)", "AppVersion 260619.90 (r419, session 30 Round 1, 21 Sept); before it 260619.89 (r418) / 260619.88 (r417)")
assert "260619.90" in lines[r]
t = idx("- s29-r10 (no engine change")
lines.insert(t + 1, "- s30-r1 (engine r419, build 260619.90, 21 Sept ≈15:40 → 16:50) · THE LANGUAGE-FONT WRAP — every run of Chinese / Japanese text takes `span.ch-text` / `span.jp-text` (KB constraint 92 / CL-0093, locked admin: MANDATORY on every occurrence, the conversion applies them; the CJK half — pinyin next; found by the s29-r10 label census + KB status row 92 whose '< 20 pages' was pre-intake; `_s30_r1_langfont.py`: the gold 5,437 / 5,512 runs = 0.99, Claude 3,812 bare on 26 pages / 14 modules; `_s30_r1_langspans.py`: carrier span 98 %, every context, the `<b>` outside, runs start on a character 4,331 : 64; `ListsAndRuns.LanguageFontWrap` at the PageAssembler whole-page seam, pre-acks; `body_region.language_fonts`, env `LANGFONT_OFF`; kana → jp anywhere, Han → the module's language by code prefix, bare where none) · SHIPPED · unit 22 / 22; probe OFF = disk 2555 / 2555, ON 25 pages / 13 modules (13 up / 7 down, +49.7pp-sum; the JPN1004 dips = alignment artefacts, form = the gold's) · SCOPED regen of the 13 + 12 spot-checks (0 stale; 12 / 12; containment 13 ⊆ 13; scoped #3 since the r416 FULL) · skeleton 54.186 → 54.207 (+0.0212pp), ≥50 1439 → 1441, ≥75 238 / ≥90 20 EXACT; cs exact +2 (the pool +2); all else EXACT; every verifier ✓; 16 selftests GREEN; miner 183 → 182 · plateau 0 of 3 · build 260619.90")
io.open(STATE, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
with io.open(ARCH, "a", encoding="utf-8", newline="\n") as f:
    f.write("\n## Session 30 — Round 1 PICK (engine r419) + what shipped — THE LANGUAGE-FONT WRAP: every CJK run takes span.ch-text / span.jp-text (KB constraint 92 / CL-0093) (21 Sept ≈15:40 → 16:50 NZST)\n\n" + "\n".join(pick).rstrip("\n") + "\n" + shipped + "\n")
print("LOOP_STATE.md", os.path.getsize(STATE), "bytes; archive", os.path.getsize(ARCH))
