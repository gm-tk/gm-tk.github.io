#!/usr/bin/env python3
"""Session 34 Round 2 PICK measurement — queue row #4235 (`body EXTRA div.col-12.col-md-6 > img.img-fluid`, 23 pages / 19 modules):
for every Claude page of the 19 modules that puts an <img> directly in a half-width (col-md-6) column, does the GOLD module carry that
image ANYWHERE (by its iStock id / file stem)?
  DROPPED   = no gold page of the module has the image — the developer removed the writer's [Image] (class C; Claude is writer-faithful)
  ELSEWHERE = the gold has the image in another wrapper — a placement class worth measuring (what wrapper?)
Run under WSL: python3 _s34_r2_img6.py
"""
import re, os, glob
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/"
MODS = ['CEDO501', 'CEDO502', 'CEDW501', 'ENFUN02', 'ENGC401', 'ENGI103', 'ENGR101', 'ENGR201', 'ENGR202', 'ENGS201', 'OSBY301', 'OSGM301', 'OSGM401', 'OSOH501', 'OSSC301', 'OSSM301', 'OSSM501', 'SSCI104', 'TEDC402']
def stem(src):
    s = os.path.basename(src)
    if "?text=" in s: s = s.split("?text=")[-1]
    s = re.sub(r'\.(jpg|png|jpeg|gif|webp|svg)$', '', s, flags=re.I)
    return s
tot = dropped = elsewhere = 0
wrappers = {}
for code in MODS:
    cdir = (glob.glob(R + "01-Claude_Modules_/*/" + code) or [None])[0]
    gdir = (glob.glob(R + "01-Finalized_Modules_/*/" + code) or [None])[0]
    if not cdir or not gdir: print("  ? no dir", code); continue
    gold = ""
    for g in glob.glob(gdir + "/*.html"): gold += open(g, encoding="utf-8", errors="replace").read()
    for c in sorted(glob.glob(cdir + "/*.html")):
        ch = open(c, encoding="utf-8", errors="replace").read()
        # split into col-md-6 columns: from the opening tag to the next column/row opener at the same indent
        for m in re.finditer(r'<div class="col-md-6 col-12[^"]*">\n((?:(?!<div class="col-md-\d).)*?)(?=\n\t*<div class="col-md-\d|\n\t*</div>\n\t*</div>)', ch, re.S):
            body = m.group(1)
            direct = re.findall(r'^\t*<img[^>]*src="([^"]+)"', body, re.M)
            if not direct: continue
            for src in direct:
                st = stem(src); tot += 1
                # normalise the gold search: iStock ids are the digits
                key = re.search(r'\d{6,}', st)
                hit = (key.group(0) in gold) if key else (st in gold)
                if hit:
                    elsewhere += 1
                    # which wrapper holds it in the gold?
                    i = gold.find(key.group(0) if key else st); before = gold[max(0, i-600):i]
                    w = re.findall(r'class="([^"]+)"', before)
                    wr = " > ".join(w[-3:]) if w else "?"
                    wrappers[wr] = wrappers.get(wr, 0) + 1
                    print(f"  ELSEWHERE {code:8s} {os.path.basename(c):20s} {st[:28]:28s} gold wrapper: {wr}")
                else:
                    dropped += 1
                    print(f"  DROPPED   {code:8s} {os.path.basename(c):20s} {st[:28]}")
print(f"\ncol-md-6 direct images in the 19 modules: {tot} — DROPPED (no trace in any gold page of the module) {dropped} / ELSEWHERE {elsewhere}")
for k, v in sorted(wrappers.items(), key=lambda x: -x[1]): print(f"  gold wrapper x{v}: {k}")
