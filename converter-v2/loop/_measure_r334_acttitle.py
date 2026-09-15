"""ROUND 334 PICK probe — the ACTIVITY TITLE HEADING LEVEL: the first child of an activity box's own row>col-12 when it is a
heading — gold vs Claude level per template (the KB 01F activity_heading form is <h3>). Counts boxes, pages and modules."""
import re, glob, os, collections, json
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
RX = re.compile(r'<div class="(activity[^"]*)"[^>]*>\s*(?:<div class="super-content row">.*?</div>\s*</div>\s*</div>\s*</div>\s*)?<div class="row">\s*<div class="col-12">\s*<(h[1-6])\b', re.S)
def census(root):
    lv = collections.defaultdict(collections.Counter); pages = collections.defaultdict(set); mods = collections.defaultdict(set)
    for f in glob.glob(os.path.join(ROOT, root, "*", "*", "*.html")):
        if re.search(r"acks|ackn", f, re.I): continue
        tmpl = os.path.basename(os.path.dirname(os.path.dirname(f))); code = os.path.basename(os.path.dirname(f))
        s = open(f, encoding="utf-8", errors="replace").read().split('<div id="body"', 1)[-1]
        for m in RX.finditer(s):
            lv[tmpl][m.group(2)] += 1
            if m.group(2) != "h3": pages[tmpl].add(f); mods[tmpl].add(code)
    return lv, pages, mods
g, gp, gm = census("01-Finalized_Modules_"); c, cp, cm = census("01-Claude_Modules_")
out = {}
for t in sorted(set(g) | set(c)):
    gn = sum(g[t].values()); cn = sum(c[t].values())
    print(f"{t:12} GOLD {dict(g[t].most_common())} h3 share {g[t]['h3']/gn if gn else 0:.3f} | CLAUDE {dict(c[t].most_common())} non-h3 on {len(cp[t])} pages / {len(cm[t])} modules")
    out[t] = {"gold": dict(g[t]), "claude": dict(c[t]), "claude_non_h3_pages": len(cp[t]), "claude_non_h3_modules": sorted(cm[t])}
json.dump(out, open(os.path.join(HERE, "_r334_acttitle.json"), "w", encoding="utf-8"), indent=1)
tot_p = sum(len(v) for v in cp.values()); tot_m = len(set().union(*cm.values())) if cm else 0
print("TOTAL Claude non-h3 title boxes:", sum(v for t in c for k, v in c[t].items() if k != "h3"), "pages", tot_p, "modules", tot_m)
