#!/usr/bin/env python3
"""ROUND 358 (loop session 19, Round 2 — the Te Reo half of a bilingual title is recognised by the Māori alphabet, not only
by a macron) — the anchored engine + data splice. Idempotent (every edit tests for its own inserted marker first);
LF preserved; node --check on every touched engine file; a duplicate-key JSON load on Emit_Templates.json.

  (1) app/js/Utils.js — Utils.LooksMaori(text, cfg): a macron, OR the Māori alphabet + phonotactics.
  (2) app/js/ContentConverter.js — #oneHalfTeReo(a, b) helper; #bilingualTwoLangGuard / #bilingualDashSplit /
      #bilingualPunctSplit decide "exactly one half Te Reo" through it (OFF = the macron-only test, byte-identical).
  (3) app/js/SkeletonBuilder.js — #lessonPair: the soft separators (spaced dash / slash / colon) after the pipe, guarded.
  (4) data/Emit_Templates.json — header.te_reo_detect {enabled, env REODETECT_OFF, …}; lesson_bilingual_pair.soft_separators.
"""
import os, re, sys, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
UT = os.path.join(PF, "app", "js", "Utils.js"); CC = os.path.join(PF, "app", "js", "ContentConverter.js")
SB = os.path.join(PF, "app", "js", "SkeletonBuilder.js"); ET = os.path.join(PF, "data", "Emit_Templates.json")


def rd(p):
    s = open(p, encoding="utf-8", newline="").read()
    assert "\r\n" not in s, p
    return s


def wr(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


# ---- (1) Utils.LooksMaori
s = rd(UT)
if "static LooksMaori(" not in s:
    anchor = "class Utils {\n"
    assert s.count(anchor) == 1
    block = "\n".join([
        "class Utils {",
        "\t/**",
        "\t * ROUND 358 (the autonomous loop's session-19 Round 2 — the diff miner's TITLE class). Does a title, or one half",
        "\t * of a title, read as te reo Māori? A macron (āēīōū) decides at once. Otherwise the MĀORI ALPHABET + PHONOTACTICS:",
        "\t * every word's letters come from a e i o u h k m n p r t w (g only inside the digraph ng), every word ends in a",
        "\t * vowel, and no two consonants stand together except the digraphs ng / wh; a LONE word needs at least",
        "\t * cfg.min_letters_single_word letters (5) so that \"Time\", \"Home\", \"Note\" stay English while \"Whaikaha\", \"Pepeha\",",
        "\t * \"Mahi Tahi\", \"Te Tautoko Ako\", \"Taku hinga motuhake\" read Māori. Digits and punctuation are skipped; an empty",
        "\t * text is not Māori. Pure. Data: Emit_Templates.header.te_reo_detect. The r321 SkeletonBuilder.#looksMaori",
        "\t * (letters-only) still decides title ORDER — this test decides whether a SEPARATOR is a bilingual boundary.",
        "\t * @param {string} text",
        "\t * @param {Object} [cfg] - header.te_reo_detect",
        "\t * @returns {boolean}",
        "\t */",
        "\tstatic LooksMaori(text, cfg) {",
        "\t\tconst s = String(text ?? \"\");",
        "\t\tif (/[\\u0101\\u0113\\u012b\\u014d\\u016b\\u0100\\u0112\\u012a\\u014c\\u016a]/.test(s)) return true;",
        "\t\tconst minSingle = Number(cfg?.min_letters_single_word ?? 5);",
        "\t\tconst words = s.toLowerCase().replace(/[^a-z\\s'\\u2019-]/g, \" \").split(/[\\s'\\u2019-]+/).filter(Boolean);",
        "\t\tif (!words.length) return false;",
        "\t\tlet letters = 0;",
        "\t\tfor (const w of words) {",
        "\t\t\tif (!/^[aeiouhkmnprtwg]+$/.test(w)) return false;          // a letter outside the Māori alphabet",
        "\t\t\tif (!/[aeiou]$/.test(w)) return false;                   // every Māori word ends in a vowel",
        "\t\t\tconst x = w.replace(/ng/g, \"N\").replace(/wh/g, \"W\");       // the digraphs count as one consonant",
        "\t\t\tif (/g/.test(x)) return false;                            // g only ever inside ng",
        "\t\t\tif (/[hkmnprtwNW]{2}/.test(x)) return false;             // no consonant clusters",
        "\t\t\tletters += w.length;",
        "\t\t}",
        "\t\tif (words.length === 1 && letters < minSingle) return false;",
        "\t\treturn true;",
        "\t}",
        "",
    ])
    s = s.replace(anchor, block, 1)
    wr(UT, s); print("Utils.js: LooksMaori added")
else:
    print("Utils.js: already")

# ---- (2) ContentConverter
s = rd(CC)
assert "Utils." in s, "ContentConverter must see Utils"
if "static #oneHalfTeReo(" not in s:
    anchor = "\tstatic #bilingualTwoLangGuard(parts) {\n"
    assert s.count(anchor) == 1
    helper = "\n".join([
        "\t/** ROUND 358 (the autonomous loop's session-19 Round 2 — the diff miner's TITLE class): \"exactly ONE half reads as",
        "\t *  Te Reo\" — the guard every bilingual title splitter shares. With header.te_reo_detect on, a half reads as Te Reo by",
        "\t *  a macron OR by the Māori alphabet + phonotactics (Utils.LooksMaori) — \"Te Tautoko Ako – Learning Partnership",
        "\t *  Whakatau\", \"Ethical Citizenship / Matatika Kirirarau\", \"Whaikaha: Use your strengths\" now split as the gold does",
        "\t *  (the corpus: 27 split : 3 glued on such lines); with it OFF (env REODETECT_OFF) this is the macron-only test every",
        "\t *  splitter used before this round — byte-identical output. Measured: outputs/_measure_r358_seps.py. */",
        "\tstatic #oneHalfTeReo(a, b) {",
        "\t\tconst td = DataService.Data.EmitTemplates.header?.te_reo_detect;",
        "\t\tconst on = td && td.enabled !== false",
        "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[td.env ?? \"REODETECT_OFF\"]);",
        "\t\tif (on) return Utils.LooksMaori(a, td) !== Utils.LooksMaori(b, td);",
        "\t\tconst macron = /[āēīōūĀĒĪŌŪ]/;",
        "\t\treturn macron.test(a) !== macron.test(b);",
        "\t};",
        "",
    ])
    s = s.replace(anchor, helper + anchor, 1)
    old1 = "\t\tconst macron = /[āēīōūĀĒĪŌŪ]/;\n\t\tif (macron.test(parts[0]) === macron.test(parts[1])) return null;   // exactly ONE half Te Reo\n"
    assert s.count(old1) == 2, s.count(old1)
    s = s.replace(old1, "\t\tif (!this.#oneHalfTeReo(parts[0], parts[1])) return null;   // exactly ONE half Te Reo (r358: a macron OR the Māori alphabet)\n")
    old2 = "\t\tconst macron = /[āēīōūĀĒĪŌŪ]/;\n\t\tif (macron.test(a) === macron.test(b)) return null;  // exactly ONE half is Te Reo (macron)\n"
    assert s.count(old2) == 1, s.count(old2)
    s = s.replace(old2, "\t\tif (!this.#oneHalfTeReo(a, b)) return null;  // exactly ONE half is Te Reo (r358: a macron OR the Māori alphabet)\n")
    wr(CC, s); print("ContentConverter.js: #oneHalfTeReo + 3 guard sites")
else:
    print("ContentConverter.js: already")

# ---- (3) SkeletonBuilder #lessonPair
s = rd(SB)
if "ROUND 358" not in s:
    old = ("\t\tconst seps = Array.isArray(cfg.separators) && cfg.separators.length ? cfg.separators : [\"|\"];\n"
           "\t\tconst sep = seps.find((s) => title.includes(s));\n"
           "\t\tif (!sep) return null;\n"
           "\t\tlet t = String(title);\n"
           "\t\tif (cfg.strip_module_code !== false && run.moduleCode) {\n"
           "\t\t\tconst esc = String(run.moduleCode).replace(/[.*+?^${}()|[\\]\\\\]/g, \"\\\\$&\");\n"
           "\t\t\tt = t.replace(new RegExp(\"^\\\\s*\" + esc + \"\\\\s*[\\\\-\\u2013\\u2014:]?\\\\s*\", \"i\"), \"\");\n"
           "\t\t}\n"
           "\t\tconst i = t.indexOf(sep);\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\tconst seps = Array.isArray(cfg.separators) && cfg.separators.length ? cfg.separators : [\"|\"];\n"
           "\t\tlet t = String(title);\n"
           "\t\tif (cfg.strip_module_code !== false && run.moduleCode) {\n"
           "\t\t\tconst esc = String(run.moduleCode).replace(/[.*+?^${}()|[\\]\\\\]/g, \"\\\\$&\");\n"
           "\t\t\tt = t.replace(new RegExp(\"^\\\\s*\" + esc + \"\\\\s*[\\\\-\\u2013\\u2014:]?\\\\s*\", \"i\"), \"\");\n"
           "\t\t}\n"
           "\t\tlet sep = seps.find((s) => t.includes(s));\n"
           "\t\tif (!sep) {\n"
           "\t\t\t// ROUND 358 (the autonomous loop's session-19 Round 2 — the diff miner's TITLE class). The SOFT separators\n"
           "\t\t\t// (a spaced dash / slash / colon — the overview splitters' own, data lesson_bilingual_pair.soft_separators)\n"
           "\t\t\t// split a lesson's OWN title only when exactly ONE half reads as Te Reo under Utils.LooksMaori (a macron\n"
           "\t\t\t// OR the Māori alphabet + phonotactics; header.te_reo_detect): \"Ngā Whare - Housing\" splits (ANZH104's\n"
           "\t\t\t// gold), \"Time – Quarter Past\" does not (MXFL103's). The pipe above stays unconditional (r316).\n"
           "\t\t\t// Env toggle: REODETECT_OFF (the whole soft path off — the r357 output).\n"
           "\t\t\tconst td = DataService.Data.EmitTemplates.header?.te_reo_detect;\n"
           "\t\t\tconst tdOn = td && td.enabled !== false\n"
           "\t\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[td.env ?? \"REODETECT_OFF\"]);\n"
           "\t\t\tconst softs = Array.isArray(cfg.soft_separators) ? cfg.soft_separators : [];\n"
           "\t\t\tif (tdOn) {\n"
           "\t\t\t\tfor (const s of softs) {\n"
           "\t\t\t\t\tif (t.split(s).length !== 2) continue;                       // exactly ONE occurrence\n"
           "\t\t\t\t\tconst p = t.slice(0, t.indexOf(s)), q = t.slice(t.indexOf(s) + s.length);\n"
           "\t\t\t\t\tif (!p.trim() || !q.trim()) continue;\n"
           "\t\t\t\t\tif (Utils.LooksMaori(p, td) !== Utils.LooksMaori(q, td)) { sep = s; break; }\n"
           "\t\t\t\t}\n"
           "\t\t\t}\n"
           "\t\t\tif (!sep) return null;\n"
           "\t\t}\n"
           "\t\tconst i = t.indexOf(sep);\n")
    s = s.replace(old, new, 1)
    wr(SB, s); print("SkeletonBuilder.js: #lessonPair soft separators")
else:
    print("SkeletonBuilder.js: already")

# ---- (4) Emit_Templates.json
s = rd(ET)
if '"te_reo_detect": {' not in s:
    anchor = '\t\t"lesson_bilingual_pair": {\n'
    assert s.count(anchor) == 1
    block = "\n".join([
        '\t\t"te_reo_detect": {',
        '\t\t\t"enabled": true,',
        '\t\t\t"env": "REODETECT_OFF",',
        '\t\t\t"mode": "macron+phonotactics",',
        '\t\t\t"min_letters_single_word": 5,',
        '\t\t\t"digraphs": ["ng", "wh"],',
        '\t\t\t"_doc": "ROUND 358 (the autonomous loop\'s session-19 Round 2, 2026-09-17 — the diff miner\'s TITLE class, DIFF_QUEUE F1 / #4: the gold\'s second title h1 Claude glues into one). Which half of a separated title is Te Reo: a macron (āēīōū) OR — this round — the MĀORI ALPHABET + PHONOTACTICS (Utils.LooksMaori: every word\'s letters from a e i o u h k m n p r t w with g only inside ng, every word vowel-final, no consonant clusters except ng / wh, a lone word ≥ min_letters_single_word letters). Read by ContentConverter.#oneHalfTeReo (the guard every overview bilingual splitter shares — dash r86, slash / colon r168 / r177, punct-pair) and by SkeletonBuilder.#lessonPair\'s soft separators. Measured (outputs/_measure_r358_seps.py over the gate\'s 1955 pairs): with exactly one Māori half the gold splits a non-pipe pair 27 : 3 — the 3 glued are the alphabet test\'s false positives on short English words (\'Time – Quarter Past\', \'Our home: Planet Earth\'), which the phonotactic test rejects. OFF = the macron-only guard every splitter used before this round (byte-identical output)."',
        '\t\t},',
        '',
    ])
    s = s.replace(anchor, block + anchor, 1)
    old = '\t\t\t"separators": ["|"],\n'
    assert s.count(old) == 1
    s = s.replace(old, old + '\t\t\t"soft_separators": [" – ", " — ", " - ", " / ", ": "],\n'
                  '\t\t\t"soft_guard": "one_half_te_reo",\n'
                  '\t\t\t"_round358_note": "ROUND 358: after the unconditional pipe, a lesson\'s own title splits on the FIRST soft separator that occurs exactly once and leaves exactly ONE half reading as Te Reo (header.te_reo_detect — Utils.LooksMaori); \'Ngā Whare - Housing\' (ANZH104 lesson 2, gold two h1) splits, \'Time – Quarter Past\' (MXFL103, gold one h1) does not. Env REODETECT_OFF disables the soft path.",\n', 1)
    def no_dupes(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit(f"duplicate key: {[k for k in keys if keys.count(k) > 1]}")
        return dict(pairs)
    json.loads(s, object_pairs_hook=no_dupes)
    wr(ET, s); print("Emit_Templates.json: te_reo_detect + soft_separators")
else:
    print("Emit_Templates.json: already")

for p in (UT, CC, SB):
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    print(os.path.basename(p), "node --check:", "OK" if r.returncode == 0 else r.stderr[:300])
