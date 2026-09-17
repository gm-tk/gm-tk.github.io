#!/usr/bin/env python3
"""r363 PICK probe — THE LESSON-PAGE MODULE MENU: does the gold render `#module-head-buttons` +
`#module-menu-content` on a lesson page exactly when the Writers Template's lesson carries a
[Lesson Overview] block (KB 01B 'Lesson pages: Overview content comes from [Lesson Overview]')?
For every paired LESSON page of the gate population: gold menu? Claude menu? WT lesson has a
[Lesson Overview] tag / bare lead / a WALT-I-can label near its opening? The registry's per-series
lesson value. Writes _r363_lessonmenu.{json,log}. Runs under WSL like every gate tool."""
import os, sys, re, json
from collections import Counter, defaultdict
BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.normpath(os.path.join(BASE, "..", ".."))
TESTS = os.path.join(ROOT, "CONVERTER_V2", "reference", "tests")
for p in (BASE, TESTS):
    if p in sys.path:
        sys.path.remove(p)
    sys.path.insert(0, p)
import _corpus
from _discrepancy_audit import pairs
from anchor_compare import CLAUDE, HUMAN
from _measure_ceiling import load_meta, SKIP_PAGE

DATA = os.path.join(ROOT, "CONVERTER_V2", "data")
REG = json.load(open(os.path.join(DATA, "Menu_Scaffold_Registry.json"), encoding="utf-8"))
RED = re.compile(r"\U0001f534\[RED TEXT\]|\[/RED TEXT\]\U0001f534")
LESSON = re.compile(r"\[\s*(?:lesson(?!\s+(?:overview|content|\d+\s+content))|page)\s*(\d*)[^\]]*\]", re.I)
LO_TAG = re.compile(r"\[\s*lesson\s+overview\s*\]", re.I)
LO_BARE = re.compile(r"^\s*lesson overview:?\s*$", re.I | re.M)
WALT = re.compile(r"we are learning|i can\b|learning intention|success criteria|you will show your understanding|ākonga will|akonga will", re.I)
HEAD = re.compile(r"\[\s*(h1|h2|h3|title bar|lesson content)\b", re.I)


def wt_text(code):
    d = _corpus.mdir(HUMAN, code)
    if not os.path.isdir(d):
        return None
    best = None
    for f in sorted(os.listdir(d)):
        if f.endswith("_parsed.txt") and "writer" in f.lower():
            t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
            if best is None or len(t) > len(best):
                best = t
    if best is None:
        for f in sorted(os.listdir(d)):
            if f.endswith("_parsed.txt"):
                t = open(os.path.join(d, f), encoding="utf-8", errors="replace").read()
                if "[lesson" in t.lower():
                    best = t
                    break
    return RED.sub("", best) if best else None


def lesson_regions(txt):
    """ordered list of (lesson_number_in_tag, region_text)"""
    ms = list(LESSON.finditer(txt))
    out = []
    for i, m in enumerate(ms):
        end = ms[i + 1].start() if i + 1 < len(ms) else len(txt)
        out.append((int(m.group(1)) if m.group(1) else i + 1, txt[m.end():end]))
    return out


def lo_signal(region):
    head = region[:6000]
    tag = bool(LO_TAG.search(head))
    bare = bool(LO_BARE.search(head))
    hm = HEAD.search(region)
    pre = region[:hm.start()] if hm else region[:3000]
    walt = bool(WALT.search(pre))
    return tag, bare, walt


def page_lesson(fn):
    m = re.search(r"_(\d+)_(\d+)\.html$", fn)
    return (int(m.group(1)), int(m.group(2))) if m else None


def has_menu(path):
    h = open(path, encoding="utf-8", errors="replace").read()
    h = re.sub(r"<!--.*?-->", "", h, flags=re.S)   # PES1003: the gold's lesson menu is COMMENTED OUT boilerplate
    return ('id="module-head-buttons"' in h), ('id="module-menu-content"' in h)


meta = load_meta()
mods = _corpus.gate_mods(CLAUDE)
rows = []
for code in mods:
    txt = wt_text(code)
    regions = lesson_regions(txt) if txt else []
    reg = (REG.get("series") or {}).get(code) or {}
    m = meta.get(code, {}) if isinstance(meta, dict) else {}
    for _n, cp, hp in pairs(code):
        cfn, hfn = os.path.basename(cp), os.path.basename(hp)
        if SKIP_PAGE.search(cfn) or SKIP_PAGE.search(hfn):
            continue
        pl = page_lesson(cfn)
        if not pl or pl[0] == 0:
            continue
        n, sub = pl
        region = None
        if regions:
            if n - 1 < len(regions):
                region = regions[n - 1][1]
            else:
                for num, r in regions:
                    if num == n:
                        region = r
        tag, bare, walt = lo_signal(region) if region is not None else (None, None, None)
        gb, gc = has_menu(hp)
        cb, cc = has_menu(cp)
        rows.append(dict(code=code, cpage=cfn, hpage=hfn, lesson=n, sub=sub,
                         template=m.get("template_type") or m.get("template") or "?",
                         subject=m.get("subject") or "?", series=m.get("series") or "?",
                         gold_menu=gb, gold_content=gc, claude_menu=cb, claude_content=cc,
                         wt_region=region is not None, lo_tag=tag, lo_bare=bare, walt=walt,
                         reg_lesson=reg.get("lesson") if reg else "none-entry"))

json.dump(rows, open(os.path.join(BASE, "_r363_lessonmenu.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
L = []


def P(*a):
    s = " ".join(str(x) for x in a)
    L.append(s)
    print(s)


def sig(r):
    return "LO" if (r["lo_tag"] or r["lo_bare"] or r["walt"]) else ("noWT" if not r["wt_region"] else "noLO")


P(f"lesson pairs {len(rows)} / modules {len(set(r['code'] for r in rows))}")
c = Counter((r["gold_menu"], r["claude_menu"], sig(r)) for r in rows)
P("\n(gold_menu, claude_menu, WT signal) -> pages")
for k, v in sorted(c.items(), key=lambda kv: -kv[1]):
    P(f"  gold={k[0]!s:5} claude={k[1]!s:5} wt={k[2]:5} : {v}")
P("\nGOLD menu vs WT signal (the rule's population):")
for s in ("LO", "noLO", "noWT"):
    sub = [r for r in rows if sig(r) == s]
    g = sum(r["gold_menu"] for r in sub)
    P(f"  wt={s:5}: pages {len(sub)}, gold has menu {g} ({g / len(sub):.2f})" if sub else f"  wt={s}: 0")
P("\nCLAUDE menu vs WT signal:")
for s in ("LO", "noLO", "noWT"):
    sub = [r for r in rows if sig(r) == s]
    g = sum(r["claude_menu"] for r in sub)
    P(f"  wt={s:5}: pages {len(sub)}, claude has menu {g} ({g / len(sub):.2f})" if sub else f"  wt={s}: 0")
P("\nLO pages by group: n / gold menu share / claude menu share / gold-yes-claude-no (modules) / claude-yes-gold-no")
for key in ("template", "subject"):
    grp = defaultdict(list)
    for r in rows:
        if sig(r) == "LO":
            grp[r[key]].append(r)
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        miss = [r for r in v if r["gold_menu"] and not r["claude_menu"]]
        extra = [r for r in v if r["claude_menu"] and not r["gold_menu"]]
        P(f"  {key}={k}: n={len(v)} gold={sum(r['gold_menu'] for r in v) / len(v):.2f} claude={sum(r['claude_menu'] for r in v) / len(v):.2f} miss={len(miss)}p/{len(set(r['code'] for r in miss))}m extra={len(extra)}p/{len(set(r['code'] for r in extra))}m")
P("\nnoLO pages by group: n / gold menu share / claude menu share")
for key in ("template",):
    grp = defaultdict(list)
    for r in rows:
        if sig(r) == "noLO":
            grp[r[key]].append(r)
    for k, v in sorted(grp.items(), key=lambda kv: -len(kv[1])):
        P(f"  {key}={k}: n={len(v)} gold={sum(r['gold_menu'] for r in v) / len(v):.2f} claude={sum(r['claude_menu'] for r in v) / len(v):.2f}")
P("\nTHE MISS CLASS (gold menu, Claude none, WT LO) by module -> registry lesson value:")
miss = [r for r in rows if r["gold_menu"] and not r["claude_menu"] and sig(r) == "LO"]
bym = defaultdict(list)
for r in miss:
    bym[r["code"]].append(r)
for k, v in sorted(bym.items()):
    P(f"  {k}: {len(v)} pages (lessons {sorted(set(r['lesson'] for r in v))}) reg.lesson={v[0]['reg_lesson']} tmpl={v[0]['template']} subj={v[0]['subject']} sig={Counter((r['lo_tag'], r['lo_bare'], r['walt']) for r in v)}")
P(f"  TOTAL {len(miss)} pages / {len(bym)} modules")
P("\nTHE EXTRA CLASS (Claude menu, gold none, WT LO) by module:")
extra = [r for r in rows if r["claude_menu"] and not r["gold_menu"] and sig(r) == "LO"]
bym2 = defaultdict(list)
for r in extra:
    bym2[r["code"]].append(r)
for k, v in sorted(bym2.items()):
    P(f"  {k}: {len(v)} pages (lessons {sorted(set(r['lesson'] for r in v))}) reg.lesson={v[0]['reg_lesson']} tmpl={v[0]['template']}")
P(f"  TOTAL {len(extra)} pages / {len(bym2)} modules")
P("\nGOLD menu WITHOUT any WT signal (not derivable) by module:")
nd = [r for r in rows if r["gold_menu"] and not r["claude_menu"] and sig(r) != "LO"]
bym3 = defaultdict(list)
for r in nd:
    bym3[r["code"]].append(r)
for k, v in sorted(bym3.items()):
    P(f"  {k}: {len(v)} pages sig={Counter(sig(r) for r in v)} reg.lesson={v[0]['reg_lesson']}")
P(f"  TOTAL {len(nd)} pages / {len(bym3)} modules")
P("\nregistry lesson value vs gold menu on LO pages:")
c2 = Counter((str(r["reg_lesson"]), r["gold_menu"]) for r in rows if sig(r) == "LO")
for k, v in sorted(c2.items()):
    P(f"  reg={k[0]:12} gold_menu={k[1]!s:5}: {v}")
P("\nregistry lesson value vs CLAUDE menu on LO pages:")
c3 = Counter((str(r["reg_lesson"]), r["claude_menu"]) for r in rows if sig(r) == "LO")
for k, v in sorted(c3.items()):
    P(f"  reg={k[0]:12} claude_menu={k[1]!s:5}: {v}")
open(os.path.join(BASE, "_r363_lessonmenu.log"), "w", encoding="utf-8").write("\n".join(L) + "\n")
