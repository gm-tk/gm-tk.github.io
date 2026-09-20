#!/usr/bin/env python3
"""Session 29 Round 4 PICK — where does the GOLD put `col-12 col-md-12` (1733 skeleton lines / 794 pages, the label census's
largest MISSING wrapper) and what does Claude ship at the same sites? For every paired page: each gold `div.col-12.col-md-12`
(either class order) → its context = the nearest enclosing open container in the 400 chars before it (activity box / row /
supervisor panel / alert …) + its first child tag; Claude's count of the same class on the paired page. Tabulated by
(context, first child) and by subject. Read-only; run from reference/tests under WSL."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reference', 'tests'))
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, DATA
META = json.load(open(os.path.join(DATA, 'Module_Structure_Index.json'), encoding='utf-8'))['module_meta']
COL = re.compile(r'<div\s+class="(?:col-12 col-md-12|col-md-12 col-12)(?:\s+[^"]*)?"[^>]*>', re.I)
OPEN = re.compile(r'<div\s+class="([^"]+)"', re.I)
NEXT = re.compile(r'<(\w+)([^>]*)>')
def read(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
def ctx_of(html, pos):
    before = html[max(0, pos - 500):pos]
    opens = [m.group(1) for m in OPEN.finditer(before)]
    # the last activity / supervisor / alert / row / clickDropContent open before the col
    for c in reversed(opens):
        t = c.split()
        if 'activity' in t: return 'activity' + ('.interactive' if 'interactive' in t else '')
        if 'super-content' in t or 'supervisor' in t: return 'supervisor'
        if 'alert' in t: return 'alert'
        if 'clickDropContent' in t: return 'clickDropContent'
        if 'accContent' in t or 'accordion' in t: return 'accordion'
        if 'row' in t and len(t) == 1: return 'row(plain)'
        if 'row' in t: return 'row.' + '.'.join(x for x in t if x != 'row')[:20]
    return 'other'
def first_child(html, pos):
    m = NEXT.search(html, pos)
    if not m: return '?'
    name = m.group(1).lower(); cls = re.search(r'class="([^"]*)"', m.group(2))
    cls = cls.group(1).split() if cls else []
    if name == 'div' and cls: return 'div.' + cls[0]
    if name == 'img': return 'img'
    return name
rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if not os.path.isdir(_corpus.mdir(CLAUDE, code)): continue
    meta = META.get(code, {})
    for n, cp, hp in pairs(code):
        g = read(hp); c = read(cp)
        gm = list(COL.finditer(g)); cm = list(COL.finditer(c))
        if not gm and not cm: continue
        for m in gm:
            rows.append((code, os.path.basename(hp), 'gold', ctx_of(g, m.start()), first_child(g, m.end()), meta.get('subject', '?'), meta.get('template_type', '?'), len(gm), len(cm)))
        for m in cm:
            rows.append((code, os.path.basename(cp), 'claude', ctx_of(c, m.start()), first_child(c, m.end()), meta.get('subject', '?'), meta.get('template_type', '?'), len(gm), len(cm)))
gold = [r for r in rows if r[2] == 'gold']; cl = [r for r in rows if r[2] == 'claude']
print('gold col-md-12 sites %d on %d pages / %d modules; Claude sites %d' % (len(gold), len({(r[0], r[1]) for r in gold}), len({r[0] for r in gold}), len(cl)))
print('\nGOLD by (context, first child):')
for k, v in collections.Counter((r[3], r[4]) for r in gold).most_common(22):
    print('  %5d  %-24s %s' % (v, k[0], k[1]))
print('\nGOLD by context, per template:')
for k, v in sorted(collections.Counter((r[6], r[3]) for r in gold).items(), key=lambda kv: -kv[1])[:16]:
    print('  %5d  %-14s %s' % (v, k[0], k[1]))
print('\nGOLD by context, per subject (top):')
for k, v in sorted(collections.Counter((r[5], r[3]) for r in gold).items(), key=lambda kv: -kv[1])[:20]:
    print('  %5d  %-30s %s' % (v, k[0], k[1]))
print('\nCLAUDE by (context, first child):')
for k, v in collections.Counter((r[3], r[4]) for r in cl).most_common(10):
    print('  %5d  %-24s %s' % (v, k[0], k[1]))
