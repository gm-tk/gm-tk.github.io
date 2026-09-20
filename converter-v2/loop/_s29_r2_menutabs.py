#!/usr/bin/env python3
"""Session 29 Round 2 PICK — the module-menu TABS wrapper census (DIFF_QUEUE rows #47 / #48).
For every paired page (the skeleton gate's own pairing) whose gold #module-menu-content holds a tabs menu:
  form = ROW+COL   (moduleMenu > div.row > div.tabs.col-*)     — the WJFUN gold form
         BARE      (moduleMenu > div.tabs)                      — what Claude emits
         ROW+TABS  (moduleMenu > div.row > div.tabs, no col class)
         OTHER:…
Reports the gold share per template / subject / prefix and the paired (gold, Claude) agreement.
Read-only. Run from reference/tests under WSL: python3 ../../outputs/_s29_r2_menutabs.py"""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reference', 'tests'))
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, DATA

META = json.load(open(os.path.join(DATA, 'Module_Structure_Index.json'), encoding='utf-8'))['module_meta']
MENU = re.compile(r'<div[^>]*id="module-menu-content"[^>]*>', re.I)
TAG = re.compile(r'<(/?)(\w+)([^>]*)>')
VOID = {'br', 'img', 'input', 'hr', 'meta', 'link'}

def menu_form(html):
    m = MENU.search(html)
    if not m:
        return None
    pos = m.end(); depth = 0; opened = []
    for t in TAG.finditer(html, pos):
        if t.start() - pos > 6000:
            break
        close, name, attrs = t.group(1), t.group(2).lower(), t.group(3)
        if name in VOID:
            continue
        if close:
            depth -= 1
            if depth < 0:
                break
            continue
        cls = re.search(r'class="([^"]*)"', attrs)
        cls = cls.group(1).split() if cls else []
        opened.append((depth, name, cls))
        depth += 1
        if len(opened) >= 3:
            break
    if not opened:
        return 'EMPTY'
    d0, n0, c0 = opened[0]
    if 'tabs' in c0:
        return 'BARE'
    if n0 == 'div' and 'row' in c0 and len(opened) > 1:
        d1, n1, c1 = opened[1]
        if 'tabs' in c1:
            return 'ROW+COL' if any(c.startswith('col-') for c in c1) else 'ROW+TABS'
        return 'ROW+' + '.'.join([n1] + c1[:2])
    return 'OTHER:' + '.'.join([n0] + c0[:2])

def read(p):
    try:
        return open(p, encoding='utf-8', errors='replace').read()
    except Exception:
        return ''

rows = []
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if not os.path.isdir(_corpus.mdir(CLAUDE, code)):
        continue
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I):
            continue
        gf = menu_form(read(hp)); cf = menu_form(read(cp))
        if gf is None:
            continue
        rows.append((code, os.path.basename(hp), gf, cf, META.get(code, {})))

tabs = [r for r in rows if r[2] in ('BARE', 'ROW+COL', 'ROW+TABS')]
print('paired pages with a gold menu %d; with a TABS menu in the gold %d (modules %d)' % (len(rows), len(tabs), len({r[0] for r in tabs})))
print('gold tabs-menu form overall:', collections.Counter(r[2] for r in tabs).most_common())
print('Claude form on those pages :', collections.Counter(r[3] for r in tabs).most_common())
print('paired (gold, Claude)      :', collections.Counter((r[2], r[3]) for r in tabs).most_common(8))
ctabs = [r for r in rows if r[3] in ('BARE', 'ROW+COL', 'ROW+TABS')]
print('Claude tabs-menu pages %d — gold form there:' % len(ctabs), collections.Counter(r[2] for r in ctabs).most_common(6))
by = collections.defaultdict(list)
for r in tabs:
    by[('template', r[4].get('template_type', '?'))].append(r)
    by[('subject', r[4].get('subject', '?'))].append(r)
    by[('prefix', r[4].get('prefix') or re.match(r'[A-Z]+', r[0]).group(0))].append(r)
print('\nGOLD tabs-menu form per group (n = tabs-menu pages; m = modules) and Claude\'s form on the same pages:')
for k in sorted(by, key=lambda k: (k[0], -len(by[k]))):
    sub = by[k]
    if len(sub) < 3:
        continue
    c = collections.Counter(r[2] for r in sub); cc = collections.Counter(r[3] for r in sub)
    print('  %-9s %-26s n=%3d m=%3d  gold %-40s  Claude %s' % (k[0], str(k[1])[:26], len(sub), len({r[0] for r in sub}),
          ' / '.join('%s %.2f' % (f, v / len(sub)) for f, v in c.most_common(3)),
          ' / '.join('%s %.2f' % (f, v / len(sub)) for f, v in cc.most_common(3))))
# the ROW+COL modules outside WJFUN
oth = sorted({r[0] for r in tabs if r[2] == 'ROW+COL' and not r[0].startswith('WJFUN')})
print('\nROW+COL gold modules outside WJFUN (%d):' % len(oth), ' '.join(oth[:60]))
bare = sorted({r[0] for r in tabs if r[2] == 'BARE'})
print('BARE gold modules (%d):' % len(bare), ' '.join(bare[:80]))
