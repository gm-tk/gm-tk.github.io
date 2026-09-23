#!/usr/bin/env python3
"""Session 40 r448 — survey the un-built quiz-type bundles (_s40_r448_quizdiag_all.log): how many carry a
highlight / green answer mark (black members' block.marks, table members' cellMarks) and how many carry red
'noise' members (red plain words — BLL244's answer words); the noise texts by frequency; per type."""
import io, re, collections, os
HERE = os.path.dirname(os.path.abspath(__file__))
cur = None; B = []
for ln in io.open(os.path.join(HERE, "_s40_r448_quizdiag_all.log"), encoding="utf-8", errors="replace"):
    if ln.startswith("BUNDLE "):
        p = ln.split()
        cur = dict(code=p[1], idx=p[2], type=p[3], built=p[4] == "built=true", act=p[5], marks=0, cellmarks=0, noise=[], members=0)
        B.append(cur); continue
    if cur is None or not ln.startswith("   "): continue
    f = ln.rstrip("\n").strip().split("\t")
    cur["members"] += 1
    if '"kind":"hl"' in ln or '"kind":"green"' in ln:
        if "cellMarks:" in ln: cur["cellmarks"] += ln.count('"kind":')
        else: cur["marks"] += ln.count('"kind":')
    if len(f) > 1 and f[1] == "cls=noise":
        cur["noise"].append((f[4][5:] if len(f) > 4 else "", f[5][6:] if len(f) > 5 else ""))
seen = set(); U = []
for b in B:   # de-duplicate repeated Build calls on the same bundle
    k = (b["code"], b["idx"], b["type"])
    if k in seen: continue
    seen.add(k); U.append(b)
unb = [b for b in U if not b["built"]]
print(f"quiz bundles (dedup) {len(U)}; un-built {len(unb)}")
bt = collections.defaultdict(lambda: collections.Counter())
for b in unb:
    t = bt[b["type"]]; t["bundles"] += 1
    if b["marks"] or b["cellmarks"]: t["with_marks"] += 1; t["marks"] += b["marks"] + b["cellmarks"]
    if b["noise"]: t["with_noise"] += 1; t["noise"] += len(b["noise"])
for k, t in sorted(bt.items(), key=lambda kv: -kv[1]["bundles"]):
    print(f"  {k:15s} bundles {t['bundles']:4d} | with hl/green marks {t['with_marks']:4d} ({t['marks']} marks) | with red noise members {t['with_noise']:4d} ({t['noise']} members)")
mods_m = {b["code"] for b in unb if b["marks"] or b["cellmarks"]}; mods_n = {b["code"] for b in unb if b["noise"]}
print(f"modules: marks {len(mods_m)}, noise {len(mods_n)}, either {len(mods_m | mods_n)}")
nc = collections.Counter(t for b in unb for t, a in b["noise"])
print("red noise texts (top 60):")
for t, n in nc.most_common(60): print(f"  {n:4d}  {t!r}")
print("noise with an EMPTY black tail (the word alone):", sum(1 for b in unb for t, a in b["noise"] if not a.strip()))
print("examples by module:")
for b in unb[:0]: pass
for b in [b for b in unb if b["noise"]][:25]:
    print(f"  {b['code']} #{b['idx']} {b['type']} {b['act']}: " + " | ".join(f"{t} ‖ {a[:40]}" for t, a in b["noise"][:3]))
