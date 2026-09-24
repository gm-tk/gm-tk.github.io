#!/usr/bin/env python3
"""Session 46 — compare_structure per module, NOW (disk) vs the fast-loop baseline (the last ship), for the modules given — without
writing the gate's own structural_comparison.json. WSL, from reference/tests: python3 ../../outputs/_s46_csdelta.py CODE …"""
import sys, os, json
sys.path.insert(0, os.getcwd())
import compare_structure as cs
base = {r["module"]: r for r in json.load(open("../../outputs/_fastloop_baseline/structural_comparison.json")) if "module" in r}
keys = ["matched", "exact_chain", "wrapper_set", "claude_extra_container", "claude_missing_container", "row_wrap_missing", "other_chain_diff"]
for m in sys.argv[1:]:
    new = cs.compare_module(m) or {}
    old = base.get(m, {})
    d = {k: (new.get(k, 0) - old.get(k, 0)) for k in keys}
    if any(d.values()):
        print(m, {k: v for k, v in d.items() if v})
        for ex in (new.get("examples") or [])[:0]: print("   ", ex)
print("done")
