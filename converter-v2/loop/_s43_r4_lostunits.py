#!/usr/bin/env python3
"""Session 43 Round 4 PICK — CONTENT THE CONVERTER DROPS, by WHOLE UNIT (the shingle probes over-count at item boundaries: a bullet
list Claude lays out in two columns breaks every cross-bullet shingle). A UNIT is one Writers Template line's BLACK text (red spans,
[tags], URLs removed), split at the writer's " / "; >= 5 words. The gold CARRIES it when >= 0.8 of its 4-word shingles are on the
gold's pages outside the acknowledgements; Claude carries it when >= 0.5 are on any Claude page or in the {CODE}_interactives.txt
worklist. LOST = the gold carries it and Claude does not. Aggregated by the writer tag at / above the unit (within 10 lines), with
per-family counts and examples. Run under WSL from CONVERTER_V2/reference/tests:
    python3 ../../outputs/_s43_r4_lostunits.py [TAG-SUBSTRING] > ../../outputs/_s43_r4_lostunits.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
RED = re.compile(r"🔴\[RED TEXT\].*?\[/RED TEXT\]🔴", re.S)
TAG = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]\[]{1,50})\]")
def norm(s):
    s = html.unescape(s).lower()
    s = re.sub(r"[‘’“”'\"`*_]", "", s)
    s = re.sub(r"[^0-9a-zāēīōū]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()
def page_text(p, ackcut):
    s = open(p, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    if ackcut: s = re.split(r"<[^>]+class=\"[^\"]*acks", s)[0]
    return re.sub(r"<[^>]+>", " ", s)
def sh(w, k=4): return {" ".join(w[i:i + k]) for i in range(max(1, len(w) - k + 1))}
WANT = sys.argv[1].lower() if len(sys.argv) > 1 else None
agg = collections.Counter(); mods = collections.defaultdict(set); pages = collections.defaultdict(set)
fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); tot_units = tot_lost = 0
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower() or "writers template" in f.lower()]
    if not wts: continue
    lines = []
    for f in wts: lines += open(f, encoding="utf-8", errors="replace").read().splitlines()
    gw = norm(" ".join(page_text(p, True) for p in glob.glob(os.path.join(hd, "*.html"))))
    ct = " ".join(page_text(p, False) for p in glob.glob(os.path.join(cd, "*.html")))
    ct += " " + " ".join(open(p, encoding="utf-8", errors="replace").read() for p in glob.glob(os.path.join(cd, "*_interactives.txt")))
    cw = norm(RED.sub(" ", ct))
    G, C = sh(gw.split()), sh(cw.split())
    for li, line in enumerate(lines):
        for part in RED.sub(" ", line).split(" / "):
            t = norm(re.sub(r"https?://\S+", " ", re.sub(r"\[[^\]]{0,80}\]", " ", part)))
            w = t.split()
            if len(w) < 5: continue
            s4 = sh(w)
            if sum(x in G for x in s4) / len(s4) < 0.8: continue            # the gold does not carry it (as written)
            tot_units += 1
            if sum(x in C for x in s4) / len(s4) >= 0.5: continue           # Claude carries it
            tag = None
            for j in range(li, max(-1, li - 11), -1):
                m = TAG.search(lines[j])
                if m: tag = re.sub(r"\d+", "N", m.group(1).strip().lower()[:30]); break
            tag = tag or "(no tag within 10 lines)"
            if WANT and WANT not in tag: continue
            tot_lost += 1
            agg[tag] += 1; mods[tag].add(code); fam[tag][re.match(r"[A-Z]+", code).group(0)] += 1
            if len(ex[tag]) < 4: ex[tag].append(f"{code} L{li + 1}: {' '.join(w[:14])}")
print(f"units the gold carries {tot_units}; lost by Claude {tot_lost} ({tot_lost / max(1, tot_units):.3f})")
print("tag | lost units | modules | families | examples")
for t, n in sorted(agg.items(), key=lambda kv: -kv[1])[:45]:
    print(f"{t:30s} | {n:5d} | {len(mods[t]):4d} | {dict(fam[t].most_common(5))} | {' ;; '.join(ex[t])[:300]}")
