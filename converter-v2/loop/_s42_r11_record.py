#!/usr/bin/env python3
"""Session 42 Round 11 — a measurement-tool round: the ORDER census added to `_placement_census.py`. LOOP_STATE.md: the follow-up line,
the round-log line; LOOP §1g item 2 already names the tool. BUILD_CHANGELOG entry (no engine change). .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
CV = os.path.join(ROOT, "pageforge-site", "converter-v2")
S = os.path.join(ROOT, "LOOP_STATE.md")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    tmp = p + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(s)
    assert os.path.getsize(tmp) > 1000; os.replace(tmp, p)
PC = os.path.join(CV, "BUILD_CHANGELOG.md"); sc = rd(PC); head = "# BUILD CHANGELOG — Stage 2 (engine + UI)\n\n"
assert sc.startswith(head) and "session 42 Round 11" not in sc[:4000]
entry = """## 2026-09-24 (session 42 Round 11 — no engine change; build 260620.35 unchanged) — THE PLACEMENT CENSUS GAINS AN ORDER CENSUS: which blocks the human places in a different ORDER than Claude on the same page (LOOP §1g, D14-S1 — Chris's original BLL110 finding was an order move: the introduction placed after the supervisor note)

**The tool** (`outputs/_placement_census.py`, section 5): every gold block matched on the paired page, in gold order, carries its Claude position; the blocks outside the longest increasing subsequence of those positions are the out-of-order ones (`lis_keep`). Reported by gold region (matched / out of order / share / pages / modules), by recurring block (tag + first five words, by modules — a text that moves in many modules is a systematic rule; with the gold block it should precede) and by region · tag. Caveat recorded in the report: repeated identical texts pair in order, so an extra developer-inserted copy in the gold shifts every later pair (the top row, `h4 "Go to your journal"` 42 modules / 85 pages, is this artefact — ANZH301 1A carries an extra journal heading + "Download journal" button the writer never typed).

**The first order census (r470 corpus, 163,771 gold blocks):** out of order 0.036 of `body:free`, 0.046 of `body:activity`, 0.096 of `menu:Overview` (46 modules — the BLL2xx Knowledge / Practices / LI list order, Needs Chris #22's territory), 0.182 of dragAndDrop internals (the un-built widgets' raw order), 0.236 of `body:alert:side`. No systematic order class reaches the floor: the recurring moves are the journal artefact, BLL menu list items (5–15 modules), the TRR / PMT reo-before-English order of a few activity / menu headings (`Rapua ngā kupu…` before `Find the rhyming words`, `Hei te mutunga o te tau:` before `By the end of the year:` — 3–7 modules) and single-module BLL110 / BLL120 activity paragraphs.

No converter output changed; plateau: neither counts nor resets. Tools `outputs/_placement_census.{py,md,json,log}`, `_s42_r11_record.py`.

"""
wr(PC, head + entry + sc[len(head):]); print("changelog ok")
ss = rd(S); L = ss.split("\n")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
shutil.copyfile(S, S + ".pre-s42-r11.bak")
k = find("- **(s42-r3) THE PLACEMENT CENSUS")
L.insert(k + 1, "- **(s42-r11) THE ORDER CENSUS (`_placement_census.md` section 5).** No systematic order move reaches the floor on r470: the "
         "`h4 \"Go to your journal\"` row (42 modules) is the repeated-text pairing artefact (the gold's extra developer-inserted journal "
         "heading + \"Download journal\" button, ANZH301 1A); the TRR / PMT reo-before-English order of a few activity / menu headings "
         "(3–7 modules — KB c79 / 07D rule 7: MTK stays Māori first) is a follow-up to size with the pair ORDER inside the bilingual "
         "activity title (`BilingualBuilder` reads the `[Activity: Embedded]` table's English column first?); BLL2xx menu list order "
         "(5–15 modules) belongs with Needs Chris #22.")
k = find("## Round log")
L.insert(k + 1, "- s42-r11 (no engine change, 24 Sept 17:25 → ≈17:45) · the placement census gains an ORDER census (LIS of Claude positions in "
         "gold order); first run: no systematic order class at the floor (the journal row is a repeated-text artefact; TRR reo-first "
         "headings 3–7 modules recorded) · a measurement-tool round · plateau 2 of 3 (neither).")
wr(S, "\n".join(L)); print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
