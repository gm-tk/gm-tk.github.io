#!/usr/bin/env python3
"""Session 46 Round 2 — the accordion declines at `if (!parts)` (the r278 member walk could not place a member), grouped by the guard
inside #accMemberParts that fired (the r286 recorder's trace, the entry before the deciding one), with the foreign tags seen. WSL, outputs/."""
import json, collections, re
R = json.load(open("_r286_declines.json"))
acc = [r for r in R if r["type"] == "accordion" and r["built"] in (False, "False")]
by = collections.defaultdict(list)
for r in acc:
    if "if (!parts)" not in (r.get("decideWhy") or ""): continue
    tr = r.get("trace") or []
    tw = r.get("traceWhy") or []
    tr = tr if isinstance(tr, list) else eval(tr)
    tw = tw if isinstance(tw, list) else eval(tw)
    # the last trace entry inside accMemberParts before the deciding guard
    inner = [(t, w) for t, w in zip(tr, tw) if t.startswith("accMemberParts") or t.startswith("accMediaTableParts")]
    key = inner[-1] if inner else ("?", "?")
    by[key].append(r)
seen = set()
for (t, w), v in sorted(by.items(), key=lambda x: -len(x[1])):
    uniq = {(r["code"], r["page"], r["index"]): r for r in v}
    mods = collections.Counter(r["code"] for r in uniq.values())
    fr = collections.Counter(x for r in uniq.values() for x in (eval(r["foreign"]) if isinstance(r["foreign"], str) else r["foreign"]))
    print(f"{len(uniq):4d} bundles {len(mods):3d} mod  {t:28s} {w[:90]}")
    print(f"        foreign: {fr.most_common(8)}")
    print(f"        e.g. {', '.join(f'{c} {p} #{i}' for (c, p, i) in list(uniq)[:8])}")
