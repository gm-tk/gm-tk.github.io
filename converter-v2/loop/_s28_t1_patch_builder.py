#!/usr/bin/env python3
"""Session 28 / Task 1 — patch build_granular_registry.build_subject_map() so the prefixes the
All_Template_Reports folders do not file are filled from data/Subject_Prefix_Map.json (gaps only;
a report-derived label is never overridden). LF-preserving, idempotent."""
import os, sys
P = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests", "build_granular_registry.py")
src = open(P, encoding="utf-8", newline="").read()
if "Subject_Prefix_Map.json" in src:
    print("already patched"); sys.exit(0)
old = '''    return {p: c.most_common(1)[0][0] for p, c in pref.items()}
'''
new = '''    out = {p: c.most_common(1)[0][0] for p, c in pref.items()}
    # SESSION 28 / TASK 1 (2026-09-20): the September-intake prefixes have no report folder, so
    # data/Subject_Prefix_Map.json supplies the label for a prefix the reports do NOT file —
    # gaps only, never an override (the report-derived label stays the standing source).
    supp = os.path.join(BASE, "..", "..", "data", "Subject_Prefix_Map.json")
    if os.path.isfile(supp):
        extra = json.load(open(supp, encoding="utf-8")).get("prefixes", {})
        for p, label in extra.items():
            if p not in out and label:
                out[p] = label
    return out
'''
assert src.count(old) == 1, "anchor not found exactly once"
src = src.replace(old, new)
open(P, "w", encoding="utf-8", newline="").write(src)
print("patched", P)
