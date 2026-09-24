#!/usr/bin/env python3
"""Session 41 Round 10 PICK — THE ACTIVITY BOX'S MISSING TITLE. For every gold activity box (div.activity…, matched to the Claude
box with the same number= on the paired page) whose first heading is an <h3> with text T: does Claude's box open with an h3 of T?
If not, where is T on the Claude page: a <p> INSIDE the box (first / later), a <p> or heading OUTSIDE the box, inside a hand-off
widget raw, or nowhere. Tallied per family and per template; with 25 examples of the largest case.
Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
from anchor_compare import CLAUDE
def norm(s): return re.sub(r"[^a-z0-9āēīōū]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s)).lower()).strip()
def boxes(s):
    out = {}
    for m in re.finditer(r'<div class="activity[^"]*"[^>]*number="([^"]+)"[^>]*>', s):
        st = m.start(); depth = 0; end = len(s)
        for t in re.finditer(r"<(/?)div\b[^>]*>", s[st:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: end = st + t.end(); break
        out.setdefault(m.group(1), (st, end))
    return out
def first_head(seg):
    m = re.search(r"<(h[1-6]|p)\b[^>]*>(.*?)</\1>", seg, re.S)
    return (m.group(1), norm(m.group(2))) if m else (None, "")
cases = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.match(r"[A-Z]+", code).group(0)
    for _, cp, hp in DA.pairs(code):
        g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8", errors="replace").read()
        gb, cb = boxes(g), boxes(c)
        for num, (gs, ge) in gb.items():
            tag, t = first_head(g[gs:ge][g[gs:ge].index(">") + 1:])
            if tag != "h3" or len(t) < 3: continue
            if num not in cb: k = "no Claude box with that number"
            else:
                cs, ce = cb[num]; seg = c[cs:ce]
                ctag, ct = first_head(seg[seg.index(">") + 1:])
                if ctag == "h3" and (ct == t or ct.startswith(t[:25]) or t.startswith(ct[:25])): k = "OK (h3 in box)"
                elif ctag and ctag.startswith("h") and (ct == t or t[:20] in ct): k = f"in box as {ctag}"
                else:
                    segn = norm(seg); raw = " ".join(norm(x) for x in re.findall(r'class="cv2-int-raw".*?</div>\s*</div>', seg, re.S))
                    before = norm(c[max(0, cs - 1500):cs])
                    if ctag == "p" and (ct == t or t[:20] in ct): k = "first <p> in box (not h3)"
                    elif t[:20] and t[:20] in raw: k = "inside the hand-off widget raw"
                    elif t[:20] and t[:20] in segn: k = "later in box (not first)"
                    elif t[:20] and t[:20] in before: k = "before the box (outside)"
                    elif t[:20] and t[:20] in norm(c): k = "elsewhere on page"
                    else: k = "absent"
            cases[k] += 1; fam[f][k] += 1
            if k != "OK (h3 in box)" and len(ex[k]) < 25: ex[k].append(f"{code} {os.path.basename(cp)} #{num}: {t[:70]}")
print("gold boxes opening with <h3>:", sum(cases.values()))
for k, n in cases.most_common(): print(f"{n:5d} {k}")
print()
for f, c in sorted(fam.items(), key=lambda x: -sum(v for k, v in x[1].items() if not k.startswith("OK"))):
    miss = sum(v for k, v in c.items() if not k.startswith("OK"))
    if miss >= 8: print(f"{f:7s} miss {miss:4d} / {sum(c.values()):4d}  " + ", ".join(f"{k} {v}" for k, v in c.most_common() if not k.startswith("OK")))
for k in [k for k, _ in cases.most_common() if not k.startswith("OK")][:4]:
    print(f"\n== {k}"); [print("  ", e) for e in ex[k][:12]]
