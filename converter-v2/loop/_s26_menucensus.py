#!/usr/bin/env python3
"""Session 26 — the MODULE-MENU list-form census (gold vs Claude), over every paired page the skeleton gate scores.
Inside `#module-menu-content` (the skeleton's module-menu region) count, per side:
  (a) list containers: ul vs ol
  (b) every block that follows a label (h3/h4/h5/p-label) until the next label: its form —
        p×1 / p×N / ul(1) / ul(N) / ol(1) / ol(N) / mixed
  (c) the item count: gold li vs Claude li on the same page (the completeness census)
Grouped ALL / template family / subject prefix (n ≥ 10 pages).
  python3 _s26_menucensus.py"""
import os, sys, re
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
LABEL = re.compile(r"^(h[1-6])$")

def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig

def prefix(code):
    m = re.match(r"^([A-Z]+)", code); return m.group(1) if m else code

def menu(lines):
    return [ln for ln in lines if ln.region == "module-menu"]

def depth_of(ln):
    return ln.depth

def blocks(mlines):
    """split the menu into label → block runs. A label = h1..h6, or a short p ending with ':' (the eng-family p label)."""
    out = []; cur = None
    for ln in mlines:
        t = tag_of(ln.sig); txt = (ln.text or "").strip()
        is_label = bool(LABEL.match(t)) or (t == "p" and txt.endswith(":") and len(txt) <= 60)
        if is_label:
            cur = {"label": txt[:40], "tags": [], "li": 0, "depth": ln.depth}
            out.append(cur)
        elif cur is not None:
            if t in ("ul", "ol", "p") and ln.depth == cur["depth"]:
                cur["tags"].append(t)
            elif t == "li":
                cur["li"] += 1
    return out

def form(b):
    tags = b["tags"]; li = b["li"]
    if not tags: return "none"
    s = set(tags)
    if s == {"p"}: return "p1" if len(tags) == 1 else "pN"
    if s == {"ul"}: return "ul1" if li == 1 else "ulN"
    if s == {"ol"}: return "ol1" if li == 1 else "olN"
    return "mixed:" + "+".join(tags)

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf

C = defaultdict(Counter)       # key -> counter of (side, stat)
PAIRS = defaultdict(Counter)   # key -> counter of (gold_form -> claude_form) for the paired block position
LI = defaultdict(lambda: [0, 0, 0, 0])  # key -> [pages, gold li, claude li, pages gold>claude]
EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; pre = prefix(code)
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gm = menu(g); cm = menu(c)
        if not gm and not cm: continue
        lesson = not os.path.basename(cp).endswith("_0_0.html")
        keys = ["ALL", f"template={tf}", f"prefix={pre}", "page=lesson" if lesson else "page=overview"]
        for side, ml in (("gold", gm), ("claude", cm)):
            for ln in ml:
                t = tag_of(ln.sig)
                if t in ("ul", "ol"):
                    for k in keys: C[k][(side, "list:" + t)] += 1
            for b in blocks(ml):
                for k in keys: C[k][(side, "block:" + form(b))] += 1
        gb = blocks(gm); cb = blocks(cm)
        for i in range(min(len(gb), len(cb))):
            gf = form(gb[i]); cf = form(cb[i])
            for k in keys: PAIRS[k][(gf, cf)] += 1
            if gf != cf and len(EX[(gf, cf)]) < 4:
                EX[(gf, cf)].append(os.path.basename(cp).replace(".html", ""))
        gli = sum(1 for ln in gm if tag_of(ln.sig) == "li"); cli = sum(1 for ln in cm if tag_of(ln.sig) == "li")
        for k in keys:
            LI[k][0] += 1; LI[k][1] += gli; LI[k][2] += cli
            if gli > cli: LI[k][3] += 1

def show(k):
    c = C[k]
    print(f"\n== {k} — pages {LI[k][0]}: gold li {LI[k][1]} / Claude li {LI[k][2]} / pages gold>claude {LI[k][3]}")
    for side in ("gold", "claude"):
        items = sorted(((s, v) for (sd, s), v in c.items() if sd == side), key=lambda kv: -kv[1])
        print(f"   {side:6s}: " + "  ".join(f"{s}={v}" for s, v in items))
    top = sorted(PAIRS[k].items(), key=lambda kv: -kv[1])[:14]
    print("   paired block forms (gold → claude): " + "  ".join(f"{a}→{b}={v}" for (a, b), v in top))

show("ALL"); show("page=overview"); show("page=lesson")
for k in sorted(K for K in C if K.startswith("template=")): show(k)
for k in sorted(K for K in C if K.startswith("prefix=") and LI[K][0] >= 10): show(k)
print("\n== examples of the swapped pairs ==")
for (a, b), ex in sorted(EX.items(), key=lambda kv: -PAIRS["ALL"][kv[0]]):
    if PAIRS["ALL"][(a, b)] >= 5: print(f"   {a}→{b} ({PAIRS['ALL'][(a, b)]}): {' '.join(ex)}")
