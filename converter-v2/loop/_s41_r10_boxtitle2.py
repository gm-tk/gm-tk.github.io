#!/usr/bin/env python3
"""Session 41 Round 10 PICK (v2 — box-number-free) — for every gold activity box whose first element is an <h3> with text T: find T on
the paired Claude page. Classes: OK = a Claude box's first element is an h3 of T; BOX-P = a Claude box's first element is a <p> of T;
BOX-LATER = T inside a Claude box but not first; RAW = inside a hand-off widget raw; OUT-H = a heading outside every box; OUT-P = a <p>
outside every box; ABSENT. Per family + examples. Run under WSL from CONVERTER_V2/reference/tests."""
import os, re, sys, collections, html as H
sys.path.insert(0, os.getcwd())
import _discrepancy_audit as DA, _corpus
from anchor_compare import CLAUDE
def norm(s): return re.sub(r"[^a-z0-9āēīōū]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", s)).lower()).strip()
def spans(s):
    out = []
    for m in re.finditer(r'<div class="activity[^"]*"[^>]*>', s):
        st = m.start(); depth = 0; end = len(s)
        for t in re.finditer(r"<(/?)div\b[^>]*>", s[st:]):
            depth += -1 if t.group(1) else 1
            if depth == 0: end = st + t.end(); break
        out.append((st, end, m.end()))
    return out
EL = re.compile(r"<(h[1-6]|p|li)\b[^>]*>(.*?)</\1>", re.S)
def first_el(s, a):
    m = EL.search(s, a); return (m.group(1), norm(m.group(2)), m.start()) if m else (None, "", -1)
cases = collections.Counter(); fam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    f = re.match(r"[A-Z]+", code).group(0)
    for _, cp, hp in DA.pairs(code):
        g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8", errors="replace").read()
        cb = spans(c)
        cfirst = [first_el(c, a) for _, _, a in cb]
        raws = [(m.start(), m.end()) for m in re.finditer(r'<div class="cv2-int-raw".*?</div>\s*</div>', c, re.S)]
        for gs, ge, ga in spans(g):
            tag, t, _ = first_el(g, ga)
            if tag != "h3" or len(t) < 4: continue
            key = t[:30]
            def has(x): return x and (x == t or x.startswith(key) or t.startswith(x[:30]))
            if any(ft == "h3" and has(fx) for ft, fx, _ in cfirst): k = "OK"
            elif any(ft == "p" and has(fx) for ft, fx, _ in cfirst): k = "BOX-P (first <p>, not h3)"
            elif any(ft and ft.startswith("h") and has(fx) for ft, fx, _ in cfirst): k = "BOX-H (first, other level)"
            else:
                k = "ABSENT"
                for m in EL.finditer(c):
                    if not has(norm(m.group(2))): continue
                    pos = m.start()
                    if any(a <= pos < b for a, b in raws): k = "RAW (inside the hand-off widget)"; break
                    inbox = any(a <= pos < b for a, b, _ in cb)
                    k = ("BOX-LATER (in a box, not first)" if inbox else ("OUT-H (a heading outside every box)" if m.group(1).startswith("h") else "OUT-P (a <p> outside every box)"))
                    break
                if k == "ABSENT" and any(key in norm(c[a:b]) for a, b in raws): k = "RAW (inside the hand-off widget)"
            cases[k] += 1; fam[f][k] += 1
            if k != "OK" and len(ex[k]) < 400: ex[k].append(f"{code} {os.path.basename(cp)}: {t[:70]}")
print("gold boxes opening with <h3>:", sum(cases.values()))
for k, n in cases.most_common(): print(f"{n:5d} {k}")
print()
for f, c in sorted(fam.items(), key=lambda x: -sum(v for k, v in x[1].items() if k != "OK")):
    miss = sum(v for k, v in c.items() if k != "OK")
    if miss >= 10: print(f"{f:7s} miss {miss:4d} / {sum(c.values()):4d}  " + ", ".join(f"{k.split(' ')[0]} {v}" for k, v in c.most_common() if k != "OK"))
for k in [k for k, _ in cases.most_common() if k != "OK"][:5]:
    print(f"\n== {k}"); [print("  ", e) for e in ex[k][:14]]
