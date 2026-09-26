#!/usr/bin/env python3
"""_s54_r3_dljournal.py — session 54 Round 3: THE DOWNLOAD-JOURNAL BUTTON. The gold ships `<a><div class="button">Download
(your) (learning) journal</div></a>` on ≈ 200 pages (mostly the first lesson page); Claude on ≈ 48. For every PAIRED page:
gold has the button? Claude has it? and the module's Writers Template — every line that mentions download + journal (the
writer's cue), with its tag. Tallied: gold-only pages by WT cue shape; Claude-only pages. WSL, from reference/tests/:
    python3 ../../outputs/_s54_r3_dljournal.py > ../../outputs/_s54_r3_dljournal.log"""
import os, re, sys, glob, collections
sys.path.insert(0, os.getcwd())
from _discrepancy_audit import pairs
import _corpus
from anchor_compare import CLAUDE, HUMAN

BTN = re.compile(r'<div class="button[^"]*">\s*(?:<[^>]+>\s*)*Download\s+(?:your\s+)?(?:learning\s+)?journal', re.I)
fam = lambda m: re.sub(r"\d.*$", "", m)
ROOT = os.path.abspath(os.path.join("..", "..", ".."))


def wt_lines(mod):
    d = _corpus.mdir(HUMAN, mod)
    out = []
    for p in sorted(glob.glob(os.path.join(d, "*_parsed.txt"))):
        if "media list" in os.path.basename(p).lower() and "writers" not in os.path.basename(p).lower(): continue
        for i, l in enumerate(open(p, encoding="utf-8", errors="replace")):
            if re.search(r"download", l, re.I) and re.search(r"journal", l, re.I):
                out.append((i + 1, re.sub(r"🔴\[RED TEXT\]\s*|\s*\[/RED TEXT\]🔴", "¦", l.strip())[:160]))
    return out


cnt = collections.Counter(); byfam = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
for mod in sorted(set(_corpus.gate_mods(CLAUDE))):
    pp = list(pairs(mod))
    if not pp: continue
    g_has = {os.path.basename(cp): bool(BTN.search(open(hp, encoding="utf-8", errors="replace").read())) for n, cp, hp in pp}
    c_has = {os.path.basename(cp): bool(BTN.search(open(cp, encoding="utf-8", errors="replace").read())) for n, cp, hp in pp}
    if not any(g_has.values()) and not any(c_has.values()): continue
    wl = wt_lines(mod)
    cue = "no WT line" if not wl else ("tagged" if any(re.search(r"¦[^¦]*\[[^\]]*(button|download)[^\]]*\][^¦]*¦", l, re.I) for _, l in wl) else "untagged text")
    for pg in g_has:
        k = ("gold+claude" if g_has[pg] and c_has[pg] else "gold only" if g_has[pg] else "claude only" if c_has[pg] else None)
        if not k: continue
        cnt[(k, cue)] += 1; byfam[(k, cue)][fam(mod)] += 1
        if len(ex[(k, cue)]) < 6: ex[(k, cue)].append(f"{pg}  WT: {wl[0][1] if wl else '—'}")
for key, c in sorted(cnt.items(), key=lambda kv: -kv[1]):
    print(f"{c:4d}  {key[0]:12s} | {key[1]:14s} {dict(byfam[key].most_common(8))}")
    for e in ex[key]: print("        e.g.", e[:230])
