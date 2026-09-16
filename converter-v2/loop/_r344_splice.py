#!/usr/bin/env python3
"""_r344_splice.py — ROUND 344 (D10-1, KB constraint 47 in full): the engine + data edits, applied surgically.
Idempotent (each anchor asserted once; a second run is a no-op). LF-safe (io.open newline=""). Never json.dumps.
Run from anywhere:  python3 _r344_splice.py            (apply)
                    python3 _r344_splice.py --check    (report only)
"""
import io, os, sys, re
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2"))
CC = os.path.join(ROOT, "app", "js", "ContentConverter.js")
PS = os.path.join(ROOT, "app", "js", "PageSplitter.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")
CHECK = "--check" in sys.argv

def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    if CHECK: return
    io.open(p, "w", encoding="utf-8", newline="").write(s)

def once(s, anchor, where):
    n = s.count(anchor)
    assert n == 1, f"{where}: anchor found {n}x: {anchor[:70]!r}"

# ---------------------------------------------------------------- Emit_Templates.json
et = rd(ET)
if '"c47": {' in et:
    print("Emit_Templates: c47 block already present")
else:
    anchor = '\t\t\t"strip_lesson_prefix": true,\n'
    once(et, anchor, "Emit_Templates")
    block = (
        '\t\t\t"c47": {\n'
        '\t\t\t\t"_doc": "ROUND 344 (the autonomous loop\'s session 12, 2026-09-16 — Chris\'s D10-1, Option A: KB constraint 47 in full, the opening duplicate body heading). On a LESSON page the FIRST RENDERED free-body heading whose text equals the header title once case, punctuation and a `Lesson N` label are ignored is DROPPED — the header already shows it and the lesson NUMBER stays in the #module-code chip (c79: the lesson\'s own title is the h1, never emptied). Three refinements of the r75 de-dup TEST, measured on today\'s corpus (outputs/_measure_r344_c47.py — the first FREE-BODY heading, activity-box titles and the later section repeats the r320 tool counted excluded): 31 target pages / 15 modules in the scored population, the gold drops the heading on 20 and keeps it on 11 = the NAMED overrides D10-1 pre-decides (SCCH301 ×5 / SCPH301 ×3 / HIS1001 / MXEO202 / XDLS903). first_rendered_heading — a heading CONSUMED by the de-dup does not spend the first-heading slot (MXEO202_3_0: `[H2] *Lesson 3 Triangles*` consumed as the title repeat, then `[H3] Triangles` — the real opening heading — was never tested; the mechanism behind most of the 31). ignore_punctuation — the compare keeps letters and digits only (HIS1001_7_0\'s curly quotes, ENGR202\'s italicised `*:*` that defeats the prefix strip, PES1002\'s `**` markers + the writer\'s trailing note). skip_inside_activity — a heading inside an open activity box is the activity\'s own title (ENGI101 \'Being Frank\'): never the candidate and never spends the slot (D10-1: KEPT). exclude_body_class — the Bilingual template (reoTranslate) is excluded: KB 07B governs the MTK section heading, the more specific rule wins (TRR111 ×2). The overview page keeps the r80 exact de-dup unchanged (c47 is strip-only there). Authority: KB level 1 (c47, Universal) over the gold\'s tie. Env DEDUPC47_OFF reverts byte-for-byte.",\n'
        '\t\t\t\t"enabled": true,\n'
        '\t\t\t\t"env": "DEDUPC47_OFF",\n'
        '\t\t\t\t"first_rendered_heading": true,\n'
        '\t\t\t\t"ignore_punctuation": true,\n'
        '\t\t\t\t"skip_inside_activity": true,\n'
        '\t\t\t\t"exclude_body_class": "reoTranslate"\n'
        '\t\t\t},\n'
        '\t\t\t"title_markers": {\n'
        '\t\t\t\t"_doc": "ROUND 344 sibling (D10-1\'s second half — c79 hygiene, upstream of the r327 title-casing seam): a lesson page\'s header title never carries a writer\'s markdown marker. PageSplitter strips every `*` from page.pageTitle at the start of the title post-pass — BEFORE the r324 label / bare-number tests, so `**3**` reads as the bare number it is and takes the lesson\'s own name from its first heading — and collapses whitespace; a title left with no letter or digit (XLP02_4_0\'s `*:`) is emptied so the module-title fallback applies. Fires only on a title that carries a `*` (blast radius = the measured class). Measured (outputs/_measure_r344_c47.py, sibling census): 23 header titles / 8 modules still carried a marker — MXFU302 `**Statistics and Sports**`, PES1008 `*Heat Capacity Calculations*` ×5, XDLS906, SSOG101 `* Police Officers` ×2, SSOG301, MXFU201 `**3**` / `**5**` / `**8. …**`, PES1002 `Fossil Fuels** *Te reo* Māori translation needed` ×9 (the trailing writer\'s note and MXFU201_8\'s `8.` number stay — separate recorded classes under the 20-page floor); the gold ships 0 header titles with a marker. Env TITLEMARK_OFF reverts byte-for-byte.",\n'
        '\t\t\t\t"enabled": true,\n'
        '\t\t\t\t"env": "TITLEMARK_OFF"\n'
        '\t\t\t},\n'
    )
    et = et.replace(anchor, anchor + block, 1)
    wr(ET, et); print("Emit_Templates: c47 + title_markers blocks inserted")

# ---------------------------------------------------------------- PageSplitter.js
ps = rd(PS)
if "ROUND 344 (D10-1 sibling" in ps:
    print("PageSplitter: title_markers strip already present")
else:
    anchor = ("\t\tfor (const p of pages) {\n"
              "\t\t\tif (p.isOverview) continue;\n"
              "\t\t\t// HARVESTING A LESSON'S TITLE FROM ITS FIRST HEADING — but only a\n")
    once(ps, anchor, "PageSplitter")
    ins = ("\t\tfor (const p of pages) {\n"
           "\t\t\tif (p.isOverview) continue;\n"
           "\t\t\t// ROUND 344 (D10-1 sibling — KB c79 hygiene): a header title never carries a writer's\n"
           "\t\t\t// markdown marker. Strip every `*` from the [LESSON] payload BEFORE the label /\n"
           "\t\t\t// bare-number tests below (so `**3**` reads as the bare number it is and takes the\n"
           "\t\t\t// lesson's own name from its first heading) and collapse whitespace; a title left with\n"
           "\t\t\t// no letter or digit is emptied so the module-title fallback applies. Fires only on a\n"
           "\t\t\t// title that carries a `*`. Data body_region.lesson_title_dedup.title_markers;\n"
           "\t\t\t// env TITLEMARK_OFF.\n"
           "\t\t\tconst _tmCfg = DataService?.Data?.EmitTemplates?.body_region?.lesson_title_dedup?.title_markers;\n"
           "\t\t\tif (_tmCfg && _tmCfg.enabled !== false && p.pageTitle && /\\*/.test(String(p.pageTitle))\n"
           "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_tmCfg.env ?? \"TITLEMARK_OFF\"])) {\n"
           "\t\t\t\tconst _t = String(p.pageTitle).replace(/\\*/g, \"\").replace(/\\s+/g, \" \").trim();\n"
           "\t\t\t\tp.pageTitle = /[\\p{L}\\p{N}]/u.test(_t) ? _t : \"\";\n"
           "\t\t\t}\n"
           "\t\t\t// HARVESTING A LESSON'S TITLE FROM ITS FIRST HEADING — but only a\n")
    ps = ps.replace(anchor, ins, 1)
    wr(PS, ps); print("PageSplitter: title_markers strip inserted")

# ---------------------------------------------------------------- ContentConverter.js
cc = rd(CC)
if "static #pageIsLesson" in cc:
    print("ContentConverter: r344 seam already present")
else:
    # (1) the page-is-lesson flag beside its siblings
    a1 = "\tstatic #pageLessonTitle = \"\";\n\tstatic #firstBodyHeadingSeen = false;\n"
    once(cc, a1, "CC field decls")
    cc = cc.replace(a1, a1 + "\t// ROUND 344: the c47 refinements apply to LESSON pages only (the overview keeps the r80 exact de-dup)\n\tstatic #pageIsLesson = false;\n", 1)
    # (2) set it at page setup
    a2 = "\t\t\t: (page.pageTitle || \"\");\n\t\tthis.#firstBodyHeadingSeen = false;\n"
    once(cc, a2, "CC page setup")
    cc = cc.replace(a2, a2 + "\t\tthis.#pageIsLesson = !page.isOverview;\n", 1)
    # (3) the de-dup block: compute the c47 gate before the slot test; slot spent on RENDER; punctuation-insensitive key
    a3 = ("\t\t\tif (!this.#firstBodyHeadingSeen && tag !== \"activity heading\") {\n"
          "\t\t\t\tthis.#firstBodyHeadingSeen = true;\n")
    once(cc, a3, "CC slot test")
    n3 = ("\t\t\t// ROUND 344 (the autonomous loop's session 12 — Chris's D10-1, KB constraint 47 in full):\n"
          "\t\t\t// three refinements of the de-dup TEST on a LESSON page, data\n"
          "\t\t\t// body_region.lesson_title_dedup.c47, env DEDUPC47_OFF. (1) first_rendered_heading — a\n"
          "\t\t\t// heading CONSUMED by the de-dup does not spend the first-heading slot (MXEO202_3_0:\n"
          "\t\t\t// `[H2] *Lesson 3 Triangles*` consumed, then `[H3] Triangles` — the real opening heading —\n"
          "\t\t\t// was never tested); the slot is spent below, only when a heading RENDERS. (2)\n"
          "\t\t\t// ignore_punctuation — the compare keeps letters and digits only (HIS1001's curly quotes,\n"
          "\t\t\t// ENGR202's italicised `*:*`, PES1002's `**` markers + trailing note). (3)\n"
          "\t\t\t// skip_inside_activity — a heading inside an open activity box is the activity's own\n"
          "\t\t\t// title (ENGI101 \"Being Frank\"): never the candidate, never spends the slot. The\n"
          "\t\t\t// Bilingual template (exclude_body_class reoTranslate) is excluded — KB 07B governs the\n"
          "\t\t\t// MTK section heading. The overview page keeps the r80 exact de-dup (c47: strip-only).\n"
          "\t\t\tconst _c47 = tpl.body_region?.lesson_title_dedup?.c47;\n"
          "\t\t\tconst _c47On = !!_c47 && _c47.enabled !== false && this.#pageIsLesson\n"
          "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[_c47.env ?? \"DEDUPC47_OFF\"])\n"
          "\t\t\t\t&& !(_c47.exclude_body_class && new RegExp(_c47.exclude_body_class, \"i\").test(String(run.resolvedRules?.body_class || \"\")));\n"
          "\t\t\tconst _c47Slot = _c47On && _c47.first_rendered_heading !== false;\n"
          "\t\t\tconst _c47InAct = _c47On && _c47.skip_inside_activity !== false\n"
          "\t\t\t\t&& Array.isArray(stack) && stack.some((s) => s && s.mode === \"activity\");\n"
          "\t\t\tif (!this.#firstBodyHeadingSeen && tag !== \"activity heading\" && !_c47InAct) {\n"
          "\t\t\t\tif (!_c47Slot) this.#firstBodyHeadingSeen = true;\n")
    cc = cc.replace(a3, n3, 1)
    # (4) the compare itself
    a4 = ("\t\t\t\tif (this.#pageLessonTitle\n"
          "\t\t\t\t\t&& Utils.Fold(_stripLessonPfx(text)).replace(/\\s+/g, \"\") === Utils.Fold(_stripLessonPfx(this.#pageLessonTitle)).replace(/\\s+/g, \"\")) {\n"
          "\t\t\t\t\t// keep any genuinely-following body text (Part-3 \"BOTH\" case)\n"
          "\t\t\t\t\tif (embedded && it.blackAfter.trim()) out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));\n"
          "\t\t\t\t\treturn out;   // the heading itself is in the header already\n"
          "\t\t\t\t}\n"
          "\t\t\t}\n")
    once(cc, a4, "CC compare")
    n4 = ("\t\t\t\t// ROUND 344: the compare key — Utils.Fold + whitespace removed (r75), or letters and\n"
          "\t\t\t\t// digits only under c47 ignore_punctuation\n"
          "\t\t\t\tconst _ddKey = (s) => {\n"
          "\t\t\t\t\tconst f = Utils.Fold(_stripLessonPfx(s));\n"
          "\t\t\t\t\treturn (_c47On && _c47.ignore_punctuation !== false) ? f.replace(/[^\\p{L}\\p{N}]+/gu, \"\") : f.replace(/\\s+/g, \"\");\n"
          "\t\t\t\t};\n"
          "\t\t\t\tif (this.#pageLessonTitle && _ddKey(text) === _ddKey(this.#pageLessonTitle)) {\n"
          "\t\t\t\t\t// keep any genuinely-following body text (Part-3 \"BOTH\" case)\n"
          "\t\t\t\t\tif (embedded && it.blackAfter.trim()) out.push(...ListsAndRuns.renderBlackText(it.blackAfter, run, it.block?.links));\n"
          "\t\t\t\t\treturn out;   // the heading itself is in the header already\n"
          "\t\t\t\t}\n"
          "\t\t\t\tif (_c47Slot) this.#firstBodyHeadingSeen = true;   // ROUND 344: rendered → the slot is spent\n"
          "\t\t\t}\n")
    cc = cc.replace(a4, n4, 1)
    wr(CC, cc); print("ContentConverter: r344 seam applied")

print("CHECK ONLY — nothing written" if CHECK else "done")
