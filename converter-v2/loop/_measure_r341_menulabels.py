#!/usr/bin/env python3
"""_measure_r341_menulabels.py — ROUND 341 PICK probe, KB constraint 23 / 01B: INSIDE the lesson page's module menu (`#module-menu-content`),
every Claude label-ish leaf (p / h3-h6) whose folded text is a learning-design lead-in → the gold's element for the same text inside ITS menu.
Void-aware HTMLParser (r315). Reports per template / subject / phrase / Claude element; lists the fix population. Writes _r341_menulabels.json."""
import os, sys, re, json, collections, html as H
from html.parser import HTMLParser
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "param", "track"}
LEAD = re.compile(r"^(we(?:\s+are)?\s+learning\b|what are we learning|i can\b|you will (?:show|demonstrate) your understanding\b|success criteria|learning intentions?|how will i know|walt\b|wilf\b|ākonga will|akonga will|i am learning to|what am i learning|what will i learn)", re.I)
def fold(s):
    s = re.sub(r"[\u2018\u2019'`´]", "'", s); s = re.sub(r"[^\w\s']", " ", s.lower()); return re.sub(r"\s+", " ", s).strip()
class Menu(HTMLParser):
    """collect (tag, text) for p/h1-6/li leaves inside #module-menu-content"""
    def __init__(self):
        super().__init__(convert_charrefs=True); self.stack = []; self.depth_in = None; self.cur = None; self.buf = []; self.out = []; self.found = False
    def handle_starttag(self, tag, attrs):
        if tag in VOID: return
        a = dict(attrs)
        if a.get("id") == "module-menu-content": self.depth_in = len(self.stack); self.found = True
        self.stack.append(tag)
        if self.depth_in is not None and tag in ("p", "h1", "h2", "h3", "h4", "h5", "h6", "li") and self.cur is None: self.cur = tag; self.buf = []
    def handle_startendtag(self, tag, attrs): return
    def handle_endtag(self, tag):
        if tag in VOID: return
        if self.cur is not None and tag == self.cur:
            t = fold("".join(self.buf))
            if t: self.out.append((tag, t))
            self.cur = None
        while self.stack:
            top = self.stack.pop()
            if top == tag: break
        if self.depth_in is not None and len(self.stack) <= self.depth_in: self.depth_in = None
    def handle_data(self, d):
        if self.cur is not None: self.buf.append(d)
def menu(path):
    m = Menu(); m.feed(open(path, encoding="utf-8", errors="replace").read()); return m.found, m.out
idx = json.load(open(os.path.join(T, "..", "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})
rows = []; pages_menu_c = pages_menu_g = 0
codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); meta = idx.get(code, {})
    for n, cp, hp in pairs(code):
        if "_0_0" in cp or re.search(r"acks|acknowledge|glossary", os.path.basename(hp) + os.path.basename(cp), re.I): continue   # lesson pages only
        fc, ce = menu(cp); fg, ge = menu(hp)
        if fc: pages_menu_c += 1
        if fg: pages_menu_g += 1
        gmap = collections.defaultdict(list)
        for tag, t in ge: gmap[t].append(tag)
        gk = list(gmap.keys())
        # every gold h5 label in the menu, for the reverse view
        for tag, t in ce:
            if tag == "li" or not LEAD.match(t): continue
            gold = gmap.get(t)
            if not gold:
                pre = " ".join(t.split()[:3]); cand = [k for k in gk if k.startswith(pre) and LEAD.match(k)]
                gold = gmap[cand[0]] if cand else []
            g = "h5" if "h5" in gold else (gold[0] if gold else ("no-gold-menu" if not fg else "absent"))
            ph = re.sub(r"\s+", " ", LEAD.match(t).group(1).lower())
            rows.append({"code": code, "template": tmpl, "subject": meta.get("subject", "?"), "page": os.path.basename(cp), "gold_page": os.path.basename(hp), "claude": tag, "gold": g, "phrase": ph, "text": t[:70]})
json.dump({"rows": rows, "pages_with_menu": {"claude": pages_menu_c, "gold": pages_menu_g}}, open(os.path.join(HERE, "_r341_menulabels.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
def tally(label, rs):
    c = collections.Counter(r["gold"] for r in rs); found = sum(v for k, v in c.items() if k not in ("absent", "no-gold-menu"))
    print(f"{label:50s} n={len(rs):4d} pages={len(set((r['code'], r['page']) for r in rs)):4d} mods={len(set(r['code'] for r in rs)):3d} | gold {dict(c.most_common())} h5/found {c['h5']/found if found else 0:.2f}")
print(f"lesson pages with a module menu: claude {pages_menu_c} / gold {pages_menu_g}; Claude lead-in labels inside the menu: {len(rows)}")
P = [r for r in rows if r["claude"] == "p"]
tally("ALL", rows); tally("  Claude <h5>", [r for r in rows if r["claude"] == "h5"]); tally("  Claude <p>", P); tally("  Claude other", [r for r in rows if r["claude"] not in ("p", "h5")])
print("\nClaude <p> labels in the menu — by template:")
for t in ("Standard", "Bilingual", "Fundamentals", "Inquiry"): tally(f"  {t}", [r for r in P if r["template"] == t])
print("\nClaude <p> labels — by phrase:")
byp = collections.defaultdict(list)
for r in P: byp[r["phrase"]].append(r)
for k, rs in sorted(byp.items(), key=lambda kv: -len(kv[1])): tally(f"  {k}", rs)
print("\nClaude <p> labels — by subject (n>=3):")
bys = collections.defaultdict(list)
for r in P: bys[r["subject"]].append(r)
for k, rs in sorted(bys.items(), key=lambda kv: -len(kv[1])):
    if len(rs) >= 3: tally(f"  {k}", rs)
print("\nClaude <p> labels — by exact text (top 20):")
byt = collections.defaultdict(list)
for r in P: byt[r["text"]].append(r)
for k, rs in sorted(byt.items(), key=lambda kv: -len(kv[1]))[:20]: tally(f"  '{k[:44]}'", rs)
fix = [r for r in P if r["gold"] == "h5"]
print(f"\nFIX POPULATION (Claude p in menu → gold h5 for the same label): {len(fix)} labels / {len(set((r['code'], r['page']) for r in fix))} pages / {len(set(r['code'] for r in fix))} modules")
print("modules:", " ".join(sorted(set(r["code"] for r in fix))))
gp = [r for r in P if r["gold"] == "p"]
print(f"gold keeps <p> (KB-over-gold sites if applied): {len(gp)} labels / {len(set((r['code'], r['page']) for r in gp))} pages / {len(set(r['code'] for r in gp))} modules: {collections.Counter(r['subject'] for r in gp).most_common(8)}")
