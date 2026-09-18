#!/usr/bin/env python3
"""Session 27 Round 2 (r399) — THE WĀNANGA / TALANOA BOX IS THE KB'S CULTURAL ALERT. Applies the three data edits + the engine
edits with exact-string assertions, LF preserved (io.open newline=''). Idempotent (each edit checks its marker first).
  wsl: python3 _s27_r399_patch.py"""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
ENG = os.path.join(ROOT, "pageforge-site", "converter-v2")
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s): io.open(p, "w", encoding="utf-8", newline="").write(s)
def patch(path, old, new, marker):
    s = rd(path)
    if marker in s:
        print("  already:", os.path.basename(path), marker[:40]); return
    assert s.count(old) == 1, (path, old[:80], s.count(old))
    wr(path, s.replace(old, new, 1)); print("  patched:", os.path.basename(path), marker[:50])

# ---------- 1. Emit_Templates.json — callouts.by_tag.wananga ----------
ET = os.path.join(ENG, "data", "Emit_Templates.json")
old = ('\t\t\t"wananga": {\n'
       '\t\t\t\t"open": "<div class=\\"wananga{modifiers}\\">",\n'
       '\t\t\t\t"close": "</div>"\n'
       '\t\t\t},\n'
       '\t\t\t"whakatauki": {')
new = ('\t\t\t"wananga": {\n'
       '\t\t\t\t"open": "<div class=\\"wananga{modifiers}\\">",\n'
       '\t\t\t\t"close": "</div>",\n'
       '\t\t\t\t"kb_form": {\n'
       '\t\t\t\t\t"enabled": true,\n'
       '\t\t\t\t\t"env": "WANANGA_OFF",\n'
       '\t\t\t\t\t"open": "<div class=\\"alert cultural\\" layout=\\"combined\\">",\n'
       '\t\t\t\t\t"close": "</div>",\n'
       '\t\t\t\t\t"wrap_content": true\n'
       '\t\t\t\t},\n'
       '\t\t\t\t"table_cell_content": {\n'
       '\t\t\t\t\t"enabled": true,\n'
       '\t\t\t\t\t"env": "WANANGA_OFF"\n'
       '\t\t\t\t},\n'
       '\t\t\t\t"_round399_note": "ROUND 399 (the autonomous loop, session 27 Round 2) — THE WĀNANGA / TALANOA BOX IS THE KB\'S CULTURAL ALERT. '
       'The CED Phase-5 writers (CEDK501 / CEDO501 / CEDO502 / CEDR501 / CEDT501 / CEDW501) type `[Wānanga/Talanoa box]` (and `[Wananga box]`, `[Talanoa/Wananga box]`, '
       'the typos `[Wanana/…]` / `[Wananaga/…]`, CEDT501\'s `[Banner - Wānanga/Talanoa box]`) on its own line, then a ONE-CELL table holding the discussion prompt. '
       'The gold renders every one as KB 05B\'s Cultural Alert `<div class=\\"alert cultural\\" layout=\\"combined\\"> > row > col-12 > p…` (63 / 63 gold boxes are '
       '`combined` — KB 14A §14.4 ConnectED Phase 5: \'all alerts are combined unless otherwise specified\'; a bulleted cell becomes a <ul>; no h4 — 0 / 63). '
       'Claude shipped an EMPTY `div.wananga` + a red flag (the strict gather finds no black text before the table) + the writer\'s table as a kept `table.table-bordered` '
       '(56 flags / 35 pages / 6 modules). Measured `outputs/_s27_r2_wananga.py` (69 tag sites / 7 modules) + `_s27_r2_callouttbl.py` (every callout tag typed bare + a '
       'one-cell table, all 416 WTs: the idiom is exactly this class — 55 sites / 6 modules / 37 gold pages, gold `alert cultural` 50 = 0.91; the only other carrier is '
       '`[alert]` on TEDC402\'s page-layout tables, gold not found). kb_form: #calloutOpen swaps the def\'s open / close / wrap_content when on (the legacy `div.wananga` '
       'is the OFF form). table_cell_content: in STRICT mode a callout whose own gather is empty and whose NEXT item is a one-row one-cell table takes the cell as its content '
       'through TablesAndGrids.renderCellParts (a <p> per \' / \'-part, \'• \' lines → a <ul>, the cell\'s own [H*] / [image] parts honoured) and marks the table consumed; '
       '#calloutWrapsStructured yields to it. The Banner form rides Tag_Lexicon._meta.tag_promote (carousel → wananga). ONE env WANANGA_OFF reverts all three."\n'
       '\t\t\t},\n'
       '\t\t\t"whakatauki": {')
patch(ET, old, new, '"_round399_note"')

# ---------- 2. Tag_Lexicon.json — tag_promote rule carousel → wananga ----------
TL = os.path.join(ENG, "data", "Tag_Lexicon.json")
old = ('\t\t\t\t\t"mark": "summary_box",\n'
       '\t\t\t\t\t"env": "SUMMARYBOX_OFF",\n')
s = rd(TL)
assert s.count(old) == 1
# find the end of the r304 rule object (the next "\t\t\t\t}" after old) and insert a new rule after it
i = s.index(old); j = s.index("\n\t\t\t\t}", i) + len("\n\t\t\t\t}")
rule = (',\n'
        '\t\t\t\t{\n'
        '\t\t\t\t\t"from": "carousel",\n'
        '\t\t\t\t\t"to": "wananga",\n'
        '\t\t\t\t\t"to_directive": "CONTAINER_OPEN",\n'
        '\t\t\t\t\t"when_match": "^\\\\s*\\\\[\\\\s*banner\\\\s*[-\\u2013\\u2014:]\\\\s*w[\\u0101a]nanga",\n'
        '\t\t\t\t\t"env": "WANANGA_OFF",\n'
        '\t\t\t\t\t"_doc": "ROUND 399 (the autonomous loop, session 27 Round 2). CEDT501\'s `[Banner - Wānanga/Talanoa box]` is the same cultural alert as every other '
        '`[Wānanga/Talanoa box]` (its 10 gold pages ship `alert cultural` layout=combined) but the `banner` alias resolves the span to the carousel / rotateBanner INTERACTIVE, '
        'which opens a bundle that captures the writer\'s one-cell table and declines. The promote rewrites the carousel tag to the wananga container on the `[Banner - Wānanga…` '
        'spelling only (the anchor excludes `[Rolling Banner - …]`, one site whose 4-cell strip the gold dropped). Env WANANGA_OFF (the round\'s single toggle)."\n'
        '\t\t\t\t}')
if '"to": "wananga"' not in s:
    assert s[j:j+3] == "\n\t\t\t]" or s[j:j+2] == "\n\t", repr(s[j:j+20])
    s = s[:j] + rule + s[j:]
    wr(TL, s); print("  patched: Tag_Lexicon.json tag_promote carousel→wananga")
else:
    print("  already: Tag_Lexicon.json tag_promote")

# ---------- 3. ContentConverter.js ----------
CC = os.path.join(ENG, "app", "js", "ContentConverter.js")
# 3a. kb_form swap right after the unknown-container guard
old = ('\t\tif (!def) {\n'
       '\t\t\treturn [NotesAndComments.redFlag(\n'
       '\t\t\t\t`Unknown container [${tag}] — content kept below without a wrapper; add it to Emit_Templates callouts.`, run)];\n'
       '\t\t}\n')
new = old + (
       '\t\t// ROUND 399 (the autonomous loop\'s session 27 Round 2): THE WĀNANGA / TALANOA BOX IS THE KB\'S CULTURAL ALERT.\n'
       '\t\t// KB 05B "Cultural Alert (Wānanga / Talanoa)" + 14A §14.4 (ConnectED Phase 5: "all alerts are combined unless\n'
       '\t\t// otherwise specified"): the gold renders every [Wānanga/Talanoa box] as <div class="alert cultural"\n'
       '\t\t// layout="combined"> > row > col-12 > p… (63 / 63 gold boxes). A callout def carrying kb_form swaps to that\n'
       '\t\t// open / close / wrap; the legacy open / close stay as the OFF form.\n'
       '\t\t// Data flag: callouts.by_tag.<tag>.kb_form   Env toggle: the def\'s own env (WANANGA_OFF)\n'
       '\t\tconst _kbf = def.kb_form;\n'
       '\t\tif (_kbf && _kbf.enabled !== false && _kbf.open\n'
       '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_kbf.env ?? "WANANGA_OFF"])) {\n'
       '\t\t\tdef = Object.assign({}, def, { open: _kbf.open, close: _kbf.close ?? def.close,\n'
       '\t\t\t\twrap_content: _kbf.wrap_content ?? def.wrap_content });\n'
       '\t\t}\n')
patch(CC, old, new, "const _kbf = def.kb_form;")

# 3b. the strict-mode table-cell content
old = ('\t\tlet content = def.proverb_only\n'
       '\t\t\t? this.#gatherProverb(it, bodyItems, i, def)\n'
       '\t\t\t: MediaBuilder.gatherFollowing(it, bodyItems, i);\n')
new = old + (
       '\t\t// ROUND 399: A CALLOUT TYPED BARE + A ONE-CELL TABLE — the cell IS the box\'s content. The CED Phase-5\n'
       '\t\t// writers put the wānanga / talanoa prompt in a one-row one-cell table under the tag; the strict gather\n'
       '\t\t// sees no black text (the next item is the table) and the box shipped EMPTY with a red flag, the table as a\n'
       '\t\t// kept <table>. The gold dissolves the cell into the box\'s own <p>s (a <ul> for "• " lines) — 50 / 55 sites.\n'
       '\t\t// Measured over every callout tag on all 416 WTs (outputs/_s27_r2_callouttbl.py): the idiom is exactly the\n'
       '\t\t// wananga class, so it is opt-in per def. The table is marked consumed (the emit site\'s `while _consumed`\n'
       '\t\t// skip steps over it); #calloutWrapsStructured yields to this rule so the box never span-wraps a kept table.\n'
       '\t\t// Data flag: callouts.by_tag.<tag>.table_cell_content   Env toggle: its env (WANANGA_OFF)\n'
       '\t\tlet _tcParts = null;\n'
       '\t\tconst _tcTable = content.trim() ? null : this.#calloutTableCell(it, bodyItems, i, def);\n'
       '\t\tif (_tcTable) {\n'
       '\t\t\tconst _cell = (_tcTable.block.rows[0] || []).find((c) => String(c ?? "").trim() !== "");\n'
       '\t\t\t_tcParts = TablesAndGrids.renderCellParts(_cell, run, this.#norm, _tcTable.block?.links).filter(Boolean);\n'
       '\t\t\tif (_tcParts.length) _tcTable._consumed = true; else _tcParts = null;\n'
       '\t\t}\n')
patch(CC, old, new, "const _tcTable = content.trim() ? null")

old = ('\t\tif (content.trim()) out.push(...deProv(deBold(deItal(ListsAndRuns.renderBlackText(content, run, it.block?.links)))));\n')
new = old + '\t\tif (_tcParts) out.push(...deProv(deBold(deItal(_tcParts))));   // ROUND 399: the one-cell table\'s cell\n'
patch(CC, old, new, "if (_tcParts) out.push(")

old = '\t\tif (!lead && !longPayload && !content.trim() && !absorbedInline) {\n'
new = '\t\tif (!lead && !longPayload && !content.trim() && !absorbedInline && !_tcParts) {\n'
patch(CC, old, new, "&& !absorbedInline && !_tcParts) {")

# 3c. #calloutWrapsStructured yields + the new helper
old = ('\tstatic #calloutWrapsStructured(it, bodyItems, i) {\n'
       '\t\tconst def = DataService.Data.EmitTemplates.callouts.by_tag[it.parse.primary?.tag];\n'
       '\t\tif (!def || !def.wrap_content) return false;        // only content callouts wrap\n')
new = ('\t/**\n'
       '\t * ROUND 399: the ONE-ROW ONE-CELL table right after a bare callout tag, when the def opts in\n'
       '\t * (callouts.by_tag.<tag>.table_cell_content) — the cell is the box\'s own content (the wānanga / talanoa\n'
       '\t * prompt). Returns the table item or null. The env toggle is the def\'s own (WANANGA_OFF).\n'
       '\t */\n'
       '\tstatic #calloutTableCell(it, bodyItems, i, def) {\n'
       '\t\tconst cfg = def?.table_cell_content;\n'
       '\t\tif (!cfg || cfg.enabled === false) return null;\n'
       '\t\tif (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "WANANGA_OFF"]) return null;\n'
       '\t\tif ((it.blackAfter ?? "").trim()) return null;\n'
       '\t\tconst next = bodyItems[i + 1];\n'
       '\t\tif (!next || next.type !== "table" || next.consumedBy !== undefined || next._consumed) return null;\n'
       '\t\tconst rows = next.block?.rows ?? [];\n'
       '\t\tif (rows.length !== 1) return null;\n'
       '\t\tconst cells = (rows[0] || []).filter((c) => String(c ?? "").trim() !== "");\n'
       '\t\tif (cells.length !== 1) return null;\n'
       '\t\treturn next;\n'
       '\t};\n\n'
       '\tstatic #calloutWrapsStructured(it, bodyItems, i) {\n'
       '\t\tconst def = DataService.Data.EmitTemplates.callouts.by_tag[it.parse.primary?.tag];\n'
       '\t\tif (this.#calloutTableCell(it, bodyItems, i, def)) return false;   // ROUND 399: the cell is the strict content\n'
       '\t\tif (!def || !def.wrap_content) return false;        // only content callouts wrap\n')
patch(CC, old, new, "static #calloutTableCell(it, bodyItems, i, def)")
print("done")
