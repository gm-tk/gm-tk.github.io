#!/usr/bin/env python3
"""Session 25 — WHERE THE SCORE GOES, in percentage points of the corpus mean (not line counts): for every paired page
the gate's difflib alignment (autojunk=False) over the miner's text-bearing skeleton lines; every unmatched line on either
side costs 1 / (|gold| + |Claude|) of that page's ratio, so summing those weights over pages / N gives the pp of the corpus
mean lost to each (region, container, direction, element) — a line on a 40-line page weighs 5× one on a 200-line page.
Groups: region (the miner's), container (inside an activity / alert / panel / free), direction (MISSING = gold-only,
EXTRA = Claude-only), element (the tag + first class, widget lines as WIDGET). Per template with the top rows.
  python3 _s25_losspp.py [prefix-filter] [--top N]"""
import os, sys, re, difflib, json
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
argv = list(sys.argv[1:]); top = 40
if "--top" in argv:
    i = argv.index("--top"); top = int(argv[i + 1]); del argv[i:i + 2]
args = [a for a in argv if not a.startswith("--")]
flt = args[0] if args else ""

def elem(sig):
    if sig == "WIDGET": return "WIDGET"
    if sig.startswith("┌"): return "repeat"
    m = re.match(r"([a-z0-9]+)(#[^.\[]+)?(\.[^\[]+)?", sig)
    if not m: return sig[:20]
    tag = m.group(1); cls = (m.group(3) or "")[1:]
    first = cls.split(".")[0] if cls else ""
    if tag == "div":
        toks = cls.split(".") if cls else []
        if "row" in toks: return "div.row" + (".supervisor" if "supervisor" in toks else "")
        col = [t for t in toks if t.startswith("col")]
        if col: return "div." + ".".join(sorted(col))
        if any(t.startswith("activity") for t in toks): return "div.activity"
        if any(t.startswith("alert") for t in toks): return "div." + [t for t in toks if t.startswith("alert")][0]
        if "videoSection" in toks: return "div.videoSection"
        return "div." + first if first else "div"
    return tag + ("." + first if first and tag in ("p", "img", "ul", "a", "span", "b", "h4", "h5", "h3", "h2", "iframe", "table") else "")

def containers(lines):
    """for each line: the nearest container kind (activity / alert / panel / free) by the ancestor chain"""
    out = []; stack = []
    for ln in lines:
        d = ln.depth
        while stack and stack[-1][0] >= d: stack.pop()
        cont = next((s[1] for s in reversed(stack) if s[1]), None) or "free"
        out.append(cont)
        s = ln.sig
        k = "activity" if s.startswith("div.activity") else "alert" if s.startswith("div.alert") else "panel" if ("Panel" in s or s.startswith("div.introduction")) else None
        stack.append((d, k))
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
loss = defaultdict(lambda: defaultdict(float))   # group -> key -> pp
pagecount = Counter(); pagesets = defaultdict(lambda: defaultdict(set))
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        gc = containers(g); cc = containers(c)
        w = 1.0 / max(len(gs) + len(cs), 1)
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        keys = ("ALL", f"template={tf}")
        for k in keys: pagecount[k] += 1
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal": continue
            for i in range(i1, i2):
                l = g[i]; key = (l.region, gc[i], "MISSING", elem(l.sig))
                for k in keys: loss[k][key] += w; pagesets[k][key].add(hp)
            for j in range(j1, j2):
                l = c[j]; key = (l.region, cc[j], "EXTRA", elem(l.sig))
                for k in keys: loss[k][key] += w; pagesets[k][key].add(cp)

for k in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"):
    if not pagecount[k]: continue
    N = pagecount[k]
    L = loss[k]
    total = sum(L.values()) / N * 100
    print(f"\n== {k} — pages {N}: total loss {total:.2f}pp of the mean (= 100 − the sequence match)")
    # by region
    byr = Counter(); byc = Counter(); byd = Counter()
    for (r, c, d, e), v in L.items():
        byr[r] += v; byc[c] += v; byd[d] += v
    print("   by region:    " + ", ".join(f"{r} {v/N*100:.2f}" for r, v in byr.most_common()))
    print("   by container: " + ", ".join(f"{r} {v/N*100:.2f}" for r, v in byc.most_common()))
    print("   by direction: " + ", ".join(f"{r} {v/N*100:.2f}" for r, v in byd.most_common()))
    print(f"   top {top} (region · container · direction · element): pp, pages")
    for key, v in sorted(L.items(), key=lambda kv: -kv[1])[:top]:
        print(f"     {v/N*100:6.2f}pp  {len(pagesets[k][key]):5d} pp   {key[0]:12s} {key[1]:9s} {key[2]:8s} {key[3]}")
