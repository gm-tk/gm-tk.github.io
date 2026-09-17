#!/usr/bin/env python3
"""r364 PICK probe — THE ID-CARRYING HEADING OPENS THE ACTIVITY: a WT heading tag whose text starts with an activity id
(`[H3] 1A Spot the place value`) followed within a few lines by an interactive tag / table. Does the gold open the box
`number=1A` with `<h3>Spot the place value</h3>` (the id stripped)? What does Claude ship — the heading before the box,
the box number, the box's first child? Per template / subject / heading level. Writes _r364_idheading.{json,log}."""
import os, re, sys, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)   # tests FIRST
import _corpus
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
HEAD = re.compile(r"^\s*\[\s*(h[1-6])\s*\]\s*\**\s*(?:activity\s+)?(\d{1,2}[A-Za-z])\b[\s.:–-]*(.+?)\**\s*$", re.I)
ACT = re.compile(r"^\s*\[\s*activity\b", re.I)
INTER = re.compile(r"\[[^\]]*(interactive|drag|drop|quiz|click|match|carousel|flip|accordion|modal|slider|sort|checkbox|fill|type the|self-marking|multichoice|multi-choice|tab)[^\]]*\]", re.I)
TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")


def norm(s): return re.sub(r"[^a-z0-9]+", " ", re.sub(r"<[^>]+>", " ", s).lower()).strip()


def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted((f for f in os.listdir(d) if f.endswith("_parsed.txt")), key=lambda f: -os.path.getsize(os.path.join(d, f)))
    return [RED.sub("", l).rstrip("\n") for l in open(os.path.join(d, fs[0]), encoding="utf-8", errors="replace")] if fs else []


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
        out.setdefault(num.group(1).upper(), (m.start(), html[m.end():pos]))
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
        m = HEAD.match(l)
        if not m: continue
        # an [Activity N] tag within the previous 2 non-blank lines means the heading is the activity's own lead, not the opener
        prev = [nb[j][1] for j in range(max(0, k - 2), k)]
        if any(ACT.match(p) for p in prev): continue
        nxt = [nb[j][1] for j in range(k + 1, min(len(nb), k + 14))]
        widget_ahead = any(INTER.search(x) or x.startswith("┌─── TABLE") for x in nxt)
        act_ahead = any(ACT.match(x) for x in nxt[:6])
        rows.append(dict(code=code, level=m.group(1).lower(), num=m.group(2).upper(), title=m.group(3).strip(), widget_ahead=widget_ahead,
                         act_tag_ahead=act_ahead, template=(meta.get(code) or {}).get("template_type", "?"), subject=(meta.get(code) or {}).get("subject", "?")))
gb = {}; cb = {}; ch = {}
for r in rows:
    code = r["code"]
    if code not in gb:
        gb[code] = {}; cb[code] = {}; ch[code] = {}
        for root, store in ((HUMAN, gb), (CLAUDE, cb)):
            d = _corpus.mdir(root, code)
            for f in sorted(os.listdir(d)):
                if f.endswith(".html") and not re.search(r"acks|glossary|references", f, re.I):
                    h = re.sub(r"<!--.*?-->", "", open(os.path.join(d, f), encoding="utf-8", errors="replace").read(), flags=re.S)
                    if root is CLAUDE: ch[code][f] = h
                    for n, (pos, inner) in boxes(h).items(): store[code].setdefault(n, (f, pos, inner))
    t = norm(r["title"]); g = gb[code].get(r["num"]); c = cb[code].get(r["num"])

    def gstate(box):
        if not box: return "no-box"
        f, pos, inner = box
        mm = re.search(r"<h3[^>]*>(.*?)</h3>", inner, re.S); h3 = norm(mm.group(1)) if mm else ""
        fb = first_block(inner)
        if mm and (h3 == t or (len(t) > 6 and (t in h3 or h3 in t))): return "h3-title-first" if fb == "h3" else "h3-title-later(" + fb + ")"
        return ("title-inside(" if t in norm(inner) else "title-absent(") + fb + ")"

    r["gold"] = gstate(g)
    if not c:
        r["claude"] = "no-box"
    else:
        f, pos, inner = c; fb = first_block(inner); h = ch[code][f]
        before = h[max(0, pos - 3000):pos]
        bl = re.findall(r"<(h[1-6]|p)\b[^>]*>(.*?)</\1>", before, re.S)
        hit = next((tag for tag, txt in reversed(bl[-4:]) if (norm(txt) == t or (len(t) > 6 and t in norm(txt)))), None)
        if hit: r["claude"] = "before-box:" + hit + "(" + fb + ")"
        elif t in norm(inner): r["claude"] = "inside:" + fb
        else: r["claude"] = "absent(" + fb + ")"
json.dump(rows, open(os.path.join(HERE, "_r364_idheading.json"), "w", encoding="utf-8"), indent=1, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
P(f"id-carrying headings: {len(rows)} / modules {len(set(r['code'] for r in rows))}; by level {collections.Counter(r['level'] for r in rows).most_common()}; widget ahead {sum(r['widget_ahead'] for r in rows)}; [Activity] tag ahead {sum(r['act_tag_ahead'] for r in rows)}")
P("GOLD:", collections.Counter(r["gold"] for r in rows).most_common(8))
P("CLAUDE:", collections.Counter(r["claude"] for r in rows).most_common(12))
P("\nGOLD × CLAUDE (top 20):")
for k, v in collections.Counter((r["gold"], r["claude"]) for r in rows).most_common(20): P(f"  {v:4}  gold={k[0]:28} claude={k[1]}")
both = [r for r in rows if r["gold"] != "no-box" and r["claude"] != "no-box"]
P(f"\npaired {len(both)}: gold h3-title-first {sum(r['gold']=='h3-title-first' for r in both)/max(1,len(both)):.2f}")
for key in ("template", "subject", "level"):
    grp = collections.defaultdict(list)
    for r in both: grp[r[key]].append(r)
    P(f"by {key}: n / gold h3-first / claude before-box / claude h3-first-inside")
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        P(f"  {k}: n={len(v)} gold={sum(r['gold']=='h3-title-first' for r in v)/len(v):.2f} before={sum(r['claude'].startswith('before-box') for r in v)/len(v):.2f} inside-h3={sum(r['claude']=='inside:h3' for r in v)/len(v):.2f}")
miss = [r for r in both if r["gold"] == "h3-title-first" and r["claude"].startswith("before-box")]
P(f"\nTHE CLASS (gold h3-first inside the box, Claude's heading BEFORE the box): {len(miss)} boxes / {len(set(r['code'] for r in miss))} modules; by module: " + ", ".join(f"{k}:{v}" for k, v in sorted(collections.Counter(r['code'] for r in miss).items())))
P("examples:", [(r["code"], r["num"], r["level"], r["title"][:30], r["claude"]) for r in miss[:8]])
open(os.path.join(HERE, "_r364_idheading.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
