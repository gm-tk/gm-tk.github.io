#!/usr/bin/env python3
"""Session 27 Round 1 candidate — THE videoSection `icon` CLASS, re-measured on the r397 corpus.
The r200 rule (Emit_Templates.video.icon_rule) adds `icon` per SERIES / SUBJECT|TEMPLATE group mined on 392 modules and
leaves every widget-embedded video plain (the r200 recorded follow-up). This probe, over the gate's own pairs:
  (1) per module: the gold's icon share, by CONTEXT (free body / activity box / carousel item / accordion / tab / clickDrop);
  (2) the r200 solidify test re-run on today's gold (series n>=3 at share>=0.85; subject|template n>=5 at share>=0.80) —
      which groups solidify now, which registry groups still hold;
  (3) the paired per-page mismatch: gold icon vs Claude icon at the same context, split registry-module / not.
  wsl: python3 _s27_r1_videoicon.py → _s27_r1_videoicon.out"""
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
    m = meta.get(code, {}) or {}
    s = m.get("series")
    if not s:
        g = re.match(r"^([A-Za-z]+)(\d+)", code)
        s = g.group(1) + g.group(2)[:2] if g else None
    return s
def st_of(code):
    m = meta.get(code, {}) or {}
    return f"{m.get('subject')}|{m.get('template_type')}" if m.get("subject") and m.get("template_type") else None
def in_registry(code):
    return series_of(code) in ICON_SERIES or (st_of(code) in ICON_ST)

TAG = re.compile(r"<(/?)([a-z][a-z0-9]*)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
VOID = {"br", "img", "input", "hr", "meta", "link", "source", "wbr", "audio"}
CTX_CLASSES = [("carousel", "item"), ("accordion", "accContent"), ("tabs", "tab-pane"), ("clickDrop", "clickDropContent"),
               ("flip", "flipCardsContainer"), ("activity", "activity"), ("modal", "TKmodal"), ("panel", "inquiryPanel"), ("panel", "fundamentalsPanel"), ("box", "cv2-interactive")]
def videos(src):
    """every videoSection div with (icon?, context) — context = the innermost enclosing widget/box kind, else 'free'."""
    st = []; out = []
    for m in TAG.finditer(src):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag in VOID and not closing: continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); toks = set((c.group(1) if c else "").split())
        kind = next((k for k, cl in CTX_CLASSES if cl in toks), None)
        if "videoSection" in toks:
            ctx = next((e for e in reversed(st) if e), "free")
            out.append(("icon" in toks, ctx))
        st.append(kind)
    return out

per_mod = {}   # code -> dict
page_rows = []
for code in sorted(fam):
    gi = Counter(); gp = Counter(); ci = Counter(); cp_ = Counter()
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gv = videos(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            cv = videos(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        g_by = defaultdict(lambda: [0, 0]); c_by = defaultdict(lambda: [0, 0])
        for ic, ctx in gv: g_by[ctx][0 if ic else 1] += 1; (gi if ic else gp)[ctx] += 1
        for ic, ctx in cv: c_by[ctx][0 if ic else 1] += 1; (ci if ic else cp_)[ctx] += 1
        page_rows.append((code, os.path.basename(cp), dict(g_by), dict(c_by)))
    if sum(gi.values()) + sum(gp.values()) == 0: continue
    per_mod[code] = {"gi": gi, "gp": gp, "ci": ci, "cp": cp_, "reg": in_registry(code), "series": series_of(code), "st": st_of(code), "tf": fam[code]}

out = []
def P(s=""): out.append(s); print(s)
P(f"video-carrying paired modules: {len(per_mod)}; in the r200 registry: {sum(1 for v in per_mod.values() if v['reg'])}")
# (1) purity
pure_icon = pure_plain = mixed = 0
for v in per_mod.values():
    a, b = sum(v["gi"].values()), sum(v["gp"].values())
    if b == 0: pure_icon += 1
    elif a == 0: pure_plain += 1
    else: mixed += 1
P(f"gold purity per module: all-icon {pure_icon} / all-plain {pure_plain} / mixed {mixed}")
# by context, corpus-wide
G = Counter(); Gp = Counter()
for v in per_mod.values(): G.update(v["gi"]); Gp.update(v["gp"])
P("gold icon share by CONTEXT (all modules): " + "; ".join(f"{k} {G[k]}/{G[k]+Gp[k]} ({G[k]/max(1,G[k]+Gp[k]):.2f})" for k in sorted(set(G)|set(Gp), key=lambda k: -(G[k]+Gp[k]))))
Gr = Counter(); Gpr = Counter()
for v in per_mod.values():
    if v["reg"]: Gr.update(v["gi"]); Gpr.update(v["gp"])
P("gold icon share by CONTEXT (REGISTRY modules): " + "; ".join(f"{k} {Gr[k]}/{Gr[k]+Gpr[k]} ({Gr[k]/max(1,Gr[k]+Gpr[k]):.2f})" for k in sorted(set(Gr)|set(Gpr), key=lambda k: -(Gr[k]+Gpr[k]))))
Gn = Counter(); Gpn = Counter()
for v in per_mod.values():
    if not v["reg"]: Gn.update(v["gi"]); Gpn.update(v["gp"])
P("gold icon share by CONTEXT (NON-registry modules): " + "; ".join(f"{k} {Gn[k]}/{Gn[k]+Gpn[k]} ({Gn[k]/max(1,Gn[k]+Gpn[k]):.2f})" for k in sorted(set(Gn)|set(Gpn), key=lambda k: -(Gn[k]+Gpn[k]))))
P()
# (2) the solidify test re-run
P("==== the r200 solidify test on today's gold — pooled icon share per group (n modules) ====")
def group_rows(keyf, nmin, smin, title):
    agg = defaultdict(lambda: [0, 0, 0]); mods = defaultdict(list)
    for code, v in per_mod.items():
        k = keyf(v)
        if not k: continue
        agg[k][0] += sum(v["gi"].values()); agg[k][1] += sum(v["gp"].values()); agg[k][2] += 1; mods[k].append(code)
    P(f"-- {title} (solidify: n>={nmin}, share>={smin}) --")
    for k, (a, b, n) in sorted(agg.items(), key=lambda kv: -(kv[1][0] + kv[1][1])):
        share = a / max(1, a + b)
        reg = (k in ICON_SERIES) if title.startswith("series") else (k in ICON_ST)
        solid = n >= nmin and share >= smin
        flag = "IN-REGISTRY" if reg else ("SOLIDIFIES-NOW" if solid else "")
        if reg or solid or a + b >= 20:
            P(f"   {k:40s} icon {a:4d} / plain {b:4d}  share {share:.2f}  n={n:3d}  {flag}")
group_rows(lambda v: v["series"], 3, 0.85, "series")
group_rows(lambda v: v["st"], 5, 0.80, "subject|template")
P()
# (3) paired mismatch
P("==== paired per-page mismatch (same context): gold icon vs Claude icon ====")
def mism(sel):
    sub = Counter(); pages = set(); mods = set(); ctxc = Counter()
    for code, pg, g_by, c_by in page_rows:
        if code not in per_mod or not sel(per_mod[code]): continue
        for ctx in set(g_by) | set(c_by):
            gI, gP = g_by.get(ctx, [0, 0]); cI, cP = c_by.get(ctx, [0, 0])
            # substitution = gold has icon where Claude has plain (min of the two surpluses)
            s_ip = min(max(0, gI - cI), max(0, cP - gP)); s_pi = min(max(0, gP - cP), max(0, cI - gI))
            if s_ip: sub["gold icon / Claude plain"] += s_ip; pages.add(pg + code); mods.add(code); ctxc[ctx] += s_ip
            if s_pi: sub["gold plain / Claude icon"] += s_pi; pages.add(pg + code); mods.add(code)
    return sub, len(pages), len(mods), ctxc
for title, sel in (("REGISTRY modules", lambda v: v["reg"]), ("NON-registry modules", lambda v: not v["reg"])):
    sub, np_, nm, ctxc = mism(sel)
    P(f"   {title}: {dict(sub)} on {np_} pages / {nm} modules; gold-icon/Claude-plain by context {dict(ctxc)}")
open(os.path.join(OUTPUTS, "_s27_r1_videoicon.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
json.dump({c: {"gi": dict(v["gi"]), "gp": dict(v["gp"]), "ci": dict(v["ci"]), "cp": dict(v["cp"]), "reg": v["reg"], "series": v["series"], "st": v["st"], "tf": v["tf"]} for c, v in per_mod.items()},
          open(os.path.join(OUTPUTS, "_s27_r1_videoicon.json"), "w"), indent=0)
