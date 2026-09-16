#!/usr/bin/env python3
"""ROUND 350 (loop session 14 Round 1 — Chris's D10-3: the dragAndDrop build kickoff, shape (1) the IMAGE-PAIR table → the KB 03B
`dragAndDrop images` standard form; + the KB button row on every built standard dragAndDrop) — the splice.

(1) data/Emit_Templates.json: `interactive_builders.dragAndDrop` gains `button_row` {enabled, env DDBUTTONS_OFF, close_inner, html,
    close_outer, note} and `images` {enabled, env DDIMAGES_OFF, open, mid, drag, image_mode_D/P/P_comment, filename_istock,
    header_row_skip, image_tag_pattern, note} — inserted TEXTUALLY after `"min_rows": 2,` (tab-indented, never json.dumps — CLAUDE.md §16).
(2) app/js/InteractiveBuilder.js: the dispatch gains `?? this.#dragAndDropImages(...)`; `#dragAndDrop`'s close goes through `#ddClose`;
    three new statics `#ddClose`, `#dragAndDropImages`, `#ddImage` after `#dragAndDrop`.
Idempotent. LF kept. §6 atomic writes: encode first, temp file, `node --check` / a duplicate-key JSON load, then os.replace."""
import io, os, json, subprocess, sys
PF = r"C:\Users\Gavin\TeKura\FINAL_MODULE_DATA\pageforge-site\converter-v2"
def rd(p):
    with io.open(p, encoding="utf-8", newline="") as f: return f.read()
def atomic(p, s, check):
    b = s.encode("utf-8"); assert len(b) > 10000, "refusing a near-empty write"
    tmp = p[:-len(os.path.splitext(p)[1])] + ".r350tmp" + os.path.splitext(p)[1]
    with open(tmp, "wb") as f: f.write(b)
    ok, msg = check(tmp)
    if not ok: os.remove(tmp); sys.exit(f"CHECK FAILED for {p}: {msg}")
    os.replace(tmp, p)
def js_ok(tmp):
    r = subprocess.run(["node", "--check", tmp], capture_output=True, text=True); return r.returncode == 0, r.stderr
def json_ok(tmp):
    def nodup(pairs):
        d = {}
        for k, v in pairs:
            if k in d: raise ValueError(f"duplicate key {k}")
            d[k] = v
        return d
    try: json.loads(rd(tmp), object_pairs_hook=nodup); return True, ""
    except Exception as e: return False, str(e)

# ------------------------------------------------------------------ (1) Emit_Templates.json
P = os.path.join(PF, "data", "Emit_Templates.json"); s = rd(P)
assert "\r\n" not in s, "CRLF in Emit_Templates.json?!"
if '"DDIMAGES_OFF"' not in s:
    A = '\t\t\t"min_rows": 2,\n\t\t\t"note": "ROUND 69 (Chris). dragAndDrop NARROW N:N TEXT-MATCHING form'
    assert s.count(A) == 1, "data anchor"
    BLOCK = '''\t\t\t"min_rows": 2,
\t\t\t"button_row": {
\t\t\t\t"enabled": true,
\t\t\t\t"env": "DDBUTTONS_OFF",
\t\t\t\t"close_inner": "</div>\\n</div>\\n</div>",
\t\t\t\t"html": "<div class=\\"row\\">\\n<div class=\\"activityButton reset\\">Reset</div>\\n<div class=\\"activityButton undo hidden\\">Undo</div>\\n<div class=\\"activityButton checkAnswer hidden\\">Check answers</div>\\n</div>",
\t\t\t\t"close_outer": "</div>",
\t\t\t\t"note": "ROUND 350 (Chris's D10-3, the dragAndDrop build kickoff — the autonomous loop's session-14 Round 1). KB 03B 'Standard Layout': every dragAndDrop ends with the activityButton row (Reset / Undo hidden / Check answers hidden). The r69 text form never emitted it; the gold carries it on 473 of its 517 standard D&Ds (0.92 — levels 1 and 3 agree). Applied to EVERY built standard dragAndDrop (the r69 text form and the r350 images form alike): the widget closes dragContainer / ddContainer / row (close_inner), emits html, then closes the dragAndDrop div (close_outer). Env DDBUTTONS_OFF restores the r69 `close` string byte-for-byte."
\t\t\t},
\t\t\t"images": {
\t\t\t\t"enabled": true,
\t\t\t\t"env": "DDIMAGES_OFF",
\t\t\t\t"open": "<div class=\\"dragAndDrop images\\" layout=\\"standard\\">\\n<div class=\\"row\\">\\n<div class=\\"col-7 questionContainer\\">",
\t\t\t\t"mid": "</div>\\n<div class=\\"col-5 ddContainer\\">\\n<div class=\\"dropContainer\\">",
\t\t\t\t"drag": "<div class=\\"drag\\" option=\\"{n}\\">{image}</div>",
\t\t\t\t"image_mode_D": "<img class=\\"img-fluid margB0\\" src=\\"images/{filename}\\" alt=\\"\\">",
\t\t\t\t"image_mode_P": "<img class=\\"img-fluid margB0\\" src=\\"https://placehold.co/600x400?text={label}\\" alt=\\"\\">",
\t\t\t\t"image_mode_P_comment": "<!-- <img class=\\"img-fluid margB0\\" src=\\"images/{filename}\\" alt=\\"\\"> -->",
\t\t\t\t"filename_istock": "iStock-{id}.jpg",
\t\t\t\t"header_row_skip": true,
\t\t\t\t"image_tag_pattern": "^\\\\[\\\\s*(?:insert\\\\s+)?image[^\\\\]]*\\\\]$",
\t\t\t\t"note": "ROUND 350 (Chris's D10-3 Option A — widget-BUILD rounds, one type per kickoff; the dragAndDrop kickoff's shape (1); the autonomous loop's session-14 Round 1). The writer's IMAGE-PAIR table — one 2-column table whose every data row pairs ONE image URL with ONE plain-text word / sentence, `image | word` (BLL112, BLL122, BLL161, BLL125, BLL220, BLL224, BLL230, BLL210, ENFUN02, MXFUN03, CHFUN05, TEFUN08, BLL244, ENGJ102) or `word | image` (BLL146, BLL130, BLL233, CEDO105, ENFUN04, ENGS201, BLL266) — builds the KB 03B 'Standard Layout — With images' form: `<div class=\\"dragAndDrop images\\" layout=\\"standard\\">`, the TEXT side is ALWAYS the fixed question side (col-7 questionContainer, one .question per row) and the IMAGES are the draggable items (col-5 ddContainer: dropContainer with a .drop per row, dragContainer with a .drag holding the image per row, option = the 1-based row index = the answer key) — 03B's placement rule ('images in the questionContainer stretch vertically and make the interactive unusably tall'), whichever way round the writer typed the columns; margB0 on the drag images (03B); the KB button row follows (button_row). The image: an iStock id → filename_istock, any other host → the r278 URL-slug placeholder (#accImageFilename); rendered in the run's image mode through the r240 FinishImg rider (the URL is passed, so the alt is the verified acks title, else the URL-slug title — the gold's BLL146 alt IS the iStock title); the image-mode templates carry no loading=lazy and the r318 lazy_free_hosts post-pass strips any the rider adds inside dragAndDrop (constraint 83 — the verifier proves 0). Tried ONLY where the r69 text form returned null (it bails on any URL) — the working half is unchanged by construction. header_row_skip: a first row with no URL in either cell is a column-label / instruction row ('Image | Sentence', '**Kupu** |', '| Correct answer - can we jumble them up though please', '| [correct answers]') — dropped; its red instruction rides along as the standard red Writers Note after the widget (bundle.instructions, the r214 class). image_tag_pattern: a red run in the IMAGE cell matching it is the writer's own [image] tag; any other red there ('Arrow added to image', 'Please crop a little so …') is a developer asset note — surfaced the same way, the build proceeds. NEVER HALF-BUILDS (null → the hand-off box as today): a second table, an extraType, a media item harvested out of the table, a ragged row, a row without exactly one image cell + one text cell, the image column changing sides, ANY red run in the TEXT cell (an answer word inside a sentence = a FIB shape — BLL226 / BLL232 / BLL243 / BLL215 / BLL231; `[correct]` — BLL253 / 254 / 256; a red-bracketed audio-word — BLL272 / 273 / 274 / 276, r342's shape; `[Body]` — CEDK102 / SSOG105), an empty label, a URL in the text cell, a repeated label (an ambiguous match), prose riding along with the image, fewer than min_rows rows. Measured on the r349 corpus (`_r350_ddcolumn.json`, every dragAndDrop bundle's table): 21 sites / 20 pages / 20 modules (Standard 14, Fundamentals 6; the image COLUMN-SORT shape is 13 clean — under the floor, recorded). The KB's optional autoCheck / noShuffle / noBG modifiers are the developer's editorial choice (no writer signal) — not emitted. The gold's own substitutions (BLL112 / ENFUN04 build a noBG column form; BLL146 is the exact KB form) are A1 — the writer's tag is the target. Verifier: reference/tests/_verify_dragdrop.cjs (protected, defect 0). Env DDIMAGES_OFF reverts the whole form (DRAGDROP_OFF still reverts the type)."
\t\t\t},
\t\t\t"note": "ROUND 69 (Chris). dragAndDrop NARROW N:N TEXT-MATCHING form'''
    s = s.replace(A, BLOCK, 1)
    atomic(P, s, json_ok); print("Emit_Templates.json: dragAndDrop.button_row + .images inserted")
else:
    print("Emit_Templates.json: already spliced")

# ------------------------------------------------------------------ (2) InteractiveBuilder.js
P = os.path.join(PF, "app", "js", "InteractiveBuilder.js"); s = rd(P)
assert "\r\n" not in s, "CRLF in InteractiveBuilder.js?!"
if "#dragAndDropImages" not in s:
    # (a) dispatch
    A1 = '\t\t\t\t\thtml = this.#dragAndDrop({ bundle, tpl, renderInline });\n'
    assert s.count(A1) == 1, "dispatch anchor"
    s = s.replace(A1, '\t\t\t\t\t// ROUND 350 — the image-pair form runs ONLY where the r69 text form declined (the r276 order).\n'
                      '\t\t\t\t\thtml = this.#dragAndDrop({ bundle, tpl, renderInline }) ?? this.#dragAndDropImages({ bundle, tpl, renderInline, run });\n', 1)
    # (b) the r69 close goes through #ddClose
    A2 = ('\t\tfor (let i = 0; i < answers.length; i++) out.push(Utils.FillTemplate(tpl.drag, { n: i + 1, answer: inline(answers[i]) }));\n'
          '\t\tout.push(tpl.close);\n'
          '\t\treturn out.join("\\n");\n'
          '\t}\n')
    assert s.count(A2) == 1, "r69 close anchor"
    NEW = ('\t\tfor (let i = 0; i < answers.length; i++) out.push(Utils.FillTemplate(tpl.drag, { n: i + 1, answer: inline(answers[i]) }));\n'
           '\t\tout.push(...this.#ddClose(tpl));   // ROUND 350 — the KB button row (button_row; DDBUTTONS_OFF = the r69 close)\n'
           '\t\treturn out.join("\\n");\n'
           '\t}\n'
           '\n'
           '\t/**\n'
           '\t * ROUND 350 (Chris\'s D10-3 — the dragAndDrop build kickoff, shape 1; the autonomous loop\'s session-14 Round 1).\n'
           '\t * The KB 03B button row on EVERY built standard dragAndDrop — "Reset / Undo hidden / Check answers hidden", 03B\'s\n'
           '\t * own form (the gold ships it on 473 of its 517 standard D&Ds = 0.92; levels 1 and 3 agree). The r69 text form never\n'
           '\t * emitted it. Data interactive_builders.dragAndDrop.button_row {enabled, env DDBUTTONS_OFF, close_inner, html,\n'
           '\t * close_outer}; OFF → the r69 `close` string byte-for-byte.\n'
           '\t */\n'
           '\tstatic #ddClose(tpl) {\n'
           '\t\tconst br = tpl?.button_row;\n'
           '\t\tconst off = typeof process !== "undefined" && process.env && br?.env && process.env[br.env];\n'
           '\t\tif (!br || br.enabled === false || off) return [tpl.close];\n'
           '\t\treturn [br.close_inner, br.html, br.close_outer ?? "</div>"];\n'
           '\t}\n'
           '\n'
           '\t/**\n'
           '\t * ROUND 350 — dragAndDrop IMAGE-PAIR form → the KB 03B "Standard Layout — With images" (Chris\'s D10-3, shape 1 of the\n'
           '\t * dragAndDrop kickoff). The writer\'s table pairs an IMAGE with a WORD / sentence on every row — `image | word` (BLL112 /\n'
           '\t * BLL122 / BLL161 …) or `word | image` (BLL146 / BLL130 / CEDO105) — and the KB\'s form is fixed whichever way round the\n'
           '\t * writer typed it: the TEXT is the fixed question side (`col-7 questionContainer`, one `.question` per row) and the\n'
           '\t * IMAGES are the draggable items (`col-5 ddContainer`, a `.drop` + a `.drag` per row, option = the 1-based row index =\n'
           '\t * the answer key), because "images in the questionContainer stretch vertically and make the interactive unusably\n'
           '\t * tall" (03B). Tried ONLY where the r69 text form returned null (the r276 order — the working half is unchanged by\n'
           '\t * construction). Image filename: an iStock id → `iStock-{id}.jpg`, any other host → the r278 URL-slug placeholder\n'
           '\t * (#accImageFilename); rendered in the run\'s image mode through the r240 FinishImg rider with the URL passed (alt =\n'
           '\t * the verified acks title, else the URL-slug title — the gold\'s BLL146 alt IS the iStock title); no loading="lazy"\n'
           '\t * survives — the templates carry none and the r318 lazy_free_hosts post-pass strips any the rider adds (c83).\n'
           '\t * NEVER HALF-BUILDS (null → the hand-off box as today): a second table, an extraType, a media item harvested out of\n'
           '\t * the table, a ragged row, a row without exactly one image cell + one text cell, the image column changing sides,\n'
           '\t * a red run in the TEXT cell (an answer word inside a sentence = a FIB shape; `[correct]`; a red-bracketed audio-word;\n'
           '\t * `[Body]` — different shapes), an empty or duplicate label, a URL in the text cell, prose riding along with the\n'
           '\t * image, fewer than min_rows rows. A first row with no URL in either cell is a HEADER / column-label row ("Image |\n'
           '\t * Sentence", "**Kupu** |", "| Correct answer - can we jumble them up though please") — dropped; its red instruction\n'
           '\t * rides along as the standard red Writers Note after the widget (bundle.instructions, the r214 class). A red run in\n'
           '\t * the IMAGE cell that is the writer\'s own [image] tag is the tag; any other red there ("Arrow added to image",\n'
           '\t * "Please crop a little") is a developer asset note — surfaced the same way, the build proceeds.\n'
           '\t * Data interactive_builders.dragAndDrop.images; env DDIMAGES_OFF (DRAGDROP_OFF still reverts the whole type).\n'
           '\t *\n'
           '\t * @param {object} args\n'
           '\t * @param {object} args.bundle - the captured interactive (opener/member items — see file header)\n'
           '\t * @param {object} args.tpl - this widget\'s editable markup templates (Emit_Templates.json)\n'
           '\t * @param {function} [args.renderInline] - inline-markup renderer (bold/italic/links); identity if omitted\n'
           '\t * @param {object} [args.run] - run context (run.imageMode is "P" or "D")\n'
           '\t * @returns {string|null} the built dragAndDrop HTML, or null to keep the hand-off box\n'
           '\t */\n'
           '\tstatic #dragAndDropImages({ bundle, tpl, renderInline, run }) {\n'
           '\t\tconst cfg = tpl?.images;\n'
           '\t\tif (!cfg || cfg.enabled === false) return null;\n'
           '\t\tif (typeof process !== "undefined" && process.env && process.env.DRAGDROP_OFF) return null;\n'
           '\t\tif (typeof process !== "undefined" && process.env && cfg.env && process.env[cfg.env]) return null;\n'
           '\t\tif (bundle?.extraTypes && bundle.extraTypes.length) return null;\n'
           '\t\tif ((bundle?.media ?? []).length) return null;                        // an image harvested OUT of the table → not the pair table\n'
           '\t\tconst tables = bundle?.tables ?? [];\n'
           '\t\tif (tables.length !== 1) return null;\n'
           '\t\tconst srcRows = tables[0].rows ?? [];\n'
           '\t\tif (!srcRows.length || !srcRows.every((r) => Array.isArray(r) && r.length === 2)) return null;   // a ragged table → not this shape\n'
           '\t\tlet rows = srcRows;\n'
           '\t\tconst notes = [];\n'
           '\t\tconst tagRe = new RegExp(cfg.image_tag_pattern ?? "^\\\\[\\\\s*(?:insert\\\\s+)?image[^\\\\]]*\\\\]$", "i");\n'
           '\t\t// the header / column-label row: a FIRST row carrying no URL in either cell\n'
           '\t\tif (cfg.header_row_skip !== false && !this.#cellMediaUrl(rows[0][0]) && !this.#cellMediaUrl(rows[0][1])) {\n'
           '\t\t\tfor (const c of rows[0]) if (this.#hasRedText(c)) { const t = this.#cellText(c); if (t) notes.push(t); }\n'
           '\t\t\trows = rows.slice(1);\n'
           '\t\t}\n'
           '\t\tif (rows.length < (tpl.min_rows ?? 2)) return null;\n'
           '\t\tconst inline = renderInline ?? ((s) => s);\n'
           '\t\tlet imgIdx = null;\n'
           '\t\tconst items = [];\n'
           '\t\tfor (const r of rows) {\n'
           '\t\t\tconst u0 = this.#cellMediaUrl(r[0]), u1 = this.#cellMediaUrl(r[1]);\n'
           '\t\t\tlet idx;\n'
           '\t\t\tif (u0 && !u1) idx = 0; else if (u1 && !u0) idx = 1; else return null;   // both / neither → not image | text\n'
           '\t\t\tif (imgIdx === null) imgIdx = idx; else if (imgIdx !== idx) return null;   // the image column must not change sides\n'
           '\t\t\tconst imgCell = String(r[idx] ?? ""), txtCell = String(r[1 - idx] ?? "");\n'
           '\t\t\tif (this.#hasRedText(txtCell)) return null;                              // a red run in the TEXT cell = a different shape\n'
           '\t\t\tconst label = this.#cellText(txtCell).trim();\n'
           '\t\t\tif (!label || /https?:\\/\\//.test(label)) return null;\n'
           '\t\t\tconst url = idx === 0 ? u0 : u1;\n'
           '\t\t\t// the image cell: its own [image] tag may be red; any OTHER red run is a developer asset note (rides along)\n'
           '\t\t\tconst reds = [...imgCell.matchAll(/\\[RED TEXT\\]([\\s\\S]*?)\\[\\/RED TEXT\\]/g)]\n'
           '\t\t\t\t.map((m) => m[1].replace(/\\u{1f534}/gu, "").trim()).filter(Boolean);\n'
           '\t\t\tfor (const x of reds) if (!tagRe.test(x)) notes.push(x);\n'
           '\t\t\tconst residual = this.#cellText(imgCell).replace(/\\[[^\\]]*\\]/g, "").replace(/https?:\\/\\/\\S+/g, "")\n'
           '\t\t\t\t.replace(/[/|\\u2013\\u2014-]/g, " ").trim();\n'
           '\t\t\tif (residual) return null;                                               // prose rode along with the image → too rich\n'
           '\t\t\tconst filename = this.#accImageFilename(url, cfg, cfg);\n'
           '\t\t\tif (!filename) return null;\n'
           '\t\t\titems.push({ label, url, filename });\n'
           '\t\t}\n'
           '\t\tif (new Set(items.map((i) => i.label.toLowerCase())).size !== items.length) return null;   // a repeated label = an ambiguous match\n'
           '\t\tconst out = [cfg.open];\n'
           '\t\tfor (const it of items) out.push(Utils.FillTemplate(tpl.question, { label: inline(it.label) }));\n'
           '\t\tout.push(cfg.mid);\n'
           '\t\tfor (let i = 0; i < items.length; i++) out.push(Utils.FillTemplate(tpl.drop, { n: i + 1 }));\n'
           '\t\tout.push(tpl.drag_open);\n'
           '\t\tfor (let i = 0; i < items.length; i++) out.push(Utils.FillTemplate(cfg.drag, { n: i + 1, image: this.#ddImage(items[i], cfg, run) }));\n'
           '\t\tout.push(...this.#ddClose(tpl));\n'
           '\t\tif (notes.length) {\n'
           '\t\t\tconst seen = new Set(bundle.instructions ?? []);\n'
           '\t\t\tbundle.instructions = [...(bundle.instructions ?? [])];\n'
           '\t\t\tfor (const n of notes) if (!seen.has(n)) { bundle.instructions.push(n); seen.add(n); }\n'
           '\t\t}\n'
           '\t\treturn out.join("\\n");\n'
           '\t}\n'
           '\n'
           '\t/**\n'
           '\t * ROUND 350 — a drag item\'s image in the run\'s image mode: the #assetImage form with the URL passed through, so the\n'
           '\t * r240 FinishImg rider takes the alt from the verified acks map else the URL slug (the gold\'s form), and with the\n'
           '\t * images form\'s own templates (margB0, no loading="lazy" — 03B / c83).\n'
           '\t */\n'
           '\tstatic #ddImage(item, cfg, run) {\n'
           '\t\tconst wcfg = DataService.Data.EmitTemplates.elements?.image_attrs;\n'
           '\t\tconst rider = wcfg && wcfg.widget_internal !== false\n'
           '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env.WIDGETIMG_OFF);\n'
           '\t\tconst istockId = String(item.filename).match(/iStock-(\\d+)/i)?.[1] ?? null;\n'
           '\t\tconst fin = rider ? ((h) => MediaBuilder.FinishImg(h, item.url, istockId, run)) : ((h) => h);\n'
           '\t\tif (run?.imageMode === "P") {\n'
           '\t\t\tconst label = String(item.filename).replace(/\\.[a-z0-9]+$/i, "");\n'
           '\t\t\treturn fin(Utils.FillTemplate(cfg.image_mode_P, { label }))\n'
           '\t\t\t\t+ fin(Utils.FillTemplate(cfg.image_mode_P_comment, { filename: item.filename }));\n'
           '\t\t}\n'
           '\t\treturn fin(Utils.FillTemplate(cfg.image_mode_D, { filename: item.filename }));\n'
           '\t}\n')
    s = s.replace(A2, NEW, 1)
    atomic(P, s, js_ok); print("InteractiveBuilder.js: dispatch + #ddClose + #dragAndDropImages + #ddImage spliced")
else:
    print("InteractiveBuilder.js: already spliced")
