#!/usr/bin/env python3
"""Round 447 — the WORD-LOSS check over every changed page: the visible text of the disk page (the r446 state)
against the ON page (outputs/_r447_on). A word the disk shows and the ON page no longer shows is LOST unless it is
part of the round's intended removals: the red "Wire this button's link …" To Do and the green button's journal
label words (journal / learning / go / to / your / the / button). Prints every other lost word with its page."""
import os, re, io, glob, html, collections
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
ON = os.path.join(HERE, "_r447_on")
pages = [l.strip() for l in io.open(os.path.join(HERE, "_r447_ON_pages.txt"), encoding="utf-8") if l.strip()]
NOTE = re.compile(r'<p class="cv2-note"[^>]*>Designer/Developer To Do: Wire this button.*?</p>', re.S)
TAGS = re.compile(r"<[^>]+>")
ALLOWED = {"journal", "learning", "go", "to", "your", "the", "button", "g", "o", "learners"}
def words(s):
    s = NOTE.sub(" ", s)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    s = html.unescape(TAGS.sub(" ", s))
    return collections.Counter(w.lower() for w in re.findall(r"[\w’']+", s))
tot_lost = 0; bad = []
for p in pages:
    code, fn = p.split("/", 1)
    disk = glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", code, fn)) + glob.glob(os.path.join(ROOT, "01-Claude_Modules_", code, fn))
    on = os.path.join(ON, code, fn)
    if not disk or not os.path.exists(on):
        bad.append(f"{p}: missing (disk {bool(disk)}, on {os.path.exists(on)})"); continue
    a = words(io.open(disk[0], encoding="utf-8").read()); b = words(io.open(on, encoding="utf-8").read())
    lost = {w: n - b.get(w, 0) for w, n in a.items() if n > b.get(w, 0) and w not in ALLOWED}
    gained = {w: n - a.get(w, 0) for w, n in b.items() if n > a.get(w, 0) and w not in ALLOWED}
    if lost:
        tot_lost += sum(lost.values())
        bad.append(f"{p}: LOST {lost}  (gained {gained})")
print(f"pages checked {len(pages)}; pages with a lost non-label word {len(bad)}; lost words {tot_lost}")
for b in bad: print("  " + b[:400])
