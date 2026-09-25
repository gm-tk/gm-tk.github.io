#!/usr/bin/env python3
"""Session 50 Round 8 record (WSL): r516 (the parked round-135 audioImage build, re-tested) DECLINED on measurement + the PICK pass.
Clears the r516 in-flight marker (archived verbatim), adds a Declined-classes entry, a follow-up line and the Round-log line."""
import io, os, subprocess, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
T = subprocess.run(["date", "+%H:%M"], capture_output=True, text=True).stdout.strip()
s = io.open(S, encoding="utf-8", newline="").read()
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s50-r8.bak"))
L = s.split("\n")
fl = [i for i, l in enumerate(L) if l.startswith("- **ROUND 516 IN FLIGHT — NOT PROVEN**")]
assert len(fl) == 1, fl
marker = L[fl[0]]; del L[fl[0]]
dc = [i for i, l in enumerate(L) if l.startswith("## Declined classes")]; assert len(dc) == 1
L.insert(dc[0] + 1, (
    f"- **Session 50 Round 8 (26 Sept ≈03:22 → {T}) — a PICK pass, then r516 (a parked registry row re-tested) DECLINED on measurement.** "
    "(1) **r516 — the round-135 bilingual `audioImage` build** (`dual_language.audio_image`, parked `enabled: false` since round 135 — "
    "'the build is CORRECT … byte-for-byte' but the grid was emitted as a bare top-level row while the gold nests it): the section "
    "nesting that has shipped since (r135 v2, r454 / r480 KB 07B) does NOT carry it — ON touches only PMT101 / TRR102 and scores "
    "skeleton −0.00, ≥50 −1, **compare_structure exact −57** (TRR102_1_0 39.4 → 35.7, PMT101_2_0 23.5 → 18.3; PMT101_3_0 +18.8). Flag "
    "back to false, the two modules regenerated → `_content_manifest.py diff` 0 pages, no ledger record (no scoped_ship run). The "
    "round-135 prerequisite (the prose + widget split inside the bilingual section) still stands. (2) The recognition census's remaining "
    "items: `[RHS]` (21 WJFUN modules — all but 3–4 notes already placed by the D15-18 side column), `[Check in]` (a placed block), "
    "`[tags]` (Writers-Template boilerplate, already omitted), `[Automated celebration]` 9 / `[engage]` 11 (below the floor); the "
    "flip-card face labels leaking into card text: 17 cards (SSOG103 `(front)` / `(back)`, TWHA906 `Facing:` / `Reverse:`) — under the "
    "floor."))
rl = [i for i, l in enumerate(L) if l.startswith("## Round log")]; assert len(rl) == 1
L.insert(rl[0] + 1, (f"- s50-r8 (engine r516, 26 Sept ≈03:22 → {T}) · a PICK pass (the census's remaining items, the flip-card face "
    "labels) then the REGISTRY-ROW lane: the parked round-135 bilingual audioImage build re-tested · DECLINED on measurement (cs exact "
    "−57 on PMT101 / TRR102 — the nesting wall stands), flag restored, corpus 0 pages differ · plateau 0 of 3 (neither)."))
io.open(A, "a", encoding="utf-8", newline="\n").write("\n## Session 50 — r516 PICK (the in-flight marker, verbatim) — DECLINED\n\n" + marker + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); os.replace(tmp, S)
print("LOOP_STATE", len(s.encode()), "->", os.path.getsize(S))
