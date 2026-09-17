#!/usr/bin/env python3
"""ROUND 362 PICK probe (loop session 19, Round 6 — the DIFF MINER's activity classes #542 / #535 / #533 / #541):
THE ACTIVITY BOX'S LEADING HEADING AND INSTRUCTION vs THE INTERACTIVE CAPTURE.

For every paired page of the gate's population, the activity boxes on both sides keyed by their `number` attribute
(the balanced div extent of each box). For each number present on both sides: the gold box's leading children
(tags before its first widget / interactive), Claude's leading children, and whether Claude's box OPENS with a
`cv2-interactive` (an unbuilt / unclassified capture) or a built widget while the gold opens with an h3 (+ p) —
and whether that gold heading text sits INSIDE Claude's capture (swallowed) or is absent altogether.
Aggregated by template, subject and the capture's classification span. Run under WSL from anywhere:
  python3 _measure_r362_actlead.py -> _r362_actlead.{json,log}
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN

TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
VOID = {"br", "img", "input", "meta", "link", "hr", "source", "wbr"}


def boxes(html):
    """activity boxes: (number, classes, inner_html) via a balanced-div scan."""
    out = []
    for m in re.finditer(r'<div class="(activity[^"]*)"([^>]*)>', html):
        num = re.search(r'number="([^"]*)"', m.group(2))
        depth = 1; pos = m.end()
        for t in TAG.finditer(html, m.end()):
            if t.group(2).lower() != "div": continue
            if t.group(1): depth -= 1
            else: depth += 1
            if depth == 0: pos = t.start(); break
        out.append((num.group(1) if num else None, m.group(1), html[m.end():pos]))
    return out


def lead(inner, side):
    """the leading element sequence of a box (skipping row/col wrappers) up to and including its first widget."""
    seq = []
    for t in TAG.finditer(inner):
        if t.group(1): continue
        tag = t.group(2).lower(); attrs = t.group(3)
        cls = re.search(r'class="([^"]*)"', attrs); cl = (cls.group(1) if cls else "").split()
        if tag == "div" and cl and cl[0] in ("row", "col-12", "col-md-8", "col-md-4", "col-md-6", "col-md-12", "col-md-10", "col-md-3", "col-6"): continue
        if tag == "div" and not cl: continue
        if tag in ("h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "img", "a", "table", "iframe", "span", "b", "i"):
            if tag == "span" and side == "claude" and "cv2-int" in " ".join(cl): continue
            txt = re.sub(r"<[^>]+>", "", inner[t.end(): t.end() + 200]).strip()[:40]
            seq.append((tag, txt))
        elif tag == "div":
            seq.append(("WIDGET:" + cl[0], ""))
            break
        if len(seq) >= 6: break
    return seq


def norm(s): return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


rows = []
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code); tmpl = os.path.basename(os.path.dirname(gdir))
    subj = None
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I): continue
        gh = open(hp, encoding="utf-8", errors="replace").read(); ch = open(cp, encoding="utf-8", errors="replace").read()
        gb = {b[0]: b for b in boxes(gh) if b[0]}; cb = {b[0]: b for b in boxes(ch) if b[0]}
        for num in gb:
            if num not in cb: continue
            gl = lead(gb[num][2], "gold"); cl = lead(cb[num][2], "claude")
            g_first = gl[0][0] if gl else "none"; c_first = cl[0][0] if cl else "none"
            g_h3 = next((t for t in gl if t[0] == "h3"), None)
            swallowed = None
            if g_h3 and c_first.startswith("WIDGET"):
                swallowed = norm(g_h3[1]) in norm(re.sub(r"<[^>]+>", " ", cb[num][2]))
            rows.append({"module": code, "template": tmpl, "page": os.path.basename(cp), "number": num,
                         "gold_lead": [t[0] for t in gl][:4], "claude_lead": [t[0] for t in cl][:4],
                         "gold_h3": g_h3[1] if g_h3 else None, "claude_first": c_first, "gold_first": g_first,
                         "swallowed": swallowed, "claude_classes": cb[num][1], "gold_classes": gb[num][1]})

L = [f"r362 activity-lead probe — {len(rows)} number-paired activity boxes / {len(codes)} modules"]
by = collections.Counter((r["gold_first"], r["claude_first"].split(":")[0]) for r in rows)
L.append("gold-first × claude-first: " + str(by.most_common(14)))
cls = [r for r in rows if r["gold_first"] == "h3" and r["claude_first"].startswith("WIDGET")]
L.append(f"CLASS — gold box opens with h3, Claude's opens with a widget/capture: {len(cls)} boxes / {len({r['module'] for r in cls})} modules / {len({(r['module'], r['page']) for r in cls})} pages")
L.append("  swallowed (gold h3 text inside Claude's box): " + str(collections.Counter(r["swallowed"] for r in cls)))
L.append("  Claude's opening widget: " + str(collections.Counter(r["claude_first"] for r in cls).most_common(8)))
L.append("  by template: " + str(collections.Counter(r["template"] for r in cls)))
L.append("  by base: " + str(collections.Counter(re.match(r"[A-Z]+", r["module"]).group(0) for r in cls).most_common(14)))
sw = [r for r in cls if r["swallowed"]]
L.append(f"SWALLOWED subset: {len(sw)} boxes / {len({r['module'] for r in sw})} modules — opening widget " + str(collections.Counter(r["claude_first"] for r in sw).most_common(6)))
L.append("  examples: " + "; ".join(f"{r['module']}/{r['page']} #{r['number']} «{r['gold_h3'][:30]}» → {r['claude_first']}" for r in sw[:12]))
cls2 = [r for r in rows if r["gold_first"] == "h3" and r["claude_first"] != "h3" and not r["claude_first"].startswith("WIDGET")]
L.append(f"OTHER — gold opens with h3, Claude opens with {collections.Counter(r['claude_first'] for r in cls2).most_common(6)}: {len(cls2)} boxes")
same = sum(1 for r in rows if r["gold_first"] == r["claude_first"] == "h3")
L.append(f"AGREE — both open with h3: {same} boxes")
open(os.path.join(HERE, "_r362_actlead.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(rows, open(os.path.join(HERE, "_r362_actlead.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\n".join(L))
