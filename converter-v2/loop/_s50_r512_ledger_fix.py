"""Session 50 Round 3 — r512 was DECLINED on measurement after scoped_ship.sh (a FAIL run) recorded it in the ship ledger.
Remove that record and restore the scoped counter (the r428 precedent: _s34_r428_ledger_fix.py). Run under WSL from outputs/."""
import json, shutil
P = "_ship_ledger.json"
shutil.copyfile(P, "_ship_ledger.pre-r512fix.json")
d = json.load(open(P))
h = d.get("history", [])
assert h and str(h[-1].get("round")) == "512" and h[-1].get("kind") == "scoped", h[-1:]
h.pop()
d["scoped_since"] = int(d["scoped_since"]) - 1
json.dump(d, open(P, "w"), indent=1)
print("ledger fixed: scoped_since", d["scoped_since"], "last", h[-1])
