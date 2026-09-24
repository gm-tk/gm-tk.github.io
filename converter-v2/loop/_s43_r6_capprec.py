#!/usr/bin/env python3
"""Session 43 Round 6 PICK — the PRECISION side of a c41 rule: every plain <p> on a Claude page that follows an <img> (directly, or with
only a comment / closing divs between), split by its word count, matched by text on the paired gold page: the gold's form
(p.captionText / plain p / another tag / absent). A rule "a short <p> right after an image is its caption" is safe only where the gold
says captionText for nearly all of them. Also split by what the WT line carries (the [caption]-less forms: the image line's own tail /
the next untagged line). Run under WSL from reference/tests: python3 ../../outputs/_s43_r6_capprec.py > …log"""
import os, re, sys, collections, html
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
def norm(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)).lower(); s = re.sub(r"[‘’“”'\"`*_]", "", s)
    return re.sub(r"\s+", " ", re.sub(r"[^0-9a-zāēīōū]+", " ", s)).strip()
P = re.compile(r"<(p|h[1-6]|li|td|th)\b([^>]*)>(.*?)</\1>", re.S | re.I)
def gold_forms(s):
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S); out = {}
    for m in P.finditer(s):
        cls = re.search(r'class="([^"]*)"', m.group(2)); t = norm(m.group(3))
        if t and t not in out: out[t] = m.group(1).lower() + ("." + ".".join(cls.group(1).split()) if cls else "")
    return out
agg = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    for _k, cp, gp in pairs(code):
        try:
            cs = open(cp, encoding="utf-8", errors="replace").read(); gs = open(gp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        GF = gold_forms(gs)
        live = re.sub(r"<!--.*?-->", "", cs, flags=re.S)
        for m in re.finditer(r"<img\b[^>]*>\s*(?:</div>\s*)*<p(\s[^>]*)?>(.*?)</p>", live, re.S):
            attrs = m.group(1) or ""
            if "class=" in attrs: continue                                   # already classed (captionText, cv2-note …)
            t = norm(m.group(2)); n = len(t.split())
            if not t: continue
            band = "1-6" if n <= 6 else "7-15" if n <= 15 else "16-30" if n <= 30 else "31+"
            g = GF.get(t)
            if g is None: g = next((v for k, v in GF.items() if t in k and len(k) < len(t) * 1.5), "absent")
            gk = "p.captionText" if g.startswith("p") and "captionText" in g else ("p plain" if g == "p" else g.split(".")[0] if g != "absent" else "absent")
            agg[(band, gk)] += 1; mods[(band, gk)].add(code)
            if len(ex[(band, gk)]) < 3: ex[(band, gk)].append(f"{code}: «{t[:50]}»")
print("words | gold form | Claude plain p after img | modules | examples")
for band in ("1-6", "7-15", "16-30", "31+"):
    tot = sum(v for (b, _), v in agg.items() if b == band)
    for (b, gk), v in sorted(agg.items(), key=lambda kv: -kv[1]):
        if b != band: continue
        print(f"{band:5s} | {gk:14s} | {v:5d} ({v / max(1, tot):.2f}) | {len(mods[(b, gk)]):4d} | {' ;; '.join(ex[(b, gk)])[:160]}")
