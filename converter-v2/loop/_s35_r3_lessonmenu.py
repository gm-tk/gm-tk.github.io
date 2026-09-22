#!/usr/bin/env python3
"""Session 35 Round 3 PICK measurement — THE LESSON-PAGE MENU: on every paired LESSON page where the gold's menu region holds
text (>= 40 chars) that Claude keeps in its BODY, classify the WT's lesson section by the marker that opens its overview
block ([Lesson Overview] / [Overview] / none), whether the block is inside a layout TABLE, and what Claude's menu region
holds (empty / some). Uses the page item stream indirectly: the parsed WT text between the lesson's boundary markers.
Run under WSL: python3 _s35_r3_lessonmenu.py
"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def texts(h): return [norm(m.group(2)) for m in re.finditer(r'<(p|h[2-6]|li)\b[^>]*>((?:(?!</?(?:p|h[2-6]|li)\b).)*?)</\1>', h, re.S)]
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
LESSON_RE = re.compile(r'\[\s*(?:lesson|page)\s*(\d+)\b[^\]]*\]', re.I)
def wt_lesson_section(wt, n):
    """the parsed-WT text from the first `[Lesson n …]` / `[LESSON n]` marker to the next lesson marker"""
    starts = [(m.start(), int(m.group(1))) for m in LESSON_RE.finditer(wt)]
    idx = [i for i, (p, k) in enumerate(starts) if k == n]
    if not idx: return ""
    a = starts[idx[0]][0]
    b = next((p for p, k in starts[idx[0] + 1:] if k != n), len(wt))
    return wt[a:b]
byform = collections.Counter(); bymod = collections.OrderedDict(); rows = []
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    try: pl = pairs(code)
    except Exception: continue
    gdir = (glob.glob(ROOT + "/01-Finalized_Modules_/*/" + code + "/") or [None])[0]
    wt = ""
    for t in glob.glob(gdir + "*parsed.txt") if gdir else []:
        if "Writers" in t or "writers" in t: wt += open(t, encoding="utf-8", errors="replace").read()
    if not wt:
        for t in glob.glob(gdir + "*parsed.txt") if gdir else []: wt += open(t, encoding="utf-8", errors="replace").read()
    for n, cp, hp in pl:
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        m = re.search(r'_(\d+)_(\d+)\.html$', os.path.basename(cp))
        if not m or m.group(1) == "0": continue          # lesson pages only
        ln = int(m.group(1))
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        i = ch.find('<div id="body">')
        if i < 0: continue
        ghead, gbody = split_gold(gh)
        ch_t = set(texts(ch[:i])); cb_t = set(texts(ch[i:]))
        under = [t for t in texts(ghead) if len(t) >= 40 and t in cb_t and t not in ch_t]
        if not under: continue
        sec = wt_lesson_section(wt, ln)
        head = sec[:4000]
        lo = bool(re.search(r'\[\s*lesson\s+overview\s*\]', head, re.I))
        ov = bool(re.search(r'\[\s*overview\s*\]', head, re.I))
        lc = bool(re.search(r'\[\s*lesson\s+content\s*\]', head, re.I))
        tbl = bool(re.search(r'┌─── TABLE ───[^┘]{0,600}(learning intentions|we are learning|success criteria|i can)', head, re.I | re.S))
        wal = bool(re.search(r'learning intentions|we are learning|success criteria|how will i know|i can', head, re.I))
        cmenu_empty = len([t for t in ch_t if len(t) >= 20]) == 0
        form = ("LO" if lo else "OV" if ov else "none") + ("+table" if tbl else "") + ("+LC" if lc else "") + ("" if wal else " (no WALT text in the section head)")
        byform[form] += len(under)
        bymod.setdefault(code, collections.Counter())[form] += len(under)
        rows.append((code, os.path.basename(cp), form, len(under), "menu-empty" if cmenu_empty else "menu-some"))
print("lesson pages with a gold-menu element in Claude's body: %d; elements %d; modules %d" % (len(rows), sum(r[3] for r in rows), len(bymod)))
print("by WT form (elements):")
for k, v in byform.most_common(): print("  %-50s %4d  pages %d  modules %d" % (k, v, sum(1 for r in rows if r[2] == k), len({r[0] for r in rows if r[2] == k})))
print("Claude menu region empty on %d of %d pages" % (sum(1 for r in rows if r[4] == "menu-empty"), len(rows)))
print("by module:")
for code, c in sorted(bymod.items(), key=lambda kv: -sum(kv[1].values()))[:30]:
    print("  %-10s %3d  %s" % (code, sum(c.values()), dict(c)))
