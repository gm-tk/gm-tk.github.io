#!/usr/bin/env python3
"""Session 36 Round 7 PICK — THE ACTIVITY-BOX BOUNDARY, a new instrument. The r436 loss ledger's largest addressable non-chrome,
non-editorial family is container-shift (activity->widget 1.28pp, free->widget 1.16, activity->free 0.70, free->activity 0.69 =
3.83pp): the text is on both pages but inside a different container. This measures the BOX itself, paired: for every paired page,
match the gold's activity boxes to Claude's by their TITLE (the box's first heading, folded) and report, per matched box, how many
text elements each side holds and which side holds the extra ones — so the question "does Claude's box start too early / end too
late / miss content" is answered per SHAPE rather than in aggregate.
Run under WSL: python3 _s36_r7_actbound.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
TEXT = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def boxes(pathhtml):
    """every div.activity subtree: (title, [normalised texts], number attribute)"""
    s = pathhtml
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bactivity\b[^"]*"[^>]*>', s):
        start = m.end()
        depth = 1; i = start
        for t in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
            depth += 1 if t.group(0) != "</div>" else -1
            if depth == 0: i = start + t.start(); break
        else: i = len(s)
        sub = s[start:i]
        texts = [norm(x.group(2)) for x in TEXT.finditer(sub) if len(norm(x.group(2))) >= 8]
        title = next((norm(x.group(2)) for x in TEXT.finditer(sub) if x.group(1).startswith("h")), "")
        num = (re.search(r'number="([^"]*)"', m.group(0)) or [None, ""])[1]
        out.append((title, texts, num))
    return out
tab = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
extra_sig = collections.Counter(); missing_sig = collections.Counter()
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        g = boxes(open(hp, encoding="utf-8", errors="replace").read())
        c = boxes(open(cp, encoding="utf-8", errors="replace").read())
        if not g or not c: continue
        cby = {t: (t, tx, nu) for t, tx, nu in c if t}
        for gt, gtx, gnu in g:
            if not gt or gt not in cby: continue
            _, ctx, cnu = cby[gt]
            gs, cs = set(gtx), set(ctx)
            onlyg = gs - cs; onlyc = cs - gs
            if not onlyg and not onlyc:
                tab["box IDENTICAL in content"] += 1; continue
            k = ("claude's box has MORE (over-capture)" if len(onlyc) > len(onlyg)
                 else "claude's box has LESS (under-capture)" if len(onlyg) > len(onlyc)
                 else "same size, different content")
            tab[k] += 1; mods[k].add(code)
            if len(ex[k]) < 6:
                ex[k].append("%s %s box «%s» gold %d / claude %d" % (code, os.path.basename(cp), plain(gt)[:34], len(gtx), len(ctx)))
print("paired activity boxes matched by title: %d" % sum(tab.values()))
for k, v in tab.most_common(): print("   %-42s %5d   modules %3d" % (k, v, len(mods.get(k, ()))))
print("\nexamples:")
for k, v in sorted(ex.items()):
    print("  " + k)
    for e in v: print("     " + e)
