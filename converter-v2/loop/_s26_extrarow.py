#!/usr/bin/env python3
"""Session 26 — the near-miss band's EXTRA row: on pages the gate scores ≥ 0.60, every Claude `div.row` / `div.col-*`
skeleton line that difflib left unmatched while ALL the text it wraps matched (the ledger's wrapper-form family).
For each: the row's FIRST text child (tag · text) and what the GOLD wraps that same text in (its nearest row/col
ancestor signature and the element that precedes it).  Aggregated by (Claude opener tag → gold wrapper form) so the
mechanism that opens the extra row is named, with module counts.  Read-only.
  python3 _s26_extrarow.py [min_score=0.60]"""
import os, sys, re, json, difflib
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "i", "em")
MIN = float(sys.argv[1]) if len(sys.argv) > 1 else 0.60
SCORES = {pg["page"]: pg["scaffold"] for pg in json.load(open(os.path.join(OUTPUTS, "_s24_r386_sk_final.json")))["per_page"]}

def fold(t): return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig
def is_rowcol(sig): return sig.startswith("div.row") or sig.startswith("div.col-")

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf

agg = Counter(); aggmods = defaultdict(set); aggpages = defaultdict(set); EX = defaultdict(list)
n_pages = 0; n_extra = 0
for code in sorted(fam):
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        sc = SCORES.get(os.path.basename(cp))
        if sc is None or sc < MIN: continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        n_pages += 1
        gs = [l.pad + l.sig for l in g]; cs = [l.pad + l.sig for l in c]
        sm = difflib.SequenceMatcher(None, gs, cs, autojunk=False)
        matched_c = set(); matched_g = set()
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag == "equal":
                matched_g.update(range(i1, i2)); matched_c.update(range(j1, j2))
        # gold text index: fold(text) -> line idx
        gtext = {}
        for i, ln in enumerate(g):
            if ln.text and tag_of(ln.sig) in TEXT_TAGS and ln.region in ("body", "activity"):
                gtext.setdefault(fold(ln.text), i)
        def gold_wrapper(i):
            """nearest row/col ancestor signature chain of gold line i, and the previous sibling-ish element"""
            d = g[i].depth; chain = []
            j = i - 1
            while j >= 0:
                if g[j].depth < d:
                    if is_rowcol(g[j].sig): chain.append(g[j].sig)
                    d = g[j].depth
                    if d == 0: break
                j -= 1
            return ">".join(reversed(chain)) or "(none)"
        for j, ln in enumerate(c):
            if j in matched_c or ln.region not in ("body", "activity") or not is_rowcol(ln.sig): continue
            if not ln.sig.startswith("div.row"): continue
            # the row's subtree
            d = ln.depth; k = j + 1; kids = []
            while k < len(c) and c[k].depth > d:
                kids.append(k); k += 1
            texts = [k2 for k2 in kids if c[k2].text and tag_of(c[k2].sig) in TEXT_TAGS]
            if not texts: continue
            # wrapper-form = every text child matched by difflib
            if any(k2 not in matched_c for k2 in texts): continue
            n_extra += 1
            first = texts[0]; ft = fold(c[first].text)
            gi = gtext.get(ft)
            gw = gold_wrapper(gi) if gi is not None else "(text not on gold page)"
            # what precedes the row on Claude's side (the previous line at the same or shallower depth)
            prev = None
            for q in range(j - 1, -1, -1):
                if c[q].depth <= d: prev = c[q]; break
            prev_sig = prev.sig if prev else "(start)"
            # what CLOSED the previous Claude row: its last content-bearing descendant (text / img / alert / widget / table)
            closer = "(none)"
            if prev is not None:
                pd = prev.depth; q = j - 1; last = None
                while q >= 0 and c[q].depth > pd:
                    sg = c[q].sig
                    if sg == "WIDGET" or sg.startswith(("img", "table", "iframe", "div.alert", "div.activity", "audio", "video", "div.button", "ul", "ol")) or (c[q].text and tag_of(sg) in TEXT_TAGS):
                        last = c[q]; break
                    q -= 1
                # prefer the enclosing alert / activity of the last text line
                if last is not None:
                    closer = tag_of(last.sig) if (last.text and tag_of(last.sig) in TEXT_TAGS) else last.sig.split("[")[0]
                    if last.text and tag_of(last.sig) in TEXT_TAGS:
                        dd = last.depth; q2 = last.idx - 1
                        while q2 >= 0 and q2 > j - 400:
                            if c[q2].depth < dd:
                                if c[q2].sig.startswith(("div.alert", "div.activity", "table")): closer = c[q2].sig.split("[")[0]; break
                                dd = c[q2].depth
                                if dd <= pd: break
                            q2 -= 1
            prev_sig = "closed-by:" + closer
            # what precedes the text on the gold side
            gprev = None
            if gi is not None:
                for q in range(gi - 1, -1, -1):
                    if g[q].text and tag_of(g[q].sig) in TEXT_TAGS: gprev = g[q]; break
            key = (tag_of(c[first].sig), prev_sig, "gold-wrap:" + gw)
            agg[key] += 1; aggmods[key].add(code); aggpages[key].add(os.path.basename(cp))
            if len(EX[key]) < 3:
                EX[key].append(f"{os.path.basename(cp)[:-5]} «{(c[first].text or '')[:45]}» gold-prev={tag_of(gprev.sig) if gprev else '-'}:«{(gprev.text if gprev else '')[:30]}»")

print(f"pages scored ≥ {MIN}: {n_pages}; Claude EXTRA rows whose text all matched: {n_extra}")
print("\n== by (row's first text tag · what precedes the row on Claude · the gold's wrapper of that text) — rows · pages · modules ==")
for key, v in agg.most_common(40):
    print(f"  {v:4d}  p={len(aggpages[key]):3d} m={len(aggmods[key]):3d}  {key}")
    for e in EX[key][:2]: print(f"           {e}")
print("\n== by the row's first text tag alone ==")
t = Counter(); tm = defaultdict(set)
for key, v in agg.items(): t[key[0]] += v; tm[key[0]] |= aggmods[key]
for k, v in t.most_common(): print(f"  {v:4d}  m={len(tm[k]):3d}  {k}")
print("\n== by what precedes the row on Claude ==")
t = Counter(); tm = defaultdict(set)
for key, v in agg.items(): t[key[1]] += v; tm[key[1]] |= aggmods[key]
for k, v in t.most_common(): print(f"  {v:4d}  m={len(tm[k]):3d}  {k}")
