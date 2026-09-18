#!/usr/bin/env python3
"""Session 26 Round 7 candidates — two paired censuses over the LIVE body (the r392 carve):
 (A) ROW-IN-ROW: a `<div class="row">` whose nearest wrapper ancestor is another `div.row` (no column between) — Claude vs gold.
 (B) PUNCTUATION-ONLY PARAGRAPHS: `<p>` whose text is one non-alphanumeric glyph (`.`, `□`, `-`, nbsp…) — Claude vs gold.
python3 _s26_r393_rowrow.py"""
import os, sys, re, html as H
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
sys.path.insert(0, OUTPUTS)
src = open(os.path.join(OUTPUTS, "_s26_r392_adjul.py"), encoding="utf-8").read()
exec(src[:src.index("ADJ = re.compile")])
from collections import Counter, defaultdict
TAG = re.compile(r"<(/?)(div|p|ul|ol|li|table|h[1-6]|section)\b([^>]*)>", re.I)
CLS = re.compile(r'class="([^"]*)"')
def rowrow(s):
    """count div.row elements whose innermost open div ancestor is a div.row."""
    st = []; n = 0; ex = []
    for m in TAG.finditer(s):
        closing, tag, attrs = m.group(1), m.group(2).lower(), m.group(3)
        if tag != "div": continue
        if closing:
            if st: st.pop()
            continue
        c = CLS.search(attrs); cls = c.group(1).split() if c else []
        isrow = "row" in cls
        if isrow and st and st[-1] == "row":
            n += 1
            if len(ex) < 2: ex.append(re.sub(r"\s+", " ", s[m.start():m.start()+140]))
        st.append("row" if isrow else ("col" if any(x.startswith("col") for x in cls) else "other"))
    return n, ex
PUNCT = re.compile(r"<p\b[^>]*>\s*(?:<[^>]+>\s*)*([^\w<>\s])\s*(?:</[^>]+>\s*)*</p>")
A = defaultdict(Counter); B = defaultdict(Counter); Ap = defaultdict(set); Am = defaultdict(set); Bp = defaultdict(set); Bm = defaultdict(set); GA = defaultdict(set); GB = defaultdict(set); EXA = []; EXB = Counter(); GXB = Counter()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subj}")
    for n, cp, hp in pairs(code):
        try:
            ch = body(open(cp, encoding="utf-8", errors="replace").read()); gh = body(open(hp, encoding="utf-8", errors="replace").read())
        except Exception:
            continue
        cl = "".join(live_pieces(ch)); gl = "".join(live_pieces(gh))
        ca, exa = rowrow(cl); ga, _ = rowrow(gl)
        cb = PUNCT.findall(cl); gb = PUNCT.findall(gl)
        for k in keys:
            A[k]["claude"] += ca; A[k]["gold"] += ga; B[k]["claude"] += len(cb); B[k]["gold"] += len(gb)
        if ca:
            Ap[keys[2]].add(cp); Am[keys[2]].add(code); Ap["ALL"].add(cp); Am["ALL"].add(code)
            if len(EXA) < 5: EXA.append(f"{os.path.basename(cp)[:-5]}: {exa[0][:130]}")
        if ga: GA[keys[2]].add(hp); GA["ALL"].add(hp)
        if cb:
            Bp[keys[2]].add(cp); Bm[keys[2]].add(code); Bp["ALL"].add(cp); Bm["ALL"].add(code)
            for g in cb: EXB[H.unescape(g)] += 1
        if gb:
            GB[keys[2]].add(hp); GB["ALL"].add(hp)
            for g in gb: GXB[H.unescape(g)] += 1
for title, C, Cp, Cm, Gp, in (("(A) ROW-IN-ROW (div.row directly inside div.row)", A, Ap, Am, GA), ("(B) PUNCTUATION-ONLY PARAGRAPHS", B, Bp, Bm, GB)):
    print("====", title, "— Claude vs gold ====")
    for k in sorted(C, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), -C[x]["claude"])):
        if C[k]["claude"] + C[k]["gold"] == 0: continue
        if not k.startswith("ALL") and not k.startswith("template") and C[k]["claude"] < 5 and C[k]["gold"] < 5: continue
        print(f"   {k:46s} claude {C[k]['claude']:4d} (pages {len(Cp.get(k, set())):3d} / mods {len(Cm.get(k, set())):3d})  gold {C[k]['gold']:4d} (pages {len(Gp.get(k, set())):3d})")
print("   (A) examples:"); [print("     ", e) for e in EXA]
print("   (B) Claude glyphs:", EXB.most_common(10)); print("   (B) gold glyphs:", GXB.most_common(10))
