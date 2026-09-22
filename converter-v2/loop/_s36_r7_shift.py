#!/usr/bin/env python3
"""Session 36 Round 7 — the BOUNDARY SHIFT detail. Of the title-matched activity boxes whose element COUNT is equal but whose
content differs (392 boxes / 214 modules in _s36_r7_actbound.log), what exactly swaps? For each such box report the element the
GOLD holds that Claude's box lacks and the element CLAUDE holds that the gold's lacks, with their tags and their position
(first / last / middle) inside the box — an off-by-one boundary shows up as "gold's last is Claude's absent, Claude's first is
the gold's absent" repeated across modules. Run under WSL: python3 _s36_r7_shift.py"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
TEXT = re.compile(r'<(p|h[1-6]|li)\b[^>]*>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def boxes(s):
    out = []
    for m in re.finditer(r'<div[^>]*class="[^"]*\bactivity\b[^"]*"[^>]*>', s):
        start = m.end(); depth = 1; i = len(s)
        for t in re.finditer(r'<div\b[^>]*>|</div>', s[start:]):
            depth += 1 if t.group(0) != "</div>" else -1
            if depth == 0: i = start + t.start(); break
        sub = s[start:i]
        items = [(x.group(1), norm(x.group(2)), plain(x.group(2))) for x in TEXT.finditer(sub) if len(norm(x.group(2))) >= 8]
        title = next((t for tag, t, _ in items if tag.startswith("h")), "")
        out.append((title, items))
    return out
def pos(items, t):
    ks = [k for k, (tag, tt, _) in enumerate(items) if tt == t]
    if not ks: return "?"
    k = ks[0]
    return "first" if k == 0 else ("last" if k == len(items) - 1 else "middle")
pat = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        g = boxes(open(hp, encoding="utf-8", errors="replace").read())
        c = boxes(open(cp, encoding="utf-8", errors="replace").read())
        cby = {t: it for t, it in c if t}
        for gt, git in g:
            if not gt or gt not in cby: continue
            cit = cby[gt]
            gs = {t for _, t, _ in git}; cs = {t for _, t, _ in cit}
            og = [x for x in git if x[1] not in cs]; oc = [x for x in cit if x[1] not in gs]
            if len(git) != len(cit) or not og or not oc: continue
            if len(og) != 1 or len(oc) != 1: continue          # the clean one-for-one swap
            gtag, gtt, gtxt = og[0]; ctag, ctt, ctxt = oc[0]
            key = "gold %s@%-6s  <->  claude %s@%s" % (gtag, pos(git, gtt), ctag, pos(cit, ctt))
            pat[key] += 1; mods[key].add(code)
            if len(ex[key]) < 5:
                ex[key].append("%s %s «%s» : gold «%s» / claude «%s»" % (code, os.path.basename(cp), plain(gt)[:26], gtxt[:40], ctxt[:40]))
print("title-matched boxes with an equal count and exactly ONE element swapped: %d" % sum(pat.values()))
for k, v in pat.most_common(16): print("   %-46s %4d   modules %3d" % (k, v, len(mods[k])))
print("\nexamples (the top patterns):")
for k, _ in pat.most_common(6):
    print("  " + k)
    for e in ex[k]: print("     " + e)
