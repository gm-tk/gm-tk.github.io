#!/usr/bin/env python3
"""Session 43 Round 5 PICK — THE ACTIVITY BOX OPENED BY A RED JOURNAL INSTRUCTION. The writer types no `[Activity NX]` tag, only a
wholly-red instruction line that NAMES the activity ("[Go to your learning journal and complete activity 3A]." — AGH1002-3.0); Claude
opens `div.activity[number=3A]` there and the box swallows the section that follows ([H3] Respiration …), where the gold's 3A box is
the instruction + the journal button alone. For every such WT line (the id NOT tagged anywhere as `[Activity <id>]` in the module),
find the `number="<id>"` box on Claude's pages and on the gold's, and compare: the box's text length, whether it carries the
instruction's words, and what it opens with. Run under WSL from CONVERTER_V2/reference/tests:
    python3 ../../outputs/_s43_r5_instrbox.py > ../../outputs/_s43_r5_instrbox.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
REDLINE = re.compile(r"^\s*🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴\s*\.?\s*$")
def norm(s):
    s = html.unescape(s).lower(); s = re.sub(r"[‘’“”'\"`*_]", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zāēīōū]+", " ", s)).strip()
def boxes(path):
    """{number: (text, first-heading-or-p)} for every div.activity[number] on the page (balanced div walk)."""
    s = open(path, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    out = {}
    for m in re.finditer(r'<div class="activity[^"]*"[^>]*\bnumber="([^"]+)"[^>]*>', s):
        depth, i = 1, m.end()
        for t in re.finditer(r"<(/?)div\b[^>]*>", s[i:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: inner = s[i:i + t.start()]; break
        else: inner = s[i:i + 4000]
        inner = re.sub(r'<p class="cv2-(?:note|comment)"[^>]*>.*?</p>', " ", inner, flags=re.S)
        first = re.search(r"<(h[1-6]|p|li)\b[^>]*>(.*?)</\1>", inner, flags=re.S)
        txt = norm(re.sub(r"<[^>]+>", " ", inner))
        out.setdefault(m.group(1).strip().upper(), []).append((txt, norm(re.sub(r"<[^>]+>", " ", first.group(2))) if first else "", os.path.basename(path)))
    return out
agg = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); pages = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower() or "writers template" in f.lower()]
    if not wts: continue
    L = []
    for f in wts: L += open(f, encoding="utf-8", errors="replace").read().splitlines()
    tagged = {m.group(1).upper() for l in L for m in re.finditer(r"\[\s*activity\s*:?\s*(\d+[a-z])\b", l, re.I)}
    C, G = {}, {}
    for p in glob.glob(os.path.join(cd, "*.html")):
        for k, v in boxes(p).items(): C.setdefault(k, []).extend(v)
    for p in glob.glob(os.path.join(hd, "*.html")):
        for k, v in boxes(p).items(): G.setdefault(k, []).extend(v)
    for li, line in enumerate(L):
        m = REDLINE.match(line)
        if not m: continue
        body = m.group(1)
        am = re.search(r"\bactivit(?:y|ies)\s+(\d+[a-z])\b", body, re.I)
        if not am or not re.search(r"journal|complete|dropbox|workbook", body, re.I): continue
        aid = am.group(1).upper()
        if aid in tagged: continue                                     # the writer tagged the box elsewhere — not this shape
        instr = norm(re.sub(r"[\[\]]", " ", body))
        iw = set(instr.split())
        def judge(lst):
            if not lst: return "no box"
            txt, first, pg = lst[0]
            carries = len(iw & set(txt.split())) / max(1, len(iw)) >= 0.7
            n = len(txt.split())
            return ("carries instr" if carries else "NO instr") + (" / short" if n <= 40 else " / LONG")
        cj, gj = judge(C.get(aid)), judge(G.get(aid))
        k = (cj, gj); agg[k] += 1; mods[k].add(code)
        if C.get(aid): pages[k].add((code, C[aid][0][2]))
        if len(ex[k]) < 4:
            cf = C[aid][0][1][:60] if C.get(aid) else "-"
            gf = G[aid][0][1][:60] if G.get(aid) else "-"
            ex[k].append(f"{code} {aid}: WT «{instr[:60]}» | Claude opens «{cf}» | gold opens «{gf}»")
print("Claude box | gold box | instructions | modules | Claude pages | examples")
for k, n in sorted(agg.items(), key=lambda kv: -kv[1]):
    print(f"{k[0]:22s} | {k[1]:22s} | {n:4d} | {len(mods[k]):3d} | {len(pages[k]):3d} | " + " ;; ".join(ex[k])[:420])
print("TOTAL", sum(agg.values()))
