#!/usr/bin/env python3
"""_s53_decline.py — session 53: record a DECLINED / PARKED round in LOOP_STATE.md (WSL). The in-flight marker line moves verbatim to the
archive with a verdict; the 'Before rN: no round in flight' line becomes the 'No round in flight' line again (a new timestamp, the
ride-along list gaining the parked patch); one Round-log line and one Declined-classes line are added.
argv: N VERDICT_ARCHIVE_LINE ROUNDLOG_LINE DECLINED_LINE PATCH_NOTE(or '-')"""
import io, os, re, sys, subprocess, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
N, verdict, roundlog, declined, patch = sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5]
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", f"LOOP_STATE.md.pre-r{N}-decline.bak"))
fl = [i for i, l in enumerate(L) if l.startswith(f"- **ROUND {N} IN FLIGHT — NOT PROVEN**")]; assert len(fl) == 1, fl
bl = [i for i, l in enumerate(L) if l.startswith(f"- **Before r{N}: no round in flight**")]; assert len(bl) == 1, bl
marker = L[fl[0]]
nr = L[bl[0]].replace(f"- **Before r{N}: no round in flight** (", f"- **No round in flight** (27 Sept 2026 {T}, session 53 — r{N} DECLINED / PARKED, backed out, corpus unchanged; before it: ", 1)
if patch != "-":
    nr = nr.replace(". Checked at r", f" / {patch}. Checked at r", 1)
L[bl[0]] = nr
del L[fl[0]]
rl = [i for i, l in enumerate(L) if l == "## Round log"]; assert len(rl) == 1
L.insert(rl[0] + 1, roundlog.replace("{T}", T))
dc = [i for i, l in enumerate(L) if l == "## Declined classes"]; assert len(dc) == 1
L.insert(dc[0] + 1, declined)
io.open(A, "a", encoding="utf-8", newline="\n").write(f"\n## Session 53 — r{N} PICK (the in-flight marker, verbatim) — {verdict}\n\n{marker}\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
print("LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S))
