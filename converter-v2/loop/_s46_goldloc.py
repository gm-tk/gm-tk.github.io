#!/usr/bin/env python3
"""Session 46 — where does the human's page put a piece of text? For a module code and a list of texts, find every gold
(or Claude, --claude) page text node that contains each text (folded) and print its container chain (the classed
ancestors: accordion / accHead / tab-pane / activity / alert / card …). Stdlib html.parser only. Import `locate` or run:
    python3 _s46_goldloc.py CODE "text one" "text two" [--claude]"""
import html.parser, os, re, sys, unicodedata
ROOT = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}
def fold(s):
    s = unicodedata.normalize("NFKD", s or "")
    s = "".join(c for c in s if not unicodedata.combining(c))
    s = re.sub(r"[‘’“”'\"*]", "", s.lower())
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s)).strip()
class P(html.parser.HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.nodes = []
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs); self.stack.append((tag, a.get("class") or "", a.get("id") or ""))
    def handle_endtag(self, tag):
        if tag in VOID: return
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag: del self.stack[i:]; break
    def handle_data(self, d):
        if d.strip(): self.nodes.append((d, list(self.stack)))
_cache = {}
def pages(code, claude=False):
    base = os.path.join(ROOT, "01-Claude_Modules_" if claude else "01-Finalized_Modules_")
    for t in os.listdir(base):
        d = os.path.join(base, t, code)
        if os.path.isdir(d): return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".html"))
    d = os.path.join(base, code)
    return sorted(os.path.join(d, f) for f in os.listdir(d) if f.endswith(".html")) if os.path.isdir(d) else []
def parsed(f):
    if f not in _cache:
        p = P(); p.feed(open(f, encoding="utf-8", errors="replace").read()); _cache[f] = p.nodes
    return _cache[f]
def chain(stack):
    keep = []
    for tag, cls, idv in stack:
        if cls or idv in ("body", "module-menu", "module-menu-content", "header"):
            keep.append(f"{tag}{'#' + idv if idv else ''}{'.' + '.'.join(cls.split()[:2]) if cls else ''}")
    return " > ".join(keep[-5:])
def locate(code, text, claude=False):
    want = fold(text)
    out = []
    if len(want) < 4: return out
    for f in pages(code, claude):
        for d, st in parsed(f):
            if want in fold(d): out.append((os.path.basename(f), chain(st), [t for t, _, _ in st][-1] if st else ""))
    return out
if __name__ == "__main__":
    a = [x for x in sys.argv[1:] if not x.startswith("--")]
    for t in a[1:]:
        print(f"--- {t!r}")
        for r in locate(a[0], t, "--claude" in sys.argv)[:6]: print("   ", r)
