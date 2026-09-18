#!/usr/bin/env python3
"""Session 26 Round 6 (engine r392) — ADJACENT SIBLING LISTS MERGE: `</ul>` + whitespace + `<ul>` in the live body becomes one list.
Data: `body_region.merge_adjacent_lists {enabled, env ULMERGE_OFF, tags, verbatim_widget_classes}`.
Engine: `ListsAndRuns.MergeAdjacentLists(html)` (the r337 carve: cv2 dumps / notes / verbatim widgets untouched), wired in
PageAssembler right after TypedNumberList. Also writes the PICK. LF preserved. Idempotent. Run under WSL."""
import io, os, sys
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"

LS = ROOT + "/LOOP_STATE.md"
s = io.open(LS, encoding="utf-8", newline="").read()
if "## Session 26 — Round 6 PICK (engine r392)" not in s:
    PICK = """## Session 26 — Round 6 PICK (engine r392): ADJACENT SIBLING LISTS are ONE list — a writer's bullet run split into two `<ul>`s by an item that rendered nothing
- **The lead:** the r391 miner's one new row #4286 (`body EXTRA div.col-12.col-md-12 › ul`, 21 pages / 3 modules) — XDLS904 / 905 / 906's panel bullets, each ending in an inline red `[link to X]` marker that renders nothing: the marker splits the black run, so `• XFUN01 Ebb and Flow` and `• XLP05 Visual Supports` ship as TWO `<ul>`s where the gold ships one.
- **The census (`outputs/_s26_r392_adjul.py` → `.out` — every paired page's LIVE body, the cv2 dumps / notes / r337 verbatim widgets carved out):** `</ul>` immediately followed by `<ul>` — **Claude 106 pairs on 54 pages / 34 modules; the gold 3 pairs on 3 pages** (English 1, ConnectED 1, Inquiry 1) → the gold's convention 0.97: two sibling lists never sit adjacent. Per subject: Leaving to Learn 27 (23 pages / 5 modules), NCEA1 20 (7 / 7), English 18 (7 / 6), the subject-less TEDC 17 (2), Fundamentals LtL 7, Mathematics 6, ConnectED 5, Arts 3. Many mechanisms split the run (the inline marker, a consumed item, an image between bullets — AGH1002 / AGH1006 / AGH1009's bullets) and every one of them ends in the same gold form.
- **`ol` is NOT taken:** Claude 202 adjacent `<ol>` pairs, gold 0 — but the r337 typed-number rule and Word's numbering restarts make a second `<ol>` a NEW numbered list (1, 2, 3 / 1, 2); merging would renumber the writer's steps. Measure the gold's form for a restart before touching it (recorded).
- **KB-first check:** 05D / constraint 42 give `<ul><li>` for a bullet run; nothing on a split run → §1b level 3 / 4 (the gold's own consensus, 0.97 corpus-wide). Structure-only → derivable.
- **Fix (DATA OVER CODE):** `body_region.merge_adjacent_lists {enabled, env: ULMERGE_OFF, tags: [ul]}` — `ListsAndRuns.MergeAdjacentLists(html)`, a full-page post-pass at the r337 seam (PageAssembler, after TypedNumberList, before LinkTextDisplay; body only, the same verbatim zones): a bare `</ul>` followed only by whitespace and a bare `<ul>` becomes one list. OFF = the r391 output. Regeneration: SCOPED (the probe's ON list) = scoped ship #4 since the r388 full.

"""
    i = s.index("## Round log\n")
    s = s[:i] + PICK + s[i:]
    io.open(LS, "w", encoding="utf-8", newline="").write(s); print("PICK written")

P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"merge_adjacent_lists"' not in s:
    old = '\t\t"typed_number_list": {\n'
    assert s.count(old) == 1
    new = ('\t\t"merge_adjacent_lists": {\n'
           '\t\t\t"_doc": "ROUND 392 (the autonomous loop\'s session 26 Round 6 — the r391 miner row #4286 decomposed; the census outputs/_s26_r392_adjul.py). A writer\'s bullet run split into two sibling `<ul>`s by an item that rendered nothing (a bullet\'s trailing inline `[link to X]` marker, a consumed item, an image between bullets) — Claude shipped 106 adjacent `</ul> <ul>` pairs on 54 pages / 34 modules in the live body; the gold ships 3 on 3 pages (0.97 one list). `ListsAndRuns.MergeAdjacentLists`, a full-page post-pass at the r337 seam (after TypedNumberList, before LinkTextDisplay; body only; the same verbatim zones — cv2 dumps, notes, the listed built widgets): a bare `</ul>` followed only by whitespace and a bare `<ul>` joins into one list. `ol` deliberately NOT listed (202 Claude pairs / gold 0 — a restart at 1 is a new numbered list; measure first). OFF = the r391 output.",\n'
           '\t\t\t"enabled": true,\n'
           '\t\t\t"env": "ULMERGE_OFF",\n'
           '\t\t\t"tags": [\n'
           '\t\t\t\t"ul"\n'
           '\t\t\t]\n'
           '\t\t},\n' + old)
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: merge_adjacent_lists added")
else:
    print("data: already")

P2 = PF + "/app/js/ListsAndRuns.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "static MergeAdjacentLists" not in s:
    old = "\tstatic TypedNumberList(html) {\n"
    assert s.count(old) == 1
    fn = (
        "\t/**\n"
        "\t * ADJACENT SIBLING LISTS → ONE LIST (round 392). A writer's bullet run split into two\n"
        "\t * sibling <ul>s by an item that rendered nothing (a bullet's trailing inline [link to X]\n"
        "\t * marker, a consumed item, an image between bullets): Claude shipped 106 adjacent\n"
        "\t * `</ul> <ul>` pairs on 54 pages / 34 modules, the gold 3 (0.97 one list). A full-page\n"
        "\t * post-pass at the TypedNumberList seam (body only, the same verbatim zones): a bare\n"
        "\t * </ul> followed only by whitespace and a bare <ul> joins. Only the data-listed tags\n"
        "\t * (ul — an <ol> restart is a new numbered list). Data body_region.merge_adjacent_lists;\n"
        "\t * env ULMERGE_OFF.\n"
        "\t * @param {string} html - one finished page's HTML (before the acks block)\n"
        "\t * @returns {string}\n"
        "\t */\n"
        "\tstatic MergeAdjacentLists(html) {\n"
        "\t\tconst cfg = DataService.Data.EmitTemplates?.body_region?.merge_adjacent_lists;\n"
        "\t\tif (!cfg || cfg.enabled === false) return html;\n"
        "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env || \"ULMERGE_OFF\"]) return html;\n"
        "\t\tconst src = String(html);\n"
        "\t\tconst tags = (cfg.tags ?? [\"ul\"]).map((t) => String(t).toLowerCase()).filter((t) => /^[a-z]+$/.test(t));\n"
        "\t\tif (!tags.length) return src;\n"
        "\t\tconst joinRe = new RegExp(\"</(\" + tags.join(\"|\") + \")>(\\\\s*)<\\\\1>\", \"g\");\n"
        "\t\tif (!joinRe.test(src)) return src;\n"
        "\t\tjoinRe.lastIndex = 0;\n"
        "\t\tconst tnl = DataService.Data.EmitTemplates?.body_region?.typed_number_list;\n"
        "\t\tconst widgets = ((cfg.verbatim_widget_classes ?? tnl?.verbatim_widget_classes) ?? []).map((c) => String(c).replace(/[.*+?^${}()|[\\]\\\\]/g, \"\\\\$&\"));\n"
        "\t\tconst openRe = new RegExp(\"<div class=\\\"(?:cv2-interactive|\" + widgets.join(\"|\")\n"
        "\t\t\t+ \")|<p class=\\\"cv2-(?:note|comment)\\\"|<script\\\\b|<style\\\\b\", \"g\");\n"
        "\t\tconst pieces = [];\n"
        "\t\t{\n"
        "\t\t\tlet i = 0, m;\n"
        "\t\t\twhile ((m = openRe.exec(src))) {\n"
        "\t\t\t\tconst j = m.index;\n"
        "\t\t\t\tlet end;\n"
        "\t\t\t\tif (m[0].startsWith(\"<div\")) {\n"
        "\t\t\t\t\tconst re = /<div\\b|<\\/div>/g;\n"
        "\t\t\t\t\tre.lastIndex = j; let depth = 0, mm; end = src.length;\n"
        "\t\t\t\t\twhile ((mm = re.exec(src))) {\n"
        "\t\t\t\t\t\tdepth += mm[0] === \"</div>\" ? -1 : 1;\n"
        "\t\t\t\t\t\tif (depth === 0) { end = re.lastIndex; break; }\n"
        "\t\t\t\t\t}\n"
        "\t\t\t\t} else if (m[0].startsWith(\"<p\")) {\n"
        "\t\t\t\t\tconst k = src.indexOf(\"</p>\", j); end = k < 0 ? src.length : k + 4;\n"
        "\t\t\t\t} else {\n"
        "\t\t\t\t\tconst close = m[0].startsWith(\"<script\") ? \"</script>\" : \"</style>\";\n"
        "\t\t\t\t\tconst k = src.indexOf(close, j); end = k < 0 ? src.length : k + close.length;\n"
        "\t\t\t\t}\n"
        "\t\t\t\tif (j > i) pieces.push({ live: true, s: src.slice(i, j) });\n"
        "\t\t\t\tpieces.push({ live: false, s: src.slice(j, end) });\n"
        "\t\t\t\ti = end; openRe.lastIndex = end;\n"
        "\t\t\t}\n"
        "\t\t\tif (i < src.length) pieces.push({ live: true, s: src.slice(i) });\n"
        "\t\t}\n"
        "\t\treturn pieces.map((p) => (p.live ? p.s.replace(joinRe, \"$2\") : p.s)).join(\"\");\n"
        "\t};\n\n"
    )
    s = s.replace(old, fn + old, 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: ListsAndRuns.MergeAdjacentLists")
else:
    print("engine: already")

P3 = PF + "/app/js/PageAssembler.js"
s = io.open(P3, encoding="utf-8", newline="").read()
if "MergeAdjacentLists" not in s:
    old = "\t\t\t\t\t\tconst deEmoji = (seg) => ListsAndRuns.TypedNumberList(ListsAndRuns.EmojiStrip(seg, () =>\n"
    assert s.count(old) == 1, s.count(old)
    new = ("\t\t\t\t\t\t// ROUND 392: adjacent sibling lists join into one (body_region.merge_adjacent_lists; env ULMERGE_OFF) — after TypedNumberList, before the link-text pass.\n"
           "\t\t\t\t\t\tconst deEmoji = (seg) => ListsAndRuns.MergeAdjacentLists(ListsAndRuns.TypedNumberList(ListsAndRuns.EmojiStrip(seg, () =>\n")
    s = s.replace(old, new, 1)
    # close the extra paren: the original call ends `run, "diagnostic")));` — find the line after and add one `)`
    old2 = "\t\t\t\t\t\t\t\trun, \"diagnostic\")));\n"
    assert s.count(old2) == 1, s.count(old2)
    s = s.replace(old2, "\t\t\t\t\t\t\t\trun, \"diagnostic\"))));\n", 1)
    io.open(P3, "w", encoding="utf-8", newline="").write(s); print("PageAssembler: wired")
else:
    print("PageAssembler: already")
