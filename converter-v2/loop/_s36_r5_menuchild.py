#!/usr/bin/env python3
"""Session 36 Round 5 PICK measurement — THE MENU SECTION'S CHILD ELEMENT, per group. Inside a module overview's two-column menu,
under each section heading (h4 / h5), the gold's content is either `<p>` paragraphs or `<ul><li>` items. Claude picks one too.
Measure, per subject family and per code prefix, the gold's dominant child and Claude's — structure only, no text matching, so
the human's rewording never clouds it. Only the OVERVIEW page's menu is counted (the lesson menu is a different shape).
Run under WSL: python3 _s36_r5_menuchild.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
TAG = re.compile(r'<(p|h[1-6]|li)\b[^>]*>', re.I)
def menu_seq(path, is_gold):
    s = open(path, encoding="utf-8", errors="replace").read()
    i = -1
    if is_gold:
        for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
            j = s.find(mark)
            if j > 0: i = j; break
    else: i = s.find('<div id="body">')
    head = s[:i] if i > 0 else s
    k = head.find("module-menu-content")
    return [m.group(1).lower() for m in TAG.finditer(head[k:] if k > 0 else "")]
def sections(seq):
    """(heading, [children]) pairs — children are the p / li tags following a heading"""
    out = []; cur = None
    for t in seq:
        if t.startswith("h"): cur = [t, []]; out.append(cur)
        elif cur is not None: cur[1].append(t)
    return out
subj = {}
try:
    import json
    mi = json.load(open(ROOT + "/pageforge-site/converter-v2/data/Module_Structure_Index.json", encoding="utf-8"))
    for k, v in (mi.get("module_meta") or {}).items(): subj[k] = v.get("subject") or "?"
except Exception: pass
bygroup = collections.defaultdict(lambda: collections.Counter())
byprefix = collections.defaultdict(lambda: collections.Counter())
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    ov = [(n, cp, hp) for n, cp, hp in pl if re.search(r'_0_0\.html$', os.path.basename(cp))]
    if not ov: continue
    _, cp, hp = ov[0]
    gs = sections(menu_seq(hp, True)); cs = sections(menu_seq(cp, False))
    gp = sum(len([t for t in ch if t == "p"]) for _, ch in gs); gl = sum(len([t for t in ch if t == "li"]) for _, ch in gs)
    cpp = sum(len([t for t in ch if t == "p"]) for _, ch in cs); cl = sum(len([t for t in ch if t == "li"]) for _, ch in cs)
    if gp + gl < 3 or cpp + cl < 3: continue
    gk = "li" if gl > gp else ("p" if gp > gl else "tie")
    ck = "li" if cl > cpp else ("p" if cpp > cl else "tie")
    key = "gold=%-3s claude=%-3s" % (gk, ck)
    bygroup[subj.get(code, "?")][key] += 1
    byprefix[(re.match(r'[A-Z]+', code) or [code])[0]][key] += 1
tot = collections.Counter()
for g, c in bygroup.items():
    for k, v in c.items(): tot[k] += v
print("paired OVERVIEW menus with >= 3 content children on both sides: %d" % sum(tot.values()))
for k, v in tot.most_common(): print("   %-26s %4d" % (k, v))
print("\nby SUBJECT family (modules; only families with a gold=li or a disagreement):")
for g, c in sorted(bygroup.items(), key=lambda kv: -sum(kv[1].values())):
    dis = sum(v for k, v in c.items() if "gold=li " in k or k.split()[0] != k.split()[1].replace("claude=", "gold="))
    if dis: print("   %-34s %s" % (g[:34], dict(c.most_common())))
print("\nby CODE PREFIX (only prefixes where the gold prefers li):")
for p, c in sorted(byprefix.items(), key=lambda kv: -sum(v for k, v in kv[1].items() if k.startswith("gold=li"))):
    li = sum(v for k, v in c.items() if k.startswith("gold=li"))
    if li: print("   %-8s li-golds %2d of %2d   %s" % (p, li, sum(c.values()), dict(c.most_common(4))))
