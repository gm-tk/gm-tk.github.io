#!/usr/bin/env python3
"""Session 40 Round 5 PICK measure — the r61 alert-title MISSES. For every Claude page, each .alert box whose FIRST
paragraph (optionally inside row > col) is a short plain <p> (<= 45 chars of text, not a red note) with another block
after it — exactly the r61 rule's own test, applied PER ALERT — but which ships as <p> rather than <h4>: the
regex's backtracking swallowed it (an earlier alert whose first <p> is a long / empty-flag paragraph extends its lazy
match across elements). Counts pages / modules and, where the page pairs, what the gold does with that text."""
import os, re, io, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
OPEN = re.compile(r'<div class="alert[^"]*">\s*(?:<div class="row">\s*<div class="col[^"]*">\s*)?<p(\b[^>]*)>([\s\S]*?)</p>(\s*<[^/])')
miss = []; ok = 0
for f in glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*.html")):
    s = io.open(f, encoding="utf-8", errors="replace").read()
    for m in re.finditer(r'<div class="alert[^"]*">', s):
        seg = s[m.start():m.start() + 4000]
        mm = OPEN.match(seg)
        if not mm: continue
        attrs, inner = mm.group(1), mm.group(2)
        if "</p>" in inner or "<p" in inner: continue            # the lazy match ran past its own paragraph
        text = re.sub(r"<[^>]+>", " ", inner); text = re.sub(r"&[a-z]+;", " ", text).strip()
        if "cv2-note" in attrs or not text or len(text) > 45: continue
        miss.append((f, text))
code = lambda f: os.path.basename(os.path.dirname(f))
print(f"alert first paragraphs still <p> though they pass the r61 test: {len(miss)} on {len({f for f, _ in miss})} pages / {len({code(f) for f, _ in miss})} modules")
gold_h = collections.Counter()
for f, t in miss:
    g = glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code(f), "*.html"))
    esc = re.escape(t[:30])
    form = "not found"
    for gf in g:
        gs = io.open(gf, encoding="utf-8", errors="replace").read()
        mm = re.search(r"<(h[1-6]|p|strong|b)\b[^>]*>\s*(?:<[^>]+>\s*)*" + esc, gs)
        if mm: form = mm.group(1); break
    gold_h[form] += 1
print("the gold's own tag for the same text:", dict(gold_h))
for f, t in miss[:25]: print(f"  {code(f)}/{os.path.basename(f)}: {t!r}")
