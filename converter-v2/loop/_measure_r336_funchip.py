#!/usr/bin/env python3
"""ROUND 336 PICK probe (loop session 6) — the OVERVIEW #module-code CHIP per registry base: the gold's chip form on every
overview page (absent / full-code / padded-number / free-text) vs the value the registry RESOLVES for that module
(outputs/_r336_resolved.json from _r336_resolve_all.cjs). A family whose gold form solidifies (share >= 0.60, n >= 3 modules)
and whose resolved value differs is the class. Run from anywhere; writes _r336_funchip.json next to itself."""
import re, glob, os, json, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
res = json.load(open(os.path.join(HERE, "_r336_resolved.json"), encoding="utf-8"))
def base_of(code):
    m = re.match(r"([A-Z]+)", code); return m.group(1) if m else code
def chip_form(html, code):
    h = html.split('<div id="header"', 1)[-1].split('<div id="body"', 1)[0]
    h = re.sub(r"<!--[\s\S]*?-->", "", h)
    m = re.search(r'id="module-code"[^>]*>\s*<h1>(.*?)</h1>', h, re.S)
    if not m: return "absent"
    t = re.sub(r"<[^>]+>", "", m.group(1)).strip()
    if t == code: return "full-code"
    if re.fullmatch(r"\d\d", t): return "padded-number"
    if re.fullmatch(r"\d+(\.\d+)?", t): return "decimal"
    return "free-text"
def overview_page(files, code):
    # the overview = the page whose name carries _0_0 / -00 / .0. or the single file
    for f in files:
        b = os.path.basename(f)
        if re.search(r"(_0_0|-00|\.00?|^%s)\.html$" % re.escape(code), b) or len(files) == 1: return f
    return sorted(files)[0]
gold = collections.defaultdict(collections.Counter); mods = collections.defaultdict(set); claude = collections.defaultdict(collections.Counter)
for f in glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*")):
    code = os.path.basename(f); tmpl = os.path.basename(os.path.dirname(f))
    gfiles = [g for g in glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", tmpl, code, "*.html")) if not re.search(r"acks|ackn", g, re.I)]
    cfiles = glob.glob(os.path.join(f, "*.html"))
    if not gfiles or not cfiles or code not in res: continue
    b = base_of(code)
    gform = chip_form(open(overview_page(gfiles, code), encoding="utf-8", errors="replace").read(), code)
    cform = chip_form(open(overview_page(cfiles, code), encoding="utf-8", errors="replace").read(), code)
    gold[(tmpl, b)][gform] += 1; claude[(tmpl, b)][cform] += 1; mods[(tmpl, b)].add(code)
rows = []
for k in sorted(gold):
    n = sum(gold[k].values()); form, c = gold[k].most_common(1)[0]; share = c / n
    cf = claude[k].most_common(1)[0][0]
    resolved = collections.Counter(res[m]["module_code"].get("overview") for m in mods[k] if "module_code" in res[m])
    mismatch = sum(v for f2, v in claude[k].items() if f2 != form)
    flag = "CLASS" if (share >= 0.60 and n >= 3 and mismatch and mismatch / n >= 0.5) else ""
    rows.append({"tmpl": k[0], "base": k[1], "n": n, "gold": dict(gold[k]), "gold_form": form, "share": round(share, 2), "claude": dict(claude[k]), "resolved": dict(resolved), "mismatch_modules": mismatch, "flag": flag})
    if flag or mismatch: print(f"{k[0]:12} {k[1]:8} n={n:3} gold {dict(gold[k])} ({form} {share:.2f}) | claude {dict(claude[k])} | resolved {dict(resolved)} {flag}")
json.dump(rows, open(os.path.join(HERE, "_r336_funchip.json"), "w", encoding="utf-8"), indent=1)
cls = [r for r in rows if r["flag"]]
print("CLASS rows:", [(r["tmpl"], r["base"], r["n"], r["gold_form"]) for r in cls], "modules", sum(r["n"] for r in cls))
