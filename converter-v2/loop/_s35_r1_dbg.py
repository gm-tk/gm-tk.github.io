#!/usr/bin/env python3
import re, glob, os
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
code = "CEDR401"
gdir = glob.glob(R + "01-Finalized_Modules_/*/" + code + "/")[0]
wt = ""
for t in glob.glob(gdir + "*parsed.txt"):
    wt += open(t, encoding="utf-8", errors="replace").read()
OPEN = re.compile(r'\[\s*(?:tab|new side tab|new tab|phase|lesson)\s*\d*\s*\]', re.I)
for line in wt.split("\n"):
    m = re.search(r'\[/RED TEXT\]\s*🔴?\s*(.+)$', line)
    if m and OPEN.search(line):
        lab = re.sub(r'\*+', '', m.group(1)).strip()
        print(repr(line[:80]), "->", repr(lab), "opener-in-label:", bool(OPEN.search(lab)))
ch = open(glob.glob(R + "01-Claude_Modules_/*/" + code + "/*_0_0.html")[0], encoding="utf-8").read()
for m in re.finditer(r'<p><b>(.*?)</b></p>', ch, re.S):
    if 'Surprises' in m.group(1):
        print("pb at", m.start(), repr(m.group(1)))
bx = []
for m in re.finditer(r'<div class="cv2-interactive"', ch):
    i = m.start(); depth = 0; j = i
    for t in re.finditer(r'<div\b|</div>', ch[i:]):
        if t.group(0) == '</div>':
            depth -= 1
            if depth == 0:
                j = i + t.end(); break
        else:
            depth += 1
    bx.append((i, j))
print("boxes:", len(bx), [b for b in bx if b[0] < 60000 < b[1] or (b[0] <= 57000)][:3], "...")
for a, b in bx:
    if a <= 55000 and b >= 55000:
        print("box spanning 55000:", a, b)
pos = [m.start() for m in re.finditer(r'<p><b>Surprises in the data</b></p>', ch)]
print("positions:", pos, [ (a,b) for a,b in bx if any(a<=p<b for p in pos)])
