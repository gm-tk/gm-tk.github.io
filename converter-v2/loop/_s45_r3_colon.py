#!/usr/bin/env python3
"""Session 45 Round 3 — the COLON-inline hover markers (no named term) the gold builds and Claude does not: what did Claude do with each?
LEAKED = the definition text is visible on a Claude page (outside any info= attribute — a literal marker or loose text); DROPPED = the
definition is nowhere on Claude's pages. Also the marker's raw form (head word, def length, split red runs, table cell, bold anchor,
what follows the ']'). WSL, from outputs/: python3 _s45_r3_colon.py > _s45_r3_colon.log"""
import os, re, sys, glob, io, collections, html as H
sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "reference", "tests"))
import _corpus
ROOT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
GOLD = os.path.join(ROOT, "01-Finalized_Modules_"); CL = os.path.join(ROOT, "01-Claude_Modules_")
RED = re.compile(r"🔴\[RED TEXT\]|\[/RED TEXT\]🔴")
def n(t): return re.sub(r"[^a-z0-9ā-ž ]+", "", re.sub(r"\s+", " ", H.unescape(t).lower())).strip()
def nz(t): return n(t).replace(" ", "")
HEAD = re.compile(r"\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\b", re.I)
FOR = re.compile(r"^\[\s*(?:hover(?:\s*info(?:rmation)?)?|roll\s*-?\s*over|rollover|mouse\s*-?\s*over|mouseover)\s*(?:-?\s*over)?\s*(?:definition|def|text|info)?\s*(?:for|of|on)\s+([^:\]]{1,40}?)\s*:", re.I)
QUOTED = re.compile(r"^\[[^\]:]*?['‘\"]([^'’\"‘\]]+)['’\"][^:\]]*:", re.I)
COLON = re.compile(r"^\[([^\]:]*):\s*([^\]]+)")
def pages(d):
    out = []
    for p in glob.glob(os.path.join(d, "*.html")):
        s = io.open(p, encoding="utf-8", errors="replace").read()
        infos = [nz(m) for m in re.findall(r'info="([^"]*)"', s)]
        vis = nz(re.sub(r"<[^>]+>", " ", re.sub(r'info="[^"]*"', "", s)))
        out.append((os.path.basename(p), infos, vis))
    return out
res = collections.Counter(); per = collections.defaultdict(collections.Counter); ex = collections.defaultdict(list)
feat = collections.defaultdict(collections.Counter)
for code in _corpus.gate_mods(GOLD):
    gd = _corpus.mdir(GOLD, code); cd = _corpus.mdir(CL, code)
    wts = [p for p in glob.glob(os.path.join(gd, "*_parsed.txt")) if "writers template" in os.path.basename(p).lower()]
    if not wts or not os.path.isdir(cd): continue
    lines = []
    for w in wts: lines += io.open(w, encoding="utf-8", errors="replace").read().split("\n")
    gp = pages(gd); cp = pages(cd)
    gi = [x for _, i, _ in gp for x in i]
    for ln in lines:
        raw = RED.sub("", ln)
        for m0 in HEAD.finditer(raw):
            mk = re.sub(r"\s+", " ", raw[m0.start():]).strip()
            pre = raw[:m0.start()].strip()
            if not pre or re.search(r"\btrigger\b", mk[:40], re.I) or FOR.match(mk) or QUOTED.match(mk): continue
            mc = COLON.match(mk)
            if not mc: continue
            d = mc.group(2); dk = nz(d)[:22]
            if not dk or not any(dk in x for x in gi): continue            # the gold builds it
            if any(dk in x for _, i, _ in cp for x in i): continue          # Claude builds it too
            where = "LEAKED" if any(dk in v for _, _, v in cp) else "DROPPED"
            if where == "LEAKED":
                # which container shows it: a converter note, a hand-off box, or plain page prose
                probe = re.escape(re.sub(r"\s+", " ", d.strip())[:18]).replace(r"\ ", r"\s+")
                ctx = "?"
                for p in glob.glob(os.path.join(cd, "*.html")):
                    s = io.open(p, encoding="utf-8", errors="replace").read()
                    mm = re.search(probe, s)
                    if not mm: continue
                    before = s[:mm.start()]
                    line = before[before.rfind("\n") + 1:]
                    ho = before.count('class="cv2-interactive') - before.count("<!--cv2-end")
                    ctx = "note" if "cv2-note" in line else ("handoff" if before.rfind('class="cv2-int-raw"') > before.rfind('<div class="row">') else "prose")
                    break
                where = "LEAKED-" + ctx
            f = []
            if "║" in raw: f.append("table-cell")
            if len(RED.findall(ln)) > 4: f.append("split-runs")
            if re.search(r"\*\*[^*]+\*\*\s*$", pre): f.append("bold-anchor")
            if re.search(r"[.!?:;]\s*$", pre): f.append("pre-ends-sentence")
            if "]" not in mk: f.append("unclosed")
            f.append("head=" + mc.group(1).strip().lower()[:24])
            res[where] += 1; per[where][code] += 1
            for x in f: feat[where][x] += 1
            if len(ex[where]) < 14: ex[where].append(f"{code} «{pre[-40:]} {mk[:70]}»")
for w in res:
    print(f"{w}: {res[w]} — modules {dict(per[w].most_common(25))}")
    print(f"   features: {dict(feat[w].most_common(20))}")
    for e in ex[w]: print("     ", e)
