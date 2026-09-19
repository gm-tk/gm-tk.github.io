#!/usr/bin/env python3
"""Session 28 / Task 1 — find fresh cascade-selftest pins on the rebuilt registry (the r218 / r253 stale-pin
class): (a) a case that DECIDES at L4 subject_template_consensus, (b) a case whose cascade defers past an
unsolid / tie level and then decides (SOLIDIFY-DEFER), plus a check that every other pinned case still holds.
Run from reference/tests under WSL:  python3 ../../outputs/_s28_t1_repin.py"""
import os, sys, json
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import granular_consensus as gc

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "pageforge-site", "converter-v2", "data")
msi = json.load(open(os.path.join(DATA, "Module_Structure_Index.json"), encoding="utf-8"))
codes = sorted(msi["modules"].keys())
KEYS = ["header|@h1", "header|h4", "header|@h2", "menu|@h5", "menu|@h4", "menu|@li", "body|@p", "body|@h3", "body|@li",
        "body|activity", "body|@h4", "body|@table", "body|@img", "body|tab n", "footer|@li", "acks|@p", "body|@h2", "menu|@p"]

print("== pinned cases on the rebuilt registry")
for code, key, lv, auth in gc._SELFTEST_CASES:
    r = gc.resolve(code, key)
    print(f"  {code:8} {key:14} -> L{r.get('level')} {r.get('authority')} esc={r.get('escalate')}  {'OK' if (not r.get('escalate') and r.get('level')==lv and r.get('authority')==auth) else 'STALE'}")
for code, key in (("ENFUN03", "body|@p"), ("AGH1001", "header|alert")):
    r = gc.resolve(code, key)
    print(f"  {code:8} {key:14} -> L{r.get('level')} {r.get('authority')} esc={r.get('escalate')} tried={r.get('tried')}")

l4, defer = [], []
for code in codes:
    for key in KEYS:
        try:
            r = gc.resolve(code, key)
        except Exception:
            continue
        if r.get("escalate"):
            continue
        if r.get("level") == 4 and r.get("authority") == "subject_template_consensus":
            l4.append((r.get("n_modules") or 0, r.get("majority_share") or 0, code, key, r.get("reference_sig")))
        if any(t.endswith(":unsolid") or t.endswith(":tie") for t in r.get("tried", [])):
            defer.append((r.get("level"), r.get("n_modules") or 0, code, key, r.get("tried")))
l4.sort(reverse=True); defer.sort(key=lambda t: (-t[1], t[0]))
print(f"\n== L4 subject_template_consensus deciders: {len(l4)} (top 12 by n_modules)")
for n, sh, code, key, sig in l4[:12]:
    print(f"  {code:8} {key:14} n={n} share={sh} sig={sig}")
print(f"\n== SOLIDIFY-DEFER cases (unsolid/tie then decided): {len(defer)} (top 12)")
for lv, n, code, key, tried in defer[:12]:
    print(f"  {code:8} {key:14} -> L{lv} n={n} tried={tried}")
