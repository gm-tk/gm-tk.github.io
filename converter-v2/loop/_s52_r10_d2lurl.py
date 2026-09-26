#!/usr/bin/env python3
"""_s52_r10_d2lurl.py — session 52 Round 10: every bare D2L / Te Kura URL paragraph (and, with argv[1] = other, every other-host bare
URL paragraph) in Claude's body outside the hand-off boxes — what the GOLD does with the same link on the paired page: a button
(`<a href=…><div class="button…">`), an inline anchor in prose, an embed, the URL as text, or nothing. Keyed by the URL's last
two path segments. WSL, from reference/tests/:  python3 ../../outputs/_s52_r10_d2lurl.py [other]"""
import os, re, sys, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import compare_structure as CS
import _corpus
P = re.compile(r"<p\b[^>]*>\s*(?:<a\b[^>]*>)?\s*(https?://[^\s<\"]+)\s*(?:</a>)?\s*</p>", re.I)
D2L = re.compile(r"desire2learn|tekura|d2l", re.I)
SKIP = re.compile(r"istockphoto|gettyimages|shutterstock|youtu|vimeo", re.I)
want_other = len(sys.argv) > 1 and sys.argv[1] == "other"
def spans_of(s):
    out = []
    for h in re.finditer(r'<div class="cv2-interactive[^"]*"', s):
        d = 0
        for x in re.finditer(r"<(/?)div\b[^>]*>", s[h.start():]):
            d += -1 if x.group(1) else 1
            if d == 0: out.append((h.start(), h.start() + x.end())); break
    return out
def key(u):
    u = u.split("?")[0].rstrip("/").replace("&amp;", "&")
    seg = [x for x in u.split("/") if x]
    return "/".join(seg[-2:]) if len(seg) >= 2 else u
st = collections.Counter(); fam = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); ex = collections.defaultdict(list)
for mod in sorted(m for m in _corpus.gate_mods(CS.CLAUDE) if os.path.isdir(_corpus.mdir(CS.CLAUDE, m))):
    for n, cp, hp in pairs(mod):
        s = open(cp, encoding="utf-8", errors="replace").read(); b = s.find('id="body"'); sp = spans_of(s)
        g = open(hp, encoding="utf-8", errors="replace").read()
        for m in P.finditer(s, max(b, 0)):
            if any(a <= m.start() < z for a, z in sp): continue
            u = m.group(1)
            if SKIP.search(u): continue
            if bool(D2L.search(u)) == want_other: continue
            k0 = key(u)
            i = g.find(k0)
            if i < 0: k = "gold: absent on the page"
            else:
                ctx = g[max(0, i - 400):i + 400]
                tagstart = g.rfind("<", 0, i); tag = g[tagstart:tagstart + 12]
                if tag.startswith("<iframe"): k = "gold: EMBED (iframe)"
                elif tag.startswith("<a"):
                    after = g[i:i + 400]
                    k = "gold: BUTTON" if re.match(r'[^>]*>\s*<div class="[^"]*button', after) else "gold: inline ANCHOR"
                else: k = "gold: other (" + tag[:8] + ")"
            st[k] += 1; fam[k][re.sub(r"\d.*$", "", mod)] += 1; pages[k].add(cp)
            if len(ex[k]) < 3: ex[k].append(f"{os.path.basename(cp)} {u[:80]}")
for k, n in st.most_common():
    print(f"{n:4d} paras / {len(pages[k]):3d} pages  {k}   top: {', '.join(f'{a} {b}' for a, b in fam[k].most_common(6))}")
    for e in ex[k]: print("      e.g.", e)
