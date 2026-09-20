#!/usr/bin/env python3
"""_s29_r6_emptybox.py — the writer-owned EMPTY activity box (session 29 Round 6 PICK candidate): a Claude `activity` box
whose visible content is nothing (or only cv2-notes / the `no content captured` flag). For each on a paired page: the
gold's box with the same number (present? what it holds), the WT bracket that carries the number (the opener's words),
by template | subject. Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s29_r6_emptybox.py
"""
import os, re, sys, json, glob, collections
sys.path.insert(0, ".")
import _discrepancy_audit as da, _corpus
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", ".."))
CLAUDE = os.path.join(ROOT, "01-Claude_Modules_"); GOLD = os.path.join(ROOT, "01-Finalized_Modules_")
meta = json.load(open(os.path.join(HERE, "..", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]

def boxes(html):
    out = []; stack = []
    for m in re.finditer(r"<(/?)div\b([^>]*)>", html):
        if m.group(1):
            if stack:
                st = stack.pop()
                if st[1] is not None: out.append((st[1], st[0], html[st[2]:m.start()]))
        else:
            if m.group(2).rstrip().endswith("/"): continue
            cls = re.search(r'class="([^"]*)"', m.group(2)); c = cls.group(1) if cls else ""
            num = re.search(r'number="([^"]*)"', m.group(2))
            isact = bool(re.search(r"(^|\s)activity(\s|$)", c)) and "cv2" not in c
            stack.append((c, (num.group(1).upper() if num else "-") if isact else None, m.end()))
    return out

def visible(inner):
    s = re.sub(r'<p class="cv2-(note|comment)"[^>]*>[\s\S]*?</p>', " ", inner)
    s = re.sub(r"<!--[\s\S]*?-->", " ", s)
    return re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", s)).strip()

def kind(inner):
    if re.search(r"INTERACTIVE \(un-built\)|cv2-interactive", inner): return "widget"
    if re.search(r"<(table|img|iframe|audio)\b", inner): return "media/table"
    t = visible(inner)
    return "text" if t else "EMPTY"

wt_cache = {}
def wt_lines(code):
    if code in wt_cache: return wt_cache[code]
    d = _corpus.mdir(GOLD, code); lines = []
    for f in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        if re.search(r"media list", os.path.basename(f), re.I) and not re.search(r"writers template", os.path.basename(f), re.I): continue
        lines += open(f, encoding="utf-8", errors="replace").read().split("\n")
    wt_cache[code] = lines; return lines

def opener_for(code, num):
    pat = re.compile(r"\[[^\]]*activit[^\]]*\b" + re.escape(num) + r"\b[^\]]*\]", re.I)
    for ln in wt_lines(code):
        m = pat.search(ln)
        if m: return m.group(0)[:70]
    return "?"

mods = _corpus.gate_mods(CLAUDE)
tot = collections.Counter(); grp = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); openers = collections.Counter()
pages = set(); modules = set()
for code in mods:
    try: prs = da.pairs(code)
    except Exception: continue
    mm = meta.get(code, {}); g = (mm.get("template_type", ""), mm.get("subject", ""))
    for t in prs:
        cp, hp = t[1], t[2]
        try: c = open(cp, encoding="utf-8").read(); gh = open(hp, encoding="utf-8", errors="replace").read()
        except Exception: continue
        gb = {n: (cl, inner) for n, cl, inner in boxes(gh)}
        for num, cl, inner in boxes(c):
            if visible(inner): continue
            if "cv2-interactive" in inner: continue
            op = opener_for(code, num) if num != "-" else "(numberless)"
            oword = re.sub(r"\s+", " ", op.lower())
            okey = "journal-instruction" if re.search(r"journal|complete activity|complete the activit", oword) else ("embedded/brainstorm" if "embedded" in oword or "brainstorm" in oword else ("(numberless)" if num == "-" else "other:" + oword[:40]))
            if num in gb: k = "gold same number: " + kind(gb[num][1])
            else: k = "gold: no box with that number"
            tot[k] += 1; grp[g][k] += 1; openers[okey] += 1; pages.add(cp); modules.add(code)
            if len(ex[(k, okey)]) < 4: ex[(k, okey)].append("%s %s %s" % (os.path.basename(cp), num, op))
print("Claude EMPTY writer-owned boxes on paired pages: %d | pages %d | modules %d" % (sum(tot.values()), len(pages), len(modules)))
for k, v in tot.most_common(): print("  %4d  %s" % (v, k))
print("\nby opener form:")
for k, v in openers.most_common(15): print("  %4d  %s" % (v, k))
print("\nexamples:")
for (k, o), v in sorted(ex.items(), key=lambda x: -len(x[1]))[:14]: print("  [%s | %s] %s" % (k, o, " ; ".join(v)))
print("\nby group:")
for g, cnt in sorted(grp.items(), key=lambda x: -sum(x[1].values()))[:12]: print("  %-14s %-26s %s" % (g[0], g[1][:26], dict(cnt)))
