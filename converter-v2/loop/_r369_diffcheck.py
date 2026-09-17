#!/usr/bin/env python3
"""r369 — list the probe's changed pages (outputs/_r369_on vs disk) and prove every differing line is an
activity `number=` attribute change; write _r369_changed_modules.txt / _r369_changed_pages.txt."""
import os, sys, re, difflib, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE
ON = os.path.join(HERE, "_r369_on")
mods = []; pages = []; bad = []; changes = collections.Counter(); nchanges = 0
for code in sorted(os.listdir(ON)):
    d = os.path.join(ON, code)
    if not os.path.isdir(d): continue
    disk = _corpus.mdir(CLAUDE, code)
    changed_here = []
    for f in sorted(os.listdir(d)):
        if not f.endswith(".html"): continue
        a = open(os.path.join(disk, f), encoding="utf-8", errors="replace").read().split("\n")
        b = open(os.path.join(d, f), encoding="utf-8", errors="replace").read().split("\n")
        if a == b: continue
        changed_here.append(f)
        for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
            if tag == "equal": continue
            if tag != "replace" or (i2 - i1) != (j2 - j1):
                bad.append((code, f, tag, a[i1:i2][:2], b[j1:j2][:2])); continue
            for x, y in zip(a[i1:i2], b[j1:j2]):
                mx = re.search(r' number="([^"]*)"', x); my = re.search(r' number="([^"]*)"', y)
                if not (mx and my and x.replace(mx.group(0), "") == y.replace(my.group(0), "")):
                    bad.append((code, f, "line", x[:120], y[:120]))
                else:
                    nchanges += 1; changes[(mx.group(1), my.group(1))] += 1
    if changed_here:
        mods.append(code); pages += [code + "/" + f for f in changed_here]
open(os.path.join(HERE, "_r369_changed_modules.txt"), "w").write("\n".join(mods) + "\n")
open(os.path.join(HERE, "_r369_changed_pages.txt"), "w").write("\n".join(pages) + "\n")
print("changed modules", len(mods), "pages", len(pages), "number attrs changed", nchanges, "non-number diff lines", len(bad))
for b in bad[:10]: print("  BAD", b)
print("top changes:", changes.most_common(12))
