#!/usr/bin/env python3
"""Session 27 Round 4 — THE GOLD'S <p> WITH A <br> (1253 gold / 3 Claude; deficit 1250 on 435 pages / 201 modules).
For every gold <p> (and <li>/<td>) that holds a <br> on a paired page: the segments around the FIRST <br>; the SOURCE —
a writer soft break (the r227 census's w:br fragments) or two separate writer paragraphs (a developer join) or a trailing /
leading empty segment (a layout br); and CLAUDE's rendering of the same two segments (consecutive <p>s = split, one
element = joined, absent). By subject.  wsl: python3 _s27_r4_goldbr.py -> _s27_r4_goldbr.out"""
import os, sys, re
from collections import Counter, defaultdict
HERE = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, HERE)
import _measure_softbreak as M
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
EL = re.compile(r'<(p|li|td|th)\b[^>]*>([\s\S]*?)</\1>', re.I)
BR = re.compile(r'<br\s*/?>', re.I)
def strip(s): return re.sub(r"<[^>]+>", " ", s)
def fold(s): return M.fold(strip(s))
KIND = Counter(); SRC = Counter(); CL = Counter(); BYG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); SEGN = Counter()
JOIN = defaultdict(Counter)   # source=para-join by subject: claude verdict
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    try: brs = M.wt_breaks(code) or []
    except Exception: brs = []
    sb_before = set(); sb_after = set()
    for before, after, red in brs:
        a = M.fold(before.replace("**", "").replace("*", ""))[-20:].strip(); b = M.fold(after.replace("**", "").replace("*", ""))[:20].strip()
        if len(a) >= 8: sb_before.add(a)
        if len(b) >= 8: sb_after.add(b)
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        gh = body_source(open(hp, encoding="utf-8", errors="replace").read()); ch = body_source(open(cp, encoding="utf-8", errors="replace").read())
        cels = [(fold(m.group(2)), m.group(1).lower()) for m in EL.finditer(ch)]
        for m in EL.finditer(gh):
            inner = m.group(2)
            if not BR.search(inner): continue
            segs = [fold(s) for s in BR.split(inner)]
            nseg = len(segs); SEGN[min(nseg, 6)] += 1
            segs_ne = [s for s in segs if s]
            if not segs_ne: kind = "all-empty"
            elif len(segs_ne) == 1: kind = "layout-br" + ("-trail" if segs[-1] == "" else "-lead" if segs[0] == "" else "-mid")
            else: kind = "two-texts"
            A = segs_ne[0][-20:].strip() if segs_ne else ""; B = segs_ne[1][:20].strip() if len(segs_ne) > 1 else ""
            src = "n/a"
            if kind == "two-texts":
                if (len(A) >= 8 and A in sb_before) or (len(B) >= 8 and B in sb_after): src = "writer-softbreak"
                else: src = "para-join?"
            cl = "n/a"
            if kind == "two-texts" and len(A) >= 8 and len(B) >= 8:
                cl = "absent"
                for i, (t, tg) in enumerate(cels):
                    ia = t.find(A)
                    if ia < 0: continue
                    if t.find(B, ia) >= 0: cl = "joined"; break
                    if i + 1 < len(cels) and cels[i + 1][0][:len(B) + 30].find(B) >= 0: cl = "split"; break
                    cl = "A-only"
            key = (m.group(1).lower(), kind, src, cl)
            KIND[key] += 1; BYG[g][key] += 1; pages[key].add(hp); mods[key].add(code)
            if kind == "two-texts": JOIN[g][cl] += 1
            if len(EX[key]) < 3: EX[key].append(f"{code} {os.path.basename(hp)} «{segs_ne[0][-30:] if segs_ne else ''}» ¦ «{segs_ne[1][:30] if len(segs_ne) > 1 else ''}»")
out = []
def P(s=""): out.append(s); print(s)
P(f"gold elements with a <br>: {sum(KIND.values())}; segments per element: {dict(SEGN)}")
P("==== (element, kind, source, claude) ====")
for key, v in KIND.most_common(30):
    P(f"   {v:5d}  pages {len(pages[key]):4d} mods {len(mods[key]):3d}   {key}")
P()
P("==== two-texts by group: Claude's rendering (split = two <p>, joined = one element) ====")
for g, c in sorted(JOIN.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 15: continue
    P(f"   {g:42s} n={t:4d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common()))
P()
for key, ex in EX.items():
    if KIND[key] >= 30:
        for e in ex: P(f"   {key}: {e}")
open(os.path.join(HERE, "_s27_r4_goldbr.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
