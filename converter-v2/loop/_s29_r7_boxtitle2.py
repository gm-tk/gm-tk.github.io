#!/usr/bin/env python3
"""_s29_r7_boxtitle2.py — drill into the `opener black tail` non-match classes of _s29_r7_boxtitle.json:
 (a) 'no box: free h3' — is the Claude h3 INSIDE an activity box with a DIFFERENT number (a numbering mismatch) or OUTSIDE every box?
 (b) 'box: ANOTHER h3 first' — what is Claude's first h3 vs the gold's, and where is the gold's title in the box?
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r7_boxtitle2.py
"""
import os, re, sys, json, html as H, collections
sys.path.insert(0, ".")
import _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_")
rows = json.load(open(os.path.join(HERE, "_s29_r7_boxtitle.json"), encoding="utf-8"))
def fold(t): return re.sub(r"[^a-z0-9]+", " ", H.unescape(re.sub(r"<[^>]+>", " ", t)).lower()).strip()

def box_spans(html):
    """list of (num, cls, start, end) for activity boxes"""
    out = []; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop()
                if st[1] is not None: out.append((st[1], st[0], st[2], m.start()))
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            isact = bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c
            stack.append((c, (num.group(1).upper() if num else "-") if isact else None, m.end()))
    return out

pg = {}
def page(code, name):
    k = (code, name)
    if k not in pg:
        d = _corpus.mdir(CLAUDE, code); pg[k] = open(os.path.join(d, name), encoding="utf-8").read()
    return pg[k]

A = collections.Counter(); Aex = collections.defaultdict(list)
B = collections.Counter(); Bex = collections.defaultdict(list)
for r in rows:
    if r["wt"] != "opener black tail": continue
    f = r["title"]
    if r["claude"] == "no box: free h3":
        c = page(r["code"], r["page"]); spans = box_spans(c)
        pos = None
        for m in re.finditer(r"<h3\b[^>]*>([\s\S]*?)</h3>", c):
            if fold(m.group(1)) == f: pos = m.start(); break
        inside = [b for b in spans if b[2] <= pos < b[3]] if pos is not None else []
        if inside:
            b = inside[-1]
            k = "inside box #%s (gold #%s): %s" % ("other", r["num"], "same lesson digit" if b[0][:1] == r["num"][:1] else "other lesson digit")
            k = "inside a box with another number — " + ("same lesson digit" if b[0][:1] == r["num"][:1] else "other lesson digit")
            A[k] += 1
            if len(Aex[k]) < 6: Aex[k].append("%s %s gold #%s claude #%s «%s»" % (r["code"], r["page"], r["num"], b[0], f[:40]))
        else:
            # what is around it?
            before = c[max(0, pos - 300):pos] if pos is not None else ""
            k = "OUTSIDE every box" + (" (after a cv2 dump)" if "cv2-interactive" in before else "")
            A[k] += 1
            if len(Aex[k]) < 10: Aex[k].append("%s %s gold #%s «%s»" % (r["code"], r["page"], r["num"], f[:40]))
    elif r["claude"] == "box: ANOTHER h3 first":
        c = page(r["code"], r["page"]); spans = [b for b in box_spans(c) if b[0] == r["num"]]
        if not spans: continue
        b = spans[0]; inner = c[b[2]:b[3]]
        m = re.search(r"<h3\b[^>]*>([\s\S]*?)</h3>", inner)
        first = fold(m.group(1)) if m else ""
        where = "title also present later in box" if f in fold(inner) else "title ABSENT from box"
        # is Claude's first h3 the gold's SECOND element?
        k = where
        B[k] += 1
        if len(Bex[k]) < 12: Bex[k].append("%s %s #%s gold «%s» / claude first h3 «%s»" % (r["code"], r["page"], r["num"], f[:38], first[:38]))
print("(a) opener black tail → 'no box: free h3' (%d):" % sum(A.values()))
for k, v in A.most_common():
    print("  %4d %s" % (v, k))
    for e in Aex[k]: print("       ", e)
print("\n(b) opener black tail → 'box: ANOTHER h3 first' (%d):" % sum(B.values()))
for k, v in B.most_common():
    print("  %4d %s" % (v, k))
    for e in Bex[k]: print("       ", e)
