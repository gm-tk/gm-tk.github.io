#!/usr/bin/env python3
"""r428 — correct the ship ledger: scoped_ship.sh recorded a scoped ship on EVERY run (three runs for r428 while the
decomposition was repaired; two for r425 on 21 Sept), over-counting the cadence toward the full-regeneration backstop.
One ship per round: keep the LAST r428 entry, drop the two earlier duplicates and the r425 duplicate, and recount
scoped_since from the history after the last full ship. (_ship_ledger.py record-scoped is now idempotent per round.)
Run under WSL: python3 _s34_r428_ledger_fix.py
"""
import json, io, os
p = os.path.dirname(os.path.abspath(__file__)) + "/_ship_ledger.json"
d = json.load(open(p, encoding="utf-8"))
hist = d.get("history", [])
before = len(hist)
dedup = []
for h in hist:
    if dedup and dedup[-1].get("kind") == "scoped" and h.get("kind") == "scoped" and str(dedup[-1].get("round")) == str(h.get("round")):
        dedup[-1] = h          # keep the latest time of the same round
    else:
        dedup.append(h)
d["history"] = dedup
lf = d.get("last_full")
since = 0
for h in dedup:
    if h.get("kind") == "full": since = 0
    elif h.get("kind") == "scoped" and (not lf or h.get("utc", "") > lf.get("utc", "")): since += 1
d["scoped_since"] = since
io.open(p, "w", encoding="utf-8", newline="\n").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
print(f"history {before} -> {len(dedup)} entries; scoped_since -> {since}; last full: {lf}")
