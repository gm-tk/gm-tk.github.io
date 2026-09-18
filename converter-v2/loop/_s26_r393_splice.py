#!/usr/bin/env python3
"""Session 26 Round 7 (engine r393) — GLYPH-ONLY LINES RENDER NOTHING: a free-body line whose whole content is ONE
non-letter, non-digit glyph (`.` `,` `[` `]` `–` `*` `+` `-` `:` `=` `?` `)` `!` `✔`) never ships as a `<p>`.
Data: `body_region.drop_glyph_only_lines {enabled, env GLYPHLINE_OFF, keep}`. Engine: ListsAndRuns.renderBlackText's line
filter (free-body text only — `stitch` true; the placeholder / built-widget dumps untouched). Also writes the PICK.
LF preserved. Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 7 PICK (engine r393)" not in s:
    PICK = """## Session 26 — Round 7 PICK (engine r393): A GLYPH-ONLY LINE RENDERS NOTHING — a free-body paragraph whose whole content is one punctuation glyph never ships
- **The lead:** the r392 follow-through — the adjacent-list census's `<p>.</p>` between two lists (CHFUN06) → a paired census of PUNCTUATION-ONLY PARAGRAPHS (`outputs/_s26_r393_rowrow.py` part B → `_s26_r393_punct.py` / `.out`, every paired page's LIVE body, the r392 carve): **Claude ships 170 glyph-only `<p>`s on 69 pages / 64 modules; the gold ships the SAME glyph paragraph on 0 of those pages — dropped 170 / 170 = 1.00.** Per glyph: `.` 32 (21 pages / 19 modules), `,` 20 (ENGJ302's broken data set), `[` 19 (18 / 17 — a text-box bracket after an image), `]` 16, `✔` 16 (PNR102's `<p reo>` ticks), `–` 13, `*` 8, `+` 8, `-` 6, `:` 6, `=` 6, `?` 5, `)` 4, `!` 3. The gold's own glyph-only paragraphs (`?` 38 on 7 pages, `°` 6, `✓` / `✗` 5) sit on pages where Claude ships none — nothing to lose (SAME 0).
- **Measured and NOT taken this round:** (1) adjacent `<ol>` merge (`_s26_r393_adjol.py` / `.out`): 54 pages / 50 modules with a Claude pair — the gold FEWER-than-merged 0.59 (the gold often ships no `<ol>` at all there: AGH1005's tick-list is a radioButtons quiz, ARFUN04_0_0 pairs a 380 KB Claude page with an 87 KB gold phase page), MERGED 0.11, SAME 0.13 → no consensus, declined. (2) ROW-IN-ROW (`_s26_r393_rowrow.py` A / `_rowrow_gold.py` / `_rowchain.py` / `_unclosed.py`): the gold has 815 plain `row › row` nestings vs Claude's 4 — every one an UNCLOSED gold row (a `div.row` never closed, so the next rows nest inside it): 281 events on 213 pages / 144 modules, but the block before the un-closure predicts it at 0.01–0.03 (`div.activity.interactive` 70 / 2316, `p` 58 / 6568) — an authoring artefact, not a convention; the miner's #660 is its alignment shadow. Declined (recorded).
- **KB-first check:** nothing in the KB on a stray-punctuation paragraph (grep `stray`, `punctuation-only`, `empty paragraph`) → §1b level 3 / 4, the gold's own consensus 1.00 on 69 pages / 64 modules (Standard / English 7 pages, Inquiry / BLL 7, Maths 9, NCEA1 11 …). A dropped paragraph = structure-only → derivable (the line's content is one non-letter, non-digit character — a deterministic test on the WT text).
- **Fix (DATA OVER CODE):** `body_region.drop_glyph_only_lines {enabled, env: GLYPHLINE_OFF, keep: ["•"]}` — in `ListsAndRuns.renderBlackText`'s line filter (free-body text only, `stitch` true — the un-built-widget / built-widget dumps stay a faithful hand-off): a line that, with its `*` emphasis markers removed, is exactly ONE character that is not a letter (`\\p{L}`), not a digit (`\\p{N}`), not `_` and not a kept glyph, is dropped before it can become a `<p>` (a lone `•` stays with the bullet path's own empty-item rule). OFF = the r392 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #5 since the r388 full.

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"drop_glyph_only_lines"' not in s:
    old = '\t\t"closer_residue_strip": {\n'
    assert s.count(old) == 1
    new = ('\t\t"drop_glyph_only_lines": {\n'
           '\t\t\t"_doc": "ROUND 393 (the autonomous loop\'s session 26 Round 7 — the paired census outputs/_s26_r393_punct.py). A free-body line whose whole content is ONE punctuation glyph (a writer\'s stray `.` / `,`, a text-box bracket `[` / `]` left after an image, a broken equation\'s `+` `=` `–`, PNR102\'s `✔` ticks) shipped as `<p>.</p>`: Claude 170 on 69 pages / 64 modules; the gold ships the same glyph paragraph on NONE of them (dropped 170 / 170 = 1.00). In ListsAndRuns.renderBlackText\'s line filter, free-body text only (stitch true — the placeholder / built-widget dumps stay a faithful hand-off): a line that, with its `*` emphasis markers removed, is exactly one character that is not a letter, not a digit, not `_` and not in `keep`, is dropped before it can become a paragraph. `•` is kept for the bullet path\'s own empty-item rule. OFF = the r392 output.",\n'
           '\t\t\t"enabled": true,\n'
           '\t\t\t"env": "GLYPHLINE_OFF",\n'
           '\t\t\t"keep": [\n'
           '\t\t\t\t"•"\n'
           '\t\t\t]\n'
           '\t\t},\n' + old)
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: drop_glyph_only_lines added")
else:
    print("data: already")

P2 = PF + "/app/js/ListsAndRuns.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "drop_glyph_only_lines" not in s:
    old = "\t\tconst lines = text.split(/\\n+/).filter((l) => l.trim());\n"
    assert s.count(old) == 1, s.count(old)
    new = ("\t\tlet lines = text.split(/\\n+/).filter((l) => l.trim());\n"
           "\t\t// ROUND 393 — GLYPH-ONLY LINE DROP. A free-body line whose whole content is ONE punctuation\n"
           "\t\t// glyph (a writer's stray \".\" / \",\", a text-box bracket \"[\" / \"]\" left behind after an image,\n"
           "\t\t// a broken equation's \"+\" \"=\" \"–\", PNR102's \"✔\" ticks) shipped as <p>.</p>: Claude 170 on 69\n"
           "\t\t// pages / 64 modules, the gold NONE of them (dropped 170 / 170). The line — with its * emphasis\n"
           "\t\t// markers removed — must be exactly one character that is not a letter, not a digit, not \"_\"\n"
           "\t\t// and not a kept glyph (\"•\" stays for the bullet path's own empty-item rule). Free-body text\n"
           "\t\t// only (stitch true): the placeholder / built-widget dumps stay a faithful hand-off.\n"
           "\t\t// Data flag: body_region.drop_glyph_only_lines. Env toggle: GLYPHLINE_OFF.\n"
           "\t\tconst _glyphCfg = tpl.body_region?.drop_glyph_only_lines;\n"
           "\t\tif (stitch && _glyphCfg && _glyphCfg.enabled !== false\n"
           "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_glyphCfg.env ?? \"GLYPHLINE_OFF\"])) {\n"
           "\t\t\tconst keep = new Set((_glyphCfg.keep ?? [\"•\"]).map(String));\n"
           "\t\t\tlines = lines.filter((l) => {\n"
           "\t\t\t\tconst g = l.trim(), t = g.replace(/\\*/g, \"\").trim() || g;   // a lone \"*\" is itself the glyph\n"
           "\t\t\t\treturn !([...t].length === 1 && !/[\\p{L}\\p{N}_]/u.test(t) && !keep.has(t));\n"
           "\t\t\t});\n"
           "\t\t}\n")
    s = s.replace(old, new, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: renderBlackText glyph-only line drop")
else:
    print("engine: already")
