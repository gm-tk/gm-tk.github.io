#!/usr/bin/env python3
"""r365 PICK probe (session 21) — THE WIDGET-TYPED ACTIVITY TAG: `[Activity 1B – self-marking type the answer] Fill in the blanks`
(the r363 residue (a)). The tag parses as the WIDGET (typing quiz, number 1B) with the title as its tail; the r217 standalone box
opens at the widget and the title lands inside the capture as a <p>. For every such opener with a title tail in every gate
module's WT: does the GOLD box `number=N` open with `<h3>Title</h3>`? Where is the title on CLAUDE's page? Per template /
subject / module. Reuses the r363 probe's box + state logic. Writes _r365_typedtag.{json,log}."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
TYPED = re.compile(r"\[\s*activity\s+([\d.]+[a-z]?)\s*[–—-]\s*([^\]]{3,60})\]\s*(\S.*)?$", re.I)
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
    for l in wt_lines(code):
        m = TYPED.search(l)
        if not m: continue
        title = (m.group(3) or "").replace("*", "").strip()
        title = re.sub(r"\(.*?\)\s*$", "", title).strip()          # a trailing writer note in brackets
        if not title: continue
        rows.append(dict(code=code, num=m.group(1).upper(), kind=re.sub(r"\s+", " ", m.group(2).lower()).strip(" ,"), title=title,
                         template=(meta.get(code) or {}).get("template_type", "?"), subject=(meta.get(code) or {}).get("subject", "?")))
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
    r["gold"] = state(g); r["claude"] = state(c); r["gpage"] = g[0] if g else None; r["cpage"] = c[0] if c else None
json.dump(rows, open(os.path.join(HERE, "_r365_typedtag.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
P(f"typed activity tags with a title tail: {len(rows)} / modules {len(set(r['code'] for r in rows))} / claude pages {len(set((r['code'], r['cpage']) for r in rows if r['cpage']))}")
P("kinds:", collections.Counter(r["kind"] for r in rows).most_common(12))
P("\nGOLD state:", collections.Counter(r["gold"] for r in rows).most_common())
P("CLAUDE state:", collections.Counter(r["claude"] for r in rows).most_common())
P("\nGOLD × CLAUDE:")
for k, v in collections.Counter((r["gold"], r["claude"]) for r in rows).most_common(): P(f"  {v:4}  gold={k[0]:28} claude={k[1]}")
both = [r for r in rows if r["gold"] != "no-box" and r["claude"] != "no-box"]
P(f"\npaired boxes {len(both)}: gold h3-title-first share = {sum(r['gold']=='h3-title-first' for r in both)/max(1,len(both)):.2f}")
for key in ("template", "subject", "code"):
    grp = collections.defaultdict(list)
    for r in both: grp[r[key]].append(r)
    P(f"\nby {key}: n / gold h3-first / claude h3-first / MISS (gold h3-first, Claude title inside the capture) boxes / pages")
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        miss = [r for r in v if r["gold"] == "h3-title-first" and r["claude"].startswith("title-inside")]
        P(f"  {k}: n={len(v)} gold={sum(r['gold']=='h3-title-first' for r in v)/len(v):.2f} claude={sum(r['claude']=='h3-title-first' for r in v)/len(v):.2f} miss={len(miss)} / {len(set(r['cpage'] for r in miss))}")
miss = [r for r in both if r["gold"] == "h3-title-first" and r["claude"].startswith("title-inside")]
P(f"\nTHE CLASS: {len(miss)} boxes / {len(set(r['code'] for r in miss))} modules / {len(set((r['code'], r['cpage']) for r in miss))} pages; by module: " + ", ".join(f"{k}:{v}" for k, v in sorted(collections.Counter(r['code'] for r in miss).items())))
P("examples:", [(r["code"], r["num"], r["kind"], r["title"][:40], r["claude"]) for r in miss[:6]])
open(os.path.join(HERE, "_r365_typedtag.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
