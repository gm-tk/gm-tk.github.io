#!/usr/bin/env python3
"""Session 26 — THE PAIRED ROW-BREAK CENSUS for every block type, both directions (the _s26_whpair.py idea generalised).
Top-level body rows only (`#body > div.row > div.col-*`), the r51 row_breaks rule's own domain.

  (A) CLAUDE BREAKS — the LAST direct child L of a Claude column, then the FIRST content F of the NEXT row.
      F a heading / activity / callout / widget → 'opener' (opens a row regardless; not a break question).
      Else locate F on the gold page and the last TEXT before-or-at L; same gold top-level row → the gold FLOWS
      across the boundary Claude broke (key: kind of L → 'break-vs-flow').  Different rows → the gold breaks too.
  (B) CLAUDE FLOWS — consecutive direct children (X, Y) of ONE Claude column, Y a text element, X a block of kind T.
      Locate Y and the last text before-or-at X on the gold: different gold rows → the gold BREAKS where Claude
      flowed (key: T → 'flow-vs-break').  Same row → the gold flows too.
Per kind: FLOW / BREAK counts in each direction, pages, modules; per template and subject.  A kind is a candidate in a
direction when the gold disagrees with Claude ≥ 0.60 on ≥ 20 pages / ≥ 10 modules.
  python3 _s26_rowpair.py"""
import os, sys, re
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
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label", "caption", "figcaption", "button", "i", "em")
OPENER_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6")
OPENER_SIGS = ("div.activity", "div.alert", "div.whakatauki", "div.wananga", "div.quoteText", "WIDGET", "div.row.supervisor", "div.rhetoricalQuestion")

def fold(t): return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig

def kind(sig):
    s = sig
    if s == "WIDGET": return "WIDGET"
    if s.startswith("div.activity"): return "activity"
    if s.startswith("div.alertActivity"): return "alertActivity"
    if s.startswith("div.alert"):
        toks = s.split("[")[0].split(".")[1:]
        return "alert" if toks == ["alert"] else "alert." + ".".join(t for t in toks if t != "alert")
    if s.startswith("div.whakatauki"): return "whakatauki"
    if s.startswith("div.wananga"): return "wananga"
    if s.startswith("div.quoteText"): return "quote"
    if s.startswith("div.button"): return "button"
    if s.startswith("a") and (len(s) == 1 or s[1] in ".>[ "): return "a"
    if s.startswith("blockquote"): return "blockquote"
    if s.startswith("iframe"): return "iframe"
    if s.startswith("audio"): return "audio"
    if s.startswith("img"): return "img"
    if s.startswith("ul") or s.startswith("ol"): return "list"
    if s.startswith("div.") and "videoSection" in s: return "video"
    if s.startswith("div.table-responsive") or s.startswith("table"): return "table"
    if s.startswith("div.row"): return "row"
    if s.startswith("br"): return "br"
    m = re.match(r"(h[1-6])\b", s)
    if m: return m.group(1)
    if s.startswith("p") and (len(s) == 1 or s[1] in ".>[ "): return "p"
    return s.split(".")[0].split("[")[0]

def top_rows(lines):
    bi = next((i for i, l in enumerate(lines) if l.sig.startswith("div#body")), None)
    if bi is None: return None, []
    base = lines[bi].depth
    rows = []
    for i in range(bi + 1, len(lines)):
        if lines[i].depth <= base: break
        if lines[i].depth == base + 1 and lines[i].sig.startswith("div.row"):
            rows.append(i)
    return base, rows

def subtree_end(lines, i):
    d = lines[i].depth; j = i + 1
    while j < len(lines) and lines[j].depth > d: j += 1
    return j

def columns_of(lines, r, base):
    """(col_line_idx, [direct child idxs]) for each top-level column of row r"""
    end = subtree_end(lines, r); out = []
    for c in range(r + 1, end):
        if lines[c].depth == base + 2 and lines[c].sig.startswith("div.col"):
            cend = subtree_end(lines, c)
            kids = [k for k in range(c + 1, cend) if lines[k].depth == base + 3]
            out.append((c, kids))
    return out

def first_text_in(lines, i):
    end = subtree_end(lines, i)
    for k in range(i, end):
        if lines[k].text and tag_of(lines[k].sig) in TEXT_TAGS: return fold(lines[k].text)
    return None

def last_text_in(lines, i):
    end = subtree_end(lines, i); t = None
    for k in range(i, end):
        if lines[k].text and tag_of(lines[k].sig) in TEXT_TAGS: t = fold(lines[k].text)
    return t


fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
FC = "div.flipCardsContainer"
POS = defaultdict(Counter); COL = defaultdict(Counter); GP = defaultdict(set); GM = defaultdict(set)
BEF = defaultdict(Counter); BEFp = defaultdict(set); BEFm = defaultdict(set); EXB = []
AFT = defaultdict(Counter)
CPOS = Counter()
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subject}")
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gbase, grows = top_rows(g); cbase, crows = top_rows(c)
        if gbase is None or cbase is None: continue
        page = os.path.basename(cp)
        # (1) gold-side census
        gfc_rows = set()
        for r in grows:
            for ccol, kids in columns_of(g, r, gbase):
                for idx, k in enumerate(kids):
                    if not g[k].sig.startswith(FC): continue
                    gfc_rows.add(r)
                    pos = "only" if len(kids) == 1 else "first" if idx == 0 else "last" if idx == len(kids) - 1 else "middle"
                    colcls = g[ccol].sig.split("[")[0]
                    for kk in keys: POS[kk][pos] += 1; COL[kk][colcls] += 1
                    GP[tf].add(page); GM[tf].add(code)
        # (2) paired before-rule on the Claude side
        g_row_of = {}
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].text and tag_of(g[k].sig) in TEXT_TAGS: g_row_of.setdefault(fold(g[k].text), ri)
        g_fc_row = {}   # the gold row index holding each flipCardsContainer, keyed by its first text
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].sig.startswith(FC):
                    ft = first_text_in(g, k)
                    if ft: g_fc_row.setdefault(ft, ri)
        for r in crows:
            for ccol, kids in columns_of(c, r, cbase):
                for idx, k in enumerate(kids):
                    if not c[k].sig.startswith(FC): continue
                    pos = "only" if len(kids) == 1 else "first" if idx == 0 else "last" if idx == len(kids) - 1 else "middle"
                    CPOS[pos] += 1
                    if idx == 0: continue   # nothing before it in the column — no before-question
                    pt = None
                    for kk in reversed(kids[:idx]):
                        pt = last_text_in(c, kk)
                        if pt: break
                    ft = first_text_in(c, k)
                    if pt is None or ft is None: verdict = "no-text"
                    else:
                        gp = g_row_of.get(pt); gf = g_fc_row.get(ft)
                        if gp is None or gf is None: verdict = "gold-nowhere"
                        elif gp == gf: verdict = "gold-flows (Claude right)"
                        else: verdict = "GOLD-BREAKS before (Claude flowed)"
                    for kk in keys: BEF[kk][verdict] += 1
                    if verdict.startswith("GOLD") or verdict.startswith("gold-flows"):
                        BEFp[kk].add(page); BEFm[kk].add(code)
                    if verdict.startswith("GOLD") and len(EXB) < 8: EXB.append(f"{page[:-5]} before=«{(pt or '')[:40]}» first-card=«{(ft or '')[:30]}»")
print("==== (1) GOLD-side: the top-level flipCardsContainer's column class + position in its column ====")
for kk in sorted(POS, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    tot = sum(POS[kk].values())
    if tot < 3 and not kk.startswith("ALL") and not kk.startswith("template"): continue
    print(f"   {kk:44s} n={tot:3d}  pos={dict(POS[kk].most_common())}  col={dict(COL[kk].most_common(4))}")
print("   gold pages / modules by template:", {k: (len(GP[k]), len(GM[k])) for k in GP})
print("\n==== (2) PAIRED before-rule: Claude's top-level flipCardsContainer with text before it in the SAME column ====")
print("   Claude container positions:", dict(CPOS))
D = "GOLD-BREAKS before (Claude flowed)"; A = "gold-flows (Claude right)"
for kk in sorted(BEF, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    cnt = BEF[kk]; dis = cnt.get(D, 0); ag = cnt.get(A, 0)
    if dis + ag == 0: continue
    print(f"   {kk:44s} gold-breaks {dis:3d} / flows {ag:3d} = {dis/(dis+ag):.2f}  pages {len(BEFp[kk])} / mods {len(BEFm[kk])}  [{ {k: v for k, v in cnt.items() if k not in (D, A)} }]")
for e in EXB: print("      ", e)
