#!/usr/bin/env python3
"""r368 PICK probe (session 21, Round 5) — THE CAPTURED LIST. The miner's activity rows carry 1,013 gold `li` lines inside Claude
captures (156 pages / 108 modules). For every un-built capture on every paired page whose LEADING member element (after the
header; the r366-freed paragraph excluded) is a <ul> / <ol> — or whose first member <p> is followed by a list before any
table — record the capture type / owner, the list's first item, and the gold's treatment of that item: FREE (a gold skeleton
li carries it), IN-WIDGET (in the gold's HTML, in no skeleton line), ABSENT. Aggregated by type, owner kind, template,
subject. Writes _r368_leadlist.{json,log}."""
import os, re, sys, json, io, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, HERE); sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _diff_miner import page_lines
from _measure_ceiling import has_source, unorm, load_meta

TAG = re.compile(r"<(/?)([a-zA-Z0-9]+)([^>]*)>")
HDR = re.compile(r"INTERACTIVE \(un-built\) #(\d+): ([^—<]+?) — ([^—<]+?) — see", re.S)
def balanced(html, start):
    depth = 1
    for t in TAG.finditer(html, start):
        if t.group(2).lower() != "div": continue
        depth += -1 if t.group(1) else 1
        if depth == 0: return t.start()
    return len(html)
def captures(html):
    out = []
    for m in re.finditer(r'<div class="cv2-interactive cv2-int-ref"[^>]*>', html):
        end = balanced(html, m.end()); block = html[m.end():end]
        h = HDR.search(block)
        if not h: continue
        k = block.find('<div style="font-size: 0.95em">', h.end())
        if k < 0: continue
        inner = block[k + len('<div style="font-size: 0.95em">'):balanced(block, k + len('<div style="font-size: 0.95em">'))]
        seq = []
        for e in re.finditer(r"<(p|ul|ol|table|div|h[1-6]|img)\b([^>]*)>", inner):
            tag = e.group(1)
            if tag == "div": continue
            seq.append((tag, e.start()))
            if len(seq) >= 4: break
        # the leading LIST: first element a list, or p then list
        pos = None; n_before = 0
        if seq and seq[0][0] in ("ul", "ol"): pos = seq[0][1]
        elif len(seq) >= 2 and seq[0][0] == "p" and seq[1][0] in ("ul", "ol"): pos = seq[1][1]; n_before = 1
        if pos is None: continue
        lst_end = inner.find("</ul>", pos); lst_end2 = inner.find("</ol>", pos)
        lst_end = min(x for x in (lst_end, lst_end2) if x >= 0) if (lst_end >= 0 or lst_end2 >= 0) else pos + 3000
        items = [re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", x)).strip() for x in re.findall(r"<li[^>]*>(.*?)</li>", inner[pos:lst_end], re.S)]
        items = [x for x in items if x]
        if not items: continue
        tail_kind = seq[n_before + 1][0] if len(seq) > n_before + 1 else "end"
        out.append({"index": h.group(1), "type": h.group(2).strip(), "owner": h.group(3).strip(), "n_items": len(items), "first": items[0][:100], "p_before": n_before, "after_list": tail_kind})
    return out

meta = load_meta()
rows = []
codes = sorted(_corpus.gate_mods(CLAUDE))
for ci, code in enumerate(codes):
    m = meta.get(code) or {}
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
        craw = re.sub(r"<!--.*?-->", "", io.open(cp, encoding="utf-8", errors="replace").read(), flags=re.S)
        caps = captures(craw)
        if not caps: continue
        g, _ = page_lines(hp)
        gli = " " + unorm(" \n ".join(l.text for l in g if l.text and l.sig != "WIDGET" and (l.sig or "").startswith("li"))) + " "
        gskel = " " + unorm(" \n ".join(l.text for l in g if l.text and l.sig != "WIDGET")) + " "
        graw = " " + unorm(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", io.open(hp, encoding="utf-8", errors="replace").read(), flags=re.S))) + " "
        for c in caps:
            t = unorm(c["first"])
            if len(t.split()) < 2: continue
            if has_source(t, gli): verdict = "gold-free-li"
            elif has_source(t, gskel): verdict = "gold-free-other"
            elif has_source(t, graw): verdict = "gold-in-widget"
            else: verdict = "gold-absent"
            owner_kind = "standalone" if "inline" in c["owner"] else ("owned" if re.search(r"Activity\s+\S", c["owner"]) else "other")
            rows.append({"module": code, "page": os.path.basename(cp), "type": c["type"], "owner_kind": owner_kind, "n_items": c["n_items"], "p_before": c["p_before"], "after_list": c["after_list"], "first": c["first"][:80], "verdict": verdict, "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
    if ci % 60 == 0: print(f"  … {ci}/{len(codes)} modules, {len(rows)} captures with a leading list", flush=True)
json.dump(rows, io.open(os.path.join(HERE, "_r368_leadlist.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
base = lambda t: t.split(" (")[0].split(" + ")[0].strip()
def agg(rs, key):
    d = collections.defaultdict(lambda: [0, 0, set(), set()])
    for r in rs:
        k = key(r); d[k][0] += 1; d[k][1] += r["verdict"].startswith("gold-free"); d[k][2].add(r["module"] + "/" + r["page"]); d[k][3].add(r["module"])
    return sorted(((k, v[0], round(v[1] / v[0], 2), len(v[2]), len(v[3])) for k, v in d.items()), key=lambda x: -x[1])
P(f"captures with a leading list: {len(rows)} on {len(set(r['module'] + '/' + r['page'] for r in rows))} pages / {len(set(r['module'] for r in rows))} modules")
P("verdicts:", collections.Counter(r["verdict"] for r in rows).most_common())
P("\nBY (owner kind, base type): n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: (r["owner_kind"], base(r["type"])))[:22]]
P("\nBY after-list element:"); [P("  ", x) for x in agg(rows, lambda r: r["after_list"])]
P("\nBY p-before:"); [P("  ", x) for x in agg(rows, lambda r: r["p_before"])]
P("\nBY template:"); [P("  ", x) for x in agg(rows, lambda r: r["template"])]
P("\nBY subject:"); [P("  ", x) for x in agg(rows, lambda r: r["subject"])[:12]]
free = [r for r in rows if r["verdict"].startswith("gold-free")]
P(f"\nTHE CLASS (gold keeps the list FREE, Claude captures it): {len(free)} captures / {len(set(r['module'] + '/' + r['page'] for r in free))} pages / {len(set(r['module'] for r in free))} modules")
P("  top modules:", collections.Counter(r["module"] for r in free).most_common(12))
P("  examples:", [(r["module"], r["page"], base(r["type"]), r["owner_kind"], r["after_list"], r["first"][:40]) for r in free[:8]])
io.open(os.path.join(HERE, "_r368_leadlist.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
