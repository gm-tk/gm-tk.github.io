#!/usr/bin/env python3
"""ROUND 427 (session 33 Round 5) — THE LESSON CHIP BY SUB-SERIES: `_meta.code_prefix_deltas` (the sixth tier's flag) and the BLL1 / BLL2
`prefix_deltas` rows in data/Style_Anchor_Registry.json (exact text edits; the pre-round file snapshotted to outputs/_s33_r427_pre/).
Run under WSL."""
import os, shutil, json, io
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
P = R + "pageforge-site/converter-v2/data/Style_Anchor_Registry.json"
PRE = R + "CONVERTER_V2/outputs/_s33_r427_pre/"
os.makedirs(PRE, exist_ok=True)
if not os.path.exists(PRE + "Style_Anchor_Registry.json"): shutil.copyfile(P, PRE + "Style_Anchor_Registry.json")
s = io.open(P, encoding="utf-8", newline="").read(); assert "\r" not in s
T = "\t"
def rep(old, new):
    global s
    assert s.count(old) == 1, (s.count(old), old[:90]); s = s.replace(old, new)
# 1. the _meta flag, right after template_deltas
rep(T*2 + '"module_code_to_level": {\n',
    T*2 + '"code_prefix_deltas": {\n'
    + T*3 + '"enabled": true,\n'
    + T*3 + '"env": "PREFIXDELTA_OFF",\n'
    + T*3 + '"_doc": "ROUND 427 (the autonomous loop\'s session 33 Round 5, 2026-09-22 — the diff miner\'s chrome facts F3 / F8: the lesson chip\'s FORM). A registry level is keyed by the hundreds digit, but a family\'s convention can turn on the TENS digit: measured over every BLL gold lesson page (outputs/_s33_r5 chip census), BLL11x / 12x / 13x carry the padded chip (01), BLL14x / 15x / 16x the DECIMAL chip (1.0 — 7 / 7, 5 / 6, 7 / 7 modules) under the BLL1 level whose delta says padded-number, BLL21x–25x decimal, and BLL26x / 27x the PADDED chip (6 / 6, 6 / 6) under the BLL2 level whose base says decimal; BLL17x is 5 padded / 2 decimal and stays. `prefix_deltas` is a SIXTH, optional tier at a base or a level — {\\"<code prefix>\\": {field: value}} — the LONGEST matching prefix wins, overlaid after the level and template deltas by ModuleResolver.Resolve; an object-valued field is merged PER KEY so a row names only the key that differs (module_code.lesson) and the overview form and the Inquiry parents\' template-delta `absent` stand. Class: 31 modules / ≈ 62 lesson pages; gate-neutral by design (the chip is TEXT inside the same div#module-code > h1 — the skeleton ignores it; the miner\'s chrome facts F3 / F8 are the verifier). Env PREFIXDELTA_OFF or enabled false restores the level\'s value for every module."\n'
    + T*2 + '},\n'
    + T*2 + '"module_code_to_level": {\n')
# 2. BLL1 level: prefix rows BLL14 / BLL15 / BLL16 → lesson chip decimal (inserted before the level's template_deltas)
rep(T*7 + '"BLL177"\n' + T*6 + '],\n' + T*6 + '"template_deltas": {\n',
    T*7 + '"BLL177"\n' + T*6 + '],\n'
    + T*6 + '"prefix_deltas": {\n'
    + T*7 + '"_note": "ROUND 427 (2026-09-22): the BLL14x / 15x / 16x sub-series carry the DECIMAL lesson chip (BLL141-1.0.html: <h1>1.0</h1>) where the level says padded-number (01) — 19 of 20 golds; BLL11x–13x and BLL17x keep the level\'s padded form.",\n'
    + T*7 + '"BLL14": { "module_code": { "lesson": "decimal" } },\n'
    + T*7 + '"BLL15": { "module_code": { "lesson": "decimal" } },\n'
    + T*7 + '"BLL16": { "module_code": { "lesson": "decimal" } }\n'
    + T*6 + '},\n'
    + T*6 + '"template_deltas": {\n')
# 3. BLL2 level: prefix rows BLL26 / BLL27 → lesson chip padded-number
rep(T*7 + '"BLL254"\n' + T*6 + '],\n' + T*6 + '"template_deltas": {\n',
    T*7 + '"BLL254"\n' + T*6 + '],\n'
    + T*6 + '"prefix_deltas": {\n'
    + T*7 + '"_note": "ROUND 427 (2026-09-22): the BLL26x / 27x sub-series carry the PADDED lesson chip (BLL261_1.0.html: <h1>01</h1>) where the base says decimal (1.0) — 12 of 12 golds; BLL21x–25x keep decimal (BLL240 / 253 / 255 are the padded minority there).",\n'
    + T*7 + '"BLL26": { "module_code": { "lesson": "padded-number" } },\n'
    + T*7 + '"BLL27": { "module_code": { "lesson": "padded-number" } }\n'
    + T*6 + '},\n'
    + T*6 + '"template_deltas": {\n')
json.loads(s)
io.open(P, "w", encoding="utf-8", newline="").write(s)
print("PATCHED", len(s))
