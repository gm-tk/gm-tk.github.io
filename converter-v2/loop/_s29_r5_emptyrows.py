#!/usr/bin/env python3
"""Session 29 Round 5 PICK — EMPTY row/col shells: `<div class="row"> <div class="col-…"> </div> </div>` with nothing but
whitespace inside the column, counted on every paired page, gold vs Claude, with the col class and the module's template / subject."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reference', 'tests'))
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, DATA
META = json.load(open(os.path.join(DATA, 'Module_Structure_Index.json'), encoding='utf-8'))['module_meta']
EMPTY = re.compile(r'<div class="row">\s*<div class="(col[^"]*)">\s*</div>\s*</div>', re.S)
EMPTYCOL = re.compile(r'<div class="(col[^"]*)">\s*</div>', re.S)
def read(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
G = collections.Counter(); C = collections.Counter(); GC = collections.Counter(); CC = collections.Counter()
pg = collections.Counter(); pc = collections.Counter(); mods = set(); ctx = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if not os.path.isdir(_corpus.mdir(CLAUDE, code)): continue
    meta = META.get(code, {}); key = (meta.get('template_type', '?'), meta.get('subject', '?'))
    for n, cp, hp in pairs(code):
        g = read(hp); c = read(cp)
        ng = len(EMPTY.findall(g)); nc = len(EMPTY.findall(c))
        G[key] += ng; C[key] += nc
        if ng: pg[key] += 1
        if nc: pc[key] += 1; mods.add(code)
        for m in EMPTY.finditer(c):
            before = c[max(0, m.start() - 300):m.start()]
            after = c[m.end():m.end() + 200]
            prev = re.findall(r'<(?:div class="([^"]*)"|(h[1-6])|(p)|(/div))', before)
            nxt = re.search(r'<(\w+)(?: class="([^"]*)")?', after)
            ctx[(m.group(1), (nxt.group(1) + '.' + (nxt.group(2) or '').split(' ')[0]) if nxt else 'END')] += 1
        for m in EMPTYCOL.finditer(g): GC[m.group(1)] += 1
        for m in EMPTYCOL.finditer(c): CC[m.group(1)] += 1
print('EMPTY row>col shells: gold %d on %d pages | Claude %d on %d pages / %d modules' % (sum(G.values()), sum(pg.values()), sum(C.values()), sum(pc.values()), len(mods)))
print('\nper template|subject (gold shells / gold pages | Claude shells / Claude pages):')
for k in sorted(set(G) | set(C), key=lambda k: -C[k])[:22]:
    print('  %-13s %-28s gold %4d / %3d | Claude %4d / %3d' % (k[0], k[1][:28], G[k], pg[k], C[k], pc[k]))
print('\nClaude empty shells by (col class, next tag):')
for k, v in ctx.most_common(12): print('  %5d  %-32s next %s' % (v, k[0], k[1]))
print('\nempty COLS (any parent) gold:', GC.most_common(5), ' Claude:', CC.most_common(5))
