#!/usr/bin/env python3
"""ROUND 358 — the refinements after the first in-memory probe (27 changed pages: 3 wrong splits + the slot problem).
  (1) Utils.LooksMaori: a hyphenated / apostrophe token is never Māori by the alphabet path ("One-to-one"); a word in
      cfg.english_stopwords (short English words that pass Māori phonotactics — one, to, me, more, here, time, home …)
      is never Māori by the alphabet path.
  (2) SkeletonBuilder.#lessonPair soft split: neither half may contain a sentence break (XMES101's three-sentence title).
  (3) SkeletonBuilder lesson emit: a pair split from an ALL-CAPS title is sentence-cased per half (HES1005 "KAITIAKITANGA –
      BE A KAITIAKI" → "Kaitiakitanga" / "Be a kaitiaki"); a half never starts with a lowercase letter.
  (4) SkeletonBuilder.#englishOf: the <title> element and the lesson-title FALLBACK take the ENGLISH half of a module pair
      by language (constraint 79 (5); 01A "<title> is English-only") — the overview h1 ORDER stays the writer's.
  (5) data: te_reo_detect.english_stopwords / english_slot_by_language / pair_half_casing.
Idempotent; LF; node --check; duplicate-key JSON guard.
"""
import os, json, subprocess
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
PF = os.path.join(ROOT, "pageforge-site", "converter-v2")
UT = os.path.join(PF, "app", "js", "Utils.js"); SB = os.path.join(PF, "app", "js", "SkeletonBuilder.js"); ET = os.path.join(PF, "data", "Emit_Templates.json")


def rd(p):
    s = open(p, encoding="utf-8", newline="").read(); assert "\r\n" not in s, p; return s


def wr(p, s):
    open(p, "w", encoding="utf-8", newline="").write(s)


# (1) Utils.LooksMaori refinements
s = rd(UT)
if "english_stopwords" not in s:
    old = ("\t\tconst words = s.toLowerCase().replace(/[^a-z\\s'\\u2019-]/g, \" \").split(/[\\s'\\u2019-]+/).filter(Boolean);\n"
           "\t\tif (!words.length) return false;\n"
           "\t\tlet letters = 0;\n"
           "\t\tfor (const w of words) {\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\t\tconst stop = new Set((cfg?.english_stopwords ?? []).map((w) => String(w).toLowerCase()));\n"
           "\t\tconst tokens = s.toLowerCase().split(/\\s+/).map((t) => t.replace(/^[^a-z'\\u2019-]+|[^a-z'\\u2019-]+$/g, \"\")).filter(Boolean);\n"
           "\t\tif (!tokens.length) return false;\n"
           "\t\tlet letters = 0;\n"
           "\t\tfor (const tok of tokens) {\n"
           "\t\t\tif (/['\\u2019-]/.test(tok)) return false;                 // a hyphenated / apostrophe token (\"One-to-one\") is never Māori here\n"
           "\t\t\tconst w = tok.replace(/[^a-z]/g, \"\");\n"
           "\t\t\tif (!w) continue;\n"
           "\t\t\tif (stop.has(w)) return false;                            // a short English word that happens to pass Māori phonotactics\n")
    s = s.replace(old, new, 1)
    old2 = "\t\tif (words.length === 1 && letters < minSingle) return false;\n"
    assert s.count(old2) == 1
    s = s.replace(old2, "\t\tif (tokens.length === 1 && letters < minSingle) return false;\n", 1)
    wr(UT, s); print("Utils.js: stopwords + hyphen guard")
else:
    print("Utils.js: already")

# (2)+(3)+(4) SkeletonBuilder
s = rd(SB)
if "static #englishOf(" not in s:
    # (2) sentence-break guard in the soft split
    old = "\t\t\t\t\tif (!p.trim() || !q.trim()) continue;\n\t\t\t\t\tif (Utils.LooksMaori(p, td) !== Utils.LooksMaori(q, td)) { sep = s; break; }\n"
    assert s.count(old) == 1, s.count(old)
    s = s.replace(old, "\t\t\t\t\tif (!p.trim() || !q.trim()) continue;\n"
                       "\t\t\t\t\tif (/[.!?]\\s/.test(p.trim()) || /[.!?]\\s/.test(q.trim())) continue;   // a multi-sentence title is not a pair (XMES101)\n"
                       "\t\t\t\t\tif (Utils.LooksMaori(p, td) !== Utils.LooksMaori(q, td)) { sep = s; break; }\n", 1)
    # (3) per-half casing after the pair is built
    old = "\t\t\tif (pairTitles) titles.push(...pairTitles);\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\t// ROUND 358: a pair split from an ALL-CAPS title is sentence-cased PER HALF (the r327 rule applied to each\n"
                       "\t\t\t// title, so a single-word Māori half — HES1005 \"KAITIAKITANGA\" — is not left in caps by the single-token\n"
                       "\t\t\t// exception), and a half never starts with a lowercase letter (a colon pair's second half). Data\n"
                       "\t\t\t// header.te_reo_detect.pair_half_casing; env REODETECT_OFF.\n"
                       "\t\t\tif (pairTitles && SkeletonBuilder.#teReoDetectOn(tpl) && tpl.header.te_reo_detect?.pair_half_casing !== false) {\n"
                       "\t\t\t\tconst allCaps = SkeletonBuilder.#titleCasing(page.pageTitle || \"\", tpl).changed;\n"
                       "\t\t\t\tpairTitles = pairTitles.map((h) => (allCaps ? String(h).toLowerCase() : String(h)).replace(/\\p{L}/u, (ch) => ch.toUpperCase()));\n"
                       "\t\t\t}\n"
                       "\t\t\tif (pairTitles) titles.push(...pairTitles);\n", 1)
    # (4) the lesson fallback + the <title>
    old = "\t\t\telse titles.push(page.pageTitle || run.englishTitle || content.titleBar.english || \"\");\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\telse titles.push(page.pageTitle || SkeletonBuilder.#englishOf(run.englishTitle, run.teReoTitle, tpl) || content.titleBar.english || \"\");\n", 1)
    old = "\t\t\t\tcode, englishTitle: content.titleBar.english || run.englishTitle || \"\",\n"
    assert s.count(old) == 1
    s = s.replace(old, "\t\t\t\tcode, englishTitle: SkeletonBuilder.#englishOf(content.titleBar.english, content.titleBar.teReo, tpl) || run.englishTitle || \"\",\n", 1)
    # the helpers, placed before #lessonPair
    anchor = "\tstatic #lessonPair(title, run, rules, cfg) {\n"
    assert s.count(anchor) == 1
    helpers = "\n".join([
        "\t/** ROUND 358 — is header.te_reo_detect on (the Māori-alphabet title test; env REODETECT_OFF)? */",
        "\tstatic #teReoDetectOn(tpl) {",
        "\t\tconst td = tpl?.header?.te_reo_detect;",
        "\t\treturn !!td && td.enabled !== false",
        "\t\t\t&& !(typeof process !== \"undefined\" && process.env && process.env[td.env ?? \"REODETECT_OFF\"]);",
        "\t}",
        "",
        "\t/**",
        "\t * ROUND 358 — the ENGLISH one of a module's two titles, BY LANGUAGE. The title-bar slots keep the writer's order",
        "\t * (so the overview h1s do — 01A: 'the parts are emitted in the order the writer wrote them'; CEDW501's gold is Te Reo",
        "\t * first), which means the 'english' slot holds the Māori half of a Māori-first pair. The two consumers that need the",
        "\t * ENGLISH text — the <title> element (01A: English-only) and a lesson page's module-title FALLBACK (constraint 79 (5):",
        "\t * 'the module English title') — ask here: when both titles exist and exactly one reads as Te Reo (Utils.LooksMaori),",
        "\t * the other is returned; otherwise the first slot, exactly as before. Data header.te_reo_detect.english_slot_by_language.",
        "\t */",
        "\tstatic #englishOf(a, b, tpl) {",
        "\t\tconst td = tpl?.header?.te_reo_detect;",
        "\t\tif (!a || !b || !SkeletonBuilder.#teReoDetectOn(tpl) || td.english_slot_by_language === false) return a;",
        "\t\tconst ma = Utils.LooksMaori(a, td), mb = Utils.LooksMaori(b, td);",
        "\t\treturn (ma && !mb) ? b : a;",
        "\t}",
        "",
    ])
    s = s.replace(anchor, helpers + anchor, 1)
    wr(SB, s); print("SkeletonBuilder.js: sentence guard, per-half casing, #englishOf (<title> + lesson fallback)")
else:
    print("SkeletonBuilder.js: already")

# (5) data
s = rd(ET)
if '"english_stopwords"' not in s:
    old = '\t\t\t"digraphs": ["ng", "wh"],\n'
    assert s.count(old) == 1
    s = s.replace(old, old + '\t\t\t"english_stopwords": ["one", "to", "me", "more", "here", "are", "we", "time", "home", "note", "name", "tea", "tie", "toe", "hope", "hero", "pure", "mine", "nine", "none", "area", "mere", "rate", "rope", "ripe", "wire", "hire", "hate", "mate", "tame", "tape", "tone", "tune", "wine", "pine", "ware", "hone", "pea", "ore", "ape", "tome", "tote", "mute", "mote", "mare"],\n'
                  '\t\t\t"english_slot_by_language": true,\n'
                  '\t\t\t"pair_half_casing": true,\n'
                  '\t\t\t"_refinements_note": "ROUND 358, after the first in-memory probe over all 416 (27 changed pages): english_stopwords — short English words that pass Māori phonotactics (\'One-to-one\' → CEDT501 lesson 7 must not split; a hyphenated token is never Māori by the alphabet path either); a multi-sentence lesson title is never a soft pair (XMES101 lesson 2); pair_half_casing — a pair split from an ALL-CAPS title is sentence-cased per half (HES1005 \'KAITIAKITANGA – BE A KAITIAKI\') and a half never starts lowercase; english_slot_by_language — the <title> element and a lesson page\'s module-title fallback take the ENGLISH half of a Māori-first pair (CEDK501 \'Kia Mahitahi – Idea to Action\' → <title>CEDK501 Idea to Action</title>, lesson fallback \'Idea to Action\'), the overview h1 order untouched.",\n', 1)
    def no_dupes(pairs):
        keys = [k for k, _ in pairs]
        if len(keys) != len(set(keys)):
            raise SystemExit(f"duplicate key: {[k for k in keys if keys.count(k) > 1]}")
        return dict(pairs)
    json.loads(s, object_pairs_hook=no_dupes)
    wr(ET, s); print("Emit_Templates.json: stopwords / english_slot_by_language / pair_half_casing")
else:
    print("Emit_Templates.json: already")
for p in (UT, SB):
    r = subprocess.run(["node", "--check", p], capture_output=True, text=True)
    print(os.path.basename(p), "node --check:", "OK" if r.returncode == 0 else r.stderr[:300])
