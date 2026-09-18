#!/usr/bin/env python3
"""r398 — prove every changed page differs ONLY by the `icon` token on a videoSection class list, and count the
tokens added, by context (free / widget-embedded). Reads _s27_r398_on/<code>/<page> vs the disk page."""
import os, re, sys, glob
from collections import Counter
OUT = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests')
import _corpus
from anchor_compare import CLAUDE
ON = os.path.join(OUT, '_s27_r398_on')
def strip_icon(html):
    return re.sub(r'class="([^"]*)"', lambda m: 'class="' + m.group(1).replace('videoSection icon', 'videoSection') + '"', html)
pages = 0; clean = 0; dirty = []; added = 0; mods = set()
for d in sorted(glob.glob(os.path.join(ON, '*'))):
    code = os.path.basename(d)
    disk_dir = _corpus.mdir(CLAUDE, code)
    for f in sorted(os.listdir(d)):
        if not f.endswith('.html'): continue
        on = open(os.path.join(d, f), encoding='utf-8', errors='replace').read()
        dp = os.path.join(disk_dir, f)
        if not os.path.exists(dp): continue
        disk = open(dp, encoding='utf-8', errors='replace').read()
        if on == disk: continue
        pages += 1; mods.add(code)
        if strip_icon(on) == strip_icon(disk):
            clean += 1
            added += on.count('videoSection icon') - disk.count('videoSection icon')
        else:
            dirty.append(f'{code}/{f}')
print(f'changed pages {pages} / modules {len(mods)}; icon-token-only {clean}; other diffs {len(dirty)}; icon tokens added {added}')
for x in dirty[:10]: print('  DIRTY', x)
open(os.path.join(OUT, '_s27_r398_changed_modules.txt'), 'w').write('\n'.join(sorted(mods)) + '\n')
