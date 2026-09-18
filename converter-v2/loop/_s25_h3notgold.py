#!/usr/bin/env python3
"""Session 25 — the 700 Claude row-opening h3s whose text is NO gold heading (_s25_h3pair.py NOT-IN-GOLD): what did the
gold do with that text? Buckets: the text is a gold NON-heading element (p / b / li / td / h1 …) → which; the text is
inside a collapsed gold WIDGET; the text is a substring of a longer gold element (the gold merged it); the text is the
page's own title (h1) or the module menu; or the text is nowhere on the gold page (reworded / dropped). Per template /
subject / series with pages + modules.
  python3 _s25_h3notgold.py [prefix-filter]"""
import os, sys, re, json
from collections import Counter, defaultdict
from html.parser import HTMLParser
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm, TextTree, _cls, node_text
import _structural_skeleton
from _structural_skeleton import WIDGET_MARKERS
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
args = [a for a in sys.argv[1:] if not a.startswith("--")]
flt = args[0] if args else ""

def fold(t):
    return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()

def kind(sig):
    s = sig
    if s == "WIDGET": return "WIDGET"
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alert"): return "alert"
    if "Panel" in s: return "panel"
    if s.startswith("div.row"): return "row"
    if s.startswith("div.col"): return "col"
    m = re.match(r"(h[1-6])\b", s)
    if m: return m.group(1)
    if s == "p" or s.startswith("p."): return "p"
    return s.split(".")[0].split("[")[0]

def claude_rowopen_h3(lines):
    bi = next((i for i, l in enumerate(lines) if l.sig.startswith("div#body")), None)
    if bi is None: return []
    base = lines[bi].depth
    stack = []; out = []
    for i in range(bi + 1, len(lines)):
        ln = lines[i]; d = ln.depth
        if d <= base: break
        while stack and stack[-1][0] >= d: stack.pop()
        parent = stack[-1] if stack else None
        cidx = parent[2] if parent else 0
        if parent: parent[2] += 1
        k = kind(ln.sig)
        if re.match(r"h3\b", ln.sig):
            anc = [s[1] for s in stack]
            if d - base == 3 and len(anc) >= 2 and anc[-1] == "col" and anc[-2] == "row" and cidx == 0 and stack[-1][3] == 0:
                nest = next((a for a in reversed(anc) if a in ("activity", "alert", "panel")), None)
                if not nest: out.append((i, fold(ln.text), ln.text))
        stack.append([d, k, 0, cidx if (k == "col" and parent and parent[1] == "row") else 0])
    return out

def gold_elements(path):
    """every text-bearing element of the gold page INCLUDING widget insides: (tag, classes, folded text, in_widget, region-ish)"""
    raw = open(path, encoding="utf-8", errors="replace").read()
    src = _structural_skeleton.body_source(raw)
    tb = TextTree(); tb.feed(src)
    out = []
    def walk(n, inw, inhead):
        c = _cls(n)
        inw2 = inw or bool(c & WIDGET_MARKERS)
        inhead2 = inhead or (n.attrs.get("id") in ("header", "module-menu-content", "footer"))
        t = node_text(n) if n.tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "span", "a", "div", "label", "caption", "figcaption", "button") else ""
        if t:
            out.append((n.tag, c, fold(t), inw2, inhead2))
        for k in n.kids: walk(k, inw2, inhead2)
    body = next((k for k in tb.root.kids if k.tag == "body"), None)
    walk(body if body is not None else tb.root, False, False)
    return out

PARSED = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/03-All_Parsed_Files'
_wtc = {}
def wt_lines_of(code):
    if code in _wtc: return _wtc[code]
    out = []
    try:
        for fn in os.listdir(PARSED):
            if fn.startswith(code + " ") and fn.endswith("_parsed.txt"):
                out += open(os.path.join(PARSED, fn), encoding="utf-8", errors="replace").read().splitlines()
    except Exception:
        pass
    _wtc[code] = out
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
agg = defaultdict(Counter); pagesets = defaultdict(set); modsets = defaultdict(set); ex = defaultdict(list)
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            c, _ = page_lines(cp); g, _ = page_lines(hp)
        except Exception:
            continue
        ch = claude_rowopen_h3(c)
        if not ch: continue
        gheads = {fold(l.text) for l in g if re.match(r"h[2-6]\b", l.sig) and l.text}
        gel = None
        for (i, ft, raw) in ch:
            if not ft or ft in gheads: continue
            if gel is None: gel = gold_elements(hp)
            verdict = None
            exact = [e for e in gel if e[2] == ft]
            if exact:
                e = exact[0]
                if e[4]: verdict = f"gold header/menu {e[0]}"
                elif e[3]: verdict = f"gold inside WIDGET ({e[0]})"
                else:
                    cl = ".".join(sorted(e[1]))
                    verdict = f"gold {e[0]}" + (f".{cl}" if cl and e[0] in ("p", "div", "span") else "")
            else:
                cont = [e for e in gel if len(ft) >= 12 and ft in e[2] and not e[4] and e[0] not in ("div",)]
                if cont:
                    e = cont[0]
                    verdict = f"gold merged into {e[0]}" + (" (widget)" if e[3] else "")
                else:
                    # partial: the first 4 words
                    w = ft.split()
                    key = " ".join(w[:4])
                    part = [e for e in gel if len(w) >= 4 and key in e[2] and not e[4] and e[0] in ("h1", "h2", "h3", "h4", "h5", "p", "b", "li", "td")]
                    verdict = f"gold reworded ({part[0][0]})" if part else "NOWHERE in gold"
            if verdict == "NOWHERE in gold":
                wt = wt_lines_of(code)
                tagged = None
                for wl in wt:
                    if ft and ft in fold(wl):
                        m2 = re.search(r"\[\s*(h[1-6]|title|introduction)\s*\]", wl, re.I)
                        tagged = m2.group(1).lower() if m2 else "untagged"
                        break
                verdict = "NOWHERE in gold — WT " + (tagged or "not found")
            for k in ("ALL", f"template={tf}", f"subject={subject}", f"series={code[:5]}"):
                agg[k][verdict] += 1; pagesets[(k, verdict)].add(cp); modsets[(k, verdict)].add(code)
            if len(ex[verdict]) < 5: ex[verdict].append((code, os.path.basename(cp), raw[:70]))

for k in sorted(agg, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("subject=") else 3, -sum(agg[k].values()))):
    tot = sum(agg[k].values())
    if tot < 25: continue
    print(f"\n== {k} — Claude row-open h3 with no gold heading of that text: {tot}")
    for v, n in agg[k].most_common(16):
        print(f"   {v:36s} {n:5d} ({n/tot:.2f})  pages {len(pagesets[(k, v)]):4d} / modules {len(modsets[(k, v)]):3d}")
print("\nexamples:")
for v, e in ex.items(): print(" ", v, "→", e)
