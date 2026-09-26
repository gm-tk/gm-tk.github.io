#!/usr/bin/env python3
"""_s51_r6_headco.py — session 51 Round 6 PICK: red spans pairing a HEADING tag ([H1]–[H6]) with any other bracket, grouped by the
other tag words; for each, the title (black tail) — is it a heading (h1–h6) in the gold (any page of the module) and in Claude?
WSL, from reference/tests/."""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd()); sys.path.append("../../outputs")
import _corpus
import _placement_census as PC
from anchor_compare import CLAUDE, HUMAN

SPAN = re.compile(r"🔴\[RED TEXT\]((?:\s*\[[^\]]*\]?)+)\s*\[/RED TEXT\]🔴\s*([^🔴\n]*)")
HD = re.compile(r"\[\s*h[1-6]\s*\]", re.I)
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\*", "", t.lower())).split())
agg = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    if not w: continue
    txt = open(w[0], encoding="utf-8", errors="replace").read()
    gb = cb = None
    for m in SPAN.finditer(txt):
        tags = m.group(1)
        if not HD.search(tags): continue
        others = [re.sub(r"\d+[a-z]?", "N", fold(x)) for x in re.findall(r"\[([^\]]*)\]?", tags) if not re.fullmatch(r"\s*h[1-6]\s*", x, re.I)]
        others = [o for o in others if o]
        if not others: continue
        title = fold(m.group(2))
        if len(title.split()) < 2: continue
        key = " + ".join(sorted(set(o.split()[0] for o in others)))[:40]
        if gb is None:
            gb = [b for f in sorted(glob.glob(os.path.join(gd, "*.html"))) for b in PC.parse(f)]
            cd = _corpus.mdir(CLAUDE, code)
            cb = [b for f in sorted(glob.glob(os.path.join(cd, "*.html"))) for b in PC.parse(f)] if os.path.isdir(cd) else []
        gh = any(re.match(r"h[1-6]$", b[0]) and PC.jacc(b[1], title) >= 0.6 for b in gb)
        ch = any(re.match(r"h[1-6]$", b[0]) and PC.jacc(b[1], title) >= 0.6 for b in cb)
        agg[key][("G" if gh else "g") + ("C" if ch else "c")] += 1; mods[key].add(code)
        if gh and not ch and len(ex[key]) < 3: ex[key].append(f"{code}: {tags.strip()[:40]} {m.group(2)[:40]}")
print("key: GC = heading in both; Gc = gold heading, Claude not; gC / gc")
for k, c in sorted(agg.items(), key=lambda kv: -kv[1]["Gc"]):
    if c["Gc"] < 3: continue
    print(f"{k:40s} mods={len(mods[k]):3d} GC {c['GC']:4d} Gc {c['Gc']:4d} gC {c['gC']:4d} gc {c['gc']:4d}   e.g. {(ex[k] or [''])[0]}")
