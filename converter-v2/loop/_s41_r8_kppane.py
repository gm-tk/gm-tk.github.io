#!/usr/bin/env python3
"""Session 41 Round 8 — WHICH PANE holds the Knowledge / Practices sections, gold vs Claude, per module; plus the WT's own
"CS: … the Knowledge and Practices into Tab 2 - Information" instruction (present / absent) and the WT's heading tag form.
Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, glob, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
KP = re.compile(r"^(?:year\s+\d+\s+|level\s+\d+\s+)?(knowledge|practices?)\s*:?\s*$", re.I)
HEAD = re.compile(r"<(h[2-6])[^>]*>(.*?)</\1>|<p>\s*<(?:b|strong)>(.*?)</(?:b|strong)>\s*</p>", re.S | re.I)
def panes(p):
    s = open(p, encoding="utf-8", errors="replace").read()
    m = re.search(r'id="module-menu-content"(.*?)<div id="body"', s, re.S)
    if not m: return None
    blk = m.group(1)
    ul = re.search(r'<ul class="nav nav-tabs">(.*?)</ul>', blk, re.S)
    tabs = [H.unescape(re.sub(r"<[^>]+>", "", t)).strip() for t in re.findall(r"<li[^>]*>(.*?)</li>", ul.group(1), re.S)] if ul else []
    parts = re.split(r'<div class="tab-pane[^"]*"[^>]*>', blk)
    where = {}
    if len(parts) > 1:
        for i, part in enumerate(parts[1:]):
            for h in HEAD.finditer(part):
                t = H.unescape(re.sub(r"<[^>]+>", "", h.group(2) or h.group(3) or "")).strip()
                k = KP.match(t)
                if k: where.setdefault("K" if k.group(1).lower().startswith("k") else "P", tabs[i] if i < len(tabs) else f"pane{i}")
    else:
        for h in HEAD.finditer(blk):
            t = H.unescape(re.sub(r"<[^>]+>", "", h.group(2) or h.group(3) or "")).strip()
            k = KP.match(t)
            if k: where.setdefault("K" if k.group(1).lower().startswith("k") else "P", "(no tabs)")
    return tabs, where
def first(d, code):
    c = sorted(glob.glob(os.path.join(d, f"{code}_0_0.html"))) or sorted(glob.glob(os.path.join(d, "*_0_0.html"))) or sorted(glob.glob(os.path.join(d, "*.html")))
    return c[0] if c else None
def label(where, tabs):
    k = where.get("K"); p = where.get("P")
    if not (k or p): return "none"
    v = k or p
    if KP.match(v or ""): return "OWN-TAB"
    if v == "(no tabs)": return "no-tabs-menu"
    return "pane:" + ("tab1" if tabs and v == tabs[0] else v)
cls = collections.Counter(); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    gp, cp = first(hd, code), first(cd, code)
    if not (gp and cp): continue
    g = panes(gp); c = panes(cp)
    if not g or not c: continue
    gl, cl = label(g[1], g[0]), label(c[1], c[0])
    if gl == "none" and cl == "none": continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower()]
    wt = open(wts[0], encoding="utf-8", errors="replace").read() if wts else ""
    instr = "INSTR-Info" if re.search(r"knowledge.{0,6}and.{0,6}practices.{0,40}tab\s*2", wt, re.I | re.S) else "no-instr"
    key = f"gold {gl:22s} claude {cl:14s} {instr}"
    cls[key] += 1; ex[key].append(code)
for k, n in sorted(cls.items(), key=lambda x: -x[1]): print(f"{n:4d} {k} :: {' '.join(ex[k])[:300]}")
