#!/usr/bin/env python3
"""Session 45 Round 2 — the hover / rollover DEFINITION markers, by shape: for every marker in every Writers Template of the scored
population whose head is hover / rollover / roll over / mouseover (the scanner's head_pattern), classify its shape — NAMED-FOR
('[rollover definition for TERM: DEF]' — the unquoted named anchor), QUOTED ('[hover info ‘TERM’: DEF]'), COLON (a bare colon def),
OTHER — and check whether its DEFINITION reaches Claude's pages as an info= attribute and the gold's pages as one (the first 25 letters
of the def, normalised). Also: for the NAMED-FOR shape, whether the TERM is in the preceding 1 / 2 / 3 non-empty WT lines, and the gold's
anchor choice (first vs last occurrence of the term in the paragraph that carries the span).
WSL, from outputs/: python3 _s45_r2_hover.py > _s45_r2_hover.log"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
def n(t): return re.sub(r"[^a-z0-9ā-ž ]+", "", re.sub(r"\s+", " ", H.unescape(t).lower())).strip()
def nz(t): return n(t).replace(" ", "")
HEAD = re.compile(r"\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\b", re.I)
FOR = re.compile(r"^\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\s*(?:-?\s*over)?\s*(?:definition|def|text|info)?\s*(?:for|of|on)\s+([^:\]]{1,40}?)\s*:\s*([^\]]+)\]?", re.I)
QUOTED = re.compile(r"^\[[^\]:]*?['‘\"]([^'’\"‘\]]+)['’\"][^:\]]*:\s*([^\]]+)", re.I)
COLON = re.compile(r"^\[[^\]:]*:\s*([^\]]+)")
# the NAMED-BARE form: head keyword(s) + 'definition' + TERM + ':' (HIS1006 '[roll over definition mamae: painful…]')
NAMED = re.compile(r"^\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\s*(?:-?\s*over)?\s*(?:definition|def)\s*[-–]?\s+([^:\]]{1,40}?)\s*:\s*([^\]]+)\]?", re.I)
def info_attrs(d):
    out = []
    for p in glob.glob(os.path.join(d, "*.html")):
        s = io.open(p, encoding="utf-8", errors="replace").read()
        out += [nz(m) for m in re.findall(r'info="([^"]*)"', s)]
    return out
shape = collections.Counter(); reach = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set)
ex = collections.defaultdict(list); look = collections.Counter(); fam = collections.defaultdict(collections.Counter)
PER = collections.defaultdict(collections.Counter)
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
    if not wts or not os.path.isdir(cd): continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gi = info_attrs(gd); ci = info_attrs(cd)
    for k, ln in enumerate(lines):
        raw = RED.sub("", ln)
        m0 = HEAD.search(raw)
        if not m0: continue
        mk = re.sub(r"\s+", " ", raw[m0.start():]).strip()
        pre = raw[:m0.start()].strip()
        mf = FOR.match(mk); mq = QUOTED.match(mk); mc = COLON.match(mk)
        mn = NAMED.match(mk) if not mf else None
        if re.search(r"\btrigger\b", mk, re.I): sh = "TRIGGER"
        elif mf: sh = "NAMED-FOR"
        elif mn and not mq: sh = "NAMED-BARE"; mf = mn
        elif mq: sh = "QUOTED"
        elif mc: sh = "COLON" + ("-inline" if pre else "-standalone")
        else: sh = "OTHER"
        d = (mf.group(2) if mf else mq.group(2) if mq else mc.group(1) if mc else "")
        dk = nz(d)[:22]
        g = "gold" if dk and any(dk in x for x in gi) else "gold-no"
        c = "claude" if dk and any(dk in x for x in ci) else "claude-no"
        shape[sh] += 1; reach[sh][(g, c)] += 1; mods[sh].add(code); PER[(sh, g, c)][code] += 1
        fam[sh][re.match(r"[A-Z]+", code).group(0)] += 1
        if len(ex[(sh, g, c)]) < 4: ex[(sh, g, c)].append(f"{code} «{mk[:90]}»")
        if mf:
            term = n(mf.group(1)); prev = [n(RED.sub("", l)) for l in lines[max(0, k - 12):k] if n(RED.sub("", l)) and not HEAD.search(RED.sub("", l))][-3:]
            pos = next((j for j, pl in enumerate(reversed(prev)) if re.search(r"(?:^| )" + re.escape(term) + r"(?: |$)", pl)), None)
            look[("inline-pre" if pre and term in n(pre) else f"prev{pos + 1}" if pos is not None else "not-in-3")] += 1
print("markers by shape (modules):")
for sh, v in shape.most_common():
    print(f"  {v:5d} {len(mods[sh]):3d}m {sh:18s} " + " | ".join(f"{a}/{b} {x}" for (a, b), x in reach[sh].most_common()))
    print(f"        families: {dict(fam[sh].most_common(8))}")
print("\nNAMED-FOR: where the TERM is (the preceding non-marker WT lines):", dict(look))
print("\nexamples:")
for k, v in sorted(ex.items()):
    print(f"  {k}: " + " || ".join(v[:3]))
print("\nper module — gold builds it, Claude does not:")
for sh in ("NAMED-FOR", "NAMED-BARE", "COLON-inline", "TRIGGER", "QUOTED"):
    c = PER[(sh, "gold", "claude-no")]
    print(f"  {sh:14s} {sum(c.values()):4d}: {dict(c.most_common(20))}")
