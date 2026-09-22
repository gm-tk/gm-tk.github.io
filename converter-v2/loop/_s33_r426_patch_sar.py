#!/usr/bin/env python3
"""ROUND 426 (session 33 Round 4) — THE SINGLE-PAGE INQUIRY PAGE MODEL for the eight over-split modules the 22 Sept intake found:
exact text edits on data/Style_Anchor_Registry.json (tab-indented, LF; formatting preserved), the pre-round copy snapshotted to
outputs/_s33_r426_pre/ (the OFF state). Run under WSL. Reversal = the committed pre-round registry (the r336 precedent)."""
import os, shutil, json, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
P = R + "pageforge-site/converter-v2/data/Style_Anchor_Registry.json"
PRE = R + "CONVERTER_V2/outputs/_s33_r426_pre/"
os.makedirs(PRE, exist_ok=True)
if not os.path.exists(PRE + "Style_Anchor_Registry.json"): shutil.copyfile(P, PRE + "Style_Anchor_Registry.json")
s = io.open(P, encoding="utf-8", newline="").read()
assert "\r" not in s
T = "\t"
def rep(old, new, n=1):
    global s
    assert s.count(old) == n, (s.count(old), old[:80])
    s = s.replace(old, new)

# 1. BLL2: the x0 parents BLL250 / 260 / 270 are single-file like BLL210 / 220 / 230 (and BLL110–170 in BLL1): 10 / 10 of the family's
#    x0 golds are ONE page.
rep(T*8 + '"BLL210",\n' + T*8 + '"BLL220",\n' + T*8 + '"BLL230"\n' + T*7 + ']',
    T*8 + '"BLL210",\n' + T*8 + '"BLL220",\n' + T*8 + '"BLL230",\n' + T*8 + '"BLL250",\n' + T*8 + '"BLL260",\n' + T*8 + '"BLL270"\n' + T*7 + '],\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22, the loop\'s session 33 Round 4): BLL250 / BLL260 / BLL270 added — the x0 parent modules of the BLL2 level, one gold page each (BLL250.html / BLL260.html / BLL270.html), exactly as BLL210 / 220 / 230 and the seven BLL1 parents (10 / 10 of the family\'s x0 golds are single-file). Never members, so the r408 miner never listed them; found by the 22 Sept intake (Claude had split them into 8 / 13 / 5 lesson pages)."')

# 2. CEDO4 (CEDO402 the only member; its gold is one page) — single-file, like CEDO2 and the phase 1-3 CEDO102 exception.
rep(T*5 + '"CEDO4": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDO402"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "9-10"\n' + T*6 + '}',
    T*5 + '"CEDO4": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDO402"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "9-10",\n' + T*7 + '"page_model": "single-file",\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22): CEDO402\'s gold is ONE page (CEDO402.html, an inquiry page); the level had no page_model so the global default (multi-file) split it into 6 pages at the 22 Sept intake."\n' + T*6 + '}')

# 3. CEDK4 — CEDK401's gold is one page (CEDK402 / 403 are registry members with no gold in the corpus); CEDK1 is single-file too.
rep(T*5 + '"CEDK4": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDK402",\n' + T*7 + '"CEDK403"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "9-10",\n',
    T*5 + '"CEDK4": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDK401",\n' + T*7 + '"CEDK402",\n' + T*7 + '"CEDK403"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "9-10",\n' + T*7 + '"page_model": "single-file",\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22): CEDK401 added as a member (its gold is ONE page, CEDK401 Food Sustainability.html — the CEDK1 form); the level had no page_model so the default split it into 12 pages at the 22 Sept intake. CEDK402 / 403 have no gold in the corpus.",\n')

# 4. TWHT9 — TWHT903's gold is one page (TWHT901 is a member with no gold); TWHK9 is single-file.
rep(T*5 + '"TWHT9": {\n' + T*6 + '"members": [\n' + T*7 + '"TWHT901"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "combo"\n' + T*6 + '}',
    T*5 + '"TWHT9": {\n' + T*6 + '"members": [\n' + T*7 + '"TWHT901",\n' + T*7 + '"TWHT903"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "combo",\n' + T*7 + '"page_model": "single-file",\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22): TWHT903 added (its gold is ONE page; the sibling base TWHK9 is single-file); the level had no page_model so the default split it into 5 pages at the 22 Sept intake."\n' + T*6 + '}')

# 5. CEDR — no CEDR1 / CEDR4 level existed, so CEDR101 and CEDR401 fell to the HIGHEST level (CEDR5, multi-file) and split into 2 pages each;
#    their golds are one page, like every other phase 1-8 CED gold. New levels with the one field that matters.
rep(T*4 + '"levels": {\n' + T*5 + '"CEDR2": {\n',
    T*4 + '"levels": {\n'
    + T*5 + '"CEDR1": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDR101"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "1-3",\n' + T*7 + '"page_model": "single-file",\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22): a new level — CEDR101\'s gold is ONE page; with no CEDR1 level the resolver fell to the highest level (CEDR5, multi-file) and split it into 2 pages at the 22 Sept intake."\n' + T*6 + '}\n' + T*5 + '},\n'
    + T*5 + '"CEDR2": {\n')
rep(T*5 + '"CEDR5": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDR501"\n',
    T*5 + '"CEDR4": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDR401"\n' + T*6 + '],\n' + T*6 + '"delta": {\n' + T*7 + '"template_phase": "9-10",\n' + T*7 + '"page_model": "single-file",\n'
    + T*7 + '"_r426_note": "ROUND 426 (2026-09-22): a new level — CEDR401\'s gold is ONE page; with no CEDR4 level the resolver fell to CEDR5 (multi-file) and split it into 2 pages at the 22 Sept intake."\n' + T*6 + '}\n' + T*5 + '},\n'
    + T*5 + '"CEDR5": {\n' + T*6 + '"members": [\n' + T*7 + '"CEDR501"\n')
json.loads(s)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("PATCHED", len(s))
