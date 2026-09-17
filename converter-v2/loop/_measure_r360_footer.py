#!/usr/bin/env python3
"""ROUND 360 PICK probe (loop session 19, Round 4 — the diff miner's FOOTER facts F26 / F28 / F35 / F36 / F37 / F38):
THE FOOTER LINK SET AND THE FOOTER CLASS per registry group and page POSITION — the r357 instrument on the registry's
pattern fields `footer_links` {overview, lesson, final} and `footer_class`.

For every paired page of the gate's population: the page's POSITION on each side (overview = the first page; final = the
side's own last content page — acks / glossary pages excluded; lesson = every other page), the gold footer's ordered link
keys (prev-lesson / next-lesson / home-nav) and `<ul>` class, Claude's, and the value the registry RESOLVES for that
position (outputs/_r359_resolved.json: footer_links + footer_class). Aggregated per (template, base, position): the gold's
dominant link SET (order-insensitive) + its share, the gold's dominant ORDER, the gold's dominant ul class, Claude's
dominant set / class, the resolved value, and a CLASS flag when the gold solidifies (>= 0.60) and Claude's set disagrees on
>= 0.50 of the group's pages (the same for the class). Also the single-page census: Fundamentals modules with ONE content
page — the gold's link set there (06 §3.3 'fundamentals-nav — typically home-nav only').
Run under WSL from anywhere: python3 _measure_r360_footer.py -> _r360_footer.{json,log}
"""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path:
        sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs, pkey
from anchor_compare import CLAUDE, HUMAN

res = json.load(open(os.path.join(HERE, "_r359_resolved.json"), encoding="utf-8"))
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)


def footer(html):
    m = re.search(r'<div id="footer">([\s\S]*?)</div>', html)
    if not m:
        m = re.search(r'<nav id="module-foot">([\s\S]*?)</nav>', html)
        if not m:
            return None
    f = m.group(1)
    ul = re.search(r'<ul class="([^"]*)"', f)
    keys = []
    for a in re.finditer(r"<a\b([^>]*)>", f):
        attrs = a.group(1)
        if 'id="prev-lesson"' in attrs:
            keys.append("prev")
        elif 'id="next-lesson"' in attrs:
            keys.append("next")
        elif "home-nav" in attrs:
            keys.append("home")
        else:
            keys.append("other")
    return {"cls": " ".join(sorted((ul.group(1) if ul else "").split())), "keys": keys, "set": "+".join(sorted(set(keys))) or "none"}


def base_of(code):
    m = re.match(r"([A-Z]+)", code)
    return m.group(1) if m else code


rows = []
codes = sorted(c for c in _corpus.gate_mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, c)))
for code in codes:
    gdir = _corpus.mdir(HUMAN, code); cdir = _corpus.mdir(CLAUDE, code)
    tmpl = os.path.basename(os.path.dirname(gdir))
    gpages = sorted((f for f in os.listdir(gdir) if f.endswith(".html") and not SKIP.search(f)), key=lambda f: pkey(f, code))
    cpages = sorted((f for f in os.listdir(cdir) if f.endswith(".html") and not re.search(r"acks|acknowledge|glossary", f, re.I)), key=lambda f: pkey(f, code))
    glast = gpages[-1] if gpages else None; clast = cpages[-1] if cpages else None
    fl = res.get(code, {}).get("footer_links") or {}; fc = res.get(code, {}).get("footer_class")
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or re.search(r"acks|acknowledge|glossary", os.path.basename(cp), re.I):
            continue
        gpos = "overview" if n == 0 else ("final" if os.path.basename(hp) == glast else "lesson")
        cpos = "overview" if n == 0 else ("final" if os.path.basename(cp) == clast else "lesson")
        g = footer(open(hp, encoding="utf-8", errors="replace").read()) or {"cls": "(no footer)", "keys": [], "set": "none"}
        c = footer(open(cp, encoding="utf-8", errors="replace").read()) or {"cls": "(no footer)", "keys": [], "set": "none"}
        rows.append({"module": code, "template": tmpl, "base": base_of(code), "page": os.path.basename(cp), "gold_page": os.path.basename(hp),
                     "gpos": gpos, "cpos": cpos, "gold_set": g["set"], "gold_order": ",".join(g["keys"]), "gold_cls": g["cls"],
                     "claude_set": c["set"], "claude_order": ",".join(c["keys"]), "claude_cls": c["cls"],
                     "resolved": fl.get(cpos if cpos != "final" or fl.get("final") else "lesson"), "resolved_final": fl.get("final"), "resolved_cls": fc,
                     "single_page_gold": len(gpages) == 1, "single_page_claude": len(cpages) == 1})

# ---- aggregate per (template, base, gold position)
groups = collections.defaultdict(list)
for r in rows:
    groups[(r["template"], r["base"], r["gpos"])].append(r)
out = []
for k, rs in sorted(groups.items()):
    n = len(rs)
    gs = collections.Counter(r["gold_set"] for r in rs).most_common(); cs = collections.Counter(r["claude_set"] for r in rs).most_common()
    go = collections.Counter(r["gold_order"] for r in rs).most_common(2)
    gc = collections.Counter(r["gold_cls"] for r in rs).most_common(); cc = collections.Counter(r["claude_cls"] for r in rs).most_common()
    dis_set = sum(1 for r in rs if r["gold_set"] != r["claude_set"]); dis_cls = sum(1 for r in rs if r["gold_cls"] != r["claude_cls"])
    gshare = gs[0][1] / n; cshare_g = gc[0][1] / n
    flag_set = "CLASS" if (gshare >= 0.60 and dis_set / n >= 0.50 and gs[0][0] != cs[0][0]) else ("part" if dis_set else "")
    flag_cls = "CLASS" if (cshare_g >= 0.60 and dis_cls / n >= 0.50 and gc[0][0] != cc[0][0]) else ("part" if dis_cls else "")
    out.append({"template": k[0], "base": k[1], "pos": k[2], "pages": n, "modules": len({r["module"] for r in rs}),
                "gold_set": gs[0][0], "gold_set_share": round(gshare, 2), "gold_sets": dict(gs), "gold_order": go[0][0], "gold_orders": dict(go),
                "claude_set": cs[0][0], "claude_sets": dict(cs), "resolved": dict(collections.Counter(str(r["resolved"]) for r in rs)),
                "gold_cls": gc[0][0], "gold_cls_share": round(cshare_g, 2), "claude_cls": cc[0][0], "resolved_cls": dict(collections.Counter(str(r["resolved_cls"]) for r in rs)),
                "disagree_set": dis_set, "disagree_cls": dis_cls, "flag_set": flag_set, "flag_cls": flag_cls,
                "module_list": sorted({r["module"] for r in rs}), "samples": [f"{r['module']}/{r['page']} gold {r['gold_order']}({r['gold_cls']}) claude {r['claude_order']}({r['claude_cls']}) resolved {r['resolved']}/{r['resolved_cls']}" for r in rs if r["gold_set"] != r["claude_set"] or r["gold_cls"] != r["claude_cls"]][:3]})

L = [f"r360 footer probe — {len(rows)} paired pages / {len(codes)} modules / {len(out)} (template, base, position) groups"]
cls_set = [o for o in out if o["flag_set"] == "CLASS"]; cls_cls = [o for o in out if o["flag_cls"] == "CLASS"]
L.append(f"LINK-SET CLASS rows: {len(cls_set)} — modules {len({m for o in cls_set for m in o['module_list']})}, disagreeing pages {sum(o['disagree_set'] for o in cls_set)}")
for o in cls_set:
    L.append(f"  SET  {o['template']:12} {o['base']:7} {o['pos']:8} n={o['pages']:3} mods={o['modules']:2} gold {o['gold_set']} {o['gold_set_share']:.2f} {o['gold_sets']} order {o['gold_order']} | claude {o['claude_set']} {o['claude_sets']} | resolved {o['resolved']} | e.g. {o['samples'][:1]}")
L.append(f"FOOTER-CLASS CLASS rows: {len(cls_cls)} — modules {len({m for o in cls_cls for m in o['module_list']})}, disagreeing pages {sum(o['disagree_cls'] for o in cls_cls)}")
for o in cls_cls:
    L.append(f"  CLS  {o['template']:12} {o['base']:7} {o['pos']:8} n={o['pages']:3} mods={o['modules']:2} gold '{o['gold_cls']}' {o['gold_cls_share']:.2f} | claude '{o['claude_cls']}' | resolved {o['resolved_cls']} | e.g. {o['samples'][:1]}")
L.append("")
L.append("PARTIAL rows (some disagreement):")
for o in out:
    if (o["flag_set"] == "part" or o["flag_cls"] == "part") and o["flag_set"] != "CLASS" and o["flag_cls"] != "CLASS":
        L.append(f"  part {o['template']:12} {o['base']:7} {o['pos']:8} n={o['pages']:3} gold {o['gold_set']} {o['gold_set_share']:.2f} '{o['gold_cls']}' | claude {o['claude_set']} '{o['claude_cls']}' | dis set {o['disagree_set']} cls {o['disagree_cls']} | resolved {o['resolved']}")
L.append("")
single = [r for r in rows if r["gpos"] == "overview" and r["single_page_gold"]]
L.append(f"SINGLE-PAGE modules (gold has ONE content page): {len(single)} — gold link sets {dict(collections.Counter(r['gold_set'] for r in single))}; by template {dict(collections.Counter((r['template'], r['gold_set']) for r in single))}")
L.append(f"  Claude on those: {dict(collections.Counter(r['claude_set'] for r in single))}; Claude single-page too: {sum(1 for r in single if r['single_page_claude'])}")
open(os.path.join(HERE, "_r360_footer.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
json.dump({"rows": rows, "groups": out}, open(os.path.join(HERE, "_r360_footer.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
print("\n".join(L)); print(f"wrote _r360_footer.json / .log")
