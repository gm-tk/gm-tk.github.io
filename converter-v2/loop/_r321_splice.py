"""ROUND 321 splice (loop Round 8 — Chris's decision 2): the MTK / Te Reo Rangatira title source.
Anchored, unique-match edits in bytes mode (LF files, tabs preserved). Idempotent (prefix test).
Five seams under ONE data block (header.mtk_titles) + one Input_Doc_Rules capture:
  A  DocxExtractor   — capture the Module Code cell's remainder as metadata.moduleCodeTitle
  B  PageAssembler   — module-title fallback: the [H1]/[Title Bar] repetition with a pipe, else the cell remainder
  C  SkeletonBuilder — overview: Maori-looking title first in reoTranslate modules
  D  SkeletonBuilder — lesson without an own title: both module titles (Maori first), exempt from the h1_count cap
  E  PageSplitter    — the first-heading harvest accepts only [H1] in reoTranslate modules"""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
DX = ROOT + "app/js/DocxExtractor.js"; PA = ROOT + "app/js/PageAssembler.js"; SB = ROOT + "app/js/SkeletonBuilder.js"; PS = ROOT + "app/js/PageSplitter.js"
ET = ROOT + "data/Emit_Templates.json"; IDR = ROOT + "data/Input_Doc_Rules.json"

def edit(path, pairs):
    b = open(path, "rb").read()
    for old, new in pairs:
        o = old.encode("utf-8"); n = new.encode("utf-8")
        ins = n[:-len(o)] if n.endswith(o) else (n[len(o):] if n.startswith(o) else n)
        if b.count(ins) == 1 and (n.endswith(o) or n.startswith(o) or b.count(o) == 0):
            print("already applied:", path.split("/")[-1], old[:40].strip()); continue
        cnt = b.count(o)
        assert cnt == 1, f"{path}: anchor count {cnt} != 1 for anchor starting {old[:60]!r}"
        b = b.replace(o, n)
    open(path, "wb").write(b)
    print("edited", path.split("/")[-1], len(pairs), "edit(s)")

MAORI_RE_JS = '/[\\u0101\\u0113\\u012b\\u014d\\u016b\\u0100\\u0112\\u012a\\u014c\\u016a]/'   # āēīōū (JS source text)

# ---------------------------------------------------------------- data: header.mtk_titles (after header.open/close)
ET_OLD = '\t"header": {\n\t\t"open": "<div id=\\"header\\">",\n\t\t"close": "</div>",\n'
ET_NEW = (ET_OLD +
 '\t\t"mtk_titles": {\n'
 '\t\t\t"enabled": true,\n'
 '\t\t\t"env": "MTKTITLES_OFF",\n'
 '\t\t\t"body_class": "reoTranslate",\n'
 '\t\t\t"repetition_tags": ["h1", "title bar"],\n'
 '\t\t\t"harvest_heading_tags": ["h1"],\n'
 '\t\t\t"_round321_note": "ROUND 321 (the autonomous loop\'s Round 8, 2026-09-15 \\u2014 Chris\'s decision 2: the MTK / Te Reo Rangatira title source; KB 07A \'Sections to EXTRACT\' (the metadata table \\u2192 module code + title; the [TITLE BAR] row; the per-page [H1] TRR1XX \\u2026 | \\u2026 repetition), 07C/07D rule 7 (titles M\\u0101ori first, English second on every page; a lesson page carries its own title else the module titles), constraint 79). The TRR1xx docx leaves its [TITLE BAR] rows EMPTY and has no Module Name row: the module title rides in the Module Code cell (\'TRR108: Ng\\u0101 Orokati Tuarua \\u2013 Final Consonants\', \'TRR102 \\u2013 Ng\\u0101 Oropuare Aa\') and the English half, where the writer gave one, in the per-page \'[H1] TRR102 The vowels: Aa | Ng\\u0101 Oropuare: Aa\' repetition. Claude shipped NO title on 13 TRR overview pages, a stray body heading (Finished!, Karakia Whakakapi) as 9 lesson titles \\u2014 the first-heading harvest has no [Activity] tag to stop at on an MTK page \\u2014 and a single title where the gold has the pair on PNR102/104 lessons (the registry h1_count cap). THE RULE, scoped to modules whose resolved body class matches body_class: (A) DocxExtractor keeps the Module Code cell\'s remainder after the code token as metadata.moduleCodeTitle; (B) when the [TITLE BAR] and Module Name gave no title, PageAssembler takes the first repetition_tags item anywhere in the item stream whose text carries a pipe (code stripped, halves in payload order), else the cell remainder (pipe \\u2192 pair; ONE spaced dash with a macron on exactly one side \\u2192 pair; else one title); (C) the overview emits the M\\u0101ori-looking title (macron, or the M\\u0101ori alphabet) first; (D) a lesson page with no own title emits BOTH module titles, M\\u0101ori first, exempt from the h1_count cap; (E) the page-title harvest accepts only harvest_heading_tags. Gold: every TRR overview carries the pair M\\u0101ori-first; lessons repeat the module pair where the writer gave no lesson title. Env toggle MTKTITLES_OFF reverts all five to the round-320 form byte-for-byte."\n'
 '\t\t},\n')

# ---------------------------------------------------------------- data: Input_Doc_Rules title_in_code_cell
IDR_OLD = '\t\t"table_row_fields": [\n\t\t\t"moduleName"\n\t\t],\n'
IDR_NEW = (IDR_OLD +
 '\t\t"title_in_code_cell": {\n'
 '\t\t\t"labels": ["module code"],\n'
 '\t\t\t"field": "moduleCodeTitle",\n'
 '\t\t\t"_round321_note": "ROUND 321: the TRR1xx MTK front-matter table has no Module Name row; the Module Code cell reads \'TRR108: Ng\\u0101 Orokati Tuarua \\u2013 Final Consonants\'. The text after the code token (and an optional colon/dash) is kept as metadata.moduleCodeTitle for PageAssembler\'s MTK title fallback (header.mtk_titles). The moduleCode field itself is unchanged. Env MTKTITLES_OFF."\n'
 '\t\t},\n')

# ---------------------------------------------------------------- A: DocxExtractor
DX_OLD = ('\t\t\t\t\tconst value = clean(row[1]);\n'
 '\t\t\t\t\tif (value && !out[hit[1]]) out[hit[1]] = value;\n'
 '\t\t\t\t}\n'
 '\t\t\t}\n'
 '\t\t}\n'
 '\t\treturn out;\n')
DX_NEW = ('\t\t\t\t\tconst value = clean(row[1]);\n'
 '\t\t\t\t\tif (value && !out[hit[1]]) out[hit[1]] = value;\n'
 '\t\t\t\t}\n'
 '\t\t\t}\n'
 '\t\t}\n'
 '\t\t// ROUND 321 (the MTK title source): the TRR1xx table has NO Module Name row \u2014 the\n'
 '\t\t// Module Code cell carries the title after the code ("TRR108: Ng\u0101 Orokati Tuarua \u2013\n'
 '\t\t// Final Consonants"). Keep that remainder as metadata.moduleCodeTitle for the\n'
 '\t\t// PageAssembler fallback. Data front_matter_metadata.title_in_code_cell; env MTKTITLES_OFF.\n'
 '\t\tconst tic = cfg.title_in_code_cell;\n'
 '\t\tif (tic && tic.enabled !== false && Array.isArray(tic.labels)\n'
 '\t\t\t&& !(typeof process !== "undefined" && process.env && process.env.MTKTITLES_OFF)) {\n'
 '\t\t\tconst clean2 = (s) => String(s ?? "").replace(/\\u{1f534}/gu, "").replace(/\\[\\/?RED TEXT\\]/g, "").replace(/\\*\\*/g, "").trim();\n'
 '\t\t\tconst want = new Set(tic.labels.map((l) => Utils.Fold(l)));\n'
 '\t\t\tfor (const b of blocks) {\n'
 '\t\t\t\tif (b.kind !== "table" || out[tic.field ?? "moduleCodeTitle"]) continue;\n'
 '\t\t\t\tfor (const row of (b.rows ?? [])) {\n'
 '\t\t\t\t\tif (!Array.isArray(row) || row.length < 2 || !want.has(Utils.Fold(clean2(row[0])))) continue;\n'
 '\t\t\t\t\tconst m = /^\\s*[A-Za-z]{2,8}\\d{2,5}[A-Za-z]?\\s*[:\\u2013\\u2014\\-]?\\s*(.+)$/.exec(clean2(row[1]));\n'
 '\t\t\t\t\tif (m && m[1].trim()) { out[tic.field ?? "moduleCodeTitle"] = m[1].trim(); break; }\n'
 '\t\t\t\t}\n'
 '\t\t\t}\n'
 '\t\t}\n'
 '\t\treturn out;\n')

# ---------------------------------------------------------------- B: PageAssembler fallback (before the Course backup)
PA_OLD = ('\t\tconst tb = overviewProduct?.content.titleBar;\n'
 '\t\tconst course = run.metadata?.course;\n')
PA_NEW = ('\t\t// ROUND 321 (loop Round 8 \u2014 the MTK / Te Reo Rangatira title source, Chris\'s\n'
 '\t\t// decision 2). The TRR1xx docx leaves its [TITLE BAR] rows empty and has no Module\n'
 '\t\t// Name row, so both run titles are still empty here. Sources, in order: the first\n'
 '\t\t// [H1] / [Title Bar] item anywhere whose text carries a pipe (the per-page\n'
 '\t\t// "TRR102 The vowels: Aa | Ng\u0101 Oropuare: Aa" repetition, code stripped, halves in\n'
 '\t\t// payload order), else the Module Code cell\'s remainder (metadata.moduleCodeTitle:\n'
 '\t\t// a pipe, or one spaced dash with a macron on exactly one side, splits it). The\n'
 '\t\t// skeleton orders the pair M\u0101ori-first for these modules (header.mtk_titles).\n'
 '\t\t{\n'
 '\t\t\tconst mtk = DataService.Data.EmitTemplates.header?.mtk_titles;\n'
 '\t\t\tconst mtkOn = mtk && mtk.enabled !== false\n'
 '\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[mtk.env ?? "MTKTITLES_OFF"])\n'
 '\t\t\t\t&& new RegExp(mtk.body_class ?? "reoTranslate", "i").test(String(run.resolvedRules?.body_class || ""));\n'
 '\t\t\tif (mtkOn && !run.englishTitle && !run.teReoTitle) {\n'
 '\t\t\t\tconst code = String(run.moduleCode || "");\n'
 '\t\t\t\tconst esc = code.replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");\n'
 '\t\t\t\tconst stripCode = (s) => code ? String(s).replace(new RegExp("^\\\\s*" + esc + "\\\\s*[:\\\\-\\u2013\\u2014]?\\\\s*", "i"), "") : String(s);\n'
 '\t\t\t\tconst tidy = (s) => String(s ?? "").replace(/\\*+/g, "").replace(/^[\\s:\\-\\u2013\\u2014|]+|[\\s:\\-\\u2013\\u2014|]+$/g, "").replace(/\\s+/g, " ").trim();\n'
 '\t\t\t\tlet parts = null, src = "";\n'
 '\t\t\t\tconst tags = new Set(mtk.repetition_tags ?? ["h1", "title bar"]);\n'
 '\t\t\t\touter: for (const p of run.pages) {\n'
 '\t\t\t\t\tfor (const it of (p.items ?? [])) {\n'
 '\t\t\t\t\t\tif (it.type !== "tag" || !tags.has(it.parse?.primary?.tag)) continue;\n'
 '\t\t\t\t\t\tconst txt = tidy(stripCode(tidy(it.blackAfter || "")));\n'
 '\t\t\t\t\t\tif (!txt.includes("|")) continue;\n'
 '\t\t\t\t\t\tconst h = txt.split("|").map(tidy).filter(Boolean);\n'
 '\t\t\t\t\t\tif (h.length >= 2) { parts = h.slice(0, 2); src = `[${it.parse.primary.tag}] repetition on page ${p.lessonLabel}`; break outer; }\n'
 '\t\t\t\t\t}\n'
 '\t\t\t\t}\n'
 '\t\t\t\tconst cell = tidy(run.metadata?.moduleCodeTitle);\n'
 '\t\t\t\tif (!parts && cell) {\n'
 '\t\t\t\t\tconst M = ' + MAORI_RE_JS + ';\n'
 '\t\t\t\t\tif (cell.includes("|")) parts = cell.split("|").map(tidy).filter(Boolean).slice(0, 2);\n'
 '\t\t\t\t\telse {\n'
 '\t\t\t\t\t\tconst d = cell.split(/\\s+[\\u2013\\u2014\\-]\\s+/);\n'
 '\t\t\t\t\t\tparts = (d.length === 2 && (M.test(d[0]) !== M.test(d[1])) && d.every((h) => tidy(h).replace(/[^A-Za-zÀ-ſ]/g, "").length >= 3)) ? d.map(tidy) : [cell];\n'
 '\t\t\t\t\t}\n'
 '\t\t\t\t\tsrc = "the Module Code cell";\n'
 '\t\t\t\t}\n'
 '\t\t\t\tif (parts && parts.length) {\n'
 '\t\t\t\t\trun.englishTitle = parts[0];\n'
 '\t\t\t\t\trun.teReoTitle = parts[1] ?? "";\n'
 '\t\t\t\t\trun.AddNote("info", "PageAssembler",\n'
 '\t\t\t\t\t\t`No [TITLE BAR] / Module Name title \u2014 MTK module title taken from ${src}: "${parts.join(" | ")}" (round 321).`);\n'
 '\t\t\t\t}\n'
 '\t\t\t}\n'
 '\t\t}\n'
 '\t\tconst tb = overviewProduct?.content.titleBar;\n'
 '\t\tconst course = run.metadata?.course;\n')

# ---------------------------------------------------------------- C: SkeletonBuilder overview order
SB_C_OLD = ('\t\t\tif (content.titleBar.teReoLines?.length) titles.push(...content.titleBar.teReoLines);\n'
 '\t\t\telse if (content.titleBar.teReo) titles.push(content.titleBar.teReo);\n')
SB_C_NEW = ('\t\t\tif (content.titleBar.teReoLines?.length) titles.push(...content.titleBar.teReoLines);\n'
 '\t\t\telse if (content.titleBar.teReo) titles.push(content.titleBar.teReo);\n'
 '\t\t\t// ROUND 321 (the MTK title source): in a reoTranslate module the overview shows\n'
 '\t\t\t// the M\u0101ori title first, English second (07C/07D rule 7) \u2014 decided by the text\n'
 '\t\t\t// (a macron, or the M\u0101ori alphabet), not by the slot, because the r212 metadata\n'
 '\t\t\t// fallback files the halves in payload order. Data header.mtk_titles; env MTKTITLES_OFF.\n'
 '\t\t\tif (SkeletonBuilder.#mtkOn(rules, tpl) && titles.length === 2 && SkeletonBuilder.#looksMaori(titles[1]) && !SkeletonBuilder.#looksMaori(titles[0])) titles.reverse();\n')

# ---------------------------------------------------------------- D: SkeletonBuilder lesson fallback pair
SB_D_OLD = ('\t\t\tconst pairTitles = SkeletonBuilder.#lessonPair(page.pageTitle || "", run, rules, tpl.header.lesson_bilingual_pair);\n'
 '\t\t\tif (pairTitles) titles.push(...pairTitles);\n'
 '\t\t\telse titles.push(page.pageTitle || run.englishTitle || content.titleBar.english || "");\n')
SB_D_NEW = ('\t\t\tlet pairTitles = SkeletonBuilder.#lessonPair(page.pageTitle || "", run, rules, tpl.header.lesson_bilingual_pair);\n'
 '\t\t\t// ROUND 321 (the MTK title source): a reoTranslate lesson page with no own title\n'
 '\t\t\t// (none harvested, or one that fold-equals a module title) repeats BOTH module\n'
 '\t\t\t// titles, M\u0101ori first (07D rule 7; the gold on every such TRR/PNR lesson), exempt\n'
 '\t\t\t// from the registry h1_count cap. Data header.mtk_titles; env MTKTITLES_OFF.\n'
 '\t\t\tif (!pairTitles && SkeletonBuilder.#mtkOn(rules, tpl) && run.englishTitle && run.teReoTitle) {\n'
 '\t\t\t\tconst own = Utils.Fold(page.pageTitle || "");\n'
 '\t\t\t\tif (!own || own === Utils.Fold(run.englishTitle) || own === Utils.Fold(run.teReoTitle)) {\n'
 '\t\t\t\t\tconst pair = [run.englishTitle, run.teReoTitle];\n'
 '\t\t\t\t\tif (SkeletonBuilder.#looksMaori(pair[1]) && !SkeletonBuilder.#looksMaori(pair[0])) pair.reverse();\n'
 '\t\t\t\t\tpairTitles = pair;\n'
 '\t\t\t\t}\n'
 '\t\t\t}\n'
 '\t\t\tif (pairTitles) titles.push(...pairTitles);\n'
 '\t\t\telse titles.push(page.pageTitle || run.englishTitle || content.titleBar.english || "");\n')

# ---------------------------------------------------------------- helpers, before #lessonPair's doc block
SB_H_OLD = ('\t/**\n'
 '\t * ROUND 316 (loop Round 3 \u2014 KB constraint 79, the lesson\'s own bilingual pair).\n')
SB_H_NEW = ('\t/** ROUND 321 \u2014 is header.mtk_titles on for this module (a reoTranslate body class)? */\n'
 '\tstatic #mtkOn(rules, tpl) {\n'
 '\t\tconst mtk = tpl.header?.mtk_titles;\n'
 '\t\tif (!mtk || mtk.enabled === false) return false;\n'
 '\t\tif (typeof process !== "undefined" && process.env && process.env[mtk.env ?? "MTKTITLES_OFF"]) return false;\n'
 '\t\treturn new RegExp(mtk.body_class ?? "reoTranslate", "i").test(String(rules?.body_class || ""));\n'
 '\t}\n'
 '\n'
 '\t/** ROUND 321 \u2014 does a title read as te reo M\u0101ori? A macron, or letters only from the\n'
 '\t *  M\u0101ori alphabet (a e i o u h k m n p r t w g) \u2014 the round-153 lone-title guard\'s test. */\n'
 '\tstatic #looksMaori(s) {\n'
 '\t\tconst t = String(s ?? "");\n'
 '\t\tif (' + MAORI_RE_JS + '.test(t)) return true;\n'
 '\t\tconst letters = t.toLowerCase().replace(/[^a-z]/g, "");\n'
 '\t\treturn letters.length > 0 && !/[bcdfjlqsvxyz]/.test(letters);\n'
 '\t}\n'
 '\n'
 + SB_H_OLD)

# ---------------------------------------------------------------- E: PageSplitter harvest
PS_OLD = ('\t\t\t\tif (["h1", "h2", "h3", "h4", "h5", "heading"].includes(pt2)\n'
 '\t\t\t\t\t&& (it2.blackAfter.trim() || it2.parse.remainders.length)) { firstHeading = it2; break; }\n')
PS_NEW = ('\t\t\t\t// ROUND 321 (the MTK title source): a reoTranslate page has no [Activity] tag to\n'
 '\t\t\t\t// stop the harvest, so a body [H3] ("Finished!") became the page title; only\n'
 '\t\t\t\t// the writer\'s [H1] title repetition may name the page there \u2014 else the module\n'
 '\t\t\t\t// titles (SkeletonBuilder). Data header.mtk_titles.harvest_heading_tags; env MTKTITLES_OFF.\n'
 '\t\t\t\tconst _mtk = DataService?.Data?.EmitTemplates?.header?.mtk_titles;\n'
 '\t\t\t\tconst _mtkOn = _mtk && _mtk.enabled !== false && Array.isArray(_mtk.harvest_heading_tags)\n'
 '\t\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_mtk.env ?? "MTKTITLES_OFF"])\n'
 '\t\t\t\t\t&& new RegExp(_mtk.body_class ?? "reoTranslate", "i").test(String(run?.resolvedRules?.body_class || ""));\n'
 '\t\t\t\tconst _hTags = _mtkOn ? _mtk.harvest_heading_tags : ["h1", "h2", "h3", "h4", "h5", "heading"];\n'
 '\t\t\t\tif (_hTags.includes(pt2)\n'
 '\t\t\t\t\t&& (it2.blackAfter.trim() || it2.parse.remainders.length)) { firstHeading = it2; break; }\n')

edit(ET, [(ET_OLD, ET_NEW)])
edit(IDR, [(IDR_OLD, IDR_NEW)])
edit(DX, [(DX_OLD, DX_NEW)])
edit(PA, [(PA_OLD, PA_NEW)])
edit(SB, [(SB_C_OLD, SB_C_NEW), (SB_D_OLD, SB_D_NEW), (SB_H_OLD, SB_H_NEW)])
edit(PS, [(PS_OLD, PS_NEW)])
print("done")
