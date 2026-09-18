#!/usr/bin/env python3
"""Session 27 Round 2 candidate — THE WORD-FORM ID IN A BARE ACTIVITY OPENER'S TAIL.
`[Activity] Activity 4B: My rohe – my iwi` (the id NOT in the bracket, the r377 word form in the black tail) ships a
numberless box titled with the whole tail; the gold takes number="4B" + <h3>My rohe – my iwi</h3>. Over every module's
parsed WT (the combined-file trap honoured): every activity-family opener whose bracket carries NO id and whose tail opens
with `Activity <id>` — count, per family; then the GOLD form on the paired page: a box with that number? its h3 = the
remainder? And what Claude ships today (number / title).
  wsl: python3 _s27_r2_acttail.py → _s27_r2_acttail2.out"""
import os, sys, re, glob
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _measure_ceiling import load_meta
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
OPEN = re.compile(r"🔴\[RED TEXT\]\s*\[(activity[^\]]*)\]\s*\[/RED TEXT\]🔴\s*(.*)$", re.I)
WORD = re.compile(r"^\s*(?:✅\s*)?(?:activity\s+)?(\d{1,2}[A-Za-z]|[A-Za-z]\d{1,2})\b\s*[:\-–—.]?\s*(.+)$", re.I)
IDIN = re.compile(r"\b\d{1,2}[A-Za-z]\b|\b[A-Za-z]\d{1,2}\b")
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    pref = [f for f in fs if "writers template" in f.lower()] or fs
    out = []
    for f in pref[:1]:
        out += open(os.path.join(d, f), encoding="utf-8", errors="replace").read().split("\n")
    return out
def fold(t): return re.sub(r"\W+", " ", t.lower()).strip()
SITES = Counter(); SITES_T = defaultdict(Counter); GOLD = Counter(); CLAUDE_F = Counter(); EX = []
pages_g = set(); mods = set()
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"
    try: lines = wt_lines(code)
    except Exception: continue
    hits = []
    for l in lines:
        m = OPEN.search(l)
        if not m: continue
        bracket, tail = m.group(1), m.group(2).strip()
        if IDIN.search(bracket): continue            # the id is in the bracket — the standard opener
        w = WORD.match(tail)
        if not w: continue
        hits.append((bracket, w.group(1).upper(), w.group(2).strip(), tail))
    if not hits: continue
    SITES[code] = len(hits); SITES_T[tf + "/" + subj][code] += len(hits); mods.add(code)
    # gold: for each hit, find a box with that number on any gold page; its h3
    gd = _corpus.mdir(HUMAN, code); gpages = {}
    for f in os.listdir(gd):
        if f.endswith(".html"): gpages[f] = open(os.path.join(gd, f), encoding="utf-8", errors="replace").read()
    cd = _corpus.mdir(CLAUDE, code); cpages = {}
    for f in os.listdir(cd):
        if f.endswith(".html"): cpages[f] = open(os.path.join(cd, f), encoding="utf-8", errors="replace").read()
    for bracket, num, title, tail in hits:
        found = None
        for f, h in gpages.items():
            m = re.search(r'<div class="activity[^"]*" number="' + re.escape(num) + r'"[^>]*>(.{0,600})', h, re.S)
            if m:
                h3 = re.search(r"<h3[^>]*>(.*?)</h3>", m.group(1), re.S)
                found = (f, re.sub(r"<[^>]+>", "", h3.group(1)).strip() if h3 else None); pages_g.add(code + f); break
        if found is None: GOLD["no box with that number in the gold"] += 1
        elif found[1] is None: GOLD["box numbered, no h3"] += 1
        elif fold(found[1]) == fold(title): GOLD["box numbered + h3 = the remainder"] += 1
        elif fold(found[1]) == fold(tail): GOLD["box numbered + h3 = the whole tail"] += 1
        else: GOLD["box numbered + a different h3"] += 1
        # Claude today
        cl = None
        for f, h in cpages.items():
            i = h.find(tail[:40])
            if i >= 0:
                seg = h[max(0, i - 400):i]
                nb = re.findall(r'<div class="activity[^"]*"( number="[^"]*")?', seg)
                cl = ("numbered" if nb and nb[-1] else "numberless") if nb else "no box"; break
        CLAUDE_F[cl or "text not found"] += 1
        if len(EX) < 8: EX.append(f"{code}: [{bracket}] «{tail[:60]}» → gold {found} · Claude {cl}")
out = []
def P(s=""): out.append(s); print(s)
P(f"word-form tails on bare activity openers: {sum(SITES.values())} sites / {len(mods)} modules; gold pages holding the numbered box: {len(pages_g)}")
P("gold form: " + "; ".join(f"{k} {v}" for k, v in GOLD.most_common()))
P("Claude today: " + "; ".join(f"{k} {v}" for k, v in CLAUDE_F.most_common()))
P("by template/subject: " + "; ".join(f"{g} {sum(c.values())} sites / {len(c)} mods" for g, c in sorted(SITES_T.items(), key=lambda kv: -sum(kv[1].values()))))
P("top modules: " + ", ".join(f"{c} {n}" for c, n in SITES.most_common(15)))
for e in EX: P("  " + e)
open(os.path.join(OUTPUTS, "_s27_r2_acttail2.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
