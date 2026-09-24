#!/usr/bin/env python3
"""Session 43 §5d condense #1 (at the session start, 97.9 KB — the start note would cross the 100 KB target): MOVE verbatim to
LOOP_STATE_ARCHIVE.md the session-42 start note and the three longest session-42 Declined-classes entries (Rounds 5 / 6 / 7);
pointer lines left. .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s43-condense1.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8")); arch = []
k = [i for i, l in enumerate(L) if l.startswith("**Session 42 started:**")]
assert len(k) == 1, k
arch.append(("Session start note 42 (verbatim, s43 §5d condense #1)", [L[k[0]]]))
L[k[0]] = ("**Session 42 started:** 24 Sept 14:14 (Opus 5.5) — clean start at 7bcb252, 12 rounds (≈ 2 h 30 min), three §5d condenses, two "
           "clock notes (the ≈ times on s42-r5 → r11 ran 20–80 min ahead — read the commit times); r465 / r466 / r467 / r470 shipped, the §1g "
           "placement census built. Verbatim → LOOP_STATE_ARCHIVE.md 'Session start note 42 (verbatim, s43 §5d condense #1)'.")
d = [i for i, l in enumerate(L) if l.startswith("- **Session 42 Round 5 ") or l.startswith("- **Session 42 Round 6 ")
     or l.startswith("- **Session 42 Round 7 ")]
assert len(d) == 3, d
arch.append(("Declined classes — session 42 Rounds 5 / 6 / 7 (verbatim, s43 §5d condense #1)", [L[i] for i in d]))
for i in sorted(d, reverse=True): del L[i]
L.insert(min(d), "- **Session 42 declined classes, Rounds 5 / 6 / 7 (engine r468 the lesson menu's `[H2]` WALT lead, 3 pages — patch "
         "`_r468_declined.patch`; the census P4 / P5 / P6 / P7 split by the writer's tag and DECLINED as class C or under the floor; the "
         "census combined-WT fix; engine r469 / r469b the alert-title `</p>` crossing (7 pages) and the button's media-URL absorb (10 pages) — "
         "ride-along patches; the HIS1 lesson-menu column declined; the TRR1 box boundary recorded)** → LOOP_STATE_ARCHIVE.md 'Declined "
         "classes — session 42 Rounds 5 / 6 / 7 (verbatim, s43 §5d condense #1)'; every verdict stands.")
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch: f.write("\n## " + title + "\n\n" + "\n".join(lines).rstrip() + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
