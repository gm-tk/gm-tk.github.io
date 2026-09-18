#!/usr/bin/env python3
"""Session 26 Round 6 candidate — ADJACENT SIBLING LISTS: `</ul>` immediately followed by `<ul>` (whitespace only between).
Census over every paired page, LIVE body only (the cv2-interactive hand-off dumps, cv2-note / cv2-comment and the r337
verbatim widget subtrees carved out exactly as TypedNumberList carves them): Claude vs gold, per template / subject.
  python3 _s26_r392_adjul.py"""
import os, sys, re, json
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
DATA = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data/Emit_Templates.json'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
widgets = json.load(open(DATA, encoding="utf-8"))["body_region"]["typed_number_list"]["verbatim_widget_classes"]
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
OPEN = re.compile(r"<div class=\"(?:cv2-interactive|" + "|".join(re.escape(w) for w in widgets) + r")|<p class=\"cv2-(?:note|comment)\"|<script\b|<style\b")
DIVS = re.compile(r"<div\b|</div>")
def live_pieces(src):
    out = []; i = 0
    for m in OPEN.finditer(src):
        j = m.start()
        if j < i: continue
        if m.group(0).startswith("<div"):
            depth = 0; end = len(src)
            for mm in DIVS.finditer(src, j):
                depth += -1 if mm.group(0) == "</div>" else 1
                if depth == 0: end = mm.end(); break
        elif m.group(0).startswith("<p"):
            k = src.find("</p>", j); end = len(src) if k < 0 else k + 4
        else:
            close = "</script>" if m.group(0).startswith("<script") else "</style>"
            k = src.find(close, j); end = len(src) if k < 0 else k + len(close)
        if j > i: out.append(src[i:j])
        i = end
    if i < len(src): out.append(src[i:])
    return out
def body(html):
    m = re.search(r"<div id=\"body\"", html); s = html[m.start():] if m else html
    a = s.find("<div class=\"acks"); return s if a < 0 else s[:a]
ADJ = re.compile(r"</ul>\s*<ul>"); ADJO = re.compile(r"</ol>\s*<ol>")
C = defaultdict(Counter); G = defaultdict(Counter); Cp = defaultdict(set); Cm = defaultdict(set); Gp = defaultdict(set); EX = []
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subj}")
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        c = len(ADJ.findall(cl)); g = len(ADJ.findall(gl)); co = len(ADJO.findall(cl)); go = len(ADJO.findall(gl))
        for k in keys:
            C[k]["ul"] += c; G[k]["ul"] += g; C[k]["ol"] += co; G[k]["ol"] += go
        if c:
            Cp[keys[2]].add(os.path.basename(cp)); Cm[keys[2]].add(code); Cp["ALL"].add(os.path.basename(cp)); Cm["ALL"].add(code)
            if len(EX) < 6:
                m = ADJ.search(cl); EX.append(f"{os.path.basename(cp)[:-5]}: …{cl[max(0, m.start()-90):m.start()].strip()[-80:]} ⟂ {cl[m.end():m.end()+60].strip()[:50]}")
        if g: Gp[keys[2]].add(os.path.basename(hp)); Gp["ALL"].add(os.path.basename(hp))
print("==== adjacent sibling lists in the LIVE body (dumps / notes / verbatim widgets carved out) — Claude vs gold ====")
for k in sorted(C, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), -C[x]["ul"])):
    if C[k]["ul"] + G[k]["ul"] == 0: continue
    print(f"   {k:46s} ul: claude {C[k]['ul']:4d} (pages {len(Cp.get(k, set())):3d} / mods {len(Cm.get(k, set())):3d})  gold {G[k]['ul']:3d} (pages {len(Gp.get(k, set())):2d})   ol: claude {C[k]['ol']} gold {G[k]['ol']}")
print("   examples:"); [print("     ", e) for e in EX]
