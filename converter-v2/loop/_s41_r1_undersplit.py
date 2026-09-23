#!/usr/bin/env python3
"""Session 41 Round 1 PICK — the UNDER-SPLIT modules: Claude builds fewer lesson pages than the human.
For every gold module dir with a Claude dir: gold page files vs Claude page files, the Claude files' page ids,
the gold ids missing, and the PageSplitter / PageAssembler notes from _run.json. Run under WSL."""
import json, os, re, glob, collections
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
G = os.path.join(ROOT, "01-Finalized_Modules_"); C = os.path.join(ROOT, "01-Claude_Modules_")
out = []
tot = 0
for t in sorted(os.listdir(G)):
    for code in sorted(os.listdir(os.path.join(G, t))):
        gd = os.path.join(G, t, code); cd = os.path.join(C, t, code)
        if not os.path.isdir(cd): continue
        pat = re.compile(r"^" + re.escape(code) + r"_(\d+)_(\d+)\.html$")
        gp = sorted(f for f in os.listdir(gd) if pat.match(f))
        cp = sorted(f for f in os.listdir(cd) if pat.match(f))
        if not gp or len(cp) >= len(gp): continue
        miss = [f for f in gp if f not in cp]
        extra = [f for f in cp if f not in gp]
        try:
            run = json.load(open(os.path.join(cd, "_run.json"), encoding="utf-8"))
        except Exception:
            run = {}
        notes = [n.get("text", "") for n in run.get("notes", []) if n.get("stage") in ("PageSplitter", "ModuleResolver", "DocxExtractor")]
        tot += len(miss)
        out.append((len(miss), t, code, len(gp), len(cp), miss, extra, notes))
out.sort(key=lambda r: -r[0])
print("modules", len(out), "missing gold pages", tot)
for m, t, code, g, c, miss, extra, notes in out:
    print(f"\n## {t} {code} gold={g} claude={c} missing={m}")
    print("   missing:", " ".join(x.replace(code + "_", "") for x in miss))
    if extra: print("   claude-only:", " ".join(x.replace(code + "_", "") for x in extra))
    for n in notes[:4]: print("   note:", n[:260])
