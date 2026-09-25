#!/usr/bin/env python3
"""Session 46 §5d condense #2 — archive verbatim: the plateau-window line's history older than r490, the AppVersion history older than
260620.53, and the oldest Follow-up entries (s42-r11, D14-S1 residue s41, s44-r2, r453, r451, r449); leave pointers. WSL."""
import io, os, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
rd = lambda p: io.open(p, encoding="utf-8", newline="").read()
ss = rd(S); L = ss.split("\n"); shutil.copyfile(S, S + ".pre-s46-condense2.bak")
def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx); return idx[0]
out = []
# (1) the plateau line: keep up to (and including) the r490 reading, archive the rest
k = find("- Plateau window (§4): **0 of 3**")
line = L[k]; cut = line.find("; r488 a widget-build round")
assert cut > 0
out.append("\n## Position — plateau readings r488 and older (verbatim, s46 §5d condense #2)\n\n" + line[cut + 2:] + "\n")
L[k] = line[:cut] + "; r488 and every older reading → LOOP_STATE_ARCHIVE.md 'Position — plateau readings r488 and older (verbatim, s46 §5d condense #2)'. Read every delta on the post-intake population (§1e)."
# (2) the AppVersion history: keep through 260620.53, archive the rest
k = find("- Standing facts: AppVersion **260620.58**")
line = L[k]; cut = line.find("; before it 260620.52")
assert cut > 0
end = line.find("; every toggle is listed", cut)
assert end > 0
out.append("\n## Position — Standing facts AppVersion history 260620.52 and older (verbatim, s46 §5d condense #2)\n\n" + line[cut + 2:end] + "\n")
L[k] = line[:cut] + "; 260620.52 and older → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.52 and older (verbatim, s46 §5d condense #2)'" + line[end:]
# (3) the oldest follow-up entries
pre = ("- **(s42-r11) THE ORDER CENSUS", "- **(D14-S1 placement residue, s41)", "- **(s44-r2) THE TRR1 LESSON-PAGE LANE", "- **(r453) The TRR family's LESSON pages",
       "- **(r451) TRR301_3_0's unclassified bundle", "- **(r449) typing — the next shapes")
idx = [i for i, l in enumerate(L) if l.startswith(pre)]
assert len(idx) == len(pre), idx
moved = [L[i] for i in idx]
first = idx[0]
for i in reversed(idx): del L[i]
L.insert(first, "- The s41–s44 follow-up entries (the s42-r11 ORDER census; the D14-S1 s41 placement residue — WJFUN tiles, the empty LI panes, the "
         "c67 Overview columns, the BLL tab split, TRR `media_in_place`; the s44-r2 TRR1 lesson-page lane (b)–(e); r453 the TRR lesson pages / "
         "TRR107's empty gold shells / TRR112–113 panes; r451 TRR301_3_0's page-capturing bundle and the empty-box row; r449 typing's next "
         "shapes) → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — s42-r11 / s41 / s44-r2 / r453 / r451 / r449 (verbatim, s46 §5d condense #2)'.")
out.append("\n## Follow-up candidates — s42-r11 / s41 / s44-r2 / r453 / r451 / r449 (verbatim, s46 §5d condense #2)\n\n" + "\n".join(moved) + "\n")
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(out))
io.open(S, "w", encoding="utf-8", newline="").write("\n".join(L))
print("LOOP_STATE", len(ss.encode("utf-8")), "->", os.path.getsize(S))
