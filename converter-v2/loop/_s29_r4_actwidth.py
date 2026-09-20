#!/usr/bin/env python3
"""Session 29 Round 4 PICK — the ACTIVITY BOX'S WRAPPER COLUMN WIDTH by the widget inside it (the D10-3 rider: 're-measure the
wrapper per built layout'). For every paired page: each gold `div.activity…` whose direct parent column is `col-md-8` or
`col-md-12` → the FIRST widget class inside the box (dragAndDrop[layout], clickDrop, carousel, flipCard, dropQuiz, mcq,
selectionBox, typing, speechBubble, table, none) + the box's number; the same for Claude; paired by number. Tabulates the
gold's width share per widget kind and the paired agreement. Read-only; run from reference/tests under WSL."""
import os, re, sys, json, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'reference', 'tests'))
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, DATA
META = json.load(open(os.path.join(DATA, 'Module_Structure_Index.json'), encoding='utf-8'))['module_meta']
TAG = re.compile(r'<(/?)(\w+)([^>]*)>')
VOID = {'br', 'img', 'input', 'hr', 'meta', 'link'}
WIDGET = ['dragAndDrop', 'clickDrop', 'carousel', 'flipCard', 'dropQuiz', 'multiChoiceQuiz', 'mcqOptions', 'selectionBox', 'typing', 'speechBubble', 'accordion', 'tabs', 'hintSlider', 'TKmodal', 'selfCheck', 'reorder', 'wordDrag', 'cv2-interactive']
def read(p):
    try: return open(p, encoding='utf-8', errors='replace').read()
    except Exception: return ''
def boxes(html):
    """[(number, wrapper_col, widget_kind)] for every activity box: walk the tag stream keeping a stack of (name, classes)."""
    out = []; stack = []
    for t in TAG.finditer(html):
        close, name, attrs = t.group(1), t.group(2).lower(), t.group(3)
        if name in VOID: continue
        if close:
            while stack:
                top = stack.pop()
                if top[0] == name: break
            continue
        cls = re.search(r'class="([^"]*)"', attrs); cls = cls.group(1).split() if cls else []
        if name == 'div' and 'activity' in cls and 'alertActivity' not in cls:
            num = re.search(r'number="([^"]*)"', attrs); num = num.group(1) if num else ''
            parent = next((s for s in reversed(stack) if any(c.startswith('col-') for c in s[1])), None)
            wrap = 'col-md-12' if parent and 'col-md-12' in parent[1] else ('col-md-8' if parent and 'col-md-8' in parent[1] else ('col-12' if parent and 'col-12' in parent[1] and len([c for c in parent[1] if c.startswith('col-')]) == 1 else 'other'))
            # the first widget class inside the box
            depth0 = len(stack); kind = 'none'; layout = ''
            for u in TAG.finditer(html, t.end()):
                if u.group(1):
                    if len(stack) <= depth0 and u.group(2).lower() == 'div': break
                    continue
                ucls = re.search(r'class="([^"]*)"', u.group(3)); ucls = ucls.group(1).split() if ucls else []
                w = next((wc for wc in WIDGET if wc in ucls), None)
                if u.group(2).lower() == 'table' and kind == 'none': kind = 'table'; break
                if w:
                    kind = w
                    lay = re.search(r'layout="([^"]*)"', u.group(3)); layout = lay.group(1) if lay else ''
                    break
                if u.start() - t.end() > 6000: break
            out.append((num, wrap, kind + (':' + layout if layout else '')))
        stack.append((name, cls))
    return out
G = collections.Counter(); C = collections.Counter(); P = collections.Counter(); PS = collections.Counter()
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if not os.path.isdir(_corpus.mdir(CLAUDE, code)): continue
    meta = META.get(code, {}); subj = meta.get('subject', '?'); tt = meta.get('template_type', '?')
    for n, cp, hp in pairs(code):
        gb = boxes(read(hp)); cb = boxes(read(cp))
        for num, wrap, kind in gb: G[(kind, wrap)] += 1
        for num, wrap, kind in cb: C[(kind, wrap)] += 1
        gm = {b[0]: b for b in gb if b[0]}; cm = {b[0]: b for b in cb if b[0]}
        for num in gm.keys() & cm.keys():
            P[(gm[num][2].split(':')[0], gm[num][1], cm[num][1])] += 1
            PS[(tt, gm[num][2].split(':')[0], gm[num][1], cm[num][1])] += 1
def share(counter, kind):
    tot = sum(v for (k, w), v in counter.items() if k == kind)
    return {w: v for (k, w), v in counter.items() if k == kind}, tot
print('GOLD activity boxes by inner widget → wrapper width (share of col-md-12):')
kinds = collections.Counter(k for (k, w) in G.elements())
for kind, n in kinds.most_common(24):
    d, tot = share(G, kind); dc, totc = share(C, kind)
    print('  %-26s gold n=%4d  col-md-12 %.2f  col-md-8 %.2f  col-12 %.2f   | Claude n=%4d col-md-12 %.2f col-md-8 %.2f' % (kind, tot, d.get('col-md-12', 0) / tot, d.get('col-md-8', 0) / tot, d.get('col-12', 0) / tot, totc, dc.get('col-md-12', 0) / max(1, totc), dc.get('col-md-8', 0) / max(1, totc)))
print('\nPAIRED by number (gold kind, gold wrap, Claude wrap):')
for k, v in P.most_common(24):
    print('  %5d  %-22s gold %-10s Claude %s' % (v, k[0], k[1], k[2]))
print('\nPAIRED per template (template, gold kind, gold wrap, Claude wrap) where gold col-md-12:')
for k, v in sorted(PS.items(), key=lambda kv: -kv[1]):
    if k[2] == 'col-md-12' and v >= 5: print('  %5d  %-13s %-22s gold %-10s Claude %s' % (v, k[0], k[1], k[2], k[3]))
