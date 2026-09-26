#!/usr/bin/env python3
"""_s51_r9_caption.py — session 51 Round 9 PICK (the KB lane, constraint 41 'caption <p class="captionText"> under an image'):
every gold p.captionText on a paired page — what Claude renders for the same text on the paired page (its tag + class, or absent),
and the Writers Template form of that text (the red tag on its line or the nearest above within 2 lines). WSL, from reference/tests/."""
import os, re, sys, glob, collections, html as H
sys.path.insert(0, os.getcwd())
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

CAP = re.compile(r'<p[^>]*class="[^"]*\bcaptionText\b[^"]*"[^>]*>(.*?)</p>', re.S | re.I)
ANY = re.compile(r'<(p|li|h[1-6]|figcaption|td)\b([^>]*)>(.*?)</\1>', re.S | re.I)
RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
strip = lambda h: re.sub(r"\s+", " ", H.unescape(re.sub(r"<[^>]+>", " ", h))).strip()
fold = lambda t: " ".join(re.sub(r"[^a-z0-9 ]", " ", re.sub(r"\*|_", "", t.lower())).split())
res = collections.Counter(); form = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    gd = _corpus.mdir(HUMAN, code)
    w = [f for f in glob.glob(os.path.join(gd, "*_parsed.txt")) if "Writers" in f]
    lines = open(w[0], encoding="utf-8", errors="replace").read().split("\n") if w else []
    fl = [fold(l) for l in lines]
    for n, cp, hp in pairs(code):
        gh = open(hp, encoding="utf-8", errors="replace").read()
        caps = [strip(m.group(1)) for m in CAP.finditer(gh)]
        caps = [c for c in caps if len(c.split()) >= 2]
        if not caps: continue
        ch = open(cp, encoding="utf-8", errors="replace").read()
        cels = [(m.group(1).lower(), (re.search(r'class="([^"]*)"', m.group(2)) or [None, ""])[1], fold(strip(m.group(3)))) for m in ANY.finditer(ch)]
        for c in caps:
            fc = fold(c)
            hit = next((e for e in cels if e[2] and (e[2] == fc or (len(fc) > 20 and fc[:40] in e[2]))), None)
            k = "absent" if not hit else f"{hit[0]}.{hit[1].split()[0] if hit[1] else ''}".rstrip(".")
            if "cv2" in k: k = "in hand-off"
            key = fc[:40]
            li = next((i for i, x in enumerate(fl) if key and key in x), None)
            tg = "(not in WT)"
            if li is not None:
                tg = "(no tag)"
                for j in range(li, max(-1, li - 3), -1):
                    br = [r for r in RED.findall(lines[j]) if "[" in r]
                    if br: tg = ("same " if j == li else "above ") + re.sub(r"\d+[a-z]?", "N", " ".join(br).lower().strip())[:40]; break
                if tg == "(no tag)": tg += " italic" if "*" in lines[li] else ""
            res[k] += 1; form[f"{k:14s} | {tg}"] += 1; mods[k].add(code)
            if os.environ.get("CAPEX") and f"{k} | {tg}" == os.environ["CAPEX"]: print("EX", os.path.basename(cp), c[:70])
            if len(ex[k]) < 3: ex[k].append(f"{os.path.basename(cp)}: {c[:50]}")
print("gold captionText blocks on paired pages:", sum(res.values()))
for k, v in res.most_common(10): print(f"  {v:4d} claude={k:14s} mods={len(mods[k])}  e.g. {ex[k][0]}")
print("by Claude form x WT form:")
for k, v in form.most_common(25): print(f"  {v:4d} {k}")
