#!/usr/bin/env python3
"""_measure_r318_lazyhosts.py — ROUND 318 (loop Round 5) measurement probe: KB constraint 83, no
loading="lazy" on an image INSIDE a moving-or-draggable interactive.

Depth-balanced containment (a void-aware tag walk): an <img> is "inside a host" when any open
ancestor carries one of the host classes. Counts, on every Claude and gold page:
  * images inside a host: with / without loading="lazy" — per host class, per template folder;
  * images outside any host: with / without loading="lazy" (the KB keeps those lazy).
Paths are dynamic (CLAUDE.md §13). Run from anywhere:  python3 _measure_r318_lazyhosts.py
Writes _r318_lazyhosts.json next to itself and prints the summary.
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
# the KB's list (constraint 83): outer hosts + the inner pieces it names (the sibling clickDropContent matters)
HOSTS = ["rotateBanner", "bannerContainer", "bannerItem", "carousel", "dragAndDrop", "drag", "drop", "ddContainer", "ddColumn",
         "clickDrop", "clickDropContent", "flipCard", "front", "back", "flipImage", "memoryGame", "memCard", "cardHidden", "canvasContainer"]
OUTER = {"rotateBanner", "bannerContainer", "carousel", "dragAndDrop", "clickDrop", "clickDropContent", "flipCard", "memoryGame", "canvasContainer"}
VOID = {"img", "br", "meta", "link", "input", "hr", "source", "wbr", "area", "base", "col", "embed", "track"}
TAG = re.compile(r'<(/?)([a-zA-Z][\w-]*)((?:"[^"]*"|\'[^\']*\'|[^>"\'])*)>')
CLS = re.compile(r'class="([^"]*)"')

def walk(html):
    """yield (img_tag_text, innermost_host_class_or_None, outer_host_or_None) for every <img>."""
    stack = []   # entries: (tag, hostclass or None)
    for m in TAG.finditer(html):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if name in ("script", "style"):
            continue
        if closing:
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == name:
                    del stack[i:]; break
            continue
        cls = set((CLS.search(attrs).group(1).split() if CLS.search(attrs) else []))
        host = next((h for h in HOSTS if h in cls), None)
        if name == "img":
            inner = next((h for t, h in reversed(stack) if h), None)
            outer = next((h for t, h in stack if h in OUTER), None)
            yield m.group(0), inner, outer
            continue
        if name in VOID or attrs.rstrip().endswith("/"):
            continue
        stack.append((name, host))

def scan(root):
    C = collections.Counter(); byhost = collections.defaultdict(collections.Counter); bytmpl = collections.defaultdict(collections.Counter)
    pages_with = set(); mods_with = set()
    for t in os.listdir(root):
        tp = os.path.join(root, t)
        if not os.path.isdir(tp): continue
        for code in os.listdir(tp):
            cd = os.path.join(tp, code)
            if not os.path.isdir(cd): continue
            for f in os.listdir(cd):
                if not f.endswith(".html"): continue
                html = open(os.path.join(cd, f), encoding="utf-8", errors="replace").read()
                for img, inner, outer in walk(html):
                    lazy = 'loading="lazy"' in img
                    if inner:
                        C["inside_lazy" if lazy else "inside_nolazy"] += 1
                        byhost[inner]["lazy" if lazy else "nolazy"] += 1
                        bytmpl[t]["lazy" if lazy else "nolazy"] += 1
                        if lazy: pages_with.add((code, f)); mods_with.add(code)
                    else:
                        C["outside_lazy" if lazy else "outside_nolazy"] += 1
    return C, byhost, bytmpl, pages_with, mods_with

def main():
    c, ch, ct, cp, cm = scan(CLAUDE); g, gh, gt, gp, gm = scan(GOLD)
    summary = {
        "claude": dict(c), "claude_by_host": {k: dict(v) for k, v in ch.items()}, "claude_by_template": {k: dict(v) for k, v in ct.items()},
        "claude_pages_with_lazy_inside": len(cp), "claude_modules_with_lazy_inside": len(cm),
        "gold": dict(g), "gold_by_host": {k: dict(v) for k, v in gh.items()}, "gold_by_template": {k: dict(v) for k, v in gt.items()},
        "gold_pages_with_lazy_inside": len(gp),
    }
    json.dump({"summary": summary, "claude_modules": sorted(cm), "claude_pages": sorted(cp)}, open(os.path.join(HERE, "_r318_lazyhosts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(json.dumps(summary, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    main()
