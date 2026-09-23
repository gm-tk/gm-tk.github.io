#!/usr/bin/env python3
"""Session 40 r449 — cross the mcq decline verdicts (_s40_r449_mcqwhy.log) with the shape census
(_s40_r449_mcqshapes.json): for each verdict, the answer signals the bundle carries; for the yellow-highlight bundles,
whether the writer ANNOUNCES the highlight anywhere in the bundle (any text field, the r309 fence) and the
per-question structure (does each question have exactly one highlighted option line)."""
import io, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
why = {}
for ln in io.open(os.path.join(HERE, "_s40_r449_mcqwhy.log"), encoding="utf-8"):
    if ln.startswith("MCQWHY\t"):
        p = ln.rstrip("\n").split("\t"); why[p[1]] = re.sub(r"^L(\d+) #multiChoiceQuiz: .*?return null;\s*(//\s*)?", r"L\1 ", p[3])[:70]
shapes = {f"{r['code']}#{r['idx']}": r for r in json.load(io.open(os.path.join(HERE, "_s40_r449_mcqshapes.json"), encoding="utf-8"))}
dump = {}
for l in io.open(os.path.join(HERE, "_s40_r449_mcq.jsonl"), encoding="utf-8"):
    b = json.loads(l); dump[f"{b['code']}#{b['idx']}"] = b
ANN = re.compile(r"highlight|✅|tick(?:ed)?\b|in yellow", re.I)
tab = collections.defaultdict(collections.Counter)
for k, w in why.items():
    s = shapes.get(k)
    sig = "+".join(s["sig"]) if s else "(built)"
    tab[w][sig or "(none)"] += 1
for w, c in sorted(tab.items(), key=lambda kv: -sum(kv[1].values())):
    print(f"{sum(c.values()):4d}  {w}")
    for sig, n in c.most_common(8): print(f"        {n:4d}  {sig}")
print("\n== yellow-highlight bundles: announcement + structure ==")
rows = []
for k, s in shapes.items():
    if "hl-yellow" not in s["sig"]: continue
    b = dump[k]
    blob = json.dumps(b, ensure_ascii=False)
    ann = bool(ANN.search(" ".join([*(b["instr"] or []), *[o["text"] + " " + o["after"] for o in b["openers"]], *[m["text"] for m in b["members"] if m["type"] == "tag"]])))
    # option lines that carry a yellow mark covering (nearly) the whole line after its list marker
    marked_lines = 0; lines = 0
    for m in b["members"]:
        if m["type"] != "black": continue
        for mk in (m.get("marks") or []):
            if mk["kind"] == "hl" and mk.get("color") == "yellow": marked_lines += 1
        lines += 1
    rows.append((k, why.get(k, "?"), s["layout"], ann, marked_lines, lines, s["extra"]))
for r in sorted(rows, key=lambda r: (r[1], r[0])):
    print(f"  {r[0]:14s} {r[1][:40]:40s} {r[2]:12s} announced={str(r[3]):5s} yellow-marks-on-lines={r[4]:3d} black-lines={r[5]:3d} extra={r[6]}")
print(f"\nyellow bundles {len(rows)}; announced {sum(1 for r in rows if r[3])}; by verdict: {collections.Counter(r[1][:22] for r in rows)}")
