#!/usr/bin/env python3
"""r366 PICK probe (session 21, Round 3) — THE CAPTURED LEAD PROSE: the black paragraph(s) a writer types between a widget
tag and the widget's first table / list ("Drag and drop the products into the correct category.") ride INTO Claude's un-built
capture as members; the gold keeps them FREE inside the activity box (h3 + p + the widget). For every Claude capture on
every paired page: its header TYPE and OWNER ("Activity (inline)" = the r217 standalone box; "Activity 1B" = an owned /
embedded box), its LEADING member paragraphs (consecutive <p> before the first non-p member), and the gold's treatment of
that text: FREE (a gold skeleton line carries it), IN-WIDGET (in the gold's HTML, in no skeleton line), ABSENT.
Aggregated by type, owner kind, template, subject; module / page counts. Writes _r366_leadprose.{json,log}."""
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
    depth = 1; pos = start
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
        # the members container: the first <div style="font-size: 0.95em"> after the header
        k = block.find('<div style="font-size: 0.95em">', h.end())
        if k < 0: continue
        inner = block[k + len('<div style="font-size: 0.95em">'):balanced(block, k + len('<div style="font-size: 0.95em">'))]
        lead = []
        for e in re.finditer(r"<(p|ul|ol|table|div|h[1-6]|img|span)\b([^>]*)>(.*?)(?=<(?:p|ul|ol|table|div|h[1-6]|img)\b|$)", inner, re.S):
            tag = e.group(1)
            if tag == "span": continue
            if tag == "p" and "color: #d9480f" not in e.group(2) and "color:#d9480f" not in e.group(2):
                txt = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", e.group(3))).strip()
                if txt: lead.append(txt)
                continue
            break
        out.append({"index": h.group(1), "type": h.group(2).strip(), "owner": h.group(3).strip(), "lead": lead})
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
        if not any(c["lead"] for c in caps): continue
        g, _ = page_lines(hp)
        gskel = " " + unorm(" \n ".join(l.text for l in g if l.text and l.sig != "WIDGET")) + " "
        graw = " " + unorm(re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", io.open(hp, encoding="utf-8", errors="replace").read(), flags=re.S))) + " "
        for c in caps:
            if not c["lead"]: continue
            t = unorm(c["lead"][0])
            if len(t.split()) < 2: continue
            if has_source(t, gskel): verdict = "gold-free"
            elif has_source(t, graw): verdict = "gold-in-widget"
            else: verdict = "gold-absent"
            owner_kind = "standalone" if "inline" in c["owner"] else ("owned" if re.search(r"Activity\s+\S", c["owner"]) else "other")
            rows.append({"module": code, "page": os.path.basename(cp), "type": c["type"], "owner": c["owner"], "owner_kind": owner_kind,
                         "n_lead": len(c["lead"]), "lead": c["lead"][0][:90], "verdict": verdict,
                         "template": m.get("template_type", "?"), "subject": m.get("subject", "?")})
    if ci % 60 == 0: print(f"  … {ci}/{len(codes)} modules, {len(rows)} captures with a lead", flush=True)
json.dump(rows, io.open(os.path.join(HERE, "_r366_leadprose.json"), "w", encoding="utf-8"), indent=0, ensure_ascii=False)
L = []
def P(*a): s = " ".join(str(x) for x in a); L.append(s); print(s)
def agg(rs, key):
    d = collections.defaultdict(lambda: [0, 0, set(), set()])
    for r in rs:
        k = key(r); d[k][0] += 1; d[k][1] += (r["verdict"] == "gold-free"); d[k][2].add(r["module"] + "/" + r["page"]); d[k][3].add(r["module"])
    return sorted(((k, v[0], round(v[1] / v[0], 2), len(v[2]), len(v[3])) for k, v in d.items()), key=lambda x: -x[1])
P(f"captures with a leading black paragraph: {len(rows)} on {len(set(r['module'] + '/' + r['page'] for r in rows))} pages / {len(set(r['module'] for r in rows))} modules")
P("verdicts:", collections.Counter(r["verdict"] for r in rows).most_common())
P("\nBY owner kind: n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: r["owner_kind"])]
P("\nBY capture type: n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: r["type"])[:16]]
P("\nBY template: n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: r["template"])]
P("\nBY subject: n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: r["subject"])[:14]]
P("\nBY (owner kind, type): n / gold-free share / pages / modules"); [P("  ", x) for x in agg(rows, lambda r: (r["owner_kind"], r["type"]))[:16]]
free = [r for r in rows if r["verdict"] == "gold-free"]
P(f"\nTHE CLASS (gold keeps the lead FREE, Claude captures it): {len(free)} captures / {len(set(r['module'] + '/' + r['page'] for r in free))} pages / {len(set(r['module'] for r in free))} modules")
P("  by owner kind:", collections.Counter(r["owner_kind"] for r in free).most_common())
P("  top modules:", collections.Counter(r["module"] for r in free).most_common(15))
P("  n_lead distribution:", collections.Counter(min(r["n_lead"], 4) for r in free).most_common())
P("  examples:", [(r["module"], r["page"], r["type"], r["owner"], r["lead"][:45]) for r in free[:8]])
io.open(os.path.join(HERE, "_r366_leadprose.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
