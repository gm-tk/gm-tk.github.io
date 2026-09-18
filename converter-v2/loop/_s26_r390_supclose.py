#!/usr/bin/env python3
"""Session 26 Round 4 candidate — THE SUPERVISOR NOTE'S EXPLICIT CLOSER: a `[Supervisor note] …` followed by more items and an
explicit `[end supervisor note]` closer — does the gold put the items between opener and closer INSIDE the panel (its
super-content row), where Claude ships them as free rows after it?
(1) WT census over every module's Writers Template parsed.txt (the union of the gold dir's *_parsed.txt, Media List first):
    per opener — has a closer before the next structural opener? items between? (tags of the items)
(2) paired: for each Claude top-level `div.row.supervisor` (non-activity panel) whose next Claude row opens with prose, is that
    prose in the gold INSIDE a super-content panel (the gold's panel column) or in a plain row?
  python3 _s26_r390_supclose.py"""
import os, sys, re, glob
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta, wt_blob

meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf

RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴", re.S)
OPEN = re.compile(r"^\s*\[\s*supervisor\s+note\b", re.I)
CLOSE = re.compile(r"^\s*\[\s*end\s+(of\s+)?supervisor\s+note\s*\]", re.I)
STRUCT = re.compile(r"^\s*\[\s*(activity|h[1-6]|alert|important|supervisor|lesson|end page|title|tab|accordion|carousel|flip|click|drag|modal|video|image|embed|quiz|interactive|button)", re.I)

def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    out = []
    for f in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        n = os.path.basename(f).lower()
        if "media list" in n and "writers template" not in n: continue   # the r313 rule: skip a SEPARATE media list only
        try: out += open(f, encoding="utf-8", errors="replace").read().split("\n")
        except Exception: pass
    return out

def tags_in(line):
    out = []
    for m in RED.finditer(line):
        t = m.group(1).strip()
        if t.startswith("["): out.append(t.lower())
    if not out:
        m = re.match(r"^\s*(\[[^\]]*\])", line)
        if m: out.append(m.group(1).lower())
    return out

WT = defaultdict(Counter); WTm = defaultdict(set); EX = []
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    lines = wt_lines(code)
    for i, l in enumerate(lines):
        tags = tags_in(l)
        if not tags or not OPEN.search(tags[0]): continue
        # walk forward to the closer or the next structural opener
        between = []; closed = False
        for j in range(i + 1, min(i + 40, len(lines))):
            l2 = lines[j]
            if not l2.strip(): continue
            t2 = tags_in(l2)
            if t2 and CLOSE.search(t2[0]): closed = True; break
            if t2 and any(CLOSE.search(t) for t in t2): closed = True; break
            if "[end supervisor note]" in l2.lower() or "[end of supervisor note]" in l2.lower(): closed = True; break
            if t2 and STRUCT.search(t2[0]) and not t2[0].startswith("[body") and not t2[0].startswith("[list") and not t2[0].startswith("[link"):
                break
            between.append((t2[0] if t2 else "black"))
        key = "closed+items" if (closed and between) else "closed+empty" if closed else "open+items" if between else "open+empty"
        for k in ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subject}"): WT[k][key] += 1
        if closed and between: WTm[f"tmpl+subj={tf}/{subject}"].add(code)
        if closed and between and len(EX) < 8: EX.append(f"{code} L{i+1}: {Counter(between).most_common(3)}")
print("==== (1) WT census — every [Supervisor note] opener: explicit closer? items between? ====")
for k in sorted(WT, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    tot = sum(WT[k].values())
    if tot < 3 and not k.startswith("ALL") and not k.startswith("template"): continue
    print(f"   {k:44s} n={tot:3d}  {dict(WT[k])}  mods(closed+items)={len(WTm.get(k, set()))}")
print("   examples:"); [print("     ", e) for e in EX]

# (2) paired
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
TEXT_TAGS = ("h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "td", "th", "b", "strong", "a", "span", "label")
def fold(t): return re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig
def subtree_end(L, i):
    d = L[i].depth; j = i + 1
    while j < len(L) and L[j].depth > d: j += 1
    return j
P = defaultdict(Counter); Pp = defaultdict(set); Pm = defaultdict(set); EXP = []
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subject}")
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        # gold: fold(text) -> "panel" if inside a div.row.super-content subtree (non-activity: the row.supervisor form), else "free"
        g_where = {}
        panel_ranges = []
        for i, l in enumerate(g):
            if l.sig.startswith("div.row.super-content"): panel_ranges.append((i, subtree_end(g, i)))
        for i, l in enumerate(g):
            if l.text and tag_of(l.sig) in TEXT_TAGS:
                inside = any(a < i < b for a, b in panel_ranges)
                g_where.setdefault(fold(l.text), "panel" if inside else "free")
        # claude: each top-level div.row.supervisor (depth 2) — the first text of the NEXT top-level row
        bi = next((i for i, l in enumerate(c) if l.sig.startswith("div#body")), None)
        if bi is None: continue
        base = c[bi].depth
        rows = [i for i in range(bi + 1, len(c)) if c[i].depth == base + 1 and c[i].sig.startswith("div.row")]
        for ri, r in enumerate(rows[:-1]):
            if not c[r].sig.startswith("div.row.supervisor"): continue
            # skip activity-owned panels (a div.activity inside)
            end = subtree_end(c, r)
            if any(c[k].sig.startswith("div.activity") for k in range(r + 1, end)): continue
            nr = rows[ri + 1]; nend = subtree_end(c, nr)
            ft = None; fsig = None
            for k in range(nr + 1, nend):
                if c[k].text and tag_of(c[k].sig) in TEXT_TAGS: ft = fold(c[k].text); fsig = c[k].sig; break
                if c[k].sig.startswith(("div.activity", "div.alert", "WIDGET", "div.row.supervisor", "h1", "h2", "h3", "h4")): fsig = c[k].sig; break
            if ft is None: verdict = "next=opener/none"
            else:
                w = g_where.get(ft)
                verdict = "gold-nowhere" if w is None else ("GOLD-IN-PANEL (Claude free)" if w == "panel" else "gold-free (Claude right)")
            for k in keys: P[k][verdict] += 1
            if verdict.startswith("GOLD") or verdict.startswith("gold-free"):
                Pp[keys[2]].add(os.path.basename(cp)); Pm[keys[2]].add(code); Pp["ALL"].add(os.path.basename(cp)); Pm["ALL"].add(code)
            if verdict.startswith("GOLD") and len(EXP) < 8: EXP.append(f"{os.path.basename(cp)[:-5]} next=«{(ft or '')[:40]}»")
print("\n==== (2) PAIRED — after a Claude non-activity supervisor panel row, the next row's first prose: inside the gold's panel? ====")
D = "GOLD-IN-PANEL (Claude free)"; A = "gold-free (Claude right)"
for k in sorted(P, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    cnt = P[k]; dis = cnt.get(D, 0); ag = cnt.get(A, 0)
    if dis + ag == 0: continue
    print(f"   {k:44s} in-panel {dis:3d} / free {ag:3d} = {dis/(dis+ag):.2f}  pages {len(Pp.get(k, set()))} / mods {len(Pm.get(k, set()))}  [{ {kk: v for kk, v in cnt.items() if kk not in (D, A)} }]")
print("   examples:"); [print("     ", e) for e in EXP]
