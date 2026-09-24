#!/usr/bin/env python3
"""Session 42 §5d condense #2 (after r468, LOOP_STATE.md 97.7 KB): MOVE verbatim to LOOP_STATE_ARCHIVE.md (1) the Position rows r461 /
r460 / r459→r453 / r452 / r451 (one pointer line left), (2) the plateau line's readings older than r461 (kept: r467 → r461), (3) the
Standing-facts AppVersion history older than 260620.30, (4) the session-41 start note (a one-line pointer left). .bak kept. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(S, S + ".pre-s42-condense2.bak")
s = io.open(S, encoding="utf-8").read(); L = s.split("\n"); n0 = len(s.encode("utf-8")); arch = []
def one(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]; assert len(idx) == 1, (prefix, idx); return idx[0]
# (1) Position tail rows
b = [one(p) for p in ("- Before it: **r461**", "- Before it: **r460**", "- Before them: **r459", "- Before it: **r452**", "- Before it: **r451**")]
assert b == list(range(b[0], b[0] + 5)), b
arch.append(("Position — LAST SHIPPED tail r461 → r451 (verbatim, s42 §5d condense #2)", L[b[0]:b[-1] + 1]))
L[b[0]:b[-1] + 1] = ["- Before them: **r461 / r460 / r459 → r453 / r452 / r451** and older — the verbatim gate rows → LOOP_STATE_ARCHIVE.md "
                     "'Position — LAST SHIPPED tail r461 → r451 (verbatim, s42 §5d condense #2)' and the tail blocks named there."]
# (2) the plateau line: keep up to (and including) the r461 reading
k = one("- Plateau window (§4): **2 of 3**"); line = L[k]
cut = line.index("; r460 predicted a small skeleton move")
arch.append(("Position — plateau readings r460 and older (verbatim, s42 §5d condense #2)", [line[cut + 2:]]))
L[k] = line[:cut] + "; r460 and every older reading → LOOP_STATE_ARCHIVE.md 'Position — plateau readings r460 and older (verbatim, s42 §5d condense #2)'. Read every delta on the post-intake population (§1e)."
# (3) Standing facts: keep AppVersion history down to 260620.30
k = one("- Standing facts: AppVersion 260620.34"); line = L[k]
cut = line.index("; before it 260620.29")
tail = line[cut + 2:]
j = tail.index("; every toggle is listed in OPERATING_GUIDE.md §11")
arch.append(("Position — Standing facts AppVersion history 260620.29 → 260620.18 (verbatim, s42 §5d condense #2)", [tail[:j]]))
L[k] = line[:cut] + "; 260620.29 and older → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.29 → 260620.18 (verbatim, s42 §5d condense #2)'" + tail[j:]
# (4) the session-41 start note
k = one("**Session 41 started:**")
arch.append(("Session start note 41 (verbatim, s42 §5d condense #2)", [L[k]]))
L[k] = ("**Session 41 started:** 24 Sept 07:25 (Opus 5.5) — clean start, 12 rounds, four §5d condenses and one compaction; r453–r461 "
        "shipped, three declined, r464 withdrawn. Verbatim → LOOP_STATE_ARCHIVE.md 'Session start note 41 (verbatim, s42 §5d condense #2)'.")
k = one("**Session 42 started:**")
L[k] += " **§5d condense #2 at ≈15:58** (after r468, 97.7 KB): the r461 → r451 Position rows, the plateau readings r460 and older, the AppVersion history 260620.29 and older and the s41 start note moved verbatim (`outputs/_s42_condense2.py`)."
with io.open(A, "a", encoding="utf-8", newline="\n") as f:
    for title, lines in arch: f.write("\n## " + title + "\n\n" + "\n".join(lines).rstrip() + "\n")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="\n").write(out); os.replace(tmp, S)
print("LOOP_STATE.md", n0, "->", os.path.getsize(S))
