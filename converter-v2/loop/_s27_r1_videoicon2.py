#!/usr/bin/env python3
"""Session 27 Round 1 — the videoSection `icon` class, part 2: the GATE-VISIBLE slice (contexts the scaffold skeleton keeps:
free body / activity box / panel / clickDropContent / TKmodal — carousel / accordion / tabs / flip collapse to WIDGET) of the
paired gold-icon / Claude-plain mismatch, per subject|template group and per series, with the reverse count (gold plain
where a group rule would add icon) so each candidate group's NET effect is known before any code.
  wsl: python3 _s27_r1_videoicon2.py → _s27_r1_videoicon2.out"""
import os, sys, re, json
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
DATA = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
rule = json.load(open(os.path.join(DATA, "Emit_Templates.json"), encoding="utf-8"))["video"]["icon_rule"]
ICON_SERIES = set(rule["icon_series"]); ICON_ST = set(rule["icon_subject_template"])
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
def series_of(code):
    m = meta.get(code, {}) or {}; s = m.get("series")
    if not s:
        g = re.match(r"^([A-Za-z]+)(\d+)", code); s = g.group(1) + g.group(2)[:2] if g else None
    return s
def st_of(code):
    m = meta.get(code, {}) or {}
    return f"{m.get('subject')}|{m.get('template_type')}" if m.get("subject") and m.get("template_type") else None
def in_registry(code): return series_of(code) in ICON_SERIES or (st_of(code) in ICON_ST)
TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I); CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "audio"}
COLLAPSE = {"carousel", "accordion", "tabs", "flipCard", "clickDrop", "hintSlider", "modal", "cv2-interactive", "speechBubble", "dragAndDrop", "multiChoiceQuiz", "dropQuiz", "typing"}
def videos(src):
    st = []; out = []
    for m in TAG.finditer(src):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); toks = set((c.group(1) if c else "").split())
        hidden = bool(toks & COLLAPSE)
        if "videoSection" in toks:
            out.append(("icon" in toks, any(st)))   # (icon?, inside a collapsed widget?)
        st.append(hidden)
    return out
rows = []   # (code, page, gI, gP, cI, cP) VISIBLE videos only
for code in sorted(fam):
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gv = [v for v in videos(body_source(open(hp, encoding="utf-8", errors="replace").read())) if not v[1]]
            cv = [v for v in videos(body_source(open(cp, encoding="utf-8", errors="replace").read())) if not v[1]]
        except Exception: continue
        if not gv and not cv: continue
        rows.append((code, os.path.basename(cp), sum(1 for v in gv if v[0]), sum(1 for v in gv if not v[0]), sum(1 for v in cv if v[0]), sum(1 for v in cv if not v[0])))
out = []
def P(s=""): out.append(s); print(s)
# per group: gold visible icon/plain (paired pages), the gate-visible mismatch both ways, pages, modules
def agg(keyf, title, floor_n, floor_s):
    A = defaultdict(lambda: Counter()); mods = defaultdict(set); pages_sub = defaultdict(set); mods_sub = defaultdict(set)
    for code, pg, gI, gP, cI, cP in rows:
        k = keyf(code)
        if not k: continue
        A[k]["gI"] += gI; A[k]["gP"] += gP; A[k]["cI"] += cI; A[k]["cP"] += cP; mods[k].add(code)
        s_ip = min(max(0, gI - cI), max(0, cP - gP)); s_pi = min(max(0, gP - cP), max(0, cI - gI))
        A[k]["sub_ip"] += s_ip; A[k]["sub_pi"] += s_pi
        if s_ip: pages_sub[k].add(code + pg); mods_sub[k].add(code)
    P(f"==== {title} — gate-VISIBLE videos on paired pages: gold icon / plain, Claude icon / plain, the same-page substitutions (gold icon→Claude plain | gold plain→Claude icon) ====")
    for k, c in sorted(A.items(), key=lambda kv: -kv[1]["sub_ip"]):
        n = len(mods[k]); share = c["gI"] / max(1, c["gI"] + c["gP"])
        reg = (k in ICON_SERIES) if title.startswith("series") else (k in ICON_ST)
        tag = "IN-REGISTRY" if reg else ("SOLIDIFIES" if (n >= floor_n and share >= floor_s) else "")
        if c["sub_ip"] + c["sub_pi"] >= 5 or reg or tag:
            P(f"   {k:40s} gold {c['gI']:4d}/{c['gP']:4d} ({share:.2f}, n={n:3d})  claude {c['cI']:4d}/{c['cP']:4d}  sub icon→plain {c['sub_ip']:4d} on {len(pages_sub[k]):3d} pp / {len(mods_sub[k]):3d} mods  plain→icon {c['sub_pi']:3d}  {tag}")
agg(st_of, "subject|template", 5, 0.80)
P()
agg(series_of, "series", 3, 0.85)
P()
# NCEA1|Standard by series
P("==== NCEA1|Standard by series (visible videos): gold icon/plain, the substitutions ====")
B = defaultdict(Counter); bm = defaultdict(set); bp = defaultdict(set)
for code, pg, gI, gP, cI, cP in rows:
    if st_of(code) != "NCEA1|Standard": continue
    k = series_of(code); B[k]["gI"] += gI; B[k]["gP"] += gP; bm[k].add(code)
    s_ip = min(max(0, gI - cI), max(0, cP - gP)); B[k]["sub_ip"] += s_ip
    if s_ip: bp[k].add(code + pg)
for k, c in sorted(B.items(), key=lambda kv: -(kv[1]["gI"] + kv[1]["gP"])):
    P(f"   {k:10s} gold {c['gI']:3d}/{c['gP']:3d} ({c['gI']/max(1,c['gI']+c['gP']):.2f}, n={len(bm[k])})  sub icon→plain {c['sub_ip']:3d} on {len(bp[k])} pp   {'IN-REGISTRY' if k in ICON_SERIES else ''}")
tot_ip = sum(min(max(0, gI - cI), max(0, cP - gP)) for code, pg, gI, gP, cI, cP in rows)
P(f"\nTOTAL gate-visible gold-icon→Claude-plain substitutions: {tot_ip}; registry modules {sum(min(max(0, gI - cI), max(0, cP - gP)) for code, pg, gI, gP, cI, cP in rows if in_registry(code))}")
open(os.path.join(OUTPUTS, "_s27_r1_videoicon2.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump(rows, open(os.path.join(OUTPUTS, "_s27_r1_videoicon2.json"), "w"))
