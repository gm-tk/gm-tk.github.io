#!/usr/bin/env python3
"""r369 — number-policy variants scored with the skeleton gate's OWN match() (scaffold), no engine run:
the disk page's `number=` attributes are rewritten in memory under each policy and scored against the gold.
  DL  : majority digit (lesson pages) + a duplicate / non-letter takes the SMALLEST unused letter (cascades)
  LA  : majority digit + a duplicate / non-letter takes the smallest letter unused by ANY box on the page (look-ahead; later writer letters untouched)
  LAD : LA, letters only for boxes whose digit was foreign or whose id is a duplicate at first sight — same as LA
  D   : majority digit only; the fixed box takes the LA letter; genuine duplicate letters left alone
  L   : LA letters only, no digit change
Reports per variant: changed paired pages, up / down / same, pp-sum. Lesson number = the page's `<h1>N.M</h1>` chip when present.
"""
import os, sys, re, json, tempfile, collections, string
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
sys.path.insert(0, TESTS)
import _corpus
from _discrepancy_audit import pairs
from _skeleton_compare import match
from anchor_compare import CLAUDE, HUMAN

RE = re.compile(r'(<div class="(?:[^"]*\s)?activity(?:\s[^"]*)?"[^>]*? number=")([^"]*)(")')
RE_ID = re.compile(r'^(\d+)([A-Za-z]?)$')

def ids_of(html):
    return [(m.start(), m.group(1), m.group(2), m.group(3), len(m.group(0))) for m in RE.finditer(html)]

def policy(ids, mode, lesson_ok):
    parsed = [RE_ID.match(i.strip()) for i in ids]
    if not parsed or any(p is None or not p.group(2) for p in parsed) or len(ids) > 26: return None
    P = [(int(p.group(1)), p.group(2).upper()) for p in parsed]
    maj = None
    if mode in ("DL", "LA", "D") and lesson_ok and len(P) >= 2:
        c = collections.Counter(d for d, _ in P).most_common()
        if (len(c) == 1 or c[0][1] > c[1][1]) and c[0][1] * 2 > len(P): maj = c[0][0]
    all_letters = collections.defaultdict(set)
    for d, l in P: all_letters[maj if maj is not None else d].add(l)
    used = set(); out = []
    for i, (d, l) in enumerate(P):
        nd = maj if maj is not None else d
        foreign = (maj is not None and d != maj)
        dup = (len(l) == 1 and l in string.ascii_uppercase and (nd, l) in used)
        badl = not (len(l) == 1 and l in string.ascii_uppercase)
        fix_letter = False
        if mode == "DL": fix_letter = dup or badl
        elif mode == "LA": fix_letter = dup or badl
        elif mode == "D": fix_letter = foreign and (dup or badl)
        elif mode == "L": fix_letter = dup or badl
        if mode == "L": nd = d
        if fix_letter:
            if mode == "DL":
                l = next(c for c in string.ascii_uppercase if (nd, c) not in used)
            else:
                taken = {x for (dd, x) in used if dd == nd} | all_letters[nd]
                l = next((c for c in string.ascii_uppercase if c not in taken), l)
        used.add((nd, l)); out.append("%d%s" % (nd, l))
    return out

def main():
    modes = ["DL", "LA", "D", "L"]
    stats = {m: collections.Counter() for m in modes}; dips = {m: [] for m in modes}; pp = {m: 0.0 for m in modes}
    tmp = tempfile.mkdtemp()
    for code in _corpus.gate_mods(CLAUDE):
        for n, cp, hp in pairs(code):
            if not (cp and hp and os.path.exists(cp) and os.path.exists(hp)): continue
            if re.search(r"acks|acknowledge|glossary|references", os.path.basename(hp), re.I): continue
            html = open(cp, encoding="utf-8", errors="replace").read()
            hits = ids_of(html)
            if not hits: continue
            ids = [h[2] for h in hits]
            m = re.search(r"<h1>\s*(\d+)(?:\.\d+)?\s*</h1>", html)
            lesson_ok = bool(m and int(m.group(1)) > 0) and not re.search(r"_0_0\.html$", cp)
            base = None
            for mode in modes:
                new = policy(ids, mode, lesson_ok)
                if new is None or new == ids: continue
                out = []; cur = 0
                for h, nid in zip(hits, new):
                    out.append(html[cur:h[0]]); out.append(h[1] + nid + h[3]); cur = h[0] + h[4]
                out.append(html[cur:])
                tp = os.path.join(tmp, "v.html"); open(tp, "w", encoding="utf-8").write("".join(out))
                if base is None: base, _, _ = match(cp, hp, scaffold=True)
                b, _, _ = match(tp, hp, scaffold=True)
                d = 100 * (b - base); pp[mode] += d; stats[mode]["changed"] += 1
                if d > 1e-9: stats[mode]["up"] += 1
                elif d < -1e-9: stats[mode]["down"] += 1; dips[mode].append((round(d, 1), code, os.path.basename(cp), ids[:6], new[:6]))
                else: stats[mode]["same"] += 1
    for mode in modes:
        print(mode, dict(stats[mode]), "pp-sum %+.1f" % pp[mode])
        for x in sorted(dips[mode])[:6]: print("    dip", x)
    json.dump({m: dict(stats[m]) for m in modes} | {"pp": pp}, open(os.path.join(HERE, "_r369_variants.json"), "w"), indent=1)

main()
