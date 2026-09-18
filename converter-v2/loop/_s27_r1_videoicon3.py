#!/usr/bin/env python3
"""Session 27 Round 1 — the videoSection `icon` registry: SIMULATE the candidate re-mine designs on the gate-visible
paired videos (_s27_r1_videoicon2.json rows: code, page, gold icon, gold plain, Claude icon, Claude plain) and report,
per design: the modules that flip to icon / to plain, the NET matched-line change vs today's output, pages / modules touched.
Designs (a cascade: series first, then subject|template; a group solidifies ICON at share >= s_icon, PLAIN at share <= s_plain):
  A  r200 as written, re-mined: series n>=3 s_icon 0.85; st n>=5 s_icon 0.80; no plain carve-out
  A' A + plain-series carve-out (series n>=3 at share <= 0.40 stays plain even inside an icon st group)
  B  series n>=2 s_icon 0.85 / plain <= 0.40; st n>=5 s_icon 0.80
  C  series n>=2 s_icon 0.85 / plain <= 0.40; st n>=5 s_icon 0.60 (the loop's §1b bar)
  wsl: python3 _s27_r1_videoicon3.py → _s27_r1_videoicon3.out"""
import os, sys, re, json
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
DATA = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/pageforge-site/converter-v2/data'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _measure_ceiling import load_meta
from collections import Counter, defaultdict
meta = load_meta()
rule = json.load(open(os.path.join(DATA, "Emit_Templates.json"), encoding="utf-8"))["video"]["icon_rule"]
ICON_SERIES = set(rule["icon_series"]); ICON_ST = set(rule["icon_subject_template"])
rows = json.load(open(os.path.join(OUTPUTS, "_s27_r1_videoicon2.json")))
def series_of(code):
    m = meta.get(code, {}) or {}; s = m.get("series")
    if not s:
        g = re.match(r"^([A-Za-z]+)(\d+)", code); s = g.group(1) + g.group(2)[:2] if g else None
    return s
def st_of(code):
    m = meta.get(code, {}) or {}
    return f"{m.get('subject')}|{m.get('template_type')}" if m.get("subject") and m.get("template_type") else None
def cur_icon(code): return series_of(code) in ICON_SERIES or (st_of(code) in ICON_ST)
# per-module gold totals (visible, paired) — the mining population is the GOLD of every paired module
gm = defaultdict(lambda: [0, 0]); pages_of = defaultdict(set)
for code, pg, gI, gP, cI, cP in rows:
    gm[code][0] += gI; gm[code][1] += gP; pages_of[code].add(pg)
# the MINING population = every gold video incl. the widget-embedded ones (the r200 rule mined all videos)
full = json.load(open(os.path.join(OUTPUTS, "_s27_r1_videoicon.json")))
gfull = {c: (sum(v["gi"].values()), sum(v["gp"].values())) for c, v in full.items()}
def group_stats(keyf):
    a = defaultdict(lambda: [0, 0, 0])
    for code, (gI, gP) in gfull.items():
        k = keyf(code)
        if not k or gI + gP == 0: continue
        a[k][0] += gI; a[k][1] += gP; a[k][2] += 1
    return {k: (v[0] / (v[0] + v[1]), v[2], v[0], v[1]) for k, v in a.items()}
S = group_stats(series_of); ST = group_stats(st_of)
def design(n_series, s_icon_series, s_plain_series, n_st, s_icon_st, carve):
    icon_series = ICON_SERIES | {k for k, (sh, n, a, b) in S.items() if n >= n_series and sh >= s_icon_series}
    plain_series = ({k for k, (sh, n, a, b) in S.items() if n >= n_series and sh <= s_plain_series} - ICON_SERIES) if carve else set()
    icon_st = ICON_ST | {k for k, (sh, n, a, b) in ST.items() if n >= n_st and sh >= s_icon_st}
    def new_icon(code):
        s = series_of(code)
        if s in icon_series: return True
        if s in plain_series: return False
        return st_of(code) in icon_st
    return icon_series, plain_series, icon_st, new_icon
out = []
def P(s=""): out.append(s); print(s)
DESIGNS = [
    ("A  r200 re-mined (series n>=3 @0.85; st n>=5 @0.80; no carve-out)", (3, 0.85, -1, 5, 0.80, False)),
    ("A' r200 re-mined + plain-series carve-out (series n>=3 @<=0.40 plain)", (3, 0.85, 0.40, 5, 0.80, True)),
    ("B  series n>=2 @0.85 / plain <=0.40; st n>=5 @0.80", (2, 0.85, 0.40, 5, 0.80, True)),
    ("C  series n>=2 @0.85 / plain <=0.40; st n>=5 @0.60", (2, 0.85, 0.40, 5, 0.60, True)),
]
for title, args in DESIGNS:
    icon_series, plain_series, icon_st, new_icon = design(*args)
    net = 0; to_icon = []; to_plain = []; pages = set(); mods = set(); gain = loss = 0
    for code, (gI, gP) in gm.items():
        if gI + gP == 0: continue
        c, n = cur_icon(code), new_icon(code)
        if c == n: continue
        # today's output: a registry module ships icon everywhere (visible); a non-registry one ships plain
        d = (gI - gP) if n else (gP - gI)
        net += d; (to_icon if n else to_plain).append((code, gI, gP)); pages |= {code + p for p in pages_of[code]}; mods.add(code)
        gain += (gI if n else gP); loss += (gP if n else gI)
    P(f"==== {title} ====")
    P(f"   icon_series +{sorted(icon_series - ICON_SERIES)}  -{sorted(ICON_SERIES - icon_series)}")
    P(f"   plain_series {sorted(plain_series)}")
    P(f"   icon_st +{sorted(icon_st - ICON_ST)}  -{sorted(ICON_ST - icon_st)}")
    P(f"   modules flipping to ICON {len(to_icon)}, to PLAIN {len(to_plain)}; pages touched {len(pages)}; NET matched lines {net:+d} (lines newly right {gain} / newly wrong {loss})")
    P("   to icon: " + ", ".join(f"{c}({a}/{b})" for c, a, b in sorted(to_icon)))
    P("   to plain: " + ", ".join(f"{c}({a}/{b})" for c, a, b in sorted(to_plain)))
    P()
open(os.path.join(OUTPUTS, "_s27_r1_videoicon3.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
