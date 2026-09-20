#!/usr/bin/env python3
"""_s29_r5_nestbox.py — the NESTED ACTIVITY BOX class (session 29 Round 5 PICK).
Claude ships an `activity` box INSIDE another `activity` box on 94 pages / 65 modules; the gold on 3 pages.
For every Claude nested (outer, inner) pair on a PAIRED page: take the inner box's text lines, find them in the
gold page, and report which gold container holds them — the box carrying the OUTER's number (→ the synthetic
inner box must be SUPPRESSED, the widget belongs to the open box), a box with ANOTHER number (→ the outer must
CLOSE first, the inner is its own box), or no box at all. Per template | subject group.
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r5_nestbox.py
"""
import os, re, sys, json, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.abspath(os.path.join(HERE, "..", "..", "01-Claude_Modules_"))
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]

def strip_tags(s): return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()
def fold(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()

def divs(html):
    """(open/close events) over div tags with a balanced walk; yields (start, end, cls, number) for every div."""
    out = []; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop(); out.append((st[0], m.end(), st[1], st[2], st[3]))
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            stack.append((m.start(), c, num.group(1) if num else None, m.end()))
    return out

def is_act(c): return bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c

def nested_pairs(html):
    ds = divs(html)
    acts = [d for d in ds if is_act(d[2])]
    pairs = []
    for inner in acts:
        outers = [o for o in acts if o is not inner and o[0] < inner[0] and o[1] > inner[1]]
        if outers:
            outer = max(outers, key=lambda o: o[0])   # nearest enclosing box
            pairs.append((outer, inner, html[inner[4]:inner[1]]))
    return pairs

def gold_box_for(gold, needle_lines):
    """the gold activity box (number) whose text contains the FIRST found needle; None when the text is in no box; 'ABSENT' when not found"""
    ds = divs(gold)
    acts = [d for d in ds if is_act(d[2])]
    gf = fold(strip_tags(gold))
    for ln in needle_lines:
        if ln not in gf: continue
        # find the position via the folded text is lossy — use the raw text search on a tolerant regex instead
        words = ln.split()
        pat = r"\W+".join(re.escape(w) for w in words[:8])
        m = re.search(pat, gold, re.I)
        if not m: continue
        holders = [a for a in acts if a[0] < m.start() < a[1]]
        if not holders: return ("NOBOX", ln)
        h = max(holders, key=lambda a: a[0])
        return (h[3] or "-", ln)
    return ("ABSENT", None)

mods = _corpus.gate_mods(CLAUDE)
tot = collections.Counter(); bygrp = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
pages_seen = set(); mods_seen = set()
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); grp = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read()
        except Exception: continue
        bi = c.find('id="body"'); cb = c[bi:] if bi >= 0 else c
        prs_ = nested_pairs(cb)
        if not prs_: continue
        try: g = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        for outer, inner, inner_html in prs_:
            # needle lines = visible text lines of the inner box (outside the cv2 dump's chrome), ≥ 5 words
            lines = [fold(strip_tags(x)) for x in re.findall(r"<(?:p|li|h\d|td|th)[^>]*>([\s\S]*?)</(?:p|li|h\d|td|th)>", inner_html)]
            lines = [l for l in lines if len(l.split()) >= 4 and "writers note" not in l and "interactive un built" not in l and "designer developer" not in l and "see " not in l[:80]]
            verdict, ln = gold_box_for(g, lines)
            if verdict == "ABSENT": k = "ABSENT (inner text not in gold)"; ln = " || ".join(l[:40] for l in lines[:2])
            elif verdict == "NOBOX": k = "gold: in NO box"
            elif verdict == (outer[3] or "-"): k = "gold: in the OUTER's box (same number)"
            elif verdict == (inner[3] or "-"): k = "gold: in its OWN box (the inner's number)"
            else: k = "gold: in ANOTHER box (%s)" % ("other number")
            tot[k] += 1; bygrp[grp][k] += 1; pages_seen.add(cp); mods_seen.add(code)
            if len(ex[k]) < 6: ex[k].append("%s %s>%s [%s] %s" % (os.path.basename(cp), outer[3], inner[3], verdict, (ln or "")[:50]))
print("nested pairs on paired pages: %d | pages %d | modules %d" % (sum(tot.values()), len(pages_seen), len(mods_seen)))
for k, v in tot.most_common():
    print("%4d  %s" % (v, k))
    for e in ex[k]: print("        ", e)
print("\nby template | subject:")
for g, cnt in sorted(bygrp.items(), key=lambda x: -sum(x[1].values())):
    print("  %-14s %-28s %s" % (g[0], g[1][:28], dict(cnt)))
