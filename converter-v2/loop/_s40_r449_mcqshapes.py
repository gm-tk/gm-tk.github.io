#!/usr/bin/env python3
"""Session 40 r449 — the multiChoiceQuiz SHAPE census (D13-4: build only where the writer marked the answer; one
authoring shape family at a time, >= 20 sites). Reads _s40_r449_mcq.jsonl (every mcq bundle, whole). For each UN-BUILT
bundle: the layout (lines / table / both), the answer signals present (yellow highlight, other highlight, green,
red answer word, [correct]-style bracket, bold option, a written answer key), the writer's announcement (opener /
instructions naming highlight / green / red / bold / tick), and a crude option structure (list-marked lines, '?'
questions). Prints the shape table (bundles / modules) and examples."""
import io, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
B = [json.loads(l) for l in io.open(os.path.join(HERE, "_s40_r449_mcq.jsonl"), encoding="utf-8")]
LIST = re.compile(r"^\s*(?:[a-hA-H][.)]|\d+[.)]|[•●▪◦\-*]|\(?[a-hA-H]\))\s+")
CORR = re.compile(r"\[\s*(?:correct|answer|right|tick|true)\b[^\]]*\]|\((?:correct|answer)\)", re.I)
KEY = re.compile(r"\b(?:correct answers?|answers?)\s*[:\-]\s*\S", re.I)
ANN = {
    "highlight": re.compile(r"highlight", re.I), "green": re.compile(r"\bgreen\b", re.I), "red": re.compile(r"\bred\b", re.I),
    "bold": re.compile(r"\bbold\b", re.I), "tick": re.compile(r"\btick", re.I)}
RED_SKIP = re.compile(r"^[^\w]*$")
RED_PLAIN = re.compile(r"^(?:answers?|correct answers?|for media|associated media|teacher[- ]marked|\(?image\)?|media)\s*[:.]?$|:$", re.I)
rows = []
for b in B:
    if b["built"]: continue
    mem = b["members"]; opn = b["openers"]
    layout = ("table" if any(m["type"] == "table" for m in mem) else "") + ("+lines" if any(m["type"] == "black" for m in mem) else "")
    layout = layout.strip("+") or "tags-only"
    sig = set()
    for m in mem:
        for mk in (m.get("marks") or []):
            sig.add("hl-yellow" if mk["kind"] == "hl" and mk.get("color") == "yellow" else ("hl-other" if mk["kind"] == "hl" else "green"))
        for r in (m.get("cellMarks") or []):
            for c in r:
                for mk in c:
                    sig.add("hl-yellow" if mk["kind"] == "hl" and mk.get("color") == "yellow" else ("hl-other" if mk["kind"] == "hl" else "green"))
        txt = m["text"] + " " + m["after"] + " " + " ".join(" ".join(r) for r in (m.get("rows") or []))
        if CORR.search(txt): sig.add("bracket")
        if KEY.search(txt): sig.add("key")
        if m["type"] == "black" and LIST.match(m["text"]) and "**" in m["text"]: sig.add("bold-option")
        if m["cls"] == "noise":
            w = re.sub(r"\s+", " ", m["text"]).strip()
            if w and not RED_SKIP.match(w) and not RED_PLAIN.search(w): sig.add("red")
    ann = set()
    blob = " ".join([*(b["instr"] or []), *[o["text"] for o in opn], *[m["text"] for m in mem if m["cls"] in ("tag", "instruction") and m["tag"] in (None, "mcq", "multiChoiceQuiz") or m["cls"] == "instruction"]])
    for k, rx in ANN.items():
        if rx.search(blob): ann.add(k)
    nlist = sum(1 for m in mem if m["type"] == "black" and LIST.match(m["text"]))
    nq = sum(1 for m in mem if m["type"] == "black" and m["text"].rstrip().endswith("?"))
    rows.append(dict(code=b["code"], idx=b["idx"], act=b["act"], layout=layout, sig=sorted(sig), ann=sorted(ann), extra=b["extra"], nlist=nlist, nq=nq))
print(f"un-built mcq bundles: {len(rows)} / modules {len({r['code'] for r in rows})}")
c = collections.Counter(); mods = collections.defaultdict(set)
for r in rows:
    k = (r["layout"], "+".join(r["sig"]) or "(no signal)")
    c[k] += 1; mods[k].add(r["code"])
print("\nlayout | answer signals -> bundles / modules")
for k, n in c.most_common(40):
    print(f"  {k[0]:12s} {k[1]:40s} {n:4d} / {len(mods[k])}")
# by single signal (any layout)
print("\nby signal (a bundle counts once per signal it carries):")
cs = collections.Counter(); ms = collections.defaultdict(set)
for r in rows:
    for s in r["sig"] or ["(none)"]: cs[s] += 1; ms[s].add(r["code"])
for s, n in cs.most_common(): print(f"  {s:14s} {n:4d} bundles / {len(ms[s])} modules")
# yellow highlight: announced?
yl = [r for r in rows if "hl-yellow" in r["sig"]]
print(f"\nyellow-highlight bundles {len(yl)}: announced 'highlight' {sum(1 for r in yl if 'highlight' in r['ann'])}, merged {sum(1 for r in yl if r['extra'])}, layout {collections.Counter(r['layout'] for r in yl)}")
io.open(os.path.join(HERE, "_s40_r449_mcqshapes.json"), "w", encoding="utf-8", newline="").write(json.dumps(rows, indent=0))
for r in yl[:40]:
    print(f"  {r['code']} #{r['idx']} {r['act']} {r['layout']} sig={r['sig']} ann={r['ann']} list={r['nlist']} q?={r['nq']} extra={r['extra']}")
