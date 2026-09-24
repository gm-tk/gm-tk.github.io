#!/usr/bin/env python3
"""Session 43 Round 6 PICK — KB constraint 41 (captionText): a <p> whose sole purpose is to caption the image next to it carries
class="captionText", in every context. For every gold `p.captionText` (paired pages, the gate population): its text, what precedes it
on the gold page (an <img> / a widget / other), the SAME text on the paired Claude page — its element (`p.captionText` / plain `p` /
another tag / absent) and whether an <img> sits immediately before it on Claude's page — and the Writers Template line that carries
it (its tag: [caption] / [image] line / untagged, and whether the line before it is an image line). Run under WSL from
CONVERTER_V2/reference/tests: python3 ../../outputs/_s43_r6_caption.py > ../../outputs/_s43_r6_caption.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)).lower(); s = re.sub(r"[‘’“”'\"`*_]", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zāēīōū]+", " ", s)).strip()
BLOCK = re.compile(r"<(p|h[1-6]|li|td|th|figcaption)\b([^>]*)>(.*?)</\1>", re.S | re.I)   # never div: a lazy div match swallows the <p>s inside it
def elements(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    out = []
    for m in BLOCK.finditer(s):
        cls = re.search(r'class="([^"]*)"', m.group(2)); inner = m.group(3)
        if m.group(1).lower() == "div" and re.search(r"<(p|div|h\d|ul|ol|table)\b", inner): continue
        before = s[max(0, m.start() - 400): m.start()]
        prev_img = bool(re.search(r"<img\b[^>]*>\s*(?:<!--.*?-->\s*)?(?:</div>\s*)*$", re.sub(r"<!--.*?-->", "", before), re.S))
        out.append((m.group(1).lower(), cls.group(1) if cls else "", norm(inner), prev_img))
    return out
agg = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); pgs = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd = _corpus.mdir(HUMAN, code)
    wtl = []
    for f in glob.glob(os.path.join(hd, "*_parsed.txt")):
        if "media list_parsed" in f.lower() and "writers template" not in f.lower(): continue
        wtl += open(f, encoding="utf-8", errors="replace").read().splitlines()
    wtn = [norm(re.sub(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", " ", l)) for l in wtl]
    for _k, cp, gp in pairs(code):
        try:
            G = elements(open(gp, encoding="utf-8", errors="replace").read())
            C = elements(open(cp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        cindex = {}
        for t, cls, txt, pi in C:
            if txt and txt not in cindex: cindex[txt] = (t, cls, pi)
        for t, cls, txt, pi in G:
            if t != "p" or "captionText" not in cls.split() or len(txt.split()) < 2: continue
            c = cindex.get(txt)
            if c is None:
                c = next(((ct, ccls, cpi) for tt, (ct, ccls, cpi) in cindex.items() if txt in tt and len(tt) < len(txt) * 2), None)
            if c is None: cf = "ABSENT"
            elif c[0] == "p" and "captionText" in c[1].split(): cf = "p.captionText"
            elif c[0] == "p": cf = "p (plain)" + (" after img" if c[2] else " NOT after img")
            else: cf = c[0] + ("." + c[1].split()[0] if c[1] else "")
            wt = next((i for i, l in enumerate(wtn) if txt and txt in l), None)
            if wt is None: src = "not in WT"
            else:
                raw = wtl[wt]
                tagm = re.search(r"\[([^\]]{1,30})\]", raw)
                tag = tagm.group(1).strip().lower() if tagm else "untagged"
                prev = next((wtl[j] for j in range(wt - 1, max(-1, wt - 4), -1) if wtl[j].strip()), "")
                previmg = bool(re.search(r"\[\s*image|istockphoto|\.(?:jpe?g|png|gif)\b", prev, re.I))
                src = ("[caption]" if "caption" in tag else ("image-line" if re.search(r"image|istock", raw, re.I) else tag if tag != "untagged" else "untagged")) + (" / after image line" if previmg else "")
            k = (cf, "gold after img" if pi else "gold NOT after img", src)
            agg[k] += 1; mods[k].add(code); pgs[k].add(os.path.basename(gp))
            if len(ex[k]) < 3: ex[k].append(f"{code}: «{txt[:60]}»")
tot = sum(agg.values())
print(f"gold p.captionText on paired pages: {tot}")
print("Claude form | gold context | WT source | n | pages | modules | examples")
for k, n in sorted(agg.items(), key=lambda kv: -kv[1])[:40]:
    print(f"{k[0]:26s} | {k[1]:18s} | {k[2]:32s} | {n:4d} | {len(pgs[k]):4d} | {len(mods[k]):3d} | {' ;; '.join(ex[k])[:200]}")
