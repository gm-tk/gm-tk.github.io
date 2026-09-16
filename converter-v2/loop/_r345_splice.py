#!/usr/bin/env python3
"""_r345_splice.py — ROUND 345 (D10-2: the bilingual lesson-title pair is ENGLISH FIRST outside the MTK reoTranslate modules).
Idempotent; LF-safe; never json.dumps. Run from anywhere:  python3 _r345_splice.py [--check]"""
import io, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", "..", "pageforge-site", "converter-v2"))
SB = os.path.join(ROOT, "app", "js", "SkeletonBuilder.js")
ET = os.path.join(ROOT, "data", "Emit_Templates.json")
CHECK = "--check" in sys.argv
def rd(p): return io.open(p, encoding="utf-8", newline="").read()
def wr(p, s):
    if not CHECK: io.open(p, "w", encoding="utf-8", newline="").write(s)
def once(s, a, w): n = s.count(a); assert n == 1, f"{w}: anchor found {n}x: {a[:70]!r}"

et = rd(ET)
if '"english_first": {' in et:
    print("Emit_Templates: english_first already present")
else:
    anchor = '\t\t\t"reo_fallback": "second",\n\t\t\t"_round316_note":'
    once(et, anchor, "Emit_Templates")
    block = ('\t\t\t"reo_fallback": "second",\n'
             '\t\t\t"english_first": {\n'
             '\t\t\t\t"_doc": "ROUND 345 (the autonomous loop\'s session 12, 2026-09-16 — Chris\'s D10-2, Option B, verbatim: \'Go with option B — English first in Standard modules\'). Outside the MTK reoTranslate modules (whose 07D rule 7 — Māori first — is untouched above) a lesson\'s own bilingual title pair ships the ENGLISH half first and the Te Reo half second: when exactly one half reads as Te Reo it goes second; when both or neither do, the writer\'s order stands and the page is recorded. reo_detect: a macron decides first (the r316 test); when neither or both halves carry one, \'alphabet\' lets the r321 #looksMaori test decide (letters only from the Māori alphabet — Rapa Nui / Whakawhanaungatanga / He kupu whakakapi read as Te Reo, Easter Island / Learning to relate… do not; One | Tahi both read as Te Reo → as written). Measured (outputs/_measure_r345_engfirst.py, every paired non-reoTranslate lesson page with a two-span title, 23 pages): the macron alone decides 2 (ANZH101_2_0 gains the gold\'s order; ANZH105_1_0 = a NAMED override, the human kept Te Reo first), the alphabet fallback decides 5 more (MXDB202_3_0 / XDLS501_1_0 / XGF9002_9_0 gain the gold\'s order; HIS1006_9_0 = the second NAMED override D10-2 itself names; TEDC402_1_0\'s gold carries a different title); gold agreement 12 → 15 of 23. The KB is silent for Standard — a KB delta (00G c79 / 01A) is recorded for a KB session. Env ENGFIRST_OFF reverts byte-for-byte.",\n'
             '\t\t\t\t"enabled": true,\n'
             '\t\t\t\t"env": "ENGFIRST_OFF",\n'
             '\t\t\t\t"reo_detect": "macron+alphabet"\n'
             '\t\t\t},\n'
             '\t\t\t"_round316_note":')
    et = et.replace(anchor, block, 1); wr(ET, et); print("Emit_Templates: english_first inserted")

sb = rd(SB)
if "ROUND 345 (Chris's D10-2" in sb:
    print("SkeletonBuilder: r345 seam already present")
else:
    a1 = ("\t\tconst reoCls = cfg.reo_first_when_body_class;\n"
          "\t\tconst reoMode = !!reoCls && new RegExp(reoCls, \"i\").test(String(rules?.body_class || \"\"));\n"
          "\t\tif (!reoMode) return [a, b];\n"
          "\t\tconst M = /[\\u0101\\u0113\\u012b\\u014d\\u016b\\u0100\\u0112\\u012a\\u014c\\u016a]/;   // āēīōū\n"
          "\t\tconst ma = M.test(a), mb = M.test(b);\n")
    once(sb, a1, "SkeletonBuilder")
    n1 = ("\t\tconst reoCls = cfg.reo_first_when_body_class;\n"
          "\t\tconst reoMode = !!reoCls && new RegExp(reoCls, \"i\").test(String(rules?.body_class || \"\"));\n"
          "\t\tconst M = /[\\u0101\\u0113\\u012b\\u014d\\u016b\\u0100\\u0112\\u012a\\u014c\\u016a]/;   // āēīōū\n"
          "\t\tconst ma = M.test(a), mb = M.test(b);\n"
          "\t\tif (!reoMode) {\n"
          "\t\t\t// ROUND 345 (Chris's D10-2): outside the reoTranslate modules the ENGLISH half goes\n"
          "\t\t\t// first — when exactly one half reads as Te Reo (a macron decides; when neither or both\n"
          "\t\t\t// halves carry one, the r321 #looksMaori alphabet test decides) it ships SECOND; both /\n"
          "\t\t\t// neither → the writer's order stands. Data lesson_bilingual_pair.english_first; env ENGFIRST_OFF.\n"
          "\t\t\tconst ef = cfg.english_first;\n"
          "\t\t\tconst efOn = !!ef && ef.enabled !== false\n"
          "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[ef.env ?? \"ENGFIRST_OFF\"]);\n"
          "\t\t\tif (efOn) {\n"
          "\t\t\t\tlet reoA = ma, reoB = mb;\n"
          "\t\t\t\tif (ma === mb && /alphabet/.test(String(ef.reo_detect ?? \"macron+alphabet\"))) {\n"
          "\t\t\t\t\treoA = SkeletonBuilder.#looksMaori(a); reoB = SkeletonBuilder.#looksMaori(b);\n"
          "\t\t\t\t}\n"
          "\t\t\t\tif (reoA && !reoB) return [b, a];\n"
          "\t\t\t}\n"
          "\t\t\treturn [a, b];\n"
          "\t\t}\n")
    sb = sb.replace(a1, n1, 1); wr(SB, sb); print("SkeletonBuilder: r345 seam applied")
print("CHECK ONLY" if CHECK else "done")
