#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE BARE [alert] + HEADING idiom: `[Alert Box]` on its own line, then `[H3] Title` + prose.
Claude: an EMPTY alert box (red flag) and the heading + prose outside it. The gold? For each site: the gold's wrapper chain at the
HEADING text (exact heading match, any hN) and at the first prose paragraph; Claude's; by template/subject.
  wsl: python3 _s27_r3_alerthead.py → _s27_r3_alerthead.out"""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
BARE = re.compile(r"^🔴\[RED TEXT\]\s*\[([^\]]*)\]\s*\[/RED TEXT\]🔴\s*$")
HEAD = re.compile(r"^🔴\[RED TEXT\]\s*\[(h[1-5]|heading|activity heading)[^\]]*\]\s*\[/RED TEXT\]🔴\s*(.+)$", re.I)
CALL = re.compile(r"^(alert|important)\b", re.I)
def fold(t): return re.sub(r"\W+", " ", re.sub(r"\*+", "", t).lower()).strip()
HTAG = re.compile(r"<(h[1-6])[^>]*>(.*?)</\1>", re.S)
def chain_at(html, pos):
    stack = []
    for t in re.finditer(r"<(/?)div\b([^>]*)>", html[:pos]):
        if t.group(1):
            if stack: stack.pop()
        else:
            c = re.search(r'class="([^"]*)"', t.group(2)); stack.append(c.group(1) if c else "")
    return stack
def box_of(stack):
    for c in reversed(stack[-5:]):
        toks = set(c.split())
        if toks & {"alert", "alertActivity", "important", "alertImage"}: return " ".join(sorted(toks))
    return "outside"
def find_heading(html, ftxt):
    for m in HTAG.finditer(html):
        if fold(re.sub(r"<[^>]+>", " ", m.group(2))) == ftxt:
            return m.group(1), box_of(chain_at(html, m.start()))
    return None
def find_para(html, key):
    words = key.split()[:7]
    if len(words) < 4: return None
    out = []; idx = []; i = 0; n = len(html)
    while i < n:
        if html[i] == "<":
            j = html.find(">", i)
            if j < 0: break
            i = j + 1; out.append(" "); idx.append(i); continue
        out.append(html[i]); idx.append(i); i += 1
    s = "".join(out)
    m = re.search(r"\W+".join(re.escape(w) for w in words), s, re.I)
    if not m: return None
    return box_of(chain_at(html, idx[m.start()]))
R = Counter(); BYG = defaultdict(Counter); pages = set(); mods = set(); EX = defaultdict(list); CLR = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    try:
        gd = _corpus.mdir(HUMAN, code); cd = _corpus.mdir(CLAUDE, code)
        fs = sorted(f for f in os.listdir(gd) if f.endswith("_parsed.txt"))
        pref = [f for f in fs if "writers template" in f.lower()] or fs
        if not pref: continue
        lines = open(os.path.join(gd, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
    except Exception: continue
    gh = ch = None
    for i, l in enumerate(lines):
        m = BARE.match(l.strip())
        if not m or not CALL.match(m.group(1).strip()): continue
        k = i + 1
        while k < len(lines) and not lines[k].strip(): k += 1
        if k >= len(lines): continue
        hm = HEAD.match(lines[k].strip())
        if not hm: continue
        htxt = fold(hm.group(2))
        # first prose line after the heading
        kk = k + 1
        while kk < len(lines) and not lines[kk].strip(): kk += 1
        prose = ""
        if kk < len(lines):
            pl = lines[kk].strip()
            pm = re.match(r"^🔴\[RED TEXT\]\s*\[[^\]]*\]\s*\[/RED TEXT\]🔴\s*(.*)$", pl)
            prose = fold(pm.group(1)) if pm else (fold(pl) if not pl.startswith("┌") else "")
        if gh is None:
            gh = {f: open(os.path.join(gd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(gd) if f.endswith(".html")}
            ch = {f: open(os.path.join(cd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(cd) if f.endswith(".html")} if os.path.isdir(cd) else {}
        gres = None; gp = None; gpro = None
        for f, h in gh.items():
            r = find_heading(h, htxt)
            if r: gres = r; gp = f; gpro = find_para(h, prose) if prose else None; break
        cres = None; cpro = None
        for f, h in ch.items():
            r = find_heading(h, htxt)
            if r: cres = r; cpro = find_para(h, prose) if prose else None; break
        gk = (f"{gres[0]} in {gres[1]}" if gres else "heading not found") + (f" / prose in {gpro}" if gpro else "")
        ck = (f"{cres[0]} in {cres[1]}" if cres else "heading not found") + (f" / prose in {cpro}" if cpro else "")
        R[(gk, ck)] += 1; BYG[g][gk] += 1; mods.add(code)
        if gp: pages.add(code + "/" + gp)
        if len(EX[(gk, ck)]) < 2: EX[(gk, ck)].append(f"{code} L{i+1} [{m.group(1)[:24]}] + [{hm.group(1)}] «{htxt[:30]}»")
out = []
def P(s=""): out.append(s); print(s)
P(f"bare [alert]/[important] + heading sites: {sum(R.values())} / {len(mods)} modules / gold pages found {len(pages)}")
P("==== gold (heading level in box / prose in box) → Claude ====")
for (gk, ck), v in R.most_common(25): P(f"   {v:4d}  gold {gk:40s} → claude {ck}")
P()
P("==== per group (n ≥ 6): the gold form ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 6: continue
    P(f"   {g:42s} n={t:3d}  " + "  ".join(f"[{k}] {v} ({v/t:.2f})" for k, v in c.most_common(4)))
P()
for key, ex in list(EX.items())[:16]:
    for e in ex: P(f"   {key}: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_alerthead.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
