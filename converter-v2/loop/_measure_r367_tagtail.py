#!/usr/bin/env python3
"""r367 PICK probe (session 21, Round 4) — THE STANDALONE WIDGET / ACTIVITY TAG'S TITLE. The r217 standalone box opens for a
bare widget tag (`[Interactive] Mix and Match`, `[Activity] Calculating soil type.`, `[Activity individual - 3A] What was
Wakefield Thinking?`, `[interactive: true/false]` + `[H3] Knowledge Check`, `[Activity: Embedded]` + a red-only line) — the
title rides on the tag line (its TAIL) or on the NEXT line, and Claude's page never shows it; the gold opens the box with
`<h3>Title</h3>`. For every such WT tag in every gate module: the title's FORM (tail / next-red / next-h3 / next-plain), the
gold box that carries it as its first h3 (any box on the module's pages), and Claude's state (h3 / inside a capture / free /
absent). Numbered `[Activity N …]` openers (r362 / r364 / r365 territory) are EXCLUDED. Writes _r367_tagtail.{json,log}."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
TAGLINE = re.compile(r"^\s*\[\s*(interactive|activity)([^\]]*)\]\s*(.*)$", re.I)
NUMBERED = re.compile(r"^\s*\d+(?:\.\d+)?[a-z]?\b", re.I)
NEXTTAG = re.compile(r"^\s*\[\s*(h[1-6]|heading|activity heading(?:\s+h\d)?)\s*\]\s*(\S.*)$", re.I)
def norm(s): return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", s).lower()).strip()
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted((f for f in os.listdir(d) if f.endswith("_parsed.txt")), key=lambda f: -os.path.getsize(os.path.join(d, f)))
    return [l.rstrip("\n") for l in open(os.path.join(d, fs[0]), encoding="utf-8", errors="replace")] if fs else []
TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
def boxes(html):
    out = []
    for m in re.finditer(r'<div class="(activity[^"]*)"([^>]*)>', html):
        num = re.search(r'number="([^"]*)"', m.group(2))
        depth = 1; pos = m.end()
        for t in TAG.finditer(html, m.end()):
            if t.group(2).lower() != "div": continue
            depth += -1 if t.group(1) else 1
            if depth == 0: pos = t.start(); break
        out.append((num.group(1).upper() if num else None, html[m.end():pos]))
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
    for k, (i, raw) in enumerate(nb):
        isred = "\U0001f534" in raw
        l = RED.sub("", raw)
        m = TAGLINE.match(l)
        if not m: continue
        inner = m.group(2).strip(" :–—-")
        if NUMBERED.match(inner): continue                      # a numbered opener — not this class
        tail = m.group(3).replace("*", "").strip()
        tail = re.sub(r"\(.*?\)\s*$", "", tail).strip()
        form = None; title = None
        if tail and len(tail.split()) <= 12 and not re.search(r"https?://", tail):
            form, title = "tail", tail
        elif not tail and k + 1 < len(nb):
            nraw = nb[k + 1][1]; nl = RED.sub("", nraw).strip()
            h = NEXTTAG.match(nl)
            if h: form, title = "next-h3", h.group(2).replace("*", "").strip()
            elif "\U0001f534" in nraw and not nl.startswith("[") and 1 <= len(nl.split()) <= 10: form, title = "next-red", nl.replace("*", "").strip()
            elif nl and not nl.startswith("[") and not nl.startswith("┌") and 1 <= len(nl.split()) <= 6 and not nl.endswith(".") : form, title = "next-plain", nl.replace("*", "").strip()
        if not form or not title or len(title) < 3: continue
        rows.append(dict(code=code, line=i + 1, tag=m.group(1).lower(), inner=inner[:40], form=form, title=title[:80], red=isred,
                         template=(meta.get(code) or {}).get("template_type", "?"), subject=(meta.get(code) or {}).get("subject", "?")))
gb = {}; cb = {}; graw = {}; craw = {}
for r in rows:
    code = r["code"]
    if code not in gb:
        gb[code] = []; cb[code] = []; graw[code] = ""; craw[code] = ""
        for root, store, rawstore in ((HUMAN, gb, graw), (CLAUDE, cb, craw)):
            d = _corpus.mdir(root, code)
            for f in sorted(os.listdir(d)):
                if f.endswith(".html") and not re.search(r"acks|glossary|references", f, re.I):
                    h = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)
                    rawstore[code] += " " + norm(h)
                    for n, inner in boxes(h): store[code].append((f, n, inner))
    t = norm(r["title"])
    def state(bx, rawtext):
        for f, n, inner in bx:
            m = re.search(r"<h3[^>]*>(.*?)</h3>", inner, re.S)
            if m:
                h3 = norm(m.group(1))
                if h3 == t or (len(t) > 6 and (t in h3 or h3 in t)):
                    return ("h3-title-first" if first_block(inner) == "h3" else "h3-title-later") , f, n
        for f, n, inner in bx:
            if t and t in norm(inner):
                cap = "inside-capture" if re.search(r'cv2-interactive', inner) else "inside-box"
                return cap, f, n
        if t and t in rawtext: return "free-on-page", None, None
        return "absent", None, None
    r["gold"], r["gpage"], r["gnum"] = state(gb[code], graw[code]); r["claude"], r["cpage"], r["cnum"] = state(cb[code], craw[code])
json.dump(rows, open(os.path.join(HERE, "_r367_tagtail.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
P(f"unnumbered widget / activity tags with a title: {len(rows)} / modules {len(set(r['code'] for r in rows))}")
P("by form:", collections.Counter(r["form"] for r in rows).most_common(), "; by tag:", collections.Counter(r["tag"] for r in rows).most_common())
P("\nGOLD state:", collections.Counter(r["gold"] for r in rows).most_common())
P("CLAUDE state:", collections.Counter(r["claude"] for r in rows).most_common())
P("\nGOLD × CLAUDE:")
for k, v in collections.Counter((r["gold"], r["claude"]) for r in rows).most_common(12): P(f"  {v:4}  gold={k[0]:18} claude={k[1]}")
both = [r for r in rows if r["gold"] != "absent"]
for key in ("form", "tag", "template", "subject"):
    grp = collections.defaultdict(list)
    for r in both: grp[r[key]].append(r)
    P(f"\nby {key}: n / gold h3-first / claude h3-first / MISS (gold h3-first, Claude not h3) rows / pages / modules")
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        miss = [r for r in v if r["gold"] == "h3-title-first" and not r["claude"].startswith("h3")]
        P(f"  {str(k)[:34]:34}: n={len(v)} gold={sum(r['gold']=='h3-title-first' for r in v)/len(v):.2f} claude={sum(r['claude'].startswith('h3') for r in v)/len(v):.2f} miss={len(miss)} / {len(set((r['code'], r['gpage']) for r in miss))} / {len(set(r['code'] for r in miss))}")
miss = [r for r in both if r["gold"] == "h3-title-first" and not r["claude"].startswith("h3")]
P(f"\nTHE CLASS: {len(miss)} rows / {len(set(r['code'] for r in miss))} modules / {len(set((r['code'], r['gpage']) for r in miss))} gold pages; by form: {collections.Counter(r['form'] for r in miss).most_common()}; Claude state of the misses: {collections.Counter(r['claude'] for r in miss).most_common()}")
P("examples:", [(r["code"], r["form"], r["tag"], r["inner"][:20], r["title"][:35], r["claude"]) for r in miss[:8]])
open(os.path.join(HERE, "_r367_tagtail.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
