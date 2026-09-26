#!/usr/bin/env python3
"""_s53_condense2.py — session 53 §5d condense #2: moves VERBATIM to LOOP_STATE_ARCHIVE.md the 'Decisions from Chris' blocks of the
loop-run sessions 40, 42–46 and 49–52 whose content is 'the standing kickoff only / no new numbered decision' (each block = its '## '
line + following lines up to the next '## ' line), and the (s51-r13) / (s51-r6) follow-up entries; one pointer line replaces them.
Sessions 41 (D14), 47 (review) and 48 (D15) — the ones carrying decisions — stay hot. WSL."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s53-condense2.bak"))
SESS = ("40", "42", "43", "44", "45", "46", "49", "50", "51", "52")
heads = [i for i, l in enumerate(L) if re.match(r"## Decisions from Chris \(session (\d+) — 20", l) and re.match(r"## Decisions from Chris \(session (\d+)", l).group(1) in SESS]
blocks = []
for h in heads:
    e = h + 1
    while e < len(L) and not L[e].startswith("## "): e += 1
    blocks.append((h, e))
moved = []
for h, e in sorted(blocks, reverse=True):
    moved.insert(0, "\n".join(L[h:e]).rstrip("\n"))
    del L[h:e]
first = min(h for h, e in blocks)
L.insert(first, "## Decisions from Chris (loop-run sessions 40 / 42–46 / 49–52 — the standing `/loop-start` kickoff each, a `/loop-stop` at the end of 41 / 43 / 49 / 51; NO new numbered decision in any) → LOOP_STATE_ARCHIVE.md 'Decisions from Chris — loop-run sessions 40 / 42–46 / 49–52 (verbatim, s53 §5d condense #2)'.\n")
fu = []
for pfx in ("- **(s51-r13) the registry rows' lane", "- **(s51-r6) swallowed-block"):
    idx = [i for i, l in enumerate(L) if l.startswith(pfx)]; assert len(idx) == 1, pfx
    fu.append(L[idx[0]]); del L[idx[0]]
ins = [i for i, l in enumerate(L) if l.startswith("- The D15 queue bullet")]; assert len(ins) == 1
L.insert(ins[0], "- The (s51-r13) registry-rows / cs-MISSING and (s51-r6) swallowed-block / empty-box / co-tag follow-up entries → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — s51-r13 / s51-r6 (verbatim, s53 §5d condense #2)'. None is struck.")
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
io.open(A, "a", encoding="utf-8", newline="\n").write(
    "\n## Decisions from Chris — loop-run sessions 40 / 42–46 / 49–52 (verbatim, s53 §5d condense #2)\n\n" + "\n\n".join(moved) + "\n"
    + "\n## Follow-up candidates — s51-r13 / s51-r6 (verbatim, s53 §5d condense #2)\n\n" + "\n".join(fu) + "\n")
print("moved", len(blocks), "decision blocks; LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S))
