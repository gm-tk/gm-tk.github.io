import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _discrepancy_audit import pairs
HEAD = re.compile(r'<div class="row[^"]*">\s*<div class="([^"]*)">\s*<(h[1-6])[^>]*>\s*Introduction\s*</\2>\s*(</div>)?', re.I)
ser = collections.defaultdict(collections.Counter)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    if not code.startswith("BLL"): continue
    for _, cp, hp in pairs(code):
        m = HEAD.search(open(hp, encoding="utf-8", errors="replace").read())
        if m: ser[code[:5]][("col-12" if m.group(1).strip() == "col-12" else "md8") + (" alone" if m.group(3) else "")] += 1
for s in sorted(ser): print(s, dict(ser[s]))
