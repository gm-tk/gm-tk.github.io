#!/usr/bin/env python3
"""Session 37 Round 1 — WHAT ARE THE 3,047 'disjoint' ACTIVITY BOXES? (`_s37_r1_actbound3.py`'s bulk).

Once the KB-mandated red-note family is excluded (round 72 already excludes it from the skeleton too),
the paired activity boxes split 559 identical / 565 ends-late / 391 ends-early / 3,047 neither-a-prefix-
nor-a-suffix. That last group is 66 % of the population and is NOT a boundary defect — the two boxes
differ somewhere in the middle. This asks what it actually is, so the lane can be closed honestly
rather than called "diffuse" a third time.

The hypothesis to test: it is the WIDGET HAND-OFF population. Where the writer tagged an interactive
that the converter does not build, Claude emits a `cv2-int-ref` reference box carrying the raw writer
content; the human gold has BUILT the widget, so the same activity holds completely different text on
the two sides. That is Needs Chris #4 (D10-3, the quiz engines), not a boundary class.

Run under WSL:  python3 _s37_r1_disjoint.py
"""
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
kind = collections.Counter(); kmods = collections.defaultdict(set); ex = collections.defaultdict(list)
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
            chas = bool(re.search(r'cv2-int-ref', csub)); ghas = bool(WIDGETCLS.search(gsub))
            cw = bool(WIDGETCLS.search(csub))
            if chas and ghas: k = "Claude HAND-OFF box vs a BUILT gold widget (D10-3 / Needs Chris #4)"
            elif chas:       k = "Claude HAND-OFF box, gold has no widget markup (gold wrote it out as prose)"
            elif ghas and not cw: k = "gold BUILT a widget, Claude built none and no hand-off box"
            elif ghas and cw:     k = "both sides have widget markup — different build, same slot"
            else:            k = "neither side has widget markup — a genuine text difference"
            kind[k] += 1; kmods[k].add(code)
            if len(ex[k]) < 4:
                ex[k].append("%s %s «%s» gold %d / claude %d elems" % (code, os.path.basename(cp), plain(gt)[:22], len(gtx), len(ctx)))
tot = sum(kind.values())
print("THE 'DISJOINT' ACTIVITY BOXES — %d" % tot)
print("=" * 92)
for k, v in kind.most_common():
    print("   %-66s %5d  mods %4d" % (k[:66], v, len(kmods[k])))
print()
for k, _ in kind.most_common():
    print("  " + k); [print("     " + e) for e in ex[k]]
