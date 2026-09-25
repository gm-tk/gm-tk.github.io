"""_s50_r4_barehover.py — session 50 Round 4 PICK: every BARE `[hover]` red tag in the Writers Templates (no colon, no
'definition' / 'trigger' word), by FORM, with the module's gold infoTrigger (info="…", anchor) matched against it.
  P  — `ANCHOR [hover] (DEF) rest…`   the def in parentheses right after the tag (black)
  R  — `ANCHOR [hover] DEF` / `[hover DEF]` the def inside the red span
  O  — anything else (the tag then a black sentence, alone on a line, …)
Run under WSL from CONVERTER_V2/outputs/."""
import os, re, glob, html, json, collections
G = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_"
RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴")
norm = lambda s: re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()
forms = collections.Counter(); gold_hit = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for wt in glob.glob(f"{G}/*/*/*_parsed.txt"):
    if re.search(r"/[^/+]* Media List_parsed\.txt$", wt): continue
    code = wt.split("/")[-2]
    golds = [open(p, encoding="utf-8", errors="ignore").read() for p in glob.glob(os.path.join(os.path.dirname(wt), "*.html"))]
    infos = [(norm(html.unescape(i)), norm(re.sub(r"<[^>]+>", " ", a))) for g in golds for i, a in re.findall(r'class="infoTrigger[^"]*"[^>]*\binfo="([^"]*)"[^>]*>(.*?)</span>', g, re.S)]
    for ln in open(wt, encoding="utf-8", errors="ignore").read().split("\n"):
        for m in RED.finditer(ln):
            red = m.group(1)
            b = re.search(r"\[\s*hover\s*([^\]:]*)\]", red, re.I)
            if not b or re.search(r"defin|trigger|info|shape|:", b.group(0), re.I): continue
            inside = (b.group(1) + " " + red[b.end():]).strip()
            after = ln[m.end():]
            before = re.sub(RED, " ", ln[:m.start()]).strip()
            pm = re.match(r"\s*\(([^)]{1,120})\)", after)
            if inside and len(inside) > 1: f, dfn = "R", inside
            elif pm: f, dfn = "P", pm.group(1)
            else: f, dfn = "O", after.strip()[:80]
            anchor = " ".join(before.split()[-2:])
            k = norm(dfn)
            hit = any(k and (k == i or (len(k) >= 6 and (k in i or i in k))) for i, a in infos)
            forms[f] += 1; mods[f].add(code); gold_hit[(f, hit)] += 1
            if len(ex[f]) < 8: ex[f].append(f"{code}: …{anchor[-25:]} [hover] {dfn[:50]!r} gold-info-hit={hit}")
out = ["BARE [hover] forms: " + ", ".join(f"{f} {n} spans / {len(mods[f])} modules" for f, n in forms.most_common()),
       "gold info= match: " + ", ".join(f"{f}:{h} {n}" for (f, h), n in sorted(gold_hit.items()))]
for f, e in ex.items(): out += [f"== {f}"] + ["  " + x for x in e]
out.append("modules P: " + " ".join(sorted(mods["P"]))); out.append("modules R: " + " ".join(sorted(mods["R"])))
open("_s50_r4_barehover.log", "w").write("\n".join(out) + "\n"); print("\n".join(out))
