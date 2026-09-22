#!/usr/bin/env python3
"""Session 36 Round 1 PICK — WHAT does the gold's lesson-menu region hold on the residue pages (the s35-r3 census's
"none (no WALT text in the section head)" bucket and the rest)? For every paired LESSON page where the gold's menu
region holds text (>= 40 chars) that Claude keeps in its BODY: print the gold menu region's element signatures with
their (truncated) text, the WT section head's first lines, and whether the same text sits in Claude's body under
which tag. Run under WSL: python3 _s36_r1_menuwhat.py [CODE ...]
"""
import re, os, sys, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests"); sys.path.insert(0, TESTS)
from _discrepancy_audit import pairs
import _corpus
def norm(s): return re.sub(r'[^a-z0-9]+', '', html.unescape(re.sub(r'<[^>]+>', ' ', s)).lower())
def plain(s): return re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))).strip()
ELEM_RE = re.compile(r'<(p|h[1-6]|li)\b([^>]*)>((?:(?!</?(?:p|h[1-6]|li)\b).)*?)</\1>', re.S)
def elems(h):
    out = []
    for m in ELEM_RE.finditer(h):
        cls = re.search(r'class="([^"]*)"', m.group(2))
        out.append((m.group(1) + ("." + cls.group(1).replace(" ", ".") if cls else ""), norm(m.group(3)), plain(m.group(3))))
    return out
def split_gold(g):
    for mark in ('<div id="body"', '<div class="inquiryPanel', '<div class="crumbs"', '<div class="phases"'):
        i = g.find(mark)
        if i > 0: return g[:i], g[i:]
    return g, ""
LESSON_RE = re.compile(r'\[\s*(?:lesson|page)\s*(\d+)\b[^\]]*\]', re.I)
def wt_lesson_section(wt, n):
    starts = [(m.start(), int(m.group(1))) for m in LESSON_RE.finditer(wt)]
    idx = [i for i, (p, k) in enumerate(starts) if k == n]
    if not idx: return ""
    a = starts[idx[0]][0]
    b = next((p for p, k in starts[idx[0] + 1:] if k != n), len(wt))
    return wt[a:b]
def wrapper_of(h, pos):
    """the nearest enclosing div class chain before pos (crude: last 3 opening divs not yet closed)"""
    head = h[:pos]
    opens = [m for m in re.finditer(r'<div\b([^>]*)>', head)]
    closes = len(re.findall(r'</div>', head))
    depth = len(opens) - closes
    chain = []
    for m in opens[-max(depth, 0):][-4:]:
        c = re.search(r'class="([^"]*)"', m.group(1)); i = re.search(r'id="([^"]*)"', m.group(1))
        chain.append(("#" + i.group(1) if i else "") + ("." + c.group(1).replace(" ", ".") if c else "div"))
    return " > ".join(chain)
want = set(sys.argv[1:])
total = collections.Counter(); sigcount = collections.Counter(); wrapcount = collections.Counter()
for code in sorted({os.path.basename(d.rstrip("/")) for d in glob.glob(ROOT + "/01-Claude_Modules_/*/*/")}):
    if want and code not in want: continue
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
        if not m or m.group(1) == "0": continue
        ln = int(m.group(1))
        ch = open(cp, encoding="utf-8", errors="replace").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        i = ch.find('<div id="body">')
        if i < 0: continue
        ghead, gbody = split_gold(gh)
        ch_e = elems(ch[:i]); cb_e = elems(ch[i:])
        ch_t = {e[1] for e in ch_e}; cb_t = {e[1]: e[0] for e in cb_e}
        g_e = elems(ghead)
        under = [(sig, t, txt) for sig, t, txt in g_e if len(t) >= 40 and t in cb_t and t not in ch_t]
        if not under: continue
        sec = wt_lesson_section(wt, ln)
        head = sec[:1200]
        total[code] += len(under)
        print("=== %s %s  (gold menu elements %d; Claude menu elements %d; under %d)" % (code, os.path.basename(cp), len(g_e), len([e for e in ch_e if len(e[1]) >= 20]), len(under)))
        # the gold menu region's structure with text, marking the under ones
        gm_start = gh.find('<div id="module-menu"');
        if gm_start < 0: gm_start = gh.find('module-menu')
        for sig, t, txt in g_e:
            if len(t) < 3: continue
            mark = "  << BODY(%s)" % cb_t[t] if (sig, t, txt) in under else ("  (Claude menu)" if t in ch_t else "")
            pos = ghead.find(txt[:30]) if txt else -1
            wr = wrapper_of(ghead, pos) if pos > 0 else "?"
            print("    gold %-22s %-60s %s" % (sig, txt[:60], mark))
            if (sig, t, txt) in under:
                sigcount[sig] += 1; wrapcount[wr.split(" > ")[-1] if wr else "?"] += 1
        print("    -- WT section head --")
        for ln_ in [l for l in head.splitlines() if l.strip()][:14]:
            print("       | " + ln_[:110])
print("\n=== TOTALS: modules %d, elements %d" % (len(total), sum(total.values())))
print("under-elements by gold signature:")
for k, v in sigcount.most_common(): print("   %-30s %d" % (k, v))
print("under-elements by gold wrapper (innermost div):")
for k, v in wrapcount.most_common(): print("   %-50s %d" % (k, v))
