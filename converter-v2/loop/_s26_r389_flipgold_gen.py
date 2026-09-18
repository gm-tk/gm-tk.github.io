#!/usr/bin/env python3
"""Generates _s26_r389_flipgold.py = the _s26_rowpair.py prefix + the flipCard-group ROW census: (1) GOLD-side — every top-level
`div.flipCardsContainer.row` in the gold: its column's class, its position in the column (only / first / last / middle),
per template + subject; (2) PAIRED before-rule — for each Claude top-level flipCardsContainer, is the gold's last text BEFORE
it in the same top-level row as the gold's container (flows) or a different one (breaks)?"""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "_s26_rowpair.py"), encoding="utf-8", newline="").read()
prefix = src[:src.index("fam = {}")]
body = r'''
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
meta = load_meta()
FC = "div.flipCardsContainer"
POS = defaultdict(Counter); COL = defaultdict(Counter); GP = defaultdict(set); GM = defaultdict(set)
BEF = defaultdict(Counter); BEFp = defaultdict(set); BEFm = defaultdict(set); EXB = []
AFT = defaultdict(Counter)
CPOS = Counter()
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    keys = ("ALL", f"template={tf}", f"tmpl+subj={tf}/{subject}")
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gbase, grows = top_rows(g); cbase, crows = top_rows(c)
        if gbase is None or cbase is None: continue
        page = os.path.basename(cp)
        # (1) gold-side census
        gfc_rows = set()
        for r in grows:
            for ccol, kids in columns_of(g, r, gbase):
                for idx, k in enumerate(kids):
                    if not g[k].sig.startswith(FC): continue
                    gfc_rows.add(r)
                    pos = "only" if len(kids) == 1 else "first" if idx == 0 else "last" if idx == len(kids) - 1 else "middle"
                    colcls = g[ccol].sig.split("[")[0]
                    for kk in keys: POS[kk][pos] += 1; COL[kk][colcls] += 1
                    GP[tf].add(page); GM[tf].add(code)
        # (2) paired before-rule on the Claude side
        g_row_of = {}
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].text and tag_of(g[k].sig) in TEXT_TAGS: g_row_of.setdefault(fold(g[k].text), ri)
        g_fc_row = {}   # the gold row index holding each flipCardsContainer, keyed by its first text
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].sig.startswith(FC):
                    ft = first_text_in(g, k)
                    if ft: g_fc_row.setdefault(ft, ri)
        for r in crows:
            for ccol, kids in columns_of(c, r, cbase):
                for idx, k in enumerate(kids):
                    if not c[k].sig.startswith(FC): continue
                    pos = "only" if len(kids) == 1 else "first" if idx == 0 else "last" if idx == len(kids) - 1 else "middle"
                    CPOS[pos] += 1
                    if idx == 0: continue   # nothing before it in the column — no before-question
                    pt = None
                    for kk in reversed(kids[:idx]):
                        pt = last_text_in(c, kk)
                        if pt: break
                    ft = first_text_in(c, k)
                    if pt is None or ft is None: verdict = "no-text"
                    else:
                        gp = g_row_of.get(pt); gf = g_fc_row.get(ft)
                        if gp is None or gf is None: verdict = "gold-nowhere"
                        elif gp == gf: verdict = "gold-flows (Claude right)"
                        else: verdict = "GOLD-BREAKS before (Claude flowed)"
                    for kk in keys: BEF[kk][verdict] += 1
                    if verdict.startswith("GOLD") or verdict.startswith("gold-flows"):
                        BEFp[kk].add(page); BEFm[kk].add(code)
                    if verdict.startswith("GOLD") and len(EXB) < 8: EXB.append(f"{page[:-5]} before=«{(pt or '')[:40]}» first-card=«{(ft or '')[:30]}»")
print("==== (1) GOLD-side: the top-level flipCardsContainer's column class + position in its column ====")
for kk in sorted(POS, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    tot = sum(POS[kk].values())
    if tot < 3 and not kk.startswith("ALL") and not kk.startswith("template"): continue
    print(f"   {kk:44s} n={tot:3d}  pos={dict(POS[kk].most_common())}  col={dict(COL[kk].most_common(4))}")
print("   gold pages / modules by template:", {k: (len(GP[k]), len(GM[k])) for k in GP})
print("\n==== (2) PAIRED before-rule: Claude's top-level flipCardsContainer with text before it in the SAME column ====")
print("   Claude container positions:", dict(CPOS))
D = "GOLD-BREAKS before (Claude flowed)"; A = "gold-flows (Claude right)"
for kk in sorted(BEF, key=lambda x: (not x.startswith("ALL"), not x.startswith("template"), x)):
    cnt = BEF[kk]; dis = cnt.get(D, 0); ag = cnt.get(A, 0)
    if dis + ag == 0: continue
    print(f"   {kk:44s} gold-breaks {dis:3d} / flows {ag:3d} = {dis/(dis+ag):.2f}  pages {len(BEFp[kk])} / mods {len(BEFm[kk])}  [{ {k: v for k, v in cnt.items() if k not in (D, A)} }]")
for e in EXB: print("      ", e)
'''
io.open(os.path.join(HERE, "_s26_r389_flipgold.py"), "w", encoding="utf-8", newline="").write(prefix + body)
print("wrote _s26_r389_flipgold.py")
