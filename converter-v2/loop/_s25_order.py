#!/usr/bin/env python3
"""Session 25 — the ORDER GAP: per paired page, the gate's sequence ratio (difflib, autojunk=False) vs a position-free
multiset ratio (2·|multiset ∩| / (|gold|+|Claude|)) over the same scaffold skeleton lines. The gap is what ORDER costs —
a block Claude ships in the wrong place. Aggregated per template / subject with the top pages, and a census of where the
distinct top-level blocks sit (the supervisor row, the intro heading row, the first widget, the first activity) — first /
second / later — gold vs Claude.  python3 _s25_order.py [prefix-filter] [--pages N]"""
import os, sys, re, difflib, json
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
sys.path.insert(0, TESTS)
import _corpus
from _skeleton_compare import _skel
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)
argv = list(sys.argv[1:]); npages = 25
if "--pages" in argv:
    i = argv.index("--pages"); npages = int(argv[i + 1]); del argv[i:i + 2]
args = [a for a in argv if not a.startswith("--")]
flt = args[0] if args else ""

def ind(l): return len(l) - len(l.lstrip(" "))

def multiset_ratio(a, b):
    ca, cb = Counter(a), Counter(b)
    inter = sum((ca & cb).values())
    return 2.0 * inter / max(len(a) + len(b), 1)

def top_kinds(lines):
    """the sequence of top-level #body children as coarse kinds"""
    bi = None
    for i, l in enumerate(lines):
        if l.strip().startswith("div#body") and ind(l) <= 4:
            bi = i; break
    if bi is None: return []
    base = ind(lines[bi]); out = []
    i = bi + 1; n = len(lines)
    while i < n and ind(lines[i]) > base:
        if ind(lines[i]) == base + 2:
            s = lines[i].strip()
            if s.startswith("div.row.supervisor") or s == "div.row.supervisor": k = "supervisor"
            elif s.startswith("div.row"):
                # the opener of the row's first column
                j = i + 1; k = "row"
                while j < n and ind(lines[j]) > base + 2:
                    if ind(lines[j]) == base + 6:
                        t = lines[j].strip()
                        k = ("row:activity" if t.startswith("div.activity") else "row:alert" if t.startswith("div.alert")
                             else "row:WIDGET" if t == "WIDGET" else "row:h" if re.match(r"h[1-6]\b", t) else "row:" + t.split(".")[0].split("[")[0])
                        break
                    j += 1
            elif s == "WIDGET": k = "WIDGET"
            elif "Panel" in s: k = "panel"
            elif s.startswith("div.phases"): k = "phases"
            elif s.startswith("div.crumbs"): k = "crumbs"
            elif s.startswith("div.introduction"): k = "introduction"
            else: k = s.split(".")[0].split("[")[0]
            out.append(k)
        i += 1
    return out

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
res = defaultdict(lambda: {"pages": 0, "seq": 0.0, "ms": 0.0, "gap": 0.0, "gap5": 0, "gap10": 0})
rows = []
pos = defaultdict(lambda: {"gold": Counter(), "claude": Counter()})
firsts = defaultdict(lambda: {"gold": Counter(), "claude": Counter()})
for code in sorted(fam):
    if flt and not code.startswith(flt): continue
    tf = fam[code]
    subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g = _skel(hp, True); c = _skel(cp, True)
        except Exception:
            continue
        seq = difflib.SequenceMatcher(None, g, c, autojunk=False).ratio()
        ms = multiset_ratio(g, c)
        gap = (ms - seq) * 100
        ptype = "overview" if n == 0 else "lesson"
        keys = ("ALL", f"template={tf}", f"template+ptype={tf}/{ptype}", f"subject={subject}")
        for k in keys:
            R = res[k]; R["pages"] += 1; R["seq"] += seq * 100; R["ms"] += ms * 100; R["gap"] += gap
            if gap >= 5: R["gap5"] += 1
            if gap >= 10: R["gap10"] += 1
        rows.append((round(gap, 1), round(seq * 100, 1), round(ms * 100, 1), code, os.path.basename(cp), tf, subject))
        gk = top_kinds(g); ck = top_kinds(c)
        for k in keys:
            for side, seqk in (("gold", gk), ("claude", ck)):
                if seqk: firsts[k][side][seqk[0]] += 1
                if "supervisor" in seqk:
                    p = seqk.index("supervisor")
                    pos[k][side]["supervisor@" + ("first" if p == 0 else "second" if p == 1 else "later")] += 1
                if "row:WIDGET" in seqk or "WIDGET" in seqk:
                    p = min([i for i, x in enumerate(seqk) if x in ("row:WIDGET", "WIDGET")])
                    pos[k][side]["firstWidget@" + ("first" if p == 0 else "second" if p == 1 else "later")] += 1

def line(c):
    t = sum(c.values()) or 1
    return ", ".join(f"{k} {v} ({v/t:.2f})" for k, v in c.most_common(8))
for k in sorted(res, key=lambda k: (0 if k == "ALL" else 1 if k.startswith("template=") else 2 if k.startswith("template+") else 3, -res[k]["pages"])):
    R = res[k]
    if R["pages"] < 30: continue
    p = R["pages"]
    print(f"\n== {k} — pages {p}: sequence {R['seq']/p:.2f} %  multiset {R['ms']/p:.2f} %  ORDER GAP {R['gap']/p:.2f}pp  (gap ≥5pp on {R['gap5']} pages, ≥10pp on {R['gap10']})")
    print(f"   first top-level block gold: {line(firsts[k]['gold'])}")
    print(f"   first top-level block claude: {line(firsts[k]['claude'])}")
    print(f"   positions gold: {line(pos[k]['gold'])}")
    print(f"   positions claude: {line(pos[k]['claude'])}")
print(f"\n== the {npages} pages with the largest order gap (gap, seq, multiset, module, page, template, subject)")
for r in sorted(rows, key=lambda r: -r[0])[:npages]: print("  ", r)
json.dump(rows, open("/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs/_s25_order.json", "w"))
