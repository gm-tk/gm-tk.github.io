#!/usr/bin/env python3
"""Session 40 Round 6 — D13-4's remaining quiz types (dropDown's dropdown-opener bundles, reorder, radioQuiz,
selectionBox): per type, the un-built bundles by ANSWER SIGNAL x layout, to find any authoring shape with an explicit
or ANNOUNCED answer mark (D13-4: highlight / green only under the r309 announcement fence) that reaches the 20-site
floor. Signals: bracket ([correct] / [answer]), red (a 'noise' red answer member), yellow / green highlight (marks),
ANNOUNCED (the r309 fence phrasing), a written key ('Answer:' / 'Correct answer:'), numbered order (reorder: the
writer's own 1..N sequence). Layout: table / merged / lines."""
import io, os, re, json, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ANN = re.compile(r"correct\s+answers?[^\n]{0,40}?(?:highlight|green)|answers?\s+(?:are\s+|is\s+)?(?:highlighted|in green)", re.I)
CORR = re.compile(r"\[\s*(?:correct|answer|right|tick|true)\b", re.I)
KEY = re.compile(r"\b(?:correct\s+)?answers?\s*[:=]\s*\S", re.I)
RED_SKIP = re.compile(r"^[^\w]*$")
RED_PLAIN = re.compile(r"^(?:answers?|correct answers?|for media|associated media|teacher[- ]marked|\(?image\)?|media)\s*[:.]?$|:$", re.I)
def signals(b):
    s = set()
    blob = json.dumps(b, ensure_ascii=False)
    if CORR.search(blob): s.add("bracket")
    if KEY.search(" ".join(m["text"] + " " + m["after"] for m in b["members"])): s.add("key")
    for m in b["members"]:
        if m["cls"] == "noise":
            w = re.sub(r"\s+", " ", m["text"]).strip()
            if w and not RED_SKIP.match(w) and not RED_PLAIN.search(w): s.add("red")
        for mk in (m.get("marks") or []):
            s.add("yellow" if mk["kind"] == "hl" and mk.get("color") == "yellow" else ("green" if mk["kind"] == "green" else "hl-other"))
        for r in (m.get("cellMarks") or []):
            for c in r:
                for mk in c:
                    s.add("yellow" if mk["kind"] == "hl" and mk.get("color") == "yellow" else ("green" if mk["kind"] == "green" else "hl-other"))
    if ANN.search(blob): s.add("ANNOUNCED")
    return s
out = []
for T, fn in (("dropDown(dropdown opener)", "_s40_dropDown.jsonl"), ("reorder", "_s40_reorder.jsonl"), ("radioQuiz", "_s40_radioQuiz.jsonl"), ("selectionBox", "_s40_selectionBox.jsonl")):
    c = collections.Counter(); mods = collections.defaultdict(set); tot = 0; tmods = set(); built = 0
    for l in io.open(os.path.join(HERE, fn), encoding="utf-8"):
        b = json.loads(l)
        if b["built"]: built += 1; continue
        if T.startswith("dropDown"):
            op = " ".join([x["text"] for x in b["members"][:2] if x["type"] == "tag"] + [x["text"] for x in b["openers"]]).lower()
            if not re.search(r"drop[\s-]*down|drop\s*quiz|select", op): continue
        tot += 1; tmods.add(b["code"])
        sig = signals(b)
        explicit = sorted(x for x in sig if x in ("bracket", "red", "key") or (x in ("yellow", "green", "hl-other") and "ANNOUNCED" in sig))
        lay = "merged" if b["extra"] else ("table" if any(m["type"] == "table" for m in b["members"]) else "lines")
        k = (lay, "+".join(explicit) or ("(unannounced highlight only)" if sig & {"yellow", "green", "hl-other"} else "(no answer)"))
        c[k] += 1; mods[k].add(b["code"])
    out.append(f"== {T}: built {built}, un-built {tot} / {len(tmods)} modules")
    for k, n in c.most_common(12): out.append(f"   {n:4d} / {len(mods[k]):3d} mod  {k}")
    big = max(((n, k) for k, n in c.items() if not k[1].startswith("(")), default=(0, None))
    out.append(f"   largest explicit / announced shape: {big[0]} {big[1]}  -> {'>= 20: a candidate' if big[0] >= 20 else 'below the 20-site floor'}")
print("\n".join(out))
io.open(os.path.join(HERE, "_s40_r6_quizsignals.log"), "w", encoding="utf-8", newline="").write("\n".join(out) + "\n")
