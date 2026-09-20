#!/usr/bin/env python3
"""_s29_r6_colwidth.py — the gold's top-level BODY section column class by what the row holds (DIFF_QUEUE #3677:
gold `div.col-12` vs Claude `div.col-12.col-md-8`, 315 pages / 180 modules, consensus 0.55 overall).
For every PAIRED page: walk the gold's `#body > div.row` rows that hold exactly ONE column; key = (template, subject,
page type, the row's content kind = first element inside the column: heading / p / list / table / img / video /
activity / alert / widget / other) → the column class distribution. Same walk on the Claude page for comparison.
Run under WSL from CONVERTER_V2/reference/tests:  python3 ../../outputs/_s29_r6_colwidth.py
"""
import os, re, sys, json, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
CLAUDE = os.path.abspath(os.path.join(HERE, "..", "..", "01-Claude_Modules_"))
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
VOID = {"br", "img", "hr", "input", "meta", "link", "source", "wbr", "area", "base", "col", "embed", "track"}

def tokens(cls): return " ".join(sorted(cls.split()))

def body_rows(html):
    """yield (colClass, kind) for every top-level #body row holding exactly one column."""
    bi = re.search(r'<div[^>]*id="body"[^>]*>', html)
    if not bi: return []
    i = bi.end(); depth = 1; out = []
    tags = list(re.finditer(r"<(/?)(\w+)([^>]*)>", html[i:]))
    # build a simple element tree of the body region
    stack = []; rows = []
    for m in tags:
        close, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if name in VOID and not close:
            if stack: stack[-1]["kids"].append({"name": name, "attrs": attrs, "kids": [], "depth": len(stack)})
            continue
        if close:
            if not stack: break   # body closed
            node = stack.pop()
            if not stack: rows.append(node)   # a direct child of #body
            continue
        if attrs.rstrip().endswith("/"): continue
        node = {"name": name, "attrs": attrs, "kids": [], "depth": len(stack)}
        if stack: stack[-1]["kids"].append(node)
        stack.append(node)
    def cls(n):
        mm = re.search(r'class="([^"]*)"', n["attrs"]); return mm.group(1) if mm else ""
    def kind(n):
        c = cls(n); nm = n["name"]
        if re.match(r"h[1-6]$", nm): return "heading"
        if nm == "p": return "p"
        if nm in ("ul", "ol"): return "list"
        if nm == "table" or "table-responsive" in c: return "table"
        if nm == "img": return "img"
        if "videoSection" in c or nm == "iframe": return "video"
        if nm == "audio" or "audioPlayer" in c: return "audio"
        if re.search(r"(^|\s)activity(\s|$)", c): return "activity"
        if re.search(r"(^|\s)(alert|whakatauki|supervisor)(\s|$)", c): return "callout"
        if "cv2-interactive" in c: return "widget"
        if nm == "a": return "a"
        if nm == "div": return "div." + (c.split()[0] if c else "")
        return nm
    for r in rows:
        if r["name"] != "div" or not re.search(r"(^|\s)row(\s|$)", cls(r)): continue
        cols = [k for k in r["kids"] if k["name"] == "div" and re.search(r"(^|\s)col", cls(k))]
        if len(cols) != 1: continue
        col = cols[0]
        kids = [k for k in col["kids"] if k["name"] != "br"]
        k = kind(kids[0]) if kids else "empty"
        out.append((tokens(cls(col)), k))
    return out

mods = _corpus.gate_mods(CLAUDE)
G = collections.defaultdict(collections.Counter); C = collections.defaultdict(collections.Counter)
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); tt, subj = mm.get("template_type", ""), mm.get("subject", "")
    for t in prs:
        cp, hp = t[1], t[2]
        pt = "overview" if re.search(r"_0_0\.html$|[_.]0\.0\.html$|_00\.html$", os.path.basename(cp)) else "lesson"
        try: g = open(hp, encoding="utf-8", errors="replace").read(); c = open(cp, encoding="utf-8").read()
        except Exception: continue
        for colc, k in body_rows(g): G[(tt, subj, pt, k)][colc] += 1; G[("ALL", "", pt, k)][colc] += 1; G[("ALL", "", "all", k)][colc] += 1
        for colc, k in body_rows(c): C[(tt, subj, pt, k)][colc] += 1; C[("ALL", "", pt, k)][colc] += 1; C[("ALL", "", "all", k)][colc] += 1

def show(title, D, minn=20):
    print("\n== " + title)
    for key, cnt in sorted(D.items(), key=lambda x: -sum(x[1].values())):
        n = sum(cnt.values())
        if n < minn: continue
        top = cnt.most_common(3)
        print("  %-12s %-26s %-8s %-10s n=%-5d %s" % (key[0], key[1][:26], key[2], key[3][:10], n, "  ".join("%s %.2f" % (a, b / n) for a, b in top)))
show("GOLD — single-column body rows by (template, subject, page type, content kind): column class shares", G)
show("CLAUDE — same", C, 40)
