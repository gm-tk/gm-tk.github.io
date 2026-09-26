#!/usr/bin/env python3
"""_s53_r4_tfquiz.py — session 53 Round 4: THE TRUE / FALSE TABLE — every UN-BUILT widget entry in the Claude corpus's
<CODE>_interactives.txt whose content carries a table with a True column and a False column in its header row. Per entry: the Type,
the rows, how many rows carry exactly ONE mark in the T/F columns (the answer key — D13-4: build only where the writer marked it),
the mark glyphs, other members. WSL:  python3 _s53_r4_tfquiz.py [--list] > _s53_r4_tfquiz.log"""
import os, re, glob, collections, sys
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
TRUE = re.compile(r"^\s*(?:true|t|tika|pono|yes|ae|āe)\s*[?.]?\s*$", re.I)
FALSE = re.compile(r"^\s*(?:false|f|hē|he|teka|no|kāo|kao)\s*[?.]?\s*$", re.I)
MARK = re.compile(r"^\s*(?:[√✓✔✅☑xX×*•]|tick|yes|correct)\s*$", re.I)
clean = lambda c: re.sub(r"\*+|__|🔴\[RED TEXT\]|\[/RED TEXT\]🔴", "", c).strip()
stats = collections.Counter(); bytype = collections.Counter(); glyphs = collections.Counter(); mods = collections.defaultdict(set)
ok_entries = []; bad = collections.Counter()
for f in sorted(glob.glob(os.path.join(ROOT, "01-Claude_Modules_", "*", "*", "*_interactives.txt"))):
    code = os.path.basename(f).split("_")[0]
    txt = open(f, encoding="utf-8", errors="replace").read()
    for ent in re.split(r"\nINTERACTIVE \d+ of \d+\n", txt)[1:]:
        ty = (re.search(r"^Type: (.+)$", ent, re.M) or [None, "?"])[1].strip()
        page = (re.search(r"^File: (.+)$", ent, re.M) or [None, "?"])[1].strip()
        for tb in re.findall(r"┌─── TABLE ───\n(.*?)\n└─── END TABLE ───", ent, re.S):
            rows = [[clean(c) for c in r.lstrip("│ ").split("║")] for r in tb.split("\n") if r.startswith("│")]
            if len(rows) < 2: continue
            hdr = rows[0]
            ti = [i for i, c in enumerate(hdr) if TRUE.match(c)]; fi = [i for i, c in enumerate(hdr) if FALSE.match(c)]
            if len(ti) != 1 or len(fi) != 1: continue
            t, fcol = ti[0], fi[0]
            others = [i for i in range(len(hdr)) if i not in (t, fcol)]
            data = rows[1:]; one = 0
            for r in data:
                tv = r[t] if t < len(r) else ""; fv = r[fcol] if fcol < len(r) else ""
                if tv: glyphs[tv[:6]] += 1
                if fv: glyphs[fv[:6]] += 1
                mt, mf = bool(MARK.match(tv)), bool(MARK.match(fv))
                if mt != mf and not (tv and not mt) and not (fv and not mf): one += 1
            full = one == len(data)
            k = f"{'ALL-MARKED' if full else ('NONE' if one == 0 else 'PARTIAL')}  cols={len(hdr)} other={len(others)}"
            stats[k] += 1; bytype[(ty, 'ALL' if full else 'not')] += 1; mods[k].add(code)
            if full: ok_entries.append((code, page, ty, len(data), hdr))
            else: bad[(code, page, ty)] += 1
print("T/F tables in un-built entries:")
for k, v in stats.most_common(): print(f"  {v:4d}  {k}  ({len(mods[k])} modules)")
print("\nby Type:", bytype.most_common(12))
print("\nmark glyphs:", glyphs.most_common(15))
print(f"\nALL-MARKED entries {len(ok_entries)} in {len({e[0] for e in ok_entries})} modules; rows {sum(e[3] for e in ok_entries)}")
if "--list" in sys.argv:
    for e in ok_entries: print("  ", e)
    for e in bad: print("  NOT", e)
