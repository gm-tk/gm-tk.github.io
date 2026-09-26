#!/usr/bin/env python3
"""_s52_r2_sumbox.py — session 52 Round 2: in the GOLD, every alert box that opens with a summary heading — does it hold a
hint (p.hintLink), and does a hint follow right after it; what does the box hold (child tags); per family. Regex-level, WSL:
    python3 _s52_r2_sumbox.py"""
import os, re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_"
PAT = re.compile(r"<h([2-5])[^>]*>\s*(lesson summary|key points|key questions|summary|what have we learned)\s*[:?.]?\s*</h\1>", re.I)
st = collections.defaultdict(collections.Counter)
for f in glob.glob(R + "/*/*/*.html"):
    mod = f.split("/")[-2]; fam = re.sub(r"\d.*$", "", mod)
    s = open(f, encoding="utf-8", errors="replace").read()
    for m in PAT.finditer(s):
        # the innermost open alert before the heading
        a = s.rfind('<div class="alert', 0, m.start())
        if a < 0 or m.start() - a > 200: st[fam]["not-in-alert"] += 1; continue
        # the alert's close
        re_ = re.compile(r"<(/?)div\b[^>]*>", re.I); d = 0; end = None
        for c in re_.finditer(s, a):
            d += -1 if c.group(1) else 1
            if d == 0: end = c.end(); break
        if end is None: continue
        box = s[a:end]; after = s[end:end + 400]
        st[fam]["boxed"] += 1
        st[fam]["hint-inside" if "hintLink" in box else "no-hint-inside"] += 1
        if "hintLink" in after: st[fam]["hint-right-after"] += 1
        st[fam]["box-ends-page" if re.match(r"\s*(?:</div>\s*)*<div id=\"footer\"", after) else "content-after"] += 1
        inner = box[box.find(m.group(0)) + len(m.group(0)):]
        kids = re.findall(r"<(p|ul|ol|img|div|h[1-6]|table|iframe)\b([^>]*)>", inner)
        seq = []
        depth_skip = False
        for t, attrs in kids:
            k = t + (".hint" if "hintLink" in attrs else "")
            if t == "div": continue
            if seq and seq[-1] == k: continue
            seq.append(k)
        st[fam]["SEQ " + " ".join(seq[:5])] += 1
for fam, c in sorted(st.items(), key=lambda x: -sum(x[1].values())):
    print(f"{fam:8s} " + ", ".join(f"{k} {v}" for k, v in c.most_common()))
