#!/usr/bin/env python3
"""Insert a markdown section file into LOOP_STATE.md just before '## Round log' (idempotent by heading).
usage: python3 _s27_insert_section.py <section.md>"""
import io, os, sys
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
HOT = os.path.join(ROOT, 'LOOP_STATE.md')
sec = io.open(sys.argv[1], encoding='utf-8').read().rstrip('\n').split('\n')
lines = io.open(HOT, encoding='utf-8').read().split('\n')
head = sec[0]
if any(l == head for l in lines):
    print('already present'); sys.exit(0)
i = next(i for i, l in enumerate(lines) if l.startswith('## Round log'))
lines[i:i] = sec + ['']
io.open(HOT, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
print('inserted at', i, 'size', os.path.getsize(HOT))
