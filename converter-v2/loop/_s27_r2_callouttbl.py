#!/usr/bin/env python3
"""Session 27 Round 2 — every CALLOUT tag (alert / important / wananga / whakatauki / quote / side alert …) typed with NO tail and
followed directly by a ONE-CELL table (the WT's boxed-prompt idiom): per tag, what wrapper the gold gives the cell's text
(a kept <table>? the callout box with <p>s?) and what Claude gives it. Over every module with a parsed WT.
  wsl: python3 _s27_r2_callouttbl.py → _s27_r2_callouttbl.out"""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
import _corpus
from _measure_ceiling import load_meta
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
TAG = re.compile(r"^🔴\[RED TEXT\]\s*\[([^\]]*)\]\s*\[/RED TEXT\]🔴\s*$")
CALL = re.compile(r"^(alert|important|wananga|wānanga|talanoa|whakatauki|whakatauaki|quote|side alert|banner - w)", re.I)
def wrapper_for(html, key):
    out = []; idx = []; i = 0; n = len(html)
    while i < n:
        if html[i] == "<":
            j = html.find(">", i)
            if j < 0: break
            i = j + 1; out.append(" "); idx.append(i); continue
        out.append(html[i]); idx.append(i); i += 1
    s = "".join(out)
    words = re.sub(r"[•\*]", " ", key).split()[:6]
    if len(words) < 3: return None
    pat = r"\W+".join(re.escape(w) for w in words)
    m = re.search(pat, s, re.I)
    if not m: return None
    pos = idx[m.start()]
    stack = []
    for t in re.finditer(r"<(/?)(div|table)\b([^>]*)>", html[:pos]):
        if t.group(1):
            if stack: stack.pop()
        else:
            c = re.search(r'class="([^"]*)"', t.group(3))
            stack.append(t.group(2) + ("." + c.group(1).replace(" ", ".") if c else ""))
    return " › ".join(stack[-3:])
def kind(w):
    if w is None: return "NOT FOUND"
    last = w.split(" › ")[-1] if w else ""
    if "table" in w: return "kept table"
    if "alert.cultural" in w: return "alert cultural"
    if "whakatauki" in w: return "whakatauki"
    if "wananga" in w: return "wananga"
    for k in ("alert.solid", "alert.top", "alertActivity", "alert"):
        if re.search(r"(^|\.| › )" + re.escape(k) + r"(\.|$| › )", w): return k.replace(".", " ")
    if "cv2-interactive" in w: return "cv2 box"
    return "plain (" + last[:30] + ")"
BY = defaultdict(Counter); PAIR = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
codes = sorted(set(os.listdir(os.path.join(CLAUDE, tf))) if os.path.isdir(os.path.join(CLAUDE, tf)) else set() for tf in _corpus.TEMPLATE_DIRS) if False else None
allc = []
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d): allc += os.listdir(d)
for code in sorted(allc):
    try:
        gd = _corpus.mdir(HUMAN, code); cd = _corpus.mdir(CLAUDE, code)
        fs = sorted(f for f in os.listdir(gd) if f.endswith("_parsed.txt"))
        pref = [f for f in fs if "writers template" in f.lower()] or fs
        if not pref: continue
        lines = open(os.path.join(gd, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
    except Exception: continue
    gh = ch = None
    for i, l in enumerate(lines):
        m = TAG.match(l.strip())
        if not m: continue
        br = m.group(1).strip().lower()
        if not CALL.match(br): continue
        tagk = "wananga" if re.match(r"(wananga|wānanga|talanoa|banner - w)", br) else ("whakatauki" if br.startswith("whakatau") else ("side alert" if br.startswith("side") else br.split(".")[0].split(" ")[0]))
        # next non-blank line must open a table; take its first cell line
        k = i + 1
        while k < len(lines) and not lines[k].strip(): k += 1
        if k >= len(lines) or not lines[k].startswith("┌"): continue
        cell = lines[k + 1] if k + 1 < len(lines) else ""
        if not cell.startswith("│"): continue
        nrows = 0; kk = k + 1
        while kk < len(lines) and lines[kk].startswith("│"): nrows += 1; kk += 1
        ncells = cell.count("║") + 1
        if nrows != 1 or ncells != 1: continue
        key = cell.lstrip("│").strip().split(" / ")[0]
        if gh is None:
            gh = {f: open(os.path.join(gd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(gd) if f.endswith(".html")}
            ch = {f: open(os.path.join(cd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(cd) if f.endswith(".html")} if os.path.isdir(cd) else {}
        gw = None
        for f, h in gh.items():
            w = wrapper_for(h, key)
            if w is not None: gw = w; pages[tagk].add(code + "/" + f); break
        cw = None
        for f, h in ch.items():
            w = wrapper_for(h, key)
            if w is not None: cw = w; break
        gk, ck = kind(gw), kind(cw)
        subj = (meta.get(code, {}) or {}).get("subject") or "None"
        BY[tagk][gk] += 1; PAIR[tagk][(gk, ck)] += 1; mods[tagk].add(code)
        if len(EX[(tagk, gk)]) < 3: EX[(tagk, gk)].append(f"{code} L{i+1} [{br[:30]}] gold={gw} claude={cw} «{key[:40]}»")
out = []
def P(s=""): out.append(s); print(s)
for tagk in sorted(BY, key=lambda t: -sum(BY[t].values())):
    t = sum(BY[tagk].values())
    P(f"== [{tagk}] + one-cell table: {t} sites / {len(mods[tagk])} modules / {len(pages[tagk])} gold pages")
    P("   gold: " + "; ".join(f"{k} {v} ({v/t:.2f})" for k, v in BY[tagk].most_common()))
    P("   paired: " + "; ".join(f"gold {g} → claude {c} {v}" for (g, c), v in PAIR[tagk].most_common(8)))
    for (tk, gk), ex in EX.items():
        if tk == tagk:
            for e in ex: P("      " + e)
open(os.path.join(OUTPUTS, "_s27_r2_callouttbl.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
