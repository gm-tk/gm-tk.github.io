#!/usr/bin/env python3
"""Session 26 — WHERE do the gold's extra lesson-menu items come from?  For every LESSON page whose gold module menu has
more <li> than Claude's, take each gold li whose text is not an li on Claude's page and locate it:
   on-page-other-tag   the same text is on Claude's page in another tag (p / h5 …)  → a tag swap
   claude-overview     the text is in Claude's OVERVIEW menu (the r110 lesson_repeats_overview mechanism: the gold repeats it)
   gold-overview-only  the text is in the gold's overview menu but nowhere in Claude's module → the WT has it once, Claude drops it
   gold-other-lesson   the text is in the gold menu of another lesson page of the module (the menu repeats across lessons)
   wt                  the text is in the module's parsed Writers Template (fuzzy)  → derivable
   nowhere             not in the WT → the human's own addition (class C)
Per module / per prefix / per template. Also the reverse: Claude li the gold lacks.
  python3 _s26_menudeficit.py"""
import os, sys, re
from collections import Counter, defaultdict
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS)
import _corpus
from _diff_miner import page_lines, unorm
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE
from _measure_ceiling import load_meta
SKIP = re.compile(r"acks|acknowledge|glossary|references", re.I)

LEAD = re.compile(r"^(?:to |i can |i am able to |you will |we are learning to |we are learning |konga will |akonga will |students will )+")
def fold(t):
    f = re.sub(r"[^a-z0-9]+", " ", unorm(t or "").lower()).strip()
    return LEAD.sub("", f).strip()   # the D10-9 wording normalisation ('We are learning:' + 'to describe' == 'We are learning to:' + 'describe')

def tag_of(sig):
    m = re.match(r"([a-z0-9]+)", sig); return m.group(1) if m else sig

def prefix(code):
    m = re.match(r"^([A-Z]+)", code); return m.group(1) if m else code

# the parsed WT text per module (the ceiling instrument's own loader: the UNION of every *_parsed.txt in the gold dir)
from _measure_ceiling import wt_blob
_wt_cache = {}
def wt_fold(code):
    if code in _wt_cache: return _wt_cache[code]
    r = wt_blob(code)
    _wt_cache[code] = fold(r[0]) if r else ""
    return _wt_cache[code]

fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf

where = defaultdict(Counter); permod = Counter(); permod_pages = Counter(); rev = defaultdict(Counter)
EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; pre = prefix(code)
    pages = []
    for n, cp, hp in pairs(code):
        if SKIP.search(os.path.basename(hp)) or SKIP.search(os.path.basename(cp)): continue
        try:
            g, _ = page_lines(hp); c, _ = page_lines(cp)
        except Exception:
            continue
        pages.append((os.path.basename(cp), g, c))
    if not pages: continue
    gm = {b: [ln for ln in g if ln.region == "module-menu"] for b, g, c in pages}
    cm = {b: [ln for ln in c if ln.region == "module-menu"] for b, g, c in pages}
    ov = next((b for b in gm if b.endswith("_0_0.html")), None)
    c_ov_txt = {fold(ln.text) for ln in cm.get(ov, []) if ln.text} if ov else set()
    g_ov_txt = {fold(ln.text) for ln in gm.get(ov, []) if ln.text} if ov else set()
    c_all_txt = {fold(ln.text) for b in cm for ln in cm[b] if ln.text}
    wt = None
    for b, g, c in pages:
        if b.endswith("_0_0.html"): continue
        gl = [fold(ln.text) for ln in gm[b] if tag_of(ln.sig) == "li" and ln.text]
        cl = [fold(ln.text) for ln in cm[b] if tag_of(ln.sig) == "li" and ln.text]
        c_page_txt = {fold(ln.text): tag_of(ln.sig) for ln in c if ln.text}
        g_other = {fold(ln.text) for b2 in gm if b2 != b and not b2.endswith("_0_0.html") for ln in gm[b2] if ln.text}
        clset = set(cl)
        missing = [t for t in gl if t not in clset]
        extra = [t for t in cl if t not in set(gl)]
        if not missing and not extra: continue
        keys = ("ALL", f"template={tf}", f"prefix={pre}")
        if missing:
            permod[code] += len(missing); permod_pages[code] += 1
        for t in missing:
            if t in c_page_txt: w = "on-page-other-tag:" + c_page_txt[t]
            elif t in c_ov_txt: w = "claude-overview"
            elif t in c_all_txt: w = "claude-other-page"
            elif t in g_ov_txt: w = "gold-overview-only"
            elif t in g_other: w = "gold-other-lesson"
            else:
                if wt is None: wt = wt_fold(code)
                w = "wt" if (t and (t in wt or " ".join(t.split()[:6]) in wt)) else "nowhere"
            for k in keys: where[k][w] += 1
            if len(EX[w]) < 6: EX[w].append((b.replace(".html", ""), t[:60]))
        for t in extra:
            for k in keys: rev[k]["claude-extra-li"] += 1

def show(k):
    tot = sum(where[k].values())
    if not tot: return
    print(f"\n== {k}: gold lesson-menu li missing from Claude = {tot}; Claude extra li = {rev[k]['claude-extra-li']}")
    for w, v in where[k].most_common(): print(f"   {v:5d}  {v/tot:5.2f}  {w}")

show("ALL")
for k in sorted(K for K in where if K.startswith("template=")): show(k)
for k in sorted(K for K in where if K.startswith("prefix=") and sum(where[K].values()) >= 20): show(k)
print("\n== top 40 modules by missing li (lesson pages) ==")
for m, v in permod.most_common(40): print(f"   {m:10s} {fam.get(m,'?'):12s} missing li={v:4d} on {permod_pages[m]:2d} lesson pages")
print("\n== examples ==")
for w, ex in EX.items():
    print(f"   {w}: " + " | ".join(f"{b}: {t}" for b, t in ex[:4]))
