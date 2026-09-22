#!/usr/bin/env python3
"""Session 37 Round 1 — WHICH WRITER TAG is in the 1,062 hand-off boxes whose GOLD BUILT NO WIDGET?
(`_s37_r1_disjoint.py`'s largest group.) If the gold wrote the content out as prose rather than building
anything, either (a) the tag is a real widget the human declined to build — D10-3 territory — or
(b) the scanner is treating a NON-widget writer tag as an interactive and emitting a hand-off box where
the human just rendered content. (b) would be an over-firing recognition defect and shippable.
The hand-off box records the type it refused in its own markup, so read it straight off the page.
Run under WSL:  python3 _s37_r1_handoff.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
sys.path.insert(0, os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"))
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
TEXT = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
REDNOTE = re.compile(r"^\s*(writers?\s*note|red\s*flag|designer\s*/\s*developer\s*to\s*do"
                     r"|designer\s*note|note\s+from\s+[A-Z])", re.I)
WIDGETCLS = re.compile(r'cv2-int-ref|cv2-int-raw|hintDrop|clickDrop|dragDrop|flipCard|speechBubble'
                       r'|accordion|carousel|tabContent|modal|wordHighlighter|quiz', re.I)
def boxes(s):
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bactivity\b[^"]*"[^>]*>', s):
        start = m.end(); depth = 1; i = len(s)
        for t in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
            depth += 1 if t.group(0) != "</div>" else -1
            if depth == 0: i = start + t.start(); break
        sub = s[start:i]
        texts = [norm(x.group(2)) for x in TEXT.finditer(sub)
                 if len(norm(x.group(2))) >= 8 and not REDNOTE.match(plain(x.group(2)))]
        title = next((norm(x.group(2)) for x in TEXT.finditer(sub) if x.group(1).startswith("h")), "")
        out.append((title, texts, sub))
    return out
typ = collections.Counter(); tmods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        try:
            g = boxes(open(hp, encoding="utf-8", errors="replace").read())
            c = boxes(open(cp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        if not g or not c: continue
        cby = {}
        for t, tx, sub in c:
            if t and t not in cby: cby[t] = (tx, sub)
        for gt, gtx, gsub in g:
            if not gt or gt not in cby: continue
            ctx, csub = cby[gt]
            G, C = "".join(gtx), "".join(ctx)
            if not G or not C: continue
            if G == C or C.startswith(G) or G.startswith(C) or C.endswith(G) or G.endswith(C): continue
            if not re.search(r'cv2-int-ref', csub) or WIDGETCLS.search(gsub): continue
            # the hand-off box states the type it refused in its own ref id, e.g.
            # "ANZH104-INT-03-01-unclassified" — read the trailing token off the page.
            m2 = re.search(r'-INT-\d+-\d+-([A-Za-z][\w-]*)', csub)
            t = (m2.group(1).strip().lower() if m2 else "?")
            typ[t] += 1; tmods[t].add(code)
            if len(ex[t]) < 3: ex[t].append("%s %s «%s»" % (code, os.path.basename(cp), plain(gt)[:22]))
print("HAND-OFF BOXES WHOSE GOLD BUILT NO WIDGET — %d" % sum(typ.values()))
print("=" * 78)
for k, v in typ.most_common(25):
    print("   %-34s %5d   modules %4d" % (k[:34], v, len(tmods[k])))
print()
for k, _ in typ.most_common(8):
    print("  %s" % k); [print("     " + e) for e in ex[k]]
