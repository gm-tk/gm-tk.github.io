#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE EMPTY [alert] (120 flags / 94 pages / 49 modules). For every WT line that is a bare callout
tag (alert / important / whakatauki / quote family) with NO tail, classify the NEXT non-blank WT item (a [body] tag line, a [list],
a table, an image, a heading, black text, another tag) and, for the text of that next item, what the gold ships: the same words
INSIDE an alert-family box (which class) / outside / not found — and what Claude ships (inside a box / outside).
  wsl: python3 _s27_r3_emptyalert.py → _s27_r3_emptyalert.out"""
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
CALL = re.compile(r"^(alert|important)\b", re.I)
TAGLINE = re.compile(r"^🔴\[RED TEXT\]\s*\[([^\]]*)\]\s*\[/RED TEXT\]🔴\s*(.*)$")
def fold(t): return re.sub(r"\W+", " ", t.lower()).strip()
def wrapper_for(html, key):
    words = re.sub(r"[•\*]", " ", key).split()[:6]
    if len(words) < 3: return None
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
    pos = idx[m.start()]
    stack = []
    for t in re.finditer(r"<(/?)div\b([^>]*)>", html[:pos]):
        if t.group(1):
            if stack: stack.pop()
        else:
            c = re.search(r'class="([^"]*)"', t.group(2)); stack.append(c.group(1) if c else "")
    return stack
def box_of(stack):
    if stack is None: return "NOT FOUND"
    for c in reversed(stack[-4:]):
        toks = set(c.split())
        if "alert" in toks or "alertActivity" in toks or "important" in toks: return " ".join(sorted(toks))
    return "outside"
NEXT = Counter(); GOLD = defaultdict(Counter); CL = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list); BYG = defaultdict(Counter)
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
        nl = lines[k]
        if nl.startswith("┌"):
            kind = "table"; text = lines[k + 1].lstrip("│").strip() if k + 1 < len(lines) else ""
        elif nl.startswith("[IMAGE"):
            kind = "image-inline"; text = ""
        else:
            tm = TAGLINE.match(nl.strip())
            if tm:
                tag = re.sub(r"\s+", " ", tm.group(1).strip().lower()); tail = tm.group(2).strip()
                head = tag.split()[0] if tag else "?"
                kind = "[" + re.sub(r"\d+[a-z]?", "N", head) + "]" + ("+tail" if tail else "")
                text = tail if tail else ""
                if not tail:
                    # the content is on the line after that tag
                    kk = k + 1
                    while kk < len(lines) and not lines[kk].strip(): kk += 1
                    text = lines[kk].strip() if kk < len(lines) and not lines[kk].startswith("🔴") and not lines[kk].startswith("┌") else ""
            else:
                kind = "black"; text = nl.strip()
        NEXT[kind] += 1
        key = text[:120]
        if gh is None:
            gh = {f: open(os.path.join(gd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(gd) if f.endswith(".html")}
            ch = {f: open(os.path.join(cd, f), encoding="utf-8", errors="replace").read() for f in os.listdir(cd) if f.endswith(".html")} if os.path.isdir(cd) else {}
        gb = "NOT FOUND"; cb = "NOT FOUND"; gp = None
        for f, h in gh.items():
            st = wrapper_for(h, key)
            if st is not None: gb = box_of(st); gp = f; break
        for f, h in ch.items():
            st = wrapper_for(h, key)
            if st is not None: cb = box_of(st); break
        GOLD[kind][gb] += 1; CL[kind][cb] += 1; BYG[(g, kind)][gb] += 1
        if gp: pages[kind].add(code + "/" + gp)
        mods[kind].add(code)
        if len(EX[(kind, gb)]) < 3: EX[(kind, gb)].append(f"{code} L{i+1} [{m.group(1)[:20]}] next «{key[:45]}» claude={cb}")
out = []
def P(s=""): out.append(s); print(s)
P("bare callout tag (no tail) → next item kind: " + "; ".join(f"{k} {v}" for k, v in NEXT.most_common(14)))
P()
P("==== per next-item kind (n ≥ 8): the gold's wrapper for the next item's text; Claude's ====")
for kind, v in NEXT.most_common():
    if v < 8: continue
    P(f"   {kind:18s} n={v:4d} pages {len(pages[kind]):3d} mods {len(mods[kind]):3d} | gold: " + "  ".join(f"{k} {c}" for k, c in GOLD[kind].most_common(4)) + " | claude: " + "  ".join(f"{k} {c}" for k, c in CL[kind].most_common(3)))
P()
P("==== per group × kind (n ≥ 10) ====")
for (g, kind), c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values())):
    t = sum(c.values())
    if t < 10: continue
    P(f"   {g:42s} {kind:14s} n={t:3d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(4)))
P()
for key, ex in list(EX.items())[:24]:
    for e in ex: P(f"   {key}: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_emptyalert.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
