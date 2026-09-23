#!/usr/bin/env python3
"""Session 41 §5d condense #2 (after r454; LOOP_STATE.md ≈ 98 KB, at the target). Moves VERBATIM to LOOP_STATE_ARCHIVE.md and
leaves one pointer line each: (1) the Declined-classes entries of sessions 34 / 36 / 37 (the class + verdict stay findable by
the pointer's class names); (2) the Position 'Before it: r452' and 'Before it: r453' verbatim gate rows. Nothing is deleted.
Run under WSL."""
import io, os, re, shutil
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
P = os.path.join(ROOT, "LOOP_STATE.md"); A = os.path.join(ROOT, "LOOP_STATE_ARCHIVE.md")
shutil.copyfile(P, P + ".pre-s41-condense2.bak")
src = io.open(P, encoding="utf-8").read(); L = src.split("\n"); moved = []
def take(pred, title, pointer):
    idx = [i for i, l in enumerate(L) if pred(l)]
    if not idx: print("NOT FOUND:", title); return
    moved.append((title, [L[i] for i in idx]))
    L[idx[0]] = pointer
    for i in reversed(idx[1:]): del L[i]
    print(f"moved {len(idx)} line(s), {sum(len(L2) for L2 in moved[-1][1])} chars: {title}")
dec = re.compile(r"^- \*\*Session 3[4-7] Round \d")
take(lambda l: bool(dec.match(l)),
     "Declined classes — sessions 34 / 36 / 37 entries (verbatim, s41 §5d condense #2)",
     "- **Sessions 34 / 36 / 37 declined classes (9 entries, verbatim → LOOP_STATE_ARCHIVE.md 'Declined classes — sessions 34 / 36 / 37 entries (verbatim, s41 §5d condense #2)'; every verdict stands, grep the class name there):** s37-r4 the gold-built widget Claude never recognised (no source / below floor per type) · s37-r3 the footer navigation link set (no discriminator; rates match) · s37-r2 the widget type named in free text (r438, built / probed / reverted; 5× over-count) · s36-r5 the module menu's section content as a list (no line-level discriminator) · s36-r1 the `[Lesson Overview]` marker's trailing sentence (KB-correct, c70) · s34-r5 the inquiry panel's first-heading level by family (h2 stands) · s34-r2 #4235 the half-column body image (class C).")
take(lambda l: l.startswith("- Before it: **r452**"),
     "Position — LAST SHIPPED tail r452 (verbatim, s41 §5d condense #2)",
     "- Before it: **r452** (260620.23, the invented journal button, D13-5, +0.0077pp named) — its verbatim gate row → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r452 (verbatim, s41 §5d condense #2)'.")
take(lambda l: l.startswith("- Before it: **r453**"),
     "Position — LAST SHIPPED tail r453 (verbatim, s41 §5d condense #2)",
     "- Before it: **r453** (260620.24, the table-cell title bar + the MTK overview-table tabs, KB 07A §4; pairs 2477 → 2487, the pre-existing pairs +0.0211pp, three movers named) — its verbatim gate row → LOOP_STATE_ARCHIVE.md 'Position — LAST SHIPPED tail r453 (verbatim, s41 §5d condense #2)'.")
out = "\n".join(L); tmp = P + ".tmp"
io.open(tmp, "w", encoding="utf-8", newline="\n").write(out)
io.open(A, "a", encoding="utf-8", newline="\n").write("".join("\n## " + t + "\n\n" + "\n".join(b) + "\n" for t, b in moved))
os.replace(tmp, P)
print("LOOP_STATE.md", len(src.encode("utf-8")), "->", os.path.getsize(P))
