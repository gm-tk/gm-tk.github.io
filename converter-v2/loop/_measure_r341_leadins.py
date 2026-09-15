#!/usr/bin/env python3
"""_measure_r341_leadins.py — ROUND 341 PICK probe (KB constraint 23 / 01B: the lesson-menu labels are <h5>). Over EVERY paired page:
every Claude element (p / h5 / h4 / h3 / b-only p) whose folded text is a learning-design LEAD-IN (we are learning…, i can, you will show
your understanding by…, success criteria, learning intentions, how will i know…, WALT/WILF) → the gold's element for the SAME text on the
paired page (h5 / h4 / h3 / p / li / absent). Reports per template / subject / phrase / Claude-element. Writes _r341_leadins.json."""
import os, sys, re, json, collections, html as H
HERE = os.path.dirname(os.path.abspath(__file__)); T = os.path.normpath(os.path.join(HERE, "..", "reference", "tests")); sys.path.insert(0, T)
import _corpus
from _discrepancy_audit import pairs, CLAUDE
LEAD = re.compile(r"^(we(?:\s+are)?\s+learning\b|what are we learning|i can\b|you will (?:show|demonstrate) your understanding\b|success criteria|learning intentions?|how will i know|walt\b|wilf\b|ākonga will|akonga will|i am learning to|what am i learning|what will i learn)", re.I)
def fold(s):
    s = H.unescape(re.sub(r"<[^>]+>", " ", s)); s = re.sub(r"[\u2018\u2019'`´]", "'", s); s = re.sub(r"[^\w\s']", " ", s.lower()); return re.sub(r"\s+", " ", s).strip()
ELEM = re.compile(r"<(h[1-6]|p|li)\b[^>]*>([\s\S]*?)</\1>", re.I)
def elems(path):
    h = open(path, encoding="utf-8", errors="replace").read(); body = h.split("<body", 1)[-1]
    body = re.sub(r"<script[\s\S]*?</script>", "", body)
    out = []
    for m in ELEM.finditer(body):
        tag = m.group(1).lower(); inner = m.group(2)
        if re.search(r"<(p|li|h[1-6]|ul|ol|div)\b", inner, re.I): continue   # keep leaf-ish elements only
        t = fold(inner)
        if not t or len(t) > 80: continue
        out.append((tag, t, inner))
    return out
idx = json.load(open(os.path.join(T, "..", "..", "..", "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8")).get("module_meta", {})
rows = []
codes = sorted(d for d in _corpus.mods(CLAUDE) if os.path.isdir(_corpus.mdir(CLAUDE, d)))
for code in codes:
    tmpl = os.path.basename(os.path.dirname(_corpus.mdir(CLAUDE, code))); meta = idx.get(code, {})
    for n, cp, hp in pairs(code):
        if re.search(r"acks|acknowledge|glossary", os.path.basename(hp) + os.path.basename(cp), re.I): continue
        try: ce = elems(cp); ge = elems(hp)
        except Exception: continue
        gmap = collections.defaultdict(list)
        for tag, t, _ in ge: gmap[t].append(tag)
        gkeys = list(gmap.keys())
        for tag, t, inner in ce:
            if not LEAD.match(t): continue
            if tag in ("li",): continue
            # the gold's element for the same folded text (exact, else prefix-8-words)
            gold = gmap.get(t)
            if not gold:
                pre = " ".join(t.split()[:4])
                cand = [k for k in gkeys if k.startswith(pre)]
                gold = gmap[cand[0]] if cand else []
            g = gold[0] if gold else "absent"
            if len(gold) > 1 and "h5" in gold: g = "h5"
            phrase = LEAD.match(t).group(1).lower()
            phrase = re.sub(r"\s+", " ", phrase)
            rows.append({"code": code, "template": tmpl, "subject": meta.get("subject", "?"), "level": meta.get("level", meta.get("year_level", "?")), "page": os.path.basename(cp), "gold_page": os.path.basename(hp),
                         "claude": tag, "gold": g, "phrase": phrase, "text": t[:70], "overview": ("_0_0" in cp)})
json.dump({"rows": rows}, open(os.path.join(HERE, "_r341_leadins.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
def tally(label, rs):
    c = collections.Counter(r["gold"] for r in rs); found = sum(v for k, v in c.items() if k != "absent")
    print(f"{label:52s} n={len(rs):4d} pages={len(set((r['code'], r['page']) for r in rs)):4d} mods={len(set(r['code'] for r in rs)):3d} | gold {dict(c.most_common())} h5/found {c['h5']/found if found else 0:.2f}")
print("Claude lead-in elements (paired pages, non-acks):", len(rows))
P = [r for r in rows if r["claude"] == "p"]; H5 = [r for r in rows if r["claude"] == "h5"]
tally("ALL", rows); tally("  Claude ships <p>", P); tally("  Claude ships <h5>", H5); tally("  Claude ships other", [r for r in rows if r["claude"] not in ("p", "h5")])
print("\nClaude <p> lead-ins — by template:"); 
for t in ("Standard", "Bilingual", "Fundamentals", "Inquiry"): tally(f"  {t}", [r for r in P if r["template"] == t])
print("\nClaude <p> lead-ins — lesson vs overview:"); tally("  lesson pages", [r for r in P if not r["overview"]]); tally("  overview pages", [r for r in P if r["overview"]])
print("\nClaude <p> lead-ins — by phrase (lesson pages):")
byp = collections.defaultdict(list)
for r in P:
    if not r["overview"]: byp[r["phrase"]].append(r)
for k, rs in sorted(byp.items(), key=lambda kv: -len(kv[1])): tally(f"  {k}", rs)
print("\nClaude <p> lead-ins — by subject (lesson pages, n>=4):")
bys = collections.defaultdict(list)
for r in P:
    if not r["overview"]: bys[r["subject"]].append(r)
for k, rs in sorted(bys.items(), key=lambda kv: -len(kv[1])):
    if len(rs) >= 4: tally(f"  {k}", rs)
gold_h5 = [r for r in P if r["gold"] == "h5" and not r["overview"]]
print(f"\nFIX POPULATION (lesson pages, Claude p → gold h5): {len(gold_h5)} lines / {len(set((r['code'], r['page']) for r in gold_h5))} pages / {len(set(r['code'] for r in gold_h5))} modules")
print("modules:", " ".join(sorted(set(r["code"] for r in gold_h5))))
print("sample texts:", collections.Counter(r["text"] for r in gold_h5).most_common(25))
