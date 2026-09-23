#!/usr/bin/env python3
"""ROUND 454 — refresh reference/tests/gate_baseline.json IN PLACE (line edits, the r453 pattern): build / round, the skeleton
mean / RAW (the only gate that moved), and the r454 notes. A .pre-r454.bak is kept. Run under WSL from anywhere."""
import io, os, json, shutil
P = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests", "gate_baseline.json"))
shutil.copyfile(P, P + ".pre-r454.bak")
L = io.open(P, encoding="utf-8").read().split("\n")
def setv(key, old, new):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            assert l.strip().rstrip(",") == f'"{key}": {old}', (key, l)
            L[i] = l.replace(f'"{key}": {old}', f'"{key}": {new}')
            return i
    raise SystemExit(f"not found {key}")
def insert_before(key, line):
    for i, l in enumerate(L):
        if l.strip().startswith(f'"{key}": '):
            L.insert(i, line); return
    raise SystemExit(f"anchor not found {key}")
setv("build", '"260620.24"', '"260620.25"'); setv("round", "453", "454")
insert_before("_note_r453", '    "_note_r454": "Round 454 (session 41 Round 2, 2026-09-24; the r453 follow-up — the TRR lesson pages) — THE RED-WRAPPED [Activity: Embedded] MARKER: BilingualBuilder.activityMarkerRe was anchored at the cell start, the MTK writer types the marker red (\'🔴[RED TEXT] [Activity: Embedded] Word select [/RED TEXT]🔴\'), so the KB 07B bilingual activity gather never fired and the instructions + data tables shipped as top-level bilingual-unbuilt dumps. Now red-tolerant; the box takes the KB 07D row > col-md-8 wrapper and the KB 07B decimal number; the marker row ships as the writer\'s cv2-note. ACTMARKRED_OFF. SCOPED ship #2 since the r452 FULL (20 Bilingual + 12 spot-check): 15 pages / 4 modules (TRR102 / 103 / 106 / 116); SCAFFOLD 54.7079 -> 54.7680 (+0.0600pp; 14 up / 1 down — TRR102_1.0 -2.3 NAMED, its gold keeps the writer\'s letter ids 1A…1E where KB 07B prefers decimal); every other gate EXACT; scoped_ship PASS.",')
setv("mean_scaffold_pct", "54.71", "54.77"); setv("raw_mean_pct", "38.7", "38.73")
insert_before("_note_r453_state", '    "_note_r454_state": "r454 (the red-wrapped [Activity: Embedded] marker): SCAFFOLD 54.7079 -> 54.7680 @ 2487 (+0.0600pp), RAW 38.676 -> 38.726, median 55.78; movers 15 (14 up / 1 down), pp-sum +149.2, 0 outside the affected set; >=50 1549 / >=75 265 / >=90 23 unchanged. outputs/_r454_sk_final.json, _r454_skdelta.log.",')
out = "\n".join(L); json.loads(out)
tmp = P + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, P)
print("gate_baseline.json refreshed to r454;", os.path.getsize(P), "bytes")
