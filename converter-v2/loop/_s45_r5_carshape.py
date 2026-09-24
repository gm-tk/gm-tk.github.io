#!/usr/bin/env python3
"""Session 45 Round 5 — from _s45_r5_cardump.log: every carousel bundle, built or declined, with a story reference among its members
([embed … story|book …]); the member sequence as a compact token string (tag names / black), per shape. WSL, from outputs/."""
import re, json, collections
blocks = []; cur = None
for ln in open("_s45_r5_cardump.log", encoding="utf-8", errors="replace"):
    if ln.startswith("=== "):
        cur = {"head": ln.strip(), "items": [], "out": None}; blocks.append(cur)
    elif cur is not None and ln.startswith("  ITEM "):
        cur["items"].append(ln[7:].rstrip())
    elif cur is not None and ln.startswith("  OUT "):
        cur["out"] = ln[6:].strip()
STORY = re.compile(r"\[[^\]]{0,25}embed[^\]]{0,40}\b(?:book|story)\b", re.I)
def tok(item):
    typ = item.split(" ", 1)[0]
    try: j = json.loads(item.split(" ", 1)[1])
    except Exception: j = {}
    if typ == "tag":
        p = (j.get("parse") or {}).get("primary") or {}
        t = p.get("tag") or ("instr" if (j.get("parse") or {}).get("class") == "instruction" else "noise")
        return "embed:story" if STORY.search(j.get("text") or "") else t
    return typ
shapes = collections.Counter(); ex = collections.defaultdict(list); built = collections.Counter(); mods = collections.defaultdict(set)
for b in blocks:
    raw = " ".join(b["items"])
    if not STORY.search(raw): continue
    toks = [tok(i) for i in b["items"]]
    isb = b["out"] not in (None, "null")
    key = " ".join(toks)[:160]
    shapes[(isb, key)] += 1; mods[(isb, key)].add(b["head"].split()[1])
    if len(ex[(isb, key)]) < 2: ex[(isb, key)].append(b["head"])
print("story-carrying carousel bundles:", sum(shapes.values()), "built", sum(n for (i, _), n in shapes.items() if i))
for (isb, k), n in shapes.most_common(40):
    print(f"{n:3d} {'BUILT ' if isb else 'BOX   '} {len(mods[(isb, k)]):2d}m  {k}   e.g. {ex[(isb, k)][0]}")
