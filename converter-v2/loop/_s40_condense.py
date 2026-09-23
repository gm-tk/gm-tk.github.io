#!/usr/bin/env python3
"""Session 40 §5d condense #1 — LOOP_STATE.md 106 KB > the 100 KB target. Moves, VERBATIM, to LOOP_STATE_ARCHIVE.md
(append-only) and leaves a pointer line in place: (1) the Position 'Before it r446 …' gate-row tail; (2) the session-39
start note; (3) the s34-r5 / s35 / s36 Round-log lines; (4) the Standing-facts AppVersion history older than 260620.18.
Nothing is deleted. Writes LF, UTF-8. Run under WSL from anywhere."""
import io, os, re
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
src = io.open(P, encoding="utf-8").read()
lines = src.split("\n")
moved = []
def take(pred, title, pointer):
    idx = [i for i, l in enumerate(lines) if pred(l)]
    if not idx: print("NOT FOUND:", title); return
    block = [lines[i] for i in idx]
    moved.append((title, block))
    lines[idx[0]] = pointer
    for i in reversed(idx[1:]): del lines[i]
    print(f"moved {len(block)} line(s), {sum(len(b) for b in block)} chars: {title}")
take(lambda l: l.startswith("- Before it **r446** (build 260620.17"),
     "Position — LAST SHIPPED tail r446 / r445 / r444 / r443 (verbatim, s40 §5d condense #1)",
     "- Before it: **r446** (260620.17, the OS / TEDC bubble placeholder, D13-9 part 2, gate-neutral), **r445** (260620.16, the comparison table, D13-2, −0.0003pp named), **r444** (260620.15, consecutive activity numbers, D13-7, THE FULL BACKSTOP — LAST FULL = r444, −0.0441pp named), **r443** (260620.14, the XOTP flagged gaps, +0.0086pp) and older — the verbatim gate rows → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r446 / r445 / r444 / r443 (verbatim, s40 §5d condense #1)' and the earlier tail blocks named there.")
take(lambda l: l.startswith("**Session 39 started:**"),
     "Session start note 39 (verbatim, s40 §5d condense #1)",
     "**Session 39 started:** 23 Sept ≈14:37 (Opus 5.5) — health check FAILED on r439's five engine checksums only (a Cowork session's loose round), the crashed-round check fired, r439 finished as Round 1; LOOP_STATE condensed 114.8 → 90 KB first. Verbatim → LOOP_STATE_ARCHIVE.md 'Session start note 39 (verbatim, s40 §5d condense #1)'.")
rl = re.compile(r"^- s(34-r5|35-r[0-9]+|36-r[0-9]+) \(")
take(lambda l: bool(rl.match(l)),
     "Round-log lines s34-r5 / s35 / s36 (verbatim, s40 §5d condense #1)",
     "- s34-r5, s35-r1…r3, s36-r1…r7 round-log lines (13 lines: engine r430–r436 shipped, the s34-r5 / s36-r5 / s36-r6 / s36-r7 PICK passes) → LOOP_STATE_ARCHIVE.md 'Round-log lines s34-r5 / s35 / s36 (verbatim, s40 §5d condense #1)'.")
# (4) Standing facts: keep the last three builds, move the rest
for i, l in enumerate(lines):
    if l.startswith("- Standing facts: AppVersion 260620.20"):
        m = re.search(r"; before it 260620\.17 ", l)
        if m:
            head, tail = l[:m.start()], l[m.start():]
            moved.append(("Position — Standing facts AppVersion history 260620.17 → 260620.09 (verbatim, s40 §5d condense #1)", ["- (continued) " + tail.lstrip("; ")]))
            lines[i] = head + "; 260620.17 and every older build → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.17 → 260620.09 (verbatim, s40 §5d condense #1)' (and the earlier history block named there); every toggle is listed in OPERATING_GUIDE.md §11; the engine + gate checksum manifests (`_MIGRATION/CHECKSUMS__engine.txt` / `CHECKSUMS__gates.txt`) are refreshed at every ship (a `.pre-rNNN.bak` copy kept)."
            print(f"moved the AppVersion tail, {len(tail)} chars")
        break
out = "\n".join(lines)
arch = io.open(A, encoding="utf-8").read()
add = "".join(f"\n\n## {t}\n" + "\n".join(b) for t, b in moved) + "\n"
io.open(A, "w", encoding="utf-8", newline="").write(arch.rstrip("\n") + add)
io.open(P, "w", encoding="utf-8", newline="").write(out)
print(f"LOOP_STATE.md {len(src.encode())} -> {len(out.encode())} bytes; archive +{len(add.encode())} bytes")
