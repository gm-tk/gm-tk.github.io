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
A = defaultdict(Counter); Apages = defaultdict(set); Amods = defaultdict(set)
B = defaultdict(Counter); Bpages = defaultdict(set); Bmods = defaultdict(set)
EXA = defaultdict(list); EXB = defaultdict(list)
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
        if gbase is None or cbase is None or not crows: continue
        g_row_of = {}
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].text and tag_of(g[k].sig) in TEXT_TAGS: g_row_of.setdefault(fold(g[k].text), ri)
        page = os.path.basename(cp)
        cols = [columns_of(c, r, cbase) for r in crows]
        # (A) Claude breaks: last child of the last column of row i → first content of row i+1
        for ri in range(len(crows) - 1):
            if not cols[ri] or not cols[ri + 1]: continue
            lcol, lkids = cols[ri][-1]
            if not lkids: continue
            L = lkids[-1]; lk = kind(c[L].sig)
            fcol, fkids = cols[ri + 1][0]
            if not fkids: continue
            F = fkids[0]; fs = c[F].sig
            if tag_of(fs) in OPENER_TAGS or fs.startswith(OPENER_SIGS):
                verdict = "opener"
            else:
                ft = first_text_in(c, F)
                # the last text at-or-before L in the same column
                pt = None
                for k in reversed(lkids):
                    pt = last_text_in(c, k)
                    if pt: break
                if ft is None or pt is None: verdict = "no-text"
                else:
                    gf = g_row_of.get(ft); gp = g_row_of.get(pt)
                    if gf is None or gp is None: verdict = "gold-nowhere"
                    elif gf == gp: verdict = "GOLD-FLOWS (Claude broke)"
                    else: verdict = "gold-breaks (Claude right)"
            for k in keys: A[(k, lk)][verdict] += 1
            if verdict.startswith("GOLD"):
                Apages[lk].add(page); Amods[lk].add(code)
                if len(EXA[lk]) < 4: EXA[lk].append(f"{page[:-5]} L=«{(c[L].text or c[L].sig)[:35]}» F=«{(c[F].text or c[F].sig)[:35]}»")
        # (B) Claude flows: consecutive direct children (X, Y) of one column, Y text
        for ri in range(len(crows)):
            for ccol, kids in cols[ri]:
                for a, b in zip(kids, kids[1:]):
                    if not (c[b].text and tag_of(c[b].sig) in TEXT_TAGS): continue
                    if tag_of(c[b].sig) in OPENER_TAGS: continue
                    xk = kind(c[a].sig)
                    yt = fold(c[b].text)
                    xt = last_text_in(c, a)
                    if xt is None:
                        # a text-less block (img / video / br …): use the last text before it in the column
                        for k in reversed(kids[:kids.index(a)]):
                            xt = last_text_in(c, k)
                            if xt: break
                    if xt is None: verdict = "no-text"
                    else:
                        gy = g_row_of.get(yt); gx = g_row_of.get(xt)
                        if gy is None or gx is None: verdict = "gold-nowhere"
                        elif gy == gx: verdict = "gold-flows (Claude right)"
                        else: verdict = "GOLD-BREAKS (Claude flowed)"
                    for k in keys: B[(k, xk)][verdict] += 1
                    if verdict.startswith("GOLD"):
                        Bpages[xk].add(page); Bmods[xk].add(code)
                        if len(EXB[xk]) < 4: EXB[xk].append(f"{page[:-5]} X=«{(c[a].text or c[a].sig)[:35]}» Y=«{(c[b].text or '')[:35]}»")

def show(D, Dp, Dm, disagree, agree, title):
    print(f"\n==== {title} ====")
    for scope in ("ALL", "template=Standard", "template=Inquiry", "template=Fundamentals", "template=Bilingual"):
        print(f"\n-- {scope} --")
        rows = []
        for (k, kd), cnt in D.items():
            if k != scope: continue
            dis = cnt.get(disagree, 0); ag = cnt.get(agree, 0)
            if dis + ag == 0: continue
            rows.append((dis / (dis + ag), dis, ag, kd, cnt))
        for share, dis, ag, kd, cnt in sorted(rows, key=lambda r: -r[1]):
            flag = "  <== CANDIDATE" if (scope == "ALL" and share >= 0.60 and len(Dp[kd]) >= 20 and len(Dm[kd]) >= 10) else ""
            extra = " ".join(f"{x}={v}" for x, v in cnt.items() if x not in (disagree, agree))
            pg = f"pages {len(Dp[kd])} / mods {len(Dm[kd])}" if scope == "ALL" else ""
            print(f"   {kd:14s} gold-disagrees {dis:4d} / agrees {ag:4d} = {share:.2f}  {pg}  [{extra}]{flag}")
    print("   subject groups with ≥ 0.60 disagree on ≥ 10 boundaries:")
    for (k, kd), cnt in sorted(D.items()):
        if not k.startswith("tmpl+subj="): continue
        dis = cnt.get(disagree, 0); ag = cnt.get(agree, 0)
        if dis + ag >= 10 and dis / (dis + ag) >= 0.60: print(f"     {k} {kd}: {dis} / {ag} = {dis/(dis+ag):.2f}")

show(A, Apages, Amods, "GOLD-FLOWS (Claude broke)", "gold-breaks (Claude right)", "(A) CLAUDE BREAKS a row after block L — does the gold flow?")
print("   examples:"); [print(f"     {k}: " + " | ".join(v)) for k, v in EXA.items() if len(Apages[k]) >= 8]
show(B, Bpages, Bmods, "GOLD-BREAKS (Claude flowed)", "gold-flows (Claude right)", "(B) CLAUDE FLOWS after block X — does the gold break?")
print("   examples:"); [print(f"     {k}: " + " | ".join(v)) for k, v in EXB.items() if len(Bpages[k]) >= 8]
