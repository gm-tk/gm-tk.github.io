#!/usr/bin/env python3
"""Session 30 Round 6 PICK — the four big widget types' bundles (the live-scanner dumps _s30_r6_<type>.log), joined to the DISK
truth (is the bundle a hand-off box on Claude's page? — by the box marker `INTERACTIVE (un-built) #N: TYPE` count per page vs
built widgets): for the UN-BUILT bundles, the member-kind SHAPE (the sequence of member kinds: tag names / black / table dims /
media) and the invocation's own words, grouped → the largest un-built authoring families per type with their module counts.
Output: _s30_r6_shapes.out"""
import os, re, glob, sys
from collections import Counter, defaultdict
sys.path.insert(0, "/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests")
import _corpus
from anchor_compare import CLAUDE
HERE = os.path.dirname(os.path.abspath(__file__))

def disk_unbuilt(code, typ):
    """the count of un-built boxes of this type per page label on disk (page label derived from the filename)"""
    out = Counter()
    d = _corpus.mdir(CLAUDE, code)
    for f in glob.glob(os.path.join(d, "*.html")):
        s = open(f, encoding="utf-8", errors="replace").read()
        n = len(re.findall(r"INTERACTIVE \(un-built\) #\d+: " + typ + r"\b", s))
        if n: out[os.path.basename(f)] += n
    return out

def parse_dump(path):
    bundles = []; cur = None
    for line in open(path, encoding="utf-8", errors="replace"):
        line = line.rstrip("\n")
        m = re.match(r"=== (\S+) page (\S+) (\S+) #\S+ modifier=\"(.*?)\" extraTypes=(\[.*?\]) owner=(.*)$", line)
        if m:
            cur = {"code": m.group(1), "page": m.group(2), "type": m.group(3), "modifier": m.group(4), "extra": m.group(5), "owner": m.group(6), "members": [], "tables": 0, "media": 0, "inv": ""}
            bundles.append(cur); continue
        if cur is None: continue
        mm = re.match(r"\s+\[tag (\S+?)(?:/(\S+))? cls=(\S+)\] text«(.*?)» after«(.*?)»", line)
        if mm:
            if not cur["inv"]: cur["inv"] = mm.group(4)
            cur["members"].append("tag:" + mm.group(1)); continue
        mt = re.match(r"\s+\[table (\d+)x(\d+)\]", line)
        if mt: cur["members"].append("table"); continue
        mb = re.match(r"\s+\[(black|nested|\w+)\] «(.*?)»", line)
        if mb: cur["members"].append(mb.group(1)); continue
        ms = re.match(r"\s+tables: (\d+); media: (\[.*?\]); instructions", line)
        if ms: cur["tables"] = int(ms.group(1)); cur["media"] = 0 if ms.group(2) == "[]" else ms.group(2).count(",") + 1
    return bundles

def shape(b):
    ms = b["members"]
    # collapse runs
    out = []
    for m in ms:
        k = "black" if m == "black" else ("table" if m == "table" else m)
        if out and out[-1][0] == k: out[-1][1] += 1
        else: out.append([k, 1])
    return " ".join(f"{k}x{n}" if n > 1 else k for k, n in out)[:70] + f" | T{b['tables']} M{b['media']}" + (" +extra" if b["extra"] != "[]" else "")

def main():
    L = []
    for typ in ("carousel", "accordion", "flipCard", "clickDrop"):
        bs = parse_dump(os.path.join(HERE, f"_s30_r6_{typ}.log"))
        # disk truth per module: total un-built boxes of the type
        unb = defaultdict(int)
        for code in sorted({b["code"] for b in bs}):
            unb[code] = sum(disk_unbuilt(code, typ).values())
        # a module whose un-built count equals its bundle count → every bundle un-built; otherwise mark the module MIXED
        sh = Counter(); mods = defaultdict(set); ex = {}
        for b in bs:
            if unb[b["code"]] == 0: continue          # every bundle of this module built
            s = shape(b); key = (s, "all-unbuilt" if unb[b["code"]] >= len([x for x in bs if x["code"] == b["code"]]) else "mixed")
            sh[key] += 1; mods[key].add(b["code"])
            ex.setdefault(key, f"{b['code']} p{b['page']} «{b['inv'][:50]}»")
        L.append(f"== {typ}: bundles {len(bs)} in {len({b['code'] for b in bs})} modules; un-built boxes on disk {sum(unb.values())} in {sum(1 for v in unb.values() if v)} modules")
        for k, v in sh.most_common(10):
            L.append(f"   {v:4d} bundles / {len(mods[k]):3d} mods  [{k[1]}]  {k[0]}   e.g. {ex[k]}")
    txt = "\n".join(L)
    open(os.path.join(HERE, "_s30_r6_shapes.out"), "w", encoding="utf-8").write(txt + "\n")
    print(txt)
main()
