#!/usr/bin/env python3
"""Generates _s26_r389_divpair.py = the _s26_rowpair.py prefix (helpers) + a direction-B census keyed on the FULL signature of
the block Claude flows after, for the 'div' kind (the r388 lead: after a built flipCard group the gold opens a row 0.79)."""
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
SIG = defaultdict(Counter); SIGp = defaultdict(set); SIGm = defaultdict(set); EX = defaultdict(list)
GRP = defaultdict(Counter); GRPp = defaultdict(set)
NEXT = defaultdict(Counter)   # what follows the div on the Claude side (the flowed text's own signature)
for code in sorted(fam):
    tf = fam[code]; subject = (meta.get(code, {}) or {}).get("subject") or "None"
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        gbase, grows = top_rows(g); cbase, crows = top_rows(c)
        if gbase is None or cbase is None or not crows: continue
        g_row_of = {}
        for ri, r in enumerate(grows):
            end = subtree_end(g, r)
            for k in range(r + 1, end):
                if g[k].text and tag_of(g[k].sig) in TEXT_TAGS: g_row_of.setdefault(fold(g[k].text), ri)
        page = os.path.basename(cp)
        for r in crows:
            for ccol, kids in columns_of(c, r, cbase):
                for a, b in zip(kids, kids[1:]):
                    if not (c[b].text and tag_of(c[b].sig) in TEXT_TAGS): continue
                    if tag_of(c[b].sig) in OPENER_TAGS: continue
                    if kind(c[a].sig) != "div": continue
                    sig = c[a].sig.split("[")[0]
                    yt = fold(c[b].text); xt = last_text_in(c, a)
                    if xt is None:
                        for k in reversed(kids[:kids.index(a)]):
                            xt = last_text_in(c, k)
                            if xt: break
                    if xt is None: verdict = "no-text"
                    else:
                        gy = g_row_of.get(yt); gx = g_row_of.get(xt)
                        if gy is None or gx is None: verdict = "gold-nowhere"
                        elif gy == gx: verdict = "gold-flows (Claude right)"
                        else: verdict = "GOLD-BREAKS (Claude flowed)"
                    SIG[sig][verdict] += 1; NEXT[sig][c[b].sig.split("[")[0]] += 1
                    GRP[(sig, tf, subject)][verdict] += 1
                    if verdict.startswith("GOLD") or verdict.startswith("gold-flows"):
                        SIGp[sig].add(page); SIGm[sig].add(code); GRPp[(sig, tf, subject)].add(page)
                    if verdict.startswith("GOLD") and len(EX[sig]) < 6:
                        EX[sig].append(f"{page[:-5]} X=«{(c[a].text or c[a].sig)[:40]}» Y=«{(c[b].text or '')[:40]}»")
D = "GOLD-BREAKS (Claude flowed)"; A = "gold-flows (Claude right)"
print("==== direction B, kind 'div' by FULL signature — Claude flows the next text after X inside the column; does the gold break? ====")
for sig, cnt in sorted(SIG.items(), key=lambda kv: -(kv[1].get(D, 0) + kv[1].get(A, 0))):
    dis = cnt.get(D, 0); ag = cnt.get(A, 0)
    if dis + ag == 0: print(f"   {sig:48s} decided 0  [{dict(cnt)}]"); continue
    print(f"   {sig:48s} gold-breaks {dis:3d} / flows {ag:3d} = {dis/(dis+ag):.2f}  pages {len(SIGp[sig])} / mods {len(SIGm[sig])}  next={dict(NEXT[sig].most_common(3))}  [{ {k: v for k, v in cnt.items() if k not in (D, A)} }]")
    for e in EX[sig]: print("        ", e)
print("\n   per (signature, template, subject) with ≥ 3 decided boundaries:")
for (sig, tf, subject), cnt in sorted(GRP.items()):
    dis = cnt.get(D, 0); ag = cnt.get(A, 0)
    if dis + ag >= 3: print(f"     {sig:44s} {tf:12s} {subject:28s} {dis:3d} / {ag:3d} = {dis/(dis+ag):.2f}  pages {len(GRPp[(sig, tf, subject)])}")
'''
out = prefix + body
io.open(os.path.join(HERE, "_s26_r389_divpair.py"), "w", encoding="utf-8", newline="").write(out)
print("wrote _s26_r389_divpair.py", len(out))
