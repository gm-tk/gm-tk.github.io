#!/usr/bin/env python3
"""_s54_condense1.py — session 54 §5d condense #1 (LOOP_STATE.md at 99.2 KB): moves VERBATIM to LOOP_STATE_ARCHIVE.md (1) the sixteen
s52-r1…r16 Round-log lines, (2) the (s52-r8) / (s52-r3) / (s52-r2) follow-up entries, (3) the plateau line's readings older than the
s54 ones (r539 and older), (4) the Standing-facts AppVersion history from 260620.93 down; one pointer line replaces each. WSL."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
S = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
s = io.open(S, encoding="utf-8", newline="").read(); L = s.split("\n")
shutil.copyfile(S, os.path.join(ROOT, "_Backups", "loop_state", "LOOP_STATE.md.pre-s54-condense1.bak"))
arch = []
# (1) the s52 round-log lines
idx = [i for i, l in enumerate(L) if re.match(r"- s52-r\d+ \(", l)]
assert len(idx) == 16, len(idx)
arch.append(("Round log s52-r1…r16 (verbatim, s54 §5d condense #1)", [L[i] for i in idx]))
first = idx[0]
for i in sorted(idx, reverse=True): del L[i]
L.insert(first, "- s52-r1…r16 round-log lines (16 lines, session 52: engine r528–r534 shipped (the untagged whakataukī, the summary heading's alert box, the whakataukī's other writer forms, the bracket fragment in a button label, the bare stock-photo URL, the bare video URL, the bare link line), the s52-r11 FULL backstop, nine PICK passes) → LOOP_STATE_ARCHIVE.md 'Round log s52-r1…r16 (verbatim, s54 §5d condense #1)'.")
# (2) the s52 follow-up entries
fu = []
for pfx in ("- **(s52-r8) the other bare-URL paragraphs", "- **(s52-r3) the whakataukī residue", "- **(s52-r2) the `div.alert` MISSING cue census"):
    j = [i for i, l in enumerate(L) if l.startswith(pfx)]; assert len(j) == 1, pfx
    fu.append(L[j[0]]); del L[j[0]]
ins = [i for i, l in enumerate(L) if l.startswith("- The (s51-r1) PICK-pass follow-up")]; assert len(ins) == 1
L.insert(ins[0], "- The (s52-r8) bare-URL residue, (s52-r3) whakataukī residue / alert lane and (s52-r2) `div.alert` MISSING cue-census follow-up entries → LOOP_STATE_ARCHIVE.md 'Follow-up candidates — s52-r8 / s52-r3 / s52-r2 (verbatim, s54 §5d condense #1)'. None is struck (r541 took the s52-r2 item (1), the `[Alert]` + heading).")
arch.append(("Follow-up candidates — s52-r8 / s52-r3 / s52-r2 (verbatim, s54 §5d condense #1)", fu))
# (3) the plateau line: keep the readings up to r541, archive the rest
pl = [i for i, l in enumerate(L) if l.startswith("- Plateau window (§4): **")]; assert len(pl) == 1
p = L[pl[0]]; cut = p.find("r539 +0.0038pp")
assert cut > 0
arch.append(("Position — plateau readings r539 → r526 (verbatim, s54 §5d condense #1)", [p[cut:]]))
L[pl[0]] = p[:cut] + "r539 and every older reading → LOOP_STATE_ARCHIVE.md 'Position — plateau readings r539 → r526 (verbatim, s54 §5d condense #1)'. Read every delta on the post-intake population (§1e)."
# (4) the Standing-facts AppVersion history from 260620.93 down
sf = [i for i, l in enumerate(L) if l.startswith("- Standing facts: AppVersion **")]; assert len(sf) == 1
f = L[sf[0]]; a = f.find("; before it 260620.93"); b = f.find("; every toggle is listed")
assert 0 < a < b
arch.append(("Position — Standing facts AppVersion history 260620.93 → 260620.87 (verbatim, s54 §5d condense #1)", [f[a:b]]))
L[sf[0]] = f[:a] + "; 260620.93 and older → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.93 → 260620.87 (verbatim, s54 §5d condense #1)'" + f[b:]
out = "\n".join(L); tmp = S + ".tmp"; io.open(tmp, "w", encoding="utf-8", newline="").write(out); assert os.path.getsize(tmp) > 50000; os.replace(tmp, S)
io.open(A, "a", encoding="utf-8", newline="\n").write("".join(f"\n## {h}\n\n" + "\n".join(x) + "\n" for h, x in arch))
print("LOOP_STATE", len(s.encode("utf-8")), "->", os.path.getsize(S))
