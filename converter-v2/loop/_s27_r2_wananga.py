#!/usr/bin/env python3
"""Session 27 Round 2 candidate — THE WĀNANGA / TALANOA BOX. The CED Phase-5 writers type `[Wānanga/Talanoa box]` (+ variants)
followed by a ONE-CELL table holding the prompt; the KB (05B Cultural Alert, 14A CED: 'all alerts are combined unless otherwise
specified') and the gold render `<div class="alert cultural" layout="combined"><div class="row"><div class="col-12"><p>…`.
Over every module whose WT carries the tag: each site → the text → the gold page's wrapper for that text → Claude's wrapper.
  wsl: python3 _s27_r2_wananga.py → _s27_r2_wananga.out"""
import os, sys, re, glob
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
TAG = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]]*(?:wananga|wānanga|wanana|wananaga|talanoa)[^\]]*)\]\s*(.*?)\[/RED TEXT\]🔴\s*(.*)$", re.I)
def fold(t): return re.sub(r"\W+", " ", t.lower()).strip()
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    pref = [f for f in fs if "writers template" in f.lower()] or fs
    return open(os.path.join(d, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
def wrapper_for(html, key):
    """the nearest enclosing div class chain (last 3 opened divs still open) at the first occurrence of key (folded search)"""
    text = re.sub(r"<[^>]+>", "\x00", html)
    # build a map from folded text to html index: simpler — search the html for the first 40 chars of key with tags stripped
    # approach: strip tags into a parallel string with index map
    out = []; idx = []
    i = 0; n = len(html)
    while i < n:
        if html[i] == "<":
            j = html.find(">", i)
            if j < 0: break
            i = j + 1; out.append(" "); idx.append(i); continue
        out.append(html[i]); idx.append(i); i += 1
    s = "".join(out)
    sf = re.sub(r"\W+", " ", s.lower())
    # index map for folded is lossy; instead search raw stripped text with whitespace-insensitive regex
    words = key.split()[:6]
    pat = r"\W+".join(re.escape(w) for w in words)
    m = re.search(pat, s, re.I)
    if not m: return None, None
    pos = idx[m.start()]
    # walk back over the html collecting open divs
    stack = []
    for t in re.finditer(r"<(/?)div\b([^>]*)>", html[:pos]):
        if t.group(1):
            if stack: stack.pop()
        else:
            c = re.search(r'class="([^"]*)"', t.group(2)); l = re.search(r'layout="([^"]*)"', t.group(2))
            stack.append((c.group(1) if c else "") + (f"[layout={l.group(1)}]" if l else ""))
    return " › ".join(stack[-4:]), pos
codes = ["CEDK501", "CEDO501", "CEDO502", "CEDR501", "CEDT501", "CEDW501", "SSOG301"]
GOLD = Counter(); CL = Counter(); PAIR = Counter(); FORMS = Counter(); rows = []
gpages = set(); cpages = set()
for code in codes:
    lines = wt_lines(code)
    gd = _corpus.mdir(HUMAN, code); cd = _corpus.mdir(CLAUDE, code)
    gh = {f: open(os.path.join(gd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(gd) if f.endswith(".html")}
    ch = {f: open(os.path.join(cd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(cd) if f.endswith(".html")} if os.path.isdir(cd) else {}
    for i, l in enumerate(lines):
        m = TAG.search(l)
        if not m: continue
        bracket = m.group(1).strip(); tail = (m.group(2) + " " + m.group(3)).strip()
        FORMS[re.sub(r"\s+", " ", bracket.lower())] += 1
        # the content: the tail if long enough, else the first table cell / paragraph after
        content = tail if len(tail.split()) >= 4 else ""
        shape = "tail"
        if not content:
            for k in range(i + 1, min(i + 12, len(lines))):
                s = lines[k].strip()
                if not s or s.startswith("┌") or s.startswith("└") or s.startswith("[IMAGE"): continue
                if s.startswith("│"):
                    content = s.lstrip("│").strip().split(" / ")[0]; shape = "table"; break
                if s.startswith("🔴[RED TEXT]"):
                    shape = "next-tag"; break
                content = s; shape = "black"; break
        key = re.sub(r"\*\*|\*", "", content)[:120]
        gw = cw = None; gp = cp = None
        for f, h in gh.items():
            w, pos = wrapper_for(h, key)
            if w is not None: gw, gp = w, f; break
        for f, h in ch.items():
            w, pos = wrapper_for(h, key)
            if w is not None: cw, cp = w, f; break
        gk = ("alert cultural" if gw and "alert cultural" in gw else ("whakatauki" if gw and "whakatauki" in gw else ("alert" if gw and "alert" in gw.split(" › ")[-1] else (gw or "NOT FOUND"))))
        ck = ("table" if cw and "table-responsive" in cw else ("wananga" if cw and "wananga" in cw else ("alert" if cw and "alert" in cw.split(" › ")[-1] else (cw or "NOT FOUND"))))
        GOLD[gk] += 1; CL[ck] += 1; PAIR[(gk, ck)] += 1
        if gp: gpages.add(code + "/" + gp)
        if cp: cpages.add(code + "/" + cp)
        rows.append(f"{code} L{i+1} [{bracket[:40]}] shape={shape} gold={gk} ({gp}) claude={ck} ({cp}) «{key[:50]}»")
out = []
def P(s=""): out.append(s); print(s)
P(f"tag sites: {sum(FORMS.values())} over {len(codes)} modules; gold pages holding a matched site {len(gpages)}; Claude pages {len(cpages)}")
P("bracket forms: " + "; ".join(f"[{k}] {v}" for k, v in FORMS.most_common()))
P("gold wrapper: " + "; ".join(f"{k} {v}" for k, v in GOLD.most_common()))
P("claude wrapper: " + "; ".join(f"{k} {v}" for k, v in CL.most_common()))
P("paired: " + "; ".join(f"gold {g} → claude {c} {v}" for (g, c), v in PAIR.most_common()))
for r in rows: P("  " + r)
open(os.path.join(OUTPUTS, "_s27_r2_wananga.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
