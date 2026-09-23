#!/usr/bin/env python3
"""Round 448 — prove the change is INSIDE the hand-off boxes only: for every changed .html page, remove every
<div class="cv2-interactive …"> subtree (depth-balanced) from the disk page (r447) and the ON page (_r448_on), then
compare the rest byte-for-byte. Also counts the ✅ added per page and the pages / modules touched."""
import os, re, io, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
pages = [l.strip() for l in io.open(os.path.join(HERE, "_r448_ON_pages.txt"), encoding="utf-8") if l.strip()]
TAG = re.compile(r"<(/?)div\b([^>]*)>", re.I)
def strip_boxes(s):
    out, i, depth, start = [], 0, 0, None
    stack = []
    for m in TAG.finditer(s):
        closing = m.group(1) == "/"
        if not closing:
            is_box = 'class="cv2-interactive' in m.group(2)
            stack.append(is_box)
            if is_box and start is None:
                start = m.start(); out.append(s[i:start])
        else:
            if not stack: continue
            was_box = stack.pop()
            if start is not None and was_box and not any(stack_b for stack_b in stack if stack_b):
                i = m.end(); start = None
    out.append(s[i:] if start is None else "")
    return "".join(out)
bad = []; ticks = 0; html = txt = 0; mods = set()
for p in pages:
    code, fn = p.split("/", 1); mods.add(code)
    d = glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code, fn)) + glob.glob(os.path.join(ROOT, "01-Claude_Modules_", code, fn))
    o = os.path.join(HERE, "_r448_on", code, fn)
    a = io.open(d[0], encoding="utf-8").read(); b = io.open(o, encoding="utf-8").read()
    ticks += b.count("✅") - a.count("✅")
    if fn.endswith(".txt"): txt += 1; continue
    html += 1
    if strip_boxes(a) != strip_boxes(b): bad.append(p)
print(f"changed files {len(pages)} (html {html}, worklists {txt}) / modules {len(mods)}; ticks added {ticks}")
print(f"html pages whose content OUTSIDE the hand-off boxes differs: {len(bad)}")
for p in bad[:20]: print("  ", p)
