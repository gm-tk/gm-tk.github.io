#!/usr/bin/env python3
"""Session 27 Round 2 candidate — THE CALLOUT BOX'S CLASS SET, paired. Every gold box whose class set holds alert / important /
whakatauki / alertActivity / cultural … is paired to the Claude box holding the same opening words (first 8 folded words);
tally gold class-set × Claude class-set, overall and per template/subject — where Claude's token differs from the gold's
convention at ≥ 0.60 in a group, that is the class.  wsl: python3 _s27_r2_alertclass.py → _s27_r2_alertclass.out"""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
BOX = re.compile(r'<div class="((?:[^"]*\b(?:alert|important|whakatauki|alertActivity|cultural)\b[^"]*))"([^>]*)>', re.I)
DIVS = re.compile(r"<div\b|</div>")
def boxes(src):
    out = []
    for m in BOX.finditer(src):
        cls = " ".join(sorted(m.group(1).split())); attrs = m.group(2)
        lay = re.search(r'layout="([^"]*)"', attrs); key = cls + (f"[layout={lay.group(1)}]" if lay else "")
        depth = 0; end = len(src)
        for mm in DIVS.finditer(src, m.start()):
            depth += -1 if mm.group(0) == "</div>" else 1
            if depth == 0: end = mm.end(); break
        inner = re.sub(r"<[^>]+>", " ", src[m.end():end])
        words = re.sub(r"\W+", " ", inner.lower()).split()
        if len(words) < 3: continue
        out.append((key, " ".join(words[:8])))
    return out
PAIRED = Counter(); PAIRED_T = defaultdict(Counter); GOLD_ONLY = Counter(); GOLD_ONLY_T = defaultdict(Counter)
pages_by = defaultdict(set); mods_by = defaultdict(set)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gb = boxes(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            cb = boxes(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cidx = {}
        for k, w in cb: cidx.setdefault(w, k)
        for k, w in gb:
            if w in cidx:
                key = (k, cidx[w]); PAIRED[key] += 1; PAIRED_T[g][key] += 1
                pages_by[key].add(hp); mods_by[key].add(code)
            else:
                GOLD_ONLY[k] += 1; GOLD_ONLY_T[g][k] += 1
out = []
def P(s=""): out.append(s); print(s)
P("==== PAIRED boxes (same opening words): gold class-set → Claude class-set — top 40 ====")
for (gk, ck), v in PAIRED.most_common(40):
    flag = "  <<< DIFFERENT" if gk != ck else ""
    P(f"   {v:5d}  pages {len(pages_by[(gk, ck)]):4d} mods {len(mods_by[(gk, ck)]):3d}   gold {gk:40s} → claude {ck}{flag}")
P()
P("==== per group, for the gold's PLAIN `alert`: what Claude ships (the solid question) ====")
for g, c in sorted(PAIRED_T.items(), key=lambda kv: -sum(kv[1].values())):
    rows = {ck: v for (gk, ck), v in c.items() if gk == "alert"}
    t = sum(rows.values())
    if t < 10: continue
    P(f"   {g:45s} gold-alert n={t:4d}  " + "  ".join(f"{ck} {v} ({v/t:.2f})" for ck, v in sorted(rows.items(), key=lambda kv: -kv[1])[:4]))
P()
P("==== per group, for Claude's `alert solid`: what the gold has ====")
for g, c in sorted(PAIRED_T.items(), key=lambda kv: -sum(kv[1].values())):
    rows = {gk: v for (gk, ck), v in c.items() if ck == "alert solid"}
    t = sum(rows.values())
    if t < 10: continue
    P(f"   {g:45s} claude-solid n={t:4d}  " + "  ".join(f"{gk} {v} ({v/t:.2f})" for gk, v in sorted(rows.items(), key=lambda kv: -kv[1])[:4]))
P()
P("==== gold boxes with NO Claude box of the same words (top 15 class sets) ====")
for k, v in GOLD_ONLY.most_common(15): P(f"   {v:5d}  {k}")
P()
P("==== `alert cultural` (gold) — where and what Claude pairs ====")
for g, c in PAIRED_T.items():
    rows = {ck: v for (gk, ck), v in c.items() if gk.startswith("alert cultural")}
    if rows: P(f"   {g}: {rows}")
for g, c in GOLD_ONLY_T.items():
    rows = {gk: v for gk, v in c.items() if gk.startswith("alert cultural")}
    if rows: P(f"   {g} (gold-only): {rows}")
open(os.path.join(OUTPUTS, "_s27_r2_alertclass.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
