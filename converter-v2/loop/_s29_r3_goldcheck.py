#!/usr/bin/env python3
"""Session 29 Round 3 PICK — for every empty task bundle whose forward walk ends at a TABLE (the `h p T` shapes in
_s29_r3_headwalk_T.log), how does the paired GOLD page render the heading + table?  For each row: is the heading text
on the gold page, at what tag, is it inside an activity box (a `class="activity` open within 800 chars before it),
does a BUILT task widget follow it within the box, and is the writer's table kept as <table>?  Same for Claude."""
import os, re, sys, html
HERE = os.path.dirname(os.path.abspath(__file__)); TESTS = os.path.join(HERE, "..", "reference", "tests")
sys.path.insert(0, TESTS)
import _corpus, _discrepancy_audit as da
CLAUDE, HUMAN = da.CLAUDE, da.HUMAN
WIDGET = re.compile(r'class="[^"]*\b(dragAndDrop|dropQuiz|mcqOptions|flipCard|clickDrop|carousel|selfCheck|typing|reorder|selectionBox|wordDrag|accordion|tabs|hintSlider|TKmodal)\b', re.I)
def fold(s):
    s = html.unescape(re.sub(r"<[^>]+>", " ", s)); s = s.replace("**", "").replace("*", "")
    return re.sub(r"[^a-z0-9āēīōū]+", " ", s.lower()).strip()
def find_head(page, htext):
    key = fold(htext)[:40]
    if not key: return None
    for m in re.finditer(r"<(h[1-6]|p)([^>]*)>(.*?)</\1>", page, re.S):
        if fold(m.group(3)).startswith(key): return m
    return None
def report(page, htext):
    m = find_head(page, htext)
    if not m: return "head:ABSENT"
    before = page[max(0, m.start() - 800):m.start()]
    in_act = 'class="activity' in before and before.rfind('class="activity') > before.rfind("</div>\n</div>\n</div>")
    # nearer test: the last activity open is not followed by a matching close before the heading — approximate by depth
    seg = page[before.rfind('class="activity') + m.start() - min(800, m.start()) if 'class="activity' in before else 0: m.start()]
    depth = seg.count("<div") - seg.count("</div>") if 'class="activity' in before else -9
    after = page[m.end():m.end() + 3500]
    w = WIDGET.search(after); t = re.search(r"<table", after)
    wpos = w.start() if w else 10**9; tpos = t.start() if t else 10**9
    nxt = "widget:" + w.group(1) if wpos < tpos else ("table" if t else "neither")
    return f"head:{m.group(1)} act:{'IN' if depth > 0 else 'out'} next:{nxt}"
rows = []
SRC = sys.argv[1] if len(sys.argv) > 1 else "_s29_r3_headwalk_T.log"
for line in open(os.path.join(HERE, SRC), encoding="utf-8", errors="replace"):
    f = line.rstrip("\n").split("\t")
    if len(f) < 9 or not f[3].endswith("T"): continue
    code, label, typ, htext = f[0], f[1], f[2], re.sub(r"^head«|»$", "", f[8])
    cf = f"{code}_{label.replace('.', '_')}.html"
    pr = {os.path.basename(t[1]): t[2] for t in da.pairs(code)}; hf = pr.get(cf)
    cpath = os.path.join(_corpus.mdir(CLAUDE, code), cf); hpath = hf
    g = report(open(hpath, encoding="utf-8", errors="replace").read(), htext) if hpath and os.path.exists(hpath) else "gold:UNPAIRED"
    c = report(open(cpath, encoding="utf-8", errors="replace").read(), htext) if os.path.exists(cpath) else "claude:MISSING"
    print(f"{code}\t{label}\t{typ:14s}\tGOLD {g:44s}\tCLAUDE {c}\t«{htext[:40]}»")
