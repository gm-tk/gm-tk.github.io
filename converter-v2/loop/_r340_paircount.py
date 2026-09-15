#!/usr/bin/env python3
"""_r340_paircount.py — size the 'pair-count' residue of the c79 lesson-title class: paired lesson pages whose FIRST h1 span matches
but the span COUNT differs (gold dual vs Claude single or v.v.). Prints direction, per module, and what the extra span is."""
import os, re, sys, collections, unicodedata
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")); import _corpus
HUMAN = os.path.join(ROOT, "01-Finalized_Modules_"); CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
H1 = re.compile(r"<h1[^>]*>\s*<span[^>]*>(.*?)</span>\s*</h1>", re.S | re.I)
def spans(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    return [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", t)).strip() for t in H1.findall(s)]
def fold(t):
    t = unicodedata.normalize("NFKD", t.lower()); t = "".join(c for c in t if not unicodedata.combining(c))
    return re.sub(r"[^a-z0-9 ]", "", t).strip()
def pkey(f):
    m = re.search(r"[_\-](\d+)[._](\d+)\.html$", f) or re.search(r"[_\-](\d+)\.html$", f)
    if not m: return None
    return float(f"{m.group(1)}.{m.group(2)}") if m.lastindex == 2 else float(m.group(1))
def pages(d):
    out = {}
    for f in sorted(os.listdir(d)):
        if f.endswith(".html"):
            k = pkey(f)
            if k is not None: out[k] = os.path.join(d, f)
    return out
rows = []
for code in _corpus.mods(HUMAN):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not os.path.isdir(cd): continue
    tmpl = os.path.basename(os.path.dirname(hd)); gp, cp = pages(hd), pages(cd)
    ov = gp.get(0.0); gov = spans(ov) if ov else []
    for k in sorted(cp):
        if k == 0.0 or k not in gp: continue
        g, c = spans(gp[k]), spans(cp[k])
        if not g or not c or fold(g[0]) != fold(c[0]) or len(g) == len(c): continue
        extra = g[1:] if len(g) > len(c) else c[1:]
        what = "module-te-reo" if (len(gov) > 1 and extra and fold(extra[0]) == fold(gov[1])) else ("module-english" if (gov and extra and fold(extra[0]) == fold(gov[0])) else "other")
        rows.append((tmpl, code, k, "gold-more" if len(g) > len(c) else "claude-more", len(g), len(c), what, extra[0][:40] if extra else ""))
print("pair-count pages:", len(rows))
print("direction:", collections.Counter(r[3] for r in rows))
print("what the extra span is:", collections.Counter((r[3], r[6]) for r in rows))
print("by module:", collections.Counter(r[1] for r in rows).most_common(20))
for r in rows[:30]: print("  ", r)
