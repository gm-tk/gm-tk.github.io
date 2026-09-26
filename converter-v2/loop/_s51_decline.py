#!/usr/bin/env python3
"""_s51_decline.py — record a DECLINED round: clears ROUND N's in-flight marker (the 'Before rN: no round in flight' line becomes
the no-round line again, with an optional ride-along note spliced before 'Checked at'), archives the marker verbatim, and inserts
the Declined entry and the Round-log line from files. Asserts every anchor; never shrinks below the pre-marker size. WSL:
python3 _s51_decline.py N DECLINED_FILE ROUNDLOG_FILE [RIDE_NOTE_FILE]"""
import io, os, sys, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
N, dfile, rfile = sys.argv[1], sys.argv[2], sys.argv[3]
ride = io.open(sys.argv[4], encoding="utf-8").read().strip() if len(sys.argv) > 4 else ""
src = io.open(S, encoding="utf-8", newline="").read(); L = src.split("\n")
mk = [i for i, l in enumerate(L) if l.startswith(f"- **ROUND {N} IN FLIGHT — NOT PROVEN")]; assert len(mk) == 1, mk
bf = [i for i, l in enumerate(L) if l.startswith(f"- **Before r{N}: no round in flight**")]; assert len(bf) == 1, bf
marker = L[mk[0]]
L[bf[0]] = L[bf[0]].replace(f"- **Before r{N}: no round in flight**", "- **No round in flight**", 1)
if ride:
    assert "Checked at r" in L[bf[0]]
    L[bf[0]] = L[bf[0]].replace("Checked at r", ride + " Checked at r", 1)
del L[mk[0]]
dc = [i for i, l in enumerate(L) if l.startswith("## Declined classes")]; assert len(dc) == 1
L[dc[0] + 1:dc[0] + 1] = io.open(dfile, encoding="utf-8").read().rstrip("\n").split("\n")
rl = [i for i, l in enumerate(L) if l.startswith("## Round log")]; assert len(rl) == 1
L[rl[0] + 1:rl[0] + 1] = io.open(rfile, encoding="utf-8").read().rstrip("\n").split("\n")
out = "\n".join(L); assert len(out) > len(src) - len(marker)
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", f"LOOP_STATE.md.pre-r{N}-decline.bak"))
io.open(A, "a", encoding="utf-8", newline="\n").write(f"\n## Session 51 — r{N} PICK (the in-flight marker, verbatim) — DECLINED\n\n" + marker + "\n")
io.open(S + ".tmp", "w", encoding="utf-8", newline="").write(out); os.replace(S + ".tmp", S)
print("LOOP_STATE", len(src.encode()), "->", os.path.getsize(S))
