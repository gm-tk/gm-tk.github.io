#!/usr/bin/env python3
"""_s52_r6_rhsimg.py — session 52 Round 6: THE WRITER-CUED RIGHT-HAND IMAGE. Every image tag in the WT item streams
(outputs/_s52_items/) whose own text cues a side placement (RHS / right / beside / next to / side) — where does the gold put that
image (matched by its file-name stem or iStock number in the gold's <img src / alt>): in a col-md-4 SIDE column, in the main
column, or not found? Per family; and where Claude puts it. WSL."""
import os, re, glob, collections
R = "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA"; O = os.path.dirname(os.path.abspath(__file__))
CUE = re.compile(r"\b(?:rhs|right[- ]hand|right|beside|next to|alongside|side)\b", re.I)
def stems(payload):
    out = []
    for m in re.finditer(r"iStock[-_ ]?(\d{6,})", payload, re.I): out.append(m.group(1))
    for m in re.finditer(r"([A-Za-z0-9][\w \-]{3,60}?)\.(?:png|jpe?g|gif|svg)", payload, re.I): out.append(m.group(1).strip().lower())
    return out
def div_close(s, i):
    d = 0
    for m in re.finditer(r"<(/?)div\b[^>]*>", s[i:]):
        d += -1 if m.group(1) else 1
        if d == 0: return i + m.end()
    return len(s)
def placement(pages, stem):
    for s in pages:
        for m in re.finditer(r"<img\b[^>]*>", s):
            tag = m.group(0)
            if stem.lower() not in tag.lower(): continue
            # the innermost enclosing col-* div before the img
            opens = [(x.start(), x.group(1)) for x in re.finditer(r'<div class="([^"]*)"', s[:m.start()])]
            for st, cls in reversed(opens):
                if "col-" in cls and div_close(s, st) > m.start():
                    return "SIDE col-md-4" if "col-md-4" in cls or "col-md-3" in cls else ("half col-md-6" if "col-md-6" in cls else "MAIN")
            return "no-col"
    return None
res = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list); cl = collections.Counter()
for tsv in sorted(glob.glob(os.path.join(O, "_s52_items", "*.tsv"))):
    mod = os.path.basename(tsv)[:-4]; fam = re.sub(r"\d.*$", "", mod)
    gdirs = glob.glob(f"{R}/01-Finalized_Modules_/*/{mod}"); cdirs = glob.glob(f"{R}/01-Claude_Modules_/*/{mod}")
    if not gdirs: continue
    gp = [open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(gdirs[0] + "/*.html")]
    cp = [open(f, encoding="utf-8", errors="replace").read() for f in glob.glob(cdirs[0] + "/*.html")] if cdirs else []
    for line in open(tsv, encoding="utf-8"):
        f = line.rstrip("\n").split("\t")
        if len(f) < 9 or f[2] != "tag" or not re.search(r"image|img|photo|picture|media item", f[3] + " " + f[6], re.I): continue
        cue = bool(CUE.search(f[6].split("]", 1)[-1] if "]" in f[6] else "")) or bool(re.search(r"\[[^\]]*\b(?:rhs|right)\b[^\]]*\]", f[6], re.I))
        st = stems(f[7] + " " + f[8] + " " + f[6])
        if not st: continue
        where = next((w for w in (placement(gp, s) for s in st) if w), None)
        cw = next((w for w in (placement(cp, s) for s in st) if w), None)
        key = "CUED" if cue else "uncued"
        res[key][where or "not-found"] += 1
        if cue: res["CUED:" + fam][where or "not-found"] += 1; cl[cw or "not-found"] += 1
        if cue and len(ex[where or "nf"]) < 6: ex[where or "nf"].append(f"{mod} {f[6][:50]!r} {st[0]!r} claude:{cw}")
for k in ("CUED", "uncued"): print(k, dict(res[k]))
print("CUED — claude places them:", dict(cl))
for k in sorted(res):
    if k.startswith("CUED:") and sum(res[k].values()) >= 3: print("  ", k, dict(res[k]))
for k, l in ex.items():
    print(k); [print("    ", x) for x in l]
