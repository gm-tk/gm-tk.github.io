"""ROUND 316 splice (loop Round 3) — the lesson page's own bilingual title pair (KB constraint 79).
Anchored, unique-match edits in bytes mode (LF files, tabs preserved). Idempotent (prefix test)."""
ROOT = r"C:/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/"
SB = ROOT + "app/js/SkeletonBuilder.js"
ET = ROOT + "data/Emit_Templates.json"

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

# ---------------------------------------------------------------- data block (header, before lesson_title_h1)
DATA_OLD = '\t\t"lesson_title_h1": {\n\t\t\t"enabled": true,\n'
DATA_NEW = ('\t\t"lesson_bilingual_pair": {\n'
 '\t\t\t"enabled": true,\n'
 '\t\t\t"env": "LESSONPAIR_OFF",\n'
 '\t\t\t"separators": ["|"],\n'
 '\t\t\t"strip_module_code": true,\n'
 '\t\t\t"reo_first_when_body_class": "reoTranslate",\n'
 '\t\t\t"reo_detect": "macron",\n'
 '\t\t\t"reo_fallback": "second",\n'
 '\t\t\t"_round316_note": "ROUND 316 (the autonomous loop\'s Round 3, 2026-09-15 \\u2014 KB constraint 79: \'a second <h1><span> appears only where the writer gave THAT lesson its own bilingual name, and is then the LESSON\'s English + Te Reo pair, split by the same TITLE BAR parsing rule\'; 01A \'YEARS 9-10 and NCEA lesson pages\'; 07D MTK skeleton rule 7 \'Titles in <h1><span> \\u2014 M\\u0101ori first, English second\'). A lesson page whose OWN title (page.pageTitle \\u2014 the [LESSON n] / [H1] / [H2] source) is a pipe-joined bilingual pair used to ship ONE <h1><span> with the pipe inside, and the module code in front where the writer typed it (\'TRR102 The vowels: Aa | Ng\\u0101 Oropuare: Aa\'). MEASURED (outputs/_measure_r316_lessonpair.py, every Claude lesson page through the gate\'s pairing): 40 paired pipe pages / 16 modules (TRR 26, MXFL101 6, PNR 1, ANZH 2, HIS/MXDB/TEDC/XDLS/XGF 1 each) \\u2014 the gold ships TWO spans on 40/40; the reoTranslate modules (TRR, PNR) put Te Reo FIRST on 27/27 although the writer types English | Te Reo; the Standard-template modules read English-first 4 : as-written 2 (n = 6, below the solidify floor \\u2014 payload order kept, the overview splitter\'s own rule); gold lesson pages never carry the module code (Claude 30 did). THE RULE: strip a leading module code (+ dash/colon), split on the first separator, trim both halves; in a module whose resolved body class matches reo_first_when_body_class the Te Reo half (the macron-bearing half; when neither or both carry a macron, the reo_fallback half) goes first, otherwise payload order; both spans are emitted, exempt from the registry h1_count cap, and the module-level Te Reo title is NOT pushed beside them (constraint 79). Named residue: MXFL101 / TEDC402 / PNR101 gold repeat the MODULE pair on lesson pages (the c79 human anti-pattern \\u2014 the KB outranks; the span COUNT now matches); TRR112/113 gold rewords the English half (editorial). Env toggle LESSONPAIR_OFF reverts to the single joined span."\n'
 '\t\t},\n'
 + DATA_OLD)

# ---------------------------------------------------------------- SkeletonBuilder (a) the lesson-title push
SB_A_OLD = ('\t\t\ttitles.push(page.pageTitle || run.englishTitle || content.titleBar.english || "");\n')
SB_A_NEW = ('\t\t\t// ROUND 316 (loop Round 3 \u2014 KB constraint 79). A lesson whose OWN title is a\n'
 '\t\t\t// pipe-joined bilingual pair ("One | Tahi", "TRR102 The vowels: Aa | Ng\u0101\n'
 '\t\t\t// Oropuare: Aa") ships the LESSON\'s English + Te Reo pair as two h1 spans \u2014\n'
 '\t\t\t// the gold\'s form on 40/40 measured pages \u2014 with the module code stripped and,\n'
 '\t\t\t// in a reoTranslate module, Te Reo first (07D MTK rule 7). See #lessonPair.\n'
 '\t\t\t// Data header.lesson_bilingual_pair; env LESSONPAIR_OFF.\n'
 '\t\t\tconst pairTitles = SkeletonBuilder.#lessonPair(page.pageTitle || "", run, rules, tpl.header.lesson_bilingual_pair);\n'
 '\t\t\tif (pairTitles) titles.push(...pairTitles);\n'
 '\t\t\telse titles.push(page.pageTitle || run.englishTitle || content.titleBar.english || "");\n')

# ---------------------------------------------------------------- SkeletonBuilder (b) the cap + the module Te Reo push
SB_B_OLD = ('\t\t\tif (run.teReoTitle && wanted > 1 && !lthSuppress && !distinctSuppress) titles.push(run.teReoTitle);\n'
 '\t\t\twhile (titles.length > wanted) titles.pop();\n')
SB_B_NEW = ('\t\t\t// ROUND 316: a lesson that carries its OWN pair never takes the module\'s Te Reo\n'
 '\t\t\t// title beside it, and the pair is exempt from the registry h1_count cap.\n'
 '\t\t\tif (!pairTitles && run.teReoTitle && wanted > 1 && !lthSuppress && !distinctSuppress) titles.push(run.teReoTitle);\n'
 '\t\t\tconst cap = pairTitles ? Math.max(wanted, pairTitles.length) : wanted;\n'
 '\t\t\twhile (titles.length > cap) titles.pop();\n')

# ---------------------------------------------------------------- SkeletonBuilder (c) the static method, before #buildHeader's doc block
SB_C_OLD = ('\t/**\n'
 '\t * Builds the #header element: the module-code "chip", the title <h1>\n')
SB_C_NEW = ('\t/**\n'
 '\t * ROUND 316 (loop Round 3 \u2014 KB constraint 79, the lesson\'s own bilingual pair).\n'
 '\t * Splits a lesson\'s OWN title into [first, second] when it carries one of the\n'
 '\t * data separators, or returns null (no separator / feature off / an empty half).\n'
 '\t * A leading module-code token (+ an optional dash or colon) is stripped first \u2014\n'
 '\t * the writer\'s "TRR102 \u2013The vowel blend: ao | Te oropuare p\u016brua: ao" \u2014 because\n'
 '\t * gold lesson pages never carry the code (0 of 1371). ORDER: in a module whose\n'
 '\t * resolved body class matches reo_first_when_body_class (the reoTranslate\n'
 '\t * M\u0101ori-medium modules) the Te Reo half goes first \u2014 the macron-bearing half,\n'
 '\t * or the reo_fallback half when the macron cannot decide (PNR101 "Number 1 |\n'
 '\t * Te tau 1"); everywhere else the halves keep the writer\'s order, the same rule\n'
 '\t * the overview [TITLE BAR] splitter follows. Pure; never touches the overview.\n'
 '\t */\n'
 '\tstatic #lessonPair(title, run, rules, cfg) {\n'
 '\t\tif (!cfg || cfg.enabled === false || !title) return null;\n'
 '\t\tif (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "LESSONPAIR_OFF"]) return null;\n'
 '\t\tconst seps = Array.isArray(cfg.separators) && cfg.separators.length ? cfg.separators : ["|"];\n'
 '\t\tconst sep = seps.find((s) => title.includes(s));\n'
 '\t\tif (!sep) return null;\n'
 '\t\tlet t = String(title);\n'
 '\t\tif (cfg.strip_module_code !== false && run.moduleCode) {\n'
 '\t\t\tconst esc = String(run.moduleCode).replace(/[.*+?^${}()|[\\]\\\\]/g, "\\\\$&");\n'
 '\t\t\tt = t.replace(new RegExp("^\\\\s*" + esc + "\\\\s*[\\\\-\\u2013\\u2014:]?\\\\s*", "i"), "");\n'
 '\t\t}\n'
 '\t\tconst i = t.indexOf(sep);\n'
 '\t\tif (i < 0) return null;\n'
 '\t\tconst clean = (s) => s.replace(/^[\\s\\-\\u2013\\u2014:|]+|[\\s\\-\\u2013\\u2014:|]+$/g, "").replace(/\\s+/g, " ").trim();\n'
 '\t\tconst a = clean(t.slice(0, i)), b = clean(t.slice(i + sep.length));\n'
 '\t\tif (!a || !b) return null;\n'
 '\t\tconst reoCls = cfg.reo_first_when_body_class;\n'
 '\t\tconst reoMode = !!reoCls && new RegExp(reoCls, "i").test(String(rules?.body_class || ""));\n'
 '\t\tif (!reoMode) return [a, b];\n'
 '\t\tconst M = /[\\u0101\\u0113\\u012b\\u014d\\u016b\\u0100\\u0112\\u012a\\u014c\\u016a]/;   // \u0101\u0113\u012b\u014d\u016b\n'
 '\t\tconst ma = M.test(a), mb = M.test(b);\n'
 '\t\tif (mb && !ma) return [b, a];\n'
 '\t\tif (ma && !mb) return [a, b];\n'
 '\t\treturn (cfg.reo_fallback ?? "second") === "second" ? [b, a] : [a, b];\n'
 '\t}\n'
 '\n'
 + SB_C_OLD)

edit(ET, [(DATA_OLD, DATA_NEW)])
edit(SB, [(SB_A_OLD, SB_A_NEW), (SB_B_OLD, SB_B_NEW), (SB_C_OLD, SB_C_NEW)])
print("done")
