#!/usr/bin/env python3
"""Session 29 Round 3 PICK — per-prefix skeleton mean over the r411 state, the September-intake modules flagged.
Reads outputs/_s29_r411_sk_final.json + 00-NEW_NEW_NEW/_MOVE_LOG_2026-09-19.tsv (the 98 intake codes)."""
import json, os, re, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.join(HERE, "..", "..")
sk = json.load(open(os.path.join(HERE, "_s29_r411_sk_final.json")))
new = set()
mv = os.path.join(ROOT, "00-NEW_NEW_NEW", "_MOVE_LOG_2026-09-19.tsv")
if os.path.exists(mv):
    for l in open(mv, encoding="utf-8", errors="replace"):
        m = re.match(r"([A-Z]+[0-9A-Z]*)\b", l.strip())
        if m: new.add(m.group(1))
by = collections.defaultdict(list); mods = collections.defaultdict(set)
for p in sk["per_page"]:
    pre = re.match(r"[A-Z]+", p["module"]).group(0)
    by[pre].append(p["scaffold"]); mods[pre].add(p["module"])
rows = []
for pre, v in by.items():
    isnew = sum(1 for m in mods[pre] if m in new)
    rows.append((100 * sum(v) / len(v), pre, len(v), len(mods[pre]), isnew))
rows.sort()
print("%-9s %6s %5s %4s %4s" % ("prefix", "mean", "pages", "mods", "NEW"))
for mean, pre, n, m, isnew in rows:
    if isnew or mean < 40:
        print("%-9s %6.1f %5d %4d %4d %s" % (pre, mean, n, m, isnew, "<- intake" if isnew else ""))
tot_new = [p["scaffold"] for p in sk["per_page"] if p["module"] in new]
tot_old = [p["scaffold"] for p in sk["per_page"] if p["module"] not in new]
print("\nintake pages %d mean %.2f%% | pre-existing pages %d mean %.2f%%" % (len(tot_new), 100 * sum(tot_new) / max(1, len(tot_new)), len(tot_old), 100 * sum(tot_old) / len(tot_old)))
print("intake codes recognised from the move log:", len(new))
