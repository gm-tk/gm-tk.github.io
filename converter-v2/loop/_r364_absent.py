#!/usr/bin/env python3
"""r364 PICK — the OTHER half of the r362 residue: gold box opens with h3, Claude's with a widget, and the gold's title is
NOT inside Claude's box. Where is it on Claude's page? (a) as an element right BEFORE the box (free h3 / p / h4 — the box
opened late), (b) elsewhere on the page, (c) not on the page (editorial). Re-uses _r362_actlead.json (re-run first)."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE
def norm(s): return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", s).lower()).strip()
rows = json.load(open(os.path.join(HERE, "_r362_actlead.json"), encoding="utf-8"))
cls = [r for r in rows if r.get("gold_first") == "h3" and str(r.get("claude_first", "")).startswith("WIDGET") and r.get("swallowed") is False]
print("absent boxes", len(cls))
kinds = collections.Counter(); ex = collections.defaultdict(list); mods = collections.defaultdict(set); pages = collections.defaultdict(set)
for r in cls:
    code = r["module"]; page = r["page"]; t = norm(r["gold_h3"] or "")
    if not t: kinds["no-text"] += 1; continue
    p = os.path.join(_corpus.mdir(CLAUDE, code), page)
    h = open(p, encoding="utf-8", errors="replace").read()
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
    m = re.search(r'<div class="activity[^"]*"[^>]*number="%s"' % re.escape(r["number"]), h)
    if not m: kinds["no-box"] += 1; continue
    before = h[max(0, m.start() - 4000):m.start()]
    # the last 3 block elements before the box
    blocks = re.findall(r"<(h[1-6]|p|li)\b[^>]*>(.*?)</\1>", before, re.S)
    tail = blocks[-3:]
    hit = None
    for tag, txt in reversed(tail):
        nt = norm(txt)
        if nt == t or (len(t) > 6 and (t in nt or nt in t)):
            hit = tag; break
    if hit:
        k = "before-box:" + hit
    elif t in norm(h):
        # where? before or after the box
        pos = norm(h).find(t); boxpos = len(norm(h[:m.start()]))
        k = "elsewhere-" + ("before" if pos < boxpos else "after")
    else:
        k = "not-on-page"
    kinds[k] += 1; mods[k].add(code); pages[k].add(code + "/" + page)
    if len(ex[k]) < 6: ex[k].append((code, page, r["number"], (r["gold_h3"] or "").strip()[:50], r["claude_first"]))
for k, v in kinds.most_common():
    print(f"{v:4}  boxes / {len(mods[k])} modules / {len(pages[k])} pages  {k}")
    for e in ex[k]: print("      ", e)
