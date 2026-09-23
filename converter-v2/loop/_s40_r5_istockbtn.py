#!/usr/bin/env python3
"""Session 40 Round 5 PICK measure — buttons whose href is an iStock page (an IMAGE reference, never a web resource):
per button, whether the same iStock id is ALSO rendered as an image on the page (then the button is only a stray link)
or NOT (then the button ate the writer's image), and what the gold page shows for that id (an <img> / a link / absent)."""
import os, re, io, glob, collections
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.normpath(os.path.join(HERE, "..", ".."))
BTN = re.compile(r'<a href="(https?://(?:www\.)?istockphoto\.com[^"]*)"[^>]*><div class="((?:external)?[Bb]utton[^"]*)">([^<]*)</div></a>')
ID = re.compile(r"gm-?(\d{6,12})|/id/(\d{5,12})|-(\d{6,12})-\d+\b")
rows = []; c = collections.Counter()
for f in glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*.html")):
    s = io.open(f, encoding="utf-8", errors="replace").read()
    for m in BTN.finditer(s):
        url, cls, label = m.groups()
        idm = ID.search(url); iid = next((g for g in idm.groups() if g), None) if idm else None
        also = bool(iid) and len(re.findall(r'<img[^>]*' + iid, s)) > 0
        code = os.path.basename(os.path.dirname(f))
        gold = "no id"
        if iid:
            gold = "absent"
            for gf in glob.glob(os.path.join(ROOT, "01-Finalized_Modules_", "*", code, "*.html")):
                gs = io.open(gf, encoding="utf-8", errors="replace").read()
                if re.search(r'<img[^>]*' + iid, gs): gold = "img"; break
                if iid in gs: gold = "mentioned"
        k = ("also-an-image" if also else "image-LOST", gold)
        c[k] += 1; rows.append((code, os.path.basename(f), label, k))
print(f"iStock-href buttons: {len(rows)} on {len({(r[0], r[1]) for r in rows})} pages / {len({r[0] for r in rows})} modules")
for k, n in c.most_common(): print(f"  {n:3d}  {k}")
for r in rows: print(f"  {r[0]}/{r[1]}: {r[2]!r} {r[3]}")
