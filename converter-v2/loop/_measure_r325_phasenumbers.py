#!/usr/bin/env python3
"""ROUND 325 measure — phase-scoped activity numbering on Fundamentals pages (the r217 recorded follow-up).
For every Fundamentals page with `div.fundamentalsPanel[phase=N]` panels, on both sides: the activity boxes
per phase panel (their number= or '-'). Simulate Claude's boxes numbered {phase}{A,B,C…} in panel order
(keeping a writer letter id as-is when it already carries one? — two simulations: (a) renumber only the
unnumbered / bare-digit boxes, keeping lettered ids; (b) renumber all positionally). Count position-wise
number matches per panel before / after. Writes outputs/_r325_phasenumbers.json."""
import re, glob, os, json, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PANEL = re.compile(r'<div class="fundamentalsPanel"[^>]*phase="(\d+)"[^>]*>', re.I)
BOX = re.compile(r'<div class="(activity[^"]*)"(?: number="([^"]*)")?[^>]*>')
def panels(s):
    """[(phase, [numbers…])] using the balanced span of each panel."""
    out = []
    for m in PANEL.finditer(s):
        i = m.end(); depth = 1; j = len(s)
        for mm in re.finditer(r'<div\b|</div>', s[i:]):
            depth += 1 if mm.group(0) == "<div" else -1
            if depth == 0: j = i + mm.start(); break
        out.append((int(m.group(1)), [n or "-" for _, n in BOX.findall(s[i:j])]))
    return out
def sim(boxes, phase, keep_letters):
    out = []; k = 0
    for n in boxes:
        if keep_letters and re.match(r"^\d+[A-Z]$", n):
            out.append(n); k = ord(n[-1]) - 64   # continue after the writer's letter
        else:
            out.append(f"{phase}{chr(65 + k) if k < 26 else '?'}"); k += 1
    return out
tot = collections.Counter(); per_mod = {}
CROOT = os.environ.get("CLAUDE_ROOT")   # an alternative Claude tree (the probe's --save dir: <dir>/<CODE>/*.html)
for cd in sorted(glob.glob(os.path.join(CROOT, "*")) if CROOT else glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "Fundamentals", "*"))):
    code = os.path.basename(cd)
    gd = os.path.join(ROOT, "01-Finalized_Modules_", "Fundamentals", code)
    if not os.path.isdir(gd): continue
    for cf in sorted(glob.glob(os.path.join(cd, "*.html"))):
        cs = open(cf, encoding="utf-8", errors="replace").read()
        cp = panels(cs)
        if not cp: continue
        # the gold page: single-file modules keep one page; multi-page gold pairs by phase across files
        gp = {}
        for gf in glob.glob(os.path.join(gd, "*.html")):
            for ph, nums in panels(open(gf, encoding="utf-8", errors="replace").read()):
                gp.setdefault(ph, []).extend(nums)
        if not gp: continue
        for ph, boxes in cp:
            g = gp.get(ph, [])
            before = sum(1 for i, n in enumerate(boxes) if i < len(g) and n != "-" and n == g[i])
            sa = sim(boxes, ph, True); sb = sim(boxes, ph, False)
            after_a = sum(1 for i, n in enumerate(sa) if i < len(g) and n == g[i])
            after_b = sum(1 for i, n in enumerate(sb) if i < len(g) and n == g[i])
            tot["claude_boxes"] += len(boxes); tot["gold_boxes"] += len(g)
            tot["unnumbered"] += sum(1 for n in boxes if n == "-"); tot["bare_digit"] += sum(1 for n in boxes if re.match(r"^\d+$", n))
            tot["match_before"] += before; tot["match_keep_letters"] += after_a; tot["match_positional"] += after_b
            per_mod.setdefault(code, []).append({"page": os.path.basename(cf), "phase": ph, "claude": boxes, "gold": g, "sim_keep": sa})
json.dump({"totals": dict(tot), "per_module": per_mod}, open(os.path.join(ROOT, "CONVERTER_V2", "outputs", os.environ.get("OUT_NAME", "_r325_phasenumbers.json")), "w", encoding="utf-8"), indent=1)
print(dict(tot))
print("modules with phase panels:", len(per_mod))
for code, rows in list(per_mod.items())[:6]:
    for r in rows[:3]: print(f"  {code} p{r['phase']}: claude {r['claude']} -> {r['sim_keep']} | gold {r['gold']}")
