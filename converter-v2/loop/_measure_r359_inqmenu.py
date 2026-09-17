#!/usr/bin/env python3
"""ROUND 359 PICK probe (loop session 19, Round 3 — the diff miner's MODULE-MENU classes #36 / #46 / #28 / #54): THE OVERVIEW
MENU'S COLUMN FORM per template family — the gold's shape vs Claude's, page by page.

For every paired OVERVIEW page (n == 0) the module-menu region is read with the miner's own page_lines (the gate's tree) and
summarised as its COLUMN SHAPE: the sequence of direct children of the menu's div.row — each column's class + the ordered
tags of its text-bearing children (h3/h4/h5/p/ul …) — e.g. "col-md-12.paddingR[h4>span] | col-md-6.paddingR[h5>span,p,h5>span,p,ul] | col-md-6.paddingR[h5,ul,h5,ul]".
Aggregates per template family and subject: the gold's column-class sequence, the heading tag used for the section headings
(the first heading of each column) and for the labels, the presence of a full-width first row, the share of each; the same
for Claude; and per page whether Claude's shape equals the gold's.
Run under WSL from anywhere: python3 _measure_r359_inqmenu.py -> _r359_inqmenu.{json,log}
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
from _measure_ceiling import load_meta
from _diff_miner import page_lines, SKIP_PAGE, _cls

meta = load_meta()
TEXTTAGS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "ul", "ol", "li", "a", "div", "span", "b", "table"}


def column_shape(lines):
    """The menu's div.row children as [(col-class, [child roles…], texts)]."""
    menu = [l for l in lines if l.region == "module-menu"]
    content = next((l for l in menu if l.node.attrs.get("id") == "module-menu-content"), None)
    if content is None:
        return None
    rows = [k for k in content.node.kids if k.tag == "div" and "row" in _cls(k)]
    if not rows:
        return {"cols": [], "note": "no row"}
    cols = []
    for row in rows:
        for col in row.kids:
            if col.tag != "div":
                continue
            cls = ".".join(sorted(c for c in _cls(col) if c not in ("col-12",)))
            kids = []
            texts = []
            for k in col.kids:
                if _cls(k) & {"cv2-note", "cv2-comment"}:
                    continue
                role = k.tag
                inl = [x for x in k.kids if x.tag in ("span", "b")]
                if len(k.kids) == 1 and inl:
                    role += ">" + inl[0].tag
                if k.tag in ("ul", "ol"):
                    role += f"×{sum(1 for x in k.kids if x.tag == 'li')}"
                kids.append(role)
                t = " ".join(k.own).strip() or (" ".join(inl[0].own).strip() if inl else "")
                if k.tag in ("h3", "h4", "h5", "p"):
                    texts.append(t[:40])
            cols.append({"cls": cls, "kids": kids, "texts": texts})
    return {"cols": cols, "rows": len(rows)}


def sig(shape):
    if not shape or "cols" not in shape:
        return "NO MENU"
    if not shape["cols"]:
        return "empty menu"
    return " | ".join(f"{c['cls'] or 'col'}[{','.join(c['kids'])}]" for c in shape["cols"])


def heads(shape):
    """The heading tags used for section HEADINGS (first child of each column) and for the other headings."""
    if not shape or not shape.get("cols"):
        return ("", "")
    first = [c["kids"][0] for c in shape["cols"] if c["kids"]]
    other = [k for c in shape["cols"] for k in c["kids"][1:] if k.startswith("h")]
    return (",".join(first), ",".join(sorted(set(other))))


rows = []
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code); tmpl = os.path.basename(os.path.dirname(gdir))
    subject = (meta.get(code) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if n != 0 or SKIP_PAGE.search(os.path.basename(hp)):
            continue
        g, _ = page_lines(hp); c, _ = page_lines(cp)
        gs, cs = column_shape(g), column_shape(c)
        rows.append({"module": code, "template": tmpl, "subject": subject, "page": os.path.basename(cp), "gold_page": os.path.basename(hp),
                     "gold": sig(gs), "claude": sig(cs), "gold_heads": heads(gs), "claude_heads": heads(cs),
                     "gold_cols": [c["cls"] for c in (gs or {}).get("cols", [])], "claude_cols": [c["cls"] for c in (cs or {}).get("cols", [])],
                     "gold_texts": [c["texts"] for c in (gs or {}).get("cols", [])], "claude_texts": [c["texts"] for c in (cs or {}).get("cols", [])],
                     "same": sig(gs) == sig(cs)})

L = [f"r359 overview-menu column-form census — {len(rows)} paired overview pages"]
for tmpl in ("Inquiry", "Standard", "Fundamentals", "Bilingual"):
    rs = [r for r in rows if r["template"] == tmpl]
    if not rs:
        continue
    L.append(f"\n=== {tmpl}: {len(rs)} overviews; Claude shape == gold on {sum(1 for r in rs if r['same'])} ===")
    gc = collections.Counter(" | ".join(r["gold_cols"]) for r in rs)
    cc = collections.Counter(" | ".join(r["claude_cols"]) for r in rs)
    L.append("  gold column classes: " + "; ".join(f"{k or '(none)'} ×{v}" for k, v in gc.most_common(8)))
    L.append("  claude column classes: " + "; ".join(f"{k or '(none)'} ×{v}" for k, v in cc.most_common(8)))
    gh = collections.Counter(r["gold_heads"][0] for r in rs); ch = collections.Counter(r["claude_heads"][0] for r in rs)
    L.append("  gold first-child per column: " + "; ".join(f"{k or '(none)'} ×{v}" for k, v in gh.most_common(8)))
    L.append("  claude first-child per column: " + "; ".join(f"{k or '(none)'} ×{v}" for k, v in ch.most_common(8)))
    bysub = collections.defaultdict(list)
    for r in rs:
        bysub[r["subject"]].append(r)
    for sub, srs in sorted(bysub.items(), key=lambda kv: -len(kv[1])):
        gcs = collections.Counter(" | ".join(r["gold_cols"]) for r in srs).most_common(2)
        ghs = collections.Counter(r["gold_heads"][0] for r in srs).most_common(2)
        L.append(f"    {sub[:30]:30} n={len(srs):3} same={sum(1 for r in srs if r['same'])} gold cols {gcs} heads {ghs}")
L.append("\n=== Inquiry overviews, page by page ===")
for r in [x for x in rows if x["template"] == "Inquiry"]:
    L.append(f"  {r['module']:9} gold: {r['gold'][:150]}")
    L.append(f"  {'':9} clau: {r['claude'][:150]}")
    L.append(f"  {'':9} gold texts: {r['gold_texts']}"[:220])
open(os.path.join(HERE, "_r359_inqmenu.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump(rows, open(os.path.join(HERE, "_r359_inqmenu.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\n".join(L[:40])); print(f"wrote _r359_inqmenu.json / .log ({len(L)} lines)")
