#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE RIGHT-COLUMN IMAGE. The gold's 605 rows [col-md-8 text | col-md-4 > img] — for each: the
image's iStock id → the WT line carrying that id (its bracket words, the tag above, what sits directly after) → Claude's placement
of the same image (inline in the col-md-8 flow / its own row / a side column / missing). Also the REVERSE: every gold img.img-fluid
by placement (side col vs inline) with the same WT features, to find a discriminator.  wsl: python3 _s27_r3_imgside.py"""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
from html.parser import HTMLParser
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}
class N:
    __slots__ = ("tag", "toks", "kids", "parent", "attrs")
    def __init__(s, tag, cls, parent, attrs): s.tag, s.toks, s.kids, s.parent, s.attrs = tag, set(cls.split()), [], parent, attrs
class TB(HTMLParser):
    def __init__(s):
        super().__init__(); s.root = N("root", "", None, {}); s.cur = s.root; s.stack = []
    def handle_starttag(s, tag, attrs):
        a = dict(attrs); n = N(tag, a.get("class") or "", s.cur, a); s.cur.kids.append(n)
        if tag in VOID: return
        s.stack.append(n); s.cur = n
    def handle_startendtag(s, tag, attrs): s.handle_starttag(tag, attrs)
    def handle_endtag(s, tag):
        if tag in VOID or not s.stack: return
        n = s.stack.pop(); s.cur = n.parent or s.root
ID = re.compile(r"(?:iStock-|gm)(\d{6,})", re.I)
def img_id(n):
    src = (n.attrs.get("src") or "") + " " + (n.attrs.get("alt") or "")
    m = ID.search(src); return m.group(1) if m else None
def placement(img):
    """side: the img's nearest col is a col-md-4 sibling of a col-md-8 in a 2-col row; inline: inside a col-md-8 (or other) with text; own-row: the only content of its col"""
    col = img.parent
    while col is not None and not (col.tag == "div" and any(t.startswith("col") for t in col.toks)): col = col.parent
    if col is None: return "no-col"
    row = col.parent
    cols = [c for c in row.kids if c.tag == "div" and any(t.startswith("col") for t in c.toks)] if row else []
    if len(cols) == 2 and "col-md-4" in col.toks and "col-md-8" in cols[0].toks and cols[1] is col: return "side-right"
    if len(cols) == 2 and "col-md-4" in col.toks and cols[0] is col: return "side-left"
    if len(cols) >= 2: return f"multi-col({len(cols)})"
    # single col: does the col hold text besides the image?
    def has_text(x):
        for k in x.kids:
            if k.tag == "#text": return True
            if k.tag not in ("img",) and has_text(k): return True
        return False
    return "inline" if has_text(col) else "own-row"
def walk_imgs(root, out):
    for k in root.kids:
        if k.tag == "img": out.append(k)
        walk_imgs(k, out)
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    pref = [f for f in fs if "writers template" in f.lower()] or fs
    if not pref: return []
    return open(os.path.join(d, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
TAGLINE = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]]*)\]")
def wt_features(lines, iid):
    for i, l in enumerate(lines):
        if iid in l:
            m = TAGLINE.search(l); own = re.sub(r"\s+", " ", (m.group(1) if m else "")).lower().strip()
            # positional words in the own bracket
            pos = "pos-word" if re.search(r"\b(right|rhs|rhc|left|side|beside|next to)\b", own) else ("image-tag" if own.startswith("image") or "image" in own else ("other-tag:" + own[:18] if own else "no-tag"))
            # previous non-blank line
            k = i - 1
            while k >= 0 and not lines[k].strip(): k -= 1
            prev = lines[k] if k >= 0 else ""
            pm = TAGLINE.search(prev); prevtag = (pm.group(1).lower().split()[0] if pm and pm.group(1).strip() else ("black" if prev.strip() and not prev.startswith("┌") and not prev.startswith("│") and not prev.startswith("└") else ("table" if prev.startswith("└") else "blank")))
            # next non-blank line
            k = i + 1
            while k < len(lines) and not lines[k].strip(): k += 1
            nxt = lines[k] if k < len(lines) else ""
            nm = TAGLINE.search(nxt); nexttag = (nm.group(1).lower().split()[0] if nm and nm.group(1).strip() else ("black" if nxt.strip() and not nxt.startswith("┌") else ("table" if nxt.startswith("┌") else "blank")))
            intable = "in-table" if l.startswith("│") else "free"
            return pos, prevtag[:12], nexttag[:12], intable, own[:40]
    return None
G = Counter(); F = defaultdict(Counter); CLP = Counter(); pages = set(); mods = set(); EX = defaultdict(list); BYG = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    lines = None
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gt = TB(); gt.feed(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            ct = TB(); ct.feed(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        gi = []; walk_imgs(gt.root, gi); ci = []; walk_imgs(ct.root, ci)
        cmap = {}
        for im in ci:
            iid = img_id(im)
            if iid and iid not in cmap: cmap[iid] = placement(im)
        for im in gi:
            iid = img_id(im)
            if not iid: continue
            pl = placement(im)
            G[pl] += 1; BYG[g][pl] += 1
            if lines is None: lines = wt_lines(code)
            feat = wt_features(lines, iid)
            fk = feat[:4] if feat else ("not-in-WT",)
            F[pl][fk] += 1
            if pl == "side-right":
                CLP[cmap.get(iid, "missing")] += 1; pages.add(hp); mods.add(code)
                if len(EX[fk]) < 2: EX[fk].append(f"{code} {os.path.basename(hp)} id={iid} own=«{feat[4] if feat else ''}» claude={cmap.get(iid, 'missing')}")
out = []
def P(s=""): out.append(s); print(s)
P("gold img placement (gate pairs, iStock/gm-id images): " + "; ".join(f"{k} {v}" for k, v in G.most_common()))
P(f"side-right images: {G['side-right']} on {len(pages)} pages / {len(mods)} modules; Claude places the same image: " + "; ".join(f"{k} {v}" for k, v in CLP.most_common()))
P()
P("==== WT features (own-bracket, prev tag, next tag, free/in-table) by gold placement — top 12 per placement ====")
for pl in ("side-right", "inline", "own-row"):
    t = sum(F[pl].values())
    P(f"  -- {pl} (n={t}) --")
    for fk, v in F[pl].most_common(12): P(f"     {v:5d} ({v/t:.2f})  {fk}")
P()
P("==== per group: side-right share of all gold images (n ≥ 30) ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 30: continue
    P(f"   {g:42s} n={t:4d}  side-right {c['side-right']/t:.2f}  inline {c['inline']/t:.2f}  own-row {c['own-row']/t:.2f}  other {(t-c['side-right']-c['inline']-c['own-row'])/t:.2f}")
P()
P("==== examples (side-right) ====")
for fk, ex in list(EX.items())[:14]:
    for e in ex: P(f"   {fk}: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_imgside.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
