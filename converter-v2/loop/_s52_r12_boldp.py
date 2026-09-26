#!/usr/bin/env python3
"""_s52_r12_boldp.py — session 52 Round 12: Claude's WHOLE-BOLD paragraphs (`<p><b>text</b></p>`, outside the hand-off boxes, not
red notes) — what the paired GOLD page renders for the same text (h2–h5 / p>b / plain p / li / absent), per family and by the
text's shape (ends with ':' / short / question). WSL, from reference/tests/:  python3 ../../outputs/_s52_r12_boldp.py"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
BP = re.compile(r"<p>\s*<(b|strong)>(.*?)</\1>\s*</p>", re.S)
norm = lambda s: re.sub(r"[^a-z0-9āēīōū ]", "", re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip().lower())
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
def gold_form(g, key):
    for m in re.finditer(r"<(h[1-6]|p|li|td|th|span|div)\b([^>]*)>(.*?)</\1>", g, re.S):
        t = norm(m.group(3))
        if t and (t == key or (len(key) > 12 and t.startswith(key[:40]))):
            inner = m.group(3).strip()
            if m.group(1) == "p":
                return "p>b" if re.fullmatch(r"<(b|strong)>.*</\1>", inner, re.S) else ("p (bold part)" if "<b>" in inner or "<strong>" in inner else "p plain")
            return m.group(1) + (("." + m.group(2).split('"')[1].split()[0]) if 'class="' in m.group(2) and m.group(1) in ("span", "div") else "")
    return "absent"
st = collections.defaultdict(collections.Counter); fam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    for n, cp, hp in pairs(mod):
        s = open(cp, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); e = s.find('class="acks'); sp = spans_of(s)
        g = open(hp, encoding="utf-8", errors="replace").read(); gb = g.find('id="body"'); g = g[gb:] if gb >= 0 else g
        for m in BP.finditer(s, max(b, 0)):
            if e > 0 and m.start() > e: break
            if any(a <= m.start() < z for a, z in sp): continue
            key = norm(m.group(2))
            if len(key) < 3: continue
            shape = "colon" if key and m.group(2).strip().rstrip("</b>").endswith(":") or re.sub(r"<[^>]+>", "", m.group(2)).strip().endswith(":") else ("short<=6w" if len(key.split()) <= 6 else "long")
            gf = gold_form(g, key)
            st[shape][gf] += 1; fam[shape + "|" + gf][re.sub(r"\d.*$", "", mod)] += 1; pages[shape + "|" + gf].add(cp)
            if len(ex[shape + "|" + gf]) < 2: ex[shape + "|" + gf].append(f"{os.path.basename(cp)}: {re.sub(r'<[^>]+>', '', m.group(2))[:60]!r}")
for shape in st:
    print(f"== {shape}: {sum(st[shape].values())}")
    for gf, n in st[shape].most_common(8):
        k = shape + "|" + gf
        print(f"   {n:4d} ({len(pages[k]):3d} pages) gold {gf:14s} top {', '.join(f'{a} {b}' for a, b in fam[k].most_common(5))}  e.g. {ex[k][0][:80] if ex[k] else ''}")
