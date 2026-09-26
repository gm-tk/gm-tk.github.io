#!/usr/bin/env python3
"""s52 §5d condense #1 — archive verbatim: the s51 start note, the AppVersion history 260620.79 and older, the plateau
readings r505 and older, the 'Before them' r523 → r467 list; add the s52 start note. Asserts every anchor. WSL."""
import io, os, sys, time
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"
S = os.path.join(R, "LOOP_STATE.md"); A = os.path.join(R, "LOOP_STATE_ARCHIVE.md")
t = io.open(S, encoding="utf-8", newline="").read()
n0 = len(t.encode("utf-8"))
L = t.split("\n")
now = time.strftime("%H:%M")
arch = []

def find(prefix):
    idx = [i for i, l in enumerate(L) if l.startswith(prefix)]
    assert len(idx) == 1, (prefix, idx)
    return idx[0]

# 1. the s51 start note
i = find("**Session 51 started:**")
arch.append("## Session start note 51 (verbatim, s52 §5d condense #1)\n\n" + L[i] + "\n")
L[i] = ("**Session start note 51** -> LOOP_STATE_ARCHIVE.md 'Session start note 51 (verbatim, s52 §5d condense #1)'. One line: 26 Sept "
        "09:36, clean start at c330fff, r522–r526 shipped + the s51-r12 FULL backstop, r528 built and toggled OFF at the `/loop-stop` "
        "(14:58). Every figure in it is superseded by the Position section below.")

# 2. the AppVersion history
i = find("- Standing facts: AppVersion **260620.86**")
cut = "; before it 260620.79 (r518"
k = L[i].find(cut); assert k > 0
tail_start = L[i].find("; 260620.52 and older"); assert tail_start > k
arch.append("## Position — Standing facts AppVersion history 260620.79 → 260620.53 (verbatim, s52 §5d condense #1)\n\n- …" + L[i][k:tail_start] + "\n")
L[i] = L[i][:k] + "; 260620.79 → 260620.53 → LOOP_STATE_ARCHIVE.md 'Position — Standing facts AppVersion history 260620.79 → 260620.53 (verbatim, s52 §5d condense #1)'" + L[i][tail_start:]

# 3. the plateau readings r505 and older
i = find("- Plateau window (§4):")
k = L[i].find("; r505 +0.0070pp"); assert k > 0
e = L[i].find("; r488 and every older reading"); assert e > k
arch.append("## Position — plateau readings r505 → r490 (verbatim, s52 §5d condense #1)\n\n- …" + L[i][k:e] + "\n")
L[i] = L[i][:k] + "; r505 → r490 → LOOP_STATE_ARCHIVE.md 'Position — plateau readings r505 → r490 (verbatim, s52 §5d condense #1)'" + L[i][e:]

# 4. the Before-them list
i = find("- Before them: **r523 → r467**")
arch.append("## Position — Before-them list r523 → r467 (verbatim, s52 §5d condense #1)\n\n" + L[i] + "\n")
L[i] = ("- Before them: **r523 → r467** and **r461 → r451** — the round-by-round list → LOOP_STATE_ARCHIVE.md 'Position — Before-them list "
        "r523 → r467 (verbatim, s52 §5d condense #1)'; each round's LAST SHIPPED block is verbatim there under 'Position — LAST SHIPPED rNNN'.")

# 5. the s52 start note, after the s51 pointer
i = find("**Session start note 51**")
note = ("**Session 52 started:** 26 Sept 15:01 NZST (Opus 5.5; the default budget, 16 rounds or 10 hours → by ≈01:00 27 Sept). "
        "Health check: tree DIRTY by design — `PageAssembler.js` + `Emit_Templates.json` = r528, toggled OFF, mtimes 14:53 / 14:56, "
        "named by the s51 `/loop-stop` (commits 93cd37e / 610fc26 at 14:59 / 15:00), so not a parallel session and not a crash; "
        "`verify_after_transfer.sh` FAIL on exactly those two engine checksums, census PASS 552 / 545 / 2673 / 2993 / 762; no git "
        "locks, no root `*.bak`; Amended line 1; intake checks (b) the 7 recorded no-source dirs only, (c) 0 docx newer than its "
        "`_run.json`, (d) both staging areas unchanged since the 19 Sept audit — no intake due; KB HEAD 910a9cb UNCHANGED; "
        "`DIFF_QUEUE.md` 14:24 on the r526 corpus (0 Claude pages newer) — current; AppVersion 260620.86 = the top changelog entry. "
        "LOOP_STATE " + f"{n0/1000:.1f}" + " → §5d condense #1. Order: Round 1 = finish or decline r528 (the Position line), then a PICK "
        "pass led by the s51-r13 `div.alert` MISSING cue census.")
L.insert(i + 1, note)

out = "\n".join(L)
assert len(out) > 60000
arch_txt = "\n" + "\n".join(arch)
a0 = os.path.getsize(A)
with io.open(A, "a", encoding="utf-8", newline="") as f: f.write(arch_txt)
assert os.path.getsize(A) > a0
tmp = S + ".tmp"
with io.open(tmp, "w", encoding="utf-8", newline="") as f: f.write(out)
assert os.path.getsize(tmp) > 60000
os.replace(tmp, S)
print("LOOP_STATE", n0, "->", os.path.getsize(S), "; archive +", os.path.getsize(A) - a0)
