#!/usr/bin/env python3
"""_s51_r1_overcap.py — session 51 Round 1 PICK: the body_compare over-capture pages (the gate rule: >= 0.40 of the page in
one widget, >= 400 chars, >= 3 free blocks lost), grouped by the biggest box's banner type and the module family. WSL, from
reference/tests/."""
import json, re, collections
d = json.load(open("body_compare.json"))
rows = [r for r in d if r["over_capture"] >= 0.40 and r["biggest_widget_chars"] >= 400 and r["lost_blocks"] >= 3]
print("over-capture pages:", len(rows), "modules:", len({r["module"] for r in rows}))
ty = lambda b: (re.search(r"#\d+:\s*([A-Za-z +]+?)\s*(?:—|-|$)", b or "") or [None, (b or "?")[:30]])[1].strip()
by = collections.Counter(ty(r["biggest_banner"]) for r in rows)
fam = collections.Counter(re.sub(r"\d.*", "", r["module"]) for r in rows)
pt = collections.Counter("overview" if re.search(r"_0_0\.html$", r["page"]) else "lesson" for r in rows)
print("by type:", by.most_common(20)); print("by family:", fam.most_common(30)); print("by page type:", pt)
for r in sorted(rows, key=lambda r: -r["lost_blocks"]):
    print(f'{r["page"]:36s} oc={r["over_capture"]:.2f} chars={r["biggest_widget_chars"]:6d} lost={r["lost_blocks"]:3d} gold_free={r["human_free_blocks"]:3d} cl_free={r["claude_free_blocks"]:3d} multi={r["multi_type"]} | {(r["biggest_banner"] or "")[:90]}')
