#!/usr/bin/env python3
"""ROUND 324 — KB c79's `Lesson N` LABEL titles (PageSplitter's title harvest). Anchored, idempotent
engine + data edits (env R324_ROOT overrides the target tree for the reproducibility test).

  (1) data  Emit_Templates.body_region.lesson_title_dedup.lesson_label_titles
  (2) engine PageSplitter harvest: label-only titles replaced by the first real heading; label prefix stripped;
      label-only headings skipped in the scan
  (3) engine PageSplitter: a label-only SUB-page with no heading inherits its parent lesson's title
"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("R324_ROOT") or os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2")
PS = os.path.join(ROOT, "app", "js", "PageSplitter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")
def rd(p):
    with io.open(p, "r", encoding="utf-8", newline="") as f: return f.read()
def wr(p, s):
    with io.open(p, "w", encoding="utf-8", newline="") as f: f.write(s)
def step(src, key, old, new, label):
    if key in src: print(f"  = {label}: already applied"); return src
    n = src.count(old); assert n == 1, f"{label}: anchor count {n} != 1"
    print(f"  + {label}: applied"); return src.replace(old, new, 1)

# ---------------------------------------------------------------- (1) data
et = rd(ET)
D_OLD = '\t\t\t"lesson_name_from_heading": {\n\t\t\t\t"enabled": true,\n'
D_NEW = ('\t\t\t"lesson_label_titles": {\n'
    '\t\t\t\t"_doc": "ROUND 324 (the autonomous loop\'s session-3 Round 11, 2026-09-15 — KB constraint 79 / CL-0069/0076, the `Lesson N` LABEL sub-mechanism). A lesson page whose header title is nothing but a lesson LABEL — \'Lesson One\' / \'Lesson 1\' (the [LESSON] tag\'s own payload), \'Lesson #3 Opening Doors…\' (the existing strip accepted \'Lesson 3\' but not \'Lesson #3\'), \'Lesson One – The Ode\' (a word number), \'Lesson 5 continued\' (a sub-page) — takes the lesson\'s OWN title: the first real heading (a label-only heading is skipped) with the label stripped; a label-prefixed title keeps its own words; a label-only SUB-page (N.M, M > 0) with no heading of its own inherits its parent lesson\'s title (CEDT501 5.1 → \'Speaking up\'). Measured over every paired lesson page (outputs/_measure_r324_lessontitles.py): 44 pages carry a label title where the gold ships the lesson\'s own title (100% of the class; ENGI102/202/203/301, ENGJ301/302/402, ENGC201, ANZH203, CEDT501). The lesson-NUMBER logic (a \'Lesson N\' heading\'s number wins) is untouched; the existing body de-dup then drops the body heading that now equals the title — the gold\'s shape. Env LESSONLABEL_OFF reverts byte-for-byte.",\n'
    '\t\t\t\t"enabled": true,\n'
    '\t\t\t\t"env": "LESSONLABEL_OFF",\n'
    '\t\t\t\t"label_pattern": "^lesson\\\\s*#?\\\\s*(\\\\d+(?:\\\\.\\\\d+)?[a-z]?|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve)\\\\b\\\\s*(continued)?\\\\s*[:.\\\\-\\u2013\\u2014]?\\\\s*(.*)$",\n'
    '\t\t\t\t"strip_existing_title": true,\n'
    '\t\t\t\t"inherit_parent_on_subpage": true\n'
    '\t\t\t},\n' + D_OLD)
et = step(et, '"lesson_label_titles"', D_OLD, D_NEW, "(1) data lesson_title_dedup.lesson_label_titles")
wr(ET, et)

ps = rd(PS)
# ---------------------------------------------------------------- (2) the harvest
E2_OLD = ('\t\t\tlet firstHeading = null;\n'
          '\t\t\tfor (const it2 of p.items) {\n'
          '\t\t\t\tif (it2.type !== "tag") continue;\n'
          '\t\t\t\tconst pt2 = it2.parse.primary?.tag;\n'
          '\t\t\t\tconst ht2 = (it2.blackAfter || it2.parse.remainders.join(" ")).replace(/\\*/g, "").trim();\n')
E2_NEW = ('\t\t\t// ROUND 324 (KB constraint 79 — the `Lesson N` LABEL titles): a title that is nothing but a\n'
          '\t\t\t// lesson label ("Lesson One", "Lesson #3", "Lesson 5 continued") is no title — the first REAL\n'
          '\t\t\t// heading names the page (label-only headings skipped, the label stripped from a prefixed one).\n'
          '\t\t\t// Data body_region.lesson_title_dedup.lesson_label_titles; env LESSONLABEL_OFF.\n'
          '\t\t\tconst _llCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_label_titles;\n'
          '\t\t\tconst _llOn = !!_llCfg && _llCfg.enabled !== false && !!_llCfg.label_pattern\n'
          '\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_llCfg.env ?? "LESSONLABEL_OFF"]);\n'
          '\t\t\tconst _llRe = _llOn ? new RegExp(_llCfg.label_pattern, "i") : null;\n'
          '\t\t\tconst _llMatch = (s) => (_llRe ? _llRe.exec(String(s ?? "").replace(/\\*/g, "").trim()) : null);\n'
          '\t\t\tconst _labelOnly = (s) => { const m = _llMatch(s); return !!m && !String(m[3] ?? "").trim(); };\n'
          '\t\t\tconst _stripLabel = (s) => { const m = _llMatch(s); const rest = m ? String(m[3] ?? "").trim() : ""; return rest || String(s ?? "").trim(); };\n'
          '\t\t\tlet firstHeading = null;\n'
          '\t\t\tfor (const it2 of p.items) {\n'
          '\t\t\t\tif (it2.type !== "tag") continue;\n'
          '\t\t\t\tconst pt2 = it2.parse.primary?.tag;\n'
          '\t\t\t\tconst ht2 = (it2.blackAfter || it2.parse.remainders.join(" ")).replace(/\\*/g, "").trim();\n'
          '\t\t\t\t// a heading that is only a lesson label never names the page — keep scanning\n'
          '\t\t\t\tif (_llOn && ["h1", "h2", "h3", "h4", "h5", "heading"].includes(pt2) && ht2 && _labelOnly(ht2)) continue;\n')
ps = step(ps, "const _llCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_label_titles;", E2_OLD, E2_NEW, "(2a) label-only headings skipped")

E2b_OLD = ('\t\t\tconst _bareNum = /^\\s*\\d+(?:\\.\\d+)?[a-z]?\\s*$/i.test(String(p.pageTitle ?? "").trim());\n'
           '\t\t\tconst _newTitle = (lm ? lm[2] : text).trim();\n'
           '\t\t\tif (!p.pageTitle) p.pageTitle = _newTitle;\n'
           '\t\t\telse if (_lnOn && _bareNum && _newTitle) p.pageTitle = _newTitle;\n')
E2b_NEW = ('\t\t\tconst _bareNum = /^\\s*\\d+(?:\\.\\d+)?[a-z]?\\s*$/i.test(String(p.pageTitle ?? "").trim());\n'
           '\t\t\t// ROUND 324: the harvested heading loses its own label ("Lesson #3 Opening Doors…" → "Opening Doors…")\n'
           '\t\t\tconst _newTitle = (_llOn ? _stripLabel(lm ? lm[2] : text) : (lm ? lm[2] : text)).trim();\n'
           '\t\t\tif (!p.pageTitle) p.pageTitle = _newTitle;\n'
           '\t\t\telse if (_lnOn && _bareNum && _newTitle) p.pageTitle = _newTitle;\n'
           '\t\t\t// ROUND 324: a label-only title ("Lesson One") is replaced by the first real heading; a\n'
           '\t\t\t// label-prefixed one ("Lesson One – The Ode") keeps its own words\n'
           '\t\t\telse if (_llOn && _labelOnly(p.pageTitle) && !(_llMatch(p.pageTitle)?.[2]) && _newTitle && !_labelOnly(_newTitle)) p.pageTitle = _newTitle;   // a "continued" sub-page inherits instead (below)\n'
           '\t\t\telse if (_llOn && _llCfg.strip_existing_title !== false && _stripLabel(p.pageTitle) !== String(p.pageTitle).trim()) p.pageTitle = _stripLabel(p.pageTitle);\n')
ps = step(ps, "_llOn && _labelOnly(p.pageTitle) && !(_llMatch(p.pageTitle)?.[2])", E2b_OLD, E2b_NEW, "(2b) label-only / label-prefixed titles")

# the harvest loop `continue`s a page with no heading BEFORE the title logic, so a label-prefixed [LESSON]
# payload with no heading ("Lesson One – The Ode" when the lesson opens straight into body) still needs the
# strip: apply it in the (3) pass below as well.
# ---------------------------------------------------------------- (3) sub-page inheritance + the no-heading strip
E3_OLD = ('\t\t// RR-4: an opening segment that is only headings (no body content)\n'
          '\t\t// merges forward into the next page rather than shipping a stub\n')
E3_NEW = ('\t\t// ROUND 324 (KB constraint 79): a page whose title is STILL only a lesson label after the harvest\n'
          '\t\t// (no heading of its own) — a sub-page (N.M, M > 0) inherits its parent lesson\'s title\n'
          '\t\t// (CEDT501 5.1 "Lesson 5 continued" → "Speaking up"); a label-PREFIXED title with no heading\n'
          '\t\t// still loses its label. Data lesson_title_dedup.lesson_label_titles; env LESSONLABEL_OFF.\n'
          '\t\t{\n'
          '\t\t\tconst _llCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.lesson_label_titles;\n'
          '\t\t\tconst _llOn = !!_llCfg && _llCfg.enabled !== false && !!_llCfg.label_pattern\n'
          '\t\t\t\t&& !(typeof process !== "undefined" && process.env && process.env[_llCfg.env ?? "LESSONLABEL_OFF"]);\n'
          '\t\t\tif (_llOn) {\n'
          '\t\t\t\tconst _llRe = new RegExp(_llCfg.label_pattern, "i");\n'
          '\t\t\t\tconst _m = (s) => _llRe.exec(String(s ?? "").replace(/\\*/g, "").trim());\n'
          '\t\t\t\tconst _only = (s) => { const m = _m(s); return !!m && !String(m[3] ?? "").trim(); };\n'
          '\t\t\t\tconst _strip = (s) => { const m = _m(s); const r = m ? String(m[3] ?? "").trim() : ""; return r || String(s ?? "").trim(); };\n'
          '\t\t\t\tconst _byLabel = new Map(pages.filter((q) => q.lessonLabel).map((q) => [String(q.lessonLabel), q]));\n'
          '\t\t\t\tfor (const p of pages) {\n'
          '\t\t\t\t\tif (p.isOverview || !p.pageTitle) continue;\n'
          '\t\t\t\t\tif (_only(p.pageTitle)) {\n'
          '\t\t\t\t\t\tif (_llCfg.inherit_parent_on_subpage === false) continue;\n'
          '\t\t\t\t\t\tconst lab = String(p.lessonLabel ?? "");\n'
          '\t\t\t\t\t\tconst mm = /^(\\d+)\\.(\\d+)$/.exec(lab);\n'
          '\t\t\t\t\t\tif (!mm || mm[2] === "0") continue;\n'
          '\t\t\t\t\t\tconst parent = _byLabel.get(`${mm[1]}.0`);\n'
          '\t\t\t\t\t\tif (parent && parent.pageTitle && !_only(parent.pageTitle)) p.pageTitle = parent.pageTitle;\n'
          '\t\t\t\t\t} else if (_llCfg.strip_existing_title !== false && _strip(p.pageTitle) !== String(p.pageTitle).trim()) {\n'
          '\t\t\t\t\t\tp.pageTitle = _strip(p.pageTitle);\n'
          '\t\t\t\t\t}\n'
          '\t\t\t\t}\n'
          '\t\t\t}\n'
          '\t\t}\n\n' + E3_OLD)
ps = step(ps, "a sub-page (N.M, M > 0) inherits its parent lesson's title", E3_OLD, E3_NEW, "(3) sub-page inheritance + no-heading strip")

# ---------------------------------------------------------------- (4) the body de-dup strips the same label forms
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
A4_OLD = '''				const _stripLessonPfx = (s) => _pfxOn
					? (String(s).replace(/^lesson\\s+#?\\d+(?:\\.\\d+)?[a-z]?\\s*[:.\\-–—]?\\s*/i, "") || String(s))
					: String(s);
'''
A4_NEW = '''				// ROUND 324 (KB c79 label titles): the de-dup strips the same label forms as the harvest
				// (word numbers, "#N", "continued") — data lesson_title_dedup.lesson_label_titles
				const _llCfg = _ddCfg?.lesson_label_titles;
				const _llOn = !!_llCfg && _llCfg.enabled !== false && !!_llCfg.label_pattern
					&& !(typeof process !== "undefined" && process.env && process.env[_llCfg.env ?? "LESSONLABEL_OFF"]);
				const _llRe = _llOn ? new RegExp(_llCfg.label_pattern, "i") : null;
				const _stripLessonPfx = (s) => {
					if (!_pfxOn) return String(s);
					if (_llRe) { const m = _llRe.exec(String(s).replace(/\\*/g, "").trim()); if (m && String(m[3] ?? "").trim()) return String(m[3]).trim(); }
					return String(s).replace(/^lesson\\s+#?\\d+(?:\\.\\d+)?[a-z]?\\s*[:.\\-–—]?\\s*/i, "") || String(s);
				};
'''
cc = rd(CC)
cc = step(cc, "const _llCfg = _ddCfg?.lesson_label_titles;", A4_OLD, A4_NEW, "(4) body de-dup label forms")
wr(CC, cc)
wr(PS, ps)
print("done")
