#!/usr/bin/env python3
"""Session 27 Round 8 — CLAUDE'S BARE `div.ratio.ratio-16x9` (no videoSection class): the generic-iframe embed wrapper — 133 on 79 pages, gold 0.
For every such site on a paired page: the iframe's src host, and what the gold ships for that URL on the paired page — an iframe (inside which
wrapper class), an anchor / button, or nothing (URL absent). By host and by subject.  wsl: python3 _s27_r8_bareratio.py"""
import os, sys, re
from collections import Counter, defaultdict
from urllib.parse import urlparse
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
RX = re.compile(r'<div class="ratio ratio-16x9">\s*<iframe[^>]*src="([^"]+)"', re.I)
def key(u):
    u = u.strip(); u = re.sub(r"^https?://(www\.)?", "", u); return u.rstrip("/").lower()
C = Counter(); BYH = defaultdict(Counter); BYG = defaultdict(Counter); pages = set(); mods = set(); EX = defaultdict(list); TOT = 0
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        for m in RX.finditer(ch):
            TOT += 1; url = m.group(1); host = urlparse("https://" + key(url)).netloc.split(":")[0]
            k = key(url); kid = re.sub(r"[?#].*$", "", k)
            # the gold: the same url (or its path stem) inside which element?
            gi = None
            for gm in re.finditer(r'<(iframe|a|source)[^>]*(?:src|href)="([^"]+)"', gh, re.I):
                gk = key(gm.group(2))
                if gk == k or (len(kid) > 20 and gk.startswith(kid)) or (len(kid) > 20 and kid.startswith(re.sub(r"[?#].*$", "", gk)) and len(re.sub(r"[?#].*$", "", gk)) > 20):
                    gi = gm; break
            if gi is None: v = "gold:absent"
            elif gi.group(1).lower() == "iframe":
                pre = gh[max(0, gi.start() - 400):gi.start()]
                wm = re.findall(r'class="([^"]*ratio[^"]*)"', pre)
                v = "gold:iframe in " + (wm[-1] if wm else "?")
            else:
                pre = gh[max(0, gi.start() - 60):gi.end() + 120]
                v = "gold:anchor" + (" button" if "button" in pre.lower() else "")
            C[v] += 1; BYH[host][v] += 1; BYG[g][v] += 1; pages.add(cp); mods.add(code)
            if len(EX[v]) < 5: EX[v].append(f"{code}/{os.path.basename(cp)} {host} {url[:60]}")
print(f"bare ratio-16x9 iframe sites on paired pages: {TOT} on {len(pages)} pages / {len(mods)} modules")
for v, n in C.most_common(): print(f"   {n:4d}  {v}")
print("==== by host (top 20) ====")
for h, c in sorted(BYH.items(), key=lambda kv: -sum(kv[1].values()))[:20]:
    t = sum(c.values()); print(f"   {h:36s} n={t:3d}  " + "  ".join(f"{k} {v}" for k, v in c.most_common(3)))
print("==== by group ====")
for g, c in sorted(BYG.items(), key=lambda kv: -sum(kv[1].values()))[:12]:
    t = sum(c.values()); print(f"   {g:42s} n={t:3d}  " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(3)))
for v, ex in EX.items():
    for e in ex: print(f"   {v}: {e}")
