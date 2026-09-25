#!/usr/bin/env python3
"""Session 46 Round 9 — every COLON-inline hover marker the gold builds as an info= and Claude does not (the s45-r2 (a) residue):
where does the definition go on Claude's side? For each: module, the WT line, and WHERE the def's first words sit in Claude's html —
an info= attribute elsewhere (a different anchor), a hand-off box (cv2-int-raw), a cv2-note, plain text (a <p>/<li>/<td>), or NOWHERE.
WSL, from outputs/: python3 _s46_r9_colon.py > _s46_r9_colon.log"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
def n(t): return re.sub(r"[^a-z0-9ā-ž ]+", "", re.sub(r"\s+", " ", H.unescape(t).lower())).strip()
def nz(t): return n(t).replace(" ", "")
HEAD = re.compile(r"\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\b", re.I)
FOR = re.compile(r"^\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\s*(?:-?\s*over)?\s*(?:definition|def|text|info)?\s*(?:for|of|on)\s+([^:\]]{1,40}?)\s*:", re.I)
QUOTED = re.compile(r"^\[[^\]:]*?['‘\"]([^'’\"‘\]]+)['’\"][^:\]]*:\s*([^\]]+)", re.I)
COLON = re.compile(r"^\[[^\]:]*:\s*([^\]]+)")
NAMED = re.compile(r"^\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\s*(?:-?\s*over)?\s*(?:definition|def)\s*[-–]?\s+([^:\]]{1,40}?)\s*:\s*([^\]]+)\]?", re.I)
def pages(d):
    out = {}
    for p in sorted(glob.glob(os.path.join(d, "*.html"))):
        out[os.path.basename(p)] = io.open(p, encoding="utf-8", errors="replace").read()
    return out
def where(dk, pg):
    """the container of the def's first words in Claude's pages"""
    for name, s in pg.items():
        for m in re.finditer(r'info="([^"]*)"', s):
            if dk in nz(m.group(1)): return name, "info-attr"
        flat = nz(re.sub(r"<[^>]+>", " ", s))
        if dk not in flat: continue
        # locate in raw by walking text nodes
        for m in re.finditer(r">([^<]{3,})<", s):
            if dk[:12] in nz(m.group(1)):
                before = s[:m.start()]
                if before.rfind("cv2-int-raw") > before.rfind("<div class=\"row"): return name, "handoff-box"
                if before.rfind("cv2-note") > max(before.rfind("<p>"), before.rfind("<li>")): return name, "cv2-note"
                tag = re.findall(r"<(\w+)[^>]*>\s*$", before[-200:])
                return name, "text:" + (tag[-1] if tag else "?")
        return name, "text:split"
    return "-", "NOWHERE"
res = collections.Counter(); rows = []
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
    if not wts or not os.path.isdir(cd): continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gp = pages(gd); cp = pages(cd)
    gi = [nz(m) for s in gp.values() for m in re.findall(r'info="([^"]*)"', s)]
    ci = [nz(m) for s in cp.values() for m in re.findall(r'info="([^"]*)"', s)]
    for ln in lines:
        raw = RED.sub("", ln)
        for m0 in HEAD.finditer(raw):
            mk = re.sub(r"\s+", " ", raw[m0.start():]).strip(); pre = raw[:m0.start()].strip()
            if re.search(r"\btrigger\b", mk[:40], re.I) or FOR.match(mk) or QUOTED.match(mk) or NAMED.match(mk): continue
            mc = COLON.match(mk)
            if not mc or not pre: continue
            dk = nz(mc.group(1))[:22]
            if not dk or not any(dk in x for x in gi) or any(dk in x for x in ci): continue
            pg, w = where(dk, cp)
            res[w] += 1
            rows.append((code, pg, w, re.sub(r"\s+", " ", raw.strip())[:230]))
            break
print("COLON-inline, gold builds / Claude not — where the def is on Claude's side:", dict(res.most_common()))
for r in rows: print(f"  {r[0]:9s} {r[1]:22s} {r[2]:14s} «{r[3]}»")
