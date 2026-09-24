#!/usr/bin/env python3
"""Session 46 Round 1 — every accHead title on the r491 ON pages (outputs/_r491_on) that is NOT on the disk page (the new
panels), located in the module's gold by _s46_goldloc: accordion head / other container / absent. WSL, from outputs/."""
import os, re, sys, html, collections
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _s46_goldloc import locate, fold
ON = "_r491_on"; CLA = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Claude_Modules_"
HEAD = re.compile(r'<div class="accHead"><h4>(.*?)</h4></div>', re.S)
def claude_disk(code, fn):
    for t in os.listdir(CLA):
        p = os.path.join(CLA, t, code, fn)
        if os.path.exists(p): return open(p, encoding="utf-8").read()
    return ""
tally = collections.Counter()
for code in sorted(os.listdir(ON)):
    for fn in sorted(os.listdir(os.path.join(ON, code))):
        if not fn.endswith(".html"): continue
        new = [html.unescape(re.sub("<[^>]+>", "", h)).strip() for h in HEAD.findall(open(os.path.join(ON, code, fn), encoding="utf-8").read())]
        old = set(fold(html.unescape(re.sub("<[^>]+>", "", h))) for h in HEAD.findall(claude_disk(code, fn)))
        added = [h for h in new if fold(h) not in old]
        res = []
        for h in added:
            hits = locate(code, h)
            kind = "ACC" if any("accHead" in c for _, c, _ in hits) else ("other:" + hits[0][1].split(" > ")[-1] if hits else "absent")
            tally[kind.split(":")[0]] += 1
            res.append(f"{h[:38]!r}→{kind[:40]}")
        print(f"{code}/{fn}: +{len(added)}  " + " | ".join(res))
print("\nTALLY", dict(tally))
