#!/usr/bin/env python3
"""Session 42 Round 10 — each dumped two-column dragAndDrop table (`_s42_r10_dd2dump.json`) matched to the gold's dragAndDrop widget on
the paired page with the most cell-token overlap; the gold form (layout, drop-column count, drop / drag counts, the drop-column
headings) cross-tabbed against writer features: HEAD = the first row's two cells carry a heading tag (`[H3]`/`[H4]`/…) or are both
short labels (≤ 6 words, no red answer marks); INSTR = the instruction's words (column / sort / categor / group vs match / pair);
CELLS = every data cell plain (no red, no URL, no [tag]). Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, json, collections, html as H
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA
O = os.path.join("..", "..", "outputs")
D = json.load(open(os.path.join(O, "_s42_r10_dd2dump.json")))
def toks(s): return set(w for w in re.sub(r"[^a-z0-9āēīōū ]", " ", H.unescape(re.sub(r"<[^>]+>", " ", s)).lower()).split() if len(w) > 1)
pairs = {}
def gold_page(code, label):
    if code not in pairs:
        pairs[code] = {}
        try:
            for _, cp, hp in DA.pairs(code):
                m = re.match(r".*_(\d+)_(\d+)\.html$", os.path.basename(cp))
                if m: pairs[code][f"{int(m.group(1))}.{int(m.group(2))}"] = hp
        except Exception: pass
    return pairs[code].get(label)
def widgets(s):
    out = []
    for m in re.finditer(r'<div class="dragAndDrop[^"]*"[^>]*>', s):
        st = m.start(); depth = 0; end = len(s)
        for t in re.finditer(r"<(/?)div\b[^>]*>", s[st:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: end = st + t.end(); break
        out.append((m.group(0), s[st:end]))
    return out
def feats(b):
    rows = b["rows"]; r0 = rows[0] if rows else ["", ""]
    head_tag = all(re.search(r"«\s*\[h\d\]\s*»", c, re.I) for c in r0 if c) and any(r0)
    short = all(c and len(re.sub(r"«[^»]*»", "", c).split()) <= 6 and "«" not in re.sub(r"«\s*\[h\d\]\s*»", "", c) for c in r0)
    data = rows[1:]
    plain = all(("«" not in c and "http" not in c) for r in data for c in r)
    instr = " ".join(b["lines"]).lower()
    iw = "col" if re.search(r"column|sort|categor|group|correct (box|side)", instr) else ("match" if re.search(r"match|pair|connect", instr) else "-")
    return ("HEADTAG" if head_tag else ("SHORTHEAD" if short else "nohead")), iw, ("plain" if plain else "marked"), len(data)
cross = collections.Counter(); ex = collections.defaultdict(list)
for b in D:
    hp = gold_page(b["code"], b["page"])
    f = feats(b)
    if not hp:
        cross[(f[0], f[1], f[2], "NO-PAIR")] += 1; continue
    s = open(hp, encoding="utf-8", errors="replace").read()
    cells = set().union(*[toks(c) for r in b["rows"][1:] for c in r]) if len(b["rows"]) > 1 else set()
    best, bw = 0, None
    for head, w in widgets(s):
        ov = len(cells & toks(w)) / max(1, len(cells))
        if ov > best: best, bw = ov, (head, w)
    if not bw or best < 0.3:
        g = "NO-GOLD-DD"
    else:
        head, w = bw
        lay = re.search(r'layout="([^"]+)"', head); lay = lay.group(1) if lay else "standard"
        dc = re.search(r'<div class="row dropContainer">(.*?)<div class="row dragContainer">', w, re.S)
        ncol = len(re.findall(r'<div class="ddColumn"', dc.group(1))) if dc else 0
        g = f"{lay}/{ncol}col" if lay == "column" else lay
    key = (f[0], f[1], f[2], g); cross[key] += 1
    if len(ex[key]) < 4: ex[key].append(f"{b['code']} {b['page']}#{b['index']} rows={f[3]} r0={b['rows'][0] if b['rows'] else ''}"[:170])
print(f"{len(D)} dumped two-column bundles")
for k, n in sorted(cross.items(), key=lambda x: -x[1]):
    print(f"{n:4d}  head={k[0]:9s} instr={k[1]:5s} cells={k[2]:6s} → gold {k[3]}")
    for e in ex[k][:2]: print("         ", e)
