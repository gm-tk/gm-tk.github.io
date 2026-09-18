#!/usr/bin/env python3
"""Session 26 Round 5 (engine r391) — the own-row supervisor panel's TEXT column is `col-12 col-md-12` in the Leaving to Learn family.
Data: `callouts.by_tag."supervisor note".inner_row.text_col_by_subject {enabled, env PANELCOL_OFF, by_subject}`.
Engine: `#calloutOpen`'s inner_row def swap replaces the LAST `<div class="col-12">` of the open string with the subject's class.
Also writes the PICK into LOOP_STATE.md. LF preserved. Idempotent. Run under WSL: python3 _s26_r391_splice.py"""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

# ---- PICK ----
LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 5 PICK (engine r391)" not in s:
    PICK = """## Session 26 — Round 5 PICK (engine r391): the own-row SUPERVISOR PANEL'S TEXT COLUMN is `col-12 col-md-12` in the Leaving to Learn family
- **The lead:** the r390 miner's ONE new row #3735 (`body EXTRA div.col-12 › ul`, 32 pages / 14 modules, LtL 26 pages, series XDLS90 c = 1.00) — a parent-LABEL mismatch: the gold's panel text column is `div.col-12.col-md-12`, Claude's r160 inner-row template writes `col-12`, so the miner keys the gold's `ul` under a different parent.
- **The census (`outputs/_s26_r391_panelcol.py` → `.out`; `_s26_r391_panelcol2.out` the activity / own-row split):** every gold super-content panel's text column (the inner row's last col) — corpus-wide `col-12` 327 / `col-12 col-md-12` 93 (Claude's `col-12` is the majority form and stays the default); per group: **Leaving to Learn OWN-ROW panels `col-12 col-md-12` 28 / 37 = 0.76 (35 pages, 15 modules; XDLS9 28 / 37)**; LtL ACTIVITY-owned panels 7 / 19 = 0.37 (keep `col-12`); English own-row 7 / 9 = 0.78 (9 pages — under the floor), English activity 9 / 9 (a tie); ConnectED own-row 1 / 5; BLL 3 / 169; Mathematics 8 / 33; OS 2 / 4. Solidify (r182): LtL own-row only.
- **KB-first check:** 05B / 01F give the panel form with `col-12` columns (the BLL / MXDI majority); the LtL family's `col-md-12` text column is its own consensus → §1b level 4 (subject). Structure-only (a wrapper class token) → derivable.
- **Fix (DATA OVER CODE):** `callouts.by_tag."supervisor note".inner_row.text_col_by_subject {enabled, env: PANELCOL_OFF, by_subject: {"Leaving to Learn": "col-12 col-md-12"}}` — `#calloutOpen`'s inner_row def swap rewrites the LAST `<div class="col-12">` of the open string to the subject's class (the module's `module_meta.subject`); the activity-owned panel template (`activity_wrapper.super_content.panel_open`) is untouched. OFF = the r390 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #3 since the r388 full.
- **Not taken:** the activity-owned panel's column (LtL 0.37, English 0.50 — ties); the English own-row panels (9 pages); the label text (`Supervisor` vs `Supervisor note` — text, invisible to the skeleton).

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

# ---- data ----
P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"text_col_by_subject"' not in s:
    old = ('\t\t\t\t"inner_row": {\n\t\t\t\t\t"enabled": true,\n\t\t\t\t\t"_note": "ROUND 160')
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t\t"inner_row": {\n\t\t\t\t\t"enabled": true,\n'
           '\t\t\t\t\t"text_col_by_subject": {\n'
           '\t\t\t\t\t\t"enabled": true,\n'
           '\t\t\t\t\t\t"env": "PANELCOL_OFF",\n'
           '\t\t\t\t\t\t"by_subject": {\n'
           '\t\t\t\t\t\t\t"Leaving to Learn": "col-12 col-md-12"\n'
           '\t\t\t\t\t\t},\n'
           '\t\t\t\t\t\t"_doc": "ROUND 391 (the autonomous loop\'s session 26 Round 5 — the r390 miner row #3735 decomposed by outputs/_s26_r391_panelcol.py). The own-row supervisor panel\'s TEXT column (the inner row\'s second col) is `col-12` corpus-wide (gold 327 / 93 — the BLL / MXDI majority, the template\'s default) but `col-12 col-md-12` in the Leaving to Learn family (own-row panels 28 / 37 = 0.76 on 35 pages / 15 modules; the XDLS90x series 28 / 37). The module\'s Module_Structure_Index subject picks the class; the LAST `<div class=\\"col-12\\">` of the inner_row open is rewritten. The activity-owned panel template (activity_wrapper.super_content.panel_open) is untouched (LtL 0.37, English 0.50 — ties). OFF = the r390 output."\n'
           '\t\t\t\t\t},\n'
           '\t\t\t\t\t"_note": "ROUND 160')
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: text_col_by_subject added")
else:
    print("data: already")

# ---- engine ----
P2 = PF + "/app/js/ContentConverter.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "text_col_by_subject" not in s:
    old = ("\t\t\tdef = Object.assign({}, def, { open: _irCfg.open, close: _irCfg.close });\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\tlet _irOpen = _irCfg.open;\n"
           "\t\t\t// ROUND 391 (the autonomous loop's session 26 Round 5): the panel's TEXT column class by subject — the\n"
           "\t\t\t// Leaving to Learn family's own-row panels carry `col-12 col-md-12` (gold 28 / 37 = 0.76); the LAST\n"
           "\t\t\t// `<div class=\"col-12\">` of the inner_row open is the text column. Data inner_row.text_col_by_subject; env PANELCOL_OFF.\n"
           "\t\t\tconst _tcCfg = _irCfg.text_col_by_subject;\n"
           "\t\t\tif (_tcCfg && _tcCfg.enabled !== false\n"
           "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_tcCfg.env ?? \"PANELCOL_OFF\"])) {\n"
           "\t\t\t\tconst _subj = String(DataService.Data.ModuleStructureIndex?.module_meta?.[String(run?.moduleCode || \"\")]?.subject ?? \"\");\n"
           "\t\t\t\tconst _cls = _subj && (_tcCfg.by_subject ?? {})[_subj];\n"
           "\t\t\t\tconst _needle = '<div class=\"col-12\">';\n"
           "\t\t\t\tconst _at = _cls ? _irOpen.lastIndexOf(_needle) : -1;\n"
           "\t\t\t\tif (_at >= 0) _irOpen = _irOpen.slice(0, _at) + `<div class=\"${_cls}\">` + _irOpen.slice(_at + _needle.length);\n"
           "\t\t\t}\n"
           "\t\t\tdef = Object.assign({}, def, { open: _irOpen, close: _irCfg.close });\n")
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: text column by subject")
else:
    print("engine: already")
