#!/usr/bin/env python3
"""_s51_r13_provgold.py — session 51 Round 13 MEASURE: for each PROV row of _s51_r13_prov.log (an untagged proverb-shaped pair in
the WT), the gold's rendering of its reo line — the enclosing callout / widget classes of the gold <p> (or heading) holding it:
whakatauki / alert / quoteText / activity / plain / NOT IN GOLD. Consensus per cue + per template dir. WSL, from reference/tests/."""
import os, re, sys, collections, unicodedata
sys.path.insert(0, os.getcwd())
import _corpus
from html.parser import HTMLParser
G = os.path.join(os.getcwd(), "..", "..", "..", "01-Finalized_Modules_")
O = os.path.join(os.getcwd(), "..", "..", "outputs")
def norm(s):
    s = unicodedata.normalize("NFD", s.lower()); s = "".join(c for c in s if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9 ]+", " ", s)).strip()
WATCH = ("whakatauki", "alert", "important", "quoteText", "activity", "accordion", "card", "tab-pane", "modal", "flipCard", "wananga")
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.stack = []; s.out = []; s.buf = None; s.bd = None
    def handle_starttag(s, t, a):
        if t in ("br", "img", "hr", "input", "meta", "link", "source", "wbr"):
            return
        s.stack.append((t, (dict(a).get("class") or "").split()))
        if t in ("p", "h2", "h3", "h4", "h5", "li", "td", "span") and s.buf is None:
            s.buf = []; s.bd = len(s.stack)
    def handle_endtag(s, t):
        if not s.stack:
            return
        if s.buf is not None and len(s.stack) == s.bd:
            cls = [c for (_t, cc) in s.stack[:-1] for c in cc if c in WATCH]
            s.out.append((norm("".join(s.buf)), s.stack[-1][0], cls)); s.buf = None
        s.stack.pop()
    def handle_data(s, d):
        if s.buf is not None:
            s.buf.append(d)
cache = {}
def gold(code):
    if code in cache:
        return cache[code]
    els = []
    try:
        d = _corpus.mdir(G, code)
        for f in sorted(os.listdir(d)):
            if f.endswith(".html"):
                p = P(); p.feed(open(os.path.join(d, f), encoding="utf-8", errors="replace").read()); els += [(f,) + e for e in p.out]
        tdir = os.path.basename(os.path.dirname(os.path.normpath(d)))
    except Exception:
        tdir = "?"
    cache[code] = (els, tdir); return cache[code]
res = collections.defaultdict(collections.Counter); tot = collections.Counter(); ex = collections.defaultdict(list)
for l in open(os.path.join(O, "_s51_r13_prov.log"), encoding="utf-8"):
    f = l.rstrip("\n").split("\t")
    if len(f) < 8 or f[0] != "PROV":
        continue
    code, lesson, cue, bold, tab, reo, engl = f[1:8]
    key = norm(reo)[:30]
    els, tdir = gold(code)
    hit = [e for e in els if key and key in e[1]]
    if not hit:
        v = "NOT IN GOLD"
    else:
        c = hit[0][3]
        v = "whakatauki" if "whakatauki" in c else (c[-1] if c else f"plain {hit[0][2]}")
    grp = "tagged" if cue == "tag:whakatauki" else "untagged"
    res[grp][v] += 1; tot[grp] += 1
    res[f"{grp} · {tdir}"][v] += 1
    if grp == "untagged" and len(ex[v]) < 5:
        ex[v].append(f"{code} [{cue} {bold}] {reo[:45]!r} / {engl[:30]!r}")
for g in sorted(res):
    n = sum(res[g].values())
    print(f"{g:28s} n={n:3d}  " + ", ".join(f"{k} {v} ({v / n:.2f})" for k, v in res[g].most_common()))
for v, xs in ex.items():
    print(f"\n{v}:"); [print("   ", x) for x in xs]
