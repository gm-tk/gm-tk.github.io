#!/usr/bin/env python3
"""Session 27 Round 4 — THE DEVELOPER'S <br> JOIN: the gold joins two consecutive writer paragraphs into ONE <p> with a
<br> (577 p-sites where Claude ships two <p>). Direction B — for every pair of CONSECUTIVE text-only <p> siblings on
Claude's page, how does the gold render them: joined by <br> in one element / kept as consecutive elements / other;
by FEATURES of the pair (words in A, words in B, A's terminal punctuation, an equation-like A, a colon-ended A) and by
subject — is there a discriminator that predicts the join at ≥ 0.60?  wsl: python3 _s27_r4_brjoin.py"""
import os, sys, re
from collections import Counter, defaultdict
HERE = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/outputs'
TESTS = '/mnt/c/Users/Gavin/TeKura/FINAL_MODULE_DATA/CONVERTER_V2/reference/tests'
for p in (HERE, TESTS):
    if p in sys.path: sys.path.remove(p)
sys.path.insert(0, TESTS); sys.path.insert(1, HERE)
from _discrepancy_audit import pairs
from _measure_ceiling import load_meta
from _structural_skeleton import body_source
import _corpus
from anchor_compare import CLAUDE
meta = load_meta()
fam = {}
for tf in _corpus.TEMPLATE_DIRS:
    d = os.path.join(CLAUDE, tf)
    if os.path.isdir(d):
        for m in os.listdir(d): fam[m] = tf
EL = re.compile(r'<(p|li|td|th|h[1-6]|div)\b([^>]*)>([\s\S]*?)</\1>', re.I)
PEL = re.compile(r'<p\b([^>]*)>([\s\S]*?)</p>', re.I)
BR = re.compile(r'<br\s*/?>', re.I)
def strip(s): return re.sub(r"<[^>]+>", " ", s)
def fold(s): return re.sub(r"[^a-z0-9āēīōū ]+", "", strip(s).lower()).strip()
def feats(a_raw, b_raw):
    a = strip(a_raw).strip(); b = strip(b_raw).strip()
    wa = len(a.split()); wb = len(b.split())
    endp = "punct" if re.search(r"[.!?]$", a) else ("colon" if a.endswith(":") else "none")
    eq = "eq" if re.search(r"[=×÷+\-−]\s*\d|\d\s*[=×÷+\-−]|\d+\s*[/%]", a) else "noeq"
    wbA = "A≤4" if wa <= 4 else ("A≤10" if wa <= 10 else "A>10")
    wbB = "B≤10" if wb <= 10 else "B>10"
    return wbA, wbB, endp, eq
RES = defaultdict(Counter); BYG = defaultdict(Counter); EX = defaultdict(list); TOT = Counter(); ENG = defaultdict(Counter); ENGP = defaultdict(set); ENGM = defaultdict(set); PREF = defaultdict(Counter)
for code in sorted(fam):
    tf = fam[code]; subj = (meta.get(code, {}) or {}).get("subject") or "None"; g = tf + "/" + subj
    for n, cp, hp in pairs(code):
        if re.search(r'acks|acknowledge|glossary|references', os.path.basename(hp), re.I): continue
        gh = body_source(open(hp, encoding="utf-8", errors="replace").read()); ch = body_source(open(cp, encoding="utf-8", errors="replace").read())
        # gold elements folded, with a br flag
        gels = []
        for m in EL.finditer(gh):
            inner = m.group(3)
            if re.search(r"<(p|li|div|td)\b", inner): continue   # only leaf-ish elements
            gels.append((fold(inner), bool(BR.search(inner))))
        # Claude consecutive <p> pairs (text-only, no nested block, not notes)
        cps = []
        for m in PEL.finditer(ch):
            attrs = m.group(1); inner = m.group(2)
            if "cv2-" in attrs: cps.append(None); continue
            if re.search(r"<(div|table|ul|ol|img|iframe)\b", inner): cps.append(None); continue
            cps.append((m.start(), inner))
        for i in range(len(cps) - 1):
            if cps[i] is None or cps[i + 1] is None: continue
            (sa, ia), (sb, ib) = cps[i], cps[i + 1]
            gap = ch[sa:sb]
            if re.search(r"<(div|ul|ol|table|h[1-6])\b|</div>", gap[gap.find("</p>"):]): continue   # not siblings
            A = fold(ia); B = fold(ib)
            if len(A) < 8 or len(B) < 8: continue
            a20 = A[-24:].strip(); b20 = B[:24].strip()
            verdict = "absent"
            for k, (t, hasbr) in enumerate(gels):
                ia_ = t.find(a20)
                if ia_ < 0: continue
                if t.find(b20, ia_) >= 0: verdict = "joined-br" if hasbr else "joined-nobr"; break
                if k + 1 < len(gels) and gels[k + 1][0][:len(b20) + 40].find(b20) >= 0: verdict = "kept-split"; break
                verdict = "A-only"
            f = feats(ia, ib)
            RES[f][verdict] += 1; BYG[g][verdict] += 1; TOT[verdict] += 1
            pref = re.match(r"[A-Z]+", code).group(0); PREF[pref][verdict] += 1
            if subj == "1-10 English":
                ENG[f][verdict] += 1
                if verdict == "joined-br": ENGP[f].add(hp); ENGM[f].add(code)
            if verdict == "joined-br" and len(EX[f]) < 2: EX[f].append(f"{code} {os.path.basename(hp)} «{strip(ia).strip()[:36]}» ¦ «{strip(ib).strip()[:36]}»")
out = []
def P(s=""): out.append(s); print(s)
P("consecutive Claude <p> sibling pairs: " + "  ".join(f"{k} {v}" for k, v in TOT.most_common()))
dec = lambda c: c["joined-br"] + c["kept-split"] + c["joined-nobr"]
P("==== by feature (decided ≥ 40): joined-br share ====")
rows = sorted(RES.items(), key=lambda kv: -dec(kv[1]))
for f, c in rows:
    d = dec(c)
    if d < 40: continue
    P(f"   {'/'.join(f):26s} decided {d:5d}  joined-br {c['joined-br']:4d} ({c['joined-br']/d:.2f})  kept-split {c['kept-split']:5d}  joined-nobr {c['joined-nobr']:3d}  absent {c['absent']} A-only {c['A-only']}")
P()
P("==== by group (decided ≥ 30): joined-br share ====")
for g, c in sorted(BYG.items(), key=lambda kv: -dec(kv[1])):
    d = dec(c)
    if d < 30: continue
    P(f"   {g:42s} decided {d:5d}  joined-br {c['joined-br']:4d} ({c['joined-br']/d:.2f})  kept-split {c['kept-split']:5d}  nobr {c['joined-nobr']}")
P()
P("==== 1-10 English by feature ====")
for f, c in sorted(ENG.items(), key=lambda kv: -dec(kv[1])):
    d = dec(c)
    if d < 8: continue
    P(f"   {'/'.join(f):26s} decided {d:4d}  joined-br {c['joined-br']:4d} ({c['joined-br']/d:.2f})  kept-split {c['kept-split']:4d}  nobr {c['joined-nobr']}  br-pages {len(ENGP[f])} mods {len(ENGM[f])} {sorted(ENGM[f])[:6]}")
P("==== by prefix (decided ≥ 20) ====")
for pf, c in sorted(PREF.items(), key=lambda kv: -dec(kv[1])):
    d = dec(c)
    if d < 20: continue
    P(f"   {pf:8s} decided {d:4d}  joined-br {c['joined-br']:4d} ({c['joined-br']/d:.2f})  kept-split {c['kept-split']:4d}  nobr {c['joined-nobr']}")
P()
for f, ex in EX.items():
    for e in ex: P(f"   {'/'.join(f)}: {e}")
open(os.path.join(HERE, "_s27_r4_brjoin.out"), "w", encoding="utf-8").write("\n".join(out) + "\n")
