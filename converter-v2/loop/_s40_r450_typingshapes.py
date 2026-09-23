#!/usr/bin/env python3
"""Session 40 r450 — the TYPING shape census (D13-4, the second quiz type; one authoring shape family at a time,
>= 20 sites; build only where the answer is marked, highlight / green under r309's announcement fence). Reads
_s40_typing.jsonl. For each UN-BUILT bundle: layout, the answer signals, the announcement, and the dominant
QUESTION-LINE form:
  red-inline   a question line = [red answer words] + black tail (or black + red + black) — BLL244's form
  red-end      black question + a red answer at the line's END (PHE1007's '[Dev correct answer is in red …]')
  yellow-in    a black line with a yellow-highlighted word / phrase inside it
  blank        a line with ____ blanks and no mark
Prints bundles / modules per (form, announced) and examples."""
import io, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ANN_HL = re.compile(r"correct\s+answers?[^\n]{0,40}?highlight|highlighted\s+answers?[^\n]{0,30}?correct|answers?\s+(?:are\s+|is\s+)?highlighted", re.I)
ANN_RED = re.compile(r"(?:correct\s+)?answers?[^\n\]]{0,40}?\bin\s+red\b|\bred\b[^\n\]]{0,30}?\banswers?\b", re.I)
RED_SKIP = re.compile(r"^[^\w]*$")
RED_PLAIN = re.compile(r"^(?:answers?|correct answers?|for media|associated media|teacher[- ]marked|\(?image\)?|media)\s*[:.]?$|:$", re.I)
rows = []
for l in io.open(os.path.join(HERE, "_s40_typing.jsonl"), encoding="utf-8"):
    b = json.loads(l)
    if b["built"]: continue
    mem = b["members"]
    blob = json.dumps(b, ensure_ascii=False)
    ann_hl, ann_red = bool(ANN_HL.search(blob)), bool(ANN_RED.search(blob))
    has_table = any(m["type"] == "table" for m in mem)
    forms = collections.Counter()
    prev = None
    for m in mem:
        if m["type"] == "black":
            y = [mk for mk in (m.get("marks") or []) if mk["kind"] == "hl" and mk.get("color") == "yellow"]
            if y: forms["yellow-in"] += 1
            elif "____" in m["text"] or "___" in m["text"]: forms["blank"] += 1
        if m["type"] == "tag" and m["cls"] == "noise":
            w = re.sub(r"\s+", " ", m["text"]).strip()
            if w and not RED_SKIP.match(w) and not RED_PLAIN.search(w):
                if m["after"].strip(): forms["red-inline"] += 1
                elif prev is not None and prev["type"] == "black": forms["red-end"] += 1
                else: forms["red-alone"] += 1
        prev = m
    dom = forms.most_common(1)[0][0] if forms else "(none)"
    rows.append(dict(key=f"{b['code']}#{b['idx']}", code=b["code"], act=b["act"], table=has_table, extra=b["extra"],
                     forms=dict(forms), dom=dom, ann_hl=ann_hl, ann_red=ann_red))
print(f"un-built typing bundles {len(rows)} / modules {len({r['code'] for r in rows})}")
c = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for r in rows:
    k = (r["dom"], "table" if r["table"] else "lines", "merged" if r["extra"] else "single",
         "ann-hl" if r["ann_hl"] else ("ann-red" if r["ann_red"] else "-"))
    c[k] += 1; mods[k].add(r["code"]); ex[k].append(r["key"])
for k, n in c.most_common(40):
    print(f"  {n:4d} / {len(mods[k]):3d} mod  {k}  e.g. {', '.join(ex[k][:5])}")
json.dump(rows, io.open(os.path.join(HERE, "_s40_r450_typingshapes.json"), "w", encoding="utf-8", newline=""), indent=0)
