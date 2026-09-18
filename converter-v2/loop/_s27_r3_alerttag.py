#!/usr/bin/env python3
"""Session 27 Round 3 candidate — THE CALLOUT BOX'S CLASS BY WRITER TAG. Every paired (gold box ↔ Claude box, same opening words)
callout on the gate pairs, with the WRITER'S TAG behind it (the bracket on the WT line holding the box's first words, or the
nearest tag line above): tally writer-tag × gold class × Claude class, per template/subject group — which tag-in-group ships
the wrong class (a swap the gold makes ≥ 0.60 of the time at ≥ 20 pages).  wsl: python3 _s27_r3_alerttag.py → _s27_r3_alerttag.out"""
import os, sys, re
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
OUTPUTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
HUMAN = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/01-Finalized_Modules_'
for p in (OUTPUTS, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, OUTPUTS)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
from collections import Counter, defaultdict
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
BOX = re.compile(r'<div class="((?:[^"]*\b(?:alert|important|alertActivity)\b[^"]*))"([^>]*)>', re.I)
DIVS = re.compile(r"<div\b|</div>")
TAGLINE = re.compile(r"🔴\[RED TEXT\]\s*\[([^\]]*)\]")
def fold(t): return re.sub(r"\W+", " ", t.lower()).strip()
def boxes(src):
    out = []
    for m in BOX.finditer(src):
        cls = " ".join(sorted(m.group(1).split()))
        if "cultural" in cls or "whakatauki" in cls: continue
        depth = 0; end = len(src)
        for mm in DIVS.finditer(src, m.start()):
            depth += -1 if mm.group(0) == "</div>" else 1
            if depth == 0: end = mm.end(); break
        inner = re.sub(r"<p class=\"cv2-note\"[^>]*>.*?</p>", " ", src[m.end():end], flags=re.S)
        inner = re.sub(r"<[^>]+>", " ", inner)
        words = fold(inner).split()
        if len(words) < 3: continue
        out.append((cls, " ".join(words[:8]), " ".join(words[:5])))
    return out
def wt_lines(code):
    d = _corpus.mdir(HUMAN, code)
    fs = sorted(f for f in os.listdir(d) if f.endswith("_parsed.txt"))
    pref = [f for f in fs if "writers template" in f.lower()] or fs
    if not pref: return []
    return open(os.path.join(d, pref[0]), encoding="utf-8", errors="replace").read().split("\n")
def writer_tag(lines, folded_lines, key5):
    """the bracket on the line holding key5 (its own tag) else the nearest tag line above (≤ 3 non-blank lines)"""
    for i, fl in enumerate(folded_lines):
        if key5 and key5 in fl:
            m = TAGLINE.search(lines[i])
            if m: return norm_tag(m.group(1))
            k = i - 1; seen = 0
            while k >= 0 and seen < 3:
                if lines[k].strip():
                    seen += 1
                    m = TAGLINE.search(lines[k])
                    if m: return norm_tag(m.group(1))
                k -= 1
            return "(no tag)"
    return "(not in WT)"
def norm_tag(b):
    b = re.sub(r"\s+", " ", b.strip().lower())
    b = re.sub(r"\d+[a-z]?\b", "N", b)
    b = re.sub(r"[.:]+$", "", b)
    return b[:40]
T = Counter(); TG = defaultdict(Counter); pages = defaultdict(set); mods = defaultdict(set); EX = defaultdict(list)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    lines = wt_lines(code); folded = [fold(l) for l in lines]
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        if re.search(r'acks|acknowledge|glossary', os.path.basename(cp), re.I): continue
        try:
            gb = boxes(body_source(open(hp, encoding="utf-8", errors="replace").read()))
            cb = boxes(body_source(open(cp, encoding="utf-8", errors="replace").read()))
        except Exception: continue
        cidx = {}
        for k, w, k5 in cb: cidx.setdefault(w, k)
        for k, w, k5 in gb:
            if w not in cidx: continue
            ck = cidx[w]
            tag = writer_tag(lines, folded, k5)
            key = (tag, k, ck)
            T[key] += 1; TG[g][key] += 1; pages[key].add(hp); mods[key].add(code)
            if k != ck and len(EX[key]) < 2: EX[key].append(f"{code} {os.path.basename(hp)} «{w[:40]}»")
out = []
def P(s=""): out.append(s); print(s)
P("==== paired boxes by WRITER TAG → gold class → claude class (top 40; <<< = a class swap) ====")
for (tag, gk, ck), v in T.most_common(40):
    P(f"   {v:5d}  pages {len(pages[(tag, gk, ck)]):4d} mods {len(mods[(tag, gk, ck)]):3d}   [{tag:32s}] gold {gk:22s} → claude {ck}{'   <<<' if gk != ck else ''}")
P()
P("==== per group: for each writer tag with a SWAP, the gold's class shares among that tag's paired boxes in the group (n ≥ 10) ====")
for g, c in sorted(TG.items(), key=lambda kv: -sum(kv[1].values())):
    bytag = defaultdict(Counter)
    for (tag, gk, ck), v in c.items(): bytag[tag][(gk, ck)] += v
    for tag, cc in bytag.items():
        t = sum(cc.values())
        if t < 10: continue
        swaps = sum(v for (gk, ck), v in cc.items() if gk != ck)
        if swaps / t < 0.3: continue
        gold = Counter()
        for (gk, ck), v in cc.items(): gold[gk] += v
        P(f"   {g:42s} [{tag:28s}] n={t:3d} swap {swaps/t:.2f}  gold: " + "  ".join(f"{k} {v} ({v/t:.2f})" for k, v in gold.most_common(4)) + "  | claude: " + "  ".join(f"{ck} {v}" for ck, v in Counter({ck: v for (gk, ck), v in cc.items()}).most_common(3)))
P()
P("==== examples of the swaps ====")
for key, ex in EX.items():
    if T[key] >= 8:
        for e in ex: P(f"   [{key[0]}] gold {key[1]} → claude {key[2]}: {e}")
open(os.path.join(OUTPUTS, "_s27_r3_alerttag.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
