#!/usr/bin/env python3
"""Round 449 — every writer word of a typing hand-off box (the disk page, r448) must reappear once the box is built:
in the typing widget's visible text, in its answer= values, in the lead paragraphs just before it, or in the red
Writers Note after it. Compares, per changed .html page, the words of the r448 box's member dump (banner line
excluded) with the words of the built region of the ON page (outputs/_r449_on). Prints any lost word."""
import os, re, io, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
pages = [l.strip() for l in io.open(os.path.join(HERE, "_r449_ON_pages.txt"), encoding="utf-8") if l.strip() and l.strip().endswith(".html")]
W = lambda s: collections.Counter(w.lower() for w in re.findall(r"[\w’']+", html.unescape(re.sub(r"<[^>]+>", " ", s))))
def box_text(page):
    # the r448 hand-off box of the typing bundle: from its banner to the box end (nested divs balanced)
    m = re.search(r'<p style="color: #d9480f; font-weight: bold">⚙ INTERACTIVE \(un-built\) #\d+: typing[^<]*</p>', page)
    if not m: return None
    start = page.rfind('<div class="cv2-interactive', 0, m.start())
    depth, i = 0, start
    for t in re.finditer(r"<(/?)div\b[^>]*>", page[start:]):
        depth += -1 if t.group(1) else 1
        if depth == 0: i = start + t.end(); break
    inner = page[m.end():i]
    inner = re.sub(r'<p class="cv2-note"[^>]*>.*?</p>', " ", inner, flags=re.S)   # notes render after the widget either way
    return inner
def built_text(page):
    m = re.search(r'<div class="typing[^"]*" layout="standardNoBorder">', page)
    if not m: return None
    s = page[max(0, m.start() - 1500):m.start()]
    lead = " ".join(re.findall(r"<p>(.*?)</p>", s)[-3:])
    rest = page[m.start():m.start() + 20000]
    end = rest.find('<div class="activityButton showAnswer hidden">')
    body = rest[:end if end > 0 else len(rest)]
    ans = " ".join(re.findall(r'answer="([^"]*)"', body))
    return lead + " " + body + " " + ans
bad = 0
for p in pages:
    code, fn = p.split("/", 1)
    d = (glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code, fn)) or [None])[0]
    a = io.open(d, encoding="utf-8").read(); b = io.open(os.path.join(HERE, "_r449_on", code, fn), encoding="utf-8").read()
    bt, nt = box_text(a), built_text(b)
    if bt is None or nt is None: print(f"{p}: box {'found' if bt else 'MISSING'} / widget {'found' if nt else 'MISSING'}"); continue
    A, B = W(bt), W(nt)
    lost = {w: n - B.get(w, 0) for w, n in A.items() if n > B.get(w, 0)}
    if lost: bad += 1
    print(f"{p}: box words {sum(A.values())}, built-region words {sum(B.values())}, LOST {lost if lost else 'none'}")
print(f"pages with a lost word: {bad} of {len(pages)}")
