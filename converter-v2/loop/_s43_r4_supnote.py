#!/usr/bin/env python3
"""Session 43 Round 4 PICK — THE UNBRACKETED SUPERVISOR NOTE. Every Writers Template line that names a supervisor note WITHOUT the
bracketed tag ("🔴 Supervisor note: 🔴" alone, then red content lines; "🔴 Supervisor note - <content> 🔴"; "Supervisor support …"),
classified by FORM, with the note's CONTENT (the rest of the line, or the following red / bullet lines up to the next tag or blank
pair) looked up in (a) Claude's pages — inside a `row supervisor` box / as a red cv2-note / elsewhere / ABSENT — and (b) the gold's
pages — inside a supervisor box (`supervisor` class) / elsewhere / absent. The bracketed `[Supervisor note]` form is counted too, as
the control. Run under WSL from CONVERTER_V2/reference/tests: python3 ../../outputs/_s43_r4_supnote.py > ../../outputs/_s43_r4_supnote.log"""
import os, re, sys, glob, html, collections
sys.path.insert(0, os.getcwd())
import _corpus
from anchor_compare import CLAUDE, HUMAN

RED = re.compile(r"🔴\[RED TEXT\](.*?)\[/RED TEXT\]🔴", re.S)
def norm(s):
    s = html.unescape(s).lower()
    s = re.sub(r"🔴|\[/?red text\]", " ", s)
    s = re.sub(r"\[[^\]]{0,60}\]", " ", s)
    s = re.sub(r"[‘’“”'\"`*_]", "", s)
    s = re.sub(r"[^0-9a-zāēīōū]+", " ", s)
    return re.sub(r"\s+", " ", s).strip()
def regions(p):
    """(all visible text, text inside supervisor boxes, text inside red cv2-notes) of one page, normalised."""
    s = open(p, encoding="utf-8", errors="replace").read()
    s = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", s, flags=re.S | re.I)
    s = re.sub(r"<!--.*?-->", " ", s, flags=re.S)
    sup = []
    for m in re.finditer(r'<div class="[^"]*\bsupervisor\b[^"]*"', s):
        chunk = s[m.start(): m.start() + 6000]
        sup.append(re.sub(r"<[^>]+>", " ", chunk))
    notes = [re.sub(r"<[^>]+>", " ", m.group(1)) for m in re.finditer(r'<p class="cv2-note"[^>]*>(.*?)</p>', s, flags=re.S)]
    return norm(re.sub(r"<[^>]+>", " ", s)), norm(" ".join(sup)), norm(" ".join(notes))
def form_of(line):
    l = line.strip()
    if re.search(r"\[\s*supervisor\s*note\s*:?\s*\]", l, re.I): return "bracketed [Supervisor note]"
    if re.search(r"\[\s*$|^\s*🔴\[RED TEXT\]\s*\[\s*\[/RED TEXT\]", l) and re.search(r"supervisor\s*note\s*:?\s*\]", l, re.I): return "split bracket [ + Supervisor note]"
    reds = RED.findall(l)
    if reds and re.fullmatch(r"\s*supervisor\s*(?:note|notes|support)?\s*[:\-–]?\s*", reds[0], re.I) and not norm(RED.sub(" ", l)):
        return "LABEL line alone (red 'Supervisor note:')"
    if re.search(r"supervisor\s*(?:note|notes)\s*[\-–:]", l, re.I): return "LABEL + content on one line (unbracketed)"
    return None
rows = []; agg = collections.Counter(); mods = collections.defaultdict(set); ex = collections.defaultdict(list)
for code in sorted(_corpus.gate_mods(CLAUDE)):
    hd, cd = _corpus.mdir(HUMAN, code), _corpus.mdir(CLAUDE, code)
    if not (os.path.isdir(hd) and os.path.isdir(cd)): continue
    wts = [f for f in glob.glob(os.path.join(hd, "*_parsed.txt")) if "media list_parsed" not in f.lower() or "writers template" in f.lower()]
    if not wts: continue
    L = []
    for f in wts: L += open(f, encoding="utf-8", errors="replace").read().splitlines()
    C = [regions(p) for p in glob.glob(os.path.join(cd, "*.html"))]
    G = [regions(p) for p in glob.glob(os.path.join(hd, "*.html"))]
    for i, line in enumerate(L):
        if "supervisor" not in line.lower(): continue
        form = form_of(line)
        if not form: continue
        if form.startswith("LABEL line alone"):
            content = []
            for j in range(i + 1, min(len(L), i + 12)):
                t = L[j].strip()
                if not t: continue
                if re.match(r"^\s*(?:•\s*)?🔴\[RED TEXT\]\s*\[", t) or "┌" in t: break      # the next tag / a table ends it
                content.append(t)
                if len(content) >= 4: break
            text = norm(" ".join(content))
        else:
            text = norm(re.sub(r"supervisor\s*(?:note|notes|support)?\s*[:\-–]?", " ", RED.sub(lambda m: m.group(1), line), count=1, flags=re.I))
        w = text.split()
        if len(w) < 4: continue
        probe = " ".join(w[:8])
        def where(P):
            if any(probe in s for _, s, _ in P): return "SUPERVISOR BOX"
            if any(probe in n for _, _, n in P): return "red note"
            if any(probe in a for a, _, _ in P): return "elsewhere"
            return "ABSENT"
        c, g = where(C), where(G)
        k = (form, c, g); agg[k] += 1; mods[k].add(code)
        if len(ex[k]) < 3: ex[k].append(f"{code}: {' '.join(w[:12])}")
print("form | Claude | gold | notes | modules")
for k, n in sorted(agg.items(), key=lambda kv: (kv[0][0], -kv[1])):
    print(f"{k[0]:44s} | {k[1]:14s} | {k[2]:14s} | {n:4d} | {len(mods[k]):3d}  e.g. {' ;; '.join(ex[k])[:220]}")
tot = collections.Counter()
for k, n in agg.items(): tot[k[0]] += n
print("\nby form:", dict(tot))
