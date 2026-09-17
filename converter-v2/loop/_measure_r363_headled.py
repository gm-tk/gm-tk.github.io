#!/usr/bin/env python3
"""r363 PICK probe — the heading-tag-led activity lead: `[Activity N]` followed by `[Activity Heading] T` /
`[Activity heading H3] T` / `[Heading] T` / `[H3] T`. For every such opener in every gate module's WT: does the
GOLD box `number=N` open with `<h3>T</h3>`? Does CLAUDE's box open with the h3, or swallow T into a capture?
Per template / subject. Writes _r363_headled.{json,log}."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)   # tests FIRST: outputs/_corpus.py is a stale copy
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
ACT = re.compile(r"^\s*\[\s*activity\s+(\d+[a-z]?)\s*\]\s*(.*)$", re.I)
HEADTAG = re.compile(r"^\s*\[\s*(activity\s+heading(?:\s+h\d)?|heading|h[1-6])\s*\]\s*(\S.*)$", re.I)
def norm(s): return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", s).lower()).strip()
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted((f for f in os.listdir(d) if f.endswith("_parsed.txt")), key=lambda f: -os.path.getsize(os.path.join(d, f)))
    return [RED.sub("", l).rstrip("\n") for l in open(os.path.join(d, fs[0]), encoding="utf-8", errors="replace")] if fs else []
TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
def boxes(html):
    out = {}
    for m in re.finditer(r'<div class="(activity[^"]*)"([^>]*)>', html):
        num = re.search(r'number="([^"]*)"', m.group(2))
        if not num: continue
        depth = 1; pos = m.end()
        for t in TAG.finditer(html, m.end()):
            if t.group(2).lower() != "div": continue
            depth += -1 if t.group(1) else 1
            if depth == 0: pos = t.start(); break
        out.setdefault(num.group(1).upper(), html[m.end():pos])
    return out
def first_block(inner):
    for m in re.finditer(r"<(h[1-6]|p|ul|ol|table|img|div class=\"[a-zA-Z0-9-]+)", inner):
        t = m.group(1)
        if t.startswith("div class=\"row") or t.startswith("div class=\"col"): continue
        return t.replace("div class=\"", "div.")
    return "none"
meta = load_meta()
rows = []
for code in _corpus.gate_mods(CLAUDE):
    lines = wt_lines(code)
    nb = [(i, l) for i, l in enumerate(lines) if l.strip()]
    for k, (i, l) in enumerate(nb):
        a = ACT.match(l)
        if not a or a.group(2).strip(): continue          # a BARE numbered opener
        if k + 1 >= len(nb): continue
        h = HEADTAG.match(nb[k + 1][1])
        if not h: continue
        num = a.group(1).upper(); tag = re.sub(r"\s+", " ", h.group(1).lower()); title = h.group(2).replace("*", "").strip()
        rows.append(dict(code=code, num=num, tag=tag, title=title, template=(meta.get(code) or {}).get("template_type", "?"),
                         subject=(meta.get(code) or {}).get("subject", "?")))
# gold / Claude boxes per module
gb = {}; cb = {}
for r in rows:
    code = r["code"]
    if code not in gb:
        gb[code] = {}; cb[code] = {}
        for root, store in ((HUMAN, gb), (CLAUDE, cb)):
            d = _corpus.mdir(root, code)
            for f in sorted(os.listdir(d)):
                if f.endswith(".html") and not re.search(r"acks|glossary|references", f, re.I):
                    h = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
                    for n, inner in boxes(h).items(): store[code].setdefault(n, (f, inner))
    g = gb[code].get(r["num"]); c = cb[code].get(r["num"])
    t = norm(r["title"])
    def state(box):
        if not box: return "no-box"
        f, inner = box
        m = re.search(r"<h3[^>]*>(.*?)</h3>", inner, re.S)
        first = first_block(inner)
        h3 = norm(m.group(1)) if m else ""
        if m and (h3 == t or (len(t) > 6 and (t in h3 or h3 in t))):
            return "h3-title-first" if first == "h3" else "h3-title-later(" + first + ")"
        if t and t in norm(inner): return "title-inside-" + first
        return "title-absent(" + first + ")"
    r["gold"] = state(g); r["claude"] = state(c); r["gpage"] = g[0] if g else None
json.dump(rows, open(os.path.join(HERE, "_r363_headled.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
P(f"heading-led openers: {len(rows)} / modules {len(set(r['code'] for r in rows))}")
P("by tag:", collections.Counter(r["tag"] for r in rows).most_common())
P("\nGOLD state:", collections.Counter(r["gold"] for r in rows).most_common())
P("CLAUDE state:", collections.Counter(r["claude"] for r in rows).most_common())
P("\nGOLD × CLAUDE:")
for k, v in collections.Counter((r["gold"], r["claude"]) for r in rows).most_common(): P(f"  {v:4}  gold={k[0]:28} claude={k[1]}")
both = [r for r in rows if r["gold"] != "no-box" and r["claude"] != "no-box"]
P(f"\npaired boxes {len(both)}: gold h3-title-first share = {sum(r['gold']=='h3-title-first' for r in both)/max(1,len(both)):.2f}")
for key in ("template", "subject", "tag"):
    grp = collections.defaultdict(list)
    for r in both: grp[r[key]].append(r)
    P(f"\nby {key}: n / gold h3-first / claude h3-first / MISS (gold h3-first, Claude title-inside capture) pages/modules")
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        miss = [r for r in v if r["gold"] == "h3-title-first" and r["claude"].startswith("title-inside")]
        P(f"  {k}: n={len(v)} gold={sum(r['gold']=='h3-title-first' for r in v)/len(v):.2f} claude={sum(r['claude']=='h3-title-first' for r in v)/len(v):.2f} miss={len(miss)} boxes / {len(set(r['code']+r['gpage'] for r in miss))} pages / {len(set(r['code'] for r in miss))} modules")
miss = [r for r in both if r["gold"] == "h3-title-first" and r["claude"].startswith("title-inside")]
P(f"\nTHE CLASS: {len(miss)} boxes / {len(set(r['code'] for r in miss))} modules; by module: " + ", ".join(f"{k}:{v}" for k, v in sorted(collections.Counter(r['code'] for r in miss).items())))
open(os.path.join(HERE, "_r363_headled.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
