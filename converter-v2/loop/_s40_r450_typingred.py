#!/usr/bin/env python3
"""Session 40 r450 — the RED-ANSWER typing family: every un-built, single (not merged), non-table typing bundle whose
question lines carry the writer's red answer (inline — BLL244 'What' + tail; at the line's end — PHE1007 '… joint.
[red] Hip Shoulder'; alone on its own line). For each: the (question, red answer) pairs, and whether the module's GOLD
has a typing input whose answer= attribute equals the red answer (normalised) — the gold agreement the build rests on."""
import io, os, re, json, glob, collections, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RED_SKIP = re.compile(r"^[^\w]*$")
RED_PLAIN = re.compile(r"^(?:answers?|correct answers?|for media|associated media|teacher[- ]marked|\(?image\)?|media)\s*[:.]?$|:$", re.I)
ANS = re.compile(r'<input[^>]*\banswer="([^"]*)"', re.I)
norm = lambda s: re.sub(r"[^\w]+", " ", H.unescape(s).lower()).strip()
gold_answers = {}
def gold(code):
    if code not in gold_answers:
        s = set()
        for f in glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, "*.html")):
            for a in ANS.findall(io.open(f, encoding="utf-8", errors="replace").read()):
                for x in a.split("||"): s.add(norm(x))
        gold_answers[code] = s
    return gold_answers[code]
tot = collections.Counter(); per = []
for l in io.open(os.path.join(HERE, "_s40_typing.jsonl"), encoding="utf-8"):
    b = json.loads(l)
    if b["built"] or b["extra"] or any(m["type"] == "table" for m in b["members"]): continue
    pairs = []
    prev = None
    for m in b["members"]:
        if m["type"] == "tag" and m["cls"] == "noise":
            w = re.sub(r"\s+", " ", m["text"]).strip()
            if w and not RED_SKIP.match(w) and not RED_PLAIN.search(w):
                form = "inline" if m["after"].strip() else ("end" if prev is not None and prev["type"] == "black" else "alone")
                pairs.append((form, w, (prev["text"] if prev and prev["type"] == "black" and form != "inline" else m["after"])[:60]))
        prev = m
    if not pairs: continue
    g = gold(b["code"])
    hit = sum(1 for f, w, q in pairs if norm(w) in g or any(norm(x) in g for x in re.split(r"\s*(?:/|,|\bor\b)\s*", w) if x))
    per.append((b["code"], b["idx"], b["act"], len(pairs), hit, collections.Counter(f for f, _, _ in pairs), pairs[:3]))
    tot["bundles"] += 1; tot["pairs"] += len(pairs); tot["gold_hit"] += hit
print(f"red-answer typing bundles (single, lines): {tot['bundles']} / modules {len({p[0] for p in per})}; answers {tot['pairs']}; found as a gold answer= {tot['gold_hit']} ({100*tot['gold_hit']/max(1,tot['pairs']):.0f}%)")
for p in per:
    print(f"  {p[0]}#{p[1]} {p[2]}: {p[3]} answers, gold-matched {p[4]}  forms {dict(p[5])}  e.g. " + " | ".join(f"{f}:{w!r}<-{q!r}" for f, w, q in p[6])[:230])
