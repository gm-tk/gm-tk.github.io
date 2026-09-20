#!/usr/bin/env python3
"""Session 29 Round 4 PICK — the OVERVIEW module-menu COLUMN-SHELL census (DIFF_QUEUE row #36: Claude's EXTRA
`div.col-12.col-md-6.paddingR` in `div.row`, 64 pages / 44 modules; the gold has no paddingR column on those pages).
For every paired OVERVIEW page (label 0 / 0.0) whose gold #module-menu-content is a NON-tabs menu, the SHELL = the
class-signature of the direct children of the first `div.row` inside the menu (col classes only, order kept):
  OFFSET   = col-md-6.offset-md-0 ×2 (the r81 ENG-family `two_col_offset` shell)
  PADLR    = col-md-6.paddingR + col-md-6.paddingL (the KB 06 §3.3 pair / the r359 inquiry shell)
  BANNER   = col-md-12.paddingR (a banner row) then a row of paddingR ×2 (the r142 BLL banner family)
  PADRR    = col-md-6.paddingR ×2 (Claude's banner-family cols without the banner)
  SINGLE8  = one col-md-8
  ...else the raw signature.
Reports the gold shell per subject|phase group and Claude's shell on the same pages, then the disagreement list.
Read-only. Run from reference/tests under WSL: python3 ../../outputs/_s29_r4_menucols.py"""
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

def menu_rows(html):
    """the menu's ROWS: for each div.row that is a direct child of the menu (depth 0 or 1 under a tabs pane), its
    direct-child col signatures. Returns (kind, [[sig,...], ...]) — kind 'tabs' when the first child is div.tabs."""
    m = MENU.search(html)
    if not m:
        return None, []
    pos = m.end(); depth = 0; rows = []; cur = None; row_depth = None; first = None
    for t in TAG.finditer(html, pos):
        if t.start() - pos > 12000:
            break
        close, name, attrs = t.group(1), t.group(2).lower(), t.group(3)
        if name in VOID:
            continue
        if close:
            depth -= 1
            if depth < 0:
                break
            if cur is not None and depth == row_depth:
                rows.append(cur); cur = None; row_depth = None
            continue
        cls = re.search(r'class="([^"]*)"', attrs)
        cls = cls.group(1).split() if cls else []
        if first is None:
            first = (name, cls)
        if name == 'div' and 'row' in cls and cur is None:
            cur = []; row_depth = depth
        elif cur is not None and depth == row_depth + 1 and name == 'div':
            cur.append('.'.join(c for c in cls if c.startswith('col-') or c.startswith('offset-') or c.startswith('padding')) or 'div')
        depth += 1
    kind = 'tabs' if first and 'tabs' in first[1] else 'plain'
    return kind, rows

def shell(rows):
    if not rows:
        return 'EMPTY'
    r0 = rows[0]
    def sig(cols): return ' | '.join(cols)
    if len(rows) >= 2 and len(r0) == 1 and 'col-md-12' in r0[0] and 'paddingR' in r0[0] and len(rows[1]) == 2 and all('paddingR' in c or 'paddingL' in c for c in rows[1]):
        return 'BANNER+' + ('PADLR' if any('paddingL' in c for c in rows[1]) else 'PADRR')
    if len(r0) == 2 and all('col-md-6' in c and 'offset-md-0' in c for c in r0):
        return 'OFFSET'
    if len(r0) == 2 and 'paddingR' in r0[0] and 'paddingL' in r0[1]:
        return 'PADLR'
    if len(r0) == 2 and all('paddingR' in c for c in r0):
        return 'PADRR'
    if len(r0) == 2 and all('col-md-6' in c for c in r0):
        return 'COL6x2'
    if len(r0) == 1 and 'col-md-8' in r0[0]:
        return 'SINGLE8'
    if len(r0) == 1 and 'col-md-12' in r0[0]:
        return 'SINGLE12'
    return sig(r0)[:40]

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
        if not re.search(r'_0_0\.html$', os.path.basename(cp)):
            continue
        gk, gr = menu_rows(read(hp)); ck, cr = menu_rows(read(cp))
        if gk is None:
            continue
        rows.append((code, os.path.basename(hp), gk, shell(gr), ck, shell(cr), META.get(code, {})))

plain = [r for r in rows if r[2] == 'plain']
print('paired overview pages with a gold menu %d; gold NON-tabs (plain) %d, tabs %d' % (len(rows), len(plain), len(rows) - len(plain)))
print('gold plain shell overall :', collections.Counter(r[3] for r in plain).most_common(8))
print('Claude shell on those    :', collections.Counter(r[5] for r in plain).most_common(8))
print('paired (gold, Claude)    :', collections.Counter((r[3], r[5]) for r in plain).most_common(12))
by = collections.defaultdict(list)
for r in plain:
    meta = r[6]
    by[('subject', meta.get('subject', '?'))].append(r)
    by[('subject+phase', '%s|%s' % (meta.get('subject', '?'), meta.get('phase', '?')))].append(r)
    by[('template', meta.get('template_type', '?'))].append(r)
print('\nGOLD plain-menu shell per group (n = overview pages) and Claude\'s shell on the same pages:')
for k in sorted(by, key=lambda k: (k[0], -len(by[k]))):
    sub = by[k]
    if len(sub) < 3:
        continue
    c = collections.Counter(r[3] for r in sub); cc = collections.Counter(r[5] for r in sub)
    agree = sum(1 for r in sub if r[3] == r[5])
    print('  %-14s %-34s n=%3d agree=%3d  gold %-46s  Claude %s' % (k[0], str(k[1])[:34], len(sub), agree,
          ' / '.join('%s %.2f' % (f, v / len(sub)) for f, v in c.most_common(3)),
          ' / '.join('%s %.2f' % (f, v / len(sub)) for f, v in cc.most_common(3))))
print('\nDISAGREEMENTS (gold shell != Claude shell), by (gold, Claude) with modules:')
dis = collections.defaultdict(list)
for r in plain:
    if r[3] != r[5]:
        dis[(r[3], r[5])].append(r[0])
for k, v in sorted(dis.items(), key=lambda kv: -len(kv[1])):
    print('  gold %-16s Claude %-16s n=%3d  %s' % (k[0], k[1], len(v), ' '.join(sorted(v)[:24])))
