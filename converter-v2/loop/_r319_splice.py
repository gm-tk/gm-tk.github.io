"""ROUND 319 splice (loop Round 6) — KB constraint 89: `learningSupport` on <html> for every X-prefixed module code.
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

# ---------------------------------------------------------------- data block (skeleton, after html_open)
DATA_OLD = '\t\t"html_open": "<html lang=\\"en\\"{levelAttr} template=\\"{templateAttr}\\" class=\\"notranslate\\" translate=\\"no\\">",\n'
DATA_NEW = (DATA_OLD +
 '\t\t"html_class_cohorts": {\n'
 '\t\t\t"enabled": true,\n'
 '\t\t\t"env": "HTMLCOHORT_OFF",\n'
 '\t\t\t"rules": [\n'
 '\t\t\t\t{ "code_prefix": "X", "add_class": "learningSupport", "kb": "constraint 89 / CL-0089" }\n'
 '\t\t\t],\n'
 '\t\t\t"_round319_note": "ROUND 319 (the autonomous loop\'s Round 6, 2026-09-15 \\u2014 KB constraint 89 / CL-0089, a locked admin decision): a module whose CODE begins with X is a learning-support module and ships `learningSupport` appended to the <html> class list on every page (class=\\"notranslate learningSupport\\"), never replacing notranslate and never altering template= (constraint 21); a non-X module never receives it. The test is the code, not the reference files (06_TEMPLATE_RECOGNITION \\u00a74.4). A CSS hook (a larger font from the stylesheet) \\u2014 the converter writes no font CSS. Each rule here is a code-prefix cohort; SkeletonBuilder appends add_class to the filled html_open tag\'s class list for every rule whose prefix matches run.moduleCode. MEASURED: Claude 0 of 228 X pages / 35 modules carried it; the gold carries it on 72 of 250 X pages and 0 non-X pages \\u2014 the KB outranks (the gold predates the rule). Gate-neutral (the <html> tag is outside the skeleton). Env toggle HTMLCOHORT_OFF reverts to the round-318 form byte-for-byte."\n'
 '\t\t},\n')

# ---------------------------------------------------------------- SkeletonBuilder: the html_open fill
SB_OLD = ('\t\t\tUtils.FillTemplate(tpl.skeleton.html_open, { levelAttr, templateAttr }),\n')
SB_NEW = ('\t\t\tSkeletonBuilder.#cohortHtmlClass(Utils.FillTemplate(tpl.skeleton.html_open, { levelAttr, templateAttr }), run, tpl),\n')

SB_M_OLD = ('\t/**\n'
 '\t * ROUND 316 (loop Round 3 \u2014 KB constraint 79, the lesson\'s own bilingual pair).\n')
SB_M_NEW = ('\t/**\n'
 '\t * ROUND 319 (loop Round 6 \u2014 KB constraint 89): a code-prefix COHORT adds a class to\n'
 '\t * the <html> tag \u2014 the X-prefixed learning-support modules ship `learningSupport`\n'
 '\t * appended to the existing class list on every page (a CSS hook for the larger\n'
 '\t * font; no font CSS is ever written). Data skeleton.html_class_cohorts (a list of\n'
 '\t * { code_prefix, add_class } rules); env HTMLCOHORT_OFF. Returns the tag unchanged\n'
 '\t * when off, when no rule matches, or when the class is already present.\n'
 '\t */\n'
 '\tstatic #cohortHtmlClass(htmlOpen, run, tpl) {\n'
 '\t\tconst cfg = tpl.skeleton?.html_class_cohorts;\n'
 '\t\tif (!cfg || cfg.enabled === false || !Array.isArray(cfg.rules)) return htmlOpen;\n'
 '\t\tif (typeof process !== "undefined" && process.env && process.env[cfg.env ?? "HTMLCOHORT_OFF"]) return htmlOpen;\n'
 '\t\tconst code = String(run?.moduleCode || "");\n'
 '\t\tlet tag = htmlOpen;\n'
 '\t\tfor (const r of cfg.rules) {\n'
 '\t\t\tif (!r || !r.code_prefix || !r.add_class || !code.startsWith(r.code_prefix)) continue;\n'
 '\t\t\tconst m = /\\bclass="([^"]*)"/.exec(tag);\n'
 '\t\t\tif (!m) { tag = tag.replace(/>$/, ` class="${r.add_class}">`); continue; }\n'
 '\t\t\tif (m[1].split(/\\s+/).includes(r.add_class)) continue;\n'
 '\t\t\ttag = tag.replace(m[0], `class="${(m[1] + " " + r.add_class).trim()}"`);\n'
 '\t\t}\n'
 '\t\treturn tag;\n'
 '\t}\n'
 '\n'
 + SB_M_OLD)

edit(ET, [(DATA_OLD, DATA_NEW)])
edit(SB, [(SB_OLD, SB_NEW), (SB_M_OLD, SB_M_NEW)])
print("done")
