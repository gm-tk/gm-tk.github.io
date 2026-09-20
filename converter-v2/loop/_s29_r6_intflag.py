#!/usr/bin/env python3
"""_s29_r6_intflag.py — the activity box's `interactive` class, paired by NUMBER (DIFF_QUEUE #587 / #606: gold
`activity interactive` vs Claude `activity` on 247 pages and the reverse on 114).
For every paired page: every gold box and Claude box keyed by its number= id (first occurrence on the page); for the
pairs, tabulate (gold interactive?, Claude interactive?) by what Claude's box holds — the widget marker kinds inside it
(cv2 hand-off dump type from its "INTERACTIVE (un-built) #n: TYPE" line, a built widget class, or none) — and by group.
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r6_intflag.py
"""
import os, re, sys, json, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.abspath(os.path.join(HERE, "..", "..", "01-Claude_Modules_"))
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
BUILT = ["dragAndDrop", "clickDrop", "flipCard", "accordion", "carousel", "dropQuiz", "mcqOptions", "speechBubble", "tabs", "hintSlider", "TKmodal", "selfCheck", "shapeHover", "rotateBanner", "wordDrag", "memoryGame"]

def boxes(html):
    """{number: (interactive?, inner_html)} for every activity div (first occurrence per number)."""
    out = {}; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop()
                if st[1] is not None and st[1] not in out: out[st[1]] = (st[2], html[st[3]:m.start()])
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            isact = bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c
            stack.append((c, num.group(1).upper() if (isact and num) else None, "interactive" in c.split(), m.end()))
    return out

def holds(inner):
    kinds = set()
    for t in re.findall(r"INTERACTIVE \(un-built\) #\d+: ([A-Za-z]+)", inner): kinds.add("dump:" + t)
    for b in BUILT:
        if re.search(r'class="[^"]*\b%s\b' % re.escape(b), inner): kinds.add("built:" + b)
    if not kinds: return "none"
    return "+".join(sorted(kinds))

mods = _corpus.gate_mods(CLAUDE)
tab = collections.defaultdict(collections.Counter); grp = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: gb = boxes(open(hp, encoding="utf-8", errors="replace").read()); cb = boxes(open(cp, encoding="utf-8").read())
        except Exception: continue
        for num, (ci, cinner) in cb.items():
            if num not in gb: continue
            gi = gb[num][0]
            h = holds(cinner)
            key = ("gold:int" if gi else "gold:plain") + " / " + ("claude:int" if ci else "claude:plain")
            tab[h][key] += 1; grp[g][key] += 1
            if gi != ci and len(ex[(h, key)]) < 3: ex[(h, key)].append("%s %s" % (os.path.basename(cp), num))
print("number-paired boxes by what Claude's box holds → (gold flag / Claude flag):")
for h, cnt in sorted(tab.items(), key=lambda x: -sum(x[1].values())):
    n = sum(cnt.values())
    if n < 8: continue
    print("  %-40s n=%-5d %s" % (h[:40], n, "  ".join("%s %d" % (k, v) for k, v in cnt.most_common())))
    for k in cnt:
        if (h, k) in ex: print("      e.g. %s: %s" % (k, ", ".join(ex[(h, k)])))
print("\nby group:")
for g, cnt in sorted(grp.items(), key=lambda x: -sum(x[1].values())):
    n = sum(cnt.values())
    if n < 20: continue
    print("  %-14s %-26s n=%-5d %s" % (g[0], g[1][:26], n, "  ".join("%s %d" % (k, v) for k, v in cnt.most_common())))
