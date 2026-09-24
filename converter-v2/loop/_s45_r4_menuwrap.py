#!/usr/bin/env python3
"""Session 45 Round 4 — the LESSON menu's wrapper: for every paired page (the skeleton gate's pairing) whose gold #module-menu-content is
non-empty, is its content BARE (the first element child is a heading / p / ul) or ROW-wrapped (div.row > div.col-*), and what does
Claude ship? Per subject (Module_Structure_Index module_meta), per page type (overview = _0_0 / lesson). WSL, from outputs/:
python3 _s45_r4_menuwrap.py > _s45_r4_menuwrap.log"""
import os, re, sys, io, json, collections
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
import _skeleton_compare as SK
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
META = json.load(io.open(os.path.join(ROOT, "pageforge-site", "converter-v2", "data", "Module_Structure_Index.json"), encoding="utf-8"))["module_meta"]
def form(path):
    try: s = io.open(path, encoding="utf-8", errors="replace").read()
    except Exception: return "nofile"
    m = re.search(r'<div[^>]*id="module-menu-content"[^>]*>', s)
    if not m: return "nomenu"
    rest = s[m.end():m.end() + 3000]
    rest = re.sub(r"<!--.*?-->", "", rest, flags=re.S)
    t = re.search(r"<\s*(/?)([a-zA-Z0-9]+)([^>]*)>", rest)
    if not t: return "empty"
    if t.group(1): return "empty"                      # the menu closes at once
    tag, attrs = t.group(2).lower(), t.group(3)
    cls = re.search(r'class="([^"]*)"', attrs); cls = cls.group(1) if cls else ""
    if tag == "div" and re.search(r"\brow\b", cls): return "row"
    if tag == "div" and "tabs" in cls: return "tabs"
    if tag == "div": return "div:" + (cls.split()[0] if cls else "")
    return "bare"
agg = collections.defaultdict(collections.Counter); mods = collections.defaultdict(lambda: collections.defaultdict(set))
pp = json.load(io.open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_diff_miner.json"), encoding="utf-8"))["per_page"]
for rec in pp:
    code, cpage, gpage = rec["module"], rec["page"], rec["gold"]
    g = form(os.path.join(_corpus.mdir(GOLD, code), gpage)); c = form(os.path.join(_corpus.mdir(CL, code), cpage))
    if g in ("nomenu", "empty", "nofile") or c in ("nofile",): continue
    ptype = "overview" if re.search(r"_0_0\.html$", cpage) else "lesson"
    subj = (META.get(code) or {}).get("subject", "?")
    for key in (("ALL", ptype), (subj, ptype)):
        agg[key][(g, c)] += 1; mods[key][(g, c)].add(code)
for key in sorted(agg, key=lambda k: -sum(agg[k].values())):
    tot = sum(agg[key].values())
    if tot < 15: continue
    gb = sum(n for (g, c), n in agg[key].items() if g == "bare")
    print(f"{key[0][:28]:28s} {key[1]:8s} n={tot:4d}  gold bare {gb / tot:.2f}  | " + "  ".join(
        f"{g}->{c} {n} ({len(mods[key][(g, c)])}m)" for (g, c), n in agg[key].most_common(5)))
print("\n1-10 Mathematics lessons by series prefix (the letters of the code) and by module:")
ser = collections.defaultdict(collections.Counter); bym = collections.defaultdict(collections.Counter)
for rec in pp:
    code, cpage, gpage = rec["module"], rec["page"], rec["gold"]
    if (META.get(code) or {}).get("subject") != "1-10 Mathematics" or re.search(r"_0_0\.html$", cpage): continue
    g = form(os.path.join(_corpus.mdir(GOLD, code), gpage)); c = form(os.path.join(_corpus.mdir(CL, code), cpage))
    if g in ("nomenu", "empty", "nofile"): continue
    ser[re.match(r"[A-Z]+", code).group(0)][(g, c)] += 1; bym[code][g] += 1
for s, c in sorted(ser.items()):
    tot = sum(c.values()); print(f"  {s:6s} n={tot:3d} " + "  ".join(f"{g}->{cl} {n}" for (g, cl), n in c.most_common()))
print("  per module (gold form counts):", {m: dict(c) for m, c in sorted(bym.items())})
