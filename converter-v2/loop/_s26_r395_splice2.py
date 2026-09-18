#!/usr/bin/env python3
"""r395 second cut — per-subject EXCLUSIONS for the by-count column: the gold's 4-card form is a tie in English (col-md-6 10 /
col-md-3 9 = 0.50) and col-md-3-led in ConnectED (4 / 3) and NCEA1 (2 / 1); the 2-card form is col-md-4 in NCEA1 (2 / 2) and a tie in
the subject-less TEDC modules (col-md-6 4 / col-md-4 3). Data `exclude_subjects_by_count`; the helper takes `run` for the module's
subject (module_meta, the r389 / r391 precedent). Idempotent; LF preserved; WSL."""
import io
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
PF = ROOT + "/pageforge-site/converter-v2"
P = PF + "/data/Emit_Templates.json"
s = io.open(P, encoding="utf-8", newline="").read()
if '"exclude_subjects_by_count"' not in s:
    old = '\t\t\t\t"by_count": {\n\t\t\t\t\t"2": "col-md-6 col-12 paddingLR",\n\t\t\t\t\t"4": "col-md-6 col-12 paddingLR"\n\t\t\t\t}\n\t\t\t},\n'
    assert s.count(old) == 1, s.count(old)
    new = ('\t\t\t\t"by_count": {\n\t\t\t\t\t"2": "col-md-6 col-12 paddingLR",\n\t\t\t\t\t"4": "col-md-6 col-12 paddingLR"\n\t\t\t\t},\n'
           '\t\t\t\t"_exclude_doc": "Per subject (module_meta.subject; the subject-less modules are the empty string): the gold\'s 4-card form is a TIE in 1-10 English (col-md-6 10 / col-md-3 9) and col-md-3-led in ConnectED (4 / 3) and NCEA1 (2 / 1); its 2-card form is col-md-4 in NCEA1 (2 / 2) and a tie in the subject-less TEDC modules (col-md-6 4 / col-md-4 3). Those keep the template default.",\n'
           '\t\t\t\t"exclude_subjects_by_count": {\n'
           '\t\t\t\t\t"2": [\n\t\t\t\t\t\t"NCEA1",\n\t\t\t\t\t\t""\n\t\t\t\t\t],\n'
           '\t\t\t\t\t"4": [\n\t\t\t\t\t\t"1-10 English",\n\t\t\t\t\t\t"ConnectED",\n\t\t\t\t\t\t"NCEA1"\n\t\t\t\t\t]\n'
           '\t\t\t\t}\n\t\t\t},\n')
    s = s.replace(old, new, 1)
    io.open(P, "w", encoding="utf-8", newline="").write(s); print("data: exclude_subjects_by_count")
else:
    print("data: already")
P2 = PF + "/app/js/InteractiveBuilder.js"
s = io.open(P2, encoding="utf-8", newline="").read()
if "exclude_subjects_by_count" not in s:
    n1 = s.count("this.#flipCardsByCount(tpl, cards)"); n2 = s.count("this.#flipCardsByCount(tpl, built)")
    assert n1 == 3 and n2 == 1, (n1, n2)
    s = s.replace("this.#flipCardsByCount(tpl, cards)", "this.#flipCardsByCount(tpl, cards, run)").replace("this.#flipCardsByCount(tpl, built)", "this.#flipCardsByCount(tpl, built, run)")
    old = ("\tstatic #flipCardsByCount(tpl, cards) {\n"
           "\t\tconst cfg = tpl?.card_col_by_count;\n"
           "\t\tif (!cfg || cfg.enabled === false || !Array.isArray(cards)) return cards;\n"
           "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"FLIPCOL_OFF\"]) return cards;\n"
           "\t\tconst to = (cfg.by_count ?? {})[String(cards.length)];\n")
    assert s.count(old) == 1, s.count(old)
    new = ("\tstatic #flipCardsByCount(tpl, cards, run) {\n"
           "\t\tconst cfg = tpl?.card_col_by_count;\n"
           "\t\tif (!cfg || cfg.enabled === false || !Array.isArray(cards)) return cards;\n"
           "\t\tif (typeof process !== \"undefined\" && process.env && process.env[cfg.env ?? \"FLIPCOL_OFF\"]) return cards;\n"
           "\t\tconst to = (cfg.by_count ?? {})[String(cards.length)];\n"
           "\t\t// per-subject exclusions (a tie or the other form leads there — see _exclude_doc); the\n"
           "\t\t// subject-less modules are the empty string\n"
           "\t\tconst excl = (cfg.exclude_subjects_by_count ?? {})[String(cards.length)];\n"
           "\t\tif (Array.isArray(excl) && excl.length) {\n"
           "\t\t\tconst meta = DataService.Data.ModuleStructureIndex?.module_meta?.[String(run?.moduleCode || \"\")];\n"
           "\t\t\tconst subj = String(meta?.subject ?? \"\");\n"
           "\t\t\tif (excl.some((x) => String(x) === subj)) return cards;\n"
           "\t\t}\n")
    s = s.replace(old, new, 1)
    s = s.replace("\t * flipCard.card_col_by_count; env FLIPCOL_OFF (= the r394 output).\n\t * @param {Object} tpl - the flipCard template block\n\t * @param {string[]} cards - the finished card html strings\n",
                  "\t * flipCard.card_col_by_count (+ exclude_subjects_by_count: English's 4-card tie, ConnectED /\n\t * NCEA1's col-md-3 lead, NCEA1 / TEDC's 2-card forms); env FLIPCOL_OFF (= the r394 output).\n\t * @param {Object} tpl - the flipCard template block\n\t * @param {string[]} cards - the finished card html strings\n\t * @param {Object} run - the conversion run (moduleCode → module_meta.subject)\n", 1)
    io.open(P2, "w", encoding="utf-8", newline="").write(s); print("engine: run-aware helper + exclusions")
else:
    print("engine: already")
