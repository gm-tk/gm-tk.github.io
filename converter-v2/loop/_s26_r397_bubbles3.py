#!/usr/bin/env python3
"""Sample the gold's right+img speech-bubble rows in OS / TEDC and Claude's text-only rows on the same pages, with the WT lines.
python3 _s26_r397_bubbles3.py"""
import os, sys, re
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r396_widgetwrap.py"), encoding="utf-8").read()
exec(src[:src.index("ROOTS = ")])
from collections import Counter
ROW = re.compile(r'<div class="row speechBubble"[^>]*>')
def rows(s):
    out = []
    for m in ROW.finditer(s):
        i = m.end(); depth = 1; j = i
        for mm in re.finditer(r"<div\b|</div>", s[i:]):
            depth += 1 if mm.group(0) == "<div" else -1
            if depth == 0: j = i + mm.start(); break
        out.append(re.sub(r"\s+", " ", s[m.start():j + 6]))
    return out
shown = 0; imgs = Counter(); cols = Counter()
for code in sorted(fam):
    subj = (meta.get(code, {}) or {}).get("subject") or "None"
    if subj not in ("Online Safety (OS9000)", "None"): continue
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception: continue
        gr = [r for r in rows(gh) if "<img" in r]; cr = [r for r in rows(ch) if "<img" not in r]
        for r in gr:
            m = re.search(r'src="([^"]*)"', r); imgs[re.sub(r"\d+", "N", os.path.basename(m.group(1))) if m else "-"] += 1
            cols[" | ".join(re.findall(r'<div class="(col[^"]*)"', r)[:2])] += 1
        if gr and cr and shown < 4:
            shown += 1
            print(f"== {os.path.basename(cp)} ({subj})\n   GOLD:   {gr[0][:420]}\n   CLAUDE: {cr[0][:300]}")
print("gold character image filenames (digits→N):", imgs.most_common(12))
print("gold column layouts:", cols.most_common(6))
