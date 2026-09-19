#!/usr/bin/env python3
"""Session 27 Round 10 SHIPPED (engine r405, the FULL backstop) — LOOP_STATE.md: the Position block (LAST SHIPPED r405, gates, ledger FULL / counter 0,
miner 169), the plateau window 2 of 3, Standing facts AppVersion 260619.76, the Round-10 PICK section moved to the archive as the what-shipped record,
the Round-log line. LF preserved; idempotent."""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LS = os.path.join(ROOT, "LOOP_STATE.md"); AR = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md"); HERE = os.path.dirname(os.path.abspath(__file__))
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
s = rd(LS)
if "s27-r10 (engine r405)" in s:
    print("already applied"); sys.exit(0)
# 1. Position: LAST SHIPPED
i = s.index("- LAST SHIPPED: **r403**"); j = s.index("\n", i) + 1
new = ("- LAST SHIPPED: **r405** (build 260619.76, 19 Sept ≈15:45, session 27 Round 10 — the journal section is an activity box; r404 DECLINED-INERT (the alert-top side column's "
       "class by subject); r403 an `[embed]` of an external web page is the KB's externalButton; r402 the `[interactive: video]` line is the box's first lead element; r401 no synthetic "
       "activity box around a widget that captured nothing; r400 the un-numbered activity opener takes the next positional letter; r399 the wānanga / talanoa box; r398 the videoSection "
       "`icon` registry; r397 a table header cell is plain; r396 the captioned carousel video slide (the previous FULL); r395–r387 session 26; r386 / r382 instrument corrections; "
       "r385–r377 session 24) — **a FULL regeneration of all 416 (the ledger's backstop after the seven scoped ships r397–r403; 36 batches rc 0, 0 stale, the manifest diff = the "
       "round's 11 pages exactly — NO residue; the scoped-since counter reset to 0)**. **Corpus = r405** (2109 pages / 416 modules). Gates at r405 (`gate_baseline.json`): skeleton "
       "**54.001 %** / ≥50 **1175** / ≥75 **200** / ≥90 **18** @ 1956 pairs; RAW 38.008 %; compare_structure exact **11796** (the text-matched pool 13816 → 13814; EXTRA 172 / "
       "MISSING 626 / row-wrap 23); body_compare 218 / 42 / 4 / 173; clean 2079 / 2102, leak 26 / 23; every widget verifier at its recorded baseline. Ceiling 91.9 % → 58.8 % of "
       "achievable. `DIFF_QUEUE.md` re-mined 19 Sept ≈15:40 on the r405 corpus (`_diff_miner_s27_r405.log`: 1956 pairs / **CANDIDATE 169**; `_s27_r405_queue_delta.log`; the "
       "pre-r405 queue kept at `_diff_queue_pre_r405.md`): nothing gone, nothing new; every disposition stands.\n")
s = s[:i] + new + s[j:]
# 2. Plateau window
old = s[s.index("- Plateau window (§4):"):]; old = old[:old.index("\n") + 1]
s = s.replace(old, "- Plateau window (§4): **2 of 3** — r404 declined-inert (1), r405 +0.0032pp with no other protected gate moving (2); r403's ≥50 +1 had RESET it. "
                   "A third round under 0.02pp with nothing else moving STOPS the session.\n", 1)
# 3. Standing facts
s = s.replace("- Standing facts: AppVersion 260619.75 (session 27 in progress);", "- Standing facts: AppVersion 260619.76 (session 27 in progress);", 1)
# 4. the Round-10 PICK section -> archive
h = "## Session 27 — Round 10 PICK (engine r405, in progress; 19 Sept ≈15:20 NZST): the journal section is an activity box — a free heading whose section ends in a go-to-journal button is boxed in English / Leaving to Learn"
i = s.index(h); j = s.index("\n## ", i + 1)
sec = s[i:j].rstrip("\n") + "\n"
shipped = sec.replace(h, "## Session 27 — Round 10 PICK (engine r405) + what shipped — the journal section is an activity box; THE FULL-regeneration backstop (19 Sept ≈15:20 → 15:45 NZST)", 1)
shipped += ("- **What shipped (r405, build 260619.76):** the probe OFF 2109 / 2109; ON 11 pages / 5 modules (ENGC301, XGF9001 / 9003 / 9004 / 9006 — the English / LtL sites the "
            "scanner's re-tag reaches; the census's other sites are the bracket-less red `Activity 4A` opener class — ENGI102 — recorded); scored on the ON pages 6 up / 3 down (+6.3); "
            "THE FULL REGENERATION of all 416 (`_s27_r405_fullship_par.sh`, 36 batches / 4 workers, all rc 0, ≈5 min): 0 stale, the manifest diff = the round's 11 pages exactly (no "
            "residue from r397–r403), probe ON == disk 47 / 47; skeleton 53.998 → 54.001 % (+0.0032pp; 9 movers 6 up / 2 down, 0 outside the affected set — XGF9006_2_0 −0.3, "
            "XGF9006_6_0 −0.2), ≥50 1175, ≥75 200, ≥90 18 EXACT, RAW 38.006 → 38.008 %; compare_structure exact 11796 (the pool −2, the r344 class) / 172 / 626; body_compare 42 / 4 / "
            "173 / 218, clean 2079 / 2102, leak 26 / 23 — EXACT; every verifier RESULT identical to r403; 15 selftests + the feature-index selftest GREEN; **ledger FULL (round 405), "
            "scoped counter 0**; miner 169 → 169; checksums engine 2 changed / gates 0. A small ship under the 20-page floor on the r320 precedent — built, proven (gold 0.88 / 0.90), right.\n"
            "- **Recorded:** the bracket-less red `Activity 4A` opener line (36 sites / 14 modules, 8 tracked — ENGI102's gold box 4A with a built D&D; the r148 BARELEAD class for the "
            "activity opener, under the floor); the NCEA1 / Mathematics journal sections (ties) and EXPlore's heading-less form stay free.\n")
a = rd(AR)
if "Round 10 PICK (engine r405) + what shipped" not in a:
    a = a.rstrip("\n") + "\n\n" + shipped
    wr(AR, a); print("archive: r405 record appended", len(a.encode("utf-8")))
s = s[:i] + s[j + 1:]
# 5. the Round-log line
line = ("- s27-r10 (engine r405) · THE JOURNAL SECTION IS AN ACTIVITY BOX (a free h2–h4 heading whose section ends in a go-to-journal `[button]` is re-tagged as a bare `[Activity]` "
        "opener in English / Leaving to Learn — the gold boxes it 0.88 / 0.90, `_s27_r6_journalsec.py`; `opener_rule.id_heading_opener.journal_section`, env `JOURNALBOX_OFF`) · "
        "11 pages / 5 modules · **THE FULL REGENERATION** of all 416 (36 batches rc 0, 0 stale, the manifest diff = the 11 pages — no residue from r397–r403; ledger FULL, counter 0) · "
        "skeleton 53.998 → 54.001 (+0.0032pp; 6 up / 2 down, named), buckets 1175 / 200 / 18 EXACT; compare_structure exact −2 = the pool −2; every other gate EXACT · 15:45 · "
        "plateau 2 of 3\n")
anchor = "- s27-r9 (engine r404"
k = s.index(anchor); k2 = s.index("\n", k) + 1
s = s[:k2] + line + s[k2:]
wr(LS, s); print("LOOP_STATE updated:", len(s.encode("utf-8")), "bytes")
